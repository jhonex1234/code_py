#include <conio.h> 
#include <stdio.h> 
#include <stdlib.h> 
void main() 
{//variables con valores: 
//1 Dólar USA = 0,4871 Libra esterlina 
//1 Libra esterlina = 2,0530 Dólar USA 
//1 US Dólar = 10.78018 México - Peso 
//1 México - Peso (MXN) = 0.09276 US Dólar (USD) 
// => 1 dolar= peso_a_dolar*dolar_libra= 0.09276*0.4871=0.045183 
float dolar_a_peso=2777.77778 ; 
float peso_a_libra=0,0002535; 
int opcion; 
int n; 
bool repet=true; 
char resp; 
while(repet==true) 
{clrscr(); 
cout<<"Ingresar opcion"<<endl<<endl; 
cout<<"[1].- De dolar a peso"<<endl; 
cout<<"[2].- De peso a libra esterlina"<<endl<<endl; 
cout<<"Ingrese opcion: ";cin>>opcion; 
clrscr(); 
if(opcion==1||opcion==2) 
{ 
cout<<"CANTIDAD A CAMBIAR"<<endl<<endl; 
cout<<"Ingrese cantidad a cambiar: ";cin>>n; 
}//fin del if-opcion 
cout<<endl<<endl; 
switch (opcion) 
{ 
case 1 : cout<<"CAMBIO DE DOLARES A PESOS"<<endl<<endl; 
cout<<n<<" dolares = "<<(n*dolar_a_peso)<< "pesos"; 
getche(); 
break; 
case 2 : cout<<"CAMBIO DE PESOS A LIBRAS"<<endl<<endl; 
cout<<n<<" pesos = "<<(n*peso_a_libra)<< "libras esterlinas"; 
getche(); 
break; 
default: cout<<"Error en escoger opcion"; getche(); 
}//fin del switch 
cout<<endl<<endl<<"Desea continuar?[Y/N]: ";cin>>resp; 
if(resp=='N'||resp=='n'||resp=='Y'||resp=='y') 
{ 
cout<<"Bye"; repet=false; 
}//fin del if-resp 
}//fin del while-repet 
} 