#include "get_next_line.h"

int main(void) {
  int fd;
  char *line;
  int lines_read;

  lines_read = 0;

  // 1. Open a file to read from
  fd = open("test.txt", O_RDONLY);
  if (fd == -1) {
    printf("Error opening file\n");
    return (1);
  }

  printf("---------- STARTING READ LOOP ----------\n");

  // 2. The Loop: Call GNL until it returns NULL
  while (1) {
    line = get_next_line(fd);

    if (line == NULL) // If NULL, we reached EOF (or error)
      break;

    lines_read++;
    printf("Line %d: %s", lines_read, line);

    free(line); // IMPORTANT: You must free the line GNL gives you!
  }

  printf("\n---------- END OF FILE ----------\n");

  // 3. Clean up
  close(fd);
  return (0);
}