require(ColonyTrack)

setwd("C:/Users/fonte/OneDrive/Desktop/Projects/MiceTrack")
dataFiles = list("Data/MiceData.csv")
subjectFile = "ColonyTrackFiles/SubjectInfo.tsv"
networkFile = "ColonyTrackFiles/CageNetwork.tsv"
eventsFile = "ColonyTrackFiles/Events.tsv"

data = read_data(dataFiles, subjectFile, networkFile, eventsFile)

days = "all"
drop.days = NULL
subjects = "all"
drop.subjects = NULL
metrics = calculate_metrics(data, days = days, drop.days = drop.days, subjects = subjects,
drop.subjects = drop.subjects, log=TRUE)

save(data, file = "Data/ColonyTrackData.RData")
save(metrics, file = "Data/ColonyTrackMetrics.RData")