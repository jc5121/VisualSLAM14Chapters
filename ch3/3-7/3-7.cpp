#include <iostream>
using namespace std;
#include <Eigen/Core>
#include <Eigen/Geometry>

int main(int argc, char** argv)
{
  Eigen::Quaterniond q1(0.35, 0.2, 0.3, 0.1);
  Eigen::Matrix<double, 3, 1> t1;
  t1 << 0.3, 0.1, 0.1;
  Eigen::Quaterniond q2(-0.5, 0.4, -0.1, 0.2);
  Eigen::Matrix<double, 3, 1> t2;
  t2 << -0.1, 0.5, 0.3;
  Eigen::Matrix<double, 3, 1> p1;
  p1 << 0.5, 0, 0.2;
  
  cout<<"q1 =\n"<<q1.coeffs()<<endl;
  cout<<"t1 =\n"<<t1<<endl;
  cout<<"q2 =\n"<<q2.coeffs()<<endl;
  cout<<"t2 =\n"<<t2<<endl;
  cout<<"p1 =\n"<<p1<<endl;
  
  //归一化
  q1 = q1.normalized();
  q2 = q2.normalized();
  cout<<"q1 after normalized:\n"<<q1.coeffs()<<endl;
  cout<<"q2 after normalized:\n"<<q2.coeffs()<<endl;
  
  //根据q1和t1计算Tc1w
  Eigen::Matrix3d q1rotation_matrix = Eigen::Matrix3d::Identity();//单位阵
  q1rotation_matrix = q1.toRotationMatrix();
  Eigen::Isometry3d Tc1w = Eigen::Isometry3d::Identity();//虽然为3d，实际上是4×4矩阵，齐次坐标
  Tc1w.rotate(q1rotation_matrix);
  Tc1w.pretranslate(t1);
  
  //根据q2和t2计算Tc2w
  Eigen::Matrix3d q2rotation_matrix = Eigen::Matrix3d::Identity();//单位阵
  q2rotation_matrix = q2.toRotationMatrix();
  Eigen::Isometry3d Tc2w = Eigen::Isometry3d::Identity();//虽然为3d，实际上是4×4矩阵，齐次坐标
  Tc2w.rotate(q2rotation_matrix);
  Tc2w.pretranslate(t2);
  
  //计算p2
  Eigen::Matrix<double, 3, 1> pw = Tc1w.inverse()*p1;
  Eigen::Matrix<double, 3, 1> p2 = Tc2w*pw;
  
  cout<<"The loc of p1 in c1 = \n"<<p1<<endl;
  cout<<"The loc of pw in world = \n"<<pw<<endl;
  cout<<"The loc of p2 in c2 = \n"<<p2<<endl;
  
  
  return 0;
}