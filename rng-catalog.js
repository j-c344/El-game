// Add the browser port of the RNG game to EL GAME's existing catalogue.
games.push({
  id: 'rng', title: 'RNG Aura Roll', cat: 'Arcade', emoji: '🎲',
  desc: 'Tente ta chance, collectionne des auras et améliore ta chance avec la boutique et les pets.',
  bg: 'linear-gradient(135deg,#102b36,#2896f0)'
});
// RNG is a standalone roll/collection game and is not part of the score API yet.
// Keep its local roll count out of the server-backed leaderboards.
window.addEventListener('message', event => {
  const frame = document.getElementById('frame');
  if (event.source === frame.contentWindow && event.origin === location.origin && event.data?.game === 'rng') {
    event.stopImmediatePropagation();
  }
}, true);
render();
