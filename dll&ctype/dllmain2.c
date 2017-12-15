/* Replace "dll.h" with the name of your header */
#include "dll.h"
#include <windows.h>

DLLIMPORT void HelloWorld()
{
	MessageBox(0,"Hello World from DLL!\n","Hi",MB_ICONINFORMATION);
}

DLLIMPORT void foo(int **a,int **b,int m, int n) //二维数组用**，定列数时可用a[][n],一维直接a[] 
{
   int i,j;
   for ( i=0; i<m; i++ )   
   {
     for ( j=0; j<n; j++ )
	 	//*((float*)a + n*i + j)=*((float*)a + n*i + j)*2;
	 	*((int*)b + n*i + j)=*((int*)a + n*i + j)*2; //根据地址写数组元素，注意其中的dtype类型 
	}
}

BOOL WINAPI DllMain(HINSTANCE hinstDLL,DWORD fdwReason,LPVOID lpvReserved)
{
	switch(fdwReason)
	{
		case DLL_PROCESS_ATTACH:
		{
			break;
		}
		case DLL_PROCESS_DETACH:
		{
			break;
		}
		case DLL_THREAD_ATTACH:
		{
			break;
		}
		case DLL_THREAD_DETACH:
		{
			break;
		}
	}
	
	/* Return TRUE on success, FALSE on failure */
	return TRUE;
}
