package main

import (
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"

	"github.com/matthewg/advent-of-code/golang/aocutils"
)

type Range struct {
	Low, High int
}

func (r Range) Contains(x Range) bool {
	return x.Low >= r.Low && x.High <= r.High
}

func (r Range) Intersects(x Range) bool {
	// 1-2,3-4 <= no
	// 3-4,1-2 <= no
	// 1-3,3-4 <= yes
	// 3-4,1-4 <= yes
	return (x.Low >= r.Low && x.Low <= r.High) || (x.High >= r.Low && x.High <= r.High)
}

type Section struct {
	A, B Range
}

func ParseRange(s string) Range {
	nums := strings.Split(s, "-")

	low, err := strconv.Atoi(nums[0])
	if err != nil {
		log.Fatalf("Error parsing range %v low %v: %v", s, nums[0], err)
	}

	high, err := strconv.Atoi(nums[1])
	if err != nil {
		log.Fatalf("Error parsing range %v high %v: %v", s, nums[1], err)
	}

	return Range{low, high}
}
func LineToSection(s string) Section {
	elves := strings.Split(s, ",")
	return Section{
		A: ParseRange(elves[0]),
		B: ParseRange(elves[1]),
	}
}

func main() {
	sections := aocutils.Lines(os.Args[1], LineToSection)

	totalDupeCount := 0
	intersectCount := 0
	for _, section := range sections {
		if section.A.Contains(section.B) || section.B.Contains(section.A) {
			totalDupeCount++
		}
		if section.A.Intersects(section.B) || section.B.Intersects(section.A) {
			intersectCount++
		}
	}
	fmt.Printf("Sections containing total duplicates: %v\n", totalDupeCount)
	fmt.Printf("Sections containing overlap: %v\n", intersectCount)
}
