#pragma once

#include "tree.hpp"
#include <memory>
#include <iostream>


namespace tree_utils
{


template<typename T>
void get_tree_data(const std::shared_ptr<Tree<T>>& t, int level, 
        std::vector<std::vector<std::pair<T, T>>>& results)
{
    if (results.size() < level + 1)
    {
        results.push_back({});
    }

    if (t->get_parent() != nullptr)
        results[level].push_back(std::make_pair(t->get_parent()->get_data(), t->get_data()));
    else
        results[level].push_back(std::make_pair(-1, t->get_data()));
    
    for (auto&& c : t->get_children())
    {
        get_tree_data(c, level+1, results);
    }
}


template<typename T>
std::vector<std::vector<std::pair<T, T>>> print_tree(const std::shared_ptr<Tree<T>>& t)
{
    std::vector<std::vector<std::pair<T, T>>> results;
    get_tree_data(t, 0, results);
    for (auto &&result : results)
    {
        for (auto &&value : result)
        {
            std::cout << "(" << value.first << ", " << value.second << ")" << ", ";
        }
        std::cout << std::endl;
    }
    
    return results;
}

};
