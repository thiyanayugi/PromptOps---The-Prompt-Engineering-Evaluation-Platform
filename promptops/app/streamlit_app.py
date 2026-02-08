import streamlit as st
import json
import os
import sys

# Add parent directory to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

from promptops.engine.prompt_loader import PromptLoader
from promptops.engine.runner import Runner
from promptops.engine.evaluator import Evaluator
from promptops.engine.judge import Judge
from promptops.engine.metrics import Metrics
from promptops.engine.storage import Storage
from promptops.llm.client import MockLLMClient

# Configure Streamlit page settings
# Page config
st.set_page_config(
    page_title="PromptOps",
    page_icon="🧠",
    layout="wide"
)

# Cache components for better performance across sessions
# Initialize components
@st.cache_resource
def init_components():
    llm_client = MockLLMClient()
    judge = Judge(llm_client)
    return {
        "prompt_loader": PromptLoader(),
        "runner": Runner(llm_client),
        "evaluator": Evaluator(judge),
        "storage": Storage()
    }

components = init_components()

# Sidebar navigation
st.sidebar.title("🧠 PromptOps")
st.sidebar.markdown("*Prompt Engineering Evaluation Platform*")
st.sidebar.markdown("---")

page = st.sidebar.radio("Navigation", ["📝 Prompts", "▶ Run Evaluation", "📊 Results"])

# ==================== PROMPTS PAGE ====================
if page == "📝 Prompts":
    st.title("📝 Prompt Versions")
    
    prompt_files = components["prompt_loader"].list_prompts()
    
    if not prompt_files:
        st.warning("No prompt files found. Create JSON files in `promptops/prompts/`")
    else:
        cols = st.columns([1, 3])
        with cols[0]:
            selected_file = st.selectbox("Select Prompt", prompt_files)
        
        if selected_file:
            prompt_data = components["prompt_loader"].load_prompt(selected_file)
            
            with cols[1]:
                st.markdown(f"### {prompt_data.get('name', 'Untitled')}")
                st.caption(f"Version: **{prompt_data.get('version', 'N/A')}**")
            
            st.markdown("#### Description")
            st.info(prompt_data.get('description', 'No description'))
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### System Prompt")
                st.code(prompt_data.get('system_prompt', ''), language="text")
            
            with col2:
                st.markdown("#### User Template")
                st.code(prompt_data.get('user_template', ''), language="text")

# ==================== RUN EVALUATION PAGE ====================
elif page == "▶ Run Evaluation":
    st.title("▶ Run Evaluation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 1. Select Prompt")
        prompt_files = components["prompt_loader"].list_prompts()
        selected_prompt_file = st.selectbox("Prompt Version", prompt_files)
        
        if selected_prompt_file:
            prompt_data = components["prompt_loader"].load_prompt(selected_prompt_file)
            st.success(f"✓ {prompt_data.get('name')} ({prompt_data.get('version')})")
    
    with col2:
        st.markdown("### 2. Select Dataset")
        dataset_dir = "promptops/datasets"
        if os.path.exists(dataset_dir):
            dataset_files = [f for f in os.listdir(dataset_dir) if f.endswith(".json")]
        else:
            dataset_files = []
        
        selected_dataset_file = st.selectbox("Dataset", dataset_files)
        
        if selected_dataset_file:
            dataset_path = os.path.join(dataset_dir, selected_dataset_file)
            with open(dataset_path, "r") as f:
                dataset = json.load(f)
            st.success(f"✓ {len(dataset)} test cases")
    
    st.markdown("---")
    st.markdown("### 3. Execute")
    
    if st.button("🚀 Run Evaluation", type="primary", use_container_width=True):
        if not selected_prompt_file or not selected_dataset_file:
            st.error("Please select both a prompt and dataset")
        else:
            with st.spinner("Running evaluation..."):
                # Load data
                prompt_data = components["prompt_loader"].load_prompt(selected_prompt_file)
                dataset_path = os.path.join(dataset_dir, selected_dataset_file)
                with open(dataset_path, "r") as f:
                    dataset = json.load(f)
                
                # Run
                run_results = components["runner"].run_batch(prompt_data, dataset, selected_dataset_file)
                
                # Evaluate
                evaluated_results = components["evaluator"].evaluate_run(run_results["results"])
                run_results["results"] = evaluated_results
                
                # Compute metrics
                metrics = Metrics.compute(evaluated_results)
                run_results["metrics"] = metrics
                
                # Save
                filename = components["storage"].save_run(run_results)
                
                st.success(f"✅ Run complete! Saved as `{filename}`")
                st.balloons()
                
                # Show quick summary
                st.markdown("#### Quick Summary")
                metric_cols = st.columns(4)
                metric_cols[0].metric("Total Runs", metrics.get("total_runs", 0))
                metric_cols[1].metric("Avg Clarity", f"{metrics.get('avg_clarity_score', 0)}/5")
                metric_cols[2].metric("Avg Latency", f"{metrics.get('avg_latency_seconds', 0)}s")
                metric_cols[3].metric("Avg Words", metrics.get('avg_word_count', 0))

# ==================== RESULTS PAGE ====================
elif page == "📊 Results":
    st.title("📊 Results Dashboard")
    
    run_files = components["storage"].list_runs()
    
    if not run_files:
        st.info("No runs yet. Go to **Run Evaluation** to create your first run.")
    else:
        selected_run = st.selectbox("Select Run", run_files)
        
        if selected_run:
            run_data = components["storage"].load_run(selected_run)
            
            # Header
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.markdown(f"### {run_data.get('prompt_name')}")
            with col2:
                st.caption(f"Version: {run_data.get('prompt_version')}")
            with col3:
                st.caption(f"Dataset: {run_data.get('dataset_id')}")
            
            # Metrics
            st.markdown("#### Metrics")
            metrics = run_data.get("metrics", {})
            cols = st.columns(4)
            cols[0].metric("Total Runs", metrics.get("total_runs", 0))
            cols[1].metric("Avg Clarity Score", f"{metrics.get('avg_clarity_score', 0)}/5")
            cols[2].metric("Avg Latency", f"{metrics.get('avg_latency_seconds', 0)}s")
            cols[3].metric("Avg Word Count", metrics.get('avg_word_count', 0))
            
            st.markdown("---")
            
            # Results table
            st.markdown("#### Detailed Results")
            results = run_data.get("results", [])
            
            for i, result in enumerate(results):
                with st.expander(f"Case {i+1}: {result.get('case_id')} - Clarity: {result.get('evaluation', {}).get('clarity_score', 'N/A')}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**Input Variables**")
                        st.json(result.get('input_variables', {}))
                        
                        st.markdown("**Prompt**")
                        st.text(result.get('prompt_text', ''))
                    
                    with col2:
                        st.markdown("**Output**")
                        st.info(result.get('output', ''))
                        
                        st.markdown("**Evaluation**")
                        eval_data = result.get('evaluation', {})
                        st.write(f"- **Clarity Score**: {eval_data.get('clarity_score', 'N/A')}/5")
                        st.write(f"- **Word Count**: {eval_data.get('word_count', 'N/A')}")
                        st.write(f"- **Reasoning**: {eval_data.get('reasoning', 'N/A')}")
                        st.write(f"- **Latency**: {result.get('latency', 'N/A'):.3f}s")
