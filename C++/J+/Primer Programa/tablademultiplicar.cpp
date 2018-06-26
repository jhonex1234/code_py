

#include <iostream>
#include <stdio.h>
using namespace std;
int main() 
{

    printf("bienvenido al programa de tablas de multiplicar");

    float a;
    float b;
    int multiplicacion;

    cout << "\n ingrese numero a:";
	cin >> a;
    if(a<9){
    	
    	a=a;

    }else{
    	cout << "este numero debe ser menor a 9";
    	cin >> a;
    }
	cout <<"\n ingrese numero b:";
	cin >> b;

	multiplicacion = a * b;

	cout << "\n la multiplicacion de "<<a<<"*"<<b<<" es:"<<multiplicacion<<endl; 

	return 0;

}



	
