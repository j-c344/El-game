const originalRender = render;
render = function () {
  const originalFilter = games;
  const survival = originalFilter.find(game => game.id === 'survival');
  const orderedGames = survival
    ? [survival, ...originalFilter.filter(game => game.id !== 'survival')]
    : originalFilter;

  const q = $('search').value.trim().toLocaleLowerCase();
  const list = orderedGames.filter(game =>
    (category === 'Tous' || game.cat === category) &&
    `${game.title} ${game.desc} ${game.cat}`.toLocaleLowerCase().includes(q)
  );

  $('games').innerHTML = list.map(game => `
    <button class="card${game.id === 'survival' ? ' featured' : ''}" data-play="${game.id}" type="button">
      <span class="cover"><span>${game.emoji}</span></span>
      <span class="card-info">
        <span class="title">${game.title}</span>
        <span class="cat-label">${game.cat}</span>
        <span class="desc">${game.desc}</span>
      </span>
    </button>
  `).join('');

  document.querySelectorAll('[data-play]').forEach(card => {
    card.onclick = () => play(card.dataset.play);
  });
};

const featuredStyle = document.createElement('style');
featuredStyle.textContent = `
  .card.featured {
    grid-column: span 2;
    border: 2px solid var(--purple);
    box-shadow: 0 10px 36px rgba(152, 114, 255, 0.35);
  }
  .card.featured .cover { height: 230px; }
  .card.featured .title { font-size: 1.18rem; }
  @media (max-width: 480px) {
    .card.featured { grid-column: 1 / -1; }
    .card.featured .cover { height: 185px; }
  }
`;
document.head.appendChild(featuredStyle);
render();
