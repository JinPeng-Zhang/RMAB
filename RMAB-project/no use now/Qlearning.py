import gurobipy as GBP
import numpy as np
import heapq
import matplotlib.pyplot as plt
import  copy
'''
using LinearAlgebra, PyPlot

L=10
p0, p1 = 1/2, 3/4 
beta = 0.75 
epsilon = 0.00001

function valueIteration(kappa)
    P0 = diagm(1=>fill(p0,L-1)) + diagm(-1=>fill(1-p0,L-1)) 
    P0[1,1], P0[L,L] = 1 - p0, p0
    P1 = diagm(1=>fill(p1,L-1)) + diagm(-1=>fill(1-p1,L-1))
    P1[1,1], P1[L,L] = 1 - p1, p1

    R0 = collect(1:L)
    R1 = R0 .- kappa

    bellmanOperator(Vprev) = max.(R0 + beta*P0*Vprev,R1 + beta*P1*Vprev)
    optimalPolicy(V,state) = (R0+beta*P0*V)[state]>=(R1+beta*P1*V)[state] ? 0 : 1

    V, Vprev = fill(0,L), fill(1,L) 
    while norm(V-Vprev) > epsilon
    	Vprev = V
    	V = bellmanOperator(Vprev)
    end

    return [optimalPolicy(V,s) for s in 1:L] 

end


#=kappaGrid = 0:0.1:2.0
policyMap = zeros(L,length(kappaGrid))


for (i,kappa) in enumerate(kappaGrid) 
    policyMap[:,i] = valueIteration(kappa)
end

matshow(policyMap);
=#

kappa = 1.2
println("\n Optimal policy : ", valueIteration(kappa))
println("\n")
'''

'''


Random.seed!(1) 

function QlearnSim(kappa)
	P0 = diagm(1=>fill(p0,L-1)) + diagm(-1=>fill(1-p0,L-1))
	P0[1,1], P0[L,L] = 1 - p0, p0

	P1 = diagm(1=>fill(p1,L-1)) + diagm(-1=>fill(1-p1,L-1))
	P1[1,1], P1[L,L] = 1 - p1, p1

	R0 = collect(1:L)
	R1 = R0 .- kappa

	nextState(s,a) = a == 0 ? sample(1:L,weights(P0[s,:])) : sample(1:L,weights(P1[s,:]))
	optimalAction(s) = Q[s,1] >= Q[s,2] ? 0 : 1

	Q = zeros(L,2) 
	s = 1
	count = 0
	t = 1
	while true 
		if rand() < pExplore(t)
            		a = rand([0,1])
		else
			a = optimalAction(s)
		end
		sNew = nextState(s,a)
		r = a == 0 ? R0[sNew] : R1[sNew] 
		Q[s,a+1] =(1-alpha(t))*Q[s,a+1] + alpha(t)*(r+beta*max(Q[sNew,1],Q[sNew,2])) 
		s=sNew
		count = count + 1
		t = t + 1
		if count == 100000
		    println("Time: ", t)
		    println([optimalAction(s) for s in 1:L])
		    count = 0
		end
	end
#	[optimalAction(s) for s in 1:L] 
end

#=kappaGrid = 0.0:0.1:2.0
policyMap = zeros(L,length(kappaGrid))

for (i,kappa) in enumerate(kappaGrid) 
	policyMap[:,i] = QlearnSim(kappa)
end

matshow(policyMap)
=#
kappa = 1.2
QlearnSim(kappa) 
'''
###param
def pExplore(t):
    return 0.15
    #return  min(2*t**(-0.5),1)
def alpha(t):
    return 0.7
I = 5 ###学生数量
K = 1##老师数量
L = 10
p0, p1 = 0.3, 0.7
beta = 0.99
T = 10**6
np.random.seed(2)
WI = np.arange(1.001,step=1/30)
print(WI,len((WI)))
# while(1):
#     pass
lambdas = np.random.randint(0,31,10)

Q = np.random.rand(31,L,2)
R = np.zeros((L,2))
r = []
for i in range(I):
    r.append([])
    r[i].append(0)
def QLearn(t,S,A,SNEW):
    o = 0
    Qold = copy.deepcopy(Q)
    for s,a,snew in zip(S,A,SNEW):
        Q[lambdas[s],s,a] = (1-alpha(t))*Qold[lambdas[s],s,a] + alpha(t)*( R[s,a] - WI[lambdas[s]]*a + beta*max(Qold[lambdas[s],snew,0],Qold[lambdas[s],snew,1]))
        r[o].append((r[o][t-1]*(t-1) +R[s,a])/t)
        o  = o + 1

    for s in range(L):
        MIN = 1000
        INDEX = 0
        for i in range(31):
            if abs(Q[i,s,0]-Q[i,s,1])<MIN:
                MIN = abs(Q[i,s,0]-Q[i,s,1])
                INDEX = i
        lambdas[s] = INDEX
    action = np.zeros(I,dtype=int)
    lam = []
    for snew in SNEW:
        lam.append(lambdas[snew])
    arr_max = heapq.nlargest(K,lam)
    act = 0
    for la,i in zip(lam,range(31)):
        if la in arr_max and act<K:
            action[i] = 1
            act = act + 1
    ###random
    ##action[np.random.randint(0,5,1)] = 1
    print(lambdas)
    for l in range(I):
        if np.random.rand()<pExplore(t):
            action[l] = np.random.randint(0,2,1)
    for s in range(L):
        if np.random.rand()<pExplore(t):
            lambdas[s] = np.random.randint(0,31,1)
    return  Q,lambdas,action

for i in range(L):
    R[i,0] = ((i+1)/10)**0.5
    R[i, 1] = ((i + 1) / 10) ** 0.5


S = np.zeros(I,dtype=int)
action = np.zeros(I,dtype=int)
SNEW = np.zeros(I,dtype=int)
for i in range(I):
    if np.random.rand() <p0:
        SNEW[i] = 1
    else:
        SNEW[i] = 0

print(Q)
for t in range(20000):
    Q,lambdas,action = QLearn(t+1,S,action,SNEW)
    S = copy.deepcopy(SNEW)

    for i in range(I):
        if action[i] == 1:
            if np.random.rand() <p1:

                if SNEW[i] == L-1:
                    SNEW[i] = SNEW[i]
                else:
                    SNEW[i] = SNEW[i]+1
            else:

                if SNEW[i] == 0:
                    SNEW[i] = SNEW[i]
                else:
                    SNEW[i] = SNEW[i]-1

        else:
            if np.random.rand() <p0:

                if SNEW[i] == L-1:
                    SNEW[i] = SNEW[i]
                else:
                    SNEW[i] = SNEW[i]+1
            else:

                if SNEW[i] == 0:
                    SNEW[i] = SNEW[i]
                else:
                    SNEW[i] = SNEW[i]-1
    #print(S,SNEW,action)

for i in range(I):
    plt.plot(r[i])
    print(r[i][-1])
plt.show()
