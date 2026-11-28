// Register Afterlight Survival once, at the beginning of the catalogue.
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

// Include the game's category in the catalogue filters.
if (Array.isArray(cats) && !cats.includes('Survie')) cats.push('Survie');

// Make sure the featured card and the rest of the catalogue stay visible and responsive.
const catalogStyle = document.createElement('style');
catalogStyle.textContent = `
  #games.grid { display: grid !important; grid-template-columns: repeat(auto-fit, minmax(min(100%, 220px), 1fr)); gap: 16px; }
  #games .card { display: block; visibility: visible; opacity: 1; min-width: 0; }
  #games .card:first-child { grid-column: span 2; border: 2px solid #9872ff; box-shadow: 0 10px 36px rgba(152,114,255,.28); }
  #games .card:first-child .cover { height: 230px; }
  @media (max-width: 760px) { #games.grid { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; } }
  @media (max-width: 480px) { #games .card:first-child { grid-column: 1 / -1; } #games .card:first-child .cover { height: 185px; } }
`;
document.head.appendChild(catalogStyle);

renderCats();
render();
