# AI Coach Chat Feature

## 🎯 Overview

The AI Coach now supports **interactive conversational analysis** with smart context management and conversation summarization. This allows you to have natural follow-up conversations about your training data instead of just getting a single analysis.

## 🚀 Key Features

### ✅ **In-Memory Session Management**
- Maintains conversation history throughout the session
- Preserves context of your workout data across all questions
- Smart token management to stay within API limits

### ✅ **Smart Context Summarization** 
- Automatically summarizes long conversations to save tokens
- Preserves important coaching insights while condensing older messages
- Maintains conversation flow without losing context

### ✅ **Multiple Usage Modes**
- **Regular Analysis**: Traditional single-shot analysis (unchanged)
- **Analysis + Chat**: Get analysis then ask follow-up questions  
- **Chat Only**: Jump straight into conversation mode

## 📁 New Files Added

```
src/
├── chat_session.py          # Core chat functionality
├── simple_openai_client.py  # Enhanced with chat support
└── ...

enhanced_main.py             # Main script with chat options
chat_demo.py                # Standalone chat demo
test_chat.py                # Test suite for chat functionality
```

## 🎮 Usage Examples

### **Option 1: Enhanced Main Script**

```bash
# Traditional analysis (unchanged)
python enhanced_main.py --user bryashko --limit 5

# Analysis followed by interactive chat
python enhanced_main.py --user bryashko --limit 5 --chat

# Jump directly to chat mode
python enhanced_main.py --user bryashko --chat-only

# Chat with initial feedback
python enhanced_main.py --user bryashko --chat --feedback "Feeling strong this week"
```

### **Option 2: Standalone Chat Demo**

```bash
# Interactive chat demo
python chat_demo.py --user bryashko --limit 5

# With initial feedback
python chat_demo.py --user bryashko --limit 3 --feedback "Ready for race day"
```

## 💬 Chat Commands

During chat sessions, you can use special commands:

- **`quit`**, **`exit`**, **`q`** - End the chat session
- **`stats`** - Show conversation statistics (messages, tokens, duration)
- Any other text - Ask a follow-up question about your training

## 🧠 How It Works

### **Context Preservation**
```python
# The AI remembers because we send full context every time
messages = [
    {"role": "system", "content": "You are an AI running coach..."},
    {"role": "user", "content": "My workout data: {...}"},
    {"role": "assistant", "content": "Initial analysis..."},
    {"role": "user", "content": "What about nutrition?"},
    {"role": "assistant", "content": "For nutrition..."},
    {"role": "user", "content": "Current question"}  # New question
]
```

### **Smart Summarization**
When conversations get long (>20 messages or >3000 tokens):
1. Keep system prompt + initial workout context
2. Summarize middle part of conversation  
3. Keep recent 8 messages
4. Continue with condensed history

### **Token Management**
- Estimates ~4 characters = 1 token
- Monitors conversation length
- Automatically summarizes when needed
- Stays within 4K token limits

## 🔧 Technical Architecture

### **Core Classes**

#### `ChatMessage`
```python
class ChatMessage:
    def __init__(self, role: str, content: str, timestamp: float)
    def estimate_tokens(self) -> int
    def to_dict(self) -> Dict
```

#### `AICoachChatSession`
```python
class AICoachChatSession:
    def __init__(self, ai_client, user_id, activities, initial_feedback)
    def start_analysis(self) -> str                    # Initial analysis
    def ask_question(self, question: str) -> str       # Follow-up questions
    def get_conversation_stats(self) -> Dict           # Statistics
    def export_conversation(self) -> Dict              # Export for saving
```

#### `ChatSessionManager`
```python
class ChatSessionManager:
    def create_session(self, ai_client, user_id, activities, feedback) -> AICoachChatSession
    def get_session(self, user_id) -> AICoachChatSession
    def end_session(self, user_id) -> Dict
    def list_active_sessions(self) -> List[str]
```

## 📊 Example Conversation Flow

```
🤖 AI Coach: Based on your 5 recent workouts, here's my analysis...
   [Initial comprehensive analysis]

🏃 You: What should I focus on for nutrition before the Dresden half marathon?

🤖 AI Coach: For the Dresden half marathon on October 26th, based on your recent 
   training pattern, I recommend... [Specific nutrition advice]

🏃 You: What pace should I target during the race?

🤖 AI Coach: Looking at your recent long run of 22.1km and your current fitness 
   level, I suggest... [Pace strategy based on your data]

🏃 You: stats

📊 Statistics: 6 messages, 1,847 tokens, 3.2 min

🏃 You: quit

📊 Session completed: 6 messages, 3.2 minutes
```

## 🎯 Benefits Over Single Analysis

### **Traditional Approach:**
- One question → One comprehensive answer
- Can't drill down into specific aspects  
- Have to re-run with new prompts for follow-ups

### **Chat Approach:**
- Natural conversation flow
- Can explore specific topics in depth
- AI remembers context from workout data
- Can clarify or expand on previous answers
- More personalized and interactive experience

## 🔮 Future Enhancements

### **Planned Features:**
- **Persistent Sessions**: Save/load conversations
- **Web Interface**: Browser-based chat
- **Voice Integration**: Speech-to-text questions
- **Training Plan Builder**: Interactive plan creation
- **Race Day Assistant**: Real-time advice during races

### **Possible Extensions:**
- **Multi-Modal**: Analyze uploaded photos/videos
- **Calendar Integration**: Training schedule management  
- **Social Features**: Share insights with other runners
- **Performance Tracking**: Long-term progress analysis

## 🧪 Testing

Run the test suite to verify everything works:

```bash
# Test chat functionality
python test_chat.py

# Test with mock data (no API calls)
python test_chat.py
```

## 💰 Cost Considerations

**Token Usage:**
- Each chat message sends FULL conversation history
- Longer conversations = more expensive API calls
- Smart summarization helps manage costs
- Typical session: 1,000-3,000 tokens

**Optimization Strategies:**
- Conversation summarization after 20 messages
- Token estimation and monitoring
- Graceful degradation for long sessions

## 🚀 Getting Started

1. **Use existing setup** (no additional config needed)
2. **Try enhanced mode**:
   ```bash
   python enhanced_main.py --user <your_user_id> --chat
   ```
3. **Ask follow-up questions** about training, nutrition, pacing, etc.
4. **Type `stats`** to monitor token usage
5. **Type `quit`** when done

The chat feature seamlessly integrates with your existing OAuth setup and workout data - just add the `--chat` flag to any analysis!