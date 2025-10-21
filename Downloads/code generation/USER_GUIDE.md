# User Guide - Terminal Input Flow 📝

## How to Use: Input Flow → Generated Code

This guide shows exactly how users provide input and receive generated code.

---

## 🎯 Method 1: Interactive Terminal (Full Featured)

### Start the Program
```bash
python3 main.py
```

### Flow Example
```
🎮 INTERACTIVE CODE GENERATOR
======================================================================

📋 MAIN MENU:
----------------------------------------------------------------------
1. View Available Commands
2. Add Command to Workflow
3. View Current Workflow
4. Generate Code (Template-Based)
5. Generate Code (AI-Generated)
6. Generate Executable Code
7. Clear Workflow
8. Remove Last Command
9. Export Workflow
0. Exit
----------------------------------------------------------------------

Enter your choice: 2

➕ ADD COMMAND
======================================================================

Available Commands:
  1. → Move Forward
  2. ← Move Backward
  3. ↰ Turn Left
  4. ↱ Turn Right
  5. ⤴ Jump
  6. ✋ Pick Object
  ... (more commands)

Enter command number (or command ID): 1

✓ Selected: Move Forward
Default parameters: {'distance': 1}

Customize parameters? (y/n): y

Enter custom parameters (press Enter to use default):
  distance (default: 1): 10

✅ Added: Move Forward
Position: 1
```

### View Generated Code
```
Enter your choice: 4

💻 GENERATED CODE:
======================================================================
Mode: Template-Based (Deterministic)

# Generated code from visual blocks
import time

# Main program

# Move forward 10 units
move_forward(10)

======================================================================
```

---

## ⚡ Method 2: Quick Mode (Fastest Input)

### Start Quick Mode
```bash
python3 main.py --quick
```

### Flow Example
```
⚡ QUICK ADD MODE
======================================================================
Enter commands quickly. Examples:
  move 5         - Move forward 5 units
  turn_left 90   - Turn left 90 degrees
  turn_right 45  - Turn right 45 degrees
  jump 3         - Jump 3 units high
  pick key       - Pick object named 'key'
  print Hello    - Print 'Hello'
  done           - Finish and return to menu
----------------------------------------------------------------------

> move 10
  ✓ Added: Move Forward

> turn_right 90
  ✓ Added: Turn Right

> pick sword
  ✓ Added: Pick Object

> jump 5
  ✓ Added: Jump

> done

✅ Quick add completed!
```

Then view the workflow and code from the main menu (options 3 and 4).

---

## 🐍 Method 3: Python Script (Direct API)

### Create a Python Script
```python
from code_generator import GameplaySession

# Initialize session
session = GameplaySession()

# User inputs commands
session.add_command_from_palette("move", {"distance": 10})
session.add_command_from_palette("turn_right", {"degrees": 90})
session.add_command_from_palette("pick_object", {"object_name": "sword"})

# Print generated code
print("=" * 70)
print("GENERATED CODE:")
print("=" * 70)
print(session.code_cache)
```

### Run the Script
```bash
python3 your_script.py
```

### Output
```
======================================================================
GENERATED CODE:
======================================================================
# Generated code from visual blocks
import time

# Main program

# Move forward 10 units
move_forward(10)
# Turn right 90 degrees
turn_right(90)
# Pick up sword
pick_object("sword")
```

---

## 📊 Complete Example: Square Pattern

### User Input (Quick Mode)
```
> move 10
> turn_right 90
> move 10
> turn_right 90
> move 10
> turn_right 90
> move 10
> turn_right 90
> done
```

### Generated Code (Printed)
```python
# Generated code from visual blocks
import time

# Main program

# Move forward 10 units
move_forward(10)
# Turn right 90 degrees
turn_right(90)
# Move forward 10 units
move_forward(10)
# Turn right 90 degrees
turn_right(90)
# Move forward 10 units
move_forward(10)
# Turn right 90 degrees
turn_right(90)
# Move forward 10 units
move_forward(10)
# Turn right 90 degrees
turn_right(90)
```

---

## 🔄 With Loops (Better Approach)

### User Input (Interactive Mode - Option 2)
1. Choose "Add Command to Workflow"
2. Select "Loop" command
3. Set iterations: 4
4. Add loop body commands:
   - move_forward(10)
   - turn_right(90)

### Generated Code (Printed with Proper Nesting)
```python
# Generated code from visual blocks
import time

# Main program

# Loop 4 times
for i in range(4):
    # Move forward 10 units
    move_forward(10)
    # Turn right 90 degrees
    turn_right(90)
```

---

## 🎮 Complete Workflow Example

### User Story: Treasure Hunt Game

**Objective:** Move to treasure, collect items, return home

### User Input Flow
```
1. Add Command → Move Forward → distance: 5
2. Add Command → Loop → iterations: 3
   Loop Body:
   - Move Forward → distance: 2
   - Pick Object → object_name: coin
   - Turn Right → degrees: 45
3. Add Command → Turn Left → degrees: 180
4. Add Command → Move Forward → distance: 5
5. Generate Code → Option 4
```

### Generated Code Output (Printed)
```python
# Generated code from visual blocks
import time

# Main program

# Move forward 5 units
move_forward(5)
# Loop 3 times
for i in range(3):
    # Move forward 2 units
    move_forward(2)
    # Pick up coin
    pick_object("coin")
    # Turn right 45 degrees
    turn_right(45)
# Turn left 180 degrees
turn_left(180)
# Move forward 5 units
move_forward(5)
```

---

## 💡 Key Points

### Input Methods
1. **Interactive Menu** - Full control, best for complex workflows
2. **Quick Mode** - Fast command entry, best for simple sequences
3. **Python API** - Programmatic access, best for automation

### Code Output
- **Always printed** to terminal/console
- **Properly formatted** with comments and indentation
- **Ready to use** - copy and run immediately
- **Multiple modes** - Template-based, AI-generated, or Executable

### Workflow
```
User Input → Command Selection → Visual Workflow → Code Generation → Print Output
```

---

## 🚀 Quick Start Commands

```bash
# Interactive mode
python3 main.py

# Quick mode
python3 main.py --quick

# See demonstrations
python3 demo_flow.py

# Help
python3 main.py --help
```

---

## 📝 Summary

**Input:** User selects commands via terminal (menu or quick mode)  
**Process:** System builds workflow and generates code  
**Output:** Code printed to terminal in clean, formatted style  

**Key Feature:** Real-time code generation as commands are added!

---

That's it! Start with `python3 main.py` and follow the prompts. Your code will be printed automatically when you choose to generate it.

