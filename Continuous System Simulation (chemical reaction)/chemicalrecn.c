#include <stdio.h>
#include<stdlib.h> 
#include<math.h>

int main() {
    FILE *fp;
    fp = fopen("lab1.txt", "w");  // write the output data to lab1.txt
    if (fp == NULL) {
        printf("Error opening file!\n");
        return 1;
    }

    printf("Simulating reaction.....");

    double t = 0.0;
    double dt = 0.001;
    double time = 100.0; // time represents the total reaction time and t represents loop time, that increases by dt
    double k1 = 0.025, k2 = 0.01;// k1 k2 are the constants
    double c1[1000], c2[1000], c3[1000]; // C1 C2 C3 are the amount of chemicals Ch1 Ch2 Ch3
    int i = 0;


    // Initial concentrations(Amount of chemicals Ch1 Ch2 Ch3 at time 0)
    c1[0] = 70.0;
    c2[0] = 35.0;
    c3[0] = 0.0;

    while (t <= time) { // this represents the amount of change in ch1 ch2 ch3 with respect to dt time
        c1[i + 1] = c1[i] + (k2 * c3[i] - k1 * c1[i] * c2[i]) * dt;  
        c2[i + 1] = c2[i] + (k2 * c3[i] - k1 * c1[i] * c2[i]) * dt;
        c3[i + 1] = c3[i] + 2.0 * (k1 * c1[i] * c2[i] - k2 * c3[i]) * dt;

        fprintf(fp, "\n%f %f %f", c1[i], c2[i], c3[i]);

        i = i + 1;  // i increases by 1
        t = t + dt; // and t increases by dt time
    }

    fclose(fp);
    return 0;
}