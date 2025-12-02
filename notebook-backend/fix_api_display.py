import re

# Read current run.py
with open('run.py', 'r') as f:
    content = f.read()

# Define the clean API endpoints HTML
clean_api_html = '''
                <div class="api-info">
                    <h3><i class="fas fa-code"></i> API Endpoints</h3>
                    <div class="endpoints-grid">
                        <div class="endpoint-col">
                            <h4>📁 Folders</h4>
                            <div class="endpoint get">GET /api/folders</div>
                            <div class="endpoint get">GET /api/folders/:id</div>
                            <div class="endpoint post">POST /api/folders</div>
                            <div class="endpoint put">PUT /api/folders/:id</div>
                            <div class="endpoint patch">PATCH /api/folders/:id</div>
                            <div class="endpoint delete">DELETE /api/folders/:id</div>
                        </div>
                        
                        <div class="endpoint-col">
                            <h4>🖼️ Images</h4>
                            <div class="endpoint get">GET /api/images</div>
                            <div class="endpoint get">GET /api/folders/:id/images</div>
                            <div class="endpoint post">POST /api/images</div>
                            <div class="endpoint post" style="background: #9c27b0;">POST /api/upload</div>
                            <div class="endpoint put">PUT /api/images/:id</div>
                            <div class="endpoint delete">DELETE /api/images/:id</div>
                        </div>
                        
                        <div class="endpoint-col">
                            <h4>🔧 Utilities</h4>
                            <div class="endpoint get">GET /health</div>
                            <div class="endpoint get">GET /test-db</div>
                            <div class="endpoint get">GET /test</div>
                            <div class="endpoint get">GET /uploads/:filename</div>
                            <div class="endpoint post" style="background: #ff9800;">POST /create-test</div>
                        </div>
                    </div>
                    <div class="api-note">
                        <small><i class="fas fa-info-circle"></i> Click any endpoint to see details</small>
                    </div>
                </div>'''

# Find and replace the API info section
# Look for the current API info (it starts with "api-info" class)
pattern = r'<div class="api-info">.*?</div>\s*</div>\s*</div>'
replacement = clean_api_html + '\n            </div>\n        </div>'

content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# Now add CSS for the new API display
new_css = '''
        /* API Endpoints Styles */
        .endpoints-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 15px;
            margin: 15px 0;
        }
        
        .endpoint-col {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
        }
        
        .endpoint-col h4 {
            margin-top: 0;
            margin-bottom: 10px;
            color: #4a5568;
            font-size: 14px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .endpoint {
            padding: 8px 12px;
            margin: 5px 0;
            border-radius: 6px;
            font-family: monospace;
            font-size: 12px;
            color: white;
            cursor: pointer;
            transition: all 0.2s ease;
            word-break: break-all;
        }
        
        .endpoint:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        
        .endpoint.get { background: #48bb78; }
        .endpoint.post { background: #4299e1; }
        .endpoint.put { background: #ed8936; }
        .endpoint.patch { background: #9c27b0; }
        .endpoint.delete { background: #f56565; }
        
        .api-note {
            text-align: center;
            margin-top: 15px;
            padding: 10px;
            background: #e6fffa;
            border-radius: 6px;
            color: #234e52;
            font-size: 12px;
            border: 1px solid #81e6d9;
        }
        
        .api-note i {
            margin-right: 5px;
        }
        
        /* Make sidebar more compact */
        .sidebar {
            overflow-y: auto;
            max-height: 90vh;
        }
        
        /* Reduce spacing in sidebar */
        .folder-controls {
            margin-bottom: 20px;
        }
        
        h2 {
            margin: 15px 0 10px 0;
            font-size: 18px;
        }'''

# Add this CSS before the closing </style> tag
if '</style>' in content:
    content = content.replace('</style>', new_css + '\n    </style>')

# Write back
with open('run.py', 'w') as f:
    f.write(content)

print("✅ Updated API endpoints display!")
print("✅ Added clean, organized API documentation")
print("✅ Improved sidebar layout")
