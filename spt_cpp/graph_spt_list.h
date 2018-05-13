//
// Created by Jiayuan Wang on 11/17/17.
//
#include <iostream>
#include <vector>
#include <map>
#include <set>
#include <queue>

#ifndef BFS_GRAPH_H
#define BFS_GRAPH_H

using namespace std;

struct vertex {
    int name;
    set<int> neighbors;
    bool discovered;
    int pre;
    float comp_min_ind;
    float func_v;

//    typedef pair<int, vertex*> ve;
//    vector<ve> adj; //cost of edge, destination vertex

    vertex(int n, float value) : name(n), func_v(value) {
        discovered = false;
        pre = -1;
        comp_min_ind = -1;
        neighbors.clear();
    }
    vertex(){
        distance = -1;
        discovered = false;
        pre = -1;
        comp_min_ind = -1;
        neighbors.clear();
    };

    void add_neighbor(int add_v) {
        neighbors.insert(add_v);
    }
};

//class vertex_spt {
//public:
//    int name;
//    vector<int> neighbors;
//    float distance;
//    bool discovered;
//    int pre;
//    float comp_min_ind;
//    float func_v;
//
//};

class graph_spt {
public:
    map<int, vertex> vertices;
    int nE;

    graph_spt() : nE(0) {
        vertices.clear();
    }

    bool add_vertex(vertex);

    bool add_edge(int, int);

    void bfs(int name, int &BMname, float &branch_min);

    void bfs_with_min_node(int name, int BMname);

    void reset_discover_state(vector<int>);

    void set_min_for_list(vector<int>, int);

    void retrive_path(int vert_name, vector<int>& vPath);

    void print_graph();

    void print_graph_bfs();

    void print_size();

};

bool graph_spt::add_vertex(vertex v) {
    if (vertices.find(v.name) == vertices.end()) {
        //Not find vertice
        vertices[v.name] = v;
        return true;
    } else {
        //cout << "vertex exitsts!" << endl;
        return false;
    }
}

bool graph_spt::add_edge(int u, int v) {
    if ((vertices.find(u) != vertices.end()) && (vertices.find(v) != vertices.end())) {
        auto iter_u = vertices.find(u);
        auto iter_v = vertices.find(v);
//        (iter_u->second).add_neighbor(v);
//        (iter_v->second).add_neighbor(u);
        vertex &uu = iter_u->second;
        vertex &vv = iter_v->second;
        uu.add_neighbor(v);
        vv.add_neighbor(u);
        nE++;
        return true;
    } else {
        cout << "vertex not found" << endl;
        return false;
    }
}

void graph_spt::bfs(int vert_name, int &BMname, float &branch_min) {
//    queue<int> myqueue;
//    myqueue.push(1);
//    myqueue.push(3);
//    while(!myqueue.empty()){
//        cout<<' '<<myqueue.front();
//        myqueue.pop();
//    }

    queue<int> q;
    vector<int> visited_list;
    q.push(vert_name);
    visited_list.push_back(vert_name);

    vertex &vert = vertices.find(vert_name)->second;
    vert.distance = 0;
    vert.pre = -1;
    branch_min = vert.func_v;
    BMname = vert_name;

    while (!q.empty()) {
        int u = q.front();
        q.pop();
        vertex &node_u = vertices.find(u)->second;
        node_u.discovered = true;
        visited_list.push_back(u);

        if (node_u.func_v <= branch_min) {
            branch_min = node_u.func_v;
            BMname = node_u.name;
        }

        //Iterate over node_u neighbor
        for (auto it = node_u.neighbors.begin(); it != node_u.neighbors.end(); it++) {
            int v = *it;
            vertex &node_v = vertices.find(v)->second;
            if (!(node_v.discovered)) {
                node_v.discovered = true;
                visited_list.push_back(v);
                node_v.distance = node_u.distance + 1;
                node_v.pre = node_u.name;
                q.push(v);
            }
        }
    }

    reset_discover_state(visited_list);
    set_min_for_list(visited_list, BMname);
    //maybe check state after reset
}

void graph_spt::bfs_with_min_node(int vert_name, int BMname) {
    queue<int> q;
    vector<int> visited_list;
    q.push(vert_name);
    visited_list.push_back(vert_name);

    vertex &vert = vertices.find(vert_name)->second;
    vert.distance = 0;
    vert.pre = -1;

    while (!q.empty()) {
        int u = q.front();
        q.pop();
        vertex &node_u = vertices.find(u)->second;
        node_u.discovered = true;
        visited_list.push_back(u);

//        if (node_u->func_v <= branch_min) {
//            branch_min = node_u->func_v;
//            BMname = node_u->name;
//        }

        //Iterate over node_u neighbor
        for (auto it = node_u.neighbors.begin(); it != node_u.neighbors.end(); it++) {
            int v = *it;
            vertex &node_v = vertices.find(v)->second;
            if (!(node_v.discovered)) {
                node_v.discovered = true;
                visited_list.push_back(v);
                node_v.distance = node_u.distance + 1;
                node_v.pre = node_u.name;
                if (node_v.name == BMname) {
                    reset_discover_state(visited_list);
                    return;
                }
                q.push(v);
            }
        }
    }
    reset_discover_state(visited_list);
}

void graph_spt::reset_discover_state(vector<int> node_list) {
    for (auto it = node_list.begin(); it != node_list.end(); it++) {
        vertex &node = vertices.find(*it)->second;
        node.discovered = false;
    }
}

void graph_spt::set_min_for_list(vector<int> node_list, int min_ind) {
    for (auto it = node_list.begin(); it != node_list.end(); it++) {
        vertex &node = vertices.find(*it)->second;
        node.comp_min_ind = min_ind;
    }
}

void graph_spt::retrive_path(int vert_name, vector<int>& vPath){
    vPath.clear();
    vertex vert = vertices.find(vert_name)->second;
    while(vert.pre!=-1){
        vPath.push_back(vert.name);
        int vpre_name = vert.pre;
        vert=vertices.find(vpre_name)->second;
    }
    vPath.push_back(vert.name);
}

void graph_spt::print_graph() {
    for (auto iter1 = vertices.begin(); iter1 != vertices.end(); iter1++) {
        vertex v = iter1->second;
        cout << iter1->first << '(' << v.func_v << ')' << " neighbors:";
        for (auto iter2 = v.neighbors.begin(); iter2 != v.neighbors.end(); iter2++) {
            cout << *iter2;
        }
        cout << '\n';
    }
}

void graph_spt::print_graph_bfs() {
    for (auto iter1 = vertices.begin(); iter1 != vertices.end(); iter1++) {
        vertex v = iter1->second;
        cout << iter1->first << '(' << v.func_v << ')' << endl;
        cout << "neighbors:";
        for (auto iter2 = v.neighbors.begin(); iter2 != v.neighbors.end(); iter2++) {
            cout << *iter2;
        }
        cout << '\n';
        cout << "discover " << v.discovered << endl;
        cout << "pre " << v.pre << endl;
        cout << "comp_min_ind " << v.comp_min_ind << endl;
        cout << '\n';
    }
}

void graph_spt::print_size() {
    cout << "V: " << vertices.size() << " E: " << nE << endl;
}
//class graph
//{
//public:
//    typedef map<string, vertex *> vmap;
//    vmap work;
//    void addvertex(const string&);
//    void addedge(const string& from, const string& to, double cost);
//};
//
//void graph::addvertex(const string &name)
//{
//    vmap::iterator itr = work.find(name);
//    if (itr == work.end())
//    {
//        vertex *v;
//        v = new vertex(name);
//        work[name] = v;
//        return;
//    }
//    cout << "\nVertex already exists!";
//}
//
//void graph::addedge(const string& from, const string& to, double cost)
//{
//    vertex *f = (work.find(from)->second);
//    vertex *t = (work.find(to)->second);
//    pair<int, vertex *> edge = make_pair(cost, t);
//    f->adj.push_back(edge);
//}

#endif //BFS_GRAPH_H
