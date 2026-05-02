const fs = require('fs'); 
const file = 'C:/Users/prave/OneDrive/Desktop/Moksh/frontend/src/app/home/components/ScrollExperience.tsx'; 
let c = fs.readFileSync(file, 'utf8'); 

if (!c.includes('const [userPath, setUserPath]')) {
    c = c.replace(/const { t } = useLanguage\(\);/, "const { t } = useLanguage();\n  const [userPath, setUserPath] = useState<string | undefined>(undefined);");
    c = c.replace(/<BookScene ref=\{bookRef\} \/>/, "<BookScene ref={bookRef} userPath={userPath} onPathSelect={setUserPath} />");
    fs.writeFileSync(file, c);
    console.log("SCROLL EXPERIENCE UPDATED!");
} else {
    console.log("ALREADY UPDATED");
}
