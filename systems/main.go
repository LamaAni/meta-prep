package main

import "syscall"

func main() {
	println("test")
	syscall.Exec("ls", []string{"/tmp"}, []string{})
	println("Done")
}
