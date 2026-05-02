const fs = require('fs');
const path = require('path');
const dashboardDir = path.join('C:', 'Users', 'prave', 'OneDrive', 'Desktop', 'Moksh', 'frontend', 'public', 'dashboard');
const htmlFiles = fs.readdirSync(dashboardDir).filter(f => f.endsWith('.html'));

const syncScript = '  // --- CLERK TO DASHBOARD SYNC LOGIC ---\\n' +
'  function loadGlobalAvatar() {\\n' +
'      const storedAvatar = localStorage.getItem(\\'userAvatar\\');\\n' +
'      const storedFirstName = localStorage.getItem(\\'userFirstName\\') || \\'User\\';\\n' +
'      const storedLastName = localStorage.getItem(\\'userLastName\\') || \\'\\';\\n' +
'      const fullName = (storedFirstName + \\' \\' + storedLastName).trim();\\n' +
'\\n' +
'      const topNavAvatar = document.getElementById(\\'top-nav-avatar\\');\\n' +
'      const dropdownName = document.getElementById(\\'dropdown-user-name\\');\\n' +
'      const mainProfileAvatar = document.getElementById(\\'main-profile-avatar\\');\\n' +
'\\n' +
'      if (topNavAvatar && storedAvatar) {\\n' +
'          topNavAvatar.src = storedAvatar;\\n' +
'      } else if (topNavAvatar && !storedAvatar) {\\n' +
'          topNavAvatar.src = \"https://ui-avatars.com/api/?name=\" + encodeURIComponent(fullName) + \"&background=a200ff&color=fff\";\\n' +
'      }\\n' +
'\\n' +
'      if (mainProfileAvatar && storedAvatar) {\\n' +
'          mainProfileAvatar.src = storedAvatar;\\n' +
'      } else if (mainProfileAvatar && !storedAvatar) {\\n' +
'          mainProfileAvatar.src = \"https://ui-avatars.com/api/?name=\" + encodeURIComponent(fullName) + \"&background=a200ff&color=fff\";\\n' +
'      }\\n' +
'\\n' +
'      if (dropdownName) {\\n' +
'          dropdownName.textContent = fullName;\\n' +
'      }\\n' +
'  }\\n' +
'\\n' +
'  document.addEventListener(\\'DOMContentLoaded\\', loadGlobalAvatar);\\n';

htmlFiles.forEach(file => {
    const filePath = path.join(dashboardDir, file);
    let content = fs.readFileSync(filePath, 'utf8');

    // Remove old sync logic if exists to avoid duplicates
    const regex1 = /\\/\\/ --- CLERK TO DASHBOARD SYNC LOGIC ---[\\s\\S]*?document\\.addEventListener\\('DOMContentLoaded', loadGlobalAvatar\\);/g;
    content = content.replace(regex1, '');
    
    // Also strip out existing <script> tags that just contain the old loadGlobalAvatar
    const regex2 = /<script>\\s*function loadGlobalAvatar\\(\\)[\\s\\S]*?document\\.addEventListener\\('DOMContentLoaded', loadGlobalAvatar\\);\\s*<\\/script>/g;
    content = content.replace(regex2, '');

    // Inject before closing </body>
    if (content.includes('</body>')) {
        content = content.replace('</body>', '<script>\\n' + syncScript + '</script>\\n</body>');
    } else {
        content += '<script>\\n' + syncScript + '</script>';
    }

    fs.writeFileSync(filePath, content, 'utf8');
    console.log('Updated ' + file);
});
