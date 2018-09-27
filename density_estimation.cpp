#include<cstdlib>
#include<cmath>
#include<dirent.h>
#include<fstream>
#include<iostream>
#include<limits>
#include<string.h>
#include<stdio.h>
#include<vector>


using namespace std;
string PATH = "./tripdata/";
// string PATH = "C:/Users/XsugarX/Desktop/Draft/DATA/trip_chicago/";
// string PATH = "C:/Users/XsugarX/Desktop/Draft/DATA/trip_berlin_large/";
//string PATH;
double STEP=10; // use 10 for default
double Support=20; // use 10 for default

int GAUSS = 3*floor(Support/STEP);
const double PI = acos(-1.0);

struct sample{
    double x;
    double y;
    double time;
};

vector<vector<sample> > data;
vector<vector<double> > density_count;
double minx = numeric_limits<double>::max(), miny = numeric_limits<double>::max(), maxx = -1, maxy = -1; // bounding box
int xdim, ydim;

vector<string> GetAllFiles(){
    DIR *pDIR;
    struct dirent *entry;
    vector<string> rtn;
    rtn.clear();

    if( (pDIR = opendir(PATH.c_str())) ){
        while( (entry = readdir(pDIR)) ){
            if( strcmp(entry->d_name, ".") != 0 && strcmp(entry->d_name, "..") != 0 )
                rtn.push_back(entry->d_name);
        }
        closedir(pDIR);
    }
    return rtn;
}

vector<sample> read_data(string filepath){
    FILE *fp = fopen(filepath.c_str(), "r");
    double x,y,time;
    vector<sample> rtn;
    rtn.clear();

    while(fscanf(fp, "%lf %lf %lf",&x, &y, &time)!=EOF){
        sample sample_data;
        sample_data.x = x; sample_data.y = y; sample_data.time = time;
        rtn.push_back(sample_data);
        if (minx > x) minx = x;
        if (miny > y) miny = y;
        if (maxx < x) maxx = x;
        if (maxy < y) maxy = y;
    }
    fclose(fp);
    return rtn;
}

int OutputProgress(int current, int total, int rem){
    int outamount = 0;
    printf("\33[2K\r");
    outamount = printf("%d / %d\n", current, total);

    return outamount;
}

void fillpoint(double x0, double y0, double xend, double yend, double step){
    // x0, y0 starting point
    // xend, yend ending point
    // x, y direction
    // px, py starting grid
    // step stepsize
    double x = xend - x0;
    double y = yend - y0;

    int px = floor((x0 - minx) / step);
    int py = floor((y0 - miny) / step);
    int range_x, range_y;

    int counter = 0;
    while ((xend-x0)*x+(yend-y0)*y > 0){ //if still not reach the ending point.
        //Gaussian kernel
        if (GAUSS > 0){
            for (range_x = -GAUSS; range_x <= GAUSS; ++range_x)
                for (range_y = -GAUSS; range_y <= GAUSS; ++range_y){
                    int now_x = (px + range_x);
                    int now_y = (py + range_y);
                    //keyv= now_y * 10 ^ 6 + now_x;
                    double dx = (now_x + 0.5) * step + minx - x0;
                    double dy = (now_y + 0.5) * step + miny - y0;

                    double val = 1.0 / (2 * PI * Support * Support) * exp(-(dx * dx + dy *dy) / 2.0 / (Support * Support) );
                    if (now_x >= 0 && now_x < xdim && now_y >=0 && now_y <ydim)
                        density_count[now_x][now_y] = density_count[now_x][now_y] + val;
                }
        }
        else{
            density_count[px][py] = density_count[px][py] + 1;
        }

        // compute next grid
        // distance to both edges
        double Sx = (px+1) * step - (x0-minx);
        double Sy = (py+1) * step - (y0-miny);

        if (x<0) Sx = step - Sx;
        if (y<0) Sy = step - Sy;

        int pxnew, pynew;
        double x1,y1;
        // intersect type
        if (x>0){ // Assume do not intersect exactly at the corner
            if (y>0){
                if (fabs(Sy*x)-fabs(Sx*y) > 0){
                    pxnew=px+1;
                    pynew=py;
                    x1=x0+Sx*(x/fabs(x));
                    y1=y0+Sx*(y/fabs(x));
                }
                else{
                    pxnew=px;
                    pynew=py+1;
                    x1=x0+Sy*(x/fabs(y));
                    y1=y0+Sy*(y/fabs(y));
                }
            }
            else{
                if ((fabs(Sy*x)- fabs(Sx*y)) > 0){
                    pxnew=px+1;
                    pynew=py;
                    x1=x0+Sx*(x/fabs(x));
                    y1=y0+Sx*(y/fabs(x));
                }
                else{
                    pxnew=px;
                    pynew=py-1;
                    x1=x0+Sy*(x/fabs(y));
                    y1=y0+Sy*(y/fabs(y));
                }
            }
        }
        else{
            if (y>0){
                if (fabs(Sy*x)- fabs(Sx*y) > 0){
                    pxnew=px-1;
                    pynew=py;
                    x1=x0+Sx*(x/fabs(x));
                    y1=y0+Sx*(y/fabs(x));
                }
                else{
                    pxnew=px;
                    pynew=py+1;
                    x1=x0+Sy*(x/fabs(y));
                    y1=y0+Sy*(y/fabs(y));
                }
            }
            else{
                if (fabs(Sy*x) - fabs(Sx*y) > 0){
                    pxnew=px-1; pynew=py;
                    x1=x0+Sx*(x/fabs(x)); y1=y0+Sx*(y/fabs(x));
                }
                else{
                    pxnew=px;
                    pynew=py-1;
                    x1=x0+Sy*(x/fabs(y));
                    y1=y0+Sy*(y/fabs(y));
                }
            }
        }
        x0 = x1; y0 = y1; px = pxnew; py = pynew;
        //printf("%f %f\n", x0, y0);
        counter++;
    }
    //printf("########%d \n", counter);
}

void KDE(){
//convert trace to density map
    if (data.size()<1){
        printf("Not enough trajectories\n");
        return;
    }
    int last = 0;
    for(int i = 0; i < data.size(); i++){
        if (data[i].size()<=3) continue;

        //output progress
        //last = OutputProgress(i+1, data.size(), last);
        for(int j = 1; j < data[i].size(); j++){
            double sx,sy,ex,ey;// start x end y
            sx = data[i][j-1].x; sy = data[i][j-1].y;
            ex = data[i][j].x; ey = data[i][j].y;
            //printf("%f %f - %f %f", sx, sy, ex, ey);
            fillpoint(sx, sy, ex, ey, STEP);
        }
    }
}

void output_grid(){
    FILE *fppts = fopen("dataset/2dgrid/grid.txt","w");
    for(int i = 0; i < density_count.size(); i++){
        for(int j = 0; j < density_count[i].size(); j++)
            if (j==0) fprintf(fppts, "%f", density_count[i][j]);
            else fprintf(fppts, " %f", density_count[i][j]);
        fprintf(fppts, "\n");
    }
    fclose(fppts);
}

int main(int nargin, char** vargin){
    if (nargin!=4){
        printf("Usage: density_estimation <path> <step size> <sigma>\n");
        //exit(0);
    }else{
        PATH = string(vargin[1]);
        STEP = atoi(vargin[2]);
        Support = atoi(vargin[3]);
        GAUSS = 3*floor(Support/STEP);
    }
    // get all file paths
    vector<string> filenames = GetAllFiles();
    printf("%d\n", filenames.size());

    // read all files and find the bounding box
    // counter location = int ((pos - min) / step)
    int last = 0;
    for(int i = 0; i < filenames.size(); i++){
        //output progress
        //last = OutputProgress(i+1, filenames.size(), last);
        string openfile = PATH + filenames[i];
        vector<sample> file_data = read_data(openfile);
        if (file_data.size()!=0)
            data.push_back(file_data);
    }
    printf("bounding box: %f %f - %f %f\n", minx, miny, maxx, maxy);

    //initialize density matrix
    xdim = ceil((maxx - minx) / STEP);
    ydim = ceil((maxy - miny) / STEP);
    printf("xy dimension %d %d", xdim, ydim);
    for(int i = 0; i < xdim; i++)
    {
        vector<double> row(ydim, 0);
        // std::fill(row.begin(), row.end(), 0);
        density_count.push_back(row);
    }

    KDE();
    output_grid();
    return 0;
}

