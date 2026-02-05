#!/usr/bin/env python3
"""Test script to verify the PromptOps pipeline."""

import json
import sys
import os

# Add promptops to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'promptops'))

from engine.prompt_loader import PromptLoader
from engine.prompt_compiler import PromptCompiler
from engine.runner import Runner
from engine.evaluator import Evaluator
from engine.judge import Judge
from engine.metrics import Metrics
from engine.storage import Storage
from llm.client import MockLLMClient

def test_pipeline():
    """Test the complete pipeline end-to-end."""
    print("🧪 Testing PromptOps Pipeline...\n")
    
    # Initialize components
    print("1️⃣ Initializing components...")
    llm_client = MockLLMClient()
    prompt_loader = PromptLoader()
    judge = Judge(llm_client)
    evaluator = Evaluator(judge)
    runner = Runner(llm_client)
    storage = Storage()
    print("   ✅ Components initialized\n")
    
    # Test prompt loading
    print("2️⃣ Testing prompt loader...")
    prompts = prompt_loader.list_prompts()
    print(f"   Found {len(prompts)} prompts: {prompts}")
    
    if not prompts:
        print("   ❌ No prompts found!")
        return False
    
    prompt_data = prompt_loader.load_prompt(prompts[0])
    print(f"   ✅ Loaded prompt: {prompt_data.get('name')}\n")
    
    # Test dataset loading
    print("3️⃣ Testing dataset loading...")
    dataset_path = "promptops/datasets/science_topics.json"
    with open(dataset_path, 'r') as f:
        dataset = json.load(f)
    print(f"   ✅ Loaded {len(dataset)} test cases\n")
    
    # Test compilation
    print("4️⃣ Testing prompt compilation...")
    compiled = PromptCompiler.compile(prompt_data, dataset[0])
    print(f"   System: {compiled['system_prompt'][:50]}...")
    print(f"   User: {compiled['user_message'][:50]}...")
    print("   ✅ Compilation successful\n")
    
    # Test runner
    print("5️⃣ Testing runner...")
    run_result = runner.run_batch(prompt_data, dataset[:2], "science_topics.json")  # Just 2 cases for speed
    print(f"   ✅ Ran {len(run_result['results'])} cases\n")
    
    # Test evaluator
    print("6️⃣ Testing evaluator...")
    evaluated = evaluator.evaluate_run(run_result['results'])
    print(f"   ✅ Evaluated {len(evaluated)} results")
    print(f"   Sample score: {evaluated[0]['evaluation']['clarity_score']}\n")
    
    # Test metrics
    print("7️⃣ Testing metrics...")
    metrics = Metrics.compute(evaluated)
    print(f"   Avg Clarity: {metrics['avg_clarity_score']}")
    print(f"   Avg Latency: {metrics['avg_latency_seconds']}s")
    print(f"   ✅ Metrics computed\n")
    
    # Test storage
    print("8️⃣ Testing storage...")
    run_result['results'] = evaluated
    run_result['metrics'] = metrics
    filename = storage.save_run(run_result)
    print(f"   ✅ Saved as: {filename}")
    
    # Verify we can load it back
    loaded = storage.load_run(filename)
    if loaded:
        print(f"   ✅ Successfully loaded run back from storage\n")
    else:
        print(f"   ❌ Failed to load run\n")
        return False
    
    print("=" * 50)
    print("✅ ALL TESTS PASSED!")
    print("=" * 50)
    return True

if __name__ == "__main__":
    try:
        success = test_pipeline()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
