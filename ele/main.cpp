// Create
// - clock.h and clock.cpp
// - elevator_door.h and elevator_door.cpp

#include <iostream>
#include <unistd.h> /* for the sleep() function */

// The elevator door motor has three states: it is either
// 0. at rest or
// 1. turning in such a way that it is opening the elevator door or
// 2. it is turning in such a way that it is closing the elevator door.
//
// There are sensors on the doors so that
// 1. When the elevator is fully open, the "door open sensor" reads 1; otherwise
//    it is 0. The "door open sensor" sets the "door open register" to 1 or 0
//    automatically, i.e., this is a read-only register.
// 2. When the elevator is fully closed, the "door close sensor" read 1; otherwise
//    it is 0. The "door close sensor" set the "door close register" to 1 or 0
//    automatically, i.e., this is a read-only register.
// 3. There are optical "obstruction sensors" on the doors so that if there
//    objects in the part of the door, the "obstruction register" is set to 1.
//
// For simulations, the elevator_door_gap indicates "how open" is the door
// where 0.0 means the door is fully closed and 1.0 means the door is fully
// open. It is not a parameter directly set by the elevator or the elevator's
// computer. Rather, it's a private parameter used by the simulation software.
// This piece of information cannot be read/set by the elevator door computer.
//
// The "load sensor" sense the amount of payload currently in the elevator.
// The max load is maximum load beyond which safety is not guaranteed.

const int DOOR_MOTOR_STATE_STOP = 0;
const int DOOR_MOTOR_STATE_OPEN = 1;
const int DOOR_MOTOR_STATE_CLOSE = 2;

// These are global variables - make them local to the simulator_run() function
static int elevator_door_motor_state;

static double elevator_door_speed;
static int elevator_door_open_register;
static int elevator_door_close_register;       
static int elevator_door_obstruction_register; 
static double elevator_door_gap;

static int elevator_load_sensor;
static int elevator_max_load;

void elevator_door_init()
{
    elevator_door_motor_state = DOOR_MOTOR_STATE_STOP;
    elevator_door_speed = 0.1;
    elevator_door_open_register = 0;
    elevator_door_close_register = 1;
    elevator_door_gap = 0.0;
    elevator_load_sensor = 0;
    elevator_max_load = 1000;
}

void elevator_door_motor_set_state(int state)
{
    elevator_door_motor_state = state;
}

bool elevator_door_open_sensor_get_state()
{
    return elevator_door_open_register;
}

void elevator_computer_run(double clock_time)
{
    if (clock_time > 2)
    {
        elevator_door_motor_state = DOOR_MOTOR_STATE_OPEN;
    }
}

void elevator_door_run(double dt)
{
    switch (elevator_door_motor_state)
    {
        case DOOR_MOTOR_STATE_STOP:
            break;
        case DOOR_MOTOR_STATE_OPEN:
            elevator_door_gap += elevator_door_speed * dt;
            break;
        case DOOR_MOTOR_STATE_CLOSE:
            elevator_door_gap -= elevator_door_speed * dt;
            break;
    }
    if (elevator_door_gap < 0)
    {
        std::cout << "ERROR: elevator_door_motor is closing too much!\n";
        elevator_door_gap = 0;
    }
    else if (elevator_door_gap > 1)
    {
        std::cout << "ERROR: elevator_door_motor is opening too much!\n";
        elevator_door_gap = 1;
    }
}

void elevator_door_print()
{
    std::cout << "<elevator_door "
              << "motor:" << elevator_door_motor_state << ", "
              << "speed:" << elevator_door_speed << ", "
              << "open_register:" << elevator_door_open_register << ", "
              << "close_register:" << elevator_door_close_register << ", "
              << "obstruction_register:" << elevator_door_obstruction_register << ", "
              << "gap:" << elevator_door_gap << '>'
              << std::endl;
}


void simulator_run()
{
    std::cout << "run elevator simulator" << std::endl;
    double clock_time = 0.0;
    double dt = 1.0;
    double total_time = 20.0;
    elevator_door_init();
    
    while (clock_time < total_time)
    {
        std::cout << '\n';
        clock_time += dt;
        std::cout << "<clock: " << clock_time << ">" << std::endl;
        
        elevator_computer_run(clock_time);
        elevator_door_run(dt);
        elevator_door_print();
        sleep(1);
    }
}


int main()
{
    simulator_run();
    return 0;
}
