const fs = require('fs');
const file = 'C:/Users/prave/OneDrive/Desktop/Moksh/frontend/src/components/UserSync.tsx';
let c = fs.readFileSync(file, 'utf8');

if (!c.includes('userAvatar')) {
  c = c.replace(
    /if \(isLoaded && isSignedIn && user\) \{/,
    "if (isLoaded && isSignedIn && user) {\n        // Sync to local storage for static HTML dashboards\n        localStorage.setItem('userAvatar', user.imageUrl || '');\n        localStorage.setItem('firstName', user.firstName || '');\n        localStorage.setItem('lastName', user.lastName || '');\n"
  );
  fs.writeFileSync(file, c);
  console.log('UserSync.tsx updated!');
} else {
  console.log('UserSync.tsx already contains local storage sync.');
}
