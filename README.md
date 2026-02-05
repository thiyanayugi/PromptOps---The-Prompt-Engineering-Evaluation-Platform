# PromptOps – Prompt Engineering Evaluation Platform

**PromptOps** is a production-style platform for evaluating and testing prompt engineering workflows. Treat prompts like versioned, testable software artifacts.

## 🎯 Features

- **Prompt Versioning**: Create and manage multiple versions of prompts as JSON files
- **Dataset Management**: Upload and organize test datasets  
- **Batch Execution**: Run prompts against entire datasets automatically
- **LLM-as-a-Judge**: Automated evaluation using LLM judges + rule-based checks
- **Performance Metrics**: Track clarity scores, latency, word counts, and more
- **Comparison Tools**: Compare performance across prompt versions
- **Streamlit UI**: Simple but functional web interface

## 🏗 Architecture

```
promptops/
├── app/
│   └── streamlit_app.py       # Web UI (3 pages: Prompts, Run, Results)
├── engine/
│   ├── prompt_loader.py       # Load prompt versions from disk
│   ├── prompt_compiler.py     # Substitute variables into templates
│   ├── runner.py              # Execute prompts in batch
│   ├── evaluator.py           # Orchestrate evaluation pipeline
│   ├── judge.py               # LLM-based scoring
│   ├── metrics.py             # Aggregate statistics
│   └── storage.py             # Save/load results
├── llm/
│   └── client.py              # Abstract LLM client (swappable providers)
├── prompts/                   # Versioned prompt JSON files
├── datasets/                  # Test case JSON files
└── results/                   # Evaluation outputs
```

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd "PromptOps – The Prompt Engineering Evaluation Platform"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**
   ```bash
   streamlit run promptops/app/streamlit_app.py
   ```

## 🚀 Quick Start

### 1. View Prompts
Navigate to the **📝 Prompts** page to see available prompt versions. Each prompt includes:
- System prompt
- User template (with `{variable}` placeholders)
- Version metadata

### 2. Run an Evaluation
Go to **▶ Run Evaluation**:
1. Select a prompt version
2. Select a dataset
3. Click **Run Evaluation**
4. Results are automatically saved to `/results`

### 3. View Results
Open **📊 Results** to:
- See aggregated metrics (clarity score, latency, word count)
- Drill down into individual test cases
- Review LLM judge reasoning

## 📄 Prompt Format

Create JSON files in `promptops/prompts/`:

```json
{
  "version": "v1",
  "name": "Science Explainer",
  "description": "Explains science topics for kids",
  "system_prompt": "You are a friendly science tutor.",
  "user_template": "Explain {topic} to a {age} year old in {max_words} words."
}
```

## 📊 Dataset Format

Create JSON files in `promptops/datasets/`:

```json
[
  {
    "id": "case1",
    "topic": "gravity",
    "age": 10,
    "max_words": 60
  }
]
```

## 🔍 How Evaluation Works

1. **Compilation**: Variables from dataset are substituted into prompt template
2. **Execution**: LLM generates output for each test case
3. **Judge Scoring**: Separate LLM scores output on criteria (e.g., clarity)
4. **Rule-Based Checks**: Validate format compliance (word count, structure)
5. **Metrics Aggregation**: Compute averages across all cases
6. **Storage**: Results saved as JSON with full provenance

## 🔧 Extending the Platform

### Add a New LLM Provider
Implement the `LLMClient` abstract class in `llm/client.py`:

```python
from llm.client import LLMClient

class OpenAIClient(LLMClient):
    def generate(self, system_prompt: str, user_prompt: str, **kwargs) -> str:
        # Your implementation here
        pass
```

### Add Custom Evaluation Criteria
Modify `engine/judge.py` to support different scoring criteria beyond clarity.

### Add New Metrics
Extend `engine/metrics.py` to compute additional statistics.

## 📝 Example Workflow

```bash
# 1. Start the app
streamlit run promptops/app/streamlit_app.py

# 2. Create a new prompt version
# Add promptops/prompts/my_prompt_v1.json

# 3. Create a dataset
# Add promptops/datasets/my_test_cases.json

# 4. Run evaluation via UI
# Select prompt → Select dataset → Click Run

# 5. View results
# Navigate to Results page → Inspect metrics
```

## 🧪 Demo Data

The platform includes demo data:
- **Prompts**: `science_explainer_v1.json`, `science_explainer_v2.json`
- **Dataset**: `science_topics.json` (5 science questions)

## 🛠 Tech Stack

- **Backend**: Python 3.8+
- **UI**: Streamlit
- **Storage**: Local JSON files (easily swappable to database)
- **LLM**: Pluggable client architecture

## 📖 License

MIT License - feel free to use and extend!

---

**Built with PromptOps** – Because prompts deserve the same rigor as code 🧠
