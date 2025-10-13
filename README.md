# 🤖 AI Coach - Strava + OpenAI Integration

An intelligent fitness coach that combines Strava workout data with AI analysis to provide personalized training insights, recommendations, and coaching advice.

## 🏗️ Project Structure

```
AICoach/
├── src/                          # Main source code
│   ├── __init__.py
│   ├── config.py                 # Configuration management
│   ├── simple_openai_client.py   # OpenAI client (HTTP-based)
│   ├── openai_client.py          # OpenAI client (library-based)
│   ├── ai_coach_integration.py   # Full AI Coach integration
│   └── config_template.py        # Configuration template
├── examples/                     # Usage examples and demos
│   ├── __init__.py
│   ├── quick_start_demo.py       # Quick start example
│   ├── secure_demo.py            # Secure demo with env variables
│   └── usage_examples.py         # Comprehensive usage examples
├── tests/                        # Test files
│   ├── __init__.py
│   ├── test_openai.py            # OpenAI client tests
│   ├── test_correct_openai.py    # OpenAI syntax tests
│   ├── test_openai_credits.py    # OpenAI credit tests
│   ├── simple_test.py            # Simple API tests
│   └── token_helper.py           # Strava token helper
├── certs/                        # SSL certificates
├── .env.template                 # Environment variables template
├── .gitignore                    # Git ignore rules
├── requirements.txt              # Python dependencies
├── strava_api_test.py           # Original Strava API test
└── README.md                    # This file
```

## 🚀 Quick Start

1. **Setup Environment**
   ```bash
   # Clone the repository
   git clone https://github.com/bbryashko/AICoach.git
   cd AICoach
   
   # Create virtual environment
   python -m venv .venv
   .venv\\Scripts\\activate  # Windows
   # or
   source .venv/bin/activate  # Linux/Mac
   
   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Configure API Keys**
   ```bash
   # Copy environment template
   copy .env.template .env
   
   # Edit .env with your API keys
   # STRAVA_TOKEN=your_strava_token_here
   # OPENAI_API_KEY=your_openai_api_key_here
   ```

3. **Run Examples**
   ```bash
   # Quick start demo
   python examples/quick_start_demo.py
   
   # Secure demo (recommended for production)
   python examples/secure_demo.py
   ```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `STRAVA_TOKEN` | Strava API access token | Required |
| `STRAVA_BASE_URL` | Strava API base URL | `https://www.strava.com/api/v3` |
| `OPENAI_API_KEY` | OpenAI API key | Required |
| `OPENAI_BASE_URL` | OpenAI API base URL | `https://api.openai.com/v1` |
| `OPENAI_MODEL` | OpenAI model to use | `gpt-4o` |
| `USE_PROXY` | Enable proxy support | `false` |
| `VERIFY_SSL` | Enable SSL verification | `false` |

### Getting API Keys

**Strava API:**
1. Go to https://www.strava.com/settings/api
2. Create an application
3. Get your access token

**OpenAI API:**
1. Go to https://platform.openai.com/
2. Create an account
3. Generate an API key

## 🏃 Features

### Core Functionality
- **Workout Analysis**: AI-powered analysis of your Strava activities
- **Training Recommendations**: Personalized training advice based on your data
- **Recovery Guidance**: Smart recovery recommendations
- **Progress Tracking**: Monitor your fitness progress over time
- **Nutrition Advice**: Personalized nutrition recommendations

### AI Models Supported
- GPT-4o (recommended for best results)
- GPT-4
- GPT-3.5-turbo

### Security Features
- ✅ All API keys stored as environment variables
- ✅ No sensitive data in source code
- ✅ Safe to commit to public repositories
- ✅ `.env` files excluded from git

## 📚 Usage Examples

### Basic Workout Analysis
```python
from src.simple_openai_client import SimpleOpenAIClient
from src.config import get_config

config = get_config()
ai_client = SimpleOpenAIClient(
    config.OPENAI_API_KEY, 
    config.OPENAI_MODEL, 
    config.OPENAI_BASE_URL
)

# Analyze workout with AI
analysis = ai_client.analyze_workout_data(workout_data)
print(analysis)
```

### Full AI Coach Integration
```python
from src.ai_coach_integration import AICoach

coach = AICoach(strava_token, openai_api_key)

# Get latest workout analysis
analysis = coach.analyze_latest_workout()

# Generate training plan
plan = coach.get_personalized_training_plan("Train for half marathon")

# Get recovery recommendations
recovery = coach.get_recovery_recommendations()
```

## 🧪 Testing

Run tests from the project root:
```bash
# Test OpenAI integration
python tests/test_openai.py

# Test Strava token
python tests/token_helper.py

# Test API credits
python tests/test_openai_credits.py
```

## 🔒 Security Best Practices

1. **Never commit API keys** - Always use environment variables
2. **Use .env files** - Keep sensitive data out of source code
3. **Enable SSL verification** - Set `VERIFY_SSL=true` in production
4. **Rotate API keys regularly** - Update tokens periodically
5. **Monitor API usage** - Keep track of OpenAI credit consumption

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Troubleshooting

### Common Issues

**Import Errors:**
- Make sure you're running from the project root directory
- Check that the virtual environment is activated

**API Key Errors:**
- Verify your `.env` file has the correct keys
- Check that environment variables are loaded properly

**SSL Errors:**
- Set `VERIFY_SSL=false` in development
- Use proper certificates in production

### Getting Help

1. Check the examples in the `examples/` directory
2. Review the test files in `tests/` for usage patterns
3. Open an issue on GitHub for bugs or feature requests

## 🎯 Roadmap

- [ ] Web interface for easier interaction
- [ ] Advanced analytics and trends
- [ ] Integration with other fitness platforms
- [ ] Mobile app support
- [ ] Community features and sharing

---

Happy training! 🏃‍♂️💪