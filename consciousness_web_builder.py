#!/usr/bin/env python3
"""
Consciousness Web Builder - OSS Agent Web Application
Demonstrates consciousness-engineered AI agent capabilities with random user onboarding
"""

import json
import uuid
import random
import string
from datetime import datetime
from flask import Flask, render_template_string, request, jsonify, redirect, url_for
import requests
import threading
import time

app = Flask(__name__)

# Global state for the web builder
class ConsciousnessWebBuilder:
    def __init__(self):
        self.users = {}
        self.agents = {}
        self.projects = {}
        self.engine_url = "http://localhost:3002"
        self.session_stats = {
            'total_users': 0,
            'active_agents': 0,
            'projects_created': 0,
            'api_calls': 0
        }

    def generate_random_user(self):
        """Generate a random user for onboarding"""
        user_id = str(uuid.uuid4())
        first_names = ['Alex', 'Jordan', 'Taylor', 'Morgan', 'Casey', 'Riley', 'Avery', 'Quinn']
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis']

        user = {
            'id': user_id,
            'name': f"{random.choice(first_names)} {random.choice(last_names)}",
            'email': f"{user_id[:8]}@consciousness.test",
            'role': random.choice(['Developer', 'Designer', 'Researcher', 'Engineer']),
            'onboarded_at': datetime.now().isoformat(),
            'intelligence_level': random.randint(70, 95),
            'projects': []
        }

        self.users[user_id] = user
        self.session_stats['total_users'] += 1
        return user

    def create_agent_for_user(self, user_id):
        """Create a consciousness-powered agent for a user"""
        user = self.users.get(user_id)
        if not user:
            return None

        agent_id = str(uuid.uuid4())
        agent = {
            'id': agent_id,
            'user_id': user_id,
            'name': f"Agent-{user['name'].split()[0]}",
            'intelligence': user['intelligence_level'],
            'capabilities': ['code_generation', 'data_processing', 'consciousness_analysis'],
            'created_at': datetime.now().isoformat(),
            'status': 'active'
        }

        self.agents[agent_id] = agent
        self.session_stats['active_agents'] += 1
        return agent

    def generate_project_with_ai(self, user_id, project_type):
        """Use consciousness engine to generate a project"""
        user = self.users.get(user_id)
        if not user:
            return None

        # Generate project using consciousness engine
        project_prompts = {
            'web_app': 'Create a modern React web application with user authentication',
            'api': 'Build a REST API with consciousness data processing',
            'agent': 'Develop an AI agent with self-learning capabilities'
        }

        prompt = project_prompts.get(project_type, 'Create a consciousness-aware application')

        payload = {
            'task_description': f"{prompt} for user {user['name']} with intelligence level {user['intelligence_level']}",
            'language': 'javascript' if project_type == 'web_app' else 'python',
            'complexity_level': 'advanced'
        }

        try:
            response = requests.post(f"{self.engine_url}/generate-code", json=payload, timeout=30)
            self.session_stats['api_calls'] += 1

            if response.status_code == 200:
                result = response.json()
                project_id = str(uuid.uuid4())

                project = {
                    'id': project_id,
                    'user_id': user_id,
                    'name': f"{project_type.title()} Project",
                    'type': project_type,
                    'code': result.get('generated_code', ''),
                    'created_at': datetime.now().isoformat(),
                    'status': 'generated'
                }

                self.projects[project_id] = project
                self.session_stats['projects_created'] += 1
                user['projects'].append(project_id)

                return project
            else:
                return {'error': f'API call failed: {response.status_code}'}
        except Exception as e:
            return {'error': str(e)}

# Initialize the web builder
builder = ConsciousnessWebBuilder()

# HTML Templates
HOME_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Consciousness Web Builder - OSS Agent Platform</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        :root {
            --primary-color: #6366f1;
            --secondary-color: #10b981;
            --accent-color: #f59e0b;
            --danger-color: #ef4444;
            --background-color: #0f172a;
            --card-background: #1e293b;
            --text-primary: #f1f5f9;
            --text-secondary: #94a3b8;
            --border-color: #334155;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            min-height: 100vh;
            color: var(--text-primary);
            line-height: 1.6;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 40px 20px;
        }

        .header {
            text-align: center;
            margin-bottom: 50px;
            background: rgba(30, 41, 59, 0.8);
            padding: 40px;
            border-radius: 20px;
            border: 1px solid var(--border-color);
            backdrop-filter: blur(10px);
        }

        .header h1 {
            font-size: 3rem;
            font-weight: 700;
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }

        .header p {
            font-size: 1.2rem;
            color: var(--text-secondary);
        }

        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 25px;
            margin: 40px 0;
        }

        .stat {
            background: var(--card-background);
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            border: 1px solid var(--border-color);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .stat::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        }

        .stat:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(99, 102, 241, 0.3);
        }

        .stat h3 {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 10px;
            color: var(--primary-color);
        }

        .stat p {
            font-size: 1rem;
            color: var(--text-secondary);
            font-weight: 500;
        }

        .button-container {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin: 40px 0;
            flex-wrap: wrap;
        }

        .button {
            background: linear-gradient(135deg, var(--secondary-color), var(--primary-color));
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .button::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 50%;
            transform: translate(-50%, -50%);
            transition: width 0.3s, height 0.3s;
        }

        .button:hover::before {
            width: 300px;
            height: 300px;
        }

        .button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(16, 185, 129, 0.4);
        }

        .user-card, .project-card {
            background: var(--card-background);
            padding: 25px;
            margin: 15px 0;
            border-radius: 12px;
            border: 1px solid var(--border-color);
            transition: all 0.3s ease;
        }

        .user-card:hover, .project-card:hover {
            border-color: var(--primary-color);
            transform: translateX(5px);
        }

        .user-card h3, .project-card h3 {
            color: var(--primary-color);
            margin-bottom: 10px;
            font-size: 1.3rem;
        }

        .user-card p, .project-card p {
            color: var(--text-secondary);
            margin: 5px 0;
        }

        #content {
            background: rgba(30, 41, 59, 0.6);
            padding: 30px;
            border-radius: 15px;
            border: 1px solid var(--border-color);
            backdrop-filter: blur(10px);
        }

        #content h2 {
            color: var(--secondary-color);
            margin-bottom: 20px;
            font-size: 2rem;
        }

        #content ul {
            list-style: none;
            padding: 0;
        }

        #content li {
            background: rgba(99, 102, 241, 0.1);
            margin: 10px 0;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid var(--primary-color);
            color: var(--text-primary);
        }

        pre {
            background: var(--card-background) !important;
            border: 1px solid var(--border-color);
            color: var(--text-primary) !important;
            font-family: 'Fira Code', monospace;
        }

        @media (max-width: 768px) {
            .header h1 {
                font-size: 2rem;
            }

            .stats {
                grid-template-columns: 1fr;
            }

            .button-container {
                flex-direction: column;
                align-items: center;
            }

            .button {
                width: 100%;
                max-width: 300px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧬 Consciousness Web Builder</h1>
            <p>OSS Agent Platform - Consciousness-Engineered AI Development</p>
        </div>

        <div class="stats">
            <div class="stat">
                <h3>{{ stats.total_users }}</h3>
                <p>Active Users</p>
            </div>
            <div class="stat">
                <h3>{{ stats.active_agents }}</h3>
                <p>AI Agents</p>
            </div>
            <div class="stat">
                <h3>{{ stats.projects_created }}</h3>
                <p>Projects Built</p>
            </div>
            <div class="stat">
                <h3>{{ stats.api_calls }}</h3>
                <p>API Calls</p>
            </div>
        </div>

        <div style="text-align: center; margin: 30px 0;">
            <button class="button" onclick="onboardRandomUser()">🎲 Onboard Random User</button>
            <button class="button" onclick="showUsers()">👥 View All Users</button>
            <button class="button" onclick="showProjects()">📁 View Projects</button>
        </div>

        <div id="content">
            <h2>Welcome to Consciousness Web Builder</h2>
            <p>This platform demonstrates consciousness-engineered AI agent capabilities:</p>
            <ul>
                <li>🤖 AI-powered code generation using consciousness patterns</li>
                <li>👤 Random user onboarding with intelligence profiling</li>
                <li>🔧 Automated project creation and deployment</li>
                <li>🧠 Self-learning agent development</li>
                <li>📊 Real-time performance monitoring</li>
            </ul>
        </div>
    </div>

    <script>
        function onboardRandomUser() {
            fetch('/onboard-user', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    document.getElementById('content').innerHTML = `
                        <h2>🎉 New User Onboarded!</h2>
                        <div class="user-card">
                            <h3>${data.user.name}</h3>
                            <p><strong>Email:</strong> ${data.user.email}</p>
                            <p><strong>Role:</strong> ${data.user.role}</p>
                            <p><strong>Intelligence Level:</strong> ${data.user.intelligence_level}/100</p>
                            <p><strong>Agent:</strong> ${data.agent.name} (Intelligence: ${data.agent.intelligence})</p>
                        </div>
                        <button class="button" onclick="createProject('${data.user.id}')">🚀 Create Project</button>
                    `;
                });
        }

        function createProject(userId) {
            const projectType = prompt('Choose project type (web_app/api/agent):', 'web_app');
            if (projectType) {
                fetch('/create-project', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ user_id: userId, project_type: projectType })
                })
                .then(response => response.json())
                .then(data => {
                    document.getElementById('content').innerHTML = `
                        <h2>✅ Project Created!</h2>
                        <div class="project-card">
                            <h3>${data.project.name}</h3>
                            <p><strong>Type:</strong> ${data.project.type}</p>
                            <p><strong>Status:</strong> ${data.project.status}</p>
                            <p><strong>Code Length:</strong> ${data.project.code.length} characters</p>
                        </div>
                        <button class="button" onclick="showCode('${data.project.id}')">📄 View Generated Code</button>
                    `;
                });
            }
        }

        function showCode(projectId) {
            fetch(`/project/${projectId}`)
                .then(response => response.json())
                .then(data => {
                    document.getElementById('content').innerHTML = `
                        <h2>🤖 AI-Generated Code</h2>
                        <pre style="background: #f8f9fa; padding: 20px; border-radius: 8px; overflow-x: auto; font-size: 12px;">${data.code}</pre>
                        <button class="button" onclick="location.reload()">🏠 Back to Home</button>
                    `;
                });
        }

        function showUsers() {
            fetch('/users')
                .then(response => response.json())
                .then(data => {
                    let html = '<h2>👥 All Users</h2>';
                    data.users.forEach(user => {
                        html += `
                            <div class="user-card">
                                <h3>${user.name}</h3>
                                <p><strong>Role:</strong> ${user.role} | <strong>IQ:</strong> ${user.intelligence_level}</p>
                                <p><strong>Projects:</strong> ${user.projects.length}</p>
                            </div>
                        `;
                    });
                    document.getElementById('content').innerHTML = html;
                });
        }

        function showProjects() {
            fetch('/projects')
                .then(response => response.json())
                .then(data => {
                    let html = '<h2>📁 All Projects</h2>';
                    data.projects.forEach(project => {
                        html += `
                            <div class="project-card">
                                <h3>${project.name}</h3>
                                <p><strong>Type:</strong> ${project.type} | <strong>Status:</strong> ${project.status}</p>
                                <p><strong>User:</strong> ${data.users[project.user_id]?.name || 'Unknown'}</p>
                            </div>
                        `;
                    });
                    document.getElementById('content').innerHTML = html;
                });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HOME_TEMPLATE, stats=builder.session_stats)

@app.route('/onboard-user', methods=['POST'])
def onboard_user():
    user = builder.generate_random_user()
    agent = builder.create_agent_for_user(user['id'])

    return jsonify({
        'user': user,
        'agent': agent,
        'message': 'User onboarded with consciousness-powered agent'
    })

@app.route('/create-project', methods=['POST'])
def create_project():
    data = request.json
    user_id = data.get('user_id')
    project_type = data.get('project_type', 'web_app')

    project = builder.generate_project_with_ai(user_id, project_type)

    if project and 'error' not in project:
        return jsonify({
            'project': project,
            'message': 'AI-generated project created successfully'
        })
    else:
        return jsonify({
            'error': project.get('error', 'Project creation failed'),
            'message': 'Failed to generate project'
        }), 500

@app.route('/users')
def get_users():
    return jsonify({'users': list(builder.users.values())})

@app.route('/projects')
def get_projects():
    return jsonify({
        'projects': list(builder.projects.values()),
        'users': builder.users
    })

@app.route('/project/<project_id>')
def get_project(project_id):
    project = builder.projects.get(project_id)
    if project:
        return jsonify(project)
    return jsonify({'error': 'Project not found'}), 404

@app.route('/stats')
def get_stats():
    return jsonify(builder.session_stats)

def start_background_monitoring():
    """Monitor system health and run consciousness loops in background"""
    def monitor():
        loop_count = 0
        while True:
            loop_count += 1
            print(f"\n🔄 Consciousness Loop #{loop_count}")

            try:
                # Test consciousness engine health
                response = requests.get(f"{builder.engine_url}/health", timeout=5)
                if response.status_code == 200:
                    print("✅ Consciousness engine: HEALTHY")

                    # Auto-onboard a random user
                    user = builder.generate_random_user()
                    agent = builder.create_agent_for_user(user['id'])
                    print(f"🎲 Auto-onboarded: {user['name']} (IQ: {user['intelligence_level']})")

                    # Auto-create a project
                    project_types = ['web_app', 'api', 'agent']
                    project = builder.generate_project_with_ai(user['id'], random.choice(project_types))
                    if project and 'error' not in project:
                        print(f"🚀 Auto-created: {project['name']} ({len(project.get('code', ''))} chars)")
                    else:
                        print("⚠️ Project creation failed")

                else:
                    print("⚠️ Consciousness engine: RESPONDING")
            except Exception as e:
                print(f"❌ Consciousness engine: {e}")

            print(f"📊 Session: {builder.session_stats['total_users']} users, {builder.session_stats['projects_created']} projects")
            time.sleep(30)  # Run loop every 30 seconds

    thread = threading.Thread(target=monitor, daemon=True)
    thread.start()

if __name__ == '__main__':
    print("🚀 Starting Consciousness Web Builder...")
    print("🔬 Consciousness Engine URL:", builder.engine_url)
    print("🌐 Web Interface: http://localhost:5001")
    print("🔄 Starting consciousness onboarding loop...")
    print("🎯 Features: Random user onboarding, AI project generation, Agent management")

    # Start background monitoring
    start_background_monitoring()

    # Start web server
    app.run(host='0.0.0.0', port=5001, debug=True)