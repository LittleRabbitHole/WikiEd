library(survminer)
library(survival)
library(KMsurv)
library(coxme)
require(lme4)
#####
##after semester comparison
#####
setwd("/Users/Ang/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data")
setwd("/Users/angli/ANG/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data")

#####after semester 2 way comparison#############
###retention######
#user_data = read.csv("retention_final_control_comp.csv")#2df_effort_afterSemester_RR_allvars
user_data = read.csv("2df_retention_afterSemester_RR.csv")#2df_effort_afterSemester_RR_allvars
colnames(user_data)
user_data[is.na(user_data)] <- 0

user_data$class_size_log= log(user_data$class_size + 0.1)
user_data$article_edit_log= log(user_data$article_count + 0.1)
user_data$talk_count_log= log(user_data$talk_count + 0.1) 
user_data$usertalk_count_log= log(user_data$usertalk_count + 0.1)
user_data$unique_articles_log= log(user_data$unique_articles + 0.1)
user_data$user_count_log= log(user_data$user_count + 0.1)
user_data$ave_sizediff_norm= scale(user_data$ave_sizediff,center = TRUE, scale = TRUE)
user_data$SurvObj <- with(user_data, Surv(time_index, death == 1))


##comparison of survival: control vs students
model2a1 <- coxme(SurvObj ~ article_edit_log + talk_count_log + usertalk_count_log+ score_diff
                  + user_count_log + unique_articles_log +class_size_log + ave_sizediff_norm
                  + control_wikied  + individual_group
                  + (1|courseID),
                  ties = "breslow",
                  data = user_data)
summary(model2a1) 
AIC(model2a1) 

model2a1 <- coxph(SurvObj ~ article_edit_log + talk_count_log + usertalk_count_log+ score_diff
                  + user_count_log + unique_articles_log +class_size_log + ave_sizediff_norm
                  + control_wikied  + individual_group
                  + cluster(courseID),
                  #ties = "breslow",
                  data = user_data)
summary(model2a1) 
AIC(model2a1) 


###### after semester edits and edit size
user_data = read.csv("2df_effort_afterSemester_RR.csv")
colnames(user_data)
user_data$class_size_log= log(user_data$class_size + 0.1)
user_data$article_edit_log= log(user_data$article_count + 0.1)
user_data$talk_count_log= log(user_data$talk_count + 0.1) 
user_data$usertalk_count_log= log(user_data$usertalk_count + 0.1)
user_data$unique_articles_log= log(user_data$unique_articles + 0.1)
user_data$user_count_log= log(user_data$user_count + 0.1)
user_data$ave_sizediff_norm= scale(user_data$ave_sizediff,center = TRUE, scale = TRUE)
user_data$SurvObj <- with(user_data, Surv(time_index, death == 1))

user_data$after_article_edits_log= log(user_data$after_article_edits + 0.1)
user_data$after_article_size= scale(user_data$after_article_size,center = TRUE, scale = TRUE)
#write.csv(user_data, "2df_effort_afterSemester_RR_for_spss.csv")

##after class edit
user_data$wiki_students_vs_control = as.factor(user_data$control_wikied)
user_data$group_vs_individual = as.factor(user_data$individual_group)
user_data$group_vs_individual_control = as.factor(user_data$individual_group_control)

med1.fit <- lmer(after_article_edits_log ~ wiki_students_vs_control + class_size_log+(1|courseID), data = user_data)
summary(med1.fit)

med1.fit <- lmer(after_article_edits_log ~ group_vs_individual + class_size_log+(1|courseID), data = user_data)
summary(med1.fit)

med1.fit <- lmer(after_article_edits_log ~ group_vs_individual_control + class_size_log+(1|courseID), data = user_data)
summary(med1.fit)


med1.fit <- lm(after_article_edits_log ~ wiki_students_vs_control + group_vs_individual + class_size_log, data = user_data)
summary(med1.fit)

##after class edit size
med2.fit <- lmer(after_article_size ~ wiki_students_vs_control + class_size_log+(1|courseID), data = user_data)
summary(med2.fit)

med1.fit <- lmer(after_article_size ~ group_vs_individual + class_size_log+(1|courseID), data = user_data)
summary(med1.fit)

med1.fit <- lmer(after_article_size ~ group_vs_individual_control + class_size_log+(1|courseID), data = user_data)
summary(med1.fit)

#####
#Nested regression for students
setwd("/Users/Ang/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data/shareData")
setwd("/Users/angli/ANG/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data/shareData")


#######only for students part##
data=read.csv("student_details_wikied_bot.csv")
colnames(data)
data$numofstu_log = log(data$numofstu +0.1)
data$out_stu_log = log(data$out_stu +0.1)
data$out_bot_log = log(data$out_bot +0.1)
data$out_wikied_log = log(data$out_wikied +0.1)
data$out_wikipedians_log = log(data$out_wikipedians +0.1)
data$in_stu_log = log(data$in_stu +0.1)
data$in_bot_log = log(data$in_bot +0.1)
data$in_wikied_log = log(data$in_wikied +0.1)
data$in_wikipedians_log = log(data$in_wikipedians +0.1)
write.csv(data, "log_communication_v2.csv",na = "" ,row.names = FALSE)

#log_communication = read.csv("log_communication.csv")
#colnames(log_communication)
log_communication = data[c("SID", "courseID", "out_stu","out_wikied","out_bot","out_wikipedians","in_stu","in_wikied","in_bot" ,"in_wikipedians")]

#user_data = read.csv("retention_0427.csv")#"user_data_studnets_0617.csv"
user_data = read.csv("retenion_students_2.csv")#"user_data_studnets_0617.csv"
user_data[is.na(user_data)] <- 0
user_data = user_data[which(user_data$newcomers==1),]
summary(user_data$newcomers)
colnames(user_data)

###merge with communication
merge_data = merge(user_data, log_communication, by=c("SID", "courseID"))
merge_data[is.na(merge_data)] <- 0
colnames(merge_data)
write.csv(merge_data, "studen_retention_communication_RR.csv",na = "" ,row.names = FALSE)
write.csv(merge_data, "studen_retention_communication_RR_v2.csv",na = "" ,row.names = FALSE)

#####start analysis
#user_data = read.csv("studen_retention_communication_RR.csv")
user_data = read.csv("studen_retention_communication_RR_v2.csv")
user_data[is.na(user_data)] <- 0
user_data = user_data[which(user_data$newcomers==1),]

user_data$SurvObj <- with(user_data, Surv(time_index, death == 1))

user_data$article_edit_log= log(user_data$article_edit + 0.1)
user_data$talk_count_log= log(user_data$talk_count + 0.1) 
user_data$usertalk_count_log= log(user_data$usertalk_count + 0.1)
user_data$unique_articles_log= log(user_data$unique_articles + 0.1)
user_data$user_count_log= log(user_data$user_count + 0.1)
user_data$student_count_log= log(user_data$student_count + 0.1)
user_data$edit_count_log = log(user_data$edit_count + 0.1)
user_data$ave_sizediff_norm= scale(user_data$ave_sizediff,center = TRUE, scale = TRUE)
user_data$score_diff[which(is.na(user_data$score_diff))] = 0

user_data$reach_out_stu_log = log(user_data$reach_out_stu + 0.1)
user_data$reach_out_wiki_log = log(user_data$reach_out_wiki + 0.1)
user_data$reach_in_stu_log = log(user_data$reach_in_stu +0.1)
user_data$reach_in_wiki_log = log(user_data$reach_in_wiki + 0.1)

user_data$out_stu_log = log(user_data$out_stu +0.1)
user_data$out_bot_log = log(user_data$out_bot +0.1)
user_data$out_wikied_log = log(user_data$out_wikied +0.1)
user_data$out_wikipedians_log = log(user_data$out_wikipedians +0.1)
user_data$in_stu_log = log(user_data$in_stu +0.1)
user_data$in_bot_log = log(user_data$in_bot +0.1)
user_data$in_wikied_log = log(user_data$in_wikied +0.1)
user_data$in_wikipedians_log = log(user_data$in_wikipedians +0.1)
user_data$group_group = as.factor(user_data$group_group)

user_data$courseID = as.factor(user_data$courseID)
summary(user_data$courseID)
length(unique(user_data$courseID))

#write.csv(user_data, "user_data_retention_for_spss.csv")
####new communication
model2a1 <- coxme(SurvObj ~ reach_out_stu_log + out_wikied_log + out_wikipedians_log #+ out_bot_log
                  + reach_in_stu_log +  in_wikied_log + in_wikipedians_log #+ in_bot_log
                  + group_group 
                  + score_diff
                  + article_edit_log 
                  + talk_count_log 
                  #+ usertalk_count_log
                  + user_count_log+unique_articles_log + ave_sizediff_norm
                  + student_count_log  
                  + (1|courseID),
                  ties = "breslow",
                  data = user_data)
summary(model2a1) #305043.2
AIC(model2a1) #0.029


model2a2 <- coxph(SurvObj ~ reach_out_stu_log + out_wikied_log + out_wikipedians_log 
                  + reach_in_stu_log +  in_wikied_log + in_wikipedians_log 
                  + grouping
                  #+ group_group 
                  + score_diff
                  + cluster(courseID)
                  + talk_count_log +usertalk_count_log
                  + article_edit_log + user_count_log+unique_articles_log + ave_sizediff_norm + student_count_log, 
                  data = user_data)
summary(model2a2) #0.029
AIC(model2a) #286720


####old communication
model2a1 <- coxme(SurvObj ~ article_edit_log + talk_count_log + usertalk_count_log+ score_diff
                  + user_count_log + unique_articles_log + ave_sizediff_norm +student_count_log + (1|courseID), 
                  data = user_data)
summary(model2a1) #r-square: 0.018
extractAIC(model2a1) 

model2a1 <- coxme(SurvObj ~ reach_out_stu_log + reach_out_wiki_log + reach_in_stu_log + reach_in_wiki_log
                 + group_group + score_diff
                 + article_edit_log + talk_count_log 
                 + usertalk_count_log
                 + user_count_log+unique_articles_log + ave_sizediff_norm
                 + student_count_log  
                 + (1|courseID),
                 #refine.n=500,
                 ties = "breslow",
                 #varlist = coxmeFull(collapse = TRUE),
                  #+ (1|courseID) + (1|student_count_log), ties = c("efron", "breslow")
                 data = user_data)
summary(model2a1) #305043.2
AIC(model2a1) #0.029


model2a2 <- coxph(SurvObj ~ reach_out_stu_log + reach_out_wiki_log + reach_in_stu_log + reach_in_wiki_log
                 + grouping + score_diff
                 + cluster(courseID)
                 + article_edit_log + talk_count_log +usertalk_count_log+ user_count_log+unique_articles_log + ave_sizediff_norm + student_count_log, 
                 data = user_data)
summary(model2a2) #0.029
AIC(model2a) #286720

anova(model2a1, model2a2)

#mediation
require(lme4)
user_data = read.csv("One_monthdeath_mediation.csv")
colnames(user_data)

merge_data = merge(user_data, log_communication, by=c("SID", "courseID"))
merge_data[is.na(merge_data)] <- 0
colnames(merge_data)
write.csv(merge_data, "One_monthdeath_mediation_communication_RR.csv",na = "" ,row.names = FALSE)

user_data = read.csv("One_monthdeath_mediation_communication_RR.csv")
user_data$article_edit_log= log(user_data$article_edit + 0.1)
user_data$talk_count_log= log(user_data$talk_count + 0.1) 
user_data$usertalk_count_log= log(user_data$usertalk_count + 0.1)
user_data$unique_articles_log= log(user_data$unique_articles + 0.1)
user_data$user_count_log= log(user_data$user_count + 0.1)
user_data$student_count_log= log(user_data$student_count + 0.1)
user_data$ave_sizediff_norm= scale(user_data$ave_sizediff,center = TRUE, scale = TRUE)

user_data$reach_out_stu_log = log(user_data$reach_out_stu + 0.1)
user_data$reach_out_wiki_log = log(user_data$reach_out_wiki + 0.1)
user_data$reach_in_stu_log = log(user_data$reach_in_stu + 0.1)
user_data$reach_in_wiki_log = log(user_data$reach_in_wiki + 0.1)

user_data$out_stu_log = log(user_data$out_stu +0.1)
user_data$out_bot_log = log(user_data$out_bot +0.1)
user_data$out_wikied_log = log(user_data$out_wikied +0.1)
user_data$out_wikipedians_log = log(user_data$out_wikipedians +0.1)
user_data$in_stu_log = log(user_data$in_stu +0.1)
user_data$in_bot_log = log(user_data$in_bot +0.1)
user_data$in_wikied_log = log(user_data$in_wikied +0.1)
user_data$in_wikipedians_log = log(user_data$in_wikipedians +0.1)

user_data$group_group = as.factor(user_data$group_group)
user_data = user_data[which(user_data$newcomer==1),]
user_data[is.na(user_data)] <- 0

write.csv(user_data, "One_monthdeath_mediation_log_RR_v2.csv",row.names = FALSE)
