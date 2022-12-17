// valves: flow rate (gpm, int), open/closed
// ...15 valves, flow rate is small int, many 0
// ...each valve has tunnels to 1-4 other valves
// Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
// time limit is 30 minutes
// valves start closed
// start w/ elephants in AA
// takes 1 minute to open a valve, 1 minute to follow a tunnel
// trying to maximize released pressure *over time*, so multiple pressure * time remaining
// return amount of pressure released
//
// Something like ~1152921504606846976 possible paths... need to be clever about pruning.
// Maybe something like 'do not backtrack unless you have opened a valve'!
// Good start, need to get more clever...

package main

import (
	"fmt"
	"os"
	"regexp"
	"strings"

	"github.com/matthewg/advent-of-code/golang/aocutils"
)

type Valve struct {
	Name      string
	Neighbors []string
	Flow      int
}

func DLS(start *Valve, valveMap *map[string]*Valve, depthLimit int, valvesOpen map[string]bool, path []string, visitedSinceLastOpen map[string]bool) []string {
	if depthLimit <= 0 {
		return path
	}

	bestPath := path
	bestPressure := Pressure(path, valveMap)
	valve := (*valveMap)[start.Name]
	valveOpen, ok := valvesOpen[valve.Name]
	if !ok {
		valveOpen = false
	}
	if valve.Flow > 0 && !valveOpen {
		newPath := path
		newPath = append(newPath, "open")
		newOpen := make(map[string]bool)
		for k, v := range valvesOpen {
			newOpen[k] = v
		}
		newOpen[valve.Name] = true
		bestPath = newPath
		if depthLimit > 1 {
			bestPath = DLS(valve, valveMap, depthLimit-1, newOpen, newPath, make(map[string]bool))
			bestPressure = Pressure(path, valveMap)
		}

	}

	for _, n := range valve.Neighbors {
		if _, ok := visitedSinceLastOpen[n]; ok {
			continue
		}
		newPath := path
		newPath = append(newPath, n)
		newVSLO := make(map[string]bool)
		for k, v := range visitedSinceLastOpen {
			newVSLO[k] = v
		}
		newVSLO[n] = true
		newOpen := make(map[string]bool)
		for k, v := range valvesOpen {
			newOpen[k] = v
		}
		newPath = DLS((*valveMap)[n], valveMap, depthLimit-1, newOpen, newPath, newVSLO)
		if newPressure := Pressure(newPath, valveMap); newPressure > bestPressure {
			bestPressure = Pressure(newPath, valveMap)
			bestPath = newPath
		}
	}
	return bestPath
}

var PathsExplored int = 0
var Cache map[string]int = make(map[string]int)

func Pressure(path []string, valveMap *map[string]*Valve) int {
	cKey := strings.Join(path, ",")
	pressure, ok := Cache[cKey]
	if ok {
		return pressure
	}
	PathsExplored++
	if PathsExplored%1000 == 0 {
		fmt.Printf("Explored paths: %v\n", PathsExplored)
	}

	pressure = 0
	gpm := 0
	current := "AA"
	//fmt.Printf("Calculating pressure of %v-path: %v\n", len(path), path)
	for _, step := range path {
		pressure += gpm
		//fmt.Printf("Existing valves release another %v; total released is %v\n", gpm, pressure)
		if step == "open" {
			gpm += (*valveMap)[current].Flow
			//fmt.Printf("After opening %v, new gpm is %v: %v\n", current, gpm, (*valveMap)[current])
		} else {
			current = step
		}
	}
	Cache[cKey] = pressure
	return pressure
}

func IDDFS(start *Valve, valveMap *map[string]*Valve) int {
	valvesOpen := make(map[string]bool)
	path := DLS(start, valveMap, 30, valvesOpen, []string{}, make(map[string]bool))
	fmt.Printf("Best path: %v\n", path)
	return Pressure(path, valveMap)
}

var Parser = regexp.MustCompile(`Valve (..) has flow rate=(\d+); tunnels? leads? to valves? (.*)`)

func ParseValve(s string) Valve {
	matches := Parser.FindStringSubmatch(s)
	return Valve{
		Name:      matches[1],
		Flow:      aocutils.Atoi(matches[2]),
		Neighbors: strings.Split(matches[3], ", "),
	}
}

func main() {
	valves := aocutils.Lines(os.Args[1], ParseValve)
	valveMap := make(map[string]*Valve)
	for i := range valves {
		valve := &valves[i]
		fmt.Printf("Valve: %v\n", *valve)
		valveMap[valve.Name] = valve
	}
	fmt.Printf("Best pressure: %v\n", IDDFS(valveMap["AA"], &valveMap))
}
