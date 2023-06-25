reset();

def log2(x):

    return log(x*1.)/log(2.);

####################################

#pos: leaf for which you want the merkle_proof (starting from 0)
#N: number of leaves in the base layer

def merkle_proof(pos,N):
    
    if len(pos)==0:
        m_proof = str(ceil(log2(N)))+'0';
    else:
        m_proof = [];
        Ns = 2^(ceil(log2(N)));

        #start from base layer
        this_pos = pos;
        for i in range(ceil(log2(N))):

            num_leaves = round(Ns/(2^i));
            val = this_pos%2;
            if val== 0:
                proof_pos = this_pos+1;
            else:
                proof_pos = this_pos-1;

            m_proof.append(str(i)+str(proof_pos));
            this_pos = floor(this_pos/2);

    return m_proof;


#pos: leaf for which you want the merkle_proof (starting from 0)
#N: number of leaves in the base layer
#tree_label specifies which tree we are considering

def common_merkle_proof(pos,N, tree_label):
    
    if len(pos)==0:
        m_proof = [tree_label+str(ceil(log2(N)))+'0'];
    else:
        
        m_proof = [];
        Ns = 2^(ceil(log2(N)));
        #start from base layer
        this_pos = pos;
        for i in range(ceil(log2(N))):
            new_pos = [];
            for x in this_pos:
                val = x%2;
                if val== 0:
                    needed_pos = x+1;
                    if needed_pos not in this_pos:
                        m_proof.append(tree_label+str(i)+str(needed_pos));
                else:
                    needed_pos = x-1;
                    if needed_pos not in this_pos:
                        m_proof.append(tree_label+str(i)+str(needed_pos));
                new_pos.append(floor(x/2));


            this_pos = uniq(new_pos);

    return m_proof;

###########################
tree_size = 24; #choose as the sum of two powers of 2, i.e., 36 = 32+4
num_proof = 3;

num_test = 10;
min_val = tree_size;
max_val = 0;
ave_val = 0;

fig_size = 32;
N = tree_size;

worst_case = 1;

worst_pos = [];
worst_proof = [];


#Separate tree into two trees
tree_size_1 = 2^(floor(log2(tree_size)));
tree_size_2 = tree_size - tree_size_1;

for i in range(num_test):
    leaves_pos = Combinations(tree_size, num_proof).random_element();
    tree1_pos = [];
    tree2_pos = [];
    for j in leaves_pos:
        if j <tree_size_1:
            tree1_pos.append(j);
        else:
            tree2_pos.append(j-tree_size_1);
            
    proofs_1 = common_merkle_proof(tree1_pos,tree_size_1,'L'); #merkle proofs for tree 1
    proofs_2 = common_merkle_proof(tree2_pos,tree_size_2,'R'); #merkle proofs for tree 2
    
    #update estimates
    if len(proofs_1)+len(proofs_2)>max_val:
        max_val = len(proofs_1)+len(proofs_2);
        worst_pos = leaves_pos;
        worst_proof = proofs_1;
        worst_proof.extend(proofs_2);
        
    if len(proofs_1)+len(proofs_2)<min_val:
        min_val = len(proofs_1) + len(proofs_2);
        
    ave_val += len(proofs_1) + len(proofs_2);

print("Average path size = "+str(ave_val*1./num_test)+" instead of "+str(round(log2(tree_size))*num_proof));
print("Min path size = "+str(min_val));

T = ceil(log(tree_size,2));
w = num_proof;
OMEGA = ceil(log(w,2));

x = 2^OMEGA + w*(T-OMEGA-1); 
print("Max path size = "+str(max_val)+", theoretic1 = "+str(num_proof*log2(tree_size/num_proof))+", theoretic2 = "+str(x));


#print worst case
if worst_case:
    leaves_pos = worst_pos;
    proofs = worst_proof;
else:
    proofs = proofs_1;
    proofs.extend(proofs_2);
        
#creating pos for graph
x_values = range(0,2*tree_size_1*tree_size_1,2*tree_size_1);

#Building tree 1
pos = {};
for ell in range(ceil(log2(tree_size_1))+1):
#    dist_nodes = tree_size_1/(2^ell); #set up node distance
    pos.update(dict(('L'+str(ell)+str(i),[fig_size*x_values[i], 2*fig_size*2*tree_size_1*ell]) for i in range(round(tree_size_1/(2^ell)))));
    new_x_values = [];
    if len(x_values)>1:
        for j in range(round(tree_size_1/(2^(1+ell)))):
            new_val = (x_values[2*j]+x_values[2*j+1])/2;
            new_x_values.append(new_val);
    else:
        new_x_values = [0];

    x_values = new_x_values;


#print("pos1 done");
#Creating tree 2
x_values = range(0,2*tree_size_1*tree_size_2,2*tree_size_1);

for ell in range(ceil(log2(tree_size_2))+1):
   # dist_nodes = tree_size_1/(2^ell); #set up node distance
    pos.update(dict(('R'+str(ell)+str(i),[fig_size*(2*tree_size_1*tree_size_1)+fig_size*x_values[i], 2*fig_size*2*tree_size_1*ell]) for i in range(round(tree_size_2/(2^ell)))));
    new_x_values = [];
    if len(x_values)>1:
        for j in range(round(tree_size_2/(2^(1+ell)))):
            new_val = (x_values[2*j]+x_values[2*j+1])/2;
            new_x_values.append(new_val);
    else:
        new_x_values = [tree_size_1+tree_size_2/2];

    x_values = new_x_values;
  #pos.update(dict((str(ell)+str(i),[-i*dist_nodes+tree_size/(2^ell), 2*tree_size*ell]) for i in range(round(tree_size/(2^ell)))));


#creating tree 1(nodes and edges)
tree = {};
colors = [];
for ell in range(ceil(log2(tree_size_1))):
    for i in range(round(tree_size_1/(2^ell))):
        upper_val = floor(i/2);
        tree.update({'L'+str(ell)+str(i): ['L'+str(ell+1)+str(upper_val)]});
        if ell == 0:
            if i in leaves_pos:
                colors.append('blue');
            else:
                if 'L0'+str(i) in proofs:
                    colors.append('green');
                else:
                    colors.append('gray');
        else:
            if 'L'+str(ell)+str(i) in proofs:
                colors.append('green');
            else:
                colors.append('gray');

if 'L'+str(ceil(log2(tree_size_1)))+'0' in proofs:
    colors.append('green');
else:
    colors.append('gray');

#creating tree 2(nodes and edges)
for ell in range(ceil(log2(tree_size_2))):
    for i in range(round(tree_size_2/(2^ell))):
        upper_val = floor(i/2);
        tree.update({'R'+str(ell)+str(i): ['R'+str(ell+1)+str(upper_val)]});
        if ell == 0:
            if i+tree_size_1 in leaves_pos:
                colors.append('blue');
            else:
                if 'R0'+str(i) in proofs:
                    colors.append('green');
                else:
                    colors.append('gray');
        else:
            if 'R'+str(ell)+str(i) in proofs:
                colors.append('green');
            else:
                colors.append('gray');
                
if 'R'+str(ceil(log2(tree_size_2)))+'0' in proofs:
    colors.append('green');
else:
    colors.append('gray');

g = Graph(tree);

#adding edges
#m_proof = proofs;
#for i in range(len(m_proof)-1):
#     g.add_edge((m_proof[i], m_proof[i+1], 'a'));

#a = g.graphplot(pos=pos, color_by_label=False, figsize = [fig_size,2*fig_size], vertex_size = 2000*32/N, title ='Gray: recomputed locally, Blue: asked, Green: in the proof', title_pos = [0.1, 2*fig_size*2*tree_size*ceil(log2(tree_size))+1 ], fontsize = 32).plot()

a = g.graphplot(pos=pos, color_by_label=False, figsize = [fig_size,2*fig_size], vertex_size = 2000*32/N, vertex_colors=colors, title ='Gray: unseen, Blue: asked, Green: in the proof', title_pos = [0.1, 2*fig_size*2*tree_size*ceil(log2(tree_size))+1 ], fontsize = 32).plot()
a.show();

