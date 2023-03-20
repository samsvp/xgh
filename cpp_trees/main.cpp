#include <vector>
#include <memory>
#include <iostream>

#include "tree.hpp"
#include "tree_utils.hpp"


std::shared_ptr<Tree<int>> create_tree()
{
    // init tree and nodes
    std::shared_ptr<Tree<int>> tree(new Tree<int>(1));
    std::shared_ptr<Tree<int>> leaf1(new Tree<int>(5));
    std::shared_ptr<Tree<int>> leaf2(new Tree<int>(4));
    std::shared_ptr<Tree<int>> leaf11(new Tree<int>(1));

    // construct tree
    leaf1->add_child(leaf11);
    std::vector<std::shared_ptr<Tree<int>>> v;
    v.push_back(leaf1);
    v.push_back(leaf2);
    tree->add_children(v);

    return tree;
}


int main() 
{

    std::shared_ptr<Tree<int>> tree = create_tree();
    // print tree
    tree_utils::print_tree(tree);

    auto f = tree_utils::find<int>(tree, 1);
    auto t = f.next();
    std::cout << "found tree" << std::endl;
    tree_utils::print_tree(t);
    t = f.next();
    if (t == nullptr)
        std::cout << "null pointer" << std::endl;
    else 
    {
        std::cout << "found tree" << std::endl;
        tree_utils::print_tree(t);
    }
    
    auto ts = tree_utils::find<int>(tree, 1).all();
    std::cout << "found " << ts.size() << " trees" << std::endl;

    return 0;
}