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
