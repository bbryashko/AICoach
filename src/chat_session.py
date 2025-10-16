"""
AI Coach Chat Session Management
Provides conversational interface with context management and smart summarization
"""

import json
import time
from typing import List, Dict, Optional, Any
from simple_openai_client import SimpleOpenAIClient


class ChatMessage:
    """Represents a single message in the conversation"""
    
    def __init__(self, role: str, content: str, timestamp: Optional[float] = None):
        self.role = role  # 'system', 'user', 'assistant'
        self.content = content
        self.timestamp = timestamp or time.time()
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp
        }
    
    def estimate_tokens(self) -> int:
        """Rough token estimation (4 chars ≈ 1 token)"""
        return len(self.content) // 4


class AICoachChatSession:
    """
    Manages conversational AI coaching sessions with context preservation
    and smart summarization to handle long conversations
    """
    
    def __init__(self, ai_client: SimpleOpenAIClient, user_id: str, 
                 activities: List[Dict], initial_feedback: str = ""):
        self.ai_client = ai_client
        self.user_id = user_id
        self.activities = activities
        self.initial_feedback = initial_feedback
        self.messages: List[ChatMessage] = []
        self.created_at = time.time()
        self.max_tokens = 3000  # Leave room for response in 4K model
        self.max_messages_before_summary = 20
        
        # Initialize with system context
        self._initialize_session()
    
    def _initialize_session(self):
        """Set up initial system context"""
        system_prompt = self._build_system_prompt()
        initial_context = self._build_initial_context()
        
        # Add system message
        self.messages.append(ChatMessage("system", system_prompt))
        
        # Add initial workout context
        self.messages.append(ChatMessage("user", initial_context))
    
    def _build_system_prompt(self) -> str:
        """Create the AI coach personality and instructions"""
        return """You are an experienced AI running coach specializing in half-marathon preparation. 

Your personality:
- Professional but encouraging and motivational
- Data-driven but also considers subjective runner feedback
- Focuses on practical, actionable advice
- Remembers context from previous parts of the conversation
- Personalizes advice based on the runner's specific workout data

Your capabilities:
- Analyze workout patterns and performance trends
- Provide training recommendations and race preparation
- Answer specific questions about running technique, nutrition, recovery
- Create personalized training plans
- Help with race strategy and goal setting

Always maintain context of the runner's specific workout data and previous conversation when responding."""
    
    def _build_initial_context(self) -> str:
        """Create initial context with workout data"""
        context = f"""RUNNER PROFILE: {self.user_id}

WORKOUT DATA FOR ANALYSIS:
{json.dumps(self.activities, indent=2)}

INITIAL RUNNER FEEDBACK: "{self.initial_feedback}"

CONTEXT: This runner is preparing for the Dresden half marathon on October 26th. 
Please analyze their workout data and be ready to answer follow-up questions about their training."""
        
        return context
    
    def start_analysis(self) -> str:
        """Perform initial workout analysis and return response"""
        analysis_prompt = """Based on the workout data provided, please give me a comprehensive analysis including:

1. Overall performance analysis across all activities
2. Training pattern assessment (intensity, volume, recovery balance)
3. Performance trends and progression
4. Specific recommendations for Dresden half marathon preparation
5. Proposed training plan for the next 2 weeks before the race

Please be specific and actionable in your recommendations."""
        
        return self.ask_question(analysis_prompt, is_initial=True)
    
    def ask_question(self, question: str, is_initial: bool = False) -> str:
        """Ask a follow-up question in the conversation"""
        
        # Add user question to conversation
        self.messages.append(ChatMessage("user", question))
        
        # Check if we need to manage conversation length
        if len(self.messages) > self.max_messages_before_summary:
            self._manage_conversation_length()
        
        # Build message array for OpenAI
        openai_messages = self._build_openai_messages()
        
        # Check token estimation
        total_tokens = sum(msg.estimate_tokens() for msg in self.messages)
        if total_tokens > self.max_tokens:
            self._summarize_conversation()
            openai_messages = self._build_openai_messages()
        
        # Get AI response
        try:
            response = self._send_to_openai(openai_messages)
            
            # Add AI response to conversation history
            self.messages.append(ChatMessage("assistant", response))
            
            return response
            
        except Exception as e:
            error_msg = f"Error getting AI response: {e}"
            self.messages.append(ChatMessage("assistant", error_msg))
            return error_msg
    
    def _build_openai_messages(self) -> List[Dict[str, str]]:
        """Convert internal messages to OpenAI format"""
        return [msg.to_dict() for msg in self.messages]
    
    def _send_to_openai(self, messages: List[Dict[str, str]]) -> str:
        """Send messages to OpenAI using existing client method"""
        # Use the existing _chat_completion method but with custom messages
        return self.ai_client._chat_completion_with_messages(messages)
    
    def _manage_conversation_length(self):
        """Manage conversation length when it gets too long"""
        if len(self.messages) > self.max_messages_before_summary:
            print(f"💭 Managing conversation length ({len(self.messages)} messages)...")
            self._summarize_conversation()
    
    def _summarize_conversation(self):
        """Summarize older parts of conversation to save tokens"""
        if len(self.messages) <= 5:  # Keep minimum messages
            return
        
        # Keep system message, initial context, and recent messages
        system_msg = self.messages[0]  # System prompt
        initial_context = self.messages[1]  # Initial workout data
        recent_messages = self.messages[-8:]  # Keep last 8 messages
        
        # Messages to summarize (everything in between)
        messages_to_summarize = self.messages[2:-8]
        
        if not messages_to_summarize:
            return
        
        # Create summarization prompt
        conversation_text = "\n".join([
            f"{msg.role.upper()}: {msg.content}" 
            for msg in messages_to_summarize
        ])
        
        summary_prompt = f"""Please summarize this conversation between a runner and their AI coach. Keep it concise but preserve key insights, recommendations, and important context:

{conversation_text}

Provide a 2-3 sentence summary that captures the main topics discussed and any important coaching advice given."""
        
        try:
            # Get summary from AI
            summary_messages = [
                {"role": "system", "content": "You are a helpful assistant that summarizes conversations."},
                {"role": "user", "content": summary_prompt}
            ]
            
            summary = self._send_to_openai(summary_messages)
            
            # Create new conversation history
            summary_message = ChatMessage("assistant", f"[CONVERSATION SUMMARY]: {summary}")
            
            # Rebuild messages array
            self.messages = [system_msg, initial_context, summary_message] + recent_messages
            
            print(f"✅ Conversation summarized: {len(messages_to_summarize)} messages → 1 summary")
            
        except Exception as e:
            print(f"⚠️ Could not summarize conversation: {e}")
            # Fallback: just keep recent messages
            self.messages = [system_msg, initial_context] + recent_messages[-10:]
    
    def get_conversation_stats(self) -> Dict[str, Any]:
        """Get statistics about the current conversation"""
        total_tokens = sum(msg.estimate_tokens() for msg in self.messages)
        user_messages = [msg for msg in self.messages if msg.role == "user"]
        assistant_messages = [msg for msg in self.messages if msg.role == "assistant"]
        
        return {
            "total_messages": len(self.messages),
            "user_messages": len(user_messages),
            "assistant_messages": len(assistant_messages),
            "estimated_tokens": total_tokens,
            "session_duration_minutes": (time.time() - self.created_at) / 60,
            "user_id": self.user_id,
            "activities_count": len(self.activities)
        }
    
    def export_conversation(self) -> Dict[str, Any]:
        """Export conversation for saving/analysis"""
        return {
            "user_id": self.user_id,
            "created_at": self.created_at,
            "activities": self.activities,
            "initial_feedback": self.initial_feedback,
            "messages": [msg.to_dict() for msg in self.messages],
            "stats": self.get_conversation_stats()
        }


class ChatSessionManager:
    """
    Manages multiple chat sessions for different users
    """
    
    def __init__(self):
        self.active_sessions: Dict[str, AICoachChatSession] = {}
    
    def create_session(self, ai_client: SimpleOpenAIClient, user_id: str, 
                      activities: List[Dict], initial_feedback: str = "") -> AICoachChatSession:
        """Create a new chat session for a user"""
        session = AICoachChatSession(ai_client, user_id, activities, initial_feedback)
        self.active_sessions[user_id] = session
        return session
    
    def get_session(self, user_id: str) -> Optional[AICoachChatSession]:
        """Get existing session for a user"""
        return self.active_sessions.get(user_id)
    
    def end_session(self, user_id: str) -> Optional[Dict[str, Any]]:
        """End a session and return conversation export"""
        session = self.active_sessions.pop(user_id, None)
        if session:
            return session.export_conversation()
        return None
    
    def list_active_sessions(self) -> List[str]:
        """List all active session user IDs"""
        return list(self.active_sessions.keys())
    
    def get_session_stats(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get statistics for a specific session"""
        session = self.get_session(user_id)
        if session:
            return session.get_conversation_stats()
        return None