#!/usr/bin/env python3
"""
Project generation API routes
"""

from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel

from ...core.database import get_db
from ...services.project_service import ProjectService
from ...services.agentic_search_service import AgenticSearchService
from ...core.engine import ConsciousnessEngine

router = APIRouter()


class ProjectGenerationRequest(BaseModel):
    """Request model for project generation"""
    user_id: str
    project_type: str = "web_app"
    requirements: Optional[str] = None
    async_processing: bool = False


class AgenticSearchRequest(BaseModel):
    """Request model for agentic search proposals"""
    context_type: str = "project_generation"  # 'project_generation', 'self_improvement', 'system_analysis'
    project_type: Optional[str] = None
    language: Optional[str] = None
    user_context: Optional[dict] = None
    system_metrics: Optional[dict] = None


@router.post("/generate", summary="Generate AI Project", description="Generate AI project using consciousness engine (preserved feature)")
async def generate_project(
    request: ProjectGenerationRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Generate AI project (preserved from original consciousness_web_builder.py)"""
    try:
        engine = ConsciousnessEngine()
        project_service = ProjectService(db, engine)

        if request.async_processing:
            # Add to background tasks for async processing
            background_tasks.add_task(
                project_service.generate_project,
                request.user_id,
                request.project_type,
                request.requirements or ""
            )

            return {
                "message": "Project generation started asynchronously",
                "task_id": f"task_{request.user_id}_{request.project_type}",
                "status": "processing"
            }
        else:
            # Generate synchronously
            result = await project_service.generate_project(
                request.user_id,
                request.project_type,
                request.requirements or ""
            )

            return {
                "project": result,
                "message": "AI-generated project created successfully"
            }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Project generation failed: {str(e)}")


@router.get("/", summary="List Projects", description="Get paginated list of projects with filtering")
async def get_projects(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(50, ge=1, le=100, description="Items per page"),
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    project_type: Optional[str] = Query(None, description="Filter by project type"),
    status: Optional[str] = Query(None, description="Filter by status"),
    db: Session = Depends(get_db)
):
    """Get paginated list of projects with filtering"""
    try:
        engine = ConsciousnessEngine()
        project_service = ProjectService(db, engine)

        result = project_service.get_projects(
            page=page,
            limit=limit,
            user_id=user_id,
            project_type=project_type,
            status=status
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve projects: {str(e)}")


@router.get("/{project_id}", summary="Get Project", description="Get detailed project information")
async def get_project(project_id: str, db: Session = Depends(get_db)):
    """Get detailed project information by ID"""
    try:
        engine = ConsciousnessEngine()
        project_service = ProjectService(db, engine)

        project = project_service.get_project(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        return project
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve project: {str(e)}")


@router.delete("/{project_id}", summary="Delete Project", description="Delete a project")
async def delete_project(project_id: str, db: Session = Depends(get_db)):
    """Delete a project by ID"""
    try:
        engine = ConsciousnessEngine()
        project_service = ProjectService(db, engine)

        success = project_service.delete_project(project_id)
        if not success:
            raise HTTPException(status_code=404, detail="Project not found")

        return {"message": "Project deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete project: {str(e)}")


@router.post("/{project_id}/regenerate", summary="Regenerate Project", description="Regenerate project with new requirements")
async def regenerate_project(
    project_id: str,
    requirements: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Regenerate an existing project with new requirements"""
    try:
        engine = ConsciousnessEngine()
        project_service = ProjectService(db, engine)

        result = await project_service.regenerate_project(project_id, requirements or "")

        return {
            "project": result,
            "message": "Project regenerated successfully"
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Project regeneration failed: {str(e)}")


@router.get("/statistics/overview", summary="Project Statistics", description="Get comprehensive project statistics")
async def get_project_statistics(db: Session = Depends(get_db)):
    """Get comprehensive project statistics"""
    try:
        engine = ConsciousnessEngine()
        project_service = ProjectService(db, engine)

        stats = project_service.get_project_statistics()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get statistics: {str(e)}")


@router.get("/types/available", summary="Available Project Types", description="Get list of available project types")
async def get_available_project_types():
    """Get list of available project types"""
    return {
        "project_types": [
            {
                "type": "web_app",
                "name": "Web Application",
                "description": "Modern React/JavaScript web application",
                "languages": ["javascript", "typescript"],
                "complexity": "medium"
            },
            {
                "type": "api",
                "name": "REST API",
                "description": "RESTful API with consciousness data processing",
                "languages": ["python", "javascript"],
                "complexity": "medium"
            },
            {
                "type": "agent",
                "name": "AI Agent",
                "description": "Self-learning AI agent with consciousness integration",
                "languages": ["python"],
                "complexity": "high"
            }
        ]
    }


@router.post("/agentic-search/propose", summary="🧬 Propose Agentic Searches", description="Generate contextual search proposals for project generation or system improvement")
async def propose_agentic_searches(request: AgenticSearchRequest):
    """🧬 Generate agentic search proposals based on context"""
    try:
        search_service = AgenticSearchService()
        proposals = []

        if request.context_type == "project_generation":
            if not request.project_type or not request.language or not request.user_context:
                raise HTTPException(
                    status_code=400,
                    detail="project_type, language, and user_context required for project_generation"
                )
            proposals = await search_service.propose_searches_for_project(
                project_type=request.project_type,
                language=request.language,
                user_context=request.user_context
            )

        elif request.context_type == "self_improvement":
            if not request.system_metrics:
                raise HTTPException(
                    status_code=400,
                    detail="system_metrics required for self_improvement"
                )
            proposals = await search_service.propose_searches_for_self_improvement(
                current_metrics=request.system_metrics
            )

        elif request.context_type == "system_analysis":
            if not request.system_metrics:
                raise HTTPException(
                    status_code=400,
                    detail="system_metrics required for system_analysis"
                )
            proposals = await search_service.propose_searches_for_system_analysis(
                system_state=request.system_metrics
            )

        else:
            raise HTTPException(status_code=400, detail=f"Unknown context_type: {request.context_type}")

        return {
            "search_proposals": [p.to_dict() for p in proposals],
            "total_proposals": len(proposals),
            "context_type": request.context_type,
            "message": f"Generated {len(proposals)} agentic search proposals for {request.context_type}"
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agentic search proposal failed: {str(e)}")


@router.get("/agentic-search/statistics", summary="🧬 Agentic Search Statistics", description="Get statistics about agentic search activities")
async def get_agentic_search_statistics():
    """🧬 Get comprehensive statistics about agentic search operations"""
    try:
        search_service = AgenticSearchService()
        stats = search_service.get_search_statistics()

        return {
            "statistics": stats,
            "message": "Agentic search statistics retrieved successfully"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get search statistics: {str(e)}")


@router.get("/agentic-search/history", summary="🧬 Agentic Search History", description="Get history of agentic search proposals and executions")
async def get_agentic_search_history(
    context_type: Optional[str] = Query(None, description="Filter by context type"),
    limit: int = Query(50, ge=1, le=200, description="Maximum number of results")
):
    """🧬 Get history of agentic search activities"""
    try:
        search_service = AgenticSearchService()
        history = search_service.get_search_history(context_type=context_type)

        # Sort by timestamp descending and limit results
        sorted_history = sorted(history, key=lambda x: x.timestamp, reverse=True)[:limit]

        return {
            "search_history": [s.to_dict() for s in sorted_history],
            "total_results": len(sorted_history),
            "filtered_by_context": context_type,
            "message": f"Retrieved {len(sorted_history)} agentic search history items"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get search history: {str(e)}")