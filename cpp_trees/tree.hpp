#pragma once
#include <memory>


namespace tree_utils
{
template<typename T>
struct find;
}

template<typename T>
class Tree : public std::enable_shared_from_this<Tree<T>>
{
public:
    Tree(T data): data(data)
    { }
    Tree(T data, std::vector<std::shared_ptr<Tree<T>>> children): data(data)
    { this->add_children(children); }

    void add_child(std::shared_ptr<Tree<T>>& child);
    void add_children(std::vector<std::shared_ptr<Tree<T>>> children);

    void set_parent(std::shared_ptr<Tree<T>> parent)
    { this->parent = parent; }
    
    const T get_data() const
    { return this->data; }
    std::shared_ptr<Tree<T>> get_parent() const
    { return this->parent.lock(); }
    const std::vector<std::shared_ptr<Tree<T>>>& get_children() const
    { return this->children; }

    tree_utils::find<T> find(T value);


private:
    T data;
    std::weak_ptr<Tree<T>> parent;
    std::vector<std::shared_ptr<Tree<T>>> children;
};

template<typename T>
void Tree<T>::add_child(std::shared_ptr<Tree<T>>& child)
{
    this->children.push_back(child);
    child->set_parent(this->shared_from_this());
}


template<typename T>
void Tree<T>::add_children(std::vector<std::shared_ptr<Tree<T>>> children)
{
    for (auto&& child : children)
    {
        this->children.push_back(child);
        child->set_parent(this->shared_from_this());
    }
}



namespace tree_utils
{

template<typename T>
struct find
{
    T value;
    std::shared_ptr<Tree<T>> current_node;
    std::vector<std::shared_ptr<Tree<T>>> to_visit;
    find(const std::shared_ptr<Tree<T>>& tree, const T& value) : value(value), current_node(tree)
    { }

    const std::shared_ptr<Tree<T>> next()
    {
        if (this->current_node == nullptr) return nullptr;

        // update nodes to visit
        for (auto&& child : this->current_node->get_children())
        {
            this->to_visit.push_back(child);
        }

        // save current node into variable
        std::shared_ptr<Tree<T>> current_node = this->current_node;
        // get next node
        if (!this->to_visit.empty())
        {
            this->current_node = this->to_visit[this->to_visit.size()-1];
            this->to_visit.pop_back();
        }
        else
        {
            this->current_node = nullptr;
        }
        // check if the current node is an answer
        return current_node->get_data() == value ? current_node : this->next();
    }


    const std::vector<std::shared_ptr<Tree<T>>> all()
    {
        std::vector<std::shared_ptr<Tree<T>>> results;

        while (true)
        {
            std::shared_ptr<Tree<T>> result = this->next();
            if (result == nullptr) break;
            results.push_back(result);
        }
        
        return results;
    }
};

}