##Clase 13 octubre, R



## EJERCICIO 1

#Tenemos 5 experimentos con 20 corridas de mediciones de la velocidad de la luz.

#¿Cómo exponen los resultados?
  library(MASS)
  library(ggplot2)
  vl <- data.frame(michelson)

  ggplot(vl, aes(Speed, fill=Expt)) +
    geom_histogram(binwidth = 100) + xlab ("Run") +
    ylab("Speed") + facet_grid(~Expt) +
    theme(legend.position = "none")

#¿Los resultados se ven equivalentes entre los experimentos?
    ##  Los resultados no son equivalentes porque van a tener 
    ##  diferentes deistribuciones para cada experimento


## EJERCICIO 2

#¿Qué dice este gráfico de barras?
  ggplot(Pima.tr2, aes(type))+geom_bar()
  help("Pima.tr2") #Para ver qué es la base de datos 
  #Base de datos de mujeres con diabetes, la gráfica nos dice cuántas mujeres
  #tiene y cuántas no tienen diabetes

#¿Por qué la parte superior izquierda está vacía?
  ggplot(Pima.tr2, aes(age,npreg))+geom_point()
  #npr es número de embarazos
  #porque las mujeres de 20 años o menos tienen menos embarazos

  
##EJERCICIO 3
head(data.frame(Titanic))
library(dplyr)
#¿Qué se les ocurre para graficar todo?
ggplot
  
#¿Cuántos pasajeros en total viajaban por clase?
data.frame(Titanic)%>% group_by(Class) %>% summarise(count=sum(Freq))
  
#Exploren una por una las otras variables categóricas del dataset
  
