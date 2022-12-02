package main

import (
	"fmt"
	"log"
	"os"
	"sort"
	"strconv"
	"strings"

	"github.com/matthewg/advent-of-code/golang/aocutils"
)

type Calories int
type Food struct {
	C Calories
}
type Elf struct {
	F []Food
	C Calories
}

type ByCalories []Elf

func (a ByCalories) Len() int           { return len(a) }
func (a ByCalories) Swap(i, j int)      { a[i], a[j] = a[j], a[i] }
func (a ByCalories) Less(i, j int) bool { return a[i].C > a[j].C }

func ParseElf(s string) Elf {
	fs := strings.Split(s, "\n")
	var e Elf
	ef := &e.F
	for i := 0; i < len(fs); i++ {
		if fs[i] == "" {
			continue
		}
		c, err := strconv.Atoi(fs[i])
		if err != nil {
			log.Fatalf("Error converting calorie count to string: %v -> %v", fs[i], err)
		}
		cCal := Calories(c)
		(*ef) = append(*ef, Food{cCal})
		e.C += cCal
	}
	return e
}

func main() {
	var elves []Elf
	elves = aocutils.Records(os.Args[1], "\n\n", ParseElf)
	sort.Sort(ByCalories(elves))
	//fmt.Printf("Elves: +%v\n", elves)
	fmt.Printf("Calories for foodiest elf: %v\n", elves[0].C)
	fmt.Printf("Calories for foodiest elves: %v\n", elves[0].C+elves[1].C+elves[2].C)
}
