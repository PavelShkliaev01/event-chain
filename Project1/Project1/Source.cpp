#include <iostream>
#include <cmath>
#include <cfloat>
#include <vector>
#include <fstream>
#include <string>
//#include <cstdlib>
using namespace std;

#define PI 3.14159265    

const double inf = DBL_MAX;


const double r = 0.5;
const double tg60 = tan(60 * PI / 180);
const double box_1 = 10;
const double box_2 = 13.89244;
const int n = 8;



int main()
{
    //box_1 - ������ ������� �� ��� X ������� ���������������, box_2 - ������ ������ ������� ���������������

    ofstream out;

    int num = 0;

    string strnum = "0";

    double box_y = (sqrt(3) * box_2) / 2;//������� ���������� �� ��� Y ����� ������� ����� ���������������, ����������� ��� X.

    vector<pair<double, double>> vec = { {1.,1.},{3.,1.2},{4.,1.6},{5.,8.},{8.1,8.1},{10.,10.},{6.,10.},{6.5,5.5} };

    double Zero_distance_to_go = 18;

    srand(time(0));

    int cur_particle = rand() % n;//��������� ������� �������� �������, ������� ����� ��������� (n - ���-�� ������).

    double cur_particle_x = vec[cur_particle].first;

    double cur_particle_y = vec[cur_particle].second;//���������� ���������� �������, ������� ����� ���������. 

    int rand_angle = rand() % 2; //��������� ������� �������� ����������� ��������.


    for (int i = 0; i < n; i++) {//���������, ��� ��� ������� ����� ������ ���������������.

        if ((vec[i].second > box_y) || (vec[i].second < 0) || (vec[i].first < vec[i].second / sqrt(3))
            || (vec[i].first > vec[i].second / sqrt(3) + box_1)) {
          
            cout << "The particle "<< i << " is outside the parallelogram.";
            
            return 0; 
        }
    }

    if (rand_angle == 0) {//���� �������� ��������� ��� ����� 0 �������� � �������������� ����������� ��� X.

        for (int i = 0; i < n; i++)//���������, ��� ���������� ����� �������� ������ ��� �� ������ �������� <2r.
        {
            for (int j = i + 1; j < n; j++) {

                double distance_between_centers = sqrt(pow((vec[i].first - vec[j].first), 2)
                    + pow((vec[i].second - vec[j].second), 2));

                if (min(distance_between_centers, box_1 - distance_between_centers) < 2 * r) {
                    cout << "The distance between the centers of particles " << i <<
                    " and " << j << " < 2*r.";

                    return 0;
                }
            }
        }

        while (Zero_distance_to_go > 0) {//���� �������� ������� �������� ����� ��������� ���������� ���� > 0.

            strnum = to_string(num);//���������� ���������� ������ � ����.

            out.open("!output" + strnum + ".dat");

            for (int i = 0; i < n; i++)
            {   
                out << vec[i].first / 20 << ' ' << vec[i].second / 20 << endl;
            }

            out.close();

            num++;

            vec.erase(vec.begin() + cur_particle);//������� �������, ������� ����� ��������� �� ������� ������.

            double Distance_to_next_event = inf;// �������, ��� ���������� �� ��������� ������� ��� �������������. 

            int next_particle = cur_particle;

            for (int i = 0; i < n - 1; i++) {

                double Collision_distance = inf;// �������, ��� ���������� �� ������� ������� ��� �������������.

                double Distance_to_line = abs(vec[i].second - cur_particle_y);

                if (min(Distance_to_line, box_y - Distance_to_line) < 2 * r) {//���� ���������� �� ��� y ������ 2-�� ��������,�� ������� ���������������� ����� �����������.


                    double distance_x = vec[i].first - cur_particle_x;//��������� ���������� �� ��� X.

                    if (distance_x < 0) {
                        distance_x += box_1;
                    }

                    Collision_distance = distance_x - sqrt(pow(2 * r, 2) - pow(vec[i].second - cur_particle_y, 2));//������� ���� ������� ������� ������� �� ������������.

                    //���� �������� ������� �������� ����� �������� ���������� ���� � ������ ��������� ���������� �� ���������� ������������
                    // ������ ��� ���������� �� ������� �������
                    if (Collision_distance < min(Zero_distance_to_go, Distance_to_next_event)) {

                        Distance_to_next_event = Collision_distance;//������� ��������� ���� ����������� �� ��������� �������.

                        next_particle = i;//���������� ����� �������, ������� ���������������� ����� ��������� ������.
                    }
                }
            }

            double Distance = min(Zero_distance_to_go, Distance_to_next_event);

            double fraction = cur_particle_x - cur_particle_y / sqrt(3) + Distance;

            while (fraction >= box_1) {
                fraction -= box_1;
            }

            cur_particle_x = cur_particle_y / sqrt(3) + fraction;//������� ����� X ���������� �������.

            vec.push_back(make_pair(cur_particle_x, cur_particle_y));//���������� �������, ������� ���������, � ������.

            if (Zero_distance_to_go < Distance_to_next_event) {//���� �������� ������� �������� ��� ����������� ���� ������,
            //��� ���������� �� ���������� ������������. 
              
                break;//��������� ���������� �����.
                
            }
            else {//�����.
                Zero_distance_to_go -= Distance;//�������� �� ���������� ��� ����� ��������� �������� ���������� ����. 

                cur_particle = next_particle;//���������� �������, ������� ����� ��������� �����. 
                
                cur_particle_x = vec[cur_particle].first;

                cur_particle_y = vec[cur_particle].second;
               
            }

        }
    }

    if (rand_angle == 1) {//���� �������� ��������� ��� ����� 60 �������� � �������������� ����������� ��� X.

        for (int i = 0; i < n; i++)//���������, ��� ���������� ����� �������� ������ ��� �� ������ �������� <2r.
        {
            for (int j = i + 1; j < n; j++) {

                double distance_between_centers = sqrt(pow((vec[i].first - vec[j].first), 2)
                + pow((vec[i].second - vec[j].second), 2));

                if (min(distance_between_centers, box_2 - distance_between_centers) < 2 * r) {
                    
                    cout << "The distance between the centers of particles " << i <<
                    " and " << j << "< 2*r.";

                    return 0;
                }
            }
        }

        while (Zero_distance_to_go > 0) {//���� �������� ������� �������� ����� ��������� ���������� ���� > 0.

            strnum = to_string(num);//���������� ������� ���������� ������ � ����.

            out.open("!output" + strnum + ".dat");

            for (int i = 0; i < n; i++)
            {
                out << vec[i].first / 20 << ' ' << vec[i].second / 20 << endl;
            }

            out.close();

            num++;

            vec.erase(vec.begin() + cur_particle);//������� �������, ������� ����� ��������� �� ������� ������.

            double Distance_to_next_event = inf;// �������, ��� ���������� �� ��������� ������� ��� �������������. 

            int next_particle = cur_particle;

            for (int i = 0; i < n - 1; i++) {

                double Collision_distance = inf;// �������, ��� ���������� �� ������� ������� ��� �������������.

                //������� ���������� �� ������ ������� ������� �� ������, �� ������� �������� �������.
                double Distance_to_line = abs(tg60 * vec[i].first - vec[i].second + cur_particle_y - tg60 * cur_particle_x) / 2;

                Distance_to_line = min(Distance_to_line, sqrt(3) * box_1 / 2 - Distance_to_line);

                if (Distance_to_line < 2 * r) {//���� ���������� �� ��� y ������ 2-�� ��������,�� ������� ���������������� ����� �����������.

                    //������� ���� ������� ������� ������� �� ������������.
                    double dist = sqrt(pow(cur_particle_x - vec[i].first, 2) + pow(cur_particle_y - vec[i].second, 2) - pow(Distance_to_line, 2));

                    if (cur_particle_y > vec[i].second) {
                        dist = box_2 - dist;
                    }

                    Collision_distance = dist - sqrt(4 * pow(r, 2) - pow(Distance_to_line, 2));
                    //���� �������� ������� �������� ����� �������� ���������� ���� � ������ ��������� ���������� �� ���������� ������������
                    // ������ ��� ���������� �� ������� �������
                    if (Collision_distance < min(Zero_distance_to_go, Distance_to_next_event)) {

                        Distance_to_next_event = Collision_distance;//������� ��������� ���� ����������� �� ��������� �������.

                        next_particle = i;//���������� ����� �������, ������� ���������������� ����� ��������� ������.
                    }
                }
            }

            double Distance = min(Zero_distance_to_go, Distance_to_next_event);

            double fraction = sqrt(pow(cur_particle_y / tg60, 2) + pow(cur_particle_y, 2)) + Distance;

            while (fraction >= box_2) {
                fraction -= box_2;
            }

            //������� ����� ���������� �������
            double temp_cur_particle_y = tg60 * (cur_particle_x - cur_particle_y / tg60 + fraction / 2) + cur_particle_y - tg60 * cur_particle_x;

            double temp_cur_particle_x = cur_particle_x - cur_particle_y / tg60 + fraction / 2;

            cur_particle_x = temp_cur_particle_x;
            cur_particle_y = temp_cur_particle_y;
            vec.push_back(make_pair(cur_particle_x, cur_particle_y));//���������� �������, ������� ���������, � ������.

            if (Zero_distance_to_go < Distance_to_next_event) {//���� �������� ������� �������� ��� ����������� ���� ������,
            //��� ���������� �� ���������� ������������. 

                Zero_distance_to_go = 0;

                break;//��������� ���������� �����.
            }
            else {//�����.
                Zero_distance_to_go -= Distance_to_next_event;//�������� �� ���������� �������� ��� ��������� ����������� ���� ���������� ����. 
                
                cur_particle = next_particle;//���������� �������, ������� ����� ��������� �����. 

                cur_particle_x = vec[cur_particle].first;

                cur_particle_y = vec[cur_particle].second;
            }
        }
    }


    strnum = to_string(num);//���������� �������� ��������� ������ � ����.

    out.open("!output" + strnum + ".dat");
    for (int i = 0; i < n; i++)
    {

        out << vec[i].first / 20 << ' ' << vec[i].second / 20 << endl;
    }

    out.close();

    system("python visualisation.py");
    return 0;
}




















