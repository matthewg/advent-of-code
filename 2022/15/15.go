package main

import (
	"fmt"
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

func NoBeaconSpots(readings []Reading, y int) map[Pos]bool {
	spots := make(map[Pos]bool)
	for _, r := range readings {
		checkXMin := r.Sensor.X - r.Distance
		checkXMax := r.Sensor.X + r.Distance
		for x := checkXMin; x <= checkXMax; x++ {
			p := Pos{X: x, Y: y}
			if Manhattan(p, r.Sensor) > r.Distance || r.Beacon == p {
				continue
			}
			spots[p] = true
		}
	}
	return spots
}

func main() {
	fmt.Printf("== Example ==\n")
	readings := aocutils.Lines("example.txt", ParseReading)
	spots := NoBeaconSpots(readings, 10)
	fmt.Printf("At row %v, spots with confirmed no beacon: %v\n", 10, len(spots))

	for checkRow := 0; checkRow <= 20; checkRow++ {
		spots = NoBeaconSpots(readings, checkRow)
		fmt.Printf("At row %v, spots with confirmed no beacon: %v\n", checkRow, len(spots))
		/*
			rangeSpots := make(map[Pos]bool)
			for p := range spots {
				if p.X >= 0 && p.X <= 20 {
					rangeSpots[p] = true
				}
			}
			if len(rangeSpots) == 1 {
				for p := range rangeSpots {
					t := p.X*4000000 + p.Y
					fmt.Printf("Coord %v has tuning frequency %v\n", p, t)
				}
			}
		*/
	}
}
