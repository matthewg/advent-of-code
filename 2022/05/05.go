package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"strconv"
	"strings"
)

type Crate rune
type Stack []Crate

func (c Crate) String() string {
	return string(c)
}

func main() {
	bs, err := ioutil.ReadFile(os.Args[1])
	if err != nil {
		log.Fatal(err)
	}

	s := string(bs)
	rs := strings.Split(s, "\n\n")
	starts := rs[0]
	moves := rs[1]

	var stacks []Stack
	startLines := strings.Split(starts, "\n")
	for i := len(startLines) - 2; i >= 0; i-- {
		line := strings.TrimSuffix(startLines[i], "\n")
		fmt.Printf("Line: %v\n", line)
		for stack := 0; stack*4 < len(line); stack++ {
			if (stack + 1) > len(stacks) {
				stacks = append(stacks, Stack{})
				fmt.Printf("After adding stack %v, now have: %v\n", stack, stacks)
			}
			c := line[stack*4+1]
			if c == ' ' {
				continue
			}

			fmt.Printf("Adding %v to stack %v\n", string(c), stack)
			stacks[stack] = append(stacks[stack], Crate(c))
		}
	}
	for i, stack := range stacks {
		fmt.Printf("Stack %v: %v\n", i, stack)
	}

	for _, move := range strings.Split(moves, "\n") {
		move = strings.TrimSuffix(move, "\n")
		if move == "" {
			continue
		}
		toks := strings.Split(move, " ")
		fmt.Printf("\nMove: '%v'\n", move)
		cnt, err := strconv.Atoi(toks[1])
		if err != nil {
			log.Fatalf("Error converting cnt from %v: %v", move, err)
		}

		srcStack, err := strconv.Atoi(toks[3])
		if err != nil {
			log.Fatalf("Error converting srcStack from %v: %v", move, err)
		}
		srcStack -= 1

		dstStack, err := strconv.Atoi(toks[5])
		if err != nil {
			log.Fatalf("Error converting dstStack from %v: %v", move, err)
		}
		dstStack -= 1

		fmt.Printf("Moving %v from %v to %v\n", cnt, srcStack, dstStack)

		// part 1
		/*
			for i := 0; i < cnt; i++ {
				item := stacks[srcStack][len(stacks[srcStack])-1]
				stacks[dstStack] = append(stacks[dstStack], item)
				stacks[srcStack] = stacks[srcStack][:len(stacks[srcStack])-1]
			}
		*/

		// part 2
		items := stacks[srcStack][len(stacks[srcStack])-cnt:]
		stacks[dstStack] = append(stacks[dstStack], items...)
		stacks[srcStack] = stacks[srcStack][:len(stacks[srcStack])-cnt]

		for i, stack := range stacks {
			fmt.Printf("Stack %v: %v\n", i, stack)
		}
	}
	for _, stack := range stacks {
		fmt.Printf("%v", stack[len(stack)-1])
	}
	fmt.Printf("\n")
}
