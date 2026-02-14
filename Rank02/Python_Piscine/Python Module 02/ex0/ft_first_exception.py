#!/usr/bin/env python3

def check_temperature(temp_str: str) -> None:
    try:
        temp = int(temp_str)
        if 0 <= temp <= 40:
            print(f"Temperature {temp}°C is perfect for plants!\n")
        elif temp < 0:
            print(f"Error: {temp}°C is too cold for plants (min 0°C)\n")
        else:
            print(f"Error: {temp}°C is too hot for plants (max 40°C)\n")
            
    except ValueError:
        print(f"Error: '{temp_str}' is not a valid number\n")

def test_temperature_input() -> None:
    print("=== Garden Temperature Checker ===\n")
    
    print(f"Testing temperature: 25")
    check_temperature("25")
    
    print(f"Testing temperature: abc")
    check_temperature("abc")
    
    print(f"Testing temperature: 100")
    check_temperature("100")
    
    print(f"Testing temperature: -50")
    check_temperature("-50")
    
    print("All tests completed - program didn't crash!")

if __name__ == "__main__":
    test_temperature_input()