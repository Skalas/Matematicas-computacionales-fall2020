data(vlt, package="DAAG")
library(dplyr)
library(ggplot2)
library(tidyr)
library(ggplot2movies)

vlt %>%
    pivot_longer(cols = starts_with('window'), names_to="window", values_to = "figure") %>%
    group_by(window, figure) %>%
    summarise(n=n()) %>%
    ggplot(aes(x=figure, weight=n, fill = window)) +
    facet_wrap(~window) +
    geom_bar()
    
movies %>%
    pivot_longer(
        cols = c(Action, Animation, Comedy, Drama, Documentary, Romance, Short),
        names_to="category", values_to = "figure") %>%
    data.frame() %>%
    head()


vlt %>%
    group_by(window1) %>%
    summarise(n = n())

vlt %>%
    group_by(window2) %>%
    summarise(n = n())

vlt %>%
    group_by(window3) %>%
    summarise(n = n()) %>%
    ggplot(aes(weight=n)) +
    aes(window3)+geom_bar(fill='blue')
    


data(Cars93, package="MASS")

Cars93 %>%
    mutate(inverse= 1/MPG.city) %>%
    ggplot(aes(x=Horsepower, y = inverse)) +
    geom_point()
