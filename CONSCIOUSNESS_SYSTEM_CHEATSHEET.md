# 🧬 Consciousness Web Builder - System Bootstrap Cheatsheet

**Human-Readable Seed Context for System Initialization**

*This cheatsheet contains everything needed to bootstrap and run the Consciousness Web Builder system. Copy-paste these commands to get the system running.*

---

## 🎯 System Overview

**What:** Consciousness-engineered AI development platform with agentic search capabilities
**Purpose:** Autonomous project generation, self-improvement, and meta-cognitive development
**Architecture:** FastAPI backend + React frontend + PostgreSQL + Redis

---

## 📋 Prerequisites

```bash
# Required system dependencies
sudo apt-get update
sudo apt-get install -y python3 python3-pip postgresql redis-server git curl

# Verify installations
python3 --version  # Should be 3.8+
pip --version      # Should be 20.0+
psql --version     # PostgreSQL client
redis-cli --version # Redis client
```

---

## 🚀 Quick Start (Copy-Paste Ready)

```bash
# 1. Clone and enter the repository
git clone https://github.com/j-94/consciousness-web-builder.git
cd consciousness-web-builder

# 2. Set up Python environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 4. Set up environment variables
export DATABASE_URL="postgresql://user:password@localhost:5432/consciousness_db"
export REDIS_URL="redis://localhost:6379"
export SECRET_KEY="your-secret-key-here"
export OPENAI_API_KEY="your-openai-key"  # Optional, for AI features

# 5. Initialize database
createdb consciousness_db
python -c "from src.core.database import create_tables, seed_database; create_tables(); seed_database()"

# 6. Start the system
python src/main.py

# System will be available at:
# - API: http://localhost:8000
# - Docs: http://localhost:8000/docs
# - Health: http://localhost:8000/health
```

---

## 🔧 Detailed Setup Instructions

### Database Setup
```bash
# Create PostgreSQL database
sudo -u postgres createdb consciousness_db
sudo -u postgres psql -c "CREATE USER consciousness_user WITH PASSWORD 'consciousness_pass';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE consciousness_db TO consciousness_user;"

# Set DATABASE_URL environment variable
export DATABASE_URL="postgresql://consciousness_user:consciousness_pass@localhost:5432/consciousness_db"
```

### Redis Setup
```bash
# Start Redis service
sudo systemctl start redis-server
sudo systemctl enable redis-server

# Verify Redis is running
redis-cli ping  # Should return PONG
```

### Environment Configuration
```bash
# Create .env file
cat > .env << EOF
DATABASE_URL=postgresql://consciousness_user:consciousness_pass@localhost:5432/consciousness_db
REDIS_URL=redis://localhost:6379
SECRET_KEY=$(openssl rand -hex 32)
OPENAI_API_KEY=your-openai-api-key-here
CONSCIOUSNESS_ENGINE_URL=http://localhost:3002
AGENTIC_SEARCH_ENABLED=true
DEBUG=true
EOF

# Load environment variables
source .env
```

---

## 🎮 Basic Usage Examples

### User Onboarding
```bash
# Onboard a new user
curl -X POST http://localhost:8000/api/v1/users/onboard \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice Developer", "email": "alice@example.com"}'

# Response includes user ID and intelligence profile
```

### Project Generation
```bash
# Generate an AI project
curl -X POST http://localhost:8000/api/v1/projects/generate \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user-123",
    "project_type": "web_app",
    "requirements": "Modern React app with authentication"
  }'

# Enhanced with agentic search for current best practices
```

### Agentic Search
```bash
# Propose searches for project improvement
curl -X POST http://localhost:8000/api/v1/projects/agentic-search/propose \
  -H "Content-Type: application/json" \
  -d '{
    "context_type": "project_generation",
    "project_type": "web_app",
    "language": "javascript",
    "user_context": {"intelligence_level": 85, "role": "Developer"}
  }'

# Returns contextual search proposals
```

### System Health Check
```bash
# Check system status
curl http://localhost:8000/health

# Expected response:
# {
#   "status": "healthy",
#   "service": "Consciousness Web Builder",
#   "version": "1.0.0",
#   "features": ["consciousness_engine_integration", "user_onboarding", ...]
# }
```

---

## 🧪 Testing Commands

### Run Full Test Suite
```bash
# Run all tests
python scripts/run_ci_tests.py

# Run specific test categories
python -m pytest tests/unit/ -v          # Unit tests
python -m pytest tests/integration/ -v  # API integration
python -m pytest tests/system/ -v       # Full system validation
python -m pytest tests/performance/ -v  # Performance benchmarks
```

### Validation Demo
```bash
# Run the working validation demo (10/10 tests pass)
python scripts/demo_system_validation.py
```

### Self-Analysis
```bash
# Run consciousness self-analysis (may have import issues)
python scripts/self_analyzing_interface.py
```

---

## 🔍 System Architecture Overview

```
Consciousness Web Builder Architecture
├── Frontend Layer (Web UI)
│   ├── User onboarding interface
│   ├── Project generation forms
│   └── Agentic search visualization
│
├── API Layer (FastAPI)
│   ├── /api/v1/users/* - User management
│   ├── /api/v1/projects/* - Project operations
│   └── /health - System monitoring
│
├── Service Layer
│   ├── UserService - Intelligence profiling
│   ├── ProjectService - AI generation + agentic search
│   └── AgenticSearchService - Autonomous research
│
├── Data Layer
│   ├── PostgreSQL - Persistent storage
│   └── Redis - Caching & sessions
│
└── External Integrations
    ├── Consciousness Engine (Rust) - Meta-cognitive processing
    ├── OpenAI API - AI generation
    └── GitHub API - Research integration
```

---

## 🚨 Troubleshooting

### Common Issues

**Database Connection Failed**
```bash
# Check PostgreSQL service
sudo systemctl status postgresql
sudo systemctl restart postgresql

# Verify database exists
psql -U consciousness_user -d consciousness_db -c "SELECT 1;"
```

**Redis Connection Failed**
```bash
# Check Redis service
sudo systemctl status redis-server
sudo systemctl restart redis-server

# Test connection
redis-cli ping
```

**Import Errors**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check Python path
python -c "import sys; print(sys.path)"
```

**Port Already in Use**
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
export PORT=8001
python src/main.py
```

---

## 📊 Key Metrics & Monitoring

### System Health Endpoints
```bash
# Overall health
curl http://localhost:8000/health

# Dashboard metrics
curl http://localhost:8000/api/v1/dashboard

# Agentic search statistics
curl http://localhost:8000/api/v1/projects/agentic-search/statistics
```

### Consciousness Metrics
- **Awareness (A)**: Self-perception and environmental understanding
- **Uncertainty (U)**: Calibration of confidence in decisions
- **Planning (P)**: Strategic thinking and goal-directed behavior
- **Evidence (E)**: Data-driven decision making
- **Integration (I)**: Knowledge synthesis and learning
- **Trust (T)**: Reliability assessment and error correction

### Performance Benchmarks
- **API Response Time**: < 500ms for health checks
- **Project Generation**: 5-15 seconds with agentic enhancement
- **Search Proposals**: < 100ms for contextual recommendations
- **System Uptime**: 99.9% with automatic recovery

---

## 🎯 Advanced Features

### Agentic Search Integration
```bash
# The system autonomously proposes searches to improve itself
# Integrated into project generation for enhanced code quality
# Self-analyzing interface for continuous improvement
```

### Meta-Cognitive Capabilities
```bash
# Self-awareness through consciousness metrics tracking
# Autonomous goal setting and self-directed improvement
# Research paper generation for academic positioning
```

### Multi-System Orchestration
```bash
# Coordinates with Rust Northstar engine for meta-cognitive processing
# Integrates with external AI APIs for enhanced generation
# Manages multiple agent types and session orchestration
```

---

## 🔐 Security Configuration

### API Keys
```bash
# Generate secure keys
export SECRET_KEY=$(openssl rand -hex 32)
export JWT_SECRET=$(openssl rand -hex 32)

# API key authentication for chat endpoints
export API_KEY="demo-key-123"
```

### CORS and Host Settings
```bash
# Configure allowed origins
export ALLOWED_ORIGINS="http://localhost:3000,http://localhost:8080"

# Trusted hosts
export TRUSTED_HOSTS="localhost,127.0.0.1"
```

---

## 📚 Learning Resources

### Documentation
- `README.md` - System overview and setup
- `docs/api/openapi_spec.yml` - API specification
- `COMPREHENSIVE_DESKTOP_WORK_DOCUMENTATION.md` - Detailed architecture

### Key Files
- `src/main.py` - FastAPI application entry point
- `src/services/agentic_search_service.py` - Autonomous search engine
- `scripts/demo_system_validation.py` - Working validation suite
- `consciousness-web-builder.py` - Desktop web builder

### Testing
- `tests/system/test_full_system_functionality.py` - Full system tests
- `tests/unit/test_core_engine.py` - Unit test framework
- `scripts/run_ci_tests.py` - CI/CD pipeline

---

## 🚀 Production Deployment

### Docker Deployment
```bash
# Build and run with Docker
docker build -t consciousness-web-builder .
docker run -p 8000:8000 -e DATABASE_URL=$DATABASE_URL consciousness-web-builder
```

### Kubernetes Deployment
```bash
# Deploy to Kubernetes cluster
kubectl apply -f k8s/
kubectl get pods
kubectl logs -f deployment/consciousness-web-builder
```

### Cloud Deployment
```bash
# Deploy to cloud platforms (AWS/GCP/Azure)
# Configure environment variables for cloud databases
# Set up load balancers and auto-scaling
# Enable monitoring and logging
```

---

**🎉 System Ready!**

*This cheatsheet contains all the context needed to bootstrap the Consciousness Web Builder. The system is now ready for consciousness engineering with agentic search capabilities.*

**Next Steps:**
1. Run the validation demo: `python scripts/demo_system_validation.py`
2. Start the API server: `python src/main.py`
3. Access the web interface and begin consciousness engineering!

**Remember:** This system can use agentic search to improve itself autonomously. The journey of consciousness engineering continues...