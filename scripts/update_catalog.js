const fs = require('fs');
const path = require('path');

const rootDir = path.resolve(__dirname, '..');
const materialsDir = path.join(rootDir, 'materials');
const catalogPath = path.join(rootDir, 'data', 'materials.json');

let catalog = [];
if (fs.existsSync(catalogPath)) {
  try {
    catalog = JSON.parse(fs.readFileSync(catalogPath, 'utf8'));
  } catch (e) {
    catalog = [];
  }
}

const files = fs.readdirSync(materialsDir).filter(f => f.endsWith('.html') && !f.startsWith('test-'));
catalog = catalog.filter(c => !c.id.startsWith('test-'));

console.log(`Found ${files.length} material files in materials/`);

function countQuestionsInHtml(content) {
  let count = 0;
  
  // Method 1: questions array declaration in JS
  const qMatch = content.match(/(const|let|var)\s+questions\s*=\s*(\[[\s\S]*?\]);/);
  if (qMatch) {
    try {
      const qs = new Function('return ' + qMatch[2])();
      count = qs.length;
    } catch (e) {
      const idMatches = qMatch[2].match(/"?id"?\s*:\s*[0-9]+/g);
      count = idMatches ? idMatches.length : 0;
    }
  }
  
  if (count === 0) {
    // Method 2: DOM cards or question containers
    const cardMatches = content.match(/class="[^"]*(question-card|quiz-card)[^"]*"/g) ||
                        content.match(/data-question-id=/g) ||
                        content.match(/id="card-[0-9]+"/g);
    count = cardMatches ? cardMatches.length : 0;
  }
  
  return count;
}

files.forEach(file => {
  const filePath = path.join(materialsDir, file);
  const relPath = 'materials/' + file;
  const existingIndex = catalog.findIndex(c => c.file === relPath || c.id === file.replace('.html', ''));

  const content = fs.readFileSync(filePath, 'utf8');
  const titleMatch = content.match(/<title>([\s\S]*?)<\/title>/);
  const title = titleMatch ? titleMatch[1].trim() : file.replace('.html', '');

  const questionsCount = countQuestionsInHtml(content);

  const isMath = title.includes('數學') || file.includes('math');
  const isChinese = title.includes('國文') || title.includes('吃冰') || title.includes('夏夜') || file.includes('eating-ice') || file.includes('summer-night');
  const subject = isMath ? '數學' : (isChinese ? '國文' : '特教');

  const grade = (title.includes('一年級') || title.includes('國一') || title.includes('七年級') || isChinese) ? '七年級' : '國中';
  const unit = title.includes('吃冰的滋味') ? '吃冰的滋味' : (title.includes('夏夜') ? '夏夜' : (title.includes('段考') ? '第一次段考' : ''));

  if (existingIndex >= 0) {
    catalog[existingIndex].title = title;
    catalog[existingIndex].subject = subject;
    catalog[existingIndex].grade = grade;
    if (unit) catalog[existingIndex].unit = unit;
    catalog[existingIndex].questionsCount = questionsCount;
    if (!catalog[existingIndex].description || catalog[existingIndex].description.includes('共 0 題')) {
      catalog[existingIndex].description = `收錄 ${title} 之語音朗讀教材，共 ${questionsCount} 題。`;
    }
    console.log(`Updated: ${title} (${questionsCount} questions, ${subject})`);
  } else {
    catalog.push({
      id: file.replace('.html', ''),
      title: title,
      subject: subject,
      grade: grade,
      unit: unit,
      questionsCount: questionsCount,
      description: `收錄 ${title} 之語音朗讀教材，共 ${questionsCount} 題。`,
      file: relPath,
      date: new Date().toISOString().split('T')[0],
      tags: [title, subject, '語音報讀']
    });
    console.log(`Added: ${title} (${questionsCount} questions, ${subject})`);
  }
});

fs.writeFileSync(catalogPath, JSON.stringify(catalog, null, 2), 'utf8');
console.log('Successfully updated data/materials.json!');

// Compute statistics
const totalMaterials = catalog.length;
const totalQuestions = catalog.reduce((sum, item) => sum + (Number(item.questionsCount) || 0), 0);
const subjects = new Set(catalog.map(item => item.subject).filter(s => s && s !== '特教'));
const totalSubjects = subjects.size || 2;

console.log(`Statistics: ${totalMaterials} materials, ${totalQuestions} questions, ${totalSubjects} subjects.`);

// Also sync index.html initialMaterials & static badges
const indexPath = path.join(rootDir, 'index.html');
if (fs.existsSync(indexPath)) {
  let indexHtml = fs.readFileSync(indexPath, 'utf8');

  // Update static badge numbers in HTML
  indexHtml = indexHtml.replace(
    /<span id="stat-total" class="stat-num">\s*\d+\s*<\/span>/,
    `<span id="stat-total" class="stat-num">${totalMaterials}</span>`
  );
  indexHtml = indexHtml.replace(
    /<span id="stat-questions" class="stat-num">\s*\d+\s*<\/span>/,
    `<span id="stat-questions" class="stat-num">${totalQuestions}</span>`
  );
  indexHtml = indexHtml.replace(
    /<span id="stat-subjects" class="stat-num">\s*\d+\s*<\/span>/,
    `<span id="stat-subjects" class="stat-num">${totalSubjects}</span>`
  );

  // Update initialMaterials array
  if (indexHtml.includes('const initialMaterials =')) {
    const newListStr = 'const initialMaterials = ' + JSON.stringify(catalog, null, 4) + ';';
    indexHtml = indexHtml.replace(/const initialMaterials = \[[\s\S]*?\];/, newListStr);
  }

  // Ensure updateStats is present and called in script
  if (!indexHtml.includes('function updateStats(')) {
    const statsScript = `
        function updateStats(items) {
            const statTotal = document.getElementById('stat-total');
            const statQuestions = document.getElementById('stat-questions');
            const statSubjects = document.getElementById('stat-subjects');

            if (statTotal) statTotal.textContent = items.length;
            if (statQuestions) {
                const totalQ = items.reduce((sum, item) => sum + (Number(item.questionsCount) || 0), 0);
                statQuestions.textContent = totalQ;
            }
            if (statSubjects) {
                const subjects = new Set(items.map(i => i.subject).filter(s => s && s !== '特教'));
                statSubjects.textContent = subjects.size || 2;
            }
        }
        updateStats(initialMaterials);
`;
    indexHtml = indexHtml.replace('renderMaterials(initialMaterials);', `renderMaterials(initialMaterials);\n${statsScript}`);
  }

  fs.writeFileSync(indexPath, indexHtml, 'utf8');
  console.log('Successfully synchronized index.html initialMaterials & stat badges!');
}
