import operator
import math

def AvgUser(values):
    summ=0
    count=0
    for val in values.values():
        if (val != -1):
            summ =summ+ val
            count+=1
    #т.к. у нас нет пустых строк, можно не обрабатывать случай "0/0"
    if count!=0:
        summ/=count
    return summ

#read data or context for task in dictionaries
def read(file, dictionaryUsers,strType='',week={}):
    f=open(file)
    lst=[]
    for row in f:
        lst.append(row.replace('\n','').split(', '))
    f.close()
    movies = lst[0]    
    for i in range(1,len(lst)):
        name = str(lst[i][0])
        dictionaryUsers[name] = {} 
        if (strType=='int'):
            dictionaryUsers[name]['values']= {} 
        else:
            dictionaryUsers[name]['days']= {}
        for j in range(1,len(lst[i])):
            if (strType=='int'):
                #{'User 1':{'values': {'Movie 1': 4, 'Movie 2': 4, ... }, {'avg': ...} } 
                dictionaryUsers[name]['values'][str(movies[j])]=int(lst[i][j])
            else:
                #{'User 1':{'days': {'Movie 1': 7, 'Movie 2': -1, ... }, {'avg': ...} } 
                if lst[i][j] in week:
                    dictionaryUsers[name]['days'][str(movies[j])]=week[lst[i][j]]
                else:
                    dictionaryUsers[name]['days'][str(movies[j])]=-1
        if (strType=='int'): #find AVG for every user
            dictionaryUsers[name]['avg']=AvgUser(dictionaryUsers[name]['values'])
        else:
            dictionaryUsers[name]['avg']=AvgUser(dictionaryUsers[name]['days'])

#Create similarity dict{'name_user':'simUV'} for user-argument
def Similarity(dictionaryUsers,user,key='values'):
    similarity={}
    for name in dictionaryUsers.keys():
        if name==user:
            similarity[name]=-1
        else:
            simUV = 0
            usqrt = 0
            vsqrt = 0
            for movie in dictionaryUsers[user][key].keys():
                if dictionaryUsers[user][key][movie]!=-1 and dictionaryUsers[name][key][movie]!=-1:
                    simUV+=dictionaryUsers[user][key][movie]*dictionaryUsers[name][key][movie]
                    usqrt+=dictionaryUsers[user][key][movie]**2
                    vsqrt+=dictionaryUsers[name][key][movie]**2
            similarity[name]=round(simUV/((usqrt**(1/2))*(vsqrt**(1/2))),3)
    return similarity

#find "count" nearest users for current user-argument 
def find5Nearest(similarity,user,count=5):
    return dict(sorted(similarity.items(), key=operator.itemgetter(1), reverse=True)[0:count])

#create new values for current user, where movie == -1
def NewValues(User,nearestUsers,dictionaryUsers,key='values'):
    curUser = dictionaryUsers[User]
    currUserVals={}
    for movie in curUser[key].keys():
        if curUser[key][movie]==-1:
            ch = 0
            zn = 0
            for user in nearestUsers.keys():
                if dictionaryUsers[user][key][movie]!=-1:
                    simvu=nearestUsers[user]
                    rv=dictionaryUsers[user][key][movie]
                    rva=dictionaryUsers[user]['avg']
                    ch+=simvu*(rv-rva)
                    zn+=math.fabs(simvu)
            curUser[key][movie]=round(curUser['avg']+ch/zn,2)
            currUserVals[movie]=curUser[key][movie]
    return currUserVals
k=5
#current user
user='User '+str(27)
week={ 'Mon' : 1, 'Tue' : 2, 'Wed' : 3, 'Thu' : 4, 'Fri' : 5, 'Sat': 6, 'Sun': 7}

'''dictionaryUsers = {'User 1':{'values': {'Movie 1': 4, 'Movie 2': 4, ... }, {'avg': ...} } '''
dictionaryUsers={}
'''dictionaryDays = {'User 1':{'days': {'Movie 1': 4, 'Movie 2': -1, ... }, {'avg': ...} } '''
dictionaryDays={}
read('./data.csv',dictionaryUsers,'int')
read('./context.csv',dictionaryDays,'str',week)

#Task 1
'''similarity = {'User 1': 0.815, 'User 2': 0.861, ... ,'User 27': -1, ...} '''
similarity=Similarity(dictionaryUsers,user)
'''nearestUsers = {'User 12': 0.934, 'User 23': 0.916, 'User 4': 0.903, 'User 38': 0.89, 'User 22': 0.886}'''
nearestUsers=find5Nearest(similarity,user,k)
'''resMovies={'Movie 4': 4.64, 'Movie 1-1': 3.2, 'Movie 14': 2.23, 'Movie 17': 2.49, 'Movie 21': 3.27, 'Movie 25': 2.75}
only movies where value == -1'''
resMovies=NewValues(user,nearestUsers,dictionaryUsers)

#Task 2
'''similarity = {'User 1': 0.868, 'User 2': 0.764, 'User 3': 0.755, 'User 4': 0.779, ... }'''
similarityDays=Similarity(dictionaryDays,user,'days')
'''nearestUsersDays = {'User 37': 0.897, 'User 22': 0.894, 'User 23': 0.873, 'User 9': 0.871, 'User 1': 0.868}'''
nearestUsersDays=find5Nearest(similarityDays,user,k)
'''resDays={'Movie 4': 3.47, 'Movie 10': 3.39, 'Movie 14': 3.26, 'Movie 17': 5.68, 'Movie 21': 4.41, 'Movie 25': 5.27}'''
resDays=NewValues(user,nearestUsersDays,dictionaryDays,'days')

''' sorted movies with it's values, then if movie[i] day is in 1..5, return it'''
def Result(resMovies,resDays):
    resMovies=dict(sorted(resMovies.items(), key=operator.itemgetter(1), reverse=True))
    answer={}
    for movie in resMovies.keys():
        if resDays[movie]>0 and resDays[movie]<6:
            answer[movie]=resMovies[movie]
            break    
    return answer   

ans=Result(resMovies,resDays)
print(resMovies)
print(ans)
import requests
import json

js = json.dumps({'user': 27, '1': resMovies, '2': ans }, indent=2) 
response = requests.post("https://cit-home1.herokuapp.com/api/rs_homework_1", js, headers={'Content-type': "application/json"})
print(response.json())












