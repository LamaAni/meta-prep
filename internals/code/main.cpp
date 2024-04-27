#include <sys/wait.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdio.h>
#include <random>
#include <chrono>

auto started = std::chrono::high_resolution_clock::now();

void tic()
{
    started = std::chrono::high_resolution_clock::now();
}

float toc()
{
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(std::chrono::high_resolution_clock::now() - started);
    return duration.count() * 1.0 / 1000;
}

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
        throw std::exception();
    }

    execl("/bin/ls", "ls", "-l", NULL);
    return 0;
}

int test_files()
{
    int fid = open("/tmp/dump.txt", O_RDWR);
    if (fid == -1)
    {
        printf("File not found or other error");
        throw "Error";
    }

    char buff[1000];
    int read_count = read(fid, &buff, sizeof(buff));
    printf("Read %d bytes: ", read_count);
    printf("%s", buff);

    close(fid);
    return 0;
}

int heap_vs_stack()
{
    tic();
    int val = 0;

    printf("%d\n", val);
    int idx = 0;
    while (idx < 1000000)
    {
        val = idx;
        idx += 1;
    }
    printf("%d in %f [ms]\n", val, toc());

    return 0;
}

int main()
{
    return heap_vs_stack();
}