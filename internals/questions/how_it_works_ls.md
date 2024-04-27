# What happens when you type ls -l

I'll describe the process going from

1. The hardware
1. The kernel (input)
1. The shell + parsing
1. The application ls

## Hardware

The user press the key, which generates a signal in the motherboard input. This is mapped to the device input, which is mapped to the memory (Memory mapping vs bus). A hardware interrupt is then called and this signal is transferred to the kernel.

## Kernel

The kernel receives the signal and triggers the right function that handles the event and data. This adds the keystroke to a buffer. We write 'ls -l'. Then press enter.

This is generally what happens on keyboard strikes, from a machine with a keyboard. These keystrokes are then forwarded to the active tty (teletypewriter) which allows remote inputs.

This input stream is then fed to the `stdin` pipe, which can be read by the running application.

## The shell

Note that the shell program started before we started typing. The program printed a prompt
`$>`
And started reading from `stdin`, and waited for symbol newline `\n`. Once read the shell has the following string

```string
ls -l
```

### Parsing

The shell will then parse the input. The parsing by default is done by spaces, but if an environment IFS is set, this can be different things.

We parse the input into fields,
[`ls`, `-a`] argument fields zero indexed.

This is the argument list, where arg0 ($0 = ls).
We now use $0 to identify the program we need to run.

### Lookup and execution

In general the we look at the possible paths and args and aliases for the application. ls for example would either be an alias or program in the path (preloaded). We look for these.

If it was "./ls" then we wil search the current folder and extra.

We now follow the symbolic links if any and find the filepath of the actual file.

### Execution

To execute under the current process we run

1. fork
1. in the fork `exec(path, *args, (char*)null)` which replaces the forked process.
1. outside the fork `wait(fork id)` if the symbol "&" did not appear at the end.

The shell will now wait for the ls command to complete.

## ls application

The ls application is aimed to show the contents of a directory, with all its properties.

1. Get the current directory (getcwd)
1. Then opens and list the directory contents (opendir(), readdir(), closedir()).
1. For each entry stat it. And print each stat.
1. We have a list.

Application exits.

## Back to shell

1. If shell was waiting, shell resumes after wait.
1. Go to top of loop and print "$>"
1. Wait for entry.
