#!/usr/bin/env python3
"""
Simple test showing terminal input → code output flow
"""

from code_generator import GameplaySession

def test_simple_flow():
    """Test simple command flow with printed output."""
    
    print("="*70)
    print("TEST: Terminal Input Flow → Printed Code Output")
    print("="*70)
    
    # Create session
    session = GameplaySession()
    
    # Simulate user input
    print("\n📝 USER INPUT (Terminal Commands):")
    print("-"*70)
    
    commands = [
        ("move", {"distance": 10}, "Move forward 10 units"),
        ("turn_right", {"degrees": 90}, "Turn right 90 degrees"),
        ("pick_object", {"object_name": "sword"}, "Pick object 'sword'"),
        ("jump", {"height": 5}, "Jump 5 units high"),
    ]
    
    for cmd_id, params, description in commands:
        print(f"  → {description}")
        session.add_command_from_palette(cmd_id, params)
    
    # Print generated code
    print("\n💻 GENERATED CODE OUTPUT (Printed to Terminal):")
    print("-"*70)
    print(session.code_cache)
    print("="*70)


def test_loop_flow():
    """Test loop with proper nesting."""
    
    print("\n\n")
    print("="*70)
    print("TEST: Loop Flow → Code with Proper Indentation")
    print("="*70)
    
    session = GameplaySession()
    
    print("\n📝 USER INPUT:")
    print("-"*70)
    print("  → Create loop: 4 iterations")
    print("      └─ Move forward 10 units")
    print("      └─ Turn right 90 degrees")
    
    # Add loop
    loop_body = [
        {"type": "move_forward", "params": {"distance": 10}},
        {"type": "turn_right", "params": {"degrees": 90}}
    ]
    
    session.workflow.add_command({
        "type": "loop",
        "params": {"iterations": 4, "body": loop_body}
    })
    session.update_code_display()
    
    # Print generated code
    print("\n💻 GENERATED CODE OUTPUT:")
    print("-"*70)
    print(session.code_cache)
    print("="*70)


def test_executable_flow():
    """Test executable code generation."""
    
    print("\n\n")
    print("="*70)
    print("TEST: Executable Code → Ready to Run")
    print("="*70)
    
    session = GameplaySession()
    
    print("\n📝 USER INPUT:")
    print("-"*70)
    print("  → Move forward 5 units")
    print("  → Pick object 'gem'")
    print("  → Turn left 90 degrees")
    
    session.add_command_from_palette("move", {"distance": 5})
    session.add_command_from_palette("pick_object", {"object_name": "gem"})
    session.add_command_from_palette("turn_left", {"degrees": 90})
    
    # Generate executable code
    sequence = session.workflow.get_sequence()
    code, _ = session.generator.generate_from_blocks(sequence, include_implementations=True)
    
    # Print executable code
    print("\n💻 EXECUTABLE CODE OUTPUT (With Implementations):")
    print("-"*70)
    print(code)
    print("="*70)
    print("\n✅ This code can be saved and run directly with: python3 output.py")


if __name__ == "__main__":
    print("\n" + "╔" + "═"*68 + "╗")
    print("║  DEMONSTRATION: Terminal Input → Generated Code (Print Output)  ║")
    print("╚" + "═"*68 + "╝\n")
    
    test_simple_flow()
    test_loop_flow()
    test_executable_flow()
    
    print("\n" + "╔" + "═"*68 + "╗")
    print("║                    ALL TESTS COMPLETED ✓                        ║")
    print("╚" + "═"*68 + "╝")
    print("\n💡 To use interactively: python3 main.py")
    print("💡 For quick mode: python3 main.py --quick\n")

