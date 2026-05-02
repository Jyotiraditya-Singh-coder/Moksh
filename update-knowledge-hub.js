const fs = require('fs');
const path = require('path');
const dir = path.join('C:', 'Users', 'prave', 'OneDrive', 'Desktop', 'Moksh', 'frontend', 'public', 'dashboard');

// 1. UPDATE CSS
const cssPath = path.join(dir, 'Dashboard.css');
let cssContent = fs.readFileSync(cssPath, 'utf8');

if (!cssContent.includes('.knowledge-sidebar.minimized')) {
    const cssToAdd = `
/* Knowledge Hub Slide-Minimize Animation */
.knowledge-sidebar {
    transition: width 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
    overflow-x: hidden;
}
.knowledge-sidebar.minimized {
    width: 65px !important;
}
.knowledge-sidebar.minimized .kh-title-text,
.knowledge-sidebar.minimized #knowledge-list {
    opacity: 0;
    pointer-events: none;
    visibility: hidden;
    transition: opacity 0.2s, visibility 0s 0.2s;
}
.kh-title-text {
    transition: opacity 0.3s 0.1s, visibility 0s;
    opacity: 1;
    visibility: visible;
    white-space: nowrap;
}
#knowledge-list {
    transition: opacity 0.3s 0.1s, visibility 0s;
    opacity: 1;
    visibility: visible;
    min-width: 200px; /* retain width even if parent shrinks so it doesn't wrap awkwardly while animating */
}
.knowledge-sidebar.minimized #kh-toggle-btn {
    transform: rotate(180deg);
}
.kh-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(255,255,255,0.1);
    padding-bottom: 10px;
    margin-bottom: 15px;
    min-width: 230px; /* Keeps the header layout fixed during collapse */
}
.kh-header h2 {
    margin: 0;
    padding: 0;
    border: none;
    font-size: 1.3em;
}
#kh-toggle-btn {
    background: rgba(255,255,255,0.1);
    border: none;
    color: white;
    border-radius: 50%;
    width: 25px;
    height: 25px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: transform 0.4s cubic-bezier(0.25, 0.8, 0.25, 1), background 0.3s;
    flex-shrink: 0;
}
#kh-toggle-btn:hover {
    background: rgba(255,255,255,0.3);
}
`;
    
    // Remove the older border-bottom rules from h2
    cssContent = cssContent.replace(/\.knowledge-sidebar h2 \{[\s\S]*?padding-bottom: 10px;\s*\}/, '.knowledge-sidebar h2 {\n    /* Styles moved to .kh-header */\n    margin: 0;\n    font-size: 1.3em;\n}');
    
    fs.writeFileSync(cssPath, cssContent + cssToAdd);
    console.log('Updated Dashboard.css');
}

// 2. UPDATE HTML FILES
const files = fs.readdirSync(dir).filter(f => f.endsWith('.html')).map(f => path.join(dir, f));

files.forEach(file => {
    let content = fs.readFileSync(file, 'utf8');
    
    // Replace <h2>Knowledge Hub</h2> with the new header
    if (content.includes('<h2>Knowledge Hub</h2>')) {
        const replacement = `
        <div class="kh-header">
            <h2 class="kh-title-text">Knowledge Hub</h2>
            <button id="kh-toggle-btn" onclick="toggleKnowledgeHub()" title="Toggle Knowledge Hub">
                <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"></polyline></svg>
            </button>
        </div>
        `;
        content = content.replace(/<h2>Knowledge Hub<\/h2>/, replacement.trim());
    }

    // Add JavaScript function at the end of the file or before </body>
    if (!content.includes('function toggleKnowledgeHub()')) {
        const scriptToAdd = `
    <script>
        function toggleKnowledgeHub() {
            const sidebar = document.querySelector('.knowledge-sidebar');
            if(sidebar) {
                sidebar.classList.toggle('minimized');
            }
        }
    </script>
</body>`;
        content = content.replace(/<\/body>/i, scriptToAdd);
    }

    if (content !== fs.readFileSync(file, 'utf8')) {
        fs.writeFileSync(file, content, 'utf8');
        console.log('Updated HTML: ' + path.basename(file));
    }
});
