# PYWLwg - IDEAM
## Python Water Level warning generator IDEAM


Fecha:       13-12-2020
Versión:     En desarrollo
Referencias: 
 * [Sanchez Lozano, 2021](https://www.doi.org/10.3390/hydrology8020071)
 * [darly Rojas](https://github.com/DarllyRojas)
 * [IDEAM](http://www.ideam.gov.co)
 * [GEOGloWS Streamflow ECMWF](https://geoglows.ecmwf.int)
 * [Centro Internacional de Agricultura Tropical](https://ciat.cgiar.org/?lang=es)
 * [Servir-Amazonia](https://servir.ciat.cgiar.org/?lang=es)


## Objetivo
A partir de los datos observados de los niveles del agua en los diferentes ríos
de Colombia obetnidas a partir de las estaciones de propiedad del IDEAM y las 
correcciones generadas a los resultados de caudales simulados por el modelo 
GEOGloWS Streamflows ECMWF Service y la metodologia propuesta por [Sanchez Lozano, 2021](https://www.doi.org/10.3390/hydrology8020071),
se presenta la libreria desarrollada para la generación de alertas respecto a la
navegabilidad de los principales cauces del país.


### Lista de tareas
- [x] Crear repositorio
- [ ] Automatizar deascarga/lectura de la información secundaria (series de niveles,
	  pronostico de niveles, perfiles de río, etc.).
- [ ] Implementar metodologia de (Sanches Lozano, 2021)
- [ ] Análizar resultados obtenidos.
- [ ] Plantear ejemplo de la herramienta.
- [ ] Dar por finalizada la herramienta.

Instalación
-----------
En desarrollo.

Uso de la herramienta
---------------------
En desarrollo.

Licencia
--------
En desarrollo.

Organizacion del proyecto
-------------------------
    .
    ├── README.md
    ├── LICENSE
    ├── setup.py            <- setup script compatible con pip
    ├── environment.yml     <- YML-file para configurar el conda environment
    ├── docs                <- Documentación
        ├── ...             <- Archivos de la documentación
    ├── examples            <- Jupyter notebooks con ejemplos de la API
        ├── ...             <- Folder con archivos para ejecutar el ejemplo.
    ├── pyorc               <- Libreria
        ├── ...             <- Funciones de la API

