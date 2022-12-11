package main

import (
	"fmt"
	"os"
	"sort"
	"strconv"
	"strings"

	"github.com/matthewg/advent-of-code/golang/aocutils"
)

type Item int

type Monkey struct {
	Items       []Item
	OperandA    func(Item) Item
	OperandB    func(Item) Item
	DoOperation func(Item, Item) Item
	TestMod     Item
	TrueMonkey  int
	FalseMonkey int
}

func OpTokToFn(s string) func(Item) Item {
	if s == "old" {
		return func(old Item) Item { return old }
	} else {
		a, _ := strconv.Atoi(s)
		return func(_ Item) Item { return Item(a) }
	}
}

func ParseMonkey(s string) *Monkey {
	lines := strings.Split(s, "\n")
	m := Monkey{}

	itemsS := strings.Split(strings.Split(lines[1], ": ")[1], ", ")
	for _, itemS := range itemsS {
		item, _ := strconv.Atoi(itemS)
		m.Items = append(m.Items, Item(item))
	}

	opToks := strings.Split(strings.Split(lines[2], ": new = ")[1], " ")
	m.OperandA = OpTokToFn(opToks[0])
	m.OperandB = OpTokToFn(opToks[2])
	if opToks[1] == "+" {
		m.DoOperation = func(a, b Item) Item {
			ret := a + b
			//fmt.Printf("    Adding %v and %v to get %v\n", a, b, ret)
			return ret
		}
	} else {
		m.DoOperation = func(a, b Item) Item {
			ret := a * b
			//fmt.Printf("    Multiplying %v and %v to get %v\n", a, b, ret)
			return ret
		}
	}

	x, _ := strconv.Atoi(strings.Split(strings.TrimPrefix(lines[3], "  "), " ")[3])
	m.TestMod = Item(x)
	m.TrueMonkey, _ = strconv.Atoi(strings.Split(strings.TrimPrefix(lines[4], "    "), " ")[5])
	m.FalseMonkey, _ = strconv.Atoi(strings.Split(strings.TrimPrefix(lines[5], "    "), " ")[5])
	//fmt.Printf("Monkey: %v\n", m)
	return &m
}

func GCD(a, b Item) Item { // Source: https://siongui.github.io/2017/06/03/go-find-lcm-by-gcd/
	for b != 0 {
		t := b
		b = a % b
		a = t
	}
	return a
}

func LCM(a, b Item, integers ...Item) Item { // Source: https://siongui.github.io/2017/06/03/go-find-lcm-by-gcd/
	result := a * b / GCD(a, b)

	for i := 0; i < len(integers); i++ {
		result = LCM(result, integers[i])
	}

	return result
}

func main() {
	monkeys := aocutils.Records(os.Args[1], "\n\n", ParseMonkey)
	var inspects []int
	megadiv := Item(1)
	for _, m := range monkeys {
		inspects = append(inspects, 0)
		megadiv *= m.TestMod
	}

	for round := 1; round <= 10000; /* part 1: 20 */ round++ {
		for mI, m := range monkeys {
			//fmt.Printf("Monkey %v:\n", mI)
			for _, item := range m.Items {
				//fmt.Printf("  Monkey inspects an item with a worry level of %v.\n", item)
				inspects[mI]++
				new := m.DoOperation(m.OperandA(item), m.OperandB(item)) % megadiv

				var dest int
				if new%Item(m.TestMod) == 0 {
					dest = m.TrueMonkey
				} else {
					dest = m.FalseMonkey
				}
				//fmt.Printf("    Throwing to %v.\n", dest)
				monkeys[dest].Items = append(monkeys[dest].Items, new)
			}
			m.Items = []Item{}
		}
		if round == 1 || round == 20 || round%1000 == 0 {
			fmt.Printf("\n== After round %v ==\n", round)
			for i, w := range inspects {
				fmt.Printf("Monkey %v inspected items %v times, and has items %v.\n", i, w, monkeys[i].Items)
			}
		}
	}

	sort.Ints(inspects)
	fmt.Printf("Monkey business: %v\n", inspects[len(inspects)-2]*inspects[len(inspects)-1])
}
