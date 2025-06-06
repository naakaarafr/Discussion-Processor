# Discussion Processor

**Created by: naakaarafr**

A powerful AI-driven system that transforms newsgroup discussions and online conversations into natural, movie-style dialogue while maintaining the essence and flow of the original conversation.

## 🎯 Overview

Discussion Processor uses a multi-agent AI crew system to analyze, filter, and transform discussion content through a sophisticated pipeline:

1. **Spam Detection** - Filters out inappropriate content, advertisements, and spam
2. **Discussion Analysis** - Extracts key arguments and participant positions  
3. **Script Writing** - Transforms conversations into natural movie-style dialogue
4. **Text Formatting** - Cleans and professionally formats the output
5. **Quality Scoring** - Evaluates the transformation quality on a 1-10 scale

## ✨ Features

- **Multi-Agent AI System** - Specialized agents for each processing stage
- **Content Filtering** - Advanced spam and inappropriate content detection
- **Natural Dialogue Generation** - Converts discussions to engaging movie-style scripts
- **Quality Assessment** - Comprehensive scoring across 10 evaluation criteria
- **File Processing** - Support for both direct input and file-based processing
- **Comprehensive Logging** - Detailed processing logs and error tracking
- **Professional Output** - Clean, formatted results saved to organized directories

## 🔧 Requirements

### Dependencies
```
crewai
langchain-google-genai
python-dotenv
pathlib
```

### Environment Setup
- **Google API Key** - Required for Gemini LLM integration
- Python 3.8+

## 📦 Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd discussion-processor
```

2. **Install dependencies**
```bash
pip install crewai langchain-google-genai python-dotenv
```

3. **Set up environment variables**

Create a `.env` file in the project root:
```env
GOOGLE_API_KEY=your_google_api_key_here
```

Or set environment variables directly:
```bash
export GOOGLE_API_KEY="your_google_api_key_here"
```

## 🚀 Usage

### Command Line Interface

**Basic usage with sample discussion:**
```bash
python main.py
# or
python main.py --demo
```

**Process from file:**
```bash
python main.py --file discussion.txt
```

**Advanced options:**
```bash
python main.py --file input.txt --no-save --no-logs
```

### Programmatic Usage

```python
from crew import NewsGroupCrew

# Initialize with discussion content
discussion_content = """
John: I think the new policy is reasonable.
Sarah: I disagree, it doesn't go far enough.
Mike: We need to consider the economic impact.
"""

crew = NewsGroupCrew(discussion_content)

# Process the discussion
result = crew.process_discussion(save_output=True, save_logs=True)

if result["status"] == "success":
    print(f"Generated dialogue: {result['dialogue']}")
    print(f"Quality score: {result['score']}/10")
```

### Processing from File

```python
crew = NewsGroupCrew("dummy content")
result = crew.process_from_file("my_discussion.txt")
```

## 📋 Command Line Options

| Option | Description |
|--------|-------------|
| `--file`, `-f` | Input file containing discussion content |
| `--no-save` | Don't save output files to disk |
| `--no-logs` | Don't save processing logs |
| `--demo` | Run with built-in sample discussion |

## 🏗️ Project Structure

```
discussion-processor/
├── agents.py              # AI agent definitions and configurations
├── crew.py               # Main crew orchestration and processing pipeline
├── tasks.py              # Task definitions for each processing stage
├── tools.py              # Utility classes for text processing and file management
├── main.py               # Command-line interface and entry point
├── sample_discussion.txt # Example discussion for testing
├── .env                  # Environment variables (create this)
├── output/               # Generated dialogue files (auto-created)
└── logs/                 # Processing logs (auto-created)
```

## 🤖 AI Agents

### 1. Spam Filter Agent
- **Role**: Content quality gatekeeper
- **Function**: Identifies spam, advertisements, and inappropriate content
- **Output**: PASS/STOP decision with reasoning

### 2. Discussion Analyst
- **Role**: Conversation analyzer
- **Function**: Extracts key arguments and participant positions
- **Output**: Structured analysis of discussion points

### 3. Script Writer Agent
- **Role**: Dialogue creator
- **Function**: Transforms analysis into natural movie-style dialogue
- **Output**: Clean script format with speaker names and dialogue

### 4. Text Formatter
- **Role**: Content cleaner
- **Function**: Removes stage directions and formatting artifacts
- **Output**: Professionally formatted, clean dialogue

### 5. Quality Scorer
- **Role**: Quality assessor
- **Function**: Evaluates dialogue across 10 quality dimensions
- **Output**: Numerical score (1-10) with detailed feedback

## 📊 Quality Scoring Criteria

The system evaluates generated dialogue across 10 dimensions:

1. **Clarity** - How understandable is the exchange?
2. **Relevance** - Do responses stay on topic?
3. **Conciseness** - Free of unnecessary redundancy?
4. **Politeness** - Respectful and considerate tone?
5. **Engagement** - Participants seem interested and involved?
6. **Flow** - Natural progression without awkward transitions?
7. **Coherence** - Logical sense overall?
8. **Responsiveness** - Participants address each other's points?
9. **Language Use** - Appropriate grammar and vocabulary?
10. **Emotional Intelligence** - Sensitivity to emotional tone?

**Score Interpretation:**
- 1-3: Poor - Significant communication issues
- 4-6: Average - Some strengths with notable weaknesses  
- 7-9: Good - Mostly effective with minor issues
- 10: Excellent - Exemplary quality

## 📁 Output Files

### Generated Files
- `output/dialogue_output.txt` - The transformed dialogue
- `output/dialogue_score.txt` - Quality score with details
- `logs/newsgroup_processing_[timestamp].txt` - Processing logs

### File Structure
```
output/
├── dialogue_output.txt    # Clean movie-style dialogue
└── dialogue_score.txt     # Score and analysis details

logs/
└── newsgroup_processing_[timestamp].txt  # Detailed processing log
```

## 🔍 Input Requirements

### Content Guidelines
- Minimum 100 characters of meaningful content
- At least 3 non-empty lines
- Should represent actual discussion/conversation
- Multiple participants preferred for best results

### Supported Formats
- Plain text files (.txt)
- UTF-8 or Latin-1 encoding
- Line-based dialogue format
- Newsgroup-style discussions
- Forum conversations
- Chat transcripts

## 🛠️ Technical Details

### Architecture
- **Framework**: CrewAI for multi-agent orchestration
- **LLM**: Google Gemini 1.5 Flash
- **Processing**: Sequential agent pipeline
- **Error Handling**: Comprehensive validation and logging
- **File Management**: Automatic directory creation and organization

### Error Handling
- Environment validation
- Content quality checks  
- Agent response validation
- File operation safety
- Graceful failure recovery

### Logging System
- Step-by-step processing logs
- Error tracking and reporting
- Result validation
- Performance monitoring
- Timestamp-based log files

## 🚨 Troubleshooting

### Common Issues

**Missing API Key:**
```
❌ GOOGLE_API_KEY not found in environment
```
**Solution:** Set up your `.env` file or environment variable with valid Google API key

**Invalid Content:**
```
❌ Invalid or insufficient discussion content
```
**Solution:** Ensure input has minimum 100 characters and represents actual discussion

**Empty Output:**
```
❌ Dialogue transformation failed - no output generated
```
**Solution:** Check input quality, API connectivity, and processing logs

### Debug Mode
Enable verbose logging by checking the `logs/` directory for detailed processing information.

## 📈 Performance Tips

1. **Input Quality**: Higher quality discussions produce better dialogue
2. **Content Length**: 200-2000 character discussions work best
3. **Participant Diversity**: Multiple speakers create more engaging dialogue
4. **Clear Structure**: Well-formatted input improves processing accuracy

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

MIT License - you are free to use, modify, and distribute this software with proper attribution.

## 📞 Support

For questions, issues, or suggestions:
- Create an issue in the repository
- Contact: naakaarafr

## 🔮 Future Enhancements

- Support for additional LLM providers
- Web interface for easier usage
- Batch processing capabilities
- Custom scoring criteria
- Integration with popular discussion platforms
- Real-time processing API

---

**Created by naakaarafr** | Discussion Processor v1.0
