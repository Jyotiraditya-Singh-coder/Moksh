const fs = require('fs');
const dests = ['c:/Users/prave/OneDrive/Desktop/Moksh/frontend/src/app/dashboard/', 'c:/Users/prave/OneDrive/Desktop/Moksh/frontend/public/dashboard/'];
const files = [
    {name: 'AIDailyChallenges.html', title: 'AI Daily Learning Challenges'},
    {name: 'DropoutRisk.html', title: 'Dropout Risk Prediction'},
    {name: 'SkillGap.html', title: 'Skill Gap Analyzer'},
    {name: 'VoiceTutor.html', title: 'Multilingual Voice Tutor'}
];

dests.forEach(p => {
    let baseContent = fs.readFileSync(p + 'CompletedTasks.html', 'utf8');
    let sIdx = baseContent.indexOf('<main class="page-content">');
    if (sIdx === -1) sIdx = baseContent.indexOf('<div id="three-canvas-container">');
    let contentStart = baseContent.substring(0, sIdx + '<main class="page-content">'.length);
    let contentEnd = baseContent.substring(baseContent.indexOf('</main>'));
    
    files.forEach(f => {
        let newContent = contentStart + "\n<div class=\"glass-panel\" style=\"padding: 40px; text-align: center; margin-top: 50px;\">\n<h1 style=\"color: var(--primary-glow); margin-bottom: 20px;\">" + f.title + "</h1>\n<p style=\"color: var(--text-color); font-size: 1.2rem;\">This module is under active construction. Experiencing " + f.title + ". Please check back later.</p>\n</div>\n" + contentEnd;
        newContent = newContent.replace(/<title>.*?<\/title>/, "<title>" + f.title + " - Dashboard</title>");
        fs.writeFileSync(p + f.name, newContent);
    });
});
