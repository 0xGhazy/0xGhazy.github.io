import os
import re

def process_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    in_block = False
    new_lines = []
    changed = False
    
    for idx, line in enumerate(lines, 1):
        if line.startswith('```'):
            in_block = not in_block
            new_lines.append(line)
        elif in_block:
            # We are inside a code block.
            # 1. Convert leading whitespace to tabs
            match = re.match(r'^([ \xa0\t]+)', line)
            new_line = line
            if match:
                lead = match.group(1)
                existing_tabs = lead.count('\t')
                spaces = lead.count(' ') + lead.count('\xa0')
                
                if spaces % 4 == 0:
                    new_tabs = spaces // 4
                    added_spaces = 0
                elif spaces % 2 == 0:
                    new_tabs = spaces // 2
                    added_spaces = 0
                else:
                    new_tabs = spaces // 4
                    added_spaces = spaces % 4
                    
                new_lead = '\t' * (existing_tabs + new_tabs) + ' ' * added_spaces
                new_line = new_lead + line[len(lead):]
            
            # 2. Convert any remaining '\xa0' inside the code block line to standard space
            if '\xa0' in new_line:
                new_line = new_line.replace('\xa0', ' ')
                
            if new_line != line:
                changed = True
            new_lines.append(new_line)
        else:
            new_lines.append(line)
            
    if changed:
        with open(path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        return True
    return False

def main():
    workspace_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    posts_dir = os.path.join(workspace_dir, '_posts')
    
    if not os.path.exists(posts_dir):
        print(f"Error: _posts directory not found at {posts_dir}")
        return

    print(f"Scanning markdown files in: {posts_dir}")
    modified_count = 0
    
    for root, dirs, files in os.walk(posts_dir):
        for file in files:
            if file.endswith('.md'):
                file_abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_abs_path, workspace_dir)
                try:
                    if process_file(file_abs_path):
                        print(f"Converted code block indentation in: {rel_path}")
                        modified_count += 1
                except Exception as e:
                    print(f"Error processing {rel_path}: {e}")
                    
    print(f"\nSuccessfully converted indentation in {modified_count} files.")

if __name__ == '__main__':
    main()
