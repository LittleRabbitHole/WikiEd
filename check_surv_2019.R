library(ggfortify)

library(survminer)
library(survival)
library(KMsurv)

setwd("/Users/jiajunluo/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data/finalRevise/final/datafanalysis/")
setwd("/Users/angli/ANG/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data/finalRevise/final/datafanalysis/")

user_data = read.csv("afterSocialization_effort_retention_v2.csv")
user_data = read.csv("students_AfterSemester_contri_aggre_censor_170601.csv")
user_data = read.csv("retention_170301.csv")

user_data = na.omit(user_data)


#user_data = user_data[which(user_data$return==0),]
colnames(user_data)
#user_data[is.na(user_data)] <- 0

user_data$class_size_log= log(user_data$class_size + 0.1)

user_data$indiv_group = as.factor(user_data$indiv_group)
summary(user_data$indiv_group)

user_data$SurvObj <- with(user_data, Surv(dayindex, death == 1))

model2a1 <-coxph(SurvObj ~ #article_edit_log + talk_count_log + usertalk_count_log
                   #+ user_count_log + unique_articles_log  + ave_sizediff_norm +
                   class_size_log
                 + indiv_group
                 + cluster(courseID),
                 #ties = "breslow",
                 data = user_data)

summary(model2a1) 


model2a1 <-coxph(SurvObj ~ #article_edit_log + talk_count_log + usertalk_count_log
                   #+ user_count_log + unique_articles_log  + ave_sizediff_norm +
                   class_size_log
                 + indiv_group
                 +control_wikied
                 + cluster(courseID),
                 #ties = "breslow",
                 data = user_data)

summary(model2a1) 
