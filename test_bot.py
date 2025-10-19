"""
Unit tests for Session Advisor Bot
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import functions from bot.py (without running the bot)
from bot import calculate_load_split, get_benefits, get_motto, format_message


def test_calculate_load_split():
    """Test load split calculation logic."""
    print("Testing calculate_load_split...")
    
    # High energy and sleep -> Lift Weights
    mechanical, metabolic, workout_type = calculate_load_split(4, 4)
    assert mechanical == 70 and metabolic == 30 and workout_type == "Lift Weights", \
        f"Expected 70/30 Lift Weights, got {mechanical}/{metabolic} {workout_type}"
    
    mechanical, metabolic, workout_type = calculate_load_split(5, 5)
    assert mechanical == 70 and metabolic == 30 and workout_type == "Lift Weights", \
        f"Expected 70/30 Lift Weights, got {mechanical}/{metabolic} {workout_type}"
    
    # Medium energy and sleep -> Technique Lift
    mechanical, metabolic, workout_type = calculate_load_split(3, 3)
    assert mechanical == 60 and metabolic == 40 and workout_type == "Technique Lift", \
        f"Expected 60/40 Technique Lift, got {mechanical}/{metabolic} {workout_type}"
    
    mechanical, metabolic, workout_type = calculate_load_split(3, 4)
    assert mechanical == 60 and metabolic == 40 and workout_type == "Technique Lift", \
        f"Expected 60/40 Technique Lift, got {mechanical}/{metabolic} {workout_type}"
    
    # Low energy or sleep -> Swim or Aqua
    mechanical, metabolic, workout_type = calculate_load_split(2, 3)
    assert mechanical == 40 and metabolic == 60 and workout_type == "Swim or Aqua", \
        f"Expected 40/60 Swim or Aqua, got {mechanical}/{metabolic} {workout_type}"
    
    mechanical, metabolic, workout_type = calculate_load_split(3, 2)
    assert mechanical == 40 and metabolic == 60 and workout_type == "Swim or Aqua", \
        f"Expected 40/60 Swim or Aqua, got {mechanical}/{metabolic} {workout_type}"
    
    mechanical, metabolic, workout_type = calculate_load_split(1, 1)
    assert mechanical == 40 and metabolic == 60 and workout_type == "Swim or Aqua", \
        f"Expected 40/60 Swim or Aqua, got {mechanical}/{metabolic} {workout_type}"
    
    # Edge case -> Balanced recovery
    mechanical, metabolic, workout_type = calculate_load_split(3, 1)
    assert mechanical == 40 and metabolic == 60 and workout_type == "Swim or Aqua", \
        f"Expected 40/60 Swim or Aqua, got {mechanical}/{metabolic} {workout_type}"
    
    print("✓ All load split tests passed!")


def test_get_benefits():
    """Test benefits generation."""
    print("Testing get_benefits...")
    
    benefits = get_benefits("Lift Weights")
    assert len(benefits) == 3, f"Expected 3 benefits, got {len(benefits)}"
    assert all(isinstance(b, str) and len(b) > 0 for b in benefits), \
        "All benefits should be non-empty strings"
    
    benefits = get_benefits("Technique Lift")
    assert len(benefits) == 3, f"Expected 3 benefits, got {len(benefits)}"
    
    benefits = get_benefits("Swim or Aqua")
    assert len(benefits) == 3, f"Expected 3 benefits, got {len(benefits)}"
    
    benefits = get_benefits("Balanced recovery")
    assert len(benefits) == 3, f"Expected 3 benefits, got {len(benefits)}"
    
    print("✓ All benefits tests passed!")


def test_get_motto():
    """Test motto generation."""
    print("Testing get_motto...")
    
    motto = get_motto("Lift Weights")
    assert isinstance(motto, str) and len(motto) > 0, "Motto should be a non-empty string"
    assert "💪" in motto, "Lift Weights motto should contain 💪"
    
    motto = get_motto("Technique Lift")
    assert isinstance(motto, str) and len(motto) > 0, "Motto should be a non-empty string"
    assert "🎯" in motto, "Technique Lift motto should contain 🎯"
    
    motto = get_motto("Swim or Aqua")
    assert isinstance(motto, str) and len(motto) > 0, "Motto should be a non-empty string"
    assert "🌊" in motto, "Swim or Aqua motto should contain 🌊"
    
    motto = get_motto("Balanced recovery")
    assert isinstance(motto, str) and len(motto) > 0, "Motto should be a non-empty string"
    assert "⚖️" in motto, "Balanced recovery motto should contain ⚖️"
    
    print("✓ All motto tests passed!")


def test_format_message():
    """Test message formatting."""
    print("Testing format_message...")
    
    mechanical, metabolic, workout_type = calculate_load_split(4, 4)
    benefits = get_benefits(workout_type)
    motto = get_motto(workout_type)
    
    message = format_message(4, 4, mechanical, metabolic, workout_type, benefits, motto)
    
    assert isinstance(message, str) and len(message) > 0, "Message should be non-empty string"
    assert "4/5" in message, "Message should contain energy level"
    assert "70% / 30%" in message, "Message should contain load split"
    assert "Lift Weights" in message, "Message should contain workout type"
    assert all(benefit in message for benefit in benefits), "Message should contain all benefits"
    assert motto in message, "Message should contain motto"
    
    print("✓ All message formatting tests passed!")


def test_complete_workflow():
    """Test complete workflow for different scenarios."""
    print("Testing complete workflow...")
    
    # Scenario 1: High energy and sleep
    mechanical, metabolic, workout_type = calculate_load_split(5, 5)
    benefits = get_benefits(workout_type)
    motto = get_motto(workout_type)
    message = format_message(5, 5, mechanical, metabolic, workout_type, benefits, motto)
    assert "70% / 30%" in message
    print("  Scenario 1 (High energy/sleep): ✓")
    
    # Scenario 2: Low energy
    mechanical, metabolic, workout_type = calculate_load_split(2, 4)
    benefits = get_benefits(workout_type)
    motto = get_motto(workout_type)
    message = format_message(2, 4, mechanical, metabolic, workout_type, benefits, motto)
    assert "40% / 60%" in message
    print("  Scenario 2 (Low energy): ✓")
    
    # Scenario 3: Low sleep
    mechanical, metabolic, workout_type = calculate_load_split(4, 2)
    benefits = get_benefits(workout_type)
    motto = get_motto(workout_type)
    message = format_message(4, 2, mechanical, metabolic, workout_type, benefits, motto)
    assert "40% / 60%" in message
    print("  Scenario 3 (Low sleep): ✓")
    
    # Scenario 4: Medium levels
    mechanical, metabolic, workout_type = calculate_load_split(3, 3)
    benefits = get_benefits(workout_type)
    motto = get_motto(workout_type)
    message = format_message(3, 3, mechanical, metabolic, workout_type, benefits, motto)
    assert "60% / 40%" in message
    print("  Scenario 4 (Medium levels): ✓")
    
    print("✓ All workflow tests passed!")


if __name__ == "__main__":
    print("=" * 50)
    print("Session Advisor Bot - Unit Tests")
    print("=" * 50)
    print()
    
    try:
        test_calculate_load_split()
        print()
        test_get_benefits()
        print()
        test_get_motto()
        print()
        test_format_message()
        print()
        test_complete_workflow()
        print()
        print("=" * 50)
        print("✓ All tests passed successfully!")
        print("=" * 50)
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error running tests: {e}")
        sys.exit(1)
