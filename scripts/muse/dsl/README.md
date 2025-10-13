# Muse DSL — A small domain-specific language for scripting the offline Muse assistant

This DSL enables authored scripts that let the Muse perform deterministic offline tasks: speak, remember, recall, search memories, run specific skills (gpt_like, claude_like, gemini_like), and control flow (if, loop, wait). Scripts are plain text, executed locally with no network.

Commands (one per line):
- SAY "text"                    -> Muse prints a line using skill_router for stylistic generation.
- ECHO "text"                   -> Direct echo (no skill).
- REMEMBER key = "value"        -> Store a memory key/value
- RECALL key                     -> Print a recalled memory value
- SEARCH "query"                -> Print up to 10 memory matches
- RUN_SKILL skill "input"       -> Run a named local skill directly (gpt_like, claude_like, gemini_like)
- WAIT seconds                   -> Sleep for given seconds (integer)
- IF EXISTS key                  -> Start conditional block if memory key exists
- IF EQ key "value"             -> Start conditional block if value equals
- ELSE                           -> Optional else
- ENDIF                          -> End conditional
- LOOP N                         -> Start loop N times
- ENDLOOP                        -> End loop
- IMPORT "file"                 -> Include another DSL file inline

Example script (see examples.muse in this folder).

Safety and privacy
- All operations run locally using the Muse SQLite store.
- Scripts cannot call external network; RUN_SKILL uses local, deterministic skill modules only.
