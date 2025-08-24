# 🤖 CrewAI Problem Solving Research Agent

A powerful AI-driven research and problem-solving system built with CrewAI framework. This application analyzes problems, conducts research, and generates comprehensive solutions with multiple output formats including PDF downloads and Google Docs integration with automatic fallback to local files.

## ✨ Features

### 🔬 **Intelligent Research Agents**
- **Research Specialist**: Analyzes problems and creates comprehensive solution approaches
- **Document Publisher**: Formats results and creates shareable documents

### 🖥️ **Multiple Interfaces**
- **Command Line Interface**: Direct terminal interaction
- **Streamlit Web UI**: Modern web interface with PDF downloads
- **Google Docs Integration**: Automatic document creation in Google Docs

### 📄 **Output Formats**
- Local markdown files with timestamps
- PDF generation and download
- Google Docs with public sharing (with local fallback)
- Professional formatting with structured sections
- Automatic error handling and graceful degradation

## 🚀 Quick Start

### 1. Clone and Install
```bash
git clone <your-repo-url>
cd crewprob
pip install -r requirements.txt
```

### 2. Configure Environment
Copy the example environment file and add your API keys:
```bash
# Copy the example file
cp .env_example .env

# Edit .env with your actual API keys
nano .env  # or use your preferred editor
```

Required variables:
```bash
# Required: OpenAI API Key
OPENAI_API_KEY=your_openai_api_key_here

# Optional: For enhanced search capabilities
SERPER_API_KEY=your_serper_api_key_here

# Optional: For Google Docs integration (falls back to local files if not configured)
GOOGLE_SERVICE_ACCOUNT_PATH=./your-service-account.json
```

### 3. Run the Application

#### Option A: Streamlit Web UI (Recommended)
```bash
streamlit run streamlit_app.py
```
- Open browser to `http://localhost:8501`
- Enter your problem statement
- Download generated PDF reports

#### Option B: Command Line
```bash
PYTHONPATH=src python src/problem_solving_research_agent/main.py run
```

## 📋 Usage Examples

### Web Interface
1. Launch Streamlit: `streamlit run streamlit_app.py`
2. Enter problem: *"How to build a scalable microservices architecture?"*
3. Click "Generate Solution"
4. Download PDF report or view in browser

### Command Line
```bash
PYTHONPATH=src python src/problem_solving_research_agent/main.py run
# Enter: "Please find an approach for building UI using streamlit for CrewAI agents"
```

## 🔧 Advanced Configuration

### Google Docs Integration (Optional)
1. **Setup**: Follow instructions in `GOOGLE_SETUP.md`
2. **APIs**: Enable Google Docs API + Drive API in Google Cloud Console
3. **Service Account**: Create service account with Editor role
4. **Credentials**: Download JSON key and set `GOOGLE_SERVICE_ACCOUNT_PATH`
5. **Fallback**: If Google Docs fails, documents save locally automatically

**Note**: The application works fully without Google Docs - it will save to local files if Google API is unavailable.

### API Keys Setup
- **OpenAI**: Required for AI agents - Get from [OpenAI Platform](https://platform.openai.com/)
- **Serper**: Optional for web search - Get from [Serper.dev](https://serper.dev/)
- **Google**: Optional for Docs integration - See `GOOGLE_SETUP.md`

## 📁 Project Structure

```
crewprob/
├── src/problem_solving_research_agent/
│   ├── main.py                 # CLI entry point
│   ├── crew.py                 # CrewAI agents configuration
│   ├── config/
│   │   ├── agents.yaml         # Agent definitions
│   │   └── tasks.yaml          # Task configurations
│   └── tools/
│       ├── file_writer.py      # Local file creation
│       └── google_docs.py      # Google Docs integration
├── streamlit_app.py            # Web UI application
├── output/                     # Generated documents
├── requirements.txt            # All dependencies
├── .env_example               # Environment template (safe to commit)
├── .env                       # Your API keys (gitignored)
├── GOOGLE_SETUP.md            # Google API setup guide
└── README.md                  # This file
```

## 🛠️ Available Commands

### CLI Commands
```bash
# Basic problem solving
PYTHONPATH=src python src/problem_solving_research_agent/main.py run

# Training mode
PYTHONPATH=src python src/problem_solving_research_agent/main.py train <iterations> <filename>

# Testing mode  
PYTHONPATH=src python src/problem_solving_research_agent/main.py test <iterations> <model_name>

# Replay previous task
PYTHONPATH=src python src/problem_solving_research_agent/main.py replay <task_id>
```

### Web UI
```bash
# Launch Streamlit application
streamlit run streamlit_app.py
```

## 🔍 How It Works

1. **Input**: User provides a problem statement
2. **Research**: Research Specialist agent analyzes the problem
3. **Solution**: Agent creates detailed step-by-step approach
4. **Publishing**: Document Publisher formats and creates output
5. **Output**: Multiple formats available (PDF, Google Docs, local files)
6. **Resilience**: Automatic fallback ensures output is always generated

### Current Status
- ✅ **Core functionality**: Fully working
- ✅ **Local file output**: Always available
- ✅ **PDF generation**: Working in Streamlit UI
- ⚠️ **Google Docs**: May require IAM permission propagation (60+ minutes)
- ✅ **Fallback system**: Ensures no data loss

## 🐛 Troubleshooting

### Common Issues
- **Import Errors**: Ensure `PYTHONPATH=src` is used for CLI commands
- **API Errors**: Check your `.env` file has correct API keys
- **Google Docs 403 Error**: This is normal - the app automatically falls back to local files

### Google Docs Issues
- **403 Permission Error**: Service account needs time (up to 60 minutes) for IAM propagation
- **Scope Issues**: Ensure service account has `roles/editor` or document creation permissions
- **Automatic Fallback**: App continues working and saves files locally when Google Docs fails
- **No OAuth Required**: Uses service account authentication, not OAuth flow

### Dependencies
If you encounter dependency issues:
```bash
pip install --upgrade -r requirements.txt
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Make changes and test
4. Commit: `git commit -m "Add feature description"`
5. Push: `git push origin feature-name`
6. Create Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with [CrewAI](https://crewai.io/) framework
- UI powered by [Streamlit](https://streamlit.io/)
- PDF generation using [ReportLab](https://www.reportlab.com/)
- Google APIs integration
