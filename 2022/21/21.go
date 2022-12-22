package main

import (
	"fmt"
	"log"
	"os"
	"strings"

	"github.com/matthewg/advent-of-code/golang/aocutils"
)

type Monkey struct {
	Name          string
	Predecessors  []string
	Successors    []string
	Operation     string
	Value         *int64
	HumnPoly      []float64
	DependsOnHumn bool
}

func ParseMonkey(s string) Monkey {
	toks := strings.Split(s, " ")
	name := toks[0][0:4]

	if len(toks) == 2 {
		i := int64(aocutils.Atoi(toks[1]))
		dependsOnHumn := false
		humnPoly := []float64{float64(i)}
		if name == "humn" {
			dependsOnHumn = true
			humnPoly = []float64{0.0, 1.0} // 1x + 0
			i = 3665520865940
		}
		return Monkey{
			Name:          name,
			Predecessors:  []string{},
			Successors:    []string{},
			Operation:     "",
			Value:         &i,
			HumnPoly:      humnPoly,
			DependsOnHumn: dependsOnHumn,
		}
	} else {
		return Monkey{
			Name:          name,
			Predecessors:  []string{toks[1], toks[3]},
			Successors:    []string{},
			Operation:     toks[2],
			Value:         nil,
			HumnPoly:      []float64{},
			DependsOnHumn: false,
		}
	}
}

func (m *Monkey) Coeff(i int) float64 {
	if i < len(m.HumnPoly) {
		return m.HumnPoly[i]
	}
	return 0.0
}

var MonkeyMap map[string]*Monkey

func (m *Monkey) Calculate() int64 {
	if m.Value == nil {
		m1 := MonkeyMap[m.Predecessors[0]]
		m2 := MonkeyMap[m.Predecessors[1]]
		v1 := m1.Calculate()
		v2 := m2.Calculate()
		var v int64
		switch m.Operation {
		case "+":
			v = v1 + v2
		case "-":
			v = v1 - v2
		case "*":
			v = v1 * v2
		case "/":
			v = v1 / v2
		default:
			log.Fatalf("Unknown operation '%v'", m.Operation)
		}
		m.Value = &v

		if m1.DependsOnHumn || m2.DependsOnHumn {
			m.DependsOnHumn = true

			degree := len(m1.HumnPoly)
			if len(m2.HumnPoly) > degree {
				degree = len(m2.HumnPoly)
			}
			switch m.Operation {
			case "+": // (ax + b) + (cx + d) = (b+d)x + (a+c)
				for i := 0; i < degree; i++ {
					c1 := m1.Coeff(i)
					c2 := m2.Coeff(i)
					m.HumnPoly = append(m.HumnPoly, c1+c2)
				}
			case "-": // (ax + b) - (cx + d) = (b-d)x + (a-c)
				for i := 0; i < degree; i++ {
					c1 := m1.Coeff(i)
					c2 := m2.Coeff(i)
					m.HumnPoly = append(m.HumnPoly, c1-c2)
				}
			case "*": // Multiply each pair of terms (FOIL generalized)
				for i := 0; i < degree; i++ {
					c1 := m1.Coeff(i)
					if c1 == 0 {
						continue
					}
					for j := 0; j < degree; j++ {
						c2 := m2.Coeff(j)
						if c2 == 0 {
							continue
						}
						xcount := i + j
						for k := len(m.HumnPoly); k <= xcount; k++ {
							m.HumnPoly = append(m.HumnPoly, 0.0)
						}
						fmt.Printf("Mult: i=%v, j=%v, xcount=%v; %v * %v = %v\n", i, j, xcount, c1, c2, c1*c2)
						m.HumnPoly[xcount] += c1 * c2
					}
				}
			case "/": // Adapted from https://en.wikipedia.org/wiki/Synthetic_division#Python_implementation
				if len(m1.HumnPoly) == 1 && len(m2.HumnPoly) == 1 {
					m.HumnPoly = []float64{m1.HumnPoly[0] / m2.HumnPoly[0]}
				} else if len(m2.HumnPoly) == 1 {
					m.HumnPoly = []float64{}
					for _, c := range m1.HumnPoly {
						m.HumnPoly = append(m.HumnPoly, c/m2.HumnPoly[0])
					}
				} else {
					log.Fatalf("wargarbl divide: %v / %v", m1.HumnPoly, m2.HumnPoly)
				}
			default:
				log.Fatalf("Unknown operation '%v'", m.Operation)
			}
			fmt.Printf("\nhumn poly calc:\n  %v\n%v\n  %v\n--------------\n%v\n\n", m1.HumnPoly, m.Operation, m2.HumnPoly, m.HumnPoly)
		} else {
			m.HumnPoly = []float64{float64(v)}
		}
	}
	if m.Name == "humn" {
		m.DependsOnHumn = true
	}
	return *m.Value
}

func main() {
	MonkeyMap = make(map[string]*Monkey)
	monkeys := aocutils.Lines(os.Args[1], ParseMonkey)
	valueMonkeys := []*Monkey{}
	for i := range monkeys {
		m := &monkeys[i]
		MonkeyMap[m.Name] = m
		if m.Value != nil {
			valueMonkeys = append(valueMonkeys, m)
		}
	}
	for i := range monkeys {
		m := &monkeys[i]
		for _, p := range m.Predecessors {
			n := MonkeyMap[p]
			n.Successors = append(n.Successors, m.Name)
		}
	}

	root := MonkeyMap["root"].Calculate()
	fmt.Printf("Value of root monkey: %v\n", root)
	fmt.Printf("Value of humn monkey: %v\n", MonkeyMap["humn"].Calculate())
	r1 := MonkeyMap[MonkeyMap["root"].Predecessors[0]]
	r2 := MonkeyMap[MonkeyMap["root"].Predecessors[1]]
	v1 := r1.Calculate()
	v2 := r2.Calculate()
	fmt.Printf("Operands for root monkey: %v %v (equals? %v)\n", v1, v2, v1 == v2)
	fmt.Printf("r1 calc: %v\n", r1.HumnPoly)
	fmt.Printf("r2 calc: %v\n", r2.HumnPoly)
}
