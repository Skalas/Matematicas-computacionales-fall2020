if(!require(dplyr, quietly = TRUE, warn.conflicts = FALSE) ){
    install.packages('dplyr',
                     dependencies = TRUE, 
                     repos = "http://cran.us.r-project.org")
}
    if(!require(nycflights13, quietly = TRUE, warn.conflicts = FALSE) ){
        install.packages('nycflights13', 
	    dependencies = TRUE, 
	    repos = "http://cran.us.r-project.org")
    }


flights %>%
    group_by(carrier, month) %>%
    summarise(
        delay = mean(dep_delay, na.rm = TRUE)
    ) %>%
    arrange(desc(delay))
