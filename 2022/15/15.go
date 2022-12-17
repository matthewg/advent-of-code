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

func NoBeaconSpots(readings []Reading, y, xMin, xMax int, invert bool) map[Pos]bool {
	spots := make(map[Pos]bool)
	for x := xMin; x <= xMax; x++ {
		p := Pos{X: x, Y: y}
		spotCanHaveBeacon := true
		for _, r := range readings {
			if Manhattan(p, r.Sensor) <= r.Distance && p != r.Beacon {
				//fmt.Printf("Could not have beacon at %v, thanks to sensor at %v/%v/%v\n", p, r.Sensor, r.Beacon, r.Distance)
				spotCanHaveBeacon = false
				if !invert {
					spots[p] = true
					break
				}
			} else if invert && p == r.Beacon {
				spotCanHaveBeacon = false
			}
		}
		if invert && spotCanHaveBeacon {
			//fmt.Printf("Could have beacon at %v\n", p)
			spots[p] = true
		}
	}
	return spots
}

func SpotMap(readings *[]Reading) *map[int]map[int]bool {
	ret := make(map[int]map[int]bool)
	for _, r := range *readings {
		for y := r.Sensor.Y - r.Distance; y <= r.Sensor.Y+r.Distance; y++ {
			row, ok := ret[y]
			if !ok {
				row = make(map[int]bool)
				ret[y] = row
			}
			for x := r.Sensor.X - r.Distance; x <= r.Sensor.X+r.Distance; x++ {
				if _, ok := row[x]; !ok {
					row[x] = true
				}
			}
		}
		ret[r.Beacon.Y][r.Beacon.X] = false
	}
	for _, v := range ret {
		for k2, v2 := range v {
			if !v2 {
				delete(v, k2)
			}
		}
	}
	return &ret
}

type RowChocker struct {
	X, RMinusDY int
	Beacon      *int
}

func (r Reading) Chocker(row int) RowChocker {
	beacon := &r.Beacon.X
	if row != r.Beacon.Y {
		beacon = nil
	}
	return RowChocker{
		X:        r.Sensor.X,
		RMinusDY: r.Distance - aocutils.Abs(row-r.Sensor.Y),
		Beacon:   beacon,
	}
}
func (r RowChocker) InCircleNoBeacon(x int) bool {
	/*if r.Beacon != nil && x == *r.Beacon {
		return false
	}*/
	return aocutils.Abs(x-r.X) <= r.RMinusDY
}

func CheckRow(readings *[]Reading, row, xMin, xMax int) []int {
	chockers := []RowChocker{}
	for _, r := range *readings {
		chockers = append(chockers, r.Chocker(row))
	}
	noBeacon := []int{}
	for x := xMin; x < xMax; x++ {
		inCircleNoBeacon := false
		for _, c := range chockers {
			if c.InCircleNoBeacon(x) {
				inCircleNoBeacon = true
				break
			}
		}
		if !inCircleNoBeacon {
			noBeacon = append(noBeacon, x)
			if len(noBeacon) > 1 {
				return noBeacon
			}
		}
	}
	return noBeacon
}

func main() {
	// Each sensor has a radius, and all points in that radius save one don't have a beacon
	// Part 1: Find number of x in a given row not within any circle
	// Part 2: Find row which has only one x not within any circle
	// Some circles have radius > 1M so we can't check all points
	// So, need O(1) lookup for "find all x not within a circle on a given y"
	// (x, y) is in circle of distance < r
	// d = abs(x1-x2)+abs(y1-y2)
	// abs(x1-x2) = d-abs(y1-y2)

	fmt.Printf("== Example ==\n")
	readings := aocutils.Lines("input.txt", ParseReading)
	//noSpots := CheckRow(&readings, 10, -4, 26)
	//fmt.Printf("Number of spots with no beacon: %v\n", len(noSpots))
	for y := 0; y < 4000000; y++ {
		if y%100 == 0 {
			fmt.Printf("Checking row %v\n", y)
		}
		noSpots := CheckRow(&readings, y, 0, 4000000)
		//fmt.Printf("%v => %v\n", y, len(noSpots))
		if len(noSpots) == 1 {
			t := noSpots[0]*4000000 + y
			fmt.Printf("Coord %v, %v has tuning frequency %v\n", noSpots[0], y, t)
			break
		}
	}

	/*
		spotMap := SpotMap(&readings)
		row := 2000000
		fmt.Printf("At row %v, spots with confirmed no beacon: %v\n", row, len((*spotMap)[row]))

		xMin := 0
		xMax := 4000000
		for checkRow := 0; checkRow <= xMax; checkRow++ {
			maybeBeaconSpots := 0
			maybeBeaconX := 0
			row := (*spotMap)[checkRow]
			for x := xMin; x <= xMax; x++ {
				if _, ok := row[x]; !ok {
					maybeBeaconSpots++
					maybeBeaconX = x
				}
				if maybeBeaconSpots > 1 {
					break
				}
			}
			//fmt.Printf("Row %v has %v maybeBeaconSpots\n", checkRow, maybeBeaconSpots)
			if maybeBeaconSpots == 1 {
				t := maybeBeaconX*4000000 + checkRow
				fmt.Printf("Coord %v, %v has tuning frequency %v\n", maybeBeaconX, checkRow, t)
				break
			}
		}
	*/

	/*
		fmt.Printf("=== Input ===\n")
		readings = aocutils.Lines("input.txt", ParseReading)
		row = 2000000
		xMin = -9999999
		xMax = 9999999
		//spots = NoBeaconSpots(readings, row, xMin, xMax, false)
		//fmt.Printf("At row %v, spots with confirmed no beacon: %v\n", row, len(spots))

		xMin = 0
		xMax = 4000000
		xToReadings := make(map[int][]Reading)
		for x := xMin; x <= xMax; x++ {
			rs := []Reading{}
			for _, r := range readings {
				p := Pos{X: x, Y: r.Beacon.Y}
				if Manhattan(p, r.Sensor) <= r.Distance || p == r.Beacon {
					rs = append(rs, r)
				}
			}
			xToReadings[x] = rs
		}
		for checkRow := 0; checkRow <= xMax; checkRow++ {
			if checkRow%100 == 0 {
				fmt.Printf("Checking row %v\n", checkRow)
			}
			spots := make(map[Pos]bool)
			for x := xMin; x <= xMax; x++ {
				p := Pos{X: x, Y: checkRow}
				spotCanHaveBeacon := true
				rs, ok := xToReadings[x]
				if ok {
					for _, r := range rs {
						if Manhattan(p, r.Sensor) <= r.Distance && p != r.Beacon {
							//fmt.Printf("Could not have beacon at %v, thanks to sensor at %v/%v/%v\n", p, r.Sensor, r.Beacon, r.Distance)
							spotCanHaveBeacon = false
							break
						} else if p == r.Beacon {
							spotCanHaveBeacon = false
							break
						}
					}
				}
				if spotCanHaveBeacon {
					spots[p] = true
					if len(spots) > 1 {
						break
					}
				}
			}
			if len(spots) == 1 {
				for p, _ := range spots {
					t := p.X*4000000 + p.Y
					fmt.Printf("Coord %v has tuning frequency %v\n", p, t)
					return
				}
			}
		}
	*/
}
