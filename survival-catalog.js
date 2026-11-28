// Register Afterlight Survival once in the original catalogue.
if (!games.some(game => game.id === 'survival')) {
  games.push({id:'survival',title:'Afterlight Survival',cat:'Survie',emoji:'🌙',desc:'Explore, recueille des ressources, fabrique ton équipement et survie de nuit en nuit.',bg:'linear-gradient(135deg,#10222a,#4c8792)'});
}
if (!cats.includes('Survie')) cats.push('Survie');
renderCats();
render();
