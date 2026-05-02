const fs = require('fs');
const file = 'C:/Users/prave/OneDrive/Desktop/Moksh/frontend/src/app/home/components/BookScene.tsx';
let content = fs.readFileSync(file, 'utf8');

content = content.replace(/NUM_PAGES\s*=\s*6/g, 'NUM_PAGES = 4');

content = content.replace(/PAGE_RANGES\s*=\s*\[[\s\S]*?\];/g, 'PAGE_RANGES = [\n  [0, 0.25], // Page 1\n  [0.25, 0.5], // Page 2\n  [0.5, 0.75], // Page 3\n  [0.75, 1.0]  // Page 4\n];');

content = content.replace(/export interface BookSceneProps \{[\s\S]*?\}/g, '');

content = content.replace(/function getPageContent\(idx: number, t: any, userPath\?: string\) \{/g, 'function getPageContent(idx: number, t: any) {');

content = content.replace(/if \(idx === 3\) \{[\s\S]*?return \{ title: '', draw: drawEmpty \};\n\}/g, `if (idx === 3) {
    return {
      title: '???\\n' + t('feat4Title'),
      draw: (c: any) => drawFeatureDesc(c, t('feat4Desc'))
    };
  }
  return { title: '', draw: drawEmpty };
}`);

content = content.replace(/function drawPageContent\(c: CanvasRenderingContext2D, idx: number, t: any, userPath\?: string\) \{/g, 'function drawPageContent(c: CanvasRenderingContext2D, idx: number, t: any) {');

content = content.replace(/const content = getPageContent\(idx, t, userPath\);/g, 'const content = getPageContent(idx, t);');

content = content.replace(/const BookScene = forwardRef<BookSceneHandle, BookSceneProps>\(\(\{ userPath \}, ref\) => \{/g, 'const BookScene = forwardRef<BookSceneHandle>((_, ref) => {');

content = content.replace(/updateTexture\(pg\.frontTex, c => drawPageContent\(c, i, t, userPath\)\);/g, 'updateTexture(pg.frontTex, c => drawPageContent(c, i, t));');

content = content.replace(/\}, \[lang, t, userPath\]\);/g, '}, [lang, t]);');

fs.writeFileSync(file, content);
