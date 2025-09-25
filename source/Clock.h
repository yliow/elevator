#ifndef CLOCK_H
#define CLOCK_H

class Clock
{
public:
    Clock()
        : time(0)
    {}
    void update()
    {
        time++;
    }
    int get_ticks() const
    {
        return time;
    }
private:
    int time;
};

inline
std::ostream & operator<<(std::ostream & cout, const Clock & clock)
{
    cout << "<Clock time: " << clock.get_ticks() << ">";
    return cout;
}

#endif
