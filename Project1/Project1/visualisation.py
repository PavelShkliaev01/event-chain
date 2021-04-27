#include <iostream>
#include <cmath>
#include <cfloat>
#include <vector>
#include <fstream>
#include <string>
#include <cstdlib>
using namespace std;

#define PI 3.14159265    

const double inf = DBL_MAX;


const double r = 0.5;
const double tg60 = tan(60 * PI / 180);
const double box_1 = 10;
const double box_2 = 13.89244;
const int n = 32;



int main()
{
    //box_1 - длинна лежащей на оси X стороны параллелограмма, box_2 - длинна второй стороны параллелограмма

    ofstream out;

    int num = 0;

    string strnum = "0";

    double box_y = (sqrt(3) * box_2) / 2;//Находим координаты по оси Y точек верхней грани параллелограмма, паралельной оси X.

    vector<pair<double, double>> vec = { {1.,1.},{5.,0.5},{7.,0},{9.,0.5},{3.,2.1},{5.,2.5},{7.5,2.5},{10.,2.},{3.,4.},
        {5.5,4.5},{9.,4.},{4.,6.},{7.,6.},{9.5,6.},{12.,5.},{6.,8.},{8.,9.},{10.,8.},{12.,9.},{13.,7.},{15.,9.},{7.,11.},{10.,11.},{14.,11.},
        {7.5,4.5},{8.5,10.5},{12,10.5},{11.5,7},{8.,7.5},{11,4},{2.5,1},{10,9.5}
    };

    double Zero_distance_to_go = 40;

    srand(time(0));

    int cur_particle = rand() % n;//Случайным образом выбираем частицу, которая будет двигаться (n - кол-во частиц).
    //cur_particle = 9;
    double cur_particle_x = vec[cur_particle].first;

    double cur_particle_y = vec[cur_particle].second;//Записываем координаты частицы, которая будет двигаться. 

    int rand_angle = rand() % 2; //Случайным образом выбираем направление движения.

    for (int i = 0; i < n; i++) {//Проверяем, что все частицы лежат внутри параллелограмма.

        if ((vec[i].second > box_y) || (vec[i].second < 0) || (vec[i].first < vec[i].second / sqrt(3))
            || (vec[i].first > vec[i].second / sqrt(3) + box_1)) {
          
            cout << "The particle "<< i << " is outside the parallelogram.";
            
            return 0; 
        }
    }
    //rand_angle = 1;

    if (rand_angle == 0) {//Если начинаем двигаться под углом 0 градусов к положительному направлению оси X.

        
        while (Zero_distance_to_go > 0) {//Пока параметр полного смещения минус суммарный пройденный путь > 0.

            strnum = to_string(num);//Записываем координаты частиц в файл.

            out.open("!output" + strnum + ".dat");

            for (int i = 0; i < n; i++)
            {   
                out << vec[i].first / 20 << ' ' << vec[i].second / 20 << endl;
            }

            out.close();

            num++;

            vec.erase(vec.begin() + cur_particle);//Удаляем частицу, которая будет смещаться из массива частиц.

            double Distance_to_next_event = inf;// Считаем, что расстояние до ближайшей частицы это бесконечность. 

            int next_particle = cur_particle;

            for (int i = 0; i < n - 1; i++) {

                double Collision_distance = inf;// Считаем, что расстояние до текущей частицы это бесконечность.

                double Distance_to_line = abs(vec[i].second - cur_particle_y);

                if (min(Distance_to_line, box_y - Distance_to_line) < 2 * r) {//Если расстояние по оси y меньше 2-ух радиусов,то частицы предположительно могут столкнуться.


                    double distance_x = vec[i].first - cur_particle_x;//Вычисляем расстояние по оси X.

                    if (distance_x < 0) {
                        distance_x += box_1;
                    }

                    Collision_distance = distance_x - sqrt(pow(2 * r, 2) - pow(vec[i].second - cur_particle_y, 2));//Находим путь который пройдет частица до столкновения.

                    //Если параметр полного смещения минус сумарный пройденный путь и текщее найденное расстояние до ближайшего столкновения
                    // больше чем расстояние до текущей частицы
                    if (Collision_distance < min(Zero_distance_to_go, Distance_to_next_event)) {

                        Distance_to_next_event = Collision_distance;//Считаем найденный путь расстоянием до ближайщей частицы.

                        next_particle = i;//Записываем номер частицы, которая предположительно будет двигаться дальше.
                    }
                }
            }

            double Distance = min(Zero_distance_to_go, Distance_to_next_event);

            double fraction = cur_particle_x - cur_particle_y / sqrt(3) + Distance;

            while (fraction >= box_1) {
                fraction -= box_1;
            }

            cur_particle_x = cur_particle_y / sqrt(3) + fraction;//Считаем новую X координату частицы.

            vec.push_back(make_pair(cur_particle_x, cur_particle_y));//Возвращаем частицу, которая двигалась, в вектор.

            if (Zero_distance_to_go < Distance_to_next_event) {//Если параметр полного смещения без пройденного пути меньше,
            //чем расстояние до ближайшего столкновения. 
              
                break;//Прерываем выполнение цикла.
                
            }
            else {//Иначе.
                Zero_distance_to_go -= Distance;//Вычитаем из парамметра без суммы смещениий смещения пройденный путь. 

                cur_particle = next_particle;//Записываем частицу, которая будет двигаться далее. 
                
                cur_particle_x = vec[cur_particle].first;

                cur_particle_y = vec[cur_particle].second;
               
            }

        }
    }

    if (rand_angle == 1) {//Если начинаем двигаться под углом 60 градусов к положительному направлению оси X.

     

        while (Zero_distance_to_go > 0) {//Пока параметр полного смещения минус суммарный пройденный путь > 0.

            strnum = to_string(num);//Записываем текущие координаты частиц в файл.

            out.open("!output" + strnum + ".dat");

            for (int i = 0; i < n; i++)
            {
                out << vec[i].first / 20 << ' ' << vec[i].second / 20 << endl;
            }

            out.close();

            num++;

            vec.erase(vec.begin() + cur_particle);//Удаляем частицу, которая будет смещаться из массива частиц.

            double Distance_to_next_event = inf;// Считаем, что расстояние до ближайшей частицы это бесконечность. 

            int next_particle = cur_particle;

            for (int i = 0; i < n - 1; i++) {

                double Collision_distance = inf;// Считаем, что расстояние до текущей частицы это бесконечность.

                //Находим расстояние от центра текущей частицы до прямой, по которой движется частица.
                double Distance_to_line = abs(tg60 * vec[i].first - vec[i].second + cur_particle_y - tg60 * cur_particle_x) / 2;

                Distance_to_line = min(Distance_to_line, sqrt(3) * box_1 / 2 - Distance_to_line);

                if (Distance_to_line < 2 * r) {//Если расстояние меньше 2-ух радиусов,то частицы предположительно могут столкнуться.

                    //Находим путь который пройдет частица до столкновения.
                    double dist = sqrt(pow(cur_particle_x - vec[i].first, 2) + pow(cur_particle_y - vec[i].second, 2) - pow(Distance_to_line, 2));

                    if (cur_particle_y > vec[i].second) {
                        dist = box_2 - dist;
                    }

                    Collision_distance = dist - sqrt(4 * pow(r, 2) - pow(Distance_to_line, 2));
                    //Если параметр полного смещения минус сумарный пройденный путь и текщее найденное расстояние до ближайшего столкновения
                    // больше чем расстояние до текущей частицы
                    if (Collision_distance < min(Zero_distance_to_go, Distance_to_next_event)) {

                        Distance_to_next_event = Collision_distance;//Считаем найденный путь расстоянием до ближайщей частицы.

                        next_particle = i;//Записываем номер частицы, которая предположительно будет двигаться дальше.
                    }
                }
            }

            double Distance = min(Zero_distance_to_go, Distance_to_next_event);

            double fraction = sqrt(pow(cur_particle_y / tg60, 2) + pow(cur_particle_y, 2)) + Distance;

            while (fraction >= box_2) {
                fraction -= box_2;
            }

            //Считаем новые координаты частицы
            double temp_cur_particle_y = tg60 * (cur_particle_x - cur_particle_y / tg60 + fraction / 2) + cur_particle_y - tg60 * cur_particle_x;

            double temp_cur_particle_x = cur_particle_x - cur_particle_y / tg60 + fraction / 2;

            cur_particle_x = temp_cur_particle_x;
            cur_particle_y = temp_cur_particle_y;
            vec.push_back(make_pair(cur_particle_x, cur_particle_y));//Возвращаем частицу, которая двигалась, в вектор.

            if (Zero_distance_to_go < Distance_to_next_event) {//Если параметр полного смещения без пройденного пути меньше,
            //чем расстояние до ближайшего столкновения. 

                Zero_distance_to_go = 0;

                break;//Прерываем выполнение цикла.
            }
            else {//Иначе.
                Zero_distance_to_go -= Distance_to_next_event;//Вычитаем из парамметра смещения без сумарного пройденного пути пройденный путь. 
                
                cur_particle = next_particle;//Записываем частицу, которая будет двигаться далее. 

                cur_particle_x = vec[cur_particle].first;

                cur_particle_y = vec[cur_particle].second;
            }
        }
    }


    strnum = to_string(num);//Записываем конечное положение частиц в файл.

    out.open("!output" + strnum + ".dat");
    for (int i = 0; i < n; i++)
    {

        out << vec[i].first / 20 << ' ' << vec[i].second / 20 << endl;
    }

    out.close();

    system("python visualisation.py");
    return 0;
}




















