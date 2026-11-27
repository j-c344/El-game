// Secure score submission endpoint. Deploy as Supabase Edge Function `submit-score`.
// The service-role key stays server-side; caller identity is verified with Supabase Auth.
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

const siteOrigin = Deno.env.get('SITE_ORIGIN') ?? '';
const corsHeaders = {
  'Access-Control-Allow-Origin': siteOrigin || 'null',
  'Access-Control-Allow-Headers': 'authorization, apikey, content-type, x-client-info',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Vary': 'Origin',
};
const maxScores: Record<string, number> = {
  snake: 10_000,
  memory: 1_000_000,
  clicker: 1_000_000,
  pong: 10_000,
  breakout: 100_000,
};

Deno.serve(async (req: Request) => {
  const origin = req.headers.get('origin');
  if (req.method === 'OPTIONS') return new Response('ok', { headers: corsHeaders });
  if (req.method !== 'POST' || !origin || origin !== siteOrigin) {
    return reply({ error: 'Forbidden' }, 403);
  }

  const token = req.headers.get('authorization')?.replace(/^Bearer\s+/i, '');
  if (!token) return reply({ error: 'Authentication required' }, 401);

  const url = Deno.env.get('SUPABASE_URL');
  const anonKey = Deno.env.get('SUPABASE_ANON_KEY');
  const serviceKey = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY');
  if (!url || !anonKey || !serviceKey || !siteOrigin) {
    return reply({ error: 'Server configuration error' }, 500);
  }

  const auth = createClient(url, anonKey, {
    auth: { persistSession: false, autoRefreshToken: false },
  });
  const { data: { user }, error: authError } = await auth.auth.getUser(token);
  if (authError || !user) return reply({ error: 'Invalid session' }, 401);

  let body: Record<string, unknown>;
  try {
    body = await req.json();
  } catch {
    return reply({ error: 'Invalid JSON' }, 400);
  }

  const game = body.game_id;
  const score = body.score;
  const name = typeof body.player_name === 'string' ? body.player_name.trim() : '';
  if (
    typeof game !== 'string' || !Object.hasOwn(maxScores, game) ||
    !Number.isSafeInteger(score) || (score as number) < 1 ||
    (score as number) > maxScores[game] ||
    !/^[\p{L}\p{N}_ -]{2,20}$/u.test(name)
  ) {
    return reply({ error: 'Invalid score payload' }, 400);
  }

  const admin = createClient(url, serviceKey, {
    auth: { persistSession: false, autoRefreshToken: false },
  });
  const { data: previous, error: lookupError } = await admin
    .from('scores')
    .select('score,updated_at')
    .eq('game_id', game)
    .eq('player_id', user.id)
    .maybeSingle();
  if (lookupError) return reply({ error: 'Score lookup failed' }, 500);

  if (
    previous && Date.now() - Date.parse(previous.updated_at) < 5_000 &&
    (score as number) > previous.score
  ) {
    return reply({ error: 'Please wait before submitting another score' }, 429);
  }

  // Requires the non-partial unique index on (game_id, player_id) created by the SQL setup.
  const { error } = await admin.from('scores').upsert(
    { game_id: game, player_id: user.id, player_name: name, score },
    { onConflict: 'game_id,player_id' },
  );
  if (error) return reply({ error: 'Score save failed' }, 500);
  return reply({ ok: true }, 200);

  function reply(payload: unknown, status: number) {
    return new Response(JSON.stringify(payload), {
      status,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
    });
  }
});
