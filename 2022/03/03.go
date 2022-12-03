package main

import (
	"fmt"
	"os"

	"github.com/matthewg/advent-of-code/golang/aocutils"
)

func Priority(i rune) int {
	if i >= 'a' && i <= 'z' {
		return int(i) - int('a') + 1
	} else {
		return int(i) - int('A') + 27
	}
}

type Empty struct{}
type Rucksack struct {
	Comp1  []rune
	Comp2  []rune
	Shared map[rune]Empty
}

func LineToRucksack(s string) Rucksack {
	var r Rucksack
	r.Shared = make(map[rune]Empty)
	c1 := make(map[rune]Empty)
	for i := 0; i < len(s)/2; i++ {
		x := rune(s[i])
		r.Comp1 = append(r.Comp1, x)
		c1[x] = Empty{}
	}
	for i := len(s) / 2; i < len(s); i++ {
		x := rune(s[i])
		r.Comp2 = append(r.Comp2, x)
		if _, ok := c1[x]; ok {
			r.Shared[x] = Empty{}
		}
	}
	return r
}

func main() {
	rucksacks := aocutils.Lines(os.Args[1], LineToRucksack)
	sharedPrios := 0
	for i := 0; i < len(rucksacks); i++ {
		rucksack := rucksacks[i]
		for x := range rucksack.Shared {
			sharedPrios += Priority(x)
		}
	}
	fmt.Printf("priority total: %v\n", sharedPrios)
}
