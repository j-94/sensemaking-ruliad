#!/usr/bin/env python3
"""
Project service for AI-powered project generation
"""

import asyncio
from typing import List, Optional, Dict, Any
from uuid import uuid4
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import func

from ..core.database import Project, User
from ..core.engine import ConsciousnessEngine
from .agentic_search_service import AgenticSearchService


class ProjectService:
    """Service for AI-powered project generation"""

    def __init__(self, db: Session, engine: ConsciousnessEngine):
        self.db = db
        self.engine = engine
        self.search_service = AgenticSearchService()

    async def generate_project(self, user_id: str, project_type: str, requirements: str = "") -> Dict[str, Any]:
        """Generate AI project using consciousness engine with agentic search enhancement"""
        # Validate user exists
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError(f"User {user_id} not found")

        # 🧬 Agentic Search: Propose contextual searches for better project generation
        user_context = {
            'intelligence_level': user.intelligence_level,
            'role': user.role,
            'name': user.name
        }

        # Determine language for search proposals
        language_map = {
            'web_app': 'javascript',
            'api': 'python',
            'agent': 'python'
        }
        language = language_map.get(project_type, 'python')

        # Propose searches to gather context for better project generation
        search_proposals = await self.search_service.propose_searches_for_project(
            project_type=project_type,
            language=language,
            user_context=user_context
        )

        # Execute top 3 highest priority searches to gather context
        search_context = []
        prioritized_searches = sorted(search_proposals, key=lambda x: x.priority, reverse=True)[:3]

        for proposal in prioritized_searches:
            try:
                search_result = await self.search_service.execute_search(proposal)
                search_context.append({
                    'query': proposal.query,
                    'insights': search_result.insights_extracted,
                    'relevance': search_result.relevance_score
                })
            except Exception as e:
                # Continue with project generation even if search fails
                print(f"Search execution failed for {proposal.query}: {e}")

        # Define project templates (preserved from original)
        project_prompts = {
            'web_app': 'Create a modern React web application with user authentication and responsive design',
            'api': 'Build a REST API with consciousness data processing and comprehensive endpoints',
            'agent': 'Develop an AI agent with self-learning capabilities and consciousness integration'
        }

        base_prompt = project_prompts.get(project_type, 'Create a consciousness-aware application')

        # 🧬 Agentic Enhancement: Include search insights in prompt
        search_insights_text = ""
        if search_context:
            search_insights_text = "\nAgentic Search Insights (gathered for optimal project generation):\n"
            for i, context in enumerate(search_context, 1):
                search_insights_text += f"{i}. {context['query']}\n"
                search_insights_text += f"   Key insights: {', '.join(context['insights'])}\n"
                search_insights_text += f"   Relevance: {context['relevance']:.2f}\n\n"

        # Enhance prompt with user context, search insights, and requirements
        full_prompt = f"""
        {base_prompt} for user {user.name} with intelligence level {user.intelligence_level}.

        User Profile:
        - Name: {user.name}
        - Role: {user.role}
        - Intelligence Level: {user.intelligence_level}/100
        - Experience: Advanced user with consciousness engineering background

        {search_insights_text}
        Requirements: {requirements if requirements else 'Create a fully functional, production-ready application'}

        Technical Specifications:
        - Use modern best practices and frameworks informed by current research
        - Include proper error handling and logging
        - Add comprehensive documentation
        - Ensure security and performance optimization
        - Make it consciousness-engineered where applicable
        - Incorporate insights from agentic search context for superior implementation
        """

        # Determine language based on project type
        language_map = {
            'web_app': 'javascript',
            'api': 'python',
            'agent': 'python'
        }
        language = language_map.get(project_type, 'python')

        try:
            # Generate code using consciousness engine
            result = await self.engine.generate_code(
                task_description=full_prompt,
                language=language,
                complexity_level='advanced'
            )

            # Create project record
            project_id = str(uuid4())
            project = Project(
                id=project_id,
                user_id=user_id,
                name=f"{project_type.title()} Project",
                type=project_type,
                code=result.get('generated_code', '# Code generation failed'),
                status='generated',
                created_at=datetime.utcnow()
            )

            self.db.add(project)
            self.db.commit()
            self.db.refresh(project)

            return {
                'id': project.id,
                'user_id': project.user_id,
                'name': project.name,
                'type': project.type,
                'code': project.code,
                'status': project.status,
                'created_at': project.created_at.isoformat(),
                'code_length': len(project.code),
                'agentic_searches': {
                    'searches_proposed': len(search_proposals),
                    'searches_executed': len(search_context),
                    'search_context': search_context,
                    'enhancement_applied': True
                }
            }

        except Exception as e:
            # Create failed project record
            project_id = str(uuid4())
            project = Project(
                id=project_id,
                user_id=user_id,
                name=f"{project_type.title()} Project (Failed)",
                type=project_type,
                code=f'# Project generation failed: {str(e)}',
                status='failed',
                created_at=datetime.utcnow()
            )

            self.db.add(project)
            self.db.commit()

            raise Exception(f"Project generation failed: {str(e)}")

    def get_projects(self, page: int = 1, limit: int = 50, user_id: Optional[str] = None,
                    project_type: Optional[str] = None, status: Optional[str] = None) -> Dict[str, Any]:
        """Get paginated list of projects with filtering"""
        query = self.db.query(Project)

        # Apply filters
        if user_id:
            query = query.filter(Project.user_id == user_id)
        if project_type:
            query = query.filter(Project.type == project_type)
        if status:
            query = query.filter(Project.status == status)

        # Get total count
        total_count = query.count()

        # Apply pagination
        offset = (page - 1) * limit
        projects_query = query.offset(offset).limit(limit).all()

        # Build response
        projects = []
        for project in projects_query:
            # Get user info
            user = self.db.query(User).filter(User.id == project.user_id).first()

            projects.append({
                'id': project.id,
                'user_id': project.user_id,
                'user_name': user.name if user else 'Unknown',
                'name': project.name,
                'type': project.type,
                'status': project.status,
                'created_at': project.created_at.isoformat(),
                'code_length': len(project.code)
            })

        return {
            'projects': projects,
            'pagination': {
                'page': page,
                'limit': limit,
                'total': total_count,
                'pages': (total_count + limit - 1) // limit
            },
            'filters': {
                'user_id': user_id,
                'project_type': project_type,
                'status': status
            }
        }

    def get_project(self, project_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed project information"""
        project = self.db.query(Project).filter(Project.id == project_id).first()
        if not project:
            return None

        # Get user info
        user = self.db.query(User).filter(User.id == project.user_id).first()

        return {
            'id': project.id,
            'user_id': project.user_id,
            'user_name': user.name if user else 'Unknown',
            'name': project.name,
            'type': project.type,
            'code': project.code,
            'status': project.status,
            'created_at': project.created_at.isoformat(),
            'updated_at': project.updated_at.isoformat() if project.updated_at else None,
            'code_length': len(project.code),
            'code_lines': len(project.code.split('\n'))
        }

    def delete_project(self, project_id: str) -> bool:
        """Delete a project"""
        project = self.db.query(Project).filter(Project.id == project_id).first()
        if not project:
            return False

        self.db.delete(project)
        self.db.commit()
        return True

    def get_project_statistics(self) -> Dict[str, Any]:
        """Get comprehensive project statistics"""
        total_projects = self.db.query(func.count(Project.id)).scalar()

        # Type distribution
        type_stats = self.db.query(
            Project.type,
            func.count(Project.id)
        ).group_by(Project.type).all()

        types = {ptype: count for ptype, count in type_stats}

        # Status distribution
        status_stats = self.db.query(
            Project.status,
            func.count(Project.id)
        ).group_by(Project.status).all()

        statuses = {status: count for status, count in status_stats}

        # Recent activity (last 30 days)
        thirty_days_ago = datetime.utcnow().replace(day=datetime.utcnow().day - 30)
        recent_projects = self.db.query(func.count(Project.id)).filter(
            Project.created_at >= thirty_days_ago
        ).scalar()

        # Average code length by type
        avg_lengths = self.db.query(
            Project.type,
            func.avg(func.length(Project.code))
        ).group_by(Project.type).all()

        avg_code_lengths = {ptype: round(length, 2) for ptype, length in avg_lengths}

        return {
            'total_projects': total_projects,
            'type_distribution': types,
            'status_distribution': statuses,
            'recent_projects': recent_projects,
            'average_code_lengths': avg_code_lengths,
            'most_popular_type': max(types.items(), key=lambda x: x[1])[0] if types else None
        }

    async def regenerate_project(self, project_id: str, new_requirements: str = "") -> Dict[str, Any]:
        """Regenerate an existing project with new requirements"""
        project = self.db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise ValueError(f"Project {project_id} not found")

        # Generate new code
        result = await self.generate_project(
            user_id=project.user_id,
            project_type=project.type,
            requirements=new_requirements or f"Regenerate {project.name} with improvements"
        )

        # Update the existing project
        project.code = result['code']
        project.status = 'regenerated'
        project.updated_at = datetime.utcnow()

        self.db.commit()

        return result