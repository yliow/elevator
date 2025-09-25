#include <iostream>
#include <algorithm>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <deque>

#include "Clock.h"
#include "Pool.h"
#include "User.h"


class Door
{
public:
    bool open;
};

class Elevator
{
    
};

class ElevatorControl
{
};





/*
  
  We need to run through the "queue".
  If a user is going the same direction as the
  elevator, the user enters the elevator. Otherwise
  the user can decide to enter or not.
  
 */
class FloorQueue
{
public:
    std::vector< User > q;
    void enqueue(const User & user)
    {
        q.push_back(user);
    }
    std::vector< User > dequeue(const int direction,
                                const int capacity)
    {
        std::vector< User > ret;
        std::vector< User > newq;
        for (unsigned int i = 0; i < q.size(); i++)
        {
            User u = q[i];
            if (u.get_direction() == direction)
            {
                // maybe it's better to pass the direction to the user and let him decide
                ret.push_back(u);
            }
            else
            {
                newq.push_back(u);
            }
        }
        q = newq;
        return ret;
    }
    unsigned int size() const
    {
        return q.size();
    }
    const User & operator[](unsigned int i) const
    {
        return q[i];
    }
};

std::ostream & operator<<(std::ostream & cout,
                          const FloorQueue & q)
{
    cout << "<FloorQueue \n";
    for (unsigned int i = 0; i < q.size(); ++i)
    {
        cout << "    " << q[i] << '\n';
    }
    cout << ">";
    return cout;
}

class Simulator
{
public:
    Simulator(int num_elevators=1,
              int num_floors=10,
              double seconds=1000)
    {}
    void run()
    {
    }
};


int main()
{
    const int NUM_USERS = 10;
    const int NUM_FLOORS = 10;
    const int NUM_ELEVATORS = 1;
    
    srand((unsigned int) time(NULL));

    Clock clock;
    std::cout << clock << std::endl;
    clock.update();
    std::cout << clock << std::endl;

    Pool< User > pool;
    for (int i = 0; i < NUM_USERS; i++)
    {
        pool.put(User());
    }
    std::cout << pool << std::endl;

    FloorQueue queue[NUM_FLOORS];
    queue[0].enqueue(User());
    std::cout << queue[0] << '\n';
    return 0;
}
