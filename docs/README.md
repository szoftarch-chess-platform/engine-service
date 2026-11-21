# engine-service documentation

- System documentation: the `docs/` folder of the infra repo

## ADRs

| ID | Title |
|---|---|
| [ES-ADR-1](adr/container-image.md) | Container image on Debian slim |
| [ES-ADR-2](adr/chess-engine.md) | Stockfish as the chess engine |
| [ES-ADR-3](adr/web-framework.md) | FastAPI as the web framework |

## Integration

- [Integration contract](integration.md)
- [Architecture](architecture.md)

## Open questions

- The open question of [ES-ADR-2](adr/chess-engine.md) on how many Stockfish processes serve parallel games against the bot.

## Next steps
- Publish the image to the GitHub Container Registry for a version tag, as ADR-2 decides.
- Complete the system-level integration after the game-service calls the engine.
