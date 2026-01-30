*This project has been created as part of the 42 curriculum by mnassiri.*

# Push_swap

## Description

`Push_swap` is a purely algorithmic project that challenges us to sort a set of integers using two stacks (Stack A and Stack B) and a limited set of instructions.

The primary goal is to learn about complexity and sorting algorithms. Unlike standard sorting (like Bubble Sort) where you swap values in an array, here you must manipulate the memory structure itself using strict operations like `push`, `swap`, and `rotate`. The challenge is not just to sort, but to do it with the absolute minimum number of operations to pass strict benchmarks (which I won't lol).

## Instructions

The project includes a `Makefile` that compiles the source files (including the parsing, stack management, and sorting algorithm) into a program named `push_swap`.

### Compilation

To compile the project, simply run `make` at the root of the repository.

```bash
make
```

### Usage Example

Run the program with a list of integers as arguments. It will output the list of operations required to sort them.

```bash
# Example
./push_swap 2 1 3 6 5 8

# Output:
# sa
# pb
# pb
# ...
```

You can also run it with a single string argument:

```bash
./push_swap "2 1 3 6 5 8"
```

To verify the sorting, you can pipe the output into the provided checker:

```bash
ARG="4 67 3 87 23"; ./push_swap $ARG | ./checker_OS $ARG
# Should print "OK" I hope...
```

## Resources

These are the resources I used to get this project done:

### Youtube Videos & Guides:

* **Radix Sort Algorithm Introduction in 5 Minutes:** https://www.youtube.com/watch?v=XiuSW_mEn7g
* **Gitbook Guide by Laendrun** https://42-cursus.gitbook.io/guide/1-rank-01/get_next_line

### AI Usage:

- Used Google Gemini's Guided Reading functionality to simulate the evaluation defense, and break down the bitwise logic required for Radix Sort.
- Used Google Gemini to help structure and format the README into a legible markdown format.


## Algorithm Explanation & Justification

While algorithms like **Turk** or **Chunks** seem to be the most efficient to fully complete this project with bonuses, I instead went for **Radix**. It's not the best, but it gets the job done and is relatively easier to implement in code.

### The Algorithm Steps:

**Step 1: Indexing**

* Radix sort relies on bitwise operations, which work best on a continuous range of positive integers.
* I assign a "Rank" (index) to every number in the stack based on its value. The smallest number gets `index 0`, the next `index 1`, and so on.
* This simplifies the problem: no matter if the input is `{-1000, 2, 50}` or `{0, 1, 2}`, the algorithm treats them exactly the same.

**Step 2: Bitwise Radix Sort**

* I sort the numbers by processing their binary representation bit by bit, from the Least Significant Bit (LSB) to the Most Significant Bit (MSB).
* **The Loop:** For each bit position `i`:
* I iterate through the entire Stack A.
* If the number's index has a `0` at bit `i`, I push it to Stack B (`pb`).
* If it has a `1`, I rotate Stack A (`ra`) to keep it there.


* After checking all numbers, I push everything back from B to A (`pa`).
* This process repeats until the most significant bit is processed.

**Step 3: Tiny Sorts (Hardcoded)**

* Radix sort is overkill for very small lists (3-5 numbers).
* For these cases, I hardcoded a simple logic (finding the min/max and rotating) to ensure I pass the strict "maximum 12 operations" limit for 5 numbers.

---