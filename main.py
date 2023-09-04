import numpy as np
import matplotlib.pyplot as plt
import numpy.random as rd
import time
import warnings
warnings.simplefilter("error", np.VisibleDeprecationWarning)

#definition de l'algorithme SAT-3
def sat3(N,M):
    #création d'un tableau c contenant 3*M valeurs comprises entre 1 et N. Puis création d'un tableau r1 contenant 3*M valeur comprises entre 0 et 1
    c=np.random.randint(1,N+1,size=3*M)
    r1=np.random.rand(3*M)
    
    #si r1[i]>0,5 alors c[i] devient négatif
    for i in range(len(c)):
        if r1[i]>0.5:
            c[i]=c[i]*-1
    c=np.reshape(c,[M,3])    
    return c

#definition de l'algorithme CU
def CU(N,M):
    c=sat3(N,M)
    r=np.array([])
    c=np.sort(c)
    
    
    #ici l'algorithme regarde si le tableau possède des lignes avec des opposés sur la même ligne (0,1,-1) et les supprime si c'est le cas.
    #Et remplace par un 0 une des valeur qui serai doublé sur une même ligne. Il remplace deux valeurs si il y a un triplé.
    #Finalement il rangera les valeurs de chaque ligne par ordre croissant pour faire apparaitre les lignes avec les même valeurs.
    x=0
    y=0
    z=1
    while x!=len(c):
        if c[x,y]==c[x,z]:
            c[x,y]=0
            if z<2:
                y=y+1
                z=z+1
            else:
                y=0
                z=1
                x=x+1
        else:
            if (c[x,y]==-c[x,z]):
                c=np.delete(c, x,0)
                y=0
                z=1
            elif z<2:
                z=z+1
                y=y+1
            else:
                y=0
                z=1
                x=x+1
    c=np.sort(c)
    
    
    #L'algorithme va supprimer les lignes parfaitement exacte.
    c=np.unique(c,axis=0)
    
    
    #L'algorithme va chercher les lignes avec deux 0 en créant un tableau k qui possèdera où k[i] sera égal à 2 si il y a deux zéros sur une ligne c[i].
    k=np.zeros([len(c),1])
    for i,proba_array in enumerate(c):
        for proba in proba_array:
            if proba==0:
                k[i]+=1
    
    
    #Création d'un tableau r qui va ajouter à son tableau toutes les lignes c[i], sans les zéros, où k[i]=2. L'agorithme rend chaque valeur de r unique.
    #Si la longueur de r est égal au nombre de ligne de c alors l'algorithme s'arrête et affiche "il existe une solution au problème et",r,"est la solutions.". 
    #Par contre, si il existe des opposés dans r alors l'algoritme s'arrête et affiche "il n existe pas une solution au problème.".
    for i in range(len(k)):
        if k[i]==2:
            b=c[i]
            r=np.append(r,b[np.nonzero(b)])
    r=np.unique(r)
    
    
    if len(r)>0:
        if len(r) != np.unique(np.abs(r)).all():
            return "il n existe pas une solution au problème."
        
    if len(r)==len(c):
        return "il existe une solution au problème et",r,"est la solutions."
    
    
    #r va ajouter à son tableau, de manière aléatoire, une valeur de chaque ligne de c différent de 0, des toutes les valeurs déjà présentent dans r et de leur opposés.
    #Si aucune des ces conditions sont respecté alors il passe à la ligne suivante.
    i=0
    while i!=len(c):
        b=c[i]
        t=b[np.nonzero(b)]
        if len(t)==1:
            if np.isin(np.abs(t[0]),np.abs(r)):
                i=i+1
            else:
                r=np.append(r,t)
                i=i+1
                
                
        elif len(t)==2:
            j=np.random.randint(0,2,size=1)
            if np.isin(np.abs(t[j]),np.abs(r)):
                t=np.delete(t,j)
                if np.isin(np.abs(t[0]),np.abs(r)):
                    i=i+1
                else:
                    r=np.append(r,t[0])
                    i=i+1
                    
            else:
                r=np.append(r,t[j])
                i=i+1
                
                
        else:
            j=np.random.randint(0,3,size=1)
            if np.isin(np.abs(t[j]),np.abs(r)):
                t=np.delete(t,j)
                j=np.random.randint(0,2,size=1)
                if np.isin(np.abs(t[j]),np.abs(r)):
                    t=np.delete(t,j)
                    if np.isin(np.abs(t[0]),np.abs(r)):
                        i=i+1
                    else:
                        r=np.append(r,t[0])
                        i=i+1
                else:
                    r=np.append(r,t[j])
                    i=i+1
                    
            else:
                r=np.append(r,t[j])
                i=i+1
    
    
    #Création d'un tableau c1 de M lignes et 3 colonnes avec des True aux endroits où il y a des valeurs de r sinon il met False.
    b=len(c)
    c=np.reshape(c,[1,3*b])
    c=c[0]
    c1=[]
    for i in c:
        c1.append(i in r)
    
    c=np.reshape(c,[b,3])
    c1=np.reshape(c1,[len(c),3])
    
    
    #Création d'un tableau p qui ajoutera un 1 à sa liste si il y a un True sur une ligne (une seul fois par ligne). 
    #Puis, si la longueur de p est égal au nombre de ligne de c alors l'algorithme s'arrête et affiche "il existe une solution au problème et",r,"est une des solutions."
    #Sinon il s'arrête est affiche "il n existe pas une solution au problème."
    i=0
    j=0
    p=[]
    while i!=len(c1):
        if c1[i,j]==True:
            p=np.append(p,1)
            i=i+1
            j=0
        else:
            if j<2:
                j=j+1
            else:
                j=0
                i=i+1
    if len(p)==len(c):
        return "il existe une solution au problème et",r,"est une des solutions."
    else:
        return "il n existe pas une solution au problème."

#definition de l'algorithme CUG
def CUG(N,M):
    c=sat3(N,M)
    r=np.array([])
    c=np.sort(c)
    
    
    #ici l'algorithme regarde si le tableau possède des lignes avec des opposés sur la même ligne (0,1,-1) et les supprime si c'est le cas.
    #Et remplace par un 0 une des valeur qui serai doublé sur une même ligne. Il remplace deux valeurs si il y a un triplé.
    #Finalement il rangera les valeurs de chaque ligne par ordre croissant pour faire apparaitre les lignes avec les même valeurs.
    x=0
    y=0
    z=1
    while x!=len(c):
        if c[x,y]==c[x,z]:
            c[x,y]=0
            if z<2:
                y=y+1
                z=z+1
            else:
                y=0
                z=1
                x=x+1
        else:
            if (c[x,y]==-c[x,z]):
                c=np.delete(c, x,0)
                y=0
                z=1
            elif z<2:
                z=z+1
                y=y+1
            else:
                y=0
                z=1
                x=x+1
    c=np.sort(c)
    
    
    #L'algorithme va supprimer les lignes parfaitement exacte.
    c=np.unique(c,axis=0)
    
    
    #L'algorithme va chercher les lignes avec deux 0 en créant un tableau k qui possèdera où k[i] sera égal à 2 si il y a deux zéros et 1 si il y a un zéro sur une ligne c[i].
    k=np.zeros([len(c),1])
    for i,proba_array in enumerate(c):
        for proba in proba_array:
            if proba==0:
                k[i]+=1
    
    
    #Création d'un tableau r qui va ajouter à son tableau toutes les lignes c[i], sans les zéros, où k[i]=2. L'agorithme rend chaque valeur de r unique.
    #Si la longueur de r est égal au nombre de ligne de c alors l'algorithme s'arrête et affiche "il existe une solution au problème et",r,"est la solutions.". 
    #Par contre, si il existe des opposés dans r alors l'algoritme s'arrête et affiche "il n existe pas une solution au problème.".
    for i in range(len(k)):
        if k[i]==2:
            b=c[i]
            r=np.append(r,b[np.nonzero(b)])
    r=np.unique(r)
        
    
    if len(r)>0:
        if len(r) != np.unique(np.abs(r)).all():
            return "il n existe pas une solution au problème."
                
    if len(r)==len(c):
        return "il existe une solution au problème et",r,"est la solution"
    
    
    #L'algorithme cherche d'abord les ligne où il y a 1 zéro.
    #Puis r va ajouter à son tableau, de manière aléatoire, une valeur de chaque ligne de c différent de 0, des toutes les valeurs déjà présentent dans r et de leur opposés.
    #Si aucune des ces conditions sont respecté alors il passe à la ligne suivante.
    i=0
    while i!=len(c):
        b=c[i]
        t=b[np.nonzero(b)]
        if len(t)==2:
            j=np.random.randint(0,2,size=1)
            if np.isin(np.abs(t[j]),np.abs(r)):
                t=np.delete(t,j)
                if np.isin(np.abs(t[0]),np.abs(r)):
                    i=i+1
                else:
                    r=np.append(r,t[0])
                    i=i+1
                    
            else:
                r=np.append(r,t[j])
                i=i+1
        else:
            i=i+1
                
    
    #L'algorithme cherche d'abord les ligne où il n'y a pas de zéro.
    #Puis, r va ajouter à son tableau, de manière aléatoire, une valeur de chaque ligne de c différent de 0, des toutes les valeurs déjà présentent dans r et de leur opposés. 
    #Si aucune des ces conditions sont respecté alors il passe à la ligne suivante.
    i=0
    while i!=len(c):
        b=c[i]
        t=b[np.nonzero(b)]
        if len(t)==3:
            j=np.random.randint(0,3,size=1)
            if np.isin(np.abs(t[j]),np.abs(r)):
                t=np.delete(t,j)
                j=np.random.randint(0,2,size=1)
                if np.isin(np.abs(t[j]),np.abs(r)):
                    t=np.delete(t,j)
                    if np.isin(np.abs(t[0]),np.abs(r)):
                        i=i+1
                    else:
                        r=np.append(r,t[0])
                        i=i+1
                else:
                    r=np.append(r,t[j])
                    i=i+1
                    
            else:
                r=np.append(r,t[j])
                i=i+1
        else:
            i=i+1
    
    
    #Création d'un tableau c1 de M lignes et 3 colonnes avec des True aux endroits où il y a des valeurs de r sinon il met False.
    b=len(c)
    c=np.reshape(c,[1,3*b])
    c=c[0]
    c1=[]
    for i in c:
        c1.append(i in r)
    
    c=np.reshape(c,[b,3])
    c1=np.reshape(c1,[len(c),3])
    
    
    #Création d'un tableau p qui ajoutera un 1 à sa liste si il y a un True sur une ligne (une seul fois par ligne). 
    #Puis, si la longueur de p est égal au nombre de ligne de c alors l'algorithme s'arrête et affiche "il existe une solution au problème et",r,"est une des solutions."
    #Sinon il s'arrête est affiche "il n existe pas une solution au problème."   
    i=0
    j=0
    p=[]
    while i!=len(c1):
        if c1[i,j]==True:
            p=np.append(p,1)
            i=i+1
            j=0
        else:
            if j<2:
                j=j+1
            else:
                j=0
                i=i+1
    if len(p)==len(c):
        return "il existe une solution au problème et",r,"est une des solutions. "
    else:
        return "il n existe pas une solution au problème."

#definition de la fonction permettant de tracer en fonction de M/N, la moyenne du nombre de fois que l'algorithme finis par trouver une solution pour chaque N.
#f étant l'algorithme choisit et K, le nombre de fois que l'on appel l'algorithme sur chaque valeur de N. Ici M peut être une liste.
def trac(f,N,M,K):
    i=0
    j=0
    x=0
    v=np.zeros([len(N),len(M)])
    mean=[]
    err=[]
    #Ici v[j,i] va faire +1 si il existe une solution avec N[j] et M[i].
    #Et ça se répétera K fois pour faire une moyenne sur chaque v[j,i].
    for x in range(K):
        i=0
        while i!=len(M):
            if j<len(N):
                if f(N[j],M[i])[0]=="il existe une solution au problème et":
                    v[j,i]+=1
                    j+=1
                else:
                    j+=1
            else:
                j=0
                i+=1
    
    
    
    v=np.reshape(v,[1,len(N)*len(M)])
    v=v[0]
    v=list(map(int,v))
    
    #Le tableau mean va faire des moyennes du nombre de fois que f(N,M) a trouvé une solution par rapport au nombre de répétition et les ajouter à sa liste.
    #Puis, il fait l'écart type pour trouver l'incertitude de mean et les ajoutes à la liste err.
    for p in v:
        h1=np.mean(np.append([0]*(10-p),[1]*p))
        h2=np.std(np.append([0]*(10-p),[1]*p))
        mean=np.append(mean,h1)
        err=np.append(err,h2)
    
    
    mean=np.reshape(mean,[len(N),len(M)])
    err=np.reshape(err,[len(N),len(M)])
    
    #Finalement, il trace mean en fonction de M/N avec une incertitude de err
    for i in range(len(M)):
        plt.errorbar(M[i]/N,mean[:,i],None,err[:,i],'+')
        plt.xlabel('%i/N' %M[i])
        plt.ylabel('mean')
        plt.title('mean en fonction de %i/N ' %M[i])
        plt.show()
    return


#definition de la fonction permettant de tracer en fonction de M/N, le temps moyen de calcul de chaque algorithme. 
#f étant l'algorithme choisit et K, le nombre de fois que l'on appel l'algorithme sur chaque valeur de N. Ici M doit être une valeur.
def tractime(f,N,M,K):
    v=np.zeros([len(N),K])
    meant=[]
    err=[]
    #Création d'un tableau dv qui possèdera les valeurs des temps mis pour un algorithme pour se terminer.
    for i in range(K):
        for line,value in enumerate(N):
            t0=time.time()
            f(value,M[0])
            t1=time.time()
            v[line,i]=t1-t0
    
    #Création d'un tableau meant et err correspondant respectivement aux temps moyens et aux écart type des valeurs de v.
    for i in range(len(N)):
        meant=np.append(meant,np.mean(v[i]))
        err=np.append(err,np.std(v[i]))
    
    #Il trace le temps moyen mis par l'algorithme pour trouver ou non une solution pour chaque N.
    plt.errorbar(M/N,meant,None,err,'+')
    plt.xlabel('%i/N' %M[0])
    plt.ylabel('meant')
    plt.title('temps moyen par N en fonction de %i/N ' %M[0])
    plt.show()
    return

