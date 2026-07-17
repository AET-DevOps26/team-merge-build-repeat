-- Only games referenced by exactly one legacy account can be assigned safely.
-- Unreferenced or ambiguously referenced games remain ownerless and inaccessible.
WITH uniquely_owned_games AS (
    SELECT game_id, (array_agg(user_id))[1] AS user_id
    FROM account
    WHERE game_id IS NOT NULL
    GROUP BY game_id
    HAVING COUNT(*) = 1
)
UPDATE game_properties AS game
SET user_id = ownership.user_id
FROM uniquely_owned_games AS ownership
WHERE game.id = ownership.game_id
  AND game.user_id IS NULL;
