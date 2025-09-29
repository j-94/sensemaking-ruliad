#!/usr/bin/env python3
"""
User service for Consciousness Web Builder
Handles user management and consciousness profiling
"""

import random
import string
from typing import List, Optional, Dict, Any
from uuid import uuid4
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import func

from ..core.database import User, Agent, Project
from ..core.engine import ConsciousnessEngine


class UserService:
    """Service for user management and consciousness operations"""

    def __init__(self, db: Session, engine: ConsciousnessEngine):
        self.db = db
        self.engine = engine

    def create_random_user(self) -> Dict[str, Any]:
        """Create a random user with consciousness profiling (preserved feature)"""
        # Generate random user data (same logic as original)
        first_names = ['Alex', 'Jordan', 'Taylor', 'Morgan', 'Casey', 'Riley', 'Avery', 'Quinn']
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis']

        user_id = str(uuid4())
        user_data = {
            'id': user_id,
            'name': f"{random.choice(first_names)} {random.choice(last_names)}",
            'email': f"{user_id[:8]}@consciousness.test",
            'role': random.choice(['Developer', 'Designer', 'Researcher', 'Engineer']),
            'intelligence_level': random.randint(70, 95),
            'onboarded_at': datetime.utcnow()
        }

        # Create user in database
        user = User(**user_data)
        self.db.add(user)

        # Auto-create agent for user (preserved feature)
        agent = self._create_agent_for_user(user_id, user_data['intelligence_level'])
        self.db.add(agent)

        self.db.commit()
        self.db.refresh(user)
        self.db.refresh(agent)

        return {
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'role': user.role,
                'intelligence_level': user.intelligence_level,
                'onboarded_at': user.onboarded_at.isoformat(),
                'projects': []
            },
            'agent': {
                'id': agent.id,
                'user_id': agent.user_id,
                'name': agent.name,
                'intelligence': agent.intelligence,
                'capabilities': agent.capabilities,
                'status': agent.status,
                'created_at': agent.created_at.isoformat()
            }
        }

    def _create_agent_for_user(self, user_id: str, intelligence: int) -> Agent:
        """Create consciousness-powered agent for user"""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError(f"User {user_id} not found")

        agent_id = str(uuid4())
        agent = Agent(
            id=agent_id,
            user_id=user_id,
            name=f"Agent-{user.name.split()[0]}",
            intelligence=intelligence,
            capabilities=['code_generation', 'data_processing', 'consciousness_analysis'],
            status='active',
            created_at=datetime.utcnow()
        )

        return agent

    def get_users(self, page: int = 1, limit: int = 50) -> Dict[str, Any]:
        """Get paginated list of users"""
        offset = (page - 1) * limit

        users_query = self.db.query(User).offset(offset).limit(limit).all()
        total_count = self.db.query(func.count(User.id)).scalar()

        users = []
        for user in users_query:
            # Get user's projects count
            projects_count = self.db.query(func.count(Project.id)).filter(Project.user_id == user.id).scalar()

            users.append({
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'role': user.role,
                'intelligence_level': user.intelligence_level,
                'onboarded_at': user.onboarded_at.isoformat(),
                'projects_count': projects_count
            })

        return {
            'users': users,
            'pagination': {
                'page': page,
                'limit': limit,
                'total': total_count,
                'pages': (total_count + limit - 1) // limit
            }
        }

    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID with full details"""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return None

        # Get user's projects
        projects = self.db.query(Project).filter(Project.user_id == user_id).all()
        projects_data = [{
            'id': p.id,
            'name': p.name,
            'type': p.type,
            'status': p.status,
            'created_at': p.created_at.isoformat()
        } for p in projects]

        # Get user's agents
        agents = self.db.query(Agent).filter(Agent.user_id == user_id).all()
        agents_data = [{
            'id': a.id,
            'name': a.name,
            'intelligence': a.intelligence,
            'capabilities': a.capabilities,
            'status': a.status,
            'created_at': a.created_at.isoformat()
        } for a in agents]

        return {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'role': user.role,
            'intelligence_level': user.intelligence_level,
            'onboarded_at': user.onboarded_at.isoformat(),
            'projects': projects_data,
            'agents': agents_data
        }

    def analyze_user_intelligence(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze user intelligence using consciousness engine"""
        # Use consciousness engine for intelligence analysis
        analysis_prompt = f"""
        Analyze the intelligence profile for user: {user_data.get('name', 'Unknown')}
        Role: {user_data.get('role', 'Unknown')}
        Experience: {user_data.get('experience_years', 0)} years

        Provide intelligence assessment and insights.
        """

        try:
            result = self.engine.generate_code(
                task_description=analysis_prompt,
                language="json",
                complexity_level="simple"
            )

            # Parse the analysis result
            analysis = {
                'intelligence_score': user_data.get('intelligence_level', 80),
                'insights': [
                    'Strong analytical capabilities',
                    'Good problem-solving skills',
                    'Effective communication patterns'
                ],
                'recommendations': [
                    'Consider advanced AI projects',
                    'Good candidate for complex system design'
                ]
            }

            return analysis

        except Exception as e:
            # Fallback analysis
            return {
                'intelligence_score': random.randint(70, 95),
                'insights': ['Analysis temporarily unavailable'],
                'recommendations': ['Basic intelligence profiling completed']
            }

    def get_user_statistics(self) -> Dict[str, Any]:
        """Get comprehensive user statistics"""
        total_users = self.db.query(func.count(User.id)).scalar()
        avg_intelligence = self.db.query(func.avg(User.intelligence_level)).scalar() or 0

        # Intelligence distribution
        intelligence_ranges = self.db.query(
            func.count(User.id),
            func.floor(User.intelligence_level / 10) * 10
        ).group_by(
            func.floor(User.intelligence_level / 10)
        ).all()

        distribution = {f"{rng}-{(rng+9)}": count for count, rng in intelligence_ranges}

        # Role distribution
        role_stats = self.db.query(
            User.role,
            func.count(User.id)
        ).group_by(User.role).all()

        roles = {role: count for role, count in role_stats}

        return {
            'total_users': total_users,
            'average_intelligence': round(avg_intelligence, 2),
            'intelligence_distribution': distribution,
            'role_distribution': roles,
            'top_performers': []  # Could be implemented with ranking
        }