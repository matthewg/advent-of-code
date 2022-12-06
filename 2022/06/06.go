package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"strings"
)

type SignalFinder struct {
	buffer  *string
	foundAt int
}

func MakeSignalFinder(length int) SignalFinder {
	var ret string
	for i := 0; i < length; i++ {
		ret += "_"
	}
	return SignalFinder{&ret, 0}
}

func (s *SignalFinder) GotByte(pos int, r rune) {
	if s.foundAt != 0 {
		//fmt.Printf("ret due to found: %v\n", s.foundAt)
		return
	}
	*s.buffer = (*s.buffer)[1:] + string(r)
	if pos < len(*s.buffer) {
		//fmt.Printf("ret due to buffer: %v\n", s.buffer)
		return
	}

	bPop := make(map[rune]bool)
	for _, c := range *s.buffer {
		r := rune(c)
		if r == '_' {
			return
		}
		bPop[r] = true
	}

	//fmt.Printf("bPop calc: %v -> %v\n", s.buffer, bPop)
	if len(bPop) == len(*s.buffer) {
		//fmt.Printf("Found at %v!\n", pos)
		s.foundAt = pos
	}
}

func main() {
	bs, err := ioutil.ReadFile(os.Args[1])
	if err != nil {
		log.Fatal(err)
	}

	startOfPacket := MakeSignalFinder(4)
	startOfMessage := MakeSignalFinder(14)
	s := strings.TrimSuffix(string(bs), "\n")
	for i, b := range s {
		bCnt := i + 1
		r := rune(b)
		startOfPacket.GotByte(bCnt, r)
		startOfMessage.GotByte(bCnt, r)
	}
	fmt.Printf("Found SOP: %v\n", startOfPacket.foundAt)
	fmt.Printf("Found SOM: %v\n", startOfMessage.foundAt)
}
