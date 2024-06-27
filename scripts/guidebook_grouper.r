# From a list of creatures, group based on archetype (area) and other
# criteria to create "regional pages" in the guidebook
library(tidyverse)
input_file <- "./out/random_creatures.csv"
tbl <- read_delim(input_file, delim = ",")
tbl <- tbl %>%
  group_by(Archetype1, ProgressionPath, Family1) %>%
  arrange(.by_group = TRUE)

# Write grouped output
output_file <- "./out/grouped_creatures.csv"
write_delim(tbl, output_file, delim = ",")
