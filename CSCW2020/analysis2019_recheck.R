library(survminer)
library(survival)
library(KMsurv)
library(coxme)
require(lme4)
require(lmerTest)

setwd("~/data/")

user_data = read.csv("duringSocialization_effort_retention.csv")
colnames(user_data)

re_check = read.csv("re_check_2.csv")

user_data = merge(re_check, user_data,  by.x = "during", by.y = "control_wpid", all.x = TRUE)

########

user_data$control_wikied = as.factor(user_data$control_wikied)
summary(user_data$control_wikied)
user_data$indiv_group = as.factor(user_data$group_recheck)
summary(user_data$indiv_group)

user_data$WikiEd = 0
user_data$WikiEd[which(user_data$control_wikied == 1)] = 1
summary(user_data$WikiEd)


user_data$class_size_log= log(user_data$class_size + 0.1)
user_data$article_edit_log= log(user_data$article_count + 0.1)
user_data$talk_count_log= log(user_data$talk_count + 0.1) 
user_data$usertalk_count_log= log(user_data$usertalk_count + 0.1)
user_data$unique_articles_log= log(user_data$unique_article_numbers + 0.1)
user_data$user_count_log= log(user_data$user_count + 0.1)
user_data$ave_sizediff_norm= scale(user_data$ave_sizediff,center = TRUE, scale = TRUE)
user_data$article_sizediff_norm= scale(user_data$article_sizediff,center = TRUE, scale = TRUE)

user_data$article_edits_log= log(user_data$article_count + 0.1)

##effort##

medfit <- lmer(article_edits_log ~  control_wikied + class_size_log:WikiEd + (1|courseID), data = user_data)
summary(medfit)
medfit <- lmer(article_edits_log ~ indiv_group  + class_size_log:WikiEd + (1|courseID), data = user_data)
summary(medfit)
ls_means(medfit, pairwise=TRUE)


####During semester quality#######
user_data = read.csv("duringSocializationQuality_uniqueArticleUnit2.csv", stringsAsFactors=FALSE)
colnames(user_data)

user_data = merge(re_check, user_data,  by.x = "during", by.y = "wikiUsername")

user_data = user_data[c("pageid", "control_wikied", "group_recheck","start_qual_aggre",  "end_qual_aggre", "courseID","classsize" )]
user_data = unique(user_data)
colnames(user_data)

user_data$start_qual_aggre = as.numeric(as.character(user_data$start_qual_aggre))
user_data$end_qual_aggre = as.numeric(as.character(user_data$end_qual_aggre))

user_data$diff2 = user_data$end_qual_aggre - user_data$start_qual_aggre

colnames(user_data)
user_data$control_wikied = as.factor(user_data$control_wikied)
summary(user_data$control_wikied)
user_data$indiv_group = as.factor(user_data$group_recheck)
summary(user_data$indiv_group)

user_data$WikiEd = 0
user_data$WikiEd[which(user_data$control_wikied == 1)] = 1
summary(user_data$WikiEd)


user_data$class_size_log= log(user_data$classsize + 0.1)

user_data_stu = user_data[which(user_data$control_wikied==1),]
summary(user_data_stu$diff2)


medfit <- lmer(diff2 ~ control_wikied 
               + class_size_log:WikiEd + (1|courseID), data = user_data)
summary(medfit)


ls_means(medfit, pairwise=TRUE)


####after semester#######
user_data = read.csv("afterSocialization_effort_retention_v2.csv")
colnames(user_data)

user_data = merge(re_check, user_data,  by.x = "after", by.y = "control_wpid")
user_data = unique(user_data)

user_data$control_wikied = as.factor(user_data$control_wikied)
user_data$indiv_group = as.factor(user_data$indiv_group)
summary(user_data$indiv_group)

user_data$WikiEd = 0
user_data$WikiEd[which(user_data$control_wikied == 1)] = 1
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

med1.fit <- lmer(article_edits_log ~  control_wikied + class_size_log:WikiEd + (1|courseID), data = user_data)
summary(med1.fit)


##retention##

model2a1 <-coxph(SurvObj ~ 
                   class_size_log:WikiEd
                 + control_wikied  
                 #+ indiv_group
                 + cluster(courseID),
                 data = user_data)

summary(model2a1) 

