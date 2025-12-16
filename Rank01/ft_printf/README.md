*This project has been created as part of the 42 curriculum by mnassiri.*

# ft_printf

## Description
`ft_printf` is a custom implementation of the standard C library function `printf`. The goal of this project is to understand the mechanisms of variadic functions in C, specifically how to get variable arguments and format them for output.

This library mimics the behavior of the original `printf` for a specific set of format specifiers (`%c`, `%s`, `%p`, `%d`, `%i`, `%u`, `%x`, `%X`, `%%`). Unlike the standard version, this implementation only covers the "Mandatory" part of the project, meaning it does not manage an internal buffer but writes directly to the standard output.

## Instructions

### Compilation
The project includes a `Makefile` that compiles the library into a static archive named `libftprintf.a`.

* **Compile the library:**
    ```bash
    make
    ```
* **Force recompile:**
    ```bash
    make re
    ```
* **Clean object files:**
    ```bash
    make clean
    ```
* **Clean everything (objects + library):**
    ```bash
    make fclean
    ```

### Usage
To use `ft_printf` in your own project:

1.  Include the header file in your source code:
    ```c
    #include "ft_printf.h"
    ```
2.  Compile your project and link the library:
    ```bash
    cc main.c libftprintf.a
    ```
## Resources
These are the resources I used to get this project done:

### Youtube Videos:
- "Let's build a mini printf function" by Oceano.
- "understanding ft\_printf" by nikito.
- "variadict functions in c (ft\_printf PART 00)" by MyCodeUrCode.

### AI Usage:
- Used Google Gemini's Guided Reading functionality to learn and test my knowledge on the project.
- Used Google Gemini to help structure and format the README into a legible markdown format.
