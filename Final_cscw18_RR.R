library(survminer)
library(survival)
library(KMsurv)
library(coxme)
require(lme4)



####teahouse edit comparison
setwd("/Users/Ang/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data/shareData/FinalShare")
setwd("/Users/angli/ANG/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data/finalRevise/final/datafanalysis/")

final = read.csv("matched_teahouse_semester_RR_v1.csv")
colnames(final)
final = read.csv("matched_teahouse_after_RR_v1.csv")

final$class_size_log= log(final$class_size + 0.1)
final$article_edit_log= log(final$article_count + 0.1)
final$article_sizediff_norm= scale(final$article_sizediff,center = TRUE, scale = TRUE)

final$wiki_students_vs_control = as.factor(final$control_students)
summary(final$wiki_students_vs_control)#-2:3674    1:4155 

####edits

med1.fit <- lmer(article_edit_log ~ wiki_students_vs_control + class_size_log + (1|courseID), data = final)
summary(med1.fit)

####edit size
med1.fit <- lmer(article_sizediff_norm ~ wiki_students_vs_control + class_size_log+(1|courseID), data = final)
summary(med1.fit)


###teahouse retention 2 way comparison####
data = read.csv("TH_students_retention_comp_RR.csv")
data$wiki_students_vs_control = as.factor(data$control_students)
data$group_vs_individual = as.factor(data$group_individual)
data$group_vs_individual_control = as.factor(data$group_control)

user_data = data
colnames(user_data)

user_data$class_size_log= log(user_data$class_size + 0.1)
user_data$article_edit_log= log(user_data$article_count + 0.1)
user_data$talk_count_log= log(user_data$talk_count + 0.1) 
user_data$usertalk_count_log= log(user_data$usertalk_count + 0.1)
user_data$unique_articles_log= log(user_data$unique_articles + 0.1)
user_data$user_count_log= log(user_data$user_count + 0.1)
user_data$ave_sizediff_norm= scale(user_data$ave_sizediff,center = TRUE, scale = TRUE)
user_data$SurvObj <- with(user_data, Surv(time_index, death == 1))


model2a1 <- coxme(SurvObj ~ wiki_students_vs_control + class_size_log + (1|courseID),
                  ties = "breslow",
                  data = user_data)
summary(model2a1) 

model2a <- coxph(SurvObj ~ wiki_students_vs_control + class_size_log  + cluster(courseID),
                 data = user_data)
summary(model2a) 


####
#####after semester 2 way comparison with random control #############
###retention######
user_data = read.csv("2df_retention_afterSemester_RR.csv")
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

###### after semester edits and edit size, comparison with random control
user_data = read.csv("2df_effort_afterSemester_RR_2.csv")

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
write.csv(user_data, "2df_effort_afterSemester_RR.csv")

exp(mean(user_data$after_article_edits_log[which(user_data$wiki_students_vs_control == 1)]))
exp(mean(user_data$after_article_edits_log[which(user_data$wiki_students_vs_control == -2)]))

summary(user_data$group_vs_individual_control)
exp(mean(user_data$after_article_edits_log[which(user_data$group_vs_individual_control == 0)]))
exp(mean(user_data$after_article_edits_log[which(user_data$group_vs_individual_control == 1)]))


med1.fit <- lmer(after_article_edits_log ~ wiki_students_vs_control + class_size_log+(1|courseID), data = user_data)
summary(med1.fit)

med1.fit <- lmer(after_article_edits_log ~ group_vs_individual + class_size_log+(1|courseID), data = user_data)
summary(med1.fit)

med1.fit <- lmer(after_article_edits_log ~ group_vs_individual_control + class_size_log+(1|courseID), data = user_data)
summary(med1.fit)


##after class edit size
med2.fit <- lmer(after_article_size ~ wiki_students_vs_control + class_size_log+(1|courseID), data = user_data)
summary(med2.fit)

med1.fit <- lmer(after_article_size ~ group_vs_individual + class_size_log+(1|courseID), data = user_data)
summary(med1.fit)

med1.fit <- lmer(after_article_size ~ group_vs_individual_control + class_size_log+(1|courseID), data = user_data)
summary(med1.fit)

#####Hypothesis 2, interactions
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

model2a1 <- coxph(SurvObj ~ #reach_out_stu_log + reach_out_wiki_log + reach_in_stu_log + reach_in_wiki_log
                  #+ grouping 
                  + score_diff
                  + cluster(courseID)
                  + article_edit_log + talk_count_log +usertalk_count_log+ user_count_log+unique_articles_log + ave_sizediff_norm + student_count_log, 
                  data = user_data)
summary(model2a1) #0.029
AIC(model2a) #286720


model2a2 <- coxph(SurvObj ~ reach_out_stu_log + reach_out_wiki_log + reach_in_stu_log + reach_in_wiki_log
                  + grouping + score_diff
                  + cluster(courseID)
                  + article_edit_log + talk_count_log +usertalk_count_log+ user_count_log+unique_articles_log + ave_sizediff_norm + student_count_log, 
                  data = user_data)
summary(model2a2) #0.029
AIC(model2a) #286720

