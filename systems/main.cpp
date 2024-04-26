#include <sys/wait.h>
#include <unistd.h>
#include <stdio.h>
#include <random>

int test_proc_management()
{
    pid_t pid;
    int a = 0;
    int b = rand();
    pid = fork();
    srand(pid);
    printf("Started %d\n", pid);

    printf("%d %d\n", a, b);
    a = rand();
    printf("%d %d\n", a, b);

    if (pid == 0)
    {
        int stat;
        printf("waiting for child...\n");
        waitpid(pid, &stat, 0);
        printf("Child done\n");
    }
    else
    {
        throw "Error";
    }

    execl("/bin/ls", "ls", "-l", NULL);
    return 0;
}

int test_files()
{
}

int main()
{
}