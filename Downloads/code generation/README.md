# Interactive Code Generator 🎮

A terminal-based interactive code generator that converts visual block commands into Python code. Perfect for teaching programming concepts, game development workflows, and creating executable code from high-level commands.

## ✨ Features

### Core Gameplay Features
1. **Command Selection** - Select commands from a visual palette
2. **Visual Workflow** - Commands displayed in a sequence list
3. **Real-time Code Display** - See Python code generated instantly
4. **Code Toggle** - Switch between template-based and AI-generated code
5. **Proper Nesting** - Loops and conditionals with correct indentation
6. **Executable Code** - Generate code that runs immediately

### Available Commands

#### Movement Commands
- 🔹 Move Forward/Backward
- 🔹 Turn Left/Right
- 🔹 Jump

#### Action Commands
- 🔹 Pick Object

#### Control Flow
- 🔹 Loop (for iterations)
- 🔹 Conditional (if/else)

#### Utility Commands
- 🔹 Print
- 🔹 Wait/Sleep

## 🚀 Quick Start

### Installation

```bash
# No external dependencies required!
# Just Python 3.6+
```

### Running the Application

```bash
# Interactive mode (recommended)
python3 main.py

# Quick add mode
python3 main.py --quick

# Help
python3 main.py --help
```

## 📖 Usage Guide

### Interactive Mode

Run the program and follow the menu:

```bash
python3 main.py
```

**Main Menu Options:**
1. **View Available Commands** - See all commands with descriptions
2. **Add Command to Workflow** - Add commands one by one
3. **View Current Workflow** - See your command sequence
4. **Generate Code (Template-Based)** - Get deterministic Python code
5. **Generate Code (AI-Generated)** - Get AI-style code (placeholder)
6. **Generate Executable Code** - Get code with full implementations
7. **Clear Workflow** - Start over
8. **Remove Last Command** - Undo last addition
9. **Export Workflow** - Save your workflow
0. **Exit** - Quit the program

### Quick Add Mode

For faster command input, use quick mode:

```bash
python3 main.py --quick
```

**Quick Commands:**
- `move 5` - Move forward 5 units
- `turn_left 90` - Turn left 90 degrees
- `turn_right 45` - Turn right 45 degrees
- `jump 3` - Jump 3 units high
- `pick key` - Pick object named "key"
- `print Hello` - Print "Hello"
- `done` - Finish and generate code

## 📝 Example Workflows

### Example 1: Simple Movement
```
> move 5
> turn_right 90
> move 3
> done
```

**Generated Code:**
```python
# Move forward 5 units
move_forward(5)
# Turn right 90 degrees
turn_right(90)
# Move forward 3 units
move_forward(3)
```

### Example 2: Square Pattern (Loop)
```python
# From the interactive menu, create a loop with:
# - 4 iterations
# - Body: move_forward(10), turn_right(90)
```

**Generated Code:**
```python
# Loop 4 times
for i in range(4):
    # Move forward 10 units
    move_forward(10)
    # Turn right 90 degrees
    turn_right(90)
```

### Example 3: Treasure Hunt
```
> move 5
> pick coin
> turn_right 90
> move 3
> pick gem
> done
```

**Generated Code:**
```python
# Move forward 5 units
move_forward(5)
# Pick up coin
pick_object("coin")
# Turn right 90 degrees
turn_right(90)
# Move forward 3 units
move_forward(3)
# Pick up gem
pick_object("gem")
```

## 🏗️ Project Structure

```
code generation/
├── main.py                          # Interactive terminal interface
├── code_generator.py                # Core code generation engine
├── README.md                        # This file
├── requirements.txt                 # Dependencies (none required)
└── GAMEPLAY_FEATURES_SUMMARY.md    # Detailed feature documentation
```

## 🔧 Technical Details

### Architecture

The system consists of three main components:

1. **CommandPalette** - Manages available commands and their metadata
2. **VisualWorkflow** - Tracks the sequence of selected commands
3. **CodeGenerator** - Converts commands to Python code

### Code Generation Modes

1. **Template-Based (Deterministic)**
   - Rule-based code generation
   - Consistent, predictable output
   - Perfect for learning and teaching

2. **AI-Generated (Placeholder)**
   - Natural language style
   - Ready for AI API integration
   - More conversational code

3. **Executable**
   - Full function implementations
   - Character state management
   - Ready to run immediately

## 💡 Use Cases

### Education
- Teaching programming concepts
- Visual programming for beginners
- Understanding control flow

### Game Development
- Scripting character movements
- Level design prototyping
- AI behavior patterns

### Automation
- Workflow automation scripts
- Task sequencing
- Process documentation

## 🎯 API Usage (Programmatic)

You can also use the code generator programmatically:

```python
from code_generator import GameplaySession

# Create a session
session = GameplaySession()

# Add commands
session.add_command_from_palette("move", {"distance": 5})
session.add_command_from_palette("turn_right", {"degrees": 90})
session.add_command_from_palette("pick_object", {"object_name": "key"})

# Get generated code
print(session.code_cache)

# Export workflow
workflow_data = session.export_session()
```

For detailed API documentation, see `GAMEPLAY_FEATURES_SUMMARY.md`.

## 🔄 Code Examples

### Basic Movement
```python
# Generated code from: move 10, turn_left 90, jump 5
move_forward(10)
turn_left(90)
jump(5)
```

### With Loop (Proper Nesting)
```python
# Generated code from loop(3) with move(5), pick(coin)
for i in range(3):
    move_forward(5)
    pick_object("coin")
```

### With Conditional (Proper Nesting)
```python
# Generated code from if/else
if has_key:
    print("Opening door")
    move_forward(5)
else:
    print("Need key")
    turn_left(180)
```

## 🤝 Contributing

This is a clean, modular codebase. To add new commands:

1. Add to `BlockType` enum in `code_generator.py`
2. Add to `CommandPalette._initialize_commands()`
3. Add handler method `_handle_your_command()`
4. Add to handler mapping in `_process_block()`

## 📄 License

Open source - feel free to use and modify.

## 🆘 Support

For detailed documentation on all features, see:
- `GAMEPLAY_FEATURES_SUMMARY.md` - Complete feature documentation
- Run `python3 main.py --help` for usage help

## 🎓 Learning Path

1. **Beginner**: Use Quick Mode with simple movement commands
2. **Intermediate**: Create loops and use the interactive menu
3. **Advanced**: Use conditionals, export workflows, integrate API

## ⚡ Tips

- Type `quick` or `q` in the main menu for quick add mode
- Press Enter on parameter prompts to use defaults
- Use executable code mode to run your generated code
- Export workflows to save and share your creations

---

**Happy Coding! 🚀**
