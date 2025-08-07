#!/usr/bin/env python3
"""
Batch analyzer and solver for ARC-AGI tasks
Identifies common patterns and implements solutions at scale
"""

import json
import os
from collections import defaultdict

def analyze_task_properties(task_num):
    """Analyze basic properties of a task"""
    with open(f"task{task_num:03d}.json") as f:
        data = json.load(f)
    
    properties = {
        'task_num': task_num,
        'train_count': len(data['train']),
        'test_count': len(data['test']),
        'arc_gen_count': len(data['arc-gen'])
    }
    
    # Analyze first training example
    if data['train']:
        example = data['train'][0]
        input_grid = example['input']
        output_grid = example['output']
        
        properties.update({
            'input_height': len(input_grid),
            'input_width': len(input_grid[0]) if input_grid else 0,
            'output_height': len(output_grid),
            'output_width': len(output_grid[0]) if output_grid else 0,
            'same_size': len(input_grid) == len(output_grid) and 
                        len(input_grid[0]) == len(output_grid[0]) if input_grid and output_grid else False,
            'size_ratio': (len(output_grid) / len(input_grid), 
                          len(output_grid[0]) / len(input_grid[0])) if input_grid and output_grid else (0, 0)
        })
        
        # Analyze color usage
        input_colors = set()
        output_colors = set()
        for row in input_grid:
            input_colors.update(row)
        for row in output_grid:
            output_colors.update(row)
            
        properties.update({
            'input_colors': sorted(list(input_colors)),
            'output_colors': sorted(list(output_colors)),
            'color_transform': len(input_colors) != len(output_colors) or input_colors != output_colors
        })
    
    return properties

def find_pattern_groups():
    """Group tasks by similar patterns"""
    print("Analyzing all 400 tasks...")
    
    size_patterns = defaultdict(list)
    color_patterns = defaultdict(list)
    
    for task_num in range(1, 401):
        try:
            props = analyze_task_properties(task_num)
            
            # Group by size transformation
            size_key = (props['same_size'], props['size_ratio'])
            size_patterns[size_key].append(task_num)
            
            # Group by color transformation
            color_key = (tuple(props['input_colors']), tuple(props['output_colors']))
            color_patterns[color_key].append(task_num)
            
        except Exception as e:
            print(f"Error analyzing task {task_num}: {e}")
    
    print("\n=== Size Pattern Groups ===")
    for pattern, tasks in sorted(size_patterns.items(), key=lambda x: len(x[1]), reverse=True):
        if len(tasks) > 5:  # Only show common patterns
            same_size, ratio = pattern
            print(f"Same size: {same_size}, Ratio: {ratio} -> {len(tasks)} tasks")
            print(f"  Examples: {tasks[:10]}")
    
    print("\n=== Color Pattern Groups ===")
    for pattern, tasks in sorted(color_patterns.items(), key=lambda x: len(x[1]), reverse=True):
        if len(tasks) > 3:  # Only show common patterns
            input_colors, output_colors = pattern
            print(f"Input: {input_colors} -> Output: {output_colors} ({len(tasks)} tasks)")
            print(f"  Examples: {tasks[:10]}")
    
    return size_patterns, color_patterns

def implement_simple_patterns():
    """Implement solutions for tasks with simple, recognizable patterns"""
    
    # Pattern 1: 3x3 to 9x9 tiling (like task001)
    tiling_3x3_tasks = []
    
    # Pattern 2: Same size with simple color transformation  
    color_transform_tasks = []
    
    # Pattern 3: Size multiplication patterns
    size_mult_tasks = []
    
    for task_num in range(1, 401):
        try:
            props = analyze_task_properties(task_num)
            
            # Check for 3x3 to 9x9 tiling pattern
            if (props['input_height'] == 3 and props['input_width'] == 3 and
                props['output_height'] == 9 and props['output_width'] == 9):
                tiling_3x3_tasks.append(task_num)
            
            # Check for same size tasks
            elif props['same_size']:
                color_transform_tasks.append(task_num)
            
            # Check for simple size multiplication
            elif (props['size_ratio'][0] in [2.0, 3.0] and 
                  props['size_ratio'][1] in [2.0, 3.0]):
                size_mult_tasks.append(task_num)
                
        except Exception as e:
            continue
    
    print(f"\n=== Implementable Patterns ===")
    print(f"3x3 to 9x9 tiling: {len(tiling_3x3_tasks)} tasks")
    print(f"  Tasks: {tiling_3x3_tasks}")
    
    print(f"Same size transformations: {len(color_transform_tasks)} tasks")
    print(f"  First 20 tasks: {color_transform_tasks[:20]}")
    
    print(f"Size multiplication: {len(size_mult_tasks)} tasks") 
    print(f"  First 20 tasks: {size_mult_tasks[:20]}")
    
    # Implement solutions for 3x3 to 9x9 tiling tasks
    implement_tiling_solutions(tiling_3x3_tasks)
    
    return tiling_3x3_tasks, color_transform_tasks, size_mult_tasks

def implement_tiling_solutions(task_list):
    """Implement the 3x3 tiling solution for multiple tasks"""
    solution_code = """def p(g):
    h,w=len(g),len(g[0])
    r=[[0]*w*3 for _ in range(h*3)]
    for i in range(h):
        for j in range(w):
            if g[i][j]:
                for di in range(h):
                    for dj in range(w):
                        r[i*h+di][j*w+dj]=g[di][dj]
    return r"""
    
    for task_num in task_list:
        if task_num == 1:  # Skip task001 since we already have it
            continue
            
        filename = f"task{task_num:03d}.py"
        if not os.path.exists(filename):
            with open(filename, 'w') as f:
                f.write(solution_code)
            print(f"Created solution for task{task_num:03d}")

def test_multiple_solutions():
    """Test all implemented solutions"""
    from task_solver import test_solution
    
    results = {}
    for task_num in range(1, 401):
        filename = f"task{task_num:03d}.py"
        if os.path.exists(filename):
            try:
                # Import the solution
                import importlib.util
                spec = importlib.util.spec_from_file_location(f"task{task_num:03d}", filename)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                if hasattr(module, 'p'):
                    test_results, failed = test_solution(task_num, module.p)
                    total_pass = (test_results['train_pass'] + 
                                test_results['test_pass'] + 
                                test_results['arc_gen_pass'])
                    total_fail = (test_results['train_fail'] + 
                                test_results['test_fail'] + 
                                test_results['arc_gen_fail'])
                    
                    success_rate = total_pass / (total_pass + total_fail) if (total_pass + total_fail) > 0 else 0
                    results[task_num] = {
                        'success_rate': success_rate,
                        'details': test_results
                    }
                    
            except Exception as e:
                print(f"Error testing task {task_num}: {e}")
    
    print("\n=== Solution Test Results ===")
    for task_num, result in sorted(results.items()):
        rate = result['success_rate']
        details = result['details']
        print(f"Task {task_num:03d}: {rate:.2%} success")
        if rate < 1.0:
            print(f"  Details: {details}")

if __name__ == "__main__":
    # First, analyze patterns across all tasks
    size_patterns, color_patterns = find_pattern_groups()
    
    # Implement solutions for simple patterns
    implement_simple_patterns()
    
    # Test all implemented solutions
    test_multiple_solutions()