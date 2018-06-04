#include <iostream>
using namespace std;
#include <Eigen/Core>

/**
 * 把一个大矩阵左上角3×3的部分取出来，赋值为单位阵。
 **/
int main(int argc, char** argv)
{
  Eigen::Matrix<int, 9, 9>matrix_99;
  // Initialize to 0
  matrix_99 = Eigen::MatrixXi::Zero(9, 9);
  cout<<matrix_99<<endl;
  // use () access element in the matrix
  for(int i=0, j;i<3;i++)
  {
    j = i;
    matrix_99(i,j) = 1;
  }
  
   cout<<"--------------------------"<<endl;
   cout<<matrix_99<<endl;
}