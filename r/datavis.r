ddj_ncount <- read.csv("~/code/twapps/newt/reports/tmp/ddj_ncount.csv")
#Convert the datetime string to a time object
ddj_ncount$ttime=as.POSIXct(strptime(ddj_ncount$datetime, "%a, %d %b %Y %H:%M:%S"),tz='UTC')

#Order the newuser factor levels into the order in which they first use the tag
dda=subset(ddj_ncount,select=c('ttime','newuser'))
dda=arrange(dda,-desc(ttime))
ddj_ncount$newuser=factor(ddj_ncount$newuser, levels = dda$newuser)

#Plot when each user first used the tag against time
ggplot(ddj_ncount) + geom_point(aes(x=ttime,y=newuser)) + opts(axis.text.x=theme_text(size=6),axis.text.y=theme_text(size=4))

#Plot the cumulative and union flavours of increasing possible audience size, as well as the difference between them
ggplot(ddj_ncount) + geom_line(aes(x=ttime,y=count,col='Unique followers')) + geom_line(aes(x=ttime,y=crudetot,col='Cumulative followers')) + geom_line(aes(x=ttime,y=crudetot-count,col='Repeated followers')) + labs(colour='Type') + xlab(NULL)

#Number of new unique followers introduced at each time step
ggplot(ddj_ncount)+geom_line(aes(x=ttime,y=count-previousCount,col='Actual delta'))

#Try to get some idea of how many of the followers of a new user are actually new potential audience members
ggplot(ddj_ncount) + opts(axis.text.x=theme_text(angle=-90,size=4)) + geom_linerange(aes(x=newuser,ymin=0,ymax=userFoCount,col='Follower count')) + geom_linerange(aes(x=newuser,ymin=0,ymax=(count-previousCount),col='Actual new audience'))

#This is still a bit experimental
#I'm playing around trying to see what proportion or number of a users followers are new to, or subsumed by, the potential audience of the tag to date...
ggplot(ddj_ncount) + geom_linerange(aes(x=newuser,ymin=0,ymax=1-(count-previousCount)/userFoCount)) + opts(axis.text.x=theme_text(angle=-90,size=6)) + xlab(NULL)
