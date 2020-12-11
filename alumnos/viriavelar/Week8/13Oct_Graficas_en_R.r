library(ggplot2)


install.packages('ggthemes')

library(MASS)
vl <- data.frame(michelson)
vl

ggplot(vl, aes(Speed, fill=Expt)) +
       geom_histogram(binwidth=100) + ylab("Run") +
       xlab("Speed") + facet_grid(~Expt) +
       theme(legend.position="none")

ggplot(Pima.tr2, aes(type))+geom_bar()

help(Pima.tr2)

ggplot(Pima.tr2, aes(age,npreg))+geom_point()

head(data.frame(Titanic))

library(dplyr)

data.frame(Titanic) %>%
group_by(Class) %>%
summarise(count=sum(Freq))

library(ggplot2movies)

movies %>% 
filter(votes < 1000) %>%
ggplot(aes(votes, rating))+
geom_point()

movies %>% 
filter(votes < 1000, votes>9) %>%
ggplot(aes(votes, rating))+
geom_point()

install.packages('DAAG')

library(tidyr)

data(vlt, package="DAAG")

head(vlt)

vlt %>%
filter(prize!=0)

vlt %>%
group_by(window1) %>%
summarise(n=n())

vlt %>%
group_by(window2) %>%
summarise(n=n())

vlt %>%
group_by(window3) %>%
summarise(n=n()) %>%
ggplot(aes(weight=n))+aes(window3)+geom_bar(fill='blue')

vlt %>%
pivot_longer(cols=starts_with('window'),names_to='window',values_to='figure') %>%
group_by(window,figure) %>%
summarise(n=n())

vlt %>%
pivot_longer(cols=starts_with('window'),names_to='window',values_to='figure') %>%
group_by(window,figure) %>%
summarise(n=n()) %>%
ggplot(aes(x=figure,weight=n,fill=window, color=figure))+
facet_wrap(~window)+
geom_bar()

#### Movies

movies %>%
data.frame() %>%
head()

movies %>%
pivot_longer(cols=c(Action,Animation,Comedy,Drama,Documentary,Romance,Short),names_to='Category',values_to='figure') %>%
data.frame() %>%
head()

#Ahi muere dice el profe

data(Cars93,package='MASS')

Cars93 %>%
head()

Cars93 %>%
mutate(inverse=1/MPG.city) %>%
ggplot(aes(x=Horsepower,y=inverse)) +
geom_point()


