/*este programa esta destinado a calcular el valor de un producto X añadiendo el Iva correspondiente*/

#include <iostream>
#include <stdio.h>
using namespace std;

int main(){

  int precio, multiplicacion =0; //variable que identifica el precio del producto
  float iva= 1.21; // 
  
    cout << "\n ingrese precio:";
    cin>>precio;
    multiplicacion = precio*iva;
    cout << "\n el resultado es  "<<precio<<"*"<<iva<<" es:"<<multiplicacion<<endl;
    return 0;
}