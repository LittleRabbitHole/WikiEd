library(survminer)
library(survival)
library(KMsurv)
library(coxme)
require(lme4)
require(lmerTest)

setwd("/Users/angli/ANG/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data/finalRevise/final/datafanalysis/")

####During semester#######
user_data = read.csv("duringSocialization_effort_retention.csv")
colnames(user_data)
user_data[is.na(user_data)] <- 0

user_data$control_wikied = as.factor(user_data$control_wikied)
summary(user_data$control_wikied)
user_data$indiv_group = as.factor(user_data$indiv_group)

user_data$class_size_log= log(user_data$class_size + 0.1)
user_data$article_edit_log= log(user_data$article_count + 0.1)
user_data$talk_count_log= log(user_data$talk_count + 0.1) 
user_data$usertalk_count_log= log(user_data$usertalk_count + 0.1)
user_data$unique_articles_log= log(user_data$unique_article_numbers + 0.1)
user_data$user_count_log= log(user_data$user_count + 0.1)
user_data$ave_sizediff_norm= scale(user_data$ave_sizediff,center = TRUE, scale = TRUE)
user_data$article_sizediff_norm= scale(user_data$article_sizediff,center = TRUE, scale = TRUE)
user_data$SurvObj <- with(user_data, Surv(dayindex, death == 1))

user_data$article_edits_log= log(user_data$article_count + 0.1)

##effort##

medfit <- lmer(article_edits_log ~ indiv_group + control_wikied + class_size_log + (1|courseID), data = user_data)
medfit <- lmer(article_edits_log ~ control_wikied  + class_size_log + (1|courseID), data = user_data)
summary(medfit)
ls_means(medfit, pairwise=TRUE)

# (group > individual/control, control < indiv/group)

##retention##
model2a1 <- coxph(SurvObj ~ article_edit_log + talk_count_log + usertalk_count_log
                  + user_count_log + unique_articles_log +class_size_log + ave_sizediff_norm
                  + control_wikied  
                  + indiv_group
                  + cluster(courseID),
                  #ties = "breslow",
                  data = user_data)
summary(model2a1) 
AIC(model2a1) 


####after semester#######
user_data = read.csv("afterSocialization_effort_retention.csv")
colnames(user_data)
user_data[is.na(user_data)] <- 0

user_data$control_wikied = as.factor(user_data$control_wikied)
user_data$indiv_group = as.factor(user_data$indiv_group)

user_data$class_size_log= log(user_data$class_size + 0.1)
user_data$article_edit_log= log(user_data$article_count + 0.1)
user_data$talk_count_log= log(user_data$talk_count + 0.1) 
user_data$usertalk_count_log= log(user_data$usertalk_count + 0.1)
user_data$unique_articles_log= log(user_data$unique_article_numbers + 0.1)
user_data$user_count_log= log(user_data$user_count + 0.1)
user_data$ave_sizediff_norm= scale(user_data$ave_sizediff,center = TRUE, scale = TRUE)
user_data$SurvObj <- with(user_data, Surv(dayindex, death == 1))

user_data$article_edits_log= log(user_data$article_count + 0.1)

##effort##

med1.fit <- lmer(article_edits_log ~ indiv_group + control_wikied + class_size_log + (1|courseID), data = user_data)
summary(med1.fit)
ls_means(medfit, pairwise=TRUE)
medfit <- lmer(article_edits_log ~ control_wikied  + class_size_log + (1|courseID), data = user_data)
ls_means(medfit)

# (control < indiv/group)

##retention##
model2a1 <- coxph(SurvObj ~ #article_edit_log + talk_count_log + usertalk_count_log
                  #+ user_count_log + unique_articles_log  + ave_sizediff_norm +
                    class_size_log
                  + control_wikied  
                  + indiv_group
                  + cluster(courseID),
                  #ties = "breslow",
                  data = user_data)
summary(model2a1) 
AIC(model2a1) 



####only students interaction####
user_data = read.csv("duringSocializationCommunication.csv")
user_data[is.na(user_data)] <- 0
#user_data = user_data[which(user_data$return==0),]

colnames(user_data)

user_data$SurvObj <- with(user_data, Surv(dayindex, death == 1))

user_data$article_edit_log= log(user_data$article_count + 0.1)
user_data$talk_count_log= log(user_data$talk_count + 0.1) 
user_data$usertalk_count_log= log(user_data$usertalk_count + 0.1)
user_data$unique_articles_log= log(user_data$unique_article_numbers + 0.1)
user_data$user_count_log= log(user_data$user_count + 0.1)
user_data$student_count_log= log(user_data$class_size + 0.1)
user_data$edit_count_log = log(user_data$edit_count + 0.1)
user_data$ave_sizediff_norm= scale(user_data$ave_sizediff,center = TRUE, scale = TRUE)
user_data$score_diff[which(is.na(user_data$score_diff))] = 0


user_data$reach_out_stu_log = log(user_data$reach_out_stu + 0.1)
user_data$reach_out_wiki_log = log(user_data$reach_out_wiki + 0.1)
user_data$reach_in_stu_log = log(user_data$reach_in_stu +0.1)
user_data$reach_in_wiki_log = log(user_data$reach_in_wiki + 0.1)


user_data$group_group = as.factor(user_data$indiv_group)
summary(user_data$group_group)

user_data$courseID = as.factor(user_data$courseID)
length(unique(user_data$courseID))

model2a1 <- coxph(SurvObj ~ #reach_out_stu_log + reach_out_wiki_log + reach_in_stu_log + reach_in_wiki_log
                    #+ group_group 
                  score_diff
                  + cluster(courseID)
                  + article_edit_log + talk_count_log +usertalk_count_log+ user_count_log+unique_articles_log + ave_sizediff_norm + student_count_log, 
                  data = user_data)
summary(model2a1) 


model2a2 <- coxph(SurvObj ~ reach_out_stu_log + reach_out_wiki_log + reach_in_stu_log + reach_in_wiki_log
                  + group_group 
                  + score_diff
                  + article_edit_log + talk_count_log +usertalk_count_log+ user_count_log+unique_articles_log + ave_sizediff_norm + student_count_log
                  + cluster(courseID), 
                  data = user_data)
summary(model2a2) #0.029
AIC(model2a) #286720


