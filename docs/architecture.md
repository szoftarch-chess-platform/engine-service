# Engine service architecture

The diagram shows only the decisions made in ADR-1 and ADR-6.

```plantuml
@startuml

actor "Player" as Player
component "Game Service" as Game
component "Engine Service" as Engine
component "Stockfish" as Stockfish

Player --> Game : move
Game --> Engine : POST /moves with FEN
Engine --> Stockfish : UCI analysis
Stockfish --> Engine : best move
Engine --> Game : UCI move
Game --> Player : updated position

@enduml
```

The game service sends synchronous requests over the internal Docker network. It owns game rules and game state. The engine service parses FEN and delegates move selection to Stockfish.
