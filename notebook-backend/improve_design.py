import re

with open('run.py', 'r') as f:
    content = f.read()

# Find and update the body background (make it cleaner)
new_body_style = '''
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            line-height: 1.6;
            color: #2d3748;
            background: linear-gradient(135deg, #f6f9fc 0%, #edf2f7 100%);
            min-height: 100vh;
            padding: 20px;
        }'''

# Replace the body style
content = re.sub(r'body\s*{[^}]*}', new_body_style, content, flags=re.DOTALL)

# Update container background (make it cleaner)
new_container_style = '''
        .container {
            max-width: 1400px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: 320px 1fr;
            gap: 25px;
        }
        
        .sidebar, .main-content {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 16px;
            padding: 25px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }'''

# Replace container styles
container_pattern = r'\.container\s*{[^}]*}\s*\.sidebar\s*{[^}]*}\s*\.main-content\s*{[^}]*}'
content = re.sub(container_pattern, new_container_style, content, flags=re.DOTALL)

# Update buttons for cleaner look
new_buttons = '''
        .btn {
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s ease;
            text-decoration: none;
            text-align: center;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        }
        
        .btn-secondary {
            background: linear-gradient(135deg, #a0aec0 0%, #718096 100%);
        }
        
        .btn-success {
            background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        }'''

# Replace button styles
content = re.sub(r'\.btn\s*{[^}]*}\s*\.btn:hover\s*{[^}]*}\s*\.btn-secondary\s*{[^}]*}\s*\.btn-secondary:hover\s*{[^}]*}', new_buttons, content, flags=re.DOTALL)

# Update image cards for better look
new_image_cards = '''
        .image-gallery {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .image-card {
            position: relative;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
            cursor: pointer;
            background: white;
        }
        
        .image-card:hover {
            transform: translateY(-8px) scale(1.02);
            box-shadow: 0 15px 35px rgba(0,0,0,0.15);
        }
        
        .image-card img {
            width: 100%;
            height: 160px;
            object-fit: cover;
            display: block;
            transition: transform 0.3s ease;
        }
        
        .image-card:hover img {
            transform: scale(1.05);
        }
        
        .image-info {
            padding: 15px;
            background: white;
        }
        
        .image-name {
            font-weight: 500;
            margin-bottom: 5px;
            color: #4a5568;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            font-size: 14px;
        }'''

# Update image card styles
content = re.sub(r'\.image-gallery\s*{[^}]*}\s*\.image-card\s*{[^}]*}\s*\.image-card:hover\s*{[^}]*}', new_image_cards, content, flags=re.DOTALL)

# Update folder items
new_folder_items = '''
        .folder-list {
            list-style: none;
            margin-bottom: 25px;
        }
        
        .folder-item {
            padding: 14px 16px;
            margin: 8px 0;
            background: #f8f9fa;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 2px solid transparent;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .folder-item:hover {
            background: #edf2f7;
            transform: translateX(5px);
            border-color: #e2e8f0;
        }
        
        .folder-item.active {
            background: linear-gradient(135deg, #ebf4ff 0%, #c3dafe 100%);
            border-color: #667eea;
            color: #4c51bf;
            font-weight: 600;
        }
        
        .folder-date {
            font-weight: 500;
            font-size: 14px;
        }
        
        .folder-count {
            background: rgba(203, 213, 224, 0.5);
            color: #4a5568;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
        }
        
        .active .folder-count {
            background: rgba(102, 126, 234, 0.2);
            color: #4c51bf;
        }'''

# Update folder styles
content = re.sub(r'\.folder-list\s*{[^}]*}\s*\.folder-item\s*{[^}]*}', new_folder_items, content, flags=re.DOTALL)

# Write back
with open('run.py', 'w') as f:
    f.write(content)

print("✅ Updated overall design!")
print("✅ Cleaner, modern gradient background")
print("✅ Better spacing and shadows")
print("✅ Improved image cards with hover effects")
print("✅ Cleaner folder items")
