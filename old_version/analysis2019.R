library(ggfortify)

library(survminer)
library(survival)
library(KMsurv)
library(coxme)
require(lme4)
require(lmerTest)

setwd("/Users/jiajunluo/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data/finalRevise/final/datafanalysis/")
setwd("/Users/angli/ANG/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data/finalRevise/final/datafanalysis/")

####During semester#######
user_data = read.csv("duringSocialization_effort_retention.csv")
colnames(user_data)

user_data$WikiEd = 0
user_data$WikiEd[which(user_data$control_wikied == 1)] = 1
#user_data$WikiEd = as.factor(user_data$WikiEd)
summary(user_data$WikiEd)

user_data$control_wikied = as.factor(user_data$control_wikied)
summary(user_data$control_wikied)
user_data$indiv_group = as.factor(user_data$group_recheck)
summary(user_data$indiv_group)


user_data$class_size_log= log(user_data$class_size + 0.1)
user_data$article_edit_log= log(user_data$article_count + 0.1)
user_data$talk_count_log= log(user_data$talk_count + 0.1) 
user_data$usertalk_count_log= log(user_data$usertalk_count + 0.1)
user_data$unique_articles_log= log(user_data$unique_article_numbers + 0.1)
user_data$user_count_log= log(user_data$user_count + 0.1)
user_data$ave_sizediff_norm= scale(user_data$ave_sizediff,center = TRUE, scale = TRUE)
user_data$article_sizediff_norm= scale(user_data$article_sizediff,center = TRUE, scale = TRUE)
#user_data$SurvObj <- with(user_data, Surv(dayindex, death == 1))

user_data$article_edits_log= log(user_data$article_count + 0.1)

##effort##

medfit <- lmer(article_edits_log ~ indiv_group + control_wikied + class_size_log:WikiEd + (1|courseID), data = user_data)
medfit <- lmer(article_edits_log ~ control_wikied + class_size_log:WikiEd + (1|courseID), data = user_data)
summary(medfit)
medfit <- lmer(article_edits_log ~ indiv_group  + class_size_log:WikiEd + (1|courseID), data = user_data)
ls_means(medfit, pairwise=TRUE)
# 
# # (group > individual/control, control < indiv/group)
# znorm <- function(ts){
#   ts.mean <- mean(ts)
#   ts.dev <- sd(ts)
#   (ts - ts.mean)/ts.dev
# }
# 
# 
# #look at the content edit size as indication of quality
# user_data = read.csv("duringSocialization_articleSize.csv")
# colnames(user_data)
# user_data$courseID[1]
# user_data[is.na(user_data)] <- 0
# 
# user_data$control_wikied = as.factor(user_data$control_wikied)
# summary(user_data$control_wikied)
# user_data$indiv_group = as.factor(user_data$indiv_group)
# 
# user_data$class_size_log= log(user_data$class_size + 0.1)
# user_data$article_edit_log= log(user_data$article_count + 0.1)
# user_data$talk_count_log= log(user_data$talk_count + 0.1) 
# user_data$usertalk_count_log= log(user_data$usertalk_count + 0.1)
# user_data$unique_articles_log= log(user_data$unique_article_numbers + 0.1)
# user_data$user_count_log= log(user_data$user_count + 0.1)
# user_data$ave_sizediff_norm= scale(user_data$ave_sizediff,center = TRUE, scale = TRUE)
# 
# user_data$article_sizeadded_norm= scale(user_data$article_sizeadded,center = TRUE, scale = TRUE)
# summary(log(user_data$article_sizeadded+2381029))
# 
# 
# medfit <- lm(article_sizeadded ~ indiv_group+ control_wikied  + class_size_log, data = user_data)
# summary(medfit)
# ls_means(medfit, pairwise=TRUE)
# 
# hist(znorm(user_data$article_sizeadded), breaks = 100)
# hist(user_data$article_sizeadded_norm)
# 
# medfit <- lmer(znorm(user_data$article_sizediff) ~ indiv_group + control_wikied + class_size_log + (1|courseID), data = user_data)
# summary(medfit)
# ls_means(medfit, pairwise=TRUE)
# 
# 

####During semester quality#######
user_data = read.csv("duringSocializationQuality_uniqueArticleUnit2.csv", stringsAsFactors=FALSE)
#user_data = user_data[which(user_data$author_prop==1),]
colnames(user_data)

#user_data = read.csv("duringSocializationQuality_uniqueArticleUnit_share.csv", stringsAsFactors=FALSE)
user_data = user_data[c("pageid", "control_wikied", "group_recheck","start_qual_aggre",  "end_qual_aggre", "courseID","classsize" )]
user_data = unique(user_data)
colnames(user_data)

user_data$start_qual_aggre = as.numeric(as.character(user_data$start_qual_aggre))
user_data$end_qual_aggre = as.numeric(as.character(user_data$end_qual_aggre))

#user_data$start_quallevel = as.numeric(as.character(user_data$start_quallevel))
#user_data$end_quallevel = as.numeric(as.character(user_data$end_quallevel))

#user_data$diff1 = user_data$end_quallevel - user_data$start_quallevel
user_data$diff2 = user_data$end_qual_aggre - user_data$start_qual_aggre
#user_data[is.na(user_data)] <- 0
#user_data = na.omit(user_data)


colnames(user_data)
user_data$control_wikied = as.factor(user_data$control_wikied)
summary(user_data$control_wikied)
user_data$indiv_group = as.factor(user_data$group_recheck)
summary(user_data$indiv_group)

user_data$class_size_log= log(user_data$classsize + 0.1)

user_data$WikiEd = 0
user_data$WikiEd[which(user_data$control_wikied == 1)] = 1
#user_data$WikiEd = as.factor(user_data$WikiEd)
summary(user_data$WikiEd)


user_data_stu = user_data[which(user_data$control_wikied==1),]
summary(user_data_stu$diff2)


medfit1 <- lmer(diff2 ~ control_wikied 
               + class_size_log:WikiEd + (1|courseID), data = user_data)

medfit1 <- lmer(end_qual_aggre ~  control_wikied 
                + class_size_log:WikiEd + (1|courseID), data = user_data)
medfit1 <- lmer(start_qual_aggre ~ control_wikied 
                + class_size_log:WikiEd + (1|courseID), data = user_data)
summary(medfit1)
ls_means(medfit1)

0.255-0.047
medfit2 <- lmer(diff2 ~ indiv_group
               + class_size_log:WikiEd + (1|courseID), data = user_data)
summary(medfit2)

ls_means(medfit2)

medfit1 <- lmer(end_qual_aggre ~  indiv_group 
                + class_size_log:WikiEd + (1|courseID), data = user_data)
medfit1 <- lmer(start_qual_aggre ~ indiv_group 
                + class_size_log:WikiEd + (1|courseID), data = user_data)
summary(medfit1)
ls_means(medfit1)

#----

medfit1 <- lmer(start_qual_aggre ~ control_wikied 
                + class_size_log:WikiEd + (1|courseID), data = user_data)
summary(medfit1)
ls_means(medfit1)

medfit1 <- lmer(end_qual_aggre ~ start_qual_aggre + control_wikied 
                + class_size_log:WikiEd + (1|courseID), data = user_data)
summary(medfit1)
ls_means(medfit1)


medfit2 <- lmer(end_qual_aggre ~ start_qual_aggre + indiv_group
                + class_size_log:WikiEd + (1|courseID), data = user_data)
summary(medfit2)
ls_means(medfit2)

medfit2 <- lmer(start_qual_aggre ~ indiv_group
                + class_size_log:WikiEd + (1|courseID), data = user_data)
summary(medfit2)
ls_means(medfit2)


####after semester#######
user_data = read.csv("afterSocialization_effort_retention_v2.csv")
user_data = read.csv("afterSocialization_effort_retention_v2.csv")
colnames(user_data)
#user_data[is.na(user_data)] <- 0

user_data$control_wikied = as.factor(user_data$control_wikied)
#user_data$indiv_group = as.factor(user_data$indiv_group)
user_data$indiv_group = as.factor(user_data$group_recheck)
summary(user_data$indiv_group)

user_data$WikiEd = 0
user_data$WikiEd[which(user_data$control_wikied == 1)] = 1
#user_data$WikiEd = as.factor(user_data$WikiEd)
summary(user_data$WikiEd)


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

med1.fit <- lmer(article_edits_log ~ control_wikied + class_size_log:WikiEd + (1|courseID), data = user_data)
summary(med1.fit)
medfit <- lmer(article_edits_log ~ indiv_group  + class_size_log:WikiEd + (1|courseID), data = user_data)
summary(medfit)
ls_means(medfit, pairwise=TRUE)

# (control < indiv/group)

##retention##

model2a1 <-coxph(SurvObj ~ #article_edit_log + talk_count_log + usertalk_count_log
                  #+ user_count_log + unique_articles_log  + ave_sizediff_norm +
                   class_size_log:WikiEd
                  + control_wikied  
                  + indiv_group
                  + cluster(courseID),
                  #ties = "breslow",
                  data = user_data)

summary(model2a1) 

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


user_data$group_group = as.factor(user_data$group_recheck)
summary(user_data$group_group)

user_data$courseID = as.factor(user_data$courseID)
length(unique(user_data$courseID))

model2a1 <- coxph(SurvObj ~ #reach_out_stu_log + reach_out_wiki_log + reach_in_stu_log + reach_in_wiki_log
                    #+ group_group 
                  #score_diff
                  + cluster(courseID)
                  + article_edit_log + talk_count_log +usertalk_count_log+ user_count_log+unique_articles_log + ave_sizediff_norm + student_count_log, 
                  data = user_data)
summary(model2a1) 


model2a2 <- coxph(SurvObj ~ reach_out_stu_log + reach_out_wiki_log + reach_in_stu_log + reach_in_wiki_log
                  + group_group 
                  #+ score_diff
                  + article_edit_log + talk_count_log +usertalk_count_log+ user_count_log+unique_articles_log + ave_sizediff_norm + student_count_log
                  + cluster(courseID), 
                  data = user_data)
summary(model2a2) #0.029
AIC(model2a) #286720


med1.fit <- lmer(article_edit_log ~ reach_out_stu_log + reach_out_wiki_log + reach_in_stu_log + reach_in_wiki_log
                   + group_group + student_count_log 
                 + (1|courseID), data = user_data)
summary(med1.fit)


##double check

setwd("/Users/jiajunluo/GoogleDrive/GoogleDrive_Pitt_PhD/Wiki_Ed_Collaboration/Data_finalRevise")
user_data = read.csv("article_with_commu_data_log_1.csv")
colnames(user_data)
user_data$start_qual_aggre = as.numeric(as.character(user_data$start_qual_aggre))
user_data$end_qual_aggre = as.numeric(as.character(user_data$end_qual_aggre))
summary(as.factor(user_data$group_recheck))

##social interaction --> quality
medfit <- lmer(end_qual_aggre ~ start_qual_aggre 
               #+ as.factor(group_recheck) 
               + out_stu_log + in_stu_log + in_wikipedians_log + out_wikipedians_log
               + classsize_log + (1|courseID), data = user_data)
summary(medfit)
ls_means(medfit)


user_data$diff = user_data$end_qual_aggre - user_data$start_qual_aggre
## group --> quality
medfit <- lmer(end_qual_aggre ~ start_qual_aggre + as.factor(group_recheck) 
               + classsize_log + (1|courseID), data = user_data)
summary(medfit)

ls_means(medfit)

#group --> social interaction
med1.fit <- lmer(in_stu_log ~ as.factor(group_recheck) + classsize_log 
                 + (1|courseID), data = user_data)
summary(med1.fit)

med1.fit <- lmer(out_stu_log ~ as.factor(group_recheck) + classsize_log 
                 + (1|courseID), data = user_data)
summary(med1.fit)

med1.fit <- lmer(in_wikipedians_log ~ as.factor(group_recheck) + classsize_log 
                 + (1|courseID), data = user_data)
summary(med1.fit)

med1.fit <- lmer(out_wikipedians_log ~ as.factor(group_recheck) + classsize_log 
                 + (1|courseID), data = user_data)
summary(med1.fit)


med1.fit <- lmer(end_qual_aggre ~ as.factor(group_recheck) + classsize_log 
                 + (1|courseID), data = user_data)
summary(med1.fit)

##step3: 
medfit <- lmer(end_qual_aggre ~ start_qual_aggre + as.factor(group_recheck) 
               + out_stu_log + in_stu_log + in_wikipedians_log + out_wikipedians_log
               + classsize_log + (1|courseID), data = user_data)
summary(medfit)
ls_means(medfit)
