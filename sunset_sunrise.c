#include <math.h>
#include <stdio.h>
#include <time.h>
#define PI 3.1415926
#define ZENITH -.83

float calculateSunrise(int year,int month,int day,float lat, float lng,int localOffset, int daylightSavings, int sunrise) {
    /*
    localOffset will be <0 for western hemisphere and >0 for eastern hemisphere
    daylightSavings should be 1 if it is in effect during the summer otherwise it should be 0
    */
    //1. first calculate the day of the year
    float N1 = floor(275 * month / 9);
    float N2 = floor((month + 9) / 12);
    float N3 = (1 + floor((year - 4 * floor(year / 4) + 2) / 3));
    float N = N1 - (N2 * N3) + day - 30;

    //2. convert the longitude to hour value and calculate an approximate time
    float lngHour = lng / 15.0;

    float t;
    if (sunrise) 
        t = N + ((6 - lngHour) / 24);   //if rising time is desired:
    else
        t = N + ((18 - lngHour) / 24);   //if setting time is desired:

    //3. calculate the Sun's mean anomaly   
    float M = (0.9856 * t) - 3.289;

    //4. calculate the Sun's true longitude
    float L = fmod(M + (1.916 * sin((PI/180)*M)) + (0.020 * sin(2 *(PI/180) * M)) + 282.634,360.0);

    //5a. calculate the Sun's right ascension      
    float RA = fmod(180/PI*atan(0.91764 * tan((PI/180)*L)),360.0);

    //5b. right ascension value needs to be in the same quadrant as L   
    float Lquadrant  = floor( L/90) * 90;
    float RAquadrant = floor(RA/90) * 90;
    RA = RA + (Lquadrant - RAquadrant);

    //5c. right ascension value needs to be converted into hours   
    RA = RA / 15;

    //6. calculate the Sun's declination
    float sinDec = 0.39782 * sin((PI/180)*L);
    float cosDec = cos(asin(sinDec));

    //7a. calculate the Sun's local hour angle
    float cosH = (sin((PI/180)*ZENITH) - (sinDec * sin((PI/180)*lat))) / (cosDec * cos((PI/180)*lat));
    /*   
    if (cosH >  1) 
    the sun never rises on this location (on the specified date)
    if (cosH < -1)
    the sun never sets on this location (on the specified date)
    */

    //7b. finish calculating H and convert into hours
    float H;
    if (sunrise) 
        H = 360 - (180/PI)*acos(cosH);   //   if if rising time is desired:
    else
        H = (180/PI)*acos(cosH); //   if setting time is desired:      
    H = H / 15;

    //8. calculate local mean time of rising/setting      
    float T = H + RA - (0.06571 * t) - 6.622;

    //9. adjust back to UTC
    float UT = fmod(T - lngHour, 24.0);
    //10. convert UT value to local time zone of latitude/longitude
    return UT + localOffset + daylightSavings;

    }

int main(int argc, char** argv){
    time_t t = time(NULL);
    struct tm tm = *localtime(&t);
    printf("%s\n", getenv("JETSON_ID"));
    printf("now: %d-%02d-%02d %02d:%02d:%02d\n", tm.tm_year + 1900, tm.tm_mon + 1, tm.tm_mday, tm.tm_hour, tm.tm_min, tm.tm_sec);
    int year, month, day;
    year = tm.tm_year + 1900;
    month = tm.tm_mon + 1;
    day = tm.tm_mday;
    // (int year,int month,int day,float lat, float lng,int localOffset, int daylightSavings, int sunrise)
    float localT = fmod(24 + calculateSunrise(year, month, day, atof(argv[1]), atof(argv[2]), 1, 0, atoll(argv[3])), 24.0);
    double hours;
    float minutes = modf(localT,&hours)*60;
    printf("%.0f:%.0f\n",hours,minutes);
}