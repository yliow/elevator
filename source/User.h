#ifndef USER_H
#define USER_H

class User
{
public:
    enum State {POOL, QUEUE, ELEVATOR};
    User(int floor0=0)
        : id(next_id++), floor(floor0), state(POOL),
          weight(1)
    {}    
    int get_id() const { return id; }
    int get_floor() const { return floor; }
    State get_state() const { return state; }
    int get_direction() const { return direction; }
    bool enter_elevator(int elevator_direction, int remaining_capacity)
    {
        return elevator_direction == direction;
    }
    static int next_id; // auto increment id
    int id;
    int floor;
    int target_floor; // set only when user is in queue
    State state;
    int start_time;
    int total_time;
    int weight;
    int direction; // set only when the user waits in queue
};

int User::next_id(0);

std::ostream & operator<<(std::ostream & cout, const User & user)
{
    cout << "<User id: " << user.get_id() << ", "
         << "floor: " << user.get_floor() << ", "
         << "state: " << (user.get_state() == User::POOL ? "POOL":
                          user.get_state() == User::QUEUE ? "QUEUE":
                          "ELEVATOR")
         << ">";
    return cout;
}

#endif
