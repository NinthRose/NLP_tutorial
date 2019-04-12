Hidden_states = ('Healthy', 'Fever') # 隐状态集合
 
Observations_states = ('normal', 'cold', 'dizzy') # 观测状态集合
 
Start_probability = {'Healthy': 0.6, 'Fever': 0.4} # 表示病人第一次到访时医生认为其所处的HMM状态，他唯一知道的是病人倾向于是健康的（可以理解为这是基于一个对大众身体信息的了解得出的初始状态）
 
Hidden_transition_probability = { # 隐马尔可夫链中身体状态的状态转移概率，我们能够看到，当天健康的人，第二天有30%的概率会发烧
   'Healthy' : {'Healthy': 0.7, 'Fever': 0.3},
   'Fever' : {'Healthy': 0.4, 'Fever': 0.6},
   }
 
Hidden_observations_probability = {    # 原来叫emission_probability。这里表示病人每天的感觉的可能性。即，如果他是一个健康人，有50%的可能会感觉正常，40%觉得冷，10%觉得头晕
   'Healthy' : {'normal': 0.5, 'cold': 0.4, 'dizzy': 0.1},
   'Fever' : {'normal': 0.1, 'cold': 0.3, 'dizzy': 0.6},
   }

# Helps visualize the steps of Viterbi.
def print_dptable(V): # 打印dp矩阵
    print ("    "),
    for i in range(len(V)): 
        print("%7d" % i)
    print()

    for y in V[0].keys():
        print ("%.5s: " % y)
        for t in range(len(V)):
            print ("%.7s" % ("%f" % V[t][y]))
        print()

def viterbi(obs, states, start_p, trans_p, h2o_p): # Viterbi算法
    V = [{}]
    path = {}

    # Initialize base cases (t == 0)
    for y in states:
        V[0][y] = start_p[y] * h2o_p[y][obs[0]]
        path[y] = [y]

    # Run Viterbi for t > 0
    for t in range(1,len(obs)):
        V.append({})
        newpath = {}

        for y in states:
            (prob, state) = max([(V[t-1][y0] * trans_p[y0][y] * h2o_p[y][obs[t]], y0) for y0 in states])
            V[t][y] = prob
            newpath[y] = path[state] + [y]

        # Don't need to remember the old paths
        path = newpath

    print_dptable(V)
    (prob, state) = max([(V[len(obs) - 1][y], y) for y in states])
    return (prob, path[state])

def example():
    return viterbi(Observations_states,
                   Hidden_states,
                   Start_probability,
                   Hidden_transition_probability,
                   Hidden_observations_probability)
print(example())



'''
example print:

      0
      1
      2

Healt:
0.30000
0.08400
0.00588

Fever:
0.04000
0.02700
0.01512

(0.01512, ['Healthy', 'Healthy', 'Fever'])
'''

