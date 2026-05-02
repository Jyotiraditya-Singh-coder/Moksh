const fs = require('fs');
const path = require('path');
const dashboardDir = path.join('C:', 'Users', 'prave', 'OneDrive', 'Desktop', 'Moksh', 'frontend', 'public', 'dashboard');
const htmlFiles = fs.readdirSync(dashboardDir).filter(f => f.endsWith('.html'));

const syncScript = "\n// --- CLERK TO DASHBOARD SYNC LOGIC ---\n" +
"function loadGlobalAvatar() {\n" +
"    const storedAvatar = localStorage.getItem('userAvatar');\n" +
"    const storedFirstName = localStorage.getItem('userFirstName') || 'User';\n" +
"    const storedLastName = localStorage.getItem('userLastName') || '';\n" +
"    const fullName = (storedFirstName + ' ' + storedLastName).trim();\n\n" +

"    const topNavAvatar = document.getElementById('top-nav-avatar');\n" +
"    const dropdownName = document.getElementById('dropdown-user-name');\n" +
"    const mainProfileAvatar = document.getElementById('main-profile-avatar');\n\n" +

"    if (topNavAvatar && storedAvatar) {\n" +
"        topNavAvatar.src = storedAvatar;\n" +
"    } else if (topNavAvatar && !storedAvatar) {\n" +
"        topNavAvatar.src = 'https://ui-avatars.com/api/?name=' + encodeURIComponent(fullName) + '&background=a200ff&color=fff';\n" +
"    }\n\n" +

"    if (mainProfileAvatar && storedAvatar) {\n" +
"        mainProfileAvatar.src = storedAvatar;\n" +
"    } else if (mainProfileAvatar && !storedAvatar) {\n" +
"        mainProfileAvatar.src = 'https://ui-avatars.com/api/?name=' + encodeURIComponent(fullName) + '&background=a200ff&color=fff';\n" +
"    }\n\n" +

"    if (dropdownName) {\n" +
"        dropdownName.textContent = fullName;\n" +
"    }\n" +
"}\n\n" +
"document.addEventListener('DOMContentLoaded', loadGlobalAvatar);\n";

htmlFiles.forEach(file => {
    const filePath = path.join(dashboardDir, file);
    let content = fs.readFileSync(filePath, 'utf8');

    // Remove old sync logic if exists
    const regex1 = /\/\/ --- CLERK TO DASHBOARD SYNC LOGIC ---\s*function loadGlobalAvatar\b[\s\S]*?document\.addEventListener\('DOMContentLoaded', loadGlobalAvatar\);/g;
    content = content.replace(regex1, '');
    
    // Some old versions may have <script> wrapped over it alone
    const regex2 = /<script>\s*<\/script>/g;
    
    // Inject at the very end right before </body>
    const scriptTag = "<script>\n" + syncScript + "</script>\n";

    if (content.includes('</body>')) {
        content = content.replace('</body>', scriptTag + '</body>');
    } else {
        content += scriptTag;
    }
    
    content = content.replace(regex2, '');

    fs.writeFileSync(filePath, content, 'utf8');
    console.log('Updated ' + file);
});