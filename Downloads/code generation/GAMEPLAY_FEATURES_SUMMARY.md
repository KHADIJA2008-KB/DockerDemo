# Core Gameplay Features - Implementation Summary

## Overview
The `code_generator.py` has been enhanced with comprehensive core gameplay features that enable:
1. **Command Selection** from a visual palette
2. **Visual Workflow** management with sequence list
3. **Real-time Code Display** in a side panel
4. **Toggle between Template-Based and AI-Generated Code**

---

## 🎮 Core Gameplay Features

### 1.1 Command Selection

#### CommandPalette Class
A structured command palette that provides all available commands organized by category:

**Categories:**
- **Movement**: move forward, move backward, turn left, turn right, jump
- **Action**: pick object
- **Control**: loop, if/else conditional
- **Utility**: print, wait

**Features:**
- Each command has:
  - `icon`: Visual emoji representation
  - `label`: Human-readable name
  - `description`: What the command does
  - `default_params`: Default parameter values
  - `category`: Organizational category

**Usage Example:**
```python
from code_generator import CommandPalette

palette = CommandPalette()

# Get all commands
all_commands = palette.get_all_commands()

# Get commands by category
by_category = palette.get_commands_by_category()

# Get specific command
move_cmd = palette.get_command("move")
```

---

### 1.2 Visual Workflow

#### VisualWorkflow Class
Manages the sequence of selected commands with full CRUD operations:

**Features:**
- Add commands to sequence
- Remove commands from sequence
- Move commands (reorder)
- Update command parameters
- Get visual text representation
- Track current execution position

**Usage Example:**
```python
from code_generator import VisualWorkflow

workflow = VisualWorkflow()

# Add commands
workflow.add_command({"type": "move_forward", "params": {"distance": 5}})
workflow.add_command({"type": "turn_right", "params": {"degrees": 90}})

# Get visual representation
print(workflow.get_visual_representation())

# Manage commands
workflow.remove_command(0)
workflow.move_command(from_index=0, to_index=1)
workflow.update_command(0, {"type": "jump", "params": {"height": 2}})
```

**Visual Output:**
```
Visual Workflow:
==================================================
  1. move_forward - {'distance': 5}
  2. turn_right - {'degrees': 90}
  3. pick_object - {'object_name': 'key'}
==================================================
```

---

### 1.3 Code Display

#### Enhanced CodeGenerator Class
Real-time Python code generation with live preview:

**Features:**
- **Live Code Preview**: Updates as commands are added
- **Proper Nesting**: Handles loops and conditionals with correct indentation
- **Single Command Preview**: Generate code for individual commands
- **Display Mode Toggle**: Switch between template-based and AI-generated

**Usage Example:**
```python
from code_generator import CodeGenerator, CodeDisplayMode

generator = CodeGenerator()

# Generate code for blocks
blocks = [
    {"type": "move_forward", "params": {"distance": 5}},
    {"type": "turn_right", "params": {"degrees": 90}}
]

# Live preview (no implementations)
preview_code = generator.generate_live_code_preview(blocks)

# Full executable code
full_code, execution_plan = generator.generate_from_blocks(blocks, include_implementations=True)

# Single command preview
single_code = generator.generate_code_for_single_command(blocks[0])
```

**Code Output Example:**
```python
# Generated code from visual blocks
import time

# Main program

# Move forward 5 units
move_forward(5)
# Turn right 90 degrees
turn_right(90)
```

---

### 1.4 Toggle Between Code Generation Modes

#### CodeDisplayMode Enum
Switch between deterministic template-based code and AI-generated code:

**Modes:**
- `TEMPLATE_BASED`: Deterministic, rule-based code generation
- `AI_GENERATED`: AI-powered code generation (placeholder for AI API integration)

**Usage Example:**
```python
from code_generator import CodeGenerator, CodeDisplayMode

generator = CodeGenerator()

# Set display mode
generator.set_display_mode(CodeDisplayMode.AI_GENERATED)

# Get code with both modes
blocks = [{"type": "move_forward", "params": {"distance": 5}}]
code_display = generator.display_code_with_mode(blocks)

print(code_display['template_based'])  # Deterministic code
print(code_display['ai_generated'])     # AI-generated code
print(code_display['active_mode'])      # Current mode
```

---

## 🎯 GameplaySession - Main Integration Class

The `GameplaySession` class integrates all components into a complete gameplay experience:

### Features:
1. **Unified Interface**: Single class to manage palette, workflow, and code generation
2. **Add Commands**: Add commands from palette to workflow
3. **Live Code Updates**: Automatically update code display when workflow changes
4. **Export/Import**: Save and load gameplay sessions
5. **Mode Switching**: Toggle between code display modes

### Complete Example:
```python
from code_generator import GameplaySession, CodeDisplayMode

# Create session
session = GameplaySession()

# Add commands from palette
session.add_command_from_palette("move", {"distance": 5})
session.add_command_from_palette("turn_right", {"degrees": 90})
session.add_command_from_palette("pick_object", {"object_name": "key"})

# View visual workflow
print(session.get_visual_workflow())

# View generated code
print(session.code_cache)

# Toggle code display mode
code_display = session.get_code_with_mode(CodeDisplayMode.TEMPLATE_BASED)

# Export session
session_data = session.export_session()

# Import session
session.import_session(session_data)
```

---

## 🔄 Proper Nesting and Indentation

Commands wrapped in loops and conditionals are properly nested:

### Loop Example:
```python
loop_body = [
    {"type": "move_forward", "params": {"distance": 2}},
    {"type": "turn_right", "params": {"degrees": 90}},
    {"type": "pick_object", "params": {"object_name": "coin"}}
]

session.workflow.add_command({
    "type": "loop",
    "params": {"iterations": 4, "body": loop_body}
})
```

**Generated Code:**
```python
# Loop 4 times
for i in range(4):
    # Move forward 2 units
    move_forward(2)
    # Turn right 90 degrees
    turn_right(90)
    # Pick up coin
    pick_object("coin")
```

### Conditional Example:
```python
if_body = [
    {"type": "move_forward", "params": {"distance": 3}}
]
else_body = [
    {"type": "turn_left", "params": {"degrees": 180}}
]

session.workflow.add_command({
    "type": "conditional",
    "params": {
        "condition": "x > 0",
        "if_body": if_body,
        "else_body": else_body
    }
})
```

**Generated Code:**
```python
# Conditional: if x > 0
if x > 0:
    # Move forward 3 units
    move_forward(3)
else:
    # Turn left 180 degrees
    turn_left(180)
```

---

## 📋 New Commands Added

### Pick Object Command
**Type:** `pick_object`  
**Category:** Action  
**Icon:** ✋  
**Parameters:**
- `object_name`: Name of the object to pick up (default: "item")

**Generated Function:**
```python
def pick_object(object_name):
    """Pick up an object and add it to inventory."""
    character.inventory.append(object_name)
    character.log_action(f'Picked up {object_name} (inventory: {len(character.inventory)} items)')
```

**Usage:**
```python
session.add_command_from_palette("pick_object", {"object_name": "key"})
```

---

## 🚀 Quick Start Guide

### 1. Basic Usage
```python
from code_generator import GameplaySession

# Initialize
session = GameplaySession()

# Add commands
session.add_command_from_palette("move", {"distance": 10})
session.add_command_from_palette("turn_left", {"degrees": 90})
session.add_command_from_palette("jump", {"height": 3})

# View results
print(session.get_visual_workflow())
print(session.code_cache)
```

### 2. With Loops
```python
# Create loop with nested commands
loop_body = [
    {"type": "move_forward", "params": {"distance": 1}},
    {"type": "pick_object", "params": {"object_name": "coin"}}
]

session.workflow.add_command({
    "type": "loop",
    "params": {"iterations": 5, "body": loop_body}
})

session.update_code_display()
print(session.code_cache)
```

### 3. Toggle Code Modes
```python
from code_generator import CodeDisplayMode

# Get both code versions
code_display = session.get_code_with_mode(CodeDisplayMode.TEMPLATE_BASED)

print("Template-Based:")
print(code_display['template_based'])

print("\nAI-Generated:")
print(code_display['ai_generated'])
```

---

## 🧪 Testing

Run the demonstration to see all features in action:

```bash
cd "/home/khadijab/Downloads/code generation"
python3 code_generator.py
```

This will demonstrate:
1. Command palette with all available commands
2. Command selection and workflow building
3. Visual workflow representation
4. Generated Python code
5. Nested commands (loops with proper indentation)
6. Toggle between code display modes

---

## 📊 API Reference

### CommandPalette
- `get_commands_by_category()` → Dict[str, List[Dict]]
- `get_command(command_id)` → Optional[Dict]
- `get_all_commands()` → List[Dict]

### VisualWorkflow
- `add_command(command)` → int (returns index)
- `insert_command(index, command)` → None
- `remove_command(index)` → None
- `move_command(from_index, to_index)` → None
- `update_command(index, command)` → None
- `clear()` → None
- `get_sequence()` → List[Dict]
- `get_visual_representation()` → str

### CodeGenerator
- `generate_live_code_preview(blocks)` → str
- `generate_code_for_single_command(block)` → str
- `set_display_mode(mode)` → None
- `get_display_mode()` → CodeDisplayMode
- `display_code_with_mode(blocks)` → Dict[str, str]
- `generate_from_blocks(blocks, include_implementations)` → Tuple[str, List]

### GameplaySession
- `add_command_from_palette(command_id, custom_params)` → Dict
- `remove_command_from_workflow(index)` → Dict
- `update_code_display()` → str
- `get_code_with_mode(mode)` → Dict[str, str]
- `get_visual_workflow()` → str
- `get_palette_commands_by_category()` → Dict
- `export_session()` → Dict
- `import_session(session_data)` → None

---

## 🎨 UI Integration Notes

For frontend integration, the system provides:

1. **Command Palette Data**: JSON structure with icons, labels, and descriptions
2. **Visual Workflow Updates**: Real-time sequence list
3. **Live Code Display**: Updated Python code on every change
4. **Mode Toggle**: Switch between template-based and AI-generated code
5. **Session Persistence**: Export/import functionality

### Example JSON Response:
```json
{
  "success": true,
  "command_id": "move",
  "command_label": "Move Forward",
  "index": 0,
  "block": {
    "type": "move_forward",
    "params": {"distance": 5}
  },
  "code": "# Generated code..."
}
```

---

## ✅ Implementation Status

All requested features have been implemented:

- ✅ Command palette with selectable commands
- ✅ Visual workflow with sequence list
- ✅ Real-time code display in side panel
- ✅ Proper nesting and indentation for loops/conditionals
- ✅ Toggle between template-based and AI-generated code
- ✅ Pick object command added
- ✅ Full CRUD operations on workflow
- ✅ Session export/import
- ✅ Demonstration function
- ✅ Comprehensive documentation

---

## 🔮 Future Enhancements

For AI-generated code mode:
1. Integrate with OpenAI API or Claude API
2. Add prompt engineering for better code generation
3. Support code optimization suggestions
4. Add code explanation features

---

## 📝 Notes

- The AI-generated code mode currently uses a placeholder. To enable real AI generation, integrate with an AI API in the `_generate_ai_code_placeholder` method.
- All code follows proper Python conventions and includes type hints.
- The system is fully extensible - new commands can be added easily to the `BlockType` enum and command palette.
- Execution plans are generated alongside code for game engine integration.

