#!/usr/bin/env python3
"""
Automated Flake8 Error Fixer
Fixes common flake8 issues across the repository
"""

import os
import re
from pathlib import Path


def fix_trailing_whitespace(content):
    """Remove trailing whitespace from lines"""
    lines = content.split('\n')
    fixed_lines = [line.rstrip() for line in lines]
    return '\n'.join(fixed_lines)


def fix_long_lines(content, max_length=100):
    """Attempt to fix long lines by breaking them appropriately"""
    lines = content.split('\n')
    fixed_lines = []
    
    for line in lines:
        if len(line) <= max_length:
            fixed_lines.append(line)
            continue
        
        # Get indentation
        indent = len(line) - len(line.lstrip())
        indent_str = line[:indent]
        
        # If it's a string concatenation, break it
        if '"""' in line or "'''" in line:
            # Don't break docstrings
            fixed_lines.append(line)
        elif ' + ' in line or '" "' in line or "' '" in line:
            # Break string concatenations
            parts = re.split(r'(\s+\+\s+|\s+"[^"]*"\s+|\s+\'[^\']*\'\s+)', line)
            current_line = indent_str
            for part in parts:
                if len(current_line + part) > max_length and current_line.strip():
                    fixed_lines.append(current_line.rstrip())
                    current_line = indent_str + '    ' + part.lstrip()
                else:
                    current_line += part
            if current_line.strip():
                fixed_lines.append(current_line.rstrip())
        elif 'SELECT' in line or 'INSERT' in line or 'UPDATE' in line:
            # Break SQL queries
            if '"' in line:
                # Find the SQL string
                match = re.search(r'(["\'])(.+?)\1', line)
                if match:
                    sql = match.group(2)
                    before = line[:match.start()]
                    after = line[match.end():]
                    
                    # Split SQL at logical points
                    sql_parts = []
                    for keyword in ['SELECT ', 'FROM ', 'WHERE ', 'ORDER BY ', 
                                   'INSERT INTO ', 'VALUES ', 'UPDATE ', 'SET ']:
                        sql = sql.replace(keyword, f'||{keyword}')
                    
                    parts = [p for p in sql.split('||') if p]
                    
                    fixed_lines.append(before + '"' + parts[0])
                    for part in parts[1:]:
                        fixed_lines.append(indent_str + '    "' + part)
                    
                    if parts:
                        fixed_lines[-1] = fixed_lines[-1] + '"' + after
                else:
                    fixed_lines.append(line)
            else:
                fixed_lines.append(line)
        else:
            # For other long lines, just add them (manual review needed)
            fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)


def fix_blank_lines(content):
    """Fix blank line issues"""
    lines = content.split('\n')
    fixed_lines = []
    blank_count = 0
    
    for i, line in enumerate(lines):
        if not line.strip():
            blank_count += 1
            # Maximum 2 consecutive blank lines
            if blank_count <= 2:
                fixed_lines.append(line)
        else:
            blank_count = 0
            fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)


def fix_imports(content):
    """Fix import ordering issues"""
    lines = content.split('\n')
    
    # Find import block
    import_start = -1
    import_end = -1
    
    for i, line in enumerate(lines):
        if line.startswith('import ') or line.startswith('from '):
            if import_start == -1:
                import_start = i
            import_end = i
        elif import_start != -1 and line.strip() and not line.startswith('#'):
            break
    
    if import_start == -1:
        return content
    
    # Extract imports
    imports = lines[import_start:import_end + 1]
    before = lines[:import_start]
    after = lines[import_end + 1:]
    
    # Separate import types
    stdlib_imports = []
    third_party_imports = []
    local_imports = []
    
    for imp in imports:
        if imp.startswith('from .') or imp.startswith('from hipaa_training'):
            local_imports.append(imp)
        elif any(imp.startswith(f'import {lib}') or imp.startswith(f'from {lib}') 
                for lib in ['os', 'sys', 'json', 'sqlite3', 'datetime', 're', 
                           'pathlib', 'typing', 'contextlib', 'logging', 'argparse',
                           'platform', 'secrets', 'base64', 'uuid']):
            stdlib_imports.append(imp)
        else:
            third_party_imports.append(imp)
    
    # Sort each group
    stdlib_imports.sort()
    third_party_imports.sort()
    local_imports.sort()
    
    # Combine with blank lines between groups
    sorted_imports = []
    if stdlib_imports:
        sorted_imports.extend(stdlib_imports)
    if third_party_imports:
        if sorted_imports:
            sorted_imports.append('')
        sorted_imports.extend(third_party_imports)
    if local_imports:
        if sorted_imports:
            sorted_imports.append('')
        sorted_imports.extend(local_imports)
    
    # Reconstruct file
    return '\n'.join(before + sorted_imports + after)


def fix_file(filepath):
    """Fix all flake8 issues in a file"""
    print(f"Fixing {filepath}...")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply fixes
        content = fix_trailing_whitespace(content)
        content = fix_blank_lines(content)
        content = fix_imports(content)
        content = fix_long_lines(content)
        
        # Ensure file ends with newline
        if content and not content.endswith('\n'):
            content += '\n'
        
        # Only write if changed
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✓ Fixed {filepath}")
            return True
        else:
            print(f"  - No changes needed for {filepath}")
            return False
            
    except Exception as e:
        print(f"  ✗ Error fixing {filepath}: {e}")
        return False


def main():
    """Main function"""
    print("🔧 Automated Flake8 Fixer")
    print("=" * 50)
    
    # Find all Python files
    python_files = []
    
    # Check main files
    if os.path.exists('main.py'):
        python_files.append('main.py')
    
    # Check hipaa_training directory
    if os.path.exists('hipaa_training'):
        for root, dirs, files in os.walk('hipaa_training'):
            for file in files:
                if file.endswith('.py'):
                    python_files.append(os.path.join(root, file))
    
    # Check tests directory
    if os.path.exists('tests'):
        for root, dirs, files in os.walk('tests'):
            for file in files:
                if file.endswith('.py'):
                    python_files.append(os.path.join(root, file))
    
    # Check scripts directory
    if os.path.exists('scripts'):
        for root, dirs, files in os.walk('scripts'):
            for file in files:
                if file.endswith('.py'):
                    python_files.append(os.path.join(root, file))
    
    print(f"\nFound {len(python_files)} Python files\n")
    
    # Fix each file
    fixed_count = 0
    for filepath in python_files:
        if fix_file(filepath):
            fixed_count += 1
    
    print("\n" + "=" * 50)
    print(f"✅ Fixed {fixed_count} out of {len(python_files)} files")
    print("\nRun 'flake8' to verify remaining issues")


if __name__ == '__main__':
    main()
