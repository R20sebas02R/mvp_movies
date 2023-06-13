LINK DEL PLANTEAMIENTO DE LA PROBLEMATICA Y REQUERIMIENTOS --> https://github.com/HX-PRomero/PI_ML_OPS/blob/main/Readme.md

# ¿Para que sirve este proyecto?, ¿Que es lo que hace?

El proyecto consiste en implementar una API de consultas particulares, en otras palabras, se utiliza Render (un sitio web donde puedes 'hacer funcionar' tu repositorio de github) y FastAPI (un framework) para deployar este repositorio. El resultado sera una pagina web donde podras realizar consultas (ingresando un valor en cada funcion y que cada una de estas te devuelvan sus resultados en funcion de la logica implementada en tu repo). 

- ¿Como se hace? 
Basicamente tienes que tener un archivo main.py en el directorio raiz de tu proyecto, donde estara implementado la logica de tus funciones y ademas tendras que utilizar un framework que te permita implementar la estructura de API (en este caso utilice FastAPI), en otras, esto significa intanciar el framework de FasAPI (la libreria de Python), colocarle un decorador a cada funcion y asegurarse de que el retorno de cada funcion este en formato Json (en el main.py). Ya teniendo el main.py en tu repo, render te facilitara el proceso de deployar tu proyecto ya que solamente debes indicarle que tipo de API vas a hacer (en este caso es un sitio web), debes añadirle el link de github de tu repositorio y llenar un formulario.
    --> LINK DE TUTORIAL: https://github.com/HX-FNegrete/render-fastapi-tutorial


# ¿Como se ha logrado 'hacer funcionar' este proyecto?

El proceso para responder a esta pregunta es el siguiente:
    - Explicar la naturaleza del proyecto (mas detalles de en que consiste el proyecto)
    - Explicar a grandes rasgos el procesamiento de la data, las decisiones tomadas y la implementacion.

- ¿De que trata el proyecto?, ¿Que es lo que se trata de solucionar?
    - Bueno la idea es existe una necesidad critica por parte de una empresa. Se ha solicitado un MVP (Minimum Viable Product, Producto Minimo Viable) y el tiempo maximo de espera es de una semana. En este MVP se requiere que sea posible consumir una API. Esta API debe responder a 7 necesidades (6 funciones + 1 sistema de recomendacion de peliculas). Para ello nos ha proporcionado una data.

- Guia respecto al Proceso de Implementacion:
    - Tenemos una data (.csv) que hemos transformado en ETL.ipynb (auxiliar_functions_transformations.py y transformations.py son archivos finales por asi decirlo (mas limpios), en cambio ETL.ipynb es un archivo mas ameno para la visualizacion del proceso). Los resultados de este archivo son: 'data_procesada.csv' (el archivo con las transformaciones particulares sugeridas (por temas de espacio estara alojada en googleDrive)) + actores.json (para la funcion 5) + directores.json (para la funcion 6).
    - En el ML.ipynb determinamos que caracteristicas o columnas vamos a considerar para el ML (la implementacion del sistema de recomendacion). El resultado sera un notebook con los analisis realizados para determinar que caracteristicas son las mas utiles + 'data_consultas.csv' (el archivo con lo justo para poder responder a las consultas en la API (funciones 1, 2, 3, 4) + ML).
    - En el main.py hemos implementado la logica de nuestras funciones y la hemos cimentado a partir de la libreria FastAPI de python para su posterior deployment en Render.
</n>
    **NOTA:**
    Algo que puede resultar interesante de añadir es respecto al sistema de recomendacion, en particular,el criterio que utilice para las recomendaciones de mi modelo (igual los detalles estan en el ML.ipynb): 
    - Una vez que ingresamos el titulo, vamos iterando sobre todos los titulos y vamos a determinar un valor que indica la semejanza entre el titulo ingresado y el titulo actual en la iteracion ¿Como se determina este valor de similitud? Bueno, lo que he hecho es separar en 'k < numero_columnas' grupos de columnas y he concluido son grupos altamente independientes (variables independientes). En cada grupo he calculado el valor de similitud entre los dos vectores (utilizando la similitud de Jaccard). y luego he multiplicado cada valor devuelto (porque asumi que son conjuntos independientes (casi)) y el resultado corresponde al grado de similitud entre ambos films o titulos (0 si no se parecen en nada y 1 si se trata del mismo film). Sin embargo, uno podria preguntarse ¿Y por que tomarse el trabajo de dividir las columnas en grupos si al final va a utilizar la similitud de Jaccard para cada grupo? Bueno el hecho es que cada grupo corresponde a una caracteristica fundamental del film, entonces si bien es cierto que utilizo en esencia la similitud de Jaccard para todos los grupos, tambien es menester conocer que este criterio se utiliza con ciertas variantes para cada grupo. 




