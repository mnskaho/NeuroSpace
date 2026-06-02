const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

console.log('🔧 Fixing @dhiwise/component-tagger...');

const taggerNodeModules = path.join(
  'node_modules',
  '@dhiwise',
  'component-tagger',
  'node_modules'
);

const internalChalk = path.join(taggerNodeModules, 'chalk');
const ourChalk = path.join('node_modules', 'chalk');

// Supprimer le dossier chalk interne
if (fs.existsSync(internalChalk)) {
  console.log('📦 Removing internal chalk...');
  fs.rmSync(internalChalk, { recursive: true, force: true });
}

// Copier notre version de chalk
if (fs.existsSync(ourChalk)) {
  console.log('📋 Copying your chalk version...');
  
  // Créer le dossier si nécessaire
  if (!fs.existsSync(taggerNodeModules)) {
    fs.mkdirSync(taggerNodeModules, { recursive: true });
  }
  
  // Copier récursivement
  const copyRecursive = (src, dest) => {
    const exists = fs.existsSync(src);
    const stats = exists && fs.statSync(src);
    const isDirectory = exists && stats.isDirectory();
    
    if (isDirectory) {
      if (!fs.existsSync(dest)) {
        fs.mkdirSync(dest);
      }
      fs.readdirSync(src).forEach(child => {
        copyRecursive(path.join(src, child), path.join(dest, child));
      });
    } else {
      fs.copyFileSync(src, dest);
    }
  };
  
  copyRecursive(ourChalk, internalChalk);
  console.log('✅ Chalk copied successfully');
}

// Patcher le loader
const loaderPath = path.join(
  'node_modules',
  '@dhiwise',
  'component-tagger',
  'dist',
  'nextLoader.js'
);

if (fs.existsSync(loaderPath)) {
  console.log('📝 Patching nextLoader.js...');
  
  let content = fs.readFileSync(loaderPath, 'utf8');
  
  const patchedContent = content.replace(
    /const chalk = require\(['"]chalk['"]\);/,
    `const chalk = (() => {
  try {
    return require('chalk');
  } catch (e) {
    return {
      red: (t) => t,
      green: (t) => t,
      yellow: (t) => t,
      blue: (t) => t,
      cyan: (t) => t,
      bold: (t) => t,
      gray: (t) => t
    };
  }
})();`
  );
  
  fs.writeFileSync(loaderPath, patchedContent);
  console.log('✅ Loader patched successfully');
}

console.log('🎉 Done! Run npm run dev to test.');