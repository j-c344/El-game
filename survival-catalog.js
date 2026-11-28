// Register Afterlight Survival once at the beginning of the existing catalogue.
if (!games.some(game => game.id === 'survival')) {
  games.unshift({
    id: 'survival',
    title: 'Afterlight Survival',
    cat: 'Survie',
    emoji: '🌙',
    desc: 'Explore, recueille des ressources, fabrique ton équipement et survie de nuit en nuit.',
    bg: 'linear-gradient(135deg,#10222a,#4c8792)'
  });
}

// Add its category to the existing category filters.
if (!cats.includes('Survie')) cats.push('Survie');

// Re-render after both the game and its category have been registered.
renderCats();
render();
