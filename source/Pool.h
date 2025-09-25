#ifndef POOL_H
#define POOL_H

#include "User.h"


template < typename T >
class Pool
{
public:
    void put(const User & user)
    {
        v.push_back(user);
    }
    User remove(unsigned int i)
    {
        if (i < v.size() - 1)
            std::swap(v[i], v.back());
        User u = v.back();
        v.pop_back();
        return u;
    }
    unsigned int size() const
    {
        return v.size();
    }
    const User & operator[](int i) const
    {
        return v[i];
    }
    std::vector< User > v;
};

template < typename T >
std::ostream & operator<<(std::ostream & cout, const Pool < T > & pool)
{
    for (unsigned int i = 0; i < pool.size(); i++)
    {
        cout << pool[i] << '\n';
    }
    return cout;
}

#endif
