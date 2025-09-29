#!/usr/bin/env python3
"""
Unit tests for core consciousness engine integration
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
import httpx
import json

from src.core.engine import ConsciousnessEngine
from src.core.config import Settings


class TestConsciousnessEngine:
    """Test consciousness engine client"""

    @pytest.fixture
    def engine(self):
        """Create test engine instance"""
        settings = Settings(
            consciousness_engine_url="http://localhost:3002",
            consciousness_engine_timeout=30
        )
        return ConsciousnessEngine(settings)

    @pytest.mark.asyncio
    async def test_successful_code_generation(self, engine):
        """Test successful code generation"""
        mock_response_data = {
            "generated_code": "def hello_world():\n    print('Hello, World!')",
            "language": "python",
            "complexity_level": "simple"
        }

        with patch('httpx.AsyncClient.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_response_data
            mock_post.return_value = mock_response

            result = await engine.generate_code(
                task_description="Create a hello world function",
                language="python",
                complexity_level="simple"
            )

            assert result == mock_response_data
            mock_post.assert_called_once()

    @pytest.mark.asyncio
    async def test_code_generation_with_retry(self, engine):
        """Test code generation with retry on failure"""
        mock_response_data = {
            "generated_code": "console.log('Hello, World!');",
            "language": "javascript",
            "complexity_level": "simple"
        }

        with patch('httpx.AsyncClient.post') as mock_post:
            # First call fails, second succeeds
            mock_fail_response = Mock()
            mock_fail_response.status_code = 500
            mock_fail_response.raise_for_status.side_effect = httpx.HTTPStatusError(
                "Server Error", request=Mock(), response=Mock()
            )

            mock_success_response = Mock()
            mock_success_response.status_code = 200
            mock_success_response.json.return_value = mock_response_data

            mock_post.side_effect = [mock_fail_response, mock_success_response]

            result = await engine.generate_code(
                task_description="Create a hello world function",
                language="javascript"
            )

            assert result == mock_response_data
            assert mock_post.call_count == 2

    @pytest.mark.asyncio
    async def test_code_generation_timeout(self, engine):
        """Test code generation timeout handling"""
        with patch('httpx.AsyncClient.post') as mock_post:
            mock_post.side_effect = httpx.TimeoutException("Request timeout")

            with pytest.raises(Exception):
                await engine.generate_code(
                    task_description="Create a complex function",
                    language="python",
                    complexity_level="advanced"
                )

    @pytest.mark.asyncio
    async def test_map_reduce_processing(self, engine):
        """Test map-reduce processing via consciousness engine"""
        mock_response_data = {
            "result": [2, 4, 6, 8, 10],
            "processing_time_ms": 150,
            "success": True
        }

        with patch('httpx.AsyncClient.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_response_data
            mock_post.return_value = mock_response

            config = {
                "data": [1, 2, 3, 4, 5],
                "map_function": "lambda x: x * 2",
                "reduce_function": "lambda x, y: x + y"
            }

            result = await engine.process_map_reduce(config)

            assert result == mock_response_data
            mock_post.assert_called_once_with(
                "http://localhost:3002/map-reduce",
                json=config,
                timeout=30
            )

    @pytest.mark.asyncio
    async def test_engine_health_check(self, engine):
        """Test consciousness engine health check"""
        with patch('httpx.AsyncClient.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"status": "healthy", "version": "1.0.0"}
            mock_get.return_value = mock_response

            health = await engine.check_health()

            assert health["status"] == "healthy"
            assert health["version"] == "1.0.0"
            mock_get.assert_called_once_with(
                "http://localhost:3002/health",
                timeout=5
            )

    @pytest.mark.asyncio
    async def test_engine_health_check_failure(self, engine):
        """Test consciousness engine health check failure"""
        with patch('httpx.AsyncClient.get') as mock_get:
            mock_get.side_effect = httpx.ConnectError("Connection refused")

            health = await engine.check_health()

            assert health["status"] == "unhealthy"
            assert "error" in health


class TestEngineIntegration:
    """Test engine integration with other components"""

    @pytest.mark.asyncio
    async def test_engine_with_user_service(self):
        """Test engine integration with user service"""
        from src.services.user_service import UserService
        from src.core.database import get_db

        # Mock database session
        mock_db = AsyncMock()

        # Mock engine
        mock_engine = AsyncMock()
        mock_engine.generate_code.return_value = {
            "generated_code": "def analyze_user(user_data):\n    return user_data",
            "language": "python"
        }

        user_service = UserService(mock_db, mock_engine)

        # Test user intelligence analysis
        analysis = await user_service.analyze_user_intelligence({
            "name": "Test User",
            "role": "Developer",
            "experience_years": 5
        })

        assert "intelligence_score" in analysis
        assert "insights" in analysis
        mock_engine.generate_code.assert_called_once()

    @pytest.mark.asyncio
    async def test_engine_with_project_service(self):
        """Test engine integration with project service"""
        from src.services.project_service import ProjectService
        from src.core.database import get_db

        # Mock database session
        mock_db = AsyncMock()

        # Mock engine
        mock_engine = AsyncMock()
        mock_engine.generate_code.return_value = {
            "generated_code": "from flask import Flask\n\napp = Flask(__name__)\n\n@app.route('/')\ndef hello():\n    return 'Hello World!'\n\nif __name__ == '__main__':\n    app.run()",
            "language": "python"
        }

        project_service = ProjectService(mock_db, mock_engine)

        # Test project generation
        project = await project_service.generate_project(
            user_id="test_user",
            project_type="web_app",
            requirements="Simple web app with hello world"
        )

        assert project["type"] == "web_app"
        assert "code" in project
        assert len(project["code"]) > 0
        mock_engine.generate_code.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])