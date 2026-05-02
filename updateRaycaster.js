const fs = require('fs'); 
const file = 'C:/Users/prave/OneDrive/Desktop/Moksh/frontend/src/app/home/components/BookScene.tsx'; 
let c = fs.readFileSync(file, 'utf8'); 

c = c.replace(/export interface BookSceneProps \{/, "export interface BookSceneProps {\n  onPathSelect?: (path: string) => void;\n");

c = c.replace(/const BookScene = forwardRef<BookSceneHandle, BookSceneProps>\(\(\{ userPath \}, ref\) => \{/, "const BookScene = forwardRef<BookSceneHandle, BookSceneProps>(({ userPath, onPathSelect }, ref) => {");

let eventCode = `
    const onClick = (e: MouseEvent) => {
      if (!onPathSelect) return;
      // Normalise mouse coords
      const rect = renderer.domElement.getBoundingClientRect();
      const mx = ((e.clientX - rect.left) / rect.width) * 2 - 1;
      const my = -((e.clientY - rect.top) / rect.height) * 2 + 1;
      
      const raycaster = new THREE.Raycaster();
      raycaster.setFromCamera(new THREE.Vector2(mx, my), camera);
      
      // Check intersection with page 4 front mesh
      const page4 = pages[4];
      if (page4) {
        const intersects = raycaster.intersectObject(page4.pivot.children[0]); // frontMesh is usually first child
        if (intersects.length > 0) {
          const uv = intersects[0].uv;
          if (uv) {
            // Check based on draw logic in getPageContent
            // Canvas Y runs 0 (top) to 1 (bottom). UV runs 0 (bottom) to 1 (top)!
            // Student button mapped on canvas at y=450 to 510 on 1024 height -> UV y is approx 1 - (450/1024) = 0.56
            const cy = 1 - uv.y;
            if (cy > 0.40 && cy < 0.55) {
              onPathSelect('student');
            } else if (cy > 0.50 && cy < 0.65) {
              onPathSelect('jobseeker');
            }
          }
        }
      }
    };
    window.addEventListener('click', onClick);
`;

c = c.replace(/return \(\) => \{/, "return () => {\n      window.removeEventListener('click', onClick);\n");
c = c.replace(/window\.addEventListener\('resize', onResize\);/, "window.addEventListener('resize', onResize);\n" + eventCode);

fs.writeFileSync(file, c);
console.log("RAYCASTER ADDED!");
