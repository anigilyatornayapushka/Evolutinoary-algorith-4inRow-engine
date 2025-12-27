# Connect Four AI Engine

A cleanly architected "Connect Four" game with implementation of engine.

## Project Essence
A modular game engine separating board logic, interface, game flow, and AI decision-making into distinct components for maximum maintainability and extensibility.

## Clean Code Philosophy
Each module has a single responsibility: Board manages state, Interface handles display, Game controls flow, Engine calculates AI moves. This separation enables independent testing and modification.

## MVC + Agent Architecture
- **Model** (`board.py`): Game state and rules
- **View** (`interface.py`): User interaction
- **Controller** (`game.py`): Game orchestration  
- **Agent** (`engine.py`): AI decision-making

The Agent extends MVC allowing to seperate Engine logic from game control for easy algorithm swapping.

## License
MIT License - see [LICENSE](LICENSE) for details.
