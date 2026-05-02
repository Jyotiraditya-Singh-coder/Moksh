const fs = require('fs'); 
const file = 'C:/Users/prave/OneDrive/Desktop/Moksh/frontend/src/app/home/components/BookScene.tsx'; 
let c = fs.readFileSync(file, 'utf8'); 

c = c.replace(/export const PAGE_RANGES: \[number, number\]\[\] = \[\[0\.15, 0\.28\], \[0\.28, 0\.41\], \[0\.41, 0\.54\], \[0\.54, 0\.67\], \[0\.67, 0\.80\]\];/g, 
  'export const PAGE_RANGES: [number, number][] = [[0.15, 0.25], [0.26, 0.36], [0.37, 0.47], [0.48, 0.58], [0.59, 0.69], [0.70, 0.80]];');

fs.writeFileSync(file, c);
console.log("PAGE RANGES UPDATED!");
