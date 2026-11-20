# engine-service documentation

- System documentation: the `docs/` folder of the infra repo

## ADRs

| ID | Title |
|---|---|
| [ES-ADR-1](adr/container-image.md) | Container image on Alpine |
| [ES-ADR-2](adr/chess-engine.md) | Stockfish as the chess engine |

## Open questions

- The open questions of [ES-ADR-2](adr/chess-engine.md) on how Stockfish gets into the image, on python-chess, and on the strength, the thinking time and the number of processes of the bot.
- The web framework, for example FastAPI, or the standard library as in the walking skeleton.

## Next steps

- Answer the open questions above.
- Implement `POST /moves` as the contract `engine-service.openapi.yaml` of the infra repo describes, with Stockfish, the check of the FEN and the restart of ES-ADR-2.
- Add tests with the example of the contract, with a position without a legal move and with invalid FENs.
- Name the version of Stockfish and the link to its source in the README, and describe the new configuration there.
- Add the CI workflow of ADR-2.
