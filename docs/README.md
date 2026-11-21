# engine-service documentation

- System documentation: the `docs/` folder of the infra repo

## ADRs

| ID | Title |
|---|---|
| [ES-ADR-1](adr/container-image.md) | Container image on Debian slim |

## Integration

- [Integration contract](integration.md)
- [Architecture](architecture.md)

## Open questions

None yet.

## Next steps
- Integrate the game-service HTTP caller and retry policy.
- Add system-level Compose smoke coverage after the game-service is available.
