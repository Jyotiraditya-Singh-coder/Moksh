const fs = require('fs'); 
const file = 'C:/Users/prave/OneDrive/Desktop/Moksh/frontend/src/app/home/components/BookScene.tsx'; 
let c = fs.readFileSync(file, 'utf8'); 

c = c.replace(/NUM_PAGES = \d+;/g, 'NUM_PAGES = 6;');

c = c.replace(/export interface BookSceneHandle \{/g, 'export interface BookSceneProps {\n  userPath?: string;\n}\n\nexport interface BookSceneHandle {');

c = c.replace(/function getPageContent\(idx: number, t: any\) \{/g, 'function getPageContent(idx: number, t: any, userPath?: string) {'); 

c = c.replace(/if \(idx === 3\) \{[\s\S]*?return \{ title: '', draw: drawEmpty \};\n\}/g, if (idx === 3) {
    return {
      title: '???\\n' + t('feat4Title'),
      draw: (c: any) => drawFeatureDesc(c, t('feat4Desc'))
    };
  }
  if (idx === 4) {
    return {
      title: '??\\nChoose Your Path',
      draw: (c: any) => {
        c.fillStyle = '#1a0f0a';
        c.font = 'bold 36px "Playfair Display", serif';
        c.textAlign = 'center';
        c.fillText('Choose Your Path', 256, 300);
        c.font = '24px "Inter", sans-serif';
        c.fillStyle = '#443';
        c.fillText('Scroll & Click to select', 256, 350);
        
        // Buttons
        c.fillStyle = '#c8a97e';
        c.roundRect(80, 450, 352, 60, 8);
        c.fill();
        c.fillStyle = '#fff';
        c.fillText('?? Student', 256, 488);
        
        c.fillStyle = '#c8a97e';
        c.roundRect(80, 550, 352, 60, 8);
        c.fill();
        c.fillStyle = '#fff';
        c.fillText('?? Job Seeker', 256, 588);
      }
    };
  }
  if (idx === 5) {
    if (userPath === 'student') {
      return {
        title: '??\\nStudent Profile',
        draw: (c: any) => drawFeatureDesc(c, '• Academic focus areas?\\n• Seeking test prep?\\n• Study schedule preferences?')
      };
    } else if (userPath === 'jobseeker') {
      return {
        title: '??\\nJob Seeker Profile',
        draw: (c: any) => drawFeatureDesc(c, '• Target industry?\\n• Current experience level?\\n• Seeking interview prep?')
      };
    }
    return {
      title: '??\\nPath Locked',
      draw: (c: any) => drawFeatureDesc(c, 'Please select "Student" or "Job Seeker"\\non the previous page to unlock.')
    };
  }
  return { title: '', draw: drawEmpty };
}); 

c = c.replace(/function drawPageContent\(c: CanvasRenderingContext2D, idx: number, t: any\) \{/g, 'function drawPageContent(c: CanvasRenderingContext2D, idx: number, t: any, userPath?: string) {'); 

c = c.replace(/const content = getPageContent\(idx, t\);/g, 'const content = getPageContent(idx, t, userPath);'); 

c = c.replace(/const BookScene = forwardRef<BookSceneHandle>\(\(\_, ref\) => \{/g, 'const BookScene = forwardRef<BookSceneHandle, BookSceneProps>(({ userPath }, ref) => {'); 

c = c.replace(/updateTexture\(pg\.frontTex, c => drawPageContent\(c, i, t\)\);/g, 'updateTexture(pg.frontTex, c => drawPageContent(c, i, t, userPath));'); 

c = c.replace(/\}, \[lang, t\]\);/g, '}, [lang, t, userPath]);'); 

fs.writeFileSync(file, c);
console.log("SUCCESS");
