El código guarda video en formato MP4 en la tarjeta SD, además de muestras del ADC del pin A0 a una tasa de muestreo de 2 kHz, de acuerdo a distintos parámetros de configuración. 
Los parámetros de interés para el usuario son dos:
- length: duración de cada archivo de video en segundos.
- no_files: cantidad de archivos de video a grabar.
Por ejemplo, en caso de seleccionar length = 30 y no_files = 3, se tendrá un tiempo de grabación total de length * no_files = 30*3 = 90 segundos dividido en tres archivos.
Si bien la grabación se detiene luego de que el tiempo estipulado ya ha pasado, la lectura del ADC continúa hasta que se desconecte el dispositivo.
Actualmente el nombre de los archivos se define en la línea 68. Se debe cuidar cambiar el nombre para evitar sobreescribir video en caso de no desearlo.
