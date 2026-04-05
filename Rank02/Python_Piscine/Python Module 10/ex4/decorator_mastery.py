import time
import functools
from collections.abc import Callable


def spell_timer(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"- Casting {func.__name__}...")
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"- Spell completed in {end - start:.3f} seconds")
        return result
    return wrapper


def power_validator(min_power: int) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            power_val = None
            if "power" in kwargs:
                power_val = kwargs["power"]
            else:
                for arg in args:
                    if isinstance(arg, int):
                        power_val = arg
                        break

            if power_val is not None and power_val >= min_power:
                return func(*args, **kwargs)
            return "Insufficient power for this spell"
        return wrapper
    return decorator


def retry_spell(max_attempts: int) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            err = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    err = e
                    print(f"- Spell failed, retrying... "
                          f"(attempt {attempt}/{max_attempts})")
                    time.sleep(0.3)
            return f"Spell casting failed after {max_attempts} attempts\n{err}"

        return wrapper

    return decorator


class MageGuild:
    @staticmethod
    def validate_mage_name(name: str) -> bool:
        return len(name) >= 3 and name.replace(" ", "").isalpha()

    @power_validator(min_power=10)
    def cast_spell(self, spell_name: str, power: int) -> str:
        return f"Successfully cast {spell_name} with {power} power"


def main() -> None:
    # ====== SPELL TIMER ======
    print("Testing spell timer...")

    @spell_timer
    def fireball():
        time.sleep(0.3)
        return "- Result: Fireball cast!"

    print(fireball())

    # ====== RETRY SPELL ======
    print("\nTesting retrying spell...")

    @retry_spell(max_attempts=3)
    def unstable_spell():
        raise ValueError("Waaaaaaagh spelled !")

    print(unstable_spell())

    # ====== MAGE GUILD ======
    print("\nTesting MageGuild...")
    print(MageGuild.validate_mage_name("Merlin"))
    print(MageGuild.validate_mage_name("M1"))

    guild = MageGuild()
    print(guild.cast_spell("Lightning", 15))
    print(guild.cast_spell("Spark", 5))


if __name__ == "__main__":
    main()
