#!/usr/bin/env python3
"""
Task solver for ARC-AGI tasks in Google Code Golf 2025
Provides infrastructure for developing and testing task solutions
"""

import json
import copy
import importlib.util
import sys
from pathlib import Path

def load_task(task_num):
    """Load task data from JSON file"""
    task_file = f"task{task_num:03d}.json"
    with open(task_file) as f:
        return json.load(f)

def test_solution(task_num, solution_func):
    """Test a solution function against all examples for a task"""
    task_data = load_task(task_num)
    
    results = {
        'train_pass': 0,
        'train_fail': 0, 
        'test_pass': 0,
        'test_fail': 0,
        'arc_gen_pass': 0,
        'arc_gen_fail': 0
    }
    
    failed_examples = []
    
    # Test train examples
    for i, example in enumerate(task_data['train']):
        input_grid = copy.deepcopy(example['input'])
        expected = example['output']
        try:
            result = solution_func(input_grid)
            if result == expected:
                results['train_pass'] += 1
            else:
                results['train_fail'] += 1
                failed_examples.append(('train', i, input_grid, expected, result))
        except Exception as e:
            results['train_fail'] += 1
            failed_examples.append(('train', i, input_grid, expected, f"Error: {e}"))
    
    # Test test examples
    for i, example in enumerate(task_data['test']):
        input_grid = copy.deepcopy(example['input'])
        expected = example['output']
        try:
            result = solution_func(input_grid)
            if result == expected:
                results['test_pass'] += 1
            else:
                results['test_fail'] += 1
                failed_examples.append(('test', i, input_grid, expected, result))
        except Exception as e:
            results['test_fail'] += 1
            failed_examples.append(('test', i, input_grid, expected, f"Error: {e}"))
    
    # Test arc-gen examples (limit to first 10 for speed)
    for i, example in enumerate(task_data['arc-gen'][:10]):
        input_grid = copy.deepcopy(example['input'])
        expected = example['output']
        try:
            result = solution_func(input_grid)
            if result == expected:
                results['arc_gen_pass'] += 1
            else:
                results['arc_gen_fail'] += 1
                failed_examples.append(('arc-gen', i, input_grid, expected, result))
        except Exception as e:
            results['arc_gen_fail'] += 1
            failed_examples.append(('arc-gen', i, input_grid, expected, f"Error: {e}"))
    
    return results, failed_examples

def print_grid(grid, title="Grid"):
    """Print a grid in a readable format"""
    print(f"{title}:")
    for row in grid:
        print("  " + " ".join(str(cell) for cell in row))

def analyze_task(task_num):
    """Analyze a task to understand patterns"""
    task_data = load_task(task_num)
    
    print(f"Task {task_num:03d} Analysis:")
    print(f"Train examples: {len(task_data['train'])}")
    print(f"Test examples: {len(task_data['test'])}")  
    print(f"Arc-gen examples: {len(task_data['arc-gen'])}")
    print()
    
    # Analyze first training example
    if task_data['train']:
        example = task_data['train'][0]
        input_grid = example['input']
        output_grid = example['output']
        
        print("First training example:")
        print_grid(input_grid, "Input")
        print_grid(output_grid, "Output")
        print(f"Input size: {len(input_grid)}x{len(input_grid[0])}")
        print(f"Output size: {len(output_grid)}x{len(output_grid[0])}")
        print()

def save_solution(task_num, solution_code):
    """Save a solution to a task file"""
    filename = f"task{task_num:03d}.py"
    with open(filename, 'w') as f:
        f.write(solution_code)
    print(f"Solution saved to {filename}")

def create_submission_zip():
    """Create submission zip file with all task solutions"""
    import zipfile
    
    task_files = []
    for i in range(1, 401):
        filename = f"task{i:03d}.py"
        if Path(filename).exists():
            task_files.append(filename)
    
    if not task_files:
        print("No task solution files found!")
        return
    
    with zipfile.ZipFile('submission.zip', 'w') as zipf:
        for filename in task_files:
            zipf.write(filename)
    
    print(f"Created submission.zip with {len(task_files)} task solutions")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python task_solver.py <task_number>")
        sys.exit(1)
    
    task_num = int(sys.argv[1])
    analyze_task(task_num)