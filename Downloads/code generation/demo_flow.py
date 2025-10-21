#!/usr/bin/env python3
"""
Demonstration of the terminal input flow.
This shows how users can input commands and get generated code.
"""

from code_generator import GameplaySession, CodeDisplayMode


def demo_simple_workflow():
    """Demo 1: Simple workflow with direct input."""
    print("=" * 70)
    print("DEMO 1: Simple Workflow - User Input Flow")
    print("=" * 70)
    
    session = GameplaySession()
    
    # Simulate user input
    commands = [
        ("move", {"distance": 10}),
        ("turn_right", {"degrees": 90}),
        ("pick_object", {"object_name": "sword"}),
        ("move", {"distance": 5}),
    ]
    
    print("\n📝 User Input:")
    print("-" * 70)
    for cmd_id, params in commands:
        print(f"  Command: {cmd_id}")
        print(f"  Parameters: {params}")
        result = session.add_command_from_palette(cmd_id, params)
        if result.get('success'):
            print(f"  ✓ Added: {result['command_label']}\n")
    
    print("\n📊 Generated Visual Workflow:")
    print("-" * 70)
    print(session.get_visual_workflow())
    
    print("\n💻 Generated Python Code:")
    print("-" * 70)
    print(session.code_cache)
    print("=" * 70 + "\n")


def demo_loop_workflow():
    """Demo 2: Workflow with loop (proper nesting)."""
    print("=" * 70)
    print("DEMO 2: Loop Workflow - Square Pattern")
    print("=" * 70)
    
    session = GameplaySession()
    
    print("\n📝 User Input:")
    print("-" * 70)
    print("  Create loop with 4 iterations")
    print("  Loop body:")
    print("    - Move forward 10 units")
    print("    - Turn right 90 degrees")
    
    # Add loop command
    loop_body = [
        {"type": "move_forward", "params": {"distance": 10}},
        {"type": "turn_right", "params": {"degrees": 90}}
    ]
    
    session.workflow.add_command({
        "type": "loop",
        "params": {"iterations": 4, "body": loop_body}
    })
    session.update_code_display()
    
    print("\n📊 Generated Visual Workflow:")
    print("-" * 70)
    print(session.get_visual_workflow())
    
    print("\n💻 Generated Python Code (Note Indentation):")
    print("-" * 70)
    print(session.code_cache)
    print("=" * 70 + "\n")


def demo_complex_workflow():
    """Demo 3: Complex workflow with multiple control structures."""
    print("=" * 70)
    print("DEMO 3: Complex Workflow - Treasure Hunt")
    print("=" * 70)
    
    session = GameplaySession()
    
    print("\n📝 User Input:")
    print("-" * 70)
    print("  1. Move forward 5 units")
    print("  2. Loop 3 times:")
    print("       - Move forward 2 units")
    print("       - Pick object 'coin'")
    print("       - Turn right 45 degrees")
    print("  3. Turn left 180 degrees (return)")
    print("  4. Move forward 5 units")
    
    # Add commands
    session.add_command_from_palette("move", {"distance": 5})
    
    loop_body = [
        {"type": "move_forward", "params": {"distance": 2}},
        {"type": "pick_object", "params": {"object_name": "coin"}},
        {"type": "turn_right", "params": {"degrees": 45}}
    ]
    session.workflow.add_command({
        "type": "loop",
        "params": {"iterations": 3, "body": loop_body}
    })
    session.update_code_display()
    
    session.add_command_from_palette("turn_left", {"degrees": 180})
    session.add_command_from_palette("move", {"distance": 5})
    
    print("\n📊 Generated Visual Workflow:")
    print("-" * 70)
    print(session.get_visual_workflow())
    
    print("\n💻 Generated Python Code:")
    print("-" * 70)
    print(session.code_cache)
    print("=" * 70 + "\n")


def demo_conditional_workflow():
    """Demo 4: Workflow with conditional logic."""
    print("=" * 70)
    print("DEMO 4: Conditional Workflow - Door Logic")
    print("=" * 70)
    
    session = GameplaySession()
    
    print("\n📝 User Input:")
    print("-" * 70)
    print("  1. Set variable: has_key = True")
    print("  2. If has_key:")
    print("       - Print 'Door opened'")
    print("       - Move forward 5 units")
    print("       - Pick object 'treasure'")
    print("     Else:")
    print("       - Print 'Need key'")
    print("       - Turn around 180 degrees")
    
    # Add variable
    session.workflow.add_command({
        "type": "variable",
        "params": {"name": "has_key", "value": True}
    })
    
    # Add conditional
    if_body = [
        {"type": "print", "params": {"message": "Door opened"}},
        {"type": "move_forward", "params": {"distance": 5}},
        {"type": "pick_object", "params": {"object_name": "treasure"}}
    ]
    
    else_body = [
        {"type": "print", "params": {"message": "Need key"}},
        {"type": "turn_left", "params": {"degrees": 180}}
    ]
    
    session.workflow.add_command({
        "type": "conditional",
        "params": {
            "condition": "has_key",
            "if_body": if_body,
            "else_body": else_body
        }
    })
    session.update_code_display()
    
    print("\n📊 Generated Visual Workflow:")
    print("-" * 70)
    print(session.get_visual_workflow())
    
    print("\n💻 Generated Python Code (Note If/Else Nesting):")
    print("-" * 70)
    print(session.code_cache)
    print("=" * 70 + "\n")


def demo_executable_code():
    """Demo 5: Generate executable code with implementations."""
    print("=" * 70)
    print("DEMO 5: Executable Code - Ready to Run")
    print("=" * 70)
    
    session = GameplaySession()
    
    print("\n📝 User Input:")
    print("-" * 70)
    print("  1. Move forward 3 units")
    print("  2. Turn right 90 degrees")
    print("  3. Pick object 'key'")
    print("  4. Jump 2 units high")
    
    # Add commands
    session.add_command_from_palette("move", {"distance": 3})
    session.add_command_from_palette("turn_right", {"degrees": 90})
    session.add_command_from_palette("pick_object", {"object_name": "key"})
    session.add_command_from_palette("jump", {"height": 2})
    
    print("\n💻 Generated Executable Python Code:")
    print("-" * 70)
    
    # Generate executable code
    sequence = session.workflow.get_sequence()
    code, _ = session.generator.generate_from_blocks(sequence, include_implementations=True)
    print(code)
    
    print("\n" + "=" * 70)
    print("This code is ready to run! Save it and execute with: python3 <filename>.py")
    print("=" * 70 + "\n")


def demo_code_mode_toggle():
    """Demo 6: Toggle between code display modes."""
    print("=" * 70)
    print("DEMO 6: Code Display Mode Toggle")
    print("=" * 70)
    
    session = GameplaySession()
    
    print("\n📝 User Input:")
    print("-" * 70)
    print("  1. Move forward 5 units")
    print("  2. Pick object 'gem'")
    print("  3. Turn left 90 degrees")
    
    session.add_command_from_palette("move", {"distance": 5})
    session.add_command_from_palette("pick_object", {"object_name": "gem"})
    session.add_command_from_palette("turn_left", {"degrees": 90})
    
    # Get both modes
    code_display = session.get_code_with_mode(CodeDisplayMode.TEMPLATE_BASED)
    
    print("\n💻 TEMPLATE-BASED CODE (Deterministic):")
    print("-" * 70)
    print(code_display['template_based'])
    
    print("\n🤖 AI-GENERATED CODE (Placeholder):")
    print("-" * 70)
    print(code_display['ai_generated'])
    
    print("=" * 70 + "\n")


def main():
    """Run all demonstrations."""
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "TERMINAL INPUT FLOW DEMONSTRATION" + " " * 20 + "║")
    print("╚" + "═" * 68 + "╝")
    print("\nThis demonstrates how users input commands and receive generated code.\n")
    
    demos = [
        demo_simple_workflow,
        demo_loop_workflow,
        demo_complex_workflow,
        demo_conditional_workflow,
        demo_executable_code,
        demo_code_mode_toggle
    ]
    
    for demo in demos:
        demo()
        input("Press Enter to continue to next demo...")
        print("\n")
    
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 22 + "ALL DEMOS COMPLETED!" + " " * 25 + "║")
    print("╚" + "═" * 68 + "╝")
    print("\n💡 To try it yourself, run: python3 main.py")
    print("💡 For quick mode, run: python3 main.py --quick\n")


if __name__ == "__main__":
    main()

