package main

import (
	"fmt"

	"github.com/matthewg/advent-of-code/golang/aocutils"
)

func main() {
	lines := aocutils.Lines("/etc/passwd")
	fmt.Printf("lines: %v\n", lines)
}
