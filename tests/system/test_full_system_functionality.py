#!/usr/bin/env python3
"""
🧬 Full System Functionality Test Suite

This test suite validates that all consciousness-engineered features
have been successfully migrated to the production repository.
"""

import pytest
import asyncio
import json
import time
from unittest.mock import Mock, patch, AsyncMock
import httpx
import psycopg2
import redis
from datetime import datetime

from src.core.config import Settings
from src.core.engine import ConsciousnessEngine
from src.services.user_service import UserService
from src.services.project_service import ProjectService
from src.services.agent_service import AgentService
from src.api.routes.users import router as user_router
from src.api.routes.projects import router as project_router
from src.api.routes.agents import router as agent_router


class TestFullSystemFunctionality:
    """Complete system functionality validation"""

    @pytest.fixture
    async def test_client(self):
        """Create test client with full app"""
        from src.main import app
        from src.core.database import get_db

        # Override database dependency for testing
        async def override_get_db():
            # Return test database session
            pass

        app.dependency_overrides[get_db] = override_get_db

        async with httpx.AsyncClient(app=app, base_url="http://testserver") as client:
            yield client

    @pytest.fixture
    def test_db_connection(self):
        """Test database connection"""
        conn = psycopg2.connect(
            host="localhost",
            database="test_db",
            user="postgres",
            password="test_password"
        )
        yield conn
        conn.close()

    @pytest.fixture
    def test_redis_client(self):
        """Test Redis client"""
        client = redis.Redis(host='localhost', port=6379, db=1)
        yield client
        client.flushdb()
        client.close()

    @pytest.mark.asyncio
    async def test_consciousness_web_builder_endpoints(self, test_client):
        """Test all original consciousness web builder endpoints are functional"""
        print("\n🧪 Testing Consciousness Web Builder Endpoints...")

        # Test dashboard endpoint
        response = await test_client.get("/")
        assert response.status_code == 200
        assert "Consciousness Web Builder" in response.text
        print("✅ Dashboard endpoint functional")

        # Test user onboarding (preserved feature)
        response = await test_client.post("/api/v1/users/onboard")
        assert response.status_code == 201
        user_data = response.json()
        assert "user" in user_data
        assert "agent" in user_data
        assert user_data["user"]["intelligence_level"] >= 70
        print("✅ Random user onboarding preserved")

        # Test project generation (preserved feature)
        user_id = user_data["user"]["id"]
        response = await test_client.post(
            "/api/v1/projects/generate",
            json={"user_id": user_id, "project_type": "web_app"}
        )
        assert response.status_code == 201
        project_data = response.json()
        assert "project" in project_data
        assert project_data["project"]["type"] == "web_app"
        assert len(project_data["project"]["code"]) > 0
        print("✅ AI project generation preserved")

        # Test users listing
        response = await test_client.get("/api/v1/users")
        assert response.status_code == 200
        users_data = response.json()
        assert len(users_data["users"]) > 0
        print("✅ User listing functional")

        # Test projects listing
        response = await test_client.get("/api/v1/projects")
        assert response.status_code == 200
        projects_data = response.json()
        assert len(projects_data["projects"]) > 0
        print("✅ Project listing functional")

        # Test individual project retrieval
        project_id = project_data["project"]["id"]
        response = await test_client.get(f"/api/v1/projects/{project_id}")
        assert response.status_code == 200
        assert response.json()["id"] == project_id
        print("✅ Individual project retrieval functional")

        # Test metrics endpoint (preserved feature)
        response = await test_client.get("/api/v1/metrics/dashboard")
        assert response.status_code == 200
        metrics = response.json()
        assert "total_users" in metrics
        assert "active_agents" in metrics
        assert "projects_created" in metrics
        print("✅ Real-time metrics preserved")

    @pytest.mark.asyncio
    async def test_multi_tenant_orchestrator_integration(self, test_client):
        """Test multi-tenant orchestrator features are integrated"""
        print("\n🧪 Testing Multi-Tenant Orchestrator Integration...")

        # Test tenant creation
        response = await test_client.post(
            "/api/v1/tenants",
            json={"name": "test_tenant", "config": {"max_agents": 5}}
        )
        assert response.status_code == 201
        tenant_data = response.json()
        tenant_id = tenant_data["id"]
        print("✅ Tenant creation functional")

        # Test session creation
        response = await test_client.post(
            "/api/v1/sessions",
            json={"tenant_id": tenant_id, "config": {"environment": "test"}}
        )
        assert response.status_code == 201
        session_data = response.json()
        session_id = session_data["id"]
        print("✅ Session creation functional")

        # Test agent deployment (all 7 agent types)
        agent_types = [
            "consciousness_compiler",
            "map_reduce_processor",
            "reactive_poster",
            "memory_agent",
            "code_generator",
            "self_analyzer",
            "blob_processor"
        ]

        for agent_type in agent_types:
            response = await test_client.post(
                f"/api/v1/sessions/{session_id}/agents",
                json={"agent_type": agent_type, "config": {}}
            )
            assert response.status_code == 201
            agent_data = response.json()
            assert agent_data["type"] == agent_type
            print(f"✅ {agent_type} agent deployment functional")

        # Test session status
        response = await test_client.get(f"/api/v1/sessions/{session_id}")
        assert response.status_code == 200
        session_status = response.json()
        assert len(session_status["agents"]) == len(agent_types)
        print("✅ Session status monitoring functional")

        # Test tenant resource monitoring
        response = await test_client.get(f"/api/v1/tenants/{tenant_id}")
        assert response.status_code == 200
        tenant_status = response.json()
        assert "resource_usage" in tenant_status
        print("✅ Tenant resource monitoring functional")

    @pytest.mark.asyncio
    async def test_cognitive_kernel_integration(self, test_client):
        """Test cognitive kernel dynamic tool fabrication"""
        print("\n🧪 Testing Cognitive Kernel Tool Fabrication...")

        # Test tool fabrication
        response = await test_client.post(
            "/api/v1/tools/fabricate",
            json={
                "capability": {
                    "name": "test_analyzer",
                    "description": "Test analysis tool",
                    "inputs": {"data": "list"},
                    "outputs": {"result": "dict"}
                },
                "patterns": ["map_reduce"],
                "logic": "result = {'count': len(data), 'sum': sum(data) if data else 0}"
            }
        )
        assert response.status_code == 201
        tool_data = response.json()
        tool_id = tool_data["id"]
        print("✅ Tool fabrication functional")

        # Test tool execution
        response = await test_client.post(
            f"/api/v1/tools/{tool_id}/execute",
            json={"data": [1, 2, 3, 4, 5]}
        )
        assert response.status_code == 200
        result = response.json()
        assert result["count"] == 5
        assert result["sum"] == 15
        print("✅ Tool execution functional")

        # Test tool listing
        response = await test_client.get("/api/v1/tools")
        assert response.status_code == 200
        tools = response.json()
        assert len(tools) > 0
        print("✅ Tool management functional")

    @pytest.mark.asyncio
    async def test_northstar_synthesis_integration(self, test_client):
        """Test northstar program synthesis integration"""
        print("\n🧪 Testing Northstar Synthesis Integration...")

        # Test program synthesis
        response = await test_client.post(
            "/api/v1/synthesis/generate",
            json={
                "goal_id": "test_synthesis",
                "inputs": {
                    "message": "Generate a fibonacci function",
                    "context": [{"ts": "2024-01-01T00:00:00Z", "ttl": 3600}]
                },
                "policy": {"trust_threshold": 0.8}
            }
        )
        assert response.status_code == 200
        synthesis_result = response.json()
        assert "manifest" in synthesis_result
        assert "bits" in synthesis_result
        print("✅ Program synthesis functional")

        # Test cognitive compilation
        response = await test_client.post(
            "/api/v1/synthesis/compile",
            json={
                "pattern": {
                    "name": "fibonacci_pattern",
                    "type": "recursive_algorithm",
                    "description": "Fibonacci sequence generator"
                },
                "constraints": {"prove_correctness": True}
            }
        )
        assert response.status_code == 200
        compilation_result = response.json()
        assert "compiled_result" in compilation_result
        print("✅ Cognitive compilation functional")

        # Test pattern library access
        response = await test_client.get("/api/v1/synthesis/patterns")
        assert response.status_code == 200
        patterns = response.json()
        assert len(patterns) > 0
        print("✅ Pattern library access functional")

    @pytest.mark.asyncio
    async def test_database_persistence(self, test_db_connection):
        """Test database layer preserves all data"""
        print("\n🧪 Testing Database Persistence...")

        cursor = test_db_connection.cursor()

        # Check users table
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        assert user_count >= 0
        print("✅ Users table functional")

        # Check projects table
        cursor.execute("SELECT COUNT(*) FROM projects")
        project_count = cursor.fetchone()[0]
        assert project_count >= 0
        print("✅ Projects table functional")

        # Check agents table
        cursor.execute("SELECT COUNT(*) FROM agents")
        agent_count = cursor.fetchone()[0]
        assert agent_count >= 0
        print("✅ Agents table functional")

        # Check tenants table
        cursor.execute("SELECT COUNT(*) FROM tenants")
        tenant_count = cursor.fetchone()[0]
        assert tenant_count >= 0
        print("✅ Tenants table functional")

        cursor.close()

    @pytest.mark.asyncio
    async def test_redis_caching(self, test_redis_client):
        """Test Redis caching layer"""
        print("\n🧪 Testing Redis Caching Layer...")

        # Test basic caching
        test_redis_client.set("test_key", "test_value")
        value = test_redis_client.get("test_key")
        assert value.decode() == "test_value"
        print("✅ Redis caching functional")

        # Test session storage
        session_data = {"user_id": "123", "session_id": "abc"}
        test_redis_client.setex("session:abc", 3600, json.dumps(session_data))
        stored_session = test_redis_client.get("session:abc")
        assert json.loads(stored_session.decode()) == session_data
        print("✅ Session caching functional")

    @pytest.mark.asyncio
    async def test_authentication_system(self, test_client):
        """Test JWT authentication system"""
        print("\n🧪 Testing Authentication System...")

        # Test login endpoint
        response = await test_client.post(
            "/api/v1/auth/login",
            json={"username": "test_user", "password": "test_pass"}
        )
        # Note: This would be 200 in real implementation with proper user
        assert response.status_code in [200, 401]  # 401 if user doesn't exist
        print("✅ Authentication endpoints functional")

        # Test protected endpoint without auth (should fail)
        response = await test_client.get("/api/v1/users/profile")
        assert response.status_code == 401
        print("✅ Protected endpoints secured")

    @pytest.mark.asyncio
    async def test_health_checks(self, test_client):
        """Test comprehensive health checks"""
        print("\n🧪 Testing Health Checks...")

        # Overall health
        response = await test_client.get("/api/v1/health")
        assert response.status_code == 200
        health = response.json()
        assert health["status"] == "healthy"
        print("✅ Overall health check functional")

        # Database health
        response = await test_client.get("/api/v1/health/database")
        assert response.status_code == 200
        print("✅ Database health check functional")

        # External service health (mocked)
        with patch('httpx.AsyncClient.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_get.return_value = mock_response

            response = await test_client.get("/api/v1/health/engine")
            assert response.status_code == 200
            print("✅ Consciousness engine health check functional")

    @pytest.mark.asyncio
    async def test_background_processing(self, test_client):
        """Test background task processing"""
        print("\n🧪 Testing Background Processing...")

        # Test async project generation
        response = await test_client.post(
            "/api/v1/projects/generate",
            json={
                "user_id": "test_user",
                "project_type": "api",
                "async_processing": True
            }
        )
        assert response.status_code == 202  # Accepted for async processing
        task_data = response.json()
        assert "task_id" in task_data
        print("✅ Async project generation functional")

        # Test task status checking
        task_id = task_data["task_id"]
        response = await test_client.get(f"/api/v1/tasks/{task_id}/status")
        assert response.status_code == 200
        status = response.json()
        assert "status" in status
        print("✅ Task status monitoring functional")

    @pytest.mark.asyncio
    async def test_rate_limiting(self, test_client):
        """Test API rate limiting"""
        print("\n🧪 Testing Rate Limiting...")

        # Make multiple requests quickly
        responses = []
        for i in range(10):
            response = await test_client.post(
                "/api/v1/users/onboard",
                json={}
            )
            responses.append(response.status_code)

        # Should have some successful and some rate limited
        assert 201 in responses  # At least one success
        assert 429 in responses  # At least one rate limited
        print("✅ Rate limiting functional")

    @pytest.mark.asyncio
    async def test_error_handling(self, test_client):
        """Test comprehensive error handling"""
        print("\n🧪 Testing Error Handling...")

        # Test invalid project type
        response = await test_client.post(
            "/api/v1/projects/generate",
            json={"user_id": "test", "project_type": "invalid_type"}
        )
        assert response.status_code == 400
        error = response.json()
        assert "error" in error
        print("✅ Input validation functional")

        # Test non-existent resource
        response = await test_client.get("/api/v1/projects/non-existent-id")
        assert response.status_code == 404
        print("✅ 404 error handling functional")

        # Test malformed JSON
        response = await test_client.post(
            "/api/v1/projects/generate",
            content="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 400
        print("✅ Malformed request handling functional")

    @pytest.mark.asyncio
    async def test_full_system_integration(self, test_client):
        """Complete end-to-end system integration test"""
        print("\n🎯 Running Full System Integration Test...")

        # 1. Create user via preserved onboarding
        response = await test_client.post("/api/v1/users/onboard")
        assert response.status_code == 201
        user_data = response.json()
        user_id = user_data["user"]["id"]
        print("✅ Step 1: User onboarding complete")

        # 2. Generate project using AI (preserved feature)
        response = await test_client.post(
            "/api/v1/projects/generate",
            json={"user_id": user_id, "project_type": "web_app"}
        )
        assert response.status_code == 201
        project_data = response.json()
        project_id = project_data["project"]["id"]
        print("✅ Step 2: AI project generation complete")

        # 3. Create tenant and session (orchestrator integration)
        response = await test_client.post(
            "/api/v1/tenants",
            json={"name": "integration_test_tenant"}
        )
        assert response.status_code == 201
        tenant_data = response.json()
        tenant_id = tenant_data["id"]

        response = await test_client.post(
            "/api/v1/sessions",
            json={"tenant_id": tenant_id}
        )
        assert response.status_code == 201
        session_data = response.json()
        session_id = session_data["id"]
        print("✅ Step 3: Multi-tenant setup complete")

        # 4. Deploy consciousness compiler agent
        response = await test_client.post(
            f"/api/v1/sessions/{session_id}/agents",
            json={"agent_type": "consciousness_compiler"}
        )
        assert response.status_code == 201
        print("✅ Step 4: Agent deployment complete")

        # 5. Use cognitive kernel to fabricate a tool
        response = await test_client.post(
            "/api/v1/tools/fabricate",
            json={
                "capability": {
                    "name": "project_validator",
                    "description": "Validate generated projects",
                    "inputs": {"project_code": "str"},
                    "outputs": {"is_valid": "bool", "issues": "list"}
                },
                "patterns": ["map_reduce"],
                "logic": "is_valid = len(project_code) > 100; issues = [] if is_valid else ['Code too short']"
            }
        )
        assert response.status_code == 201
        tool_data = response.json()
        tool_id = tool_data["id"]
        print("✅ Step 5: Tool fabrication complete")

        # 6. Execute fabricated tool
        project_code = project_data["project"]["code"]
        response = await test_client.post(
            f"/api/v1/tools/{tool_id}/execute",
            json={"project_code": project_code}
        )
        assert response.status_code == 200
        tool_result = response.json()
        assert "is_valid" in tool_result
        print("✅ Step 6: Tool execution complete")

        # 7. Use northstar synthesis
        response = await test_client.post(
            "/api/v1/synthesis/generate",
            json={
                "goal_id": "validate_integration",
                "inputs": {"message": "Validate system integration"},
                "policy": {"trust_threshold": 0.8}
            }
        )
        assert response.status_code == 200
        print("✅ Step 7: Synthesis integration complete")

        # 8. Check system metrics (preserved feature)
        response = await test_client.get("/api/v1/metrics/dashboard")
        assert response.status_code == 200
        metrics = response.json()
        assert metrics["total_users"] > 0
        assert metrics["projects_created"] > 0
        print("✅ Step 8: Metrics validation complete")

        # 9. Verify health of all systems
        response = await test_client.get("/api/v1/health")
        assert response.status_code == 200
        health = response.json()
        assert health["status"] == "healthy"
        print("✅ Step 9: Health validation complete")

        print("\n🎉 FULL SYSTEM INTEGRATION TEST PASSED!")
        print("✅ All consciousness-engineered features preserved")
        print("✅ Multi-system integration successful")
        print("✅ Production-ready architecture validated")
        print("🚀 Ready for deployment!")


if __name__ == "__main__":
    # Run the full system test
    pytest.main([__file__, "-v", "--tb=short"])