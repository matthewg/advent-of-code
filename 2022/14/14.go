package main

import (
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"

	"github.com/matthewg/advent-of-code/golang/aocutils"
)

type Pos struct {
	X, Y int
}
type RockLine struct {
	Start, End Pos
}

func (l RockLine) AllPos() []Pos {
	ret := []Pos{}
	x := l.Start.X
	y := l.Start.Y

	x2 := l.End.X
	y2 := l.End.Y

	if x > x2 {
		x, x2 = x2, x
	} else if y > y2 {
		y, y2 = y2, y
	}

	if x == x2 {
		for ; y <= y2; y++ {
			ret = append(ret, Pos{X: x, Y: y})
		}
	} else if y == y2 {
		for ; x <= x2; x++ {
			ret = append(ret, Pos{X: x, Y: y})
		}
	} else {
		log.Fatalf("Should be a straight line!")
	}
	return ret
}

func ParsePos(s string) Pos {
	toks := strings.Split(s, ",")
	x, _ := strconv.Atoi(toks[0])
	y, _ := strconv.Atoi(toks[1])
	return Pos{X: x, Y: y}
}

func ParseRock(s string) []RockLine {
	pss := strings.Split(s, " -> ")
	prev := ParsePos(pss[0])
	ret := []RockLine{}
	for i := 1; i < len(pss); i++ {
		pos := ParsePos(pss[i])
		ret = append(ret, RockLine{Start: prev, End: pos})
		prev = pos
	}
	return ret
}

func ReleaseSand(rockuppied map[Pos]bool, maxRockY int, useFloor bool) int {
	occupied := make(map[Pos]bool)
	for k, v := range rockuppied {
		occupied[k] = v
	}

	floor := maxRockY + 2
	isOccupied := func(p Pos) bool {
		return occupied[p] || (useFloor && p.Y >= floor)
	}
	if useFloor {
		maxRockY += 2
	}

	minX := 0
	maxX := 500

	sandRested := 0
	origin := Pos{X: 500, Y: 0}
	for {
		sandCanRest := false
		//fmt.Printf("Releasing sand grain %v...\n", sandRested)
		for sand := origin; sand.Y <= maxRockY && !isOccupied(origin); {
			//fmt.Printf("  Sand is at %v\n", sand)
			next := Pos{X: sand.X, Y: sand.Y + 1}
			if isOccupied(next) {
				next = Pos{X: sand.X - 1, Y: sand.Y + 1}
				if isOccupied(next) {
					next = Pos{X: sand.X + 1, Y: sand.Y + 1}
					if isOccupied(next) {
						occupied[sand] = true
						if sand.X > maxX {
							maxX = sand.X
						}
						if sand.X < minX {
							minX = sand.X
						}
						sandRested++
						sandCanRest = true
						break
					}
				}
			}
			sand = next
		}
		if !sandCanRest {
			break
		}
	}

	for y := 0; y <= maxRockY; y++ {
		for x := minX; x <= maxX; x++ {
			p := Pos{X: x, Y: y}
			if rockuppied[p] || (useFloor && y == maxRockY) {
				fmt.Printf("#")
			} else if occupied[p] {
				fmt.Printf("o")
			} else {
				fmt.Printf(" ")
			}
		}
		fmt.Printf("\n")
	}
	return sandRested
}

func main() {
	lines := aocutils.Lines(os.Args[1], ParseRock)
	occupied1 := make(map[Pos]bool)
	occupied2 := make(map[Pos]bool)

	fmt.Printf("Marking rocks\n")
	maxRockY := 0
	for _, l := range lines {
		for _, line := range l {
			for _, lp := range line.AllPos() {
				occupied1[lp] = true
				occupied2[lp] = true
				if lp.Y > maxRockY {
					maxRockY = lp.Y
				}
			}
		}
	}

	// Part 1
	sandRested := ReleaseSand(occupied1, maxRockY, false)
	fmt.Printf("Sand grains rested, part 1: %v\n", sandRested)

	// Part 2
	sandRested = ReleaseSand(occupied2, maxRockY, true)
	fmt.Printf("Sand grains rested, part 2: %v\n", sandRested)
}
