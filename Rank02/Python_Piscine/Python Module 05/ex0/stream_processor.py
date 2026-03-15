#!/usr/bin/env python3

from abc import ABC, abstractmethod
from typing import Any, List, Dict, Union, Optional


class DataProcessor(ABC):

    @abstractmethod
    def process(self, data: Any) -> str:
        pass

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    def format_output(self, result: str) -> str:
        return f"Output: {result}"


class NumericProcessor(DataProcessor):

    def validate(self, data: Any) -> bool:
        if isinstance(data, list) and len(data) > 0 and all(isinstance(x, (int, float)) for x in data):
            return True
        return False

    def process(self, data: Any) -> str:
        if not self.validate(data):
            raise ValueError("[ERROR] Numeric Processing requires a list of numbers.")
        avg = sum(data) / len(data)
        return f"Processed {len(data)} numeric values, sum={sum(data)}, avg={avg:.1f}"


class TextProcessor(DataProcessor):

    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True
        return False

    def process(self, data: Any) -> str:
        if not self.validate(data):
            raise ValueError("[ERROR] Text Processing requires a text string.")
        words = data.split()
        return f"Processed text: {len(data)} characters, {len(words)} words"


class LogProcessor(DataProcessor):

    def validate(self, data: Any) -> bool:
        if isinstance(data, str) and ":" in data:
            return True
        return False

    def process(self, data: Any) -> str:
        if not self.validate(data):
            raise ValueError("[ERROR] Invalid log format.")
        level, msg = data.split(":", 1)
        level = level.strip().upper()
        msg = msg.strip()
        if level in ["ERROR", "ALERT"]:
            flag = "ALERT"
        else:
            flag = "INFO"
        return f"[{flag}] {level} level detected: {msg}"


def main():
    print("=== CODE NEXUS - DATA PROCESSOR FOUNDATION ===")

    # NUMERIC PROCESSING
    print("\nInitializing Numeric Processor...")
    num_proc = NumericProcessor()
    num = [1, 2, 3, 4, 5]
    print(f"Processing data: {num}")
    try:
        if num_proc.validate(num):
            print("Validation: Numeric data verified")
            result = num_proc.process(num)
            output = num_proc.format_output(result)
            print(output)
        else:
            num_proc.process(num)
    except ValueError as e:
        print(f"Validation: {e}")

    # TEXT PROCESSING
    print("\nInitializing Text Processor...")
    txt_proc = TextProcessor()
    txt = "Hello Nexus World"
    print(f"Processing data: \"{txt}\"")
    try:
        if txt_proc.validate(txt):
            print("Validation: Text data verified")
            result = txt_proc.process(txt)
            output = txt_proc.format_output(result)
            print(result)
        else:
            txt_proc.process(txt)
    except ValueError as e:
        print(f"Validation: {e}")

    # LOG PROCESSING
    print("\nInitializing Log Processor...")
    log_proc = LogProcessor()
    log = "ERROR: Connection timeout"
    print(f"Processing data: \"{log}\"")
    try:
        if log_proc.validate(log):
            print("Validation: Log entry verified")
            result = log_proc.process(log)
            output = log_proc.format_output(result)
            print(result)
        else:
            log_proc.process(log)
    except ValueError as e:
        print(f"Validation: {e}")

    # POLYMORPHIC PROCESSING
    print("\n=== Polymorphic Processing Demo ===\n")
    print("Processing multiple data types through same interface...")
    processors = [NumericProcessor(), TextProcessor(), LogProcessor()]
    all_data = [[1, 2, 3], "Hello world!", "INFO: System ready"]
    for i in range(3):
        proc = processors[i]
        data = all_data[i]
        result = proc.process(data)
        print(f"Ressult {i+1}: {result}")
    
    print("\nFoundation systems online. Nexus ready for advanced streams.")


if __name__ == "__main__":
    main()
