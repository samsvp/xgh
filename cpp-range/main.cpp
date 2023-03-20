#include <vector>
#include <iostream>
#include <range/v3/all.hpp>

using namespace ranges;


int main()
{
    std::vector<int> v = views::iota(0) 
        | views::take(10) 
        | views::transform([](const int& i) {return 2 * i; })
        | views::remove_if([](const int& i) { return i % 2; })
        | to<std::vector>();

    ranges::for_each(v, [](const int& i) { std::cout << i << std::endl; });
    return 0;
}