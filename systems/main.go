package main

import (
	"syscall"
)

func main() {
	var buf []byte
	syscall.Read(9, buf)
}
