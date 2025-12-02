# run.py - ENHANCED VERSION WITH FASTER LOADING AND RICH TEXT EDITOR
from flask import Flask, jsonify, request, send_from_directory, render_template_string
from flask_migrate import Migrate
from datetime import datetime
import os
from werkzeug.utils import secure_filename
import time

# Import db from app module
from app import db
from app.models import Folder, Image

app = Flask(__name__)

# Use absolute path for database to avoid permission issues
basedir = os.path.abspath(os.path.dirname(__file__))

# Database setup
os.makedirs(os.path.join(basedir, 'instance'), exist_ok=True)
db_path = os.path.join(basedir, 'instance', 'notebook.db')
database_uri = f'sqlite:///{db_path}'

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# File upload configuration
UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp'}

# Create upload folder
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

print(f"✓ Database: {database_uri}")
print(f"✓ Upload folder: {UPLOAD_FOLDER}")

# Initialize db with app
db.init_app(app)

# Don't initialize migrate if you don't have flask_migrate installed
try:
    migrate = Migrate(app, db)
    print("✓ Flask-Migrate initialized")
except:
    print("⚠ Flask-Migrate not installed, continuing without migrations")

# ===== HELPER FUNCTIONS =====
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# ===== CREATE DATABASE TABLES =====
with app.app_context():
    db.create_all()
    print("✓ Database tables created")

# ===== ENHANCED FRONTEND WITH RICH TEXT EDITOR =====
@app.route('/')
def index():
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>Notebook</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        
        body {
            background: #f5f5f7;
            color: #1d1d1f;
            line-height: 1.5;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: 280px 1fr;
            gap: 30px;
        }
        
        .sidebar {
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            height: fit-content;
        }
        
        .main-content {
            background: white;
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        
        h1 {
            font-size: 32px;
            font-weight: 600;
            color: #1d1d1f;
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 1px solid #e5e5e7;
        }
        
        h2 {
            font-size: 20px;
            font-weight: 500;
            color: #1d1d1f;
            margin: 25px 0 15px 0;
            padding-bottom: 10px;
            border-bottom: 1px solid #e5e5e7;
        }
        
        .folder-controls {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        
        .btn {
            padding: 10px 18px;
            border: none;
            border-radius: 8px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .btn-primary {
            background: #007aff;
            color: white;
            flex: 1;
        }
        
        .btn-primary:hover {
            background: #0056cc;
        }
        
        .btn-secondary {
            background: #8e8e93;
            color: white;
            flex: 1;
        }
        
        .btn-secondary:hover {
            background: #6d6d72;
        }
        
        .folder-list {
            list-style: none;
        }
        
        .folder-item {
            padding: 15px;
            margin: 8px 0;
            background: #f5f5f7;
            border-radius: 8px;
            border-left: 4px solid transparent;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .folder-item:hover {
            background: #e5e5e7;
            transform: translateX(2px);
        }
        
        .folder-item.active {
            background: #e8f4ff;
            border-left-color: #007aff;
        }
        
        .folder-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }
        
        .folder-date {
            font-weight: 500;
            color: #1d1d1f;
        }
        
        .folder-image-count {
            color: #ff3b30;
            font-size: 14px;
            font-weight: 500;
        }
        
        .image-indicator {
            color: #ff3b30;
            font-size: 12px;
            margin-top: 5px;
            display: flex;
            align-items: center;
            gap: 5px;
        }
        
        .image-gallery {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
            gap: 20px;
            margin: 20px 0 30px 0;
        }
        
        .image-item {
            background: #f5f5f7;
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid #e5e5e7;
            transition: transform 0.2s;
        }
        
        .image-item:hover {
            transform: translateY(-4px);
        }
        
        .image-preview {
            width: 100%;
            height: 120px;
            object-fit: cover;
            background: #e5e5e7;
        }
        
        .image-info {
            padding: 12px;
        }
        
        .image-name {
            font-weight: 500;
            margin-bottom: 5px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        
        .image-date {
            color: #8e8e93;
            font-size: 12px;
        }
        
        .notes-controls {
            display: flex;
            gap: 10px;
            margin: 20px 0;
        }
        
        .btn-danger {
            background: #ff3b30;
            color: white;
        }
        
        .btn-danger:hover {
            background: #d70015;
        }
        
        /* RICH TEXT EDITOR STYLES */
        .editor-container {
            border: 1px solid #e5e5e7;
            border-radius: 8px;
            overflow: hidden;
            margin-bottom: 20px;
        }
        
        .editor-toolbar {
            background: #f5f5f7;
            padding: 12px;
            border-bottom: 1px solid #e5e5e7;
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            align-items: center;
        }
        
        .toolbar-btn {
            background: white;
            border: 1px solid #d1d1d6;
            padding: 8px 12px;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 14px;
        }
        
        .toolbar-btn:hover {
            background: #e5e5e7;
        }
        
        .toolbar-btn.active {
            background: #007aff;
            color: white;
            border-color: #007aff;
        }
        
        .toolbar-separator {
            width: 1px;
            height: 24px;
            background: #d1d1d6;
            margin: 0 4px;
        }
        
        .editor-content {
            min-height: 300px;
            padding: 20px;
            outline: none;
            font-size: 16px;
            line-height: 1.6;
            overflow-y: auto;
        }
        
        .editor-content:empty:before {
            content: "Start typing your notes here...";
            color: #8e8e93;
        }
        
        .editor-content h1, .editor-content h2, .editor-content h3 {
            margin: 20px 0 10px 0;
            color: #1d1d1f;
        }
        
        .editor-content p {
            margin-bottom: 15px;
        }
        
        .editor-content ul, .editor-content ol {
            margin-left: 24px;
            margin-bottom: 15px;
        }
        
        .editor-content blockquote {
            border-left: 4px solid #007aff;
            padding-left: 16px;
            margin: 15px 0;
            font-style: italic;
            color: #48484a;
        }
        
        .save-section {
            display: flex;
            justify-content: flex-end;
            margin-top: 20px;
        }
        
        .btn-save {
            background: #34c759;
            color: white;
            padding: 12px 30px;
            font-size: 16px;
        }
        
        .btn-save:hover {
            background: #2da84e;
        }
        
        .status-message {
            padding: 12px 16px;
            border-radius: 8px;
            margin: 15px 0;
            display: none;
        }
        
        .status-success {
            background: #d4f7e2;
            color: #1d7c47;
            border: 1px solid #34c759;
            display: block;
        }
        
        .status-error {
            background: #ffe5e5;
            color: #d70015;
            border: 1px solid #ff3b30;
            display: block;
        }
        
        .upload-btn {
            background: #5856d6;
            color: white;
        }
        
        .upload-btn:hover {
            background: #4745c4;
        }
        
        .api-section {
            background: #f5f5f7;
            border-radius: 8px;
            padding: 20px;
            margin-top: 30px;
        }
        
        .api-endpoint {
            font-family: 'Menlo', 'Monaco', monospace;
            background: white;
            padding: 8px 12px;
            border-radius: 6px;
            margin: 5px 0;
            border-left: 3px solid #007aff;
        }
        
        hr {
            border: none;
            border-top: 1px solid #e5e5e7;
            margin: 25px 0;
        }
        
        /* UPLOAD PROGRESS */
        .upload-progress {
            display: none;
            margin: 15px 0;
        }
        
        .progress-bar {
            width: 100%;
            height: 8px;
            background: #e5e5e7;
            border-radius: 4px;
            overflow: hidden;
            margin-bottom: 8px;
        }
        
        .progress-fill {
            height: 100%;
            background: #34c759;
            width: 0%;
            transition: width 0.3s ease;
        }
        
        .upload-status {
            text-align: center;
            color: #48484a;
            font-size: 14px;
        }
        
        /* DELETE CONFIRMATION MODAL */
        .modal-overlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            z-index: 1000;
            justify-content: center;
            align-items: center;
        }
        
        .modal-content {
            background: white;
            border-radius: 12px;
            padding: 30px;
            max-width: 400px;
            width: 90%;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }
        
        .modal-title {
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 15px;
            color: #1d1d1f;
        }
        
        .modal-message {
            color: #48484a;
            margin-bottom: 25px;
            line-height: 1.5;
        }
        
        .modal-actions {
            display: flex;
            gap: 12px;
            justify-content: flex-end;
        }
        
        .modal-btn {
            padding: 10px 20px;
            border-radius: 8px;
            border: none;
            cursor: pointer;
            font-weight: 500;
        }
        
        .modal-btn-cancel {
            background: #f5f5f7;
            color: #48484a;
        }
        
        .modal-btn-cancel:hover {
            background: #e5e5e7;
        }
        
        .modal-btn-delete {
            background: #ff3b30;
            color: white;
        }
        
        .modal-btn-delete:hover {
            background: #d70015;
        }
        
        /* FAST LOADING ANIMATION */
        .image-placeholder {
            background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
            background-size: 200% 100%;
            animation: loading 1.5s infinite;
        }
        
        @keyframes loading {
            0% { background-position: 200% 0; }
            100% { background-position: -200% 0; }
        }
    </style>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
    <div class="container">
        <!-- Sidebar (Left) -->
        <div class="sidebar">
            <h1>Notebook</h1>
            
            <div class="folder-controls">
                <button class="btn btn-primary" onclick="createNewFolder()">
                    <i class="fas fa-plus"></i> New Folder
                </button>
                <button class="btn btn-secondary" onclick="loadFolders()">
                    <i class="fas fa-sync-alt"></i> Refresh
                </button>
            </div>
            
            <h2>Folders</h2>
            <ul class="folder-list" id="folderList">
                <div style="color: #8e8e93; text-align: center; padding: 20px;">
                    <i class="fas fa-spinner fa-spin"></i> Loading folders...
                </div>
            </ul>
        </div>
        
        <!-- Main Content (Right) -->
        <div class="main-content">
            <div id="contentArea">
                <div style="text-align: center; padding: 60px 20px; color: #8e8e93;">
                    <i class="fas fa-folder-open" style="font-size: 48px; margin-bottom: 20px;"></i>
                    <h2>Select a folder to view content</h2>
                    <p>Choose a folder from the sidebar</p>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Hidden file input for image upload -->
    <input type="file" id="fileInput" accept="image/*" multiple style="display: none;">
    
    <!-- Delete Confirmation Modal -->
    <div class="modal-overlay" id="deleteModal">
        <div class="modal-content">
            <div class="modal-title" id="modalTitle">Delete Folder</div>
            <div class="modal-message" id="modalMessage">
                Are you sure you want to delete this folder? All images and notes will be permanently deleted.
            </div>
            <div class="modal-actions">
                <button class="modal-btn modal-btn-cancel" onclick="closeDeleteModal()">Cancel</button>
                <button class="modal-btn modal-btn-delete" onclick="confirmDelete()">Delete</button>
            </div>
        </div>
    </div>
    
    <script>
        let currentFolderId = null;
        let pendingDeleteFolderId = null;
        let pendingDeleteImageId = null;
        
        // Load folders on page load
        document.addEventListener('DOMContentLoaded', () => {
            loadFolders();
        });
        
        // Load all folders
        async function loadFolders() {
            try {
                const folderList = document.getElementById('folderList');
                folderList.innerHTML = '<div style="color: #8e8e93; text-align: center; padding: 20px;"><i class="fas fa-spinner fa-spin"></i> Loading folders...</div>';
                
                const response = await fetch('/api/folder=;');
                const data = await response.json();
                
                if (!data.folders || data.folders.length === 0) {
                    folderList.innerHTML = '<div style="color: #8e8e93; text-align: center; padding: 20px;">No folders yet. Create one!</div>';
                    return;
                }
                
                // Sort folders by date (newest first)
                const sortedFolders = data.folders.sort((a, b) => 
                    new Date(b.date) - new Date(a.date)
                );
                
                folderList.innerHTML = sortedFolders.map(folder => `
                    <li class="folder-item" onclick="loadFolder(${folder.id})">
                        <div class="folder-header">
                            <span class="folder-date">${folder.date}</span>
                            <span class="folder-image-count">${folder.image_count || 0} images</span>
                        </div>
                        <div class="image-indicator">
                            <i class="fas fa-circle"></i> images
                        </div>
                    </li>
                `).join('');
                
            } catch (error) {
                console.error('Error loading folders:', error);
                showMessage('Error loading folders', 'error');
            }
        }
        
        // Load a specific folder
        async function loadFolder(folderId) {
            try {
                currentFolderId = folderId;
                
                // Update active state
                document.querySelectorAll('.folder-item').forEach(item => {
                    item.classList.remove('active');
                });
                event.currentTarget.classList.add('active');
                
                // Show loading state
                const contentArea = document.getElementById('contentArea');
                contentArea.innerHTML = `
                    <div style="text-align: center; padding: 40px;">
                        <i class="fas fa-spinner fa-spin" style="font-size: 24px; color: #007aff;"></i>
                        <p style="margin-top: 15px; color: #8e8e93;">Loading folder content...</p>
                    </div>
                `;
                
                // Load folder data and images in parallel for faster loading
                const [folderResponse, imagesResponse] = await Promise.all([
                    fetch(`/api/folder=./${folderId};`),
                    fetch(`/api/folder=./${folderId}/images;`)
                ]);
                
                const folder = await folderResponse.json();
                const imagesData = await imagesResponse.json();
                const images = imagesData.images || [];
                
                // Render the folder content
                renderFolderContent(folder, images);
                
            } catch (error) {
                console.error('Error loading folder:', error);
                showMessage('Error loading folder content', 'error');
            }
        }
        
        // Render folder content with rich text editor
        function renderFolderContent(folder, images) {
            const contentArea = document.getElementById('contentArea');
            
            contentArea.innerHTML = `
                <h1 style="margin-bottom: 10px;">${folder.date}</h1>
                <p style="color: #8e8e93; margin-bottom: 30px; font-size: 14px;">
                    Created: ${new Date(folder.created_at).toLocaleDateString()}
                </p>
                
                <hr>
                
                <div style="margin: 25px 0;">
                    <h2>Images (${images.length})</h2>
                    
                    <div style="margin: 15px 0;">
                        <button class="btn upload-btn" onclick="uploadImage()">
                            <i class="fas fa-plus"></i> Add Image
                        </button>
                    </div>
                    
                    <!-- Upload Progress -->
                    <div class="upload-progress" id="uploadProgress">
                        <div class="progress-bar">
                            <div class="progress-fill" id="progressFill"></div>
                        </div>
                        <div class="upload-status" id="uploadStatus">Uploading...</div>
                    </div>
                    
                    <div class="image-gallery" id="imageGallery">
                        ${images.length > 0 ? renderImagesFast(images) : 
                        '<div style="color: #8e8e93; text-align: center; padding: 40px; grid-column: 1/-1;">No images yet</div>'}
                    </div>
                </div>
                
                <hr>
                
                <div style="margin: 25px 0;">
                    <h2>Notes</h2>
                    
                    <div class="notes-controls">
                        <button class="btn btn-danger" onclick="clearNotes()">
                            <i class="fas fa-eraser"></i> Clear
                        </button>
                        <button class="btn btn-danger" onclick="showDeleteFolderModal(${folder.id})">
                            <i class="fas fa-trash"></i> Delete Folder
                        </button>
                    </div>
                    
                    <!-- Rich Text Editor -->
                    <div class="editor-container">
                        <div class="editor-toolbar" id="toolbar">
                            <button class="toolbar-btn" onclick="formatText('bold')" title="Bold">
                                <i class="fas fa-bold"></i>
                            </button>
                            <button class="toolbar-btn" onclick="formatText('italic')" title="Italic">
                                <i class="fas fa-italic"></i>
                            </button>
                            <button class="toolbar-btn" onclick="formatText('underline')" title="Underline">
                                <i class="fas fa-underline"></i>
                            </button>
                            
                            <div class="toolbar-separator"></div>
                            
                            <button class="toolbar-btn" onclick="formatText('justifyLeft')" title="Align Left">
                                <i class="fas fa-align-left"></i>
                            </button>
                            <button class="toolbar-btn" onclick="formatText('justifyCenter')" title="Center">
                                <i class="fas fa-align-center"></i>
                            </button>
                            <button class="toolbar-btn" onclick="formatText('justifyRight')" title="Align Right">
                                <i class="fas fa-align-right"></i>
                            </button>
                            <button class="toolbar-btn" onclick="formatText('justifyFull')" title="Justify">
                                <i class="fas fa-align-justify"></i>
                            </button>
                            
                            <div class="toolbar-separator"></div>
                            
                            <button class="toolbar-btn" onclick="formatText('insertUnorderedList')" title="Bullet List">
                                <i class="fas fa-list-ul"></i>
                            </button>
                            <button class="toolbar-btn" onclick="formatText('insertOrderedList')" title="Numbered List">
                                <i class="fas fa-list-ol"></i>
                            </button>
                            
                            <div class="toolbar-separator"></div>
                            
                            <button class="toolbar-btn" onclick="formatText('formatBlock', '<h1>')" title="Heading 1">
                                H1
                            </button>
                            <button class="toolbar-btn" onclick="formatText('formatBlock', '<h2>')" title="Heading 2">
                                H2
                            </button>
                            <button class="toolbar-btn" onclick="formatText('formatBlock', '<h3>')" title="Heading 3">
                                H3
                            </button>
                        </div>
                        
                        <div class="editor-content" id="editor" contenteditable="true" oninput="autoSave()">
                            ${folder.notes_html || ''}
                        </div>
                    </div>
                    
                    <div class="save-section">
                        <button class="btn btn-save" onclick="saveNotes(${folder.id})">
                            <i class="fas fa-save"></i> Save Notes
                        </button>
                    </div>
                </div>
                
                <div class="api-section">
                    <h2>API Endpoints</h2>
                    <div style="color: #8e8e93; margin-bottom: 15px;">
                        Available backend endpoints for this application
                    </div>
                    
                    <div class="api-endpoint">GET /api/folder=;</div>
                    <div class="api-endpoint">GET /api/folder=./:id;</div>
                    <div class="api-endpoint">PUT /api/folder=./:id;</div>
                    <div class="api-endpoint">POST /api/images;</div>
                    <div class="api-endpoint">PUT /api/folder=./:do;</div>
                    <div class="api-endpoint">PATCH /api/folder=./:do;</div>
                    <div class="api-endpoint">DELETE /api/folder=./:do;</div>
                    <div class="api-endpoint">PUT /api/images=./:do;</div>
                    <div class="api-endpoint">DELETE /api/images=./:do;</div>
                </div>
                
                <div id="statusMessage" class="status-message"></div>
            `;
            
            // Initialize toolbar button states
            updateToolbarButtons();
        }
        
        // Render images with fast loading
        function renderImagesFast(images) {
            return images.map(image => `
                <div class="image-item">
                    <img src="${image.url}" class="image-preview" 
                         alt="${image.filename}"
                         loading="lazy"
                         onload="this.classList.remove('image-placeholder')"
                         onerror="this.src='https://via.placeholder.com/180x120?text=Image+Error'">
                    <div class="image-info">
                        <div class="image-name">${image.filename}</div>
                        <div class="image-date">
                            ${new Date(image.uploaded_at).toLocaleDateString()}
                        </div>
                        <button onclick="showDeleteImageModal(${image.id}, event)" 
                                style="margin-top: 8px; padding: 4px 8px; background: #ff3b30; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 12px;">
                            <i class="fas fa-trash"></i> Delete
                        </button>
                    </div>
                </div>
            `).join('');
        }
        
        // Rich text editor functions
        function formatText(command, value = null) {
            document.execCommand(command, false, value);
            document.getElementById('editor').focus();
            updateToolbarButtons();
        }
        
        function updateToolbarButtons() {
            const buttons = document.querySelectorAll('.toolbar-btn');
            buttons.forEach(btn => btn.classList.remove('active'));
            
            // Check for bold
            if (document.queryCommandState('bold')) {
                document.querySelector('[onclick*="bold"]').classList.add('active');
            }
            
            // Check for italic
            if (document.queryCommandState('italic')) {
                document.querySelector('[onclick*="italic"]').classList.add('active');
            }
            
            // Check for underline
            if (document.queryCommandState('underline')) {
                document.querySelector('[onclick*="underline"]').classList.add('active');
            }
        }
        
        // Create new folder
        async function createNewFolder() {
            const date = prompt('Enter date (YYYY-MM-DD):', new Date().toISOString().split('T')[0]);
            
            if (!date) return;
            
            try {
                const response = await fetch('/api/folder=;', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        date: date,
                        notes_html: ''
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    showMessage('New folder created!', 'success');
                    loadFolders();
                    // Load the new folder
                    setTimeout(() => {
                        loadFolder(data.folder.id);
                    }, 100);
                } else {
                    showMessage('Error: ' + data.error, 'error');
                }
                
            } catch (error) {
                console.error('Error creating folder:', error);
                showMessage('Error creating folder', 'error');
            }
        }
        
        // Upload image with progress tracking
        async function uploadImage() {
            if (!currentFolderId) {
                showMessage('Please select a folder first', 'error');
                return;
            }
            
            const fileInput = document.getElementById('fileInput');
            fileInput.onchange = async (e) => {
                const files = e.target.files;
                const uploadProgress = document.getElementById('uploadProgress');
                const progressFill = document.getElementById('progressFill');
                const uploadStatus = document.getElementById('uploadStatus');
                
                // Show progress bar
                uploadProgress.style.display = 'block';
                progressFill.style.width = '0%';
                
                let uploadedCount = 0;
                const totalFiles = files.length;
                
                for (let i = 0; i < files.length; i++) {
                    const file = files[i];
                    
                    if (!file.type.startsWith('image/')) {
                        showMessage(`Skipping non-image: ${file.name}`, 'error');
                        continue;
                    }
                    
                    uploadStatus.textContent = `Uploading ${file.name}... (${i + 1}/${totalFiles})`;
                    
                    const formData = new FormData();
                    formData.append('file', file);
                    formData.append('folder_id', currentFolderId);
                    
                    try {
                        // Show image placeholder immediately
                        const imageGallery = document.getElementById('imageGallery');
                        const placeholderHtml = `
                            <div class="image-item">
                                <div class="image-preview image-placeholder"></div>
                                <div class="image-info">
                                    <div class="image-name">${file.name}</div>
                                    <div class="image-date">Uploading...</div>
                                </div>
                            </div>
                        `;
                        imageGallery.insertAdjacentHTML('afterbegin', placeholderHtml);
                        
                        const response = await fetch('/api/images;', {
                            method: 'POST',
                            body: formData
                        });
                        
                        const data = await response.json();
                        
                        if (data.success) {
                            uploadedCount++;
                        } else {
                            showMessage(`Failed: ${data.error}`, 'error');
                        }
                    } catch (error) {
                        console.error('Upload error:', error);
                        showMessage('Upload failed', 'error');
                    }
                    
                    // Update progress
                    const progress = Math.round((i + 1) / totalFiles * 100);
                    progressFill.style.width = `${progress}%`;
                }
                
                uploadStatus.textContent = `Upload complete! ${uploadedCount}/${totalFiles} uploaded`;
                progressFill.style.width = '100%';
                
                // Hide progress after 2 seconds and reload images
                setTimeout(() => {
                    uploadProgress.style.display = 'none';
                    if (uploadedCount > 0) {
                        // FAST RELOAD: Just reload the images, not the whole folder
                        refreshImages();
                    }
                }, 2000);
                
                // Reset file input
                fileInput.value = '';
            };
            
            fileInput.click();
        }
        
        // FAST: Refresh only images without reloading entire folder
        async function refreshImages() {
            if (!currentFolderId) return;
            
            try {
                const imagesResponse = await fetch(`/api/folder=./${currentFolderId}/images;`);
                const imagesData = await imagesResponse.json();
                const images = imagesData.images || [];
                
                // Update only the image gallery
                const imageGallery = document.getElementById('imageGallery');
                if (imageGallery) {
                    imageGallery.innerHTML = images.length > 0 ? renderImagesFast(images) : 
                        '<div style="color: #8e8e93; text-align: center; padding: 40px; grid-column: 1/-1;">No images yet</div>';
                }
                
            } catch (error) {
                console.error('Error refreshing images:', error);
            }
        }
        
        // Delete image with confirmation modal
        function showDeleteImageModal(imageId, event) {
            event.stopPropagation();
            pendingDeleteImageId = imageId;
            document.getElementById('deleteModal').style.display = 'flex';
            document.getElementById('modalTitle').textContent = 'Delete Image';
            document.getElementById('modalMessage').textContent = 'Are you sure you want to delete this image?';
        }
        
        // Delete folder with confirmation modal
        function showDeleteFolderModal(folderId) {
            pendingDeleteFolderId = folderId;
            document.getElementById('deleteModal').style.display = 'flex';
            document.getElementById('modalTitle').textContent = 'Delete Folder';
            document.getElementById('modalMessage').textContent = 'Are you sure you want to delete this folder? All images and notes will be permanently deleted.';
        }
        
        function closeDeleteModal() {
            document.getElementById('deleteModal').style.display = 'none';
            pendingDeleteFolderId = null;
            pendingDeleteImageId = null;
        }
        
        async function confirmDelete() {
            if (pendingDeleteImageId) {
                await deleteImage(pendingDeleteImageId);
            } else if (pendingDeleteFolderId) {
                await deleteFolderAction(pendingDeleteFolderId);
            }
            closeDeleteModal();
        }
        
        async function deleteImage(imageId) {
            try {
                const response = await fetch(`/api/images=./delete;`, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ id: imageId })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    showMessage('Image deleted!', 'success');
                    // FAST: Refresh only images
                    refreshImages();
                } else {
                    showMessage('Error: ' + data.error, 'error');
                }
                
            } catch (error) {
                console.error('Error deleting image:', error);
                showMessage('Error deleting image', 'error');
            }
        }
        
        // Clear notes
        function clearNotes() {
            if (confirm('Clear all notes?')) {
                document.getElementById('editor').innerHTML = '';
                document.getElementById('editor').focus();
            }
        }
        
        // Auto-save notes
        let saveTimeout;
        function autoSave() {
            clearTimeout(saveTimeout);
            saveTimeout = setTimeout(() => {
                saveNotes(currentFolderId, true);
            }, 2000);
        }
        
        // Save notes
        async function saveNotes(folderId, auto = false) {
            try {
                const notes = document.getElementById('editor').innerHTML;
                
                const response = await fetch(`/api/folder=./${folderId};`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        notes_html: notes
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    if (!auto) {
                        showMessage('Notes saved successfully!', 'success');
                    }
                } else {
                    showMessage('Error: ' + data.error, 'error');
                }
                
            } catch (error) {
                console.error('Error saving notes:', error);
                showMessage('Error saving notes', 'error');
            }
        }
        
        // Delete folder action
        async function deleteFolderAction(folderId) {
            try {
                const response = await fetch(`/api/folder=./delete;`, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ id: folderId })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    showMessage('Folder deleted!', 'success');
                    loadFolders();
                    
                    // Clear content area
                    document.getElementById('contentArea').innerHTML = `
                        <div style="text-align: center; padding: 60px 20px; color: #8e8e93;">
                            <i class="fas fa-check-circle" style="font-size: 48px; margin-bottom: 20px;"></i>
                            <h2>Folder deleted successfully</h2>
                            <p>Select another folder from the sidebar</p>
                        </div>
                    `;
                } else {
                    showMessage('Error: ' + data.error, 'error');
                }
                
            } catch (error) {
                console.error('Error deleting folder:', error);
                showMessage('Error deleting folder', 'error');
            }
        }
        
        // Show status message
        function showMessage(message, type = 'success') {
            const statusDiv = document.getElementById('statusMessage');
            if (!statusDiv) return;
            
            statusDiv.textContent = message;
            statusDiv.className = `status-message status-${type}`;
            statusDiv.style.display = 'block';
            
            setTimeout(() => {
                statusDiv.style.display = 'none';
            }, 3000);
        }
        
        // Keyboard shortcuts for rich text editor
        document.addEventListener('keydown', (e) => {
            if ((e.ctrlKey || e.metaKey) && document.activeElement.id === 'editor') {
                switch(e.key.toLowerCase()) {
                    case 'b':
                        e.preventDefault();
                        formatText('bold');
                        break;
                    case 'i':
                        e.preventDefault();
                        formatText('italic');
                        break;
                    case 'u':
                        e.preventDefault();
                        formatText('underline');
                        break;
                    case 'l':
                        e.preventDefault();
                        formatText('justifyLeft');
                        break;
                    case 'e':
                        e.preventDefault();
                        formatText('justifyCenter');
                        break;
                    case 'r':
                        e.preventDefault();
                        formatText('justifyRight');
                        break;
                    case 's':
                        e.preventDefault();
                        if (currentFolderId) saveNotes(currentFolderId);
                        break;
                }
            }
        });
    </script>
</body>
</html>
    '''

# ===== API ENDPOINTS =====

# 1. GET /api/folder=; (Get all folders)
@app.route('/api/folder=;', methods=['GET'])
def get_all_folders_api():
    try:
        folders = Folder.query.order_by(Folder.date.desc()).all()
        return jsonify({
            'success': True,
            'folders': [folder.to_dict() for folder in folders]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# 2. GET /api/folder=./:id; (Get specific folder)
@app.route('/api/folder=./<int:id>;', methods=['GET'])
def get_folder_api(id):
    try:
        folder = Folder.query.get_or_404(id)
        return jsonify(folder.to_dict())
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 404

# 3. PUT /api/folder=./:id; (Update folder)
@app.route('/api/folder=./<int:id>;', methods=['PUT'])
def update_folder_api(id):
    try:
        folder = Folder.query.get_or_404(id)
        data = request.get_json()
        
        if 'notes_html' in data:
            folder.notes_html = data['notes_html']
        if 'date' in data:
            folder.date = data['date']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'folder': folder.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

# 4. POST /api/images; (Upload/create image) - OPTIMIZED FOR SPEED
@app.route('/api/images;', methods=['POST'])
def upload_image_api():
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        folder_id = request.form.get('folder_id')
        
        if not file or file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        if not folder_id:
            return jsonify({'success': False, 'error': 'No folder specified'}), 400
        
        folder = Folder.query.get(folder_id)
        if not folder:
            return jsonify({'success': False, 'error': 'Folder not found'}), 404
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            name, ext = os.path.splitext(filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]
            unique_filename = f"{name}_{timestamp}{ext}"
            
            # Save file
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(filepath)
            
            # Create image record
            image = Image(
                filename=unique_filename,
                original_filename=filename,
                url=f'/uploads/{unique_filename}',
                folder_id=folder_id
            )
            
            db.session.add(image)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Image uploaded',
                'image': image.to_dict()
            })
        
        return jsonify({'success': False, 'error': 'Invalid file type'}), 400
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

# 5. PUT /api/folder=./:do; (Update folder with action)
@app.route('/api/folder=./<action>;', methods=['PUT'])
def update_folder_action_api(action):
    try:
        data = request.get_json()
        
        if action == 'rename':
            if 'id' not in data or 'new_date' not in data:
                return jsonify({'success': False, 'error': 'Missing id or new_date'}), 400
            
            folder = Folder.query.get(data['id'])
            if not folder:
                return jsonify({'success': False, 'error': 'Folder not found'}), 404
            
            folder.date = data['new_date']
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': f'Folder renamed to {data["new_date"]}',
                'folder': folder.to_dict()
            })
        
        return jsonify({'success': False, 'error': f'Unknown action: {action}'}), 400
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

# 6. PATCH /api/folder=./:do; (Partial update)
@app.route('/api/folder=./<action>;', methods=['PATCH'])
def patch_folder_action_api(action):
    try:
        data = request.get_json()
        
        if action == 'update':
            if 'id' not in data:
                return jsonify({'success': False, 'error': 'Missing id'}), 400
            
            folder = Folder.query.get(data['id'])
            if not folder:
                return jsonify({'success': False, 'error': 'Folder not found'}), 404
            
            if 'notes_html' in data:
                folder.notes_html = data['notes_html']
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Folder updated',
                'folder': folder.to_dict()
            })
        
        return jsonify({'success': False, 'error': f'Unknown action: {action}'}), 400
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

# 7. DELETE /api/folder=./:do; (Delete folder)
@app.route('/api/folder=./<action>;', methods=['DELETE'])
def delete_folder_action_api(action):
    try:
        data = request.get_json()
        
        if action == 'delete':
            if 'id' not in data:
                return jsonify({'success': False, 'error': 'Missing id'}), 400
            
            folder = Folder.query.get(data['id'])
            if not folder:
                return jsonify({'success': False, 'error': 'Folder not found'}), 404
            
            # Delete folder (cascade will delete images)
            db.session.delete(folder)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Folder deleted'
            })
        
        return jsonify({'success': False, 'error': f'Unknown action: {action}'}), 400
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

# 8. PUT /api/images=./:do; (Update image)
@app.route('/api/images=./<action>;', methods=['PUT'])
def update_image_action_api(action):
    try:
        data = request.get_json()
        
        if action == 'rename':
            if 'id' not in data or 'new_filename' not in data:
                return jsonify({'success': False, 'error': 'Missing id or new_filename'}), 400
            
            image = Image.query.get(data['id'])
            if not image:
                return jsonify({'success': False, 'error': 'Image not found'}), 404
            
            image.filename = data['new_filename']
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': f'Image renamed to {data["new_filename"]}',
                'image': image.to_dict()
            })
        
        return jsonify({'success': False, 'error': f'Unknown action: {action}'}), 400
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

# 9. DELETE /api/images=./:do; (Delete image)
@app.route('/api/images=./<action>;', methods=['DELETE'])
def delete_image_action_api(action):
    try:
        data = request.get_json()
        
        if action == 'delete':
            if 'id' not in data:
                return jsonify({'success': False, 'error': 'Missing id'}), 400
            
            image = Image.query.get(data['id'])
            if not image:
                return jsonify({'success': False, 'error': 'Image not found'}), 404
            
            # Delete physical file
            try:
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
                if os.path.exists(filepath):
                    os.remove(filepath)
            except:
                pass
            
            db.session.delete(image)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Image deleted'
            })
        
        return jsonify({'success': False, 'error': f'Unknown action: {action}'}), 400
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

# Additional endpoint: Get images for a folder - OPTIMIZED
@app.route('/api/folder=./<int:folder_id>/images;', methods=['GET'])
def get_folder_images_api(folder_id):
    try:
        images = Image.query.filter_by(folder_id=folder_id).order_by(Image.uploaded_at.desc()).all()
        return jsonify({
            'success': True,
            'images': [image.to_dict() for image in images]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Create folder endpoint (POST to /api/folder=;)
@app.route('/api/folder=;', methods=['POST'])
def create_folder_api():
    try:
        data = request.get_json()
        
        if not data or 'date' not in data:
            return jsonify({'success': False, 'error': 'Missing date'}), 400
        
        folder = Folder(
            date=data['date'],
            notes_html=data.get('notes_html', '')
        )
        
        db.session.add(folder)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'folder': folder.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

# Serve uploaded files
@app.route('/uploads/<filename>')
def serve_uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    print("🚀 Starting ENHANCED Notebook App...")
    print("🌐 Open: http://localhost:5000")
    print("✅ NEW FEATURES:")
    print("   1. 🎯 DELETE CONFIRMATION MODAL for folders and images")
    print("   2. ⚡ FASTER IMAGE LOADING with placeholders and lazy loading")
    print("   3. 📝 RICH TEXT EDITOR with:")
    print("      • Bold, Italic, Underline")
    print("      • Alignment (Left, Center, Right, Justify)")
    print("      • Numbered & Bullet Lists")
    print("      • Headings (H1, H2, H3)")
    print("      • Keyboard shortcuts (Ctrl+B, Ctrl+I, etc.)")
    print("      • Auto-save every 2 seconds")
    print("   4. 📤 FAST IMAGE UPLOAD with progress bar")
    print("   5. 🖼️ INSTANT IMAGE PREVIEW when uploading")
    app.run(debug=True, host='0.0.0.0', port=5000)
   