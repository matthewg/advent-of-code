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

func main() {
	lines := aocutils.Lines(os.Args[1], ParseRock)
	occupied := make(map[Pos]bool)

	maxRockY := 0
	for _, l := range lines {
		for _, line := range l {
			for _, lp := range line.AllPos() {
				occupied[lp] = true
				if lp.Y > maxRockY {
					maxRockY = lp.Y
				}
			}
		}
	}

	sandRested := 0
	for {
		sandCanRest := false
		for sand := (Pos{X: 500, Y: 0}); sand.Y <= maxRockY; sand.Y++ {
			next := Pos{X: sand.X, Y: sand.Y + 1}
			if occupied[next] {
				next = Pos{X: sand.X - 1, Y: sand.Y + 1}
				if occupied[next] {
					next = Pos{X: sand.X + 1, Y: sand.Y + 1}
					if occupied[next] {
						sandRested++
						sandCanRest = true
						break
					}
				}
			}
		}
		if !sandCanRest {
			break
		}
	}
	fmt.Printf("Sand grains rested: %v\n", sandRested)
}
