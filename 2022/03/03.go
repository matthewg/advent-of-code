package main

import (
	"fmt"
	"os"

	"github.com/golang-collections/collections/set"
	"github.com/matthewg/advent-of-code/golang/aocutils"
)

func Priority(i rune) int {
	if i >= 'a' && i <= 'z' {
		return int(i) - int('a') + 1
	} else {
		return int(i) - int('A') + 27
	}
}

type Rucksack struct {
	Comp1 *set.Set
	Comp2 *set.Set
}

func (r Rucksack) Items() *set.Set {
	return r.Comp1.Union(r.Comp2)
}

func LineToRucksack(s string) Rucksack {
	r := Rucksack{set.New(), set.New()}
	add := func(s *set.Set, b byte) {
		s.Insert(rune(b))
	}
	for i := 0; i < len(s)/2; i++ {
		add(r.Comp1, s[i])
	}
	for i := len(s) / 2; i < len(s); i++ {
		add(r.Comp2, s[i])
	}
	return r
}

func main() {
	rucksacks := aocutils.Lines(os.Args[1], LineToRucksack)

	// part 1
	sharedPrios := 0
	for i := 0; i < len(rucksacks); i++ {
		rucksack := rucksacks[i]
		shared := rucksack.Comp1.Intersection(rucksack.Comp2)
		shared.Do(func(x interface{}) {
			sharedPrios += Priority(x.(rune))
		})
	}
	fmt.Printf("per-rucksack shared item priority total: %v\n", sharedPrios)

	// part 2
	groupPrios := 0
	for i := 0; i < len(rucksacks); i += 3 {
		r1 := rucksacks[i].Items()
		r2 := rucksacks[i+1].Items()
		r3 := rucksacks[i+2].Items()
		shared := r1.Intersection(r2).Intersection(r3)
		shared.Do(func(x interface{}) {
			groupPrios += Priority(x.(rune))
		})
	}
	fmt.Printf("group-shared item priority total: %v\n", groupPrios)
}
