

#include <iostream>
#include <stdio.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <filesystem>
#include <iostream>
#include <stdlib.h>
#include <limits.h>
#include <stdio.h>

using namespace std;

char *shm_path = (char *)malloc(PATH_MAX);

int write_shared()
{
    // ftok to generate unique key
    key_t key = ftok(shm_path, 65);

    // shmget returns an identifier in shmid
    int shmid = shmget(key, 1024, 0666 | IPC_CREAT);

    // shmat to attach to shared memory
    char *str = (char *)shmat(shmid, (void *)0, 0);

    cout << "Write Data : ";
    cin.getline(str, 1024);

    cout << "Data written in memory: " << str << endl;

    // detach from shared memory
    shmdt(str);

    return 0;
}

int read_shared()
{

    // ftok to generate unique key
    key_t key = ftok(shm_path, 65);

    // shmget returns an identifier in shmid
    int shmid = shmget(key, 1024, 0666 | IPC_CREAT);

    // shmat to attach to shared memory
    char *str = (char *)shmat(shmid, (void *)0, 0);

    cout << "Data read from memory:" << str;

    // detach from shared memory
    shmdt(str);

    // destroy the shared memory
    shmctl(shmid, IPC_RMID, NULL);

    return 0;
}

int main()
{
    printf("Started");
    realpath("./../../../.local/g++/shmfile", shm_path);
    printf("Running @ %s\n", shm_path);
    read_shared();
    printf("\n");
}