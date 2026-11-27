# EL GAME

Mini-plateforme de jeux HTML statiques : Snake, Memory, Space Clicker, Pong, Cosmic Breakout et Tic-Tac-Toe multijoueur.

## Lancer le site

Ouvrir `index.html` via un serveur HTTP local ou GitHub Pages. Aucun outil de compilation n’est nécessaire. Les jeux sont indépendants et jouables sur écran tactile ou clavier/souris.

## Configuration des scores Supabase

1. Dans Supabase Auth, activez **Anonymous Sign-Ins**.
2. Dans SQL Editor, appliquez `supabase-setup.sql`.
3. Déployez `supabase/functions/submit-score/index.ts` avec Supabase CLI : `supabase functions deploy submit-score`.
4. Configurez les secrets de fonction : `supabase secrets set SITE_ORIGIN=https://VOTRE-UTILISATEUR.github.io`. Pour un domaine personnalisé, utilisez son origine complète (schéma + hôte, sans chemin). `SUPABASE_URL`, `SUPABASE_ANON_KEY` et `SUPABASE_SERVICE_ROLE_KEY` doivent être disponibles à la fonction ; ne publiez jamais la service-role key dans le site.
5. Vérifiez le fournisseur anonyme et l’origine autorisée avant de déployer en production.

Le navigateur ne possède que la clé publishable. RLS autorise la lecture publique mais refuse les écritures directes ; seule la fonction serveur, après validation d’un JWT Supabase, utilise la clé service-role. La fonction impose une liste de jeux, des bornes, un pseudo valide et un délai entre les améliorations de score.

**Limite anti-triche :** un jeu exécuté entièrement dans le navigateur ne peut pas prouver son propre score. L’authentification anonyme, les limites et la fonction réduisent les abus et protègent la table, mais un client modifié peut encore envoyer un score plausible. Une garantie anti-triche forte nécessite des sessions/événements de jeu validés côté serveur et une identité vérifiée.

## Tic-Tac-Toe en ligne

Le jeu utilise Supabase Realtime Broadcast avec un code de salon à partager. Activez Realtime pour le projet et assurez-vous que les canaux Broadcast publics sont autorisés pour les clients anonymes. Le jeu reste jouable localement si Realtime n’est pas configuré. Les salons ne sont pas persistants et le code n’est pas un mécanisme d’authentification.

## Vérifications

Contrôle manuel recommandé après déploiement : largeur mobile 320–430 px et bureau, rotation d’écran, navigation clavier, tactile, parcours de score, session anonyme et salon Realtime sur deux navigateurs/appareils. L’environnement d’édition ne fournit pas de navigateur d’exécution : ces vérifications réelles ne peuvent pas être certifiées depuis le dépôt seul.
