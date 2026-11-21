# ES-ADR-2: Stockfish as the chess engine

**Related:** F-2, NF-6, ADR-1, ADR-6, ADR-8, ADR-10, [ES-ADR-1](container-image.md)

## Context

ADR-1 decides that an external engine generates the computer moves. ADR-6 decides that the engine-service gets a position in FEN and returns a move in UCI notation within the time limit of its contract.

## Decision

- The engine is Stockfish 19.
- Stockfish runs as a separate process next to the service in the same container, and the service talks to it over UCI on its standard input and output.
- The bot plays at one fixed strength, without difficulty levels.
- The service chooses the thinking time of Stockfish below the time limit of the contract.
- The service checks the FEN before it passes it to Stockfish, and it starts Stockfish again if the process exits.

## Rationale

- The team chose Stockfish without difficulty levels.
- Stockfish is the strongest open-source engine and it is actively developed, with version 19 on 5 September 2026. It speaks UCI, the standard protocol of chess engines, whose move notation ADR-8 uses.
- The project publishes universal binaries for Linux on x86-64 and ARM64, which detect the features of the processor, so the image can be built for the two architectures of the other images.
- Since version 19 Stockfish validates the positions, the FEN strings and the UCI commands strictly, and it terminates on an error. So an invalid FEN must not reach it.
- Programs that exchange data over pipes are normally separate programs in the sense of the GPL, so the service talks to Stockfish as a separate program.

## Rejected alternatives

- **Difficulty levels:** Stockfish can limit its strength through UCI options, but the team does not need levels in the first version. They can come later with an optional field of the move request.
- **An engine of our own:** ADR-1 decides on an external engine.

## Consequences

- Stockfish is under GPL-3.0, and the published image contains it, so the README names its version and links to its source.
- The thinking time limits the throughput. One process that thinks 10 seconds per move serves six moves per minute, so parallel games against the bot need several processes or a much shorter thinking time (NF-6).
- To do: Stockfish goes into the image, and the move request of the contract into the service.

## Open questions

- How Stockfish 19 gets into the image. The documentation does not say whether the official Linux binaries run on Alpine, which uses musl. Alpine has Stockfish 19 only in its edge branch, in the testing repository, and Debian trixie has version 17. If no option works on Alpine, the image moves to `python:3.14-slim`, which is a change of one line.
- Whether the service checks the FEN and runs Stockfish with python-chess or with its own code. python-chess is under GPL-3.0-or-later, so with it the code of the engine-service would also have to be released under the GPL, and its package lists Python versions only up to 3.13.
- The fixed strength and the thinking time of the bot, and how many Stockfish processes serve parallel requests.

## Sources

- Stockfish 19: https://stockfishchess.org/blog/2026/stockfish-19/
- Stockfish: https://github.com/official-stockfish/Stockfish
- Downloads of Stockfish: https://stockfishchess.org/download/
- GPL FAQ, aggregates and separate programs: https://www.gnu.org/licenses/gpl-faq.html#MereAggregation
