#include <coroutine>

using namespace std;

struct CoroFrame
{
    Task<int>::promise_type promise;
    bool initial_await_resume_called = false;
    int state = 0;
};

int coro_func(CoroFrame &coro)
{
    while (true)
    {
        switch (coro.state)
        {
        case 0:
            // Do something
            coro.state = 1;
            coro.promise.yield_value(42);
            await coro.promise.initial_suspend();
        case 1:
            // Do something else
            coro.state = 2;
            coro.promise.yield_value(84);
            await coro.promise.final_suspend();
        case 2:
            // Done
            coro.promise.return_value(126);
            return 126;
        }
    }
}

int main()
{
    CoroFrame coro;
    coro_func(coro);

    int result = coro.promise.get_return_object().get_result();

    cout << result << endl;

    return 0;
}