# Configuration des classements Supabase

Le site utilise uniquement la **publishable key** Supabase côté navigateur. Cette clé est publique par conception ; ne remplacez jamais par une `secret` ou `service_role` key.

## Mise en route (une seule fois)

1. Ouvrez le projet Supabase associé à `https://xlfbnulmyfoigrpgbzly.supabase.co`.
2. Dans **SQL Editor**, exécutez le contenu du fichier `supabase-setup.sql` à la racine du dépôt.
3. Publiez le site (ou servez-le en HTTP local) puis choisissez un pseudo dans le panneau **Classement**. Le classement est distinct par jeu.

Les pseudos sont conservés dans le navigateur. Les jeux envoient le score au terme d'une partie (Snake/Pong/Memory) ; Space Clicker l'enregistre pendant la partie et au bouton « Recommencer ». Le meilleur score d'un pseudo pour un jeu ne peut pas être remplacé par un résultat inférieur grâce au trigger SQL.
