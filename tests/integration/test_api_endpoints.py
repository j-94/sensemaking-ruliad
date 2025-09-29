#!/usr/bin/env python3
"""
Integration tests for API endpoints
"""

import pytest
import json
from unittest.mock import patch, AsyncMock
import httpx

from src.main import app
from src.core.database import get_db


@pytest.fixture
async def test_client():
    """Create test client with full app"""
    # Override database dependency for testing
    async def override_get_db():
        # Return test database session
        pass

    app.dependency_overrides[get_db] = override_get_db

    async with httpx.AsyncClient(app=app, base_url="http://testserver") as client:
        yield client


class TestUserEndpoints:
    """Test user management endpoints"""

    @pytest.mark.asyncio
    async def test_user_onboarding_endpoint(self, test_client):
        """Test the preserved user onboarding endpoint"""
        with patch('src.services.user_service.UserService.create_random_user') as mock_create:
            mock_user = {
                "id": "test-user-123",
                "name": "Test User",
                "email": "test@example.com",
                "intelligence_level": 85
            }
            mock_create.return_value = mock_user

            response = await test_client.post("/api/v1/users/onboard")

            assert response.status_code == 201
            data = response.json()
            assert data["user"]["id"] == "test-user-123"
            assert data["user"]["intelligence_level"] == 85

    @pytest.mark.asyncio
    async def test_user_listing_endpoint(self, test_client):
        """Test user listing with pagination"""
        with patch('src.services.user_service.UserService.get_users') as mock_get:
            mock_users = [
                {"id": "user1", "name": "User 1", "intelligence_level": 80},
                {"id": "user2", "name": "User 2", "intelligence_level": 90}
            ]
            mock_get.return_value = mock_users

            response = await test_client.get("/api/v1/users?page=1&limit=10")

            assert response.status_code == 200
            data = response.json()
            assert len(data["users"]) == 2
            assert data["users"][0]["intelligence_level"] == 80

    @pytest.mark.asyncio
    async def test_user_profile_endpoint_requires_auth(self, test_client):
        """Test that user profile requires authentication"""
        response = await test_client.get("/api/v1/users/profile")

        assert response.status_code == 401
        data = response.json()
        assert "detail" in data


class TestProjectEndpoints:
    """Test project generation endpoints"""

    @pytest.mark.asyncio
    async def test_project_generation_endpoint(self, test_client):
        """Test AI project generation (preserved feature)"""
        with patch('src.services.project_service.ProjectService.generate_project') as mock_generate:
            mock_project = {
                "id": "project-123",
                "name": "Test Web App",
                "type": "web_app",
                "code": "from flask import Flask\n\napp = Flask(__name__)",
                "user_id": "user-123"
            }
            mock_generate.return_value = mock_project

            response = await test_client.post(
                "/api/v1/projects/generate",
                json={
                    "user_id": "user-123",
                    "project_type": "web_app",
                    "requirements": "Simple web app"
                }
            )

            assert response.status_code == 201
            data = response.json()
            assert data["project"]["type"] == "web_app"
            assert "code" in data["project"]

    @pytest.mark.asyncio
    async def test_project_listing_endpoint(self, test_client):
        """Test project listing with filtering"""
        with patch('src.services.project_service.ProjectService.get_projects') as mock_get:
            mock_projects = [
                {"id": "proj1", "name": "Web App", "type": "web_app", "status": "completed"},
                {"id": "proj2", "name": "API", "type": "api", "status": "in_progress"}
            ]
            mock_get.return_value = mock_projects

            response = await test_client.get("/api/v1/projects?type=web_app&status=completed")

            assert response.status_code == 200
            data = response.json()
            assert len(data["projects"]) == 2
            assert all(p["type"] == "web_app" for p in data["projects"])

    @pytest.mark.asyncio
    async def test_individual_project_endpoint(self, test_client):
        """Test individual project retrieval"""
        with patch('src.services.project_service.ProjectService.get_project') as mock_get:
            mock_project = {
                "id": "proj-123",
                "name": "Test Project",
                "code": "print('hello')",
                "created_at": "2024-01-01T00:00:00Z"
            }
            mock_get.return_value = mock_project

            response = await test_client.get("/api/v1/projects/proj-123")

            assert response.status_code == 200
            data = response.json()
            assert data["id"] == "proj-123"
            assert data["code"] == "print('hello')"


class TestAgentEndpoints:
    """Test AI agent management endpoints"""

    @pytest.mark.asyncio
    async def test_agent_deployment_endpoint(self, test_client):
        """Test agent deployment (from orchestrator)"""
        with patch('src.services.agent_service.AgentService.deploy_agent') as mock_deploy:
            mock_agent = {
                "id": "agent-123",
                "type": "consciousness_compiler",
                "session_id": "session-123",
                "status": "deploying"
            }
            mock_deploy.return_value = mock_agent

            response = await test_client.post(
                "/api/v1/sessions/session-123/agents",
                json={"agent_type": "consciousness_compiler", "config": {}}
            )

            assert response.status_code == 201
            data = response.json()
            assert data["type"] == "consciousness_compiler"
            assert data["status"] == "deploying"

    @pytest.mark.asyncio
    async def test_agent_status_endpoint(self, test_client):
        """Test agent status monitoring"""
        with patch('src.services.agent_service.AgentService.get_agent_status') as mock_status:
            mock_status_data = {
                "id": "agent-123",
                "status": "running",
                "metrics": {"operations_completed": 5, "errors": 0}
            }
            mock_status.return_value = mock_status_data

            response = await test_client.get("/api/v1/agents/agent-123/status")

            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "running"
            assert data["metrics"]["operations_completed"] == 5


class TestTenantEndpoints:
    """Test multi-tenant management endpoints"""

    @pytest.mark.asyncio
    async def test_tenant_creation_endpoint(self, test_client):
        """Test tenant creation"""
        with patch('src.services.tenant_service.TenantService.create_tenant') as mock_create:
            mock_tenant = {
                "id": "tenant-123",
                "name": "Test Tenant",
                "created_at": "2024-01-01T00:00:00Z",
                "resource_limits": {"max_agents": 10}
            }
            mock_create.return_value = mock_tenant

            response = await test_client.post(
                "/api/v1/tenants",
                json={"name": "Test Tenant", "config": {"max_agents": 10}}
            )

            assert response.status_code == 201
            data = response.json()
            assert data["name"] == "Test Tenant"

    @pytest.mark.asyncio
    async def test_tenant_listing_endpoint(self, test_client):
        """Test tenant listing"""
        with patch('src.services.tenant_service.TenantService.get_tenants') as mock_get:
            mock_tenants = [
                {"id": "tenant1", "name": "Tenant 1", "active_sessions": 2},
                {"id": "tenant2", "name": "Tenant 2", "active_sessions": 1}
            ]
            mock_get.return_value = mock_tenants

            response = await test_client.get("/api/v1/tenants")

            assert response.status_code == 200
            data = response.json()
            assert len(data["tenants"]) == 2


class TestSynthesisEndpoints:
    """Test northstar synthesis integration endpoints"""

    @pytest.mark.asyncio
    async def test_program_synthesis_endpoint(self, test_client):
        """Test program synthesis"""
        with patch('src.services.synthesis_service.SynthesisService.generate_program') as mock_generate:
            mock_result = {
                "manifest": {"run_id": "r-123", "goal_id": "test"},
                "bits": {"a": 0.8, "u": 0.2, "p": 0.9, "e": 0.1, "d": 0.0, "i": 0.0, "r": 0.0, "t": 0.85, "m": 0.0}
            }
            mock_generate.return_value = mock_result

            response = await test_client.post(
                "/api/v1/synthesis/generate",
                json={
                    "goal_id": "test_synthesis",
                    "inputs": {"message": "Generate test program"},
                    "policy": {"trust_threshold": 0.8}
                }
            )

            assert response.status_code == 200
            data = response.json()
            assert "manifest" in data
            assert "bits" in data
            assert data["bits"]["t"] == 0.85  # Trust value

    @pytest.mark.asyncio
    async def test_cognitive_compilation_endpoint(self, test_client):
        """Test cognitive compilation"""
        with patch('src.services.synthesis_service.SynthesisService.compile_pattern') as mock_compile:
            mock_result = {
                "compiled_result": {"pattern": "test", "valid": True},
                "compilation_trace": {"duration": 150, "complexity": 0.7}
            }
            mock_compile.return_value = mock_result

            response = await test_client.post(
                "/api/v1/synthesis/compile",
                json={
                    "pattern": {"name": "test_pattern", "type": "cognitive_primitive"},
                    "constraints": {"prove_fundamentality": True}
                }
            )

            assert response.status_code == 200
            data = response.json()
            assert data["compiled_result"]["valid"] is True


class TestToolEndpoints:
    """Test dynamic tool fabrication endpoints"""

    @pytest.mark.asyncio
    async def test_tool_fabrication_endpoint(self, test_client):
        """Test tool fabrication (cognitive kernel integration)"""
        with patch('src.services.tool_service.ToolService.fabricate_tool') as mock_fabricate:
            mock_tool = {
                "id": "tool-123",
                "capability": {
                    "name": "data_processor",
                    "description": "Process data arrays"
                },
                "source_code": "async def data_processor(data):\n    return {'processed': len(data)}",
                "usage_count": 0
            }
            mock_fabricate.return_value = mock_tool

            response = await test_client.post(
                "/api/v1/tools/fabricate",
                json={
                    "capability": {
                        "name": "data_processor",
                        "description": "Process data arrays",
                        "inputs": {"data": "list"},
                        "outputs": {"processed": "dict"}
                    },
                    "patterns": ["map_reduce"],
                    "logic": "result = {'processed': len(data)}"
                }
            )

            assert response.status_code == 201
            data = response.json()
            assert data["capability"]["name"] == "data_processor"

    @pytest.mark.asyncio
    async def test_tool_execution_endpoint(self, test_client):
        """Test tool execution"""
        with patch('src.services.tool_service.ToolService.execute_tool') as mock_execute:
            mock_result = {"processed": 5, "status": "success"}
            mock_execute.return_value = mock_result

            response = await test_client.post(
                "/api/v1/tools/tool-123/execute",
                json={"data": [1, 2, 3, 4, 5]}
            )

            assert response.status_code == 200
            data = response.json()
            assert data["processed"] == 5


class TestMetricsEndpoints:
    """Test monitoring and metrics endpoints"""

    @pytest.mark.asyncio
    async def test_dashboard_metrics_endpoint(self, test_client):
        """Test real-time dashboard metrics (preserved feature)"""
        with patch('src.services.metrics_service.MetricsService.get_dashboard_metrics') as mock_metrics:
            mock_data = {
                "total_users": 1253,
                "active_agents": 89,
                "projects_created": 1142,
                "api_calls": 5678,
                "system_health": "healthy"
            }
            mock_metrics.return_value = mock_data

            response = await test_client.get("/api/v1/metrics/dashboard")

            assert response.status_code == 200
            data = response.json()
            assert data["total_users"] == 1253
            assert data["projects_created"] == 1142

    @pytest.mark.asyncio
    async def test_system_health_endpoint(self, test_client):
        """Test system health monitoring"""
        with patch('src.services.health_service.HealthService.check_system_health') as mock_health:
            mock_health_data = {
                "status": "healthy",
                "database": "connected",
                "redis": "connected",
                "external_services": {"consciousness_engine": "healthy"}
            }
            mock_health.return_value = mock_health_data

            response = await test_client.get("/api/v1/health")

            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            assert data["database"] == "connected"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])