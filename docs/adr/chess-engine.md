# ES-ADR-2: Stockfish as the chess engine

**Related:** F-2, NF-6, ADR-1, ADR-6, ADR-8, ADR-10, [ES-ADR-1](container-image.md), [ES-ADR-3](web-framework.md)

## Context

ADR-1 decides that an external engine generates the computer moves. ADR-6 decides that the engine-service gets a position in FEN and returns a move in UCI notation within the time limit of its contract.

## Decision

- The engine is Stockfish from the package of Debian in the base image of ES-ADR-1. The documents name no exact version of it.
- Stockfish runs as a separate process next to the service in the same container, and the service talks to it over UCI on its standard input and output.
- The service checks the FEN and talks to Stockfish with python-chess, and it starts Stockfish again if the process exits.
- The bot plays at one fixed strength, without difficulty levels. Stockfish searches to the depth of `STOCKFISH_DEPTH`, which is 10 by default, and for at most 8.5 seconds, which is below the time limit of the contract.
- One Stockfish process serves the requests one after the other, and a request waits at most one second for it.
- The code of the engine-service is under the GNU General Public License version 3 or any later version.

## Rationale

- The team chose Stockfish without difficulty levels.
- Stockfish is the strongest open-source engine and it is actively developed. It speaks UCI, the standard protocol of chess engines, whose move notation ADR-8 uses.
- Debian packages Stockfish for amd64 and arm64, so the image can be built for the two architectures of the other images without a download of its own.
- Stockfish can stop or misbehave on an invalid FEN, so an invalid FEN must not reach it.
- python-chess checks the FEN, the legal moves and the end of the game, and it runs a UCI engine as a separate process with a depth and a time limit, so the service needs no code of its own for these.
- python-chess is under GPL-3.0-or-later, and the service imports it, so the service is under the same license.
- Programs that exchange data over pipes are normally separate programs in the sense of the GPL, so the service talks to Stockfish as a separate program.
- The depth sets the strength, and the time limit keeps a deep search below the 10 seconds of the contract.
- One process is the simplest setup for the first version.

## Rejected alternatives

- **Difficulty levels:** Stockfish can limit its strength through UCI options, but the team does not need levels in the first version. They can come later with an optional field of the move request.
- **An engine of our own:** ADR-1 decides on an external engine.
- **The official binaries of the Stockfish project:** they give the newest version, but the image would have to download and check a binary for each architecture.
- **Own code instead of python-chess:** the service could keep a permissive license, but it would have to check the FEN and speak UCI itself.

## Consequences

- Stockfish is under GPL-3.0, and the published image contains it, so the README links to its source.
- The image gets the Stockfish of the Debian release of its base image, so a new Debian release can bring a new version of Stockfish.
- The package of python-chess lists Python versions only up to 3.13, while the service runs on Python 3.14, which the tests cover.
- The thinking time limits the throughput. A request that arrives while the process searches fails with 500 after one second, so parallel games against the bot need several processes or a much shorter thinking time (NF-6).

## Open questions

- How many Stockfish processes serve parallel games against the bot, and how a request waits for a free one (NF-6).

## Sources

- Stockfish: https://github.com/official-stockfish/Stockfish
- Downloads of Stockfish: https://stockfishchess.org/download/
- The Stockfish package of Debian: https://tracker.debian.org/pkg/stockfish
- python-chess: https://python-chess.readthedocs.io/
- GPL FAQ, aggregates and separate programs: https://www.gnu.org/licenses/gpl-faq.html#MereAggregation
- GPL FAQ, programs that use a GPL library: https://www.gnu.org/licenses/gpl-faq.html#IfLibraryIsGPL
