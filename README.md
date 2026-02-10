# RsChat_Boot_AI - Free AI Assistant for Students

A beautiful web-based AI chatbot powered by AWS Bedrock, designed specifically for students. Features multiple AI models, custom prompt engineering, and an intuitive user interface.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)
![AWS](https://img.shields.io/badge/AWS-Bedrock-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

- 🤖 **Multiple AI Models** - Amazon Nova, Claude, Llama, and more
- 🎯 **Prompt Engineering** - 7 preset prompt types + custom prompts
- 📊 **Performance Tracking** - Token counter, message count, response time
- 🎨 **Beautiful UI/UX** - Modern, responsive design
- 🔄 **Reset Function** - Clear chat and refresh session
- 🆓 **Free for Students** - Educational purpose

## 🚀 Quick Start

### Prerequisites

1. Python 3.8 or higher
2. AWS Account with Bedrock access
3. AWS credentials configured

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/RsChat_Boot_AI.git
cd RsChat_Boot_AI
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up AWS credentials:
```bash
# Option 1: Environment variables
set AWS_ACCESS_KEY_ID=your_access_key
set AWS_SECRET_ACCESS_KEY=your_secret_key

# Option 2: AWS CLI
aws configure
```

4. Run the application:
```bash
python app.py
```

5. Open browser:
```
http://localhost:5000
```

## 📖 Usage

### Model Selection
Choose from multiple AI models:
- Amazon Nova Lite (Fast & Efficient)
- Amazon Nova Pro (Balanced)
- Claude 3 Haiku (Anthropic)
- Llama 3 (Meta)

### Prompt Engineering

**Preset Prompts:**
- General Response
- Simple (For Students)
- Detailed Explanation
- Brief & Concise
- Step-by-Step Guide
- Creative Response
- Technical & Precise

**Custom Prompts:**
1. Click "Custom Prompt" button
2. Enter your instructions (e.g., "Act as a teacher and explain with examples")
3. Ask your question
4. AI follows your custom instructions!

### Example Custom Prompts

```
"Explain this like I'm 10 years old with simple examples"
"Act as a coding tutor and provide code examples"
"Be encouraging and motivational in your response"
"Answer in bullet points with key takeaways"
```

## 🛠️ Configuration

### Change Default Model

Edit `app.py`:
```python
generator = BedrockTextGenerator(
    region='us-east-1', 
    model_id='amazon.nova-lite-v1:0'
)
```

### Adjust Token Limits

Edit `bedrock_text_generator.py`:
```python
def generate_text(self, question, max_tokens=1000, timeout=30):
```

## 📁 Project Structure

```
AWS_BEDROCK_PROJECT/
├── app.py                      # Flask application
├── bedrock_text_generator.py   # AWS Bedrock integration
├── check_credentials.py        # AWS credentials checker
├── check_models.py            # List available models
├── requirements.txt           # Python dependencies
├── templates/
│   └── index.html            # Web UI
├── static/                   # Static files (if any)
└── README.md                # This file
```

## 🔒 Security

- Never commit AWS credentials to GitHub
- Use `.env` file for sensitive data (already in .gitignore)
- Follow AWS IAM best practices
- Rotate credentials regularly

## 📋 Requirements

```
boto3>=1.34.0
flask>=2.3.0
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- AWS Bedrock for AI models
- Flask for web framework
- Font Awesome for icons

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Made with ❤️ for Students**
