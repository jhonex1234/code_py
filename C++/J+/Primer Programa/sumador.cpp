/*
cout //salida 
cin //entrada
*/

#include <iostream>
#include <stdio.h>
using namespace std;
int main()
{
	printf("bienvenido al program de suma de dos valores");

	int a;
	int b;
	int suma;
	

	cout << "\n ingrese numero a:";
	cin >> a;
	cout <<"\n ingrese numero b:";
	cin >> b;
	suma = a + b;
	cout << "\n la suma de "<<a<<"+"<<b<<" es:"<<suma;

	Return 0;
}