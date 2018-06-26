/*Querido usuario ingrese el precio de su producto y se le mostrara este precio con su iva incluido*/

#include <iostream>
#include <stdio.h>
using namespace std;
int main(){

  int precio;
  float iva= 1.21;
  int multiplicacion =0;
  
    cout << "\n ingrese precio:";
    cin>>precio;
    multiplicacion = precio*iva;
    cout << "\n el resultado es  "<<precio<<"*"<<iva<<" es:"<<multiplicacion;

    return 0;

}



