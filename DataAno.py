#generalization
def generalization(data,dg=0):
    if dg==0:
        data='*'
    else:
        for i in range(0,len(data)):
            digit=str(data[i])
            new_char="*"
            digit=digit[:len(digit)-dg]
            for k in range(0,dg):
                digit=digit + new_char
            data[i]=digit
    return data

#K-annonymity numerical
def kannonimity(data,c=3):
    data=data.to_numpy()
    data=data.reshape(-1, 1)   
    #Clustering K-annonymity
    from sklearn.cluster import KMeans
    km = KMeans(n_clusters=c)
    km.fit(data)
    clusters=km.predict(data)
    return clusters



#Sensetive Atribe
def sensetive(message):
    translated=message
    return translated