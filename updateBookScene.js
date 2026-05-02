const fs = require('fs'); 
const file = 'C:/Users/prave/OneDrive/Desktop/Moksh/frontend/src/app/home/components/BookScene.tsx'; 
let c = fs.readFileSync(file, 'utf8'); 

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
      draw: (c: any) => drawPathSelect(c)
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

c = c.replace(/updateTexture\(s\.pages\[i\]\.frontTex/g, 'NO_MATCH');

c = c.replace(/updateTexture\(pg\.frontTex, c => drawPageContent\(c, i, t\)\);/g, 'updateTexture(pg.frontTex, c => drawPageContent(c, i, t, userPath));'); 

c = c.replace(/\}, \[lang, t\]\);/g, '}, [lang, t, userPath]);'); 

fs.writeFileSync(file, c);
