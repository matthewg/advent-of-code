#include <stdio.h>

int main (int argc, char* argv[]) {
  unsigned long t = 366244;
  while (1) {
    t += 405859;
    if (t % 19 != 0) continue;
    if (t % 41 != 32) continue;
    if (t % 521 != 502) continue;
    if (t % 23 != 19) continue;
    if (t % 17 != 15) continue;
    if (t % 29 != 10) continue;
    if (t % 523 != 473) continue;
    if (t % 37 != 18) continue;
    if (t % 13 != 2) continue;

    /*
    t += 7;
    if (t % 13 != 12) continue;
    if (t % 59 != 55) continue;
    if (t % 31 != 25) continue;
    if (t % 19 != 12) continue;
    */
    
    printf("%lu\n", t);
    break;
  }

  return 0;
}
