// Keep the original catalogue order and its card artwork intact.
// RNG is added by rng-catalog.js immediately before this file runs, so Survival
// belongs at the end rather than being unshifted ahead of the original games.
if (!games.some(game => game.id === 'survival')) {
  games.push({
    id: 'survival',
    title: 'Afterlight Survival',
    cat: 'Survie',
    emoji: '🌙',
    desc: 'Explore, recueille des ressources, fabrique ton équipement et survie de nuit en nuit.',
    bg: 'linear-gradient(135deg,#10222a,#4c8792)'
  });
}

if (!cats.includes('Survie')) cats.push('Survie');
renderCats();
render();
