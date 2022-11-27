package main

import (
	"fmt"
	"os"
	"strconv"

	"github.com/matthewg/advent-of-code/golang/aocutils"
)

func strConv(str string) int {
	ret, _ := strconv.Atoi(str)
	return ret
}

func main() {
	depths := aocutils.Lines(os.Args[1], strConv)

	prev := depths[0]
	increases := 0
	for i := 0; i < len(depths); i++ {
		depth := depths[i]
		if depth > prev {
			increases++
		}
		prev = depth
	}
	fmt.Printf("increases: %v\n", increases)
}
