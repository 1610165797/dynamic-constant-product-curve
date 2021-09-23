#include <vector>
#include <iostream>
#include <iomanip>
#include <fstream>
using namespace std;

volatile long double granularity = 1;
volatile long double xf = 110;

class Curve
{
public:
    long double w, a, mkp, x, y, k;
    vector<Curve *> next;
    Curve *prev;
    Curve(long double k, long double mkp, long double x, long double y, Curve *prev, ofstream &myfile);
    void print();
    long double get_y(long double x);
    long double minimum();
    void export_final_y();
};

long double Curve::get_y(long double x)
{
    return this->k / this->w / (x - this->a);
}

Curve::Curve(long double k, long double mkp, long double x, long double y, Curve *prev, ofstream &myfile)
{
    this->x = x;
    this->y = y;
    this->k = k;
    this->mkp = mkp;
    this->a = x - (y / mkp);
    this->w = k * mkp / y / y;
    if (x == xf)
    {
        myfile << this->get_y(xf) << endl;
    }
    for (long double i = x + granularity; i <= xf; i += granularity)
    {
        Curve *temp = new Curve(k, mkp, i, this->get_y(i), this, myfile);
        this->next.push_back(temp);
    }
}

void Curve::print()
{
    cout << "w is: " << this->w << ", a is: " << this->a << ", point is: (" << this->x << ", " << this->y << ")" << endl;
}

int main()
{
     std::setprecision(16);
    long double x0 = 100;
    long double y0 = 100;
    long double mkp = 5;
    long double k = 10000;
    long double sensitivity = 0.01;
    xf = 110;

    ofstream myfile;
    myfile.open("data.txt");
    myfile << "Final y values.\n";

    Curve *head = new Curve(k, mkp, x0, y0, NULL, myfile);
    myfile.close();
    head->print();
    Curve *temp = head;

    int c = 0;
    while (c < 10)
    {
        for (int i = 0; i < c; i++)
        {
            temp = temp->next[0];
        }
        temp->print();
        c++;
    }

  

    return 0;
}