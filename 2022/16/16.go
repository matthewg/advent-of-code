package main

import (
	"fmt"
	"os"
	"regexp"
	"strings"

	"github.com/albertorestifo/dijkstra"
	"github.com/matthewg/advent-of-code/golang/aocutils"
)

type Valve struct {
	Name      string
	Neighbors []string
	Flow      int
}

var ValveMap map[string]*Valve
var ValveGraph dijkstra.Graph
var FlowGraph dijkstra.Graph

var Parser = regexp.MustCompile(`Valve (..) has flow rate=(\d+); tunnels? leads? to valves? (.*)`)

func ParseValve(s string) *Valve {
	matches := Parser.FindStringSubmatch(s)
	v := Valve{
		Name:      matches[1],
		Flow:      aocutils.Atoi(matches[2]),
		Neighbors: strings.Split(matches[3], ", "),
	}
	ValveMap[v.Name] = &v
	ValveGraph[v.Name] = make(map[string]int)
	for _, n := range v.Neighbors {
		ValveGraph[v.Name][n] = 1
	}
	return &v
}

func OpenValves(pathCost, pathFlow int, path []string, pos string, openValves map[string]bool) (int, []string) {
	bestFlow := pathFlow
	path = append(path, pos)
	bestPath := path
	maxCost := 30
	for valve, cost := range FlowGraph[pos] {
		if cost+pathCost > maxCost || openValves[valve] {
			continue
		}

		newOpenValves := make(map[string]bool)
		for k, v := range openValves {
			newOpenValves[k] = v
		}
		newOpenValves[valve] = true
		newCost := pathCost
		newFlow := pathFlow
		//newFlow += ValveMap[valve].Flow
		newCost += cost
		newFlow += (maxCost - newCost) * ValveMap[valve].Flow
		newFlow, newPath := OpenValves(newCost, newFlow, path, valve, newOpenValves)
		if newFlow > bestFlow {
			bestFlow = newFlow
			bestPath = newPath
		}
	}
	return bestFlow, bestPath
}

func OpenValves2(pathCost1, pathCost2, pathFlow int, path1, path2 []string, pos1, pos2 string, openValves map[string]bool) (int, []string, []string) {
	bestFlow := pathFlow
	path1 = append(path1, pos1)
	path2 = append(path2, pos2)
	bestPath1 := path1
	bestPath2 := path2
	for valve1, cost1 := range FlowGraph[pos1] {
		if cost1+pathCost1 > 26 || openValves[valve1] {
			continue
		}
		newCost1 := pathCost1
		newCost1 += cost1

		for valve2, cost2 := range FlowGraph[pos2] {
			if cost2+pathCost2 > 30 || openValves[valve2] || valve1 == valve2 {
				continue
			}

			newOpenValves := make(map[string]bool)
			for k, v := range openValves {
				newOpenValves[k] = v
			}
			newOpenValves[valve1] = true
			newOpenValves[valve2] = true
			newCost2 := pathCost2
			newCost2 += cost2
			//fmt.Printf("H:%v@%v; E:%v@%v\n", valve1, newCost1, valve2, newCost2)
			newFlow := pathFlow
			newFlow += (30 - newCost1) * ValveMap[valve1].Flow
			newFlow += (30 - newCost2) * ValveMap[valve2].Flow
			newFlow, newPath1, newPath2 := OpenValves2(newCost1, newCost2, newFlow, path1, path2, valve1, valve2, newOpenValves)
			if newFlow > bestFlow {
				bestFlow = newFlow
				bestPath1 = newPath1
				bestPath2 = newPath2
			}
		}
	}
	return bestFlow, bestPath1, bestPath2
}

func main() {
	ValveMap = make(map[string]*Valve)
	ValveGraph = make(dijkstra.Graph)
	FlowGraph = make(dijkstra.Graph)
	valves := aocutils.Lines(os.Args[1], ParseValve)

	openValves := make(map[string]bool)
	for _, v1 := range valves {
		openValves[v1.Name] = false
		if v1.Flow == 0 && v1.Name != "AA" {
			continue
		}
		FlowGraph[v1.Name] = make(map[string]int)
		for _, v2 := range valves {
			if v2.Flow == 0 || v2.Name == v1.Name {
				continue
			}
			_, cost, _ := ValveGraph.Path(v1.Name, v2.Name)
			//fmt.Printf("Path from %v to %v @ %v: %v\n", v1.Name, v2.Name, cost, path)
			FlowGraph[v1.Name][v2.Name] = cost + 1 // Include cost of opening the valve
		}
	}

	// How many valves can we get to in 30 minutes?
	flow, path := OpenValves(0, 0, []string{}, "AA", openValves)
	fmt.Printf("Maximum flow, part 1: %v (%v)\n", flow, path)

	//flow, path1, path2 := OpenValves2(0, 0, 0, []string{}, []string{}, "AA", "AA", make(map[string]bool))
	//fmt.Printf("Maximum flow, part 2: %v (%v) + (%v)\n", flow, path1, path2)
}
