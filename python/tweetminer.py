mport newt,csv,tweepy
import networkx as nx

#the term we're going to search for
tag='ddj'
#how many tweets to search for (max 1500)
num=500

##Something along lines of:
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(SKEY, SSECRET)
api = tweepy.API(auth, cache=tweepy.FileCache('cache',cachetime), retry_errors=[500], retry_delay=5, retry_count=2)

#You need to do some work here to search the Twitter API
tweeters, tweets=yourSearchTwitterFunction(api,tag,num)
#tweeters is a list of folk who tweeted the term of interest
#tweets is a list of the Twitter tweet objects returned from the search
#My code for this is tightly bound up in a large and rambling library atm...

#Put tweets into chronological order
tweets.reverse()

#I was being lazy and wasn't sure what vars I needed or what I was trying to do when I started this!
#The whole thing really needs rewriting...
tweepFo={}
seenToDate=set([])
uniqSourceFo=[]
#runtot is crude and doesn't measure overlap
runtot=0
oldseentodate=0

#Construct a digraph from folk using the tag to their followers
DG=nx.DiGraph()

for tweet in tweets:
	user=tweet['from_user']
	if user not in tweepFo:
		tweepFo[user]=[]
		print "Getting follower data for", str(user), str(len(tweepFo)), 'of', str(len(tweeters))
		mi=tweepy.Cursor(api.followers_ids,id=user).items()
		userID=tweet['from_user_id'] #check
		DG.add_node(userID,label=user)
		for m in mi:
			tweepFo[user].append(m)
			#construct graph
			DG.add_edge(userID,m,weight=1)
			DG.node[m]['label']=''
		ufc=len(tweepFo[user])
		runtot=runtot+ufc
		#seen to date is all people who have seen so far, plus new ones, so it's the union
		oldseentodate=len(seenToDate)
		seenToDate=seenToDate.union(set(tweepFo[user]))
		uniqSourceFo.append((tweet['created_at'],len(seenToDate),user,runtot,ufc,oldseentodate))
	else:
		#I'm weighting the edges so we can count how many times folk see the hashtag
		if len(DG.edges(userID))>0:
			tmp1,tmp2=DG.edges(userID)[0]
			weight=DG[userID][tmp2]['weight']+1
			for fromN,toN in DG.edges(userID):
				DG[fromN][toN]['weight']=weight


fo='reports/tmp/'+tag+'_ncount.csv'
f=open(fo,'wb+')
writer=csv.writer(f)
writer.writerow(['datetime','count','newuser','crudetot','userFoCount','previousCount'])
for ts,l,u,ct,ufc,ols in uniqSourceFo:
	print ts,l
	writer.writerow([ts,l,u,ct,ufc,ols])

f.close()

print "Writing graph.."
filter=[]
for n in DG:
	if DG.degree(n)>1: filter.append(n)
filter=set(filter)
H=DG.subgraph(filter)
nx.write_graphml(H, 'reports/tmp/'+tag+'_ncount_2up.graphml')
print "Writing other graph.."
nx.write_graphml(DG, 'reports/tmp/'+tag+'_ncount.graphml')
