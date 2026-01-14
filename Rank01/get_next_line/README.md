*This project has been created as part of the 42 curriculum by mnassiri.*

# Get Next Line

## Description

`Get Next Line` is a programming project that challenged us to write a function capable of reading a text file (or any file descriptor) one line at a time.

The primary goal is to learn about Static Variables and how they persist in memory across function calls. Unlike normal local variables that disappear when a function ends, a static variable allows the program to remember data between reads. This project also heavily emphasizes memory management (preventing leaks w dakchi) and handling File Descriptors efficiently.

## Instructions

The project is submitted as a library of functions (`get_next_line.c`, `get_next_line_utils.c`, etc.). It is not a standalone executable, so you must compile it with your own `main.c` file to test it.

### Compilation

To compile the project, you can choose to define the `BUFFER_SIZE` macro. This determines how many bytes the function reads at a time. By default, it's set to 42.

```bash
# Example

cc -Wall -Wextra -Werror -D BUFFER_SIZE=42 main.c get_next_line.c get_next_line_utils.c
```


### Usage Example

Include the header in your C file and call the function in a loop:

```c
#include "get_next_line.h"

int main(void)
{
    int   fd = open("test.txt", O_RDONLY);
    char  *line;

    while ((line = get_next_line(fd)) != NULL)
    {
        printf("%s", line);
        free(line); // don't forget to free the line!!
    }
    close(fd);
    return (0);
}
```

## Resources
These are the resources I used to get this project done:

### Documentation & Guides:
- **Get_Next_Line Guide by mzanana:** https://github.com/mzanana/1337-Circle2/tree/main/Get_Next_Line
- **Gitbook Guide by Laendrun:** https://42-cursus.gitbook.io/guide/1-rank-01/get_next_line

### AI Usage:
- **Google Gemini:** Used it for a mockup defense to simulate evaluation questions, debug the memory leaks, and explain the theory behind some concepts.



## Algorithm Explanation & Justification

The core challenge of GNL is that `read()` returns a fixed block of bytes, but a "line" might end at byte 10, byte 50, or not exist at all in that block.

To solve this, I implemented a "stash/cut" algorithm using a single static variable.

### The Algorithm Steps:

1. **Step 1: The Read Loop**
* The function reads from the file into a temporary buffer.
* This buffer is appended to the **Static Stash** using `ft_strjoin`.
* This loop repeats only until a newline character (`\n`) is found in the stash, or if end of file is reached. This ensures we only read what is necessary. If the stash already contains a newline from a previous call, we skip reading entirely.


2. **Step 2: The Cut**
* Once the stash contains a newline, I allocate memory for a new string (`line`) containing characters from the start of the stash up to the `\n`.
* This string is returned to the user.


3. **Step 3: The Clean Up**
* The remaining part of the stash (everything *after* the `\n`) is copied into a new string.
* The old stash is freed, and the static pointer is updated to point to this new "leftover" string. This step is very important for memory management. Without cleaning the stash and freeing the old data, the program would leak memory with every call.

### Why this approach?

* **Efficiency:** It works regardless of the `BUFFER_SIZE`. A small buffer just means more loop iterations, and a large buffer means fewer.
* **Persistence:** The **Static Variable** is the only way to store the "leftover" data between function calls without using global variables (which are forbidden).
* **Scalability (Bonus part):** By converting the single static pointer into an array of pointers (`static char *stash[1024]`), this algorithm easily handles multiple file descriptors simultaneously without any conflicts.