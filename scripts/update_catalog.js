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

const files = fs.readdirSync(materialsDir).filter(f => f.endsWith('.html'));

console.log(`Found ${files.length} material files in materials/`);

files.forEach(file => {
  const filePath = path.join(materialsDir, file);
  const relPath = 'materials/' + file;
  const existingIndex = catalog.findIndex(c => c.file === relPath);

  const content = fs.readFileSync(filePath, 'utf8');
  const titleMatch = content.match(/<title>([\s\S]*?)<\/title>/);
  const title = titleMatch ? titleMatch[1].trim() : file.replace('.html', '');

  const questionsMatch = content.match(/const questions = (\[[\s\S]*?\]);/);
  let questionsCount = 0;
  if (questionsMatch) {
    try {
      const qs = JSON.parse(questionsMatch[1]);
      questionsCount = qs.length;
    } catch (e) {}
  }

  if (existingIndex >= 0) {
    catalog[existingIndex].title = title;
    catalog[existingIndex].questionsCount = questionsCount;
    console.log(`Updated: ${title} (${questionsCount} questions)`);
  } else {
    catalog.push({
      id: file.replace('.html', ''),
      title: title,
      subject: title.includes('數學') ? '數學' : title.includes('國文') ? '國文' : '特教',
      grade: title.includes('一年級') || title.includes('國一') || title.includes('七年級') ? '七年級' : '國中',
      unit: '',
      questionsCount: questionsCount,
      description: `收錄 ${title} 之語音朗讀教材，共 ${questionsCount} 題。`,
      file: relPath,
      date: new Date().toISOString().split('T')[0],
      tags: [title]
    });
    console.log(`Added: ${title} (${questionsCount} questions)`);
  }
});

fs.writeFileSync(catalogPath, JSON.stringify(catalog, null, 2), 'utf8');
console.log('Successfully updated data/materials.json!');
