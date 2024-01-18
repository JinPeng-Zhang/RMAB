using LinearAlgebra, StatsBase, PyPlot, Random

L = 10
p0, p1 = 1/2, 3/4
beta = 0.75
pExplore(t) = t^-0.5
alpha(t) = t^-0.99
T = 10^6

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
