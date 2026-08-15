import os
import re
import urllib.parse
from PIL import Image

def main():
    workspace_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    img_dir = os.path.join(workspace_dir, 'assets', 'img')
    
    if not os.path.exists(img_dir):
        print(f"Error: assets/img directory not found at {img_dir}")
        return

    print(f"Workspace directory: {workspace_dir}")
    print(f"Image directory: {img_dir}")

    # Step 1: Find images to convert
    image_extensions = ('.png', '.jpg', '.jpeg')
    converted_mapping = {}  # maps original normalized relative path -> new relative path
    original_files = []     # list of original file paths to delete later

    for root, dirs, files in os.walk(img_dir):
        # Skip favicons directory
        if 'favicons' in root.replace('\\', '/').split('/'):
            continue
            
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in image_extensions:
                orig_abs_path = os.path.join(root, file)
                # Compute webp destination path
                name_without_ext = os.path.splitext(file)[0]
                webp_abs_path = os.path.join(root, name_without_ext + '.webp')
                
                # Relative paths (forward slashes)
                orig_rel_path = os.path.relpath(orig_abs_path, workspace_dir).replace('\\', '/')
                webp_rel_path = os.path.relpath(webp_abs_path, workspace_dir).replace('\\', '/')
                
                print(f"Converting: {orig_rel_path} -> {webp_rel_path}")
                try:
                    with Image.open(orig_abs_path) as img:
                        img.save(webp_abs_path, 'webp', quality=85)
                    
                    converted_mapping[orig_rel_path] = webp_rel_path
                    original_files.append((orig_abs_path, orig_rel_path))
                except Exception as e:
                    print(f"Failed to convert {orig_rel_path}: {e}")

    if not converted_mapping:
        print("No images found or converted.")
        return

    # Step 2: Build replacements lists including URL-encoded versions
    replacements = []
    # We want to sort mappings by length descending so that longer paths match first
    # e.g., 'assets/img/blogs/multi-tenancy/project.png' should replace before 'assets/img/blogs/project.png'
    sorted_mappings = sorted(converted_mapping.items(), key=lambda x: len(x[0]), reverse=True)

    for orig_rel, webp_rel in sorted_mappings:
        # Standard relative path
        replacements.append((orig_rel, webp_rel))
        # Slash prefixed absolute/site-root path
        replacements.append(('/' + orig_rel, '/' + webp_rel))
        
        # URL encoded versions
        orig_url = urllib.parse.quote(orig_rel)
        webp_url = urllib.parse.quote(webp_rel)
        if orig_url != orig_rel:
            replacements.append((orig_url, webp_url))
            replacements.append(('/' + orig_url, '/' + webp_url))

    print(f"\nCreated mapping for {len(converted_mapping)} images. Total replacement patterns: {len(replacements)}")

    # Step 3: Scan workspace files and replace references
    allowed_extensions = ('.md', '.html', '.yml', '.json', '.xml', '.css', '.js')
    ignored_dirs = {'.git', '.github', '_site', '.jekyll-cache', 'node_modules', 'tools'}
    
    modified_files_count = 0

    for root, dirs, files in os.walk(workspace_dir):
        # Skip ignored directories
        dirs[:] = [d for d in dirs if d not in ignored_dirs]
        
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in allowed_extensions:
                file_abs_path = os.path.join(root, file)
                
                # Read content
                try:
                    with open(file_abs_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                except UnicodeDecodeError:
                    # Skip binary files if they happen to match extension
                    continue
                except Exception as e:
                    print(f"Error reading {file_abs_path}: {e}")
                    continue
                
                # Perform replacements
                new_content = content
                for orig_pat, webp_pat in replacements:
                    # Case-insensitive replacement of the pattern
                    pattern = re.compile(re.escape(orig_pat), re.IGNORECASE)
                    new_content = pattern.sub(webp_pat, new_content)
                
                # Write back if changed
                if new_content != content:
                    print(f"Updating references in: {os.path.relpath(file_abs_path, workspace_dir)}")
                    try:
                        with open(file_abs_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        modified_files_count += 1
                    except Exception as e:
                        print(f"Error writing to {file_abs_path}: {e}")

    print(f"\nUpdated references in {modified_files_count} files.")

    # Step 4: Delete original image files
    deleted_count = 0
    for orig_abs, orig_rel in original_files:
        try:
            if os.path.exists(orig_abs):
                os.remove(orig_abs)
                deleted_count += 1
        except Exception as e:
            print(f"Error deleting original file {orig_rel}: {e}")

    print(f"Successfully deleted {deleted_count} original image files.")
    print("WebP image conversion and reference update completed successfully!")

if __name__ == '__main__':
    main()
