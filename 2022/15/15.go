package main

import (
	"fmt"
	"os"
	"regexp"

	"github.com/matthewg/advent-of-code/golang/aocutils"
)

type Pos struct {
	X, Y int
}

type Reading struct {
	Sensor, Beacon Pos
	Distance       int
}

func Manhattan(a, b Pos) int {
	return aocutils.Abs(a.X-b.X) + aocutils.Abs(a.Y-b.Y)
}

func ManhattanArea(i int) int {
	area := 2*i + 1
	for n := area - 2; area > 0; area -= 2 {
		area += 2 * n
	}
	return area
}

var Parser = regexp.MustCompile(`Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)`)

func ParseReading(s string) Reading {
	matches := Parser.FindStringSubmatch(s)
	sensor := Pos{
		X: aocutils.Atoi(matches[1]),
		Y: aocutils.Atoi(matches[2]),
	}
	beacon := Pos{
		X: aocutils.Atoi(matches[3]),
		Y: aocutils.Atoi(matches[4]),
	}
	return Reading{
		Sensor:   sensor,
		Beacon:   beacon,
		Distance: Manhattan(sensor, beacon),
	}
}

func main() {
	readings := aocutils.Lines(os.Args[1], ParseReading)

	// Part 1
	spots := map[int]map[Pos]bool{
		10: make(map[Pos]bool),
		//2000000: make(map[Pos]bool),
	}
	for _, r := range readings {
		for checkRow := range spots {
			checkXMin := r.Sensor.X - r.Distance
			checkXMax := r.Sensor.X + r.Distance
			for x := checkXMin; x <= checkXMax; x++ {
				p := Pos{X: x, Y: checkRow}
				if Manhattan(p, r.Sensor) > r.Distance || r.Beacon == p {
					continue
				}
				spots[checkRow][p] = true
			}
		}
	}
	for k, v := range spots {
		fmt.Printf("At row %v, spots with confirmed no beacon: %v\n", k, len(v))
	}

	// Part 2
	for _, r := range readings {
		for checkRow := 0; checkRow <= 20; checkRow++ {
			ss := make(map[Pos]bool)
			// numTrue := 0

			checkXMin := r.Sensor.X - r.Distance
			checkXMax := r.Sensor.X + r.Distance
			for x := aocutils.Max(checkXMin, 0); x <= aocutils.Min(checkXMax, 20); x++ {
				p := Pos{X: x, Y: checkRow}
				if Manhattan(p, r.Sensor) <= r.Distance || r.Beacon == p || r.Sensor == p {
					ss[p] = false
					//} else if _, ok := ss[p]; !ok {
					//	ss[p] = true
				}
			}
			/*
				if numTrue == len(ss) {
					continue
				}
			*/
			fmt.Printf("\n== Row %v ==\n", checkRow)
			for k, v := range ss {
				fmt.Printf("- %v: %v\n", k, v)
				if v {
					continue
				}
				/*
					t := k.X*4000000 + k.Y
					fmt.Printf("Coord %v has tuning frequency %v\n", k, t)
					return
				*/
			}
		}
	}
}
