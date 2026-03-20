#!/usr/bin/env python3


from abc import ABC, abstractmethod
from typing import Any, List, Dict, Union, Optional # noqa


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
        if isinstance(data, list):
            if len(data) > 0:
                if all(isinstance(num, (int, float)) for num in data):
                    return True
        return False

    def process(self, data: Any) -> str:
        if self.validate(data) is False:
            raise ValueError("Validation: [ERROR] Numeric Processor can only"
                             " take a LIST of numbers (INT/FLOAT).")
        vals = [a for a in data]
        total = sum(vals)
        avg = sum(vals) / len(vals)
        return f"Processed {len(vals)} numeric values, sum={total}, avg={avg}"


class TextProcessor(DataProcessor):

    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True
        return False

    def process(self, data: Any) -> str:
        if self.validate(data) is False:
            raise ValueError("Validation: [ERROR] "
                             "Text Processor takes text strings only!")
        if len(data.strip()) < 1:
            raise ValueError("Validation: [ERROR] "
                             "No text data detected (Empty string).")
        words = data.split(" ")
        return f"Processed text: {len(data)} characters, {len(words)} words"


class LogProcessor(DataProcessor):

    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True
        return False

    def process(self, data: Any) -> str:
        if self.validate(data) is False or ":" not in data:
            raise ValueError("Validation: [ERROR] Invalid log format!"
                             " [USAGE] <LOG TYPE>: <LOG MESSAGE>")

        label, msg = data.split(":")

        if label.upper() == "ERROR" and len(msg.strip()) > 0:
            flag = "[ALERT]"
        elif len(label) > 0 and len(msg.strip()) > 0:
            flag = "[INFO]"
        else:
            raise ValueError("Validation: [ERROR] Invalid log format!"
                             " [USAGE] <LOG TYPE>: <LOG MESSAGE>")

        return f"{flag} {label.upper()} level detected: {msg.strip()}"


def main():
    print("=== CODE NEXUS - DATA PROCESSOR FOUNDATION ===")

    num_proc = NumericProcessor()
    num = [1, 2, 3, 4, 5]
    print("\nInitializing Numeric Processor...")
    try:
        print(f"Processing data: {num}")
        res = num_proc.process(num)
        output = num_proc.format_output(res)
        print("Validation: Numeric data verified")
        print(output)

    except ValueError as e:
        print(e)

    txt_proc = TextProcessor()
    txt = "Hello Nexus World"
    print("\nInitializing Text Processor...")
    try:
        print(f"Processing data: \"{txt}\"")
        res = txt_proc.process(txt)
        output = txt_proc.format_output(res)
        print("Validation: Text data verified")
        print(output)

    except ValueError as e:
        print(e)

    log_proc = LogProcessor()
    log = "ERROR: Connection timeout"
    print("\nInitializing Log Processor...")
    try:
        print(f"Processing data: \"{log}\"")
        res = log_proc.process(log)
        output = log_proc.format_output(res)
        print("Validation: Log entry verified")
        print(output)

    except ValueError as e:
        print(e)

    print("\n=== Polymorphic Processing Demo ===")
    print("\nProcessing multiple data types through same interface...")

    proc = [NumericProcessor(), TextProcessor(), LogProcessor()]
    data = [num, txt, log]
    for i in range(0, 3):
        res = proc[i].process(data[i])
        print(f"Result {i+1}: {res}")

    print("\nFoundation systems online. Nexus ready for advanced streams.")


if __name__ == "__main__":
    main()
