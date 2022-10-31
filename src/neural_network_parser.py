from tensorflow import keras
import hmod_validator


def main(parameters, species, species_checkboxes, parameters_checkboxes, h5_file, curr_file_name, hmod_file_string):
    inputs = [] #input IDs for the model network test ["S"]
    for i in range(len(species_checkboxes)):
        if species_checkboxes[i][1].get() == 1:
            inputs.append(species[i])

    hybout = [] #output IDs for the model network test ["miu","vPM","vPT"]
    for i in range(len(parameters_checkboxes)):
        if parameters_checkboxes[i][1].get() == 1:
            hybout.append(parameters[i])

    # open Keras file
    model = keras.models.load_model(h5_file)

    weights = model.get_weights() # list of numpy arrays containing weights in a per layer/bias basis

    # This section orders the weights in a single list for future usage in the format:
    # Input->Hidden1 weights;
    # Input->Hidden1 bias;
    # Hidden1->Hidden2 weights;
    # Hidden1->Hidden2 bias; etc.
    countgroup=0
    countsubgroup=0
    orderedweights=[]
    for groups in weights:
        if (countgroup % 2) == 0:
            for subgroups in weights[countgroup]:
                orderedweights.extend(weights[countgroup][countsubgroup])
                countsubgroup=countsubgroup+1
        else:
            orderedweights.extend(weights[countgroup])
        countsubgroup=0
        countgroup=countgroup+1

    nlayers=len(model.layers) #Check number of model layers
    nin = len(inputs) #Check number of inputs
    countin=0 #Create a parsed input counter
    equations =[] #Create empty equations list to be built
    H=[] #Create empty hidden nodes list
    wcount=0 #number of parsed weights (required for some adjustments)

    for layer in range(nlayers):
        H.append([]) #Add a new layer to list
        nH = len(weights[layer*2+1]) #number of nodes in the layer. Read from the number of bias values, since it is currently assumed to be one per node (Standard dense layers)
        if layer == 0:
            for node in range(nH):
                H[layer].append("")
                #First layer and node is w1*in1 +(w1+nH)*in2 + (w1+nH*2)*in2... w1+nh*nin. Second node sums 1 to each. Third sums 2 to the first and so on.
                for n in range(nin):
                    H[layer][node] = H[layer][node] + ("w" if n==0 else "+w") + str(1+node+nH*n) + "*" + inputs[n]

                    if n==nin-1:
                        H[layer][node] = H[layer][node] + "+w" + str(1+node+nH*(n+1))
                        H[layer][node] = "tanh(" + H[layer][node] + ")"

            wcount=wcount+ len(H[layer])*len(inputs)+len(H[layer]) #add number of parsed on this step nodes to count

        elif 0 < layer < nlayers-1:
            for node in range(nH):
                H[layer].append("")
                #Second to second last layer are based on the previous number of nodes (size of the H in the previous row list) to the next number of nodes(nH)
                for n in range(len(H[layer-1])):
                    H[layer][node] = H[layer][node] + ("w" if n==0 else "+w") + str(wcount+1+node+nH*n) + "*" + H[layer-1][n]

                    if n==len(H[layer-1])-1:
                        H[layer][node] = H[layer][node] + "+w" + str(wcount+1+node+nH*(n+1))
                        H[layer][node] = "tanh(" + H[layer][node] + ")"

            wcount=wcount+ len(H[layer])*len(H[layer-1])+len(H[layer]) #add number of parsed on this step nodes to count

        elif layer == nlayers-1:
            for node in range(nH):
                H[layer].append("")
                #Last layer is based on the previous number of nodes (size of the H in the previous row list) to the number of outputs
                for n in range(len(H[layer-1])):
                    H[layer][node] = H[layer][node] + ("w" if n==0 else "+w") + str(wcount+1+node+nH*n) + "*" + H[layer-1][n]

                    if n==len(H[layer-1])-1:
                        H[layer][node] = H[layer][node] + "+w" + str(wcount+1+node+nH*(n+1))


            wcount=wcount+ len(H[layer])*len(H[layer-1])+len(H[layer]) #add number of parsed on this step nodes to count

    equations = H[-1]
    # Original file and output file
    f = hmod_file_string.split("\n")
    h = ""

    o_name = curr_file_name.split(".hmod")[0] if ".hmod" in curr_file_name else curr_file_name.split(".xml")[0]
    n_name = o_name

    # Prepare automatic variables
    Asscount=0 #counter for assignments
    wcount=0 #counter for weights
    subAss=0 # counter for repeated assignments
    for line in f:
        if ".nparameters=" in line:
            pos=line.index("=")
            nbasepar=int(line[pos+1:-1])#obtain number of base parameters
            nhybpar=int(line[pos+1:-1]) #Define a counter for the hybrid parameters

        elif ".nruleAss" in line:
            pos=line.index("=")
            nbaseAss=int(line[pos+1:-1]) #obtain number of base assignments
            nhybAss=int(line[pos+1:-1]) #Define a counter for the hybrid assignments

        elif (".ruleAss(" in line) and (").id" in line): #check for assignment rules to substitute
            if any(item in line for item in hybout):
                subAss=subAss+1

    skip = 0 # Placeholder for skipped lines
    outhyb = 0 # Placeholder of hybrid output
    #Write hybrid file
    for line in f:
        if ".parameters("+str(nbasepar)+").reaction" in line: #Check if the last standard parameter line has been reached
            if outhyb==1:
                outhyb=0
                h += line.replace(o_name, n_name).replace("local","global") +"\n"
            else:
                h += line.replace(o_name,n_name)+"\n" #write the last standard line for the hybrid model
            for w in orderedweights: #Add all hybrid weights
                nhybpar=nhybpar+1 #Increase hybrid parameter counter. Following 4 lines write the new hybrid parameter
                h += n_name+'.parameters('+str(nhybpar)+').id="w'+str(wcount+1)+'";\n'
                h += n_name+".parameters("+str(nhybpar)+").val="+str(orderedweights[wcount])+";\n"
                h += n_name+".parameters("+str(nhybpar)+").fixed=0;\n"
                h += n_name+'.parameters('+str(nhybpar)+').reaction="global";\n'
                wcount=wcount+1 #Increase weights counter

        elif (".parameters(" in line) and (").id" in line):
            if any(item in line for item in hybout):
                h += line.replace(o_name,n_name)+"\n"
                outhyb=1 #reduced number of new hybrid assignments
            else:
                h += line.replace(o_name,n_name)+"\n"

        elif (".parameters(" in line) and (").reaction" in line):
            if outhyb==1:
                outhyb=0
                h += line.replace(o_name, n_name).replace("local","global")+"\n"
            else:
                h += line.replace(o_name, n_name)+"\n"

        elif ".ruleAss("+str(nbaseAss)+").val" in line or ("nruleAss=0" in line): #Check if the last standard assignment line has been reached
            if skip>0:
                skip=skip-1
            elif skip==0 and ("nruleAss=0" in line):
                h += line.replace(str(nbaseAss),str(nbaseAss+len(hybout)-subAss)).replace(o_name,n_name)+"\n"
            else:
                h += line.replace(o_name,n_name)+"\n" #write the last standard line for the hybrid model
            for par in hybout: #Add all hybrid assignments
                if Asscount >= len(equations):
                    return [None, len(equations)]
                nhybAss=nhybAss+1 #Increase hybrid assignments counter. Following 4 lines write the new hybrid assignments
                h += n_name+'.ruleAss('+str(nhybAss)+').id="'+hybout[Asscount]+'";\n'
                h += n_name+'.ruleAss('+str(nhybAss)+').val="'+equations[Asscount]+'";\n'
                Asscount=Asscount+1 #Increase assignments counter

        elif ".nparameters=" in line: #Correct number of parameters
            h += line.replace(str(nbasepar),str(nbasepar+len(orderedweights))).replace(o_name,n_name)+"\n"

        elif ".nruleAss" in line: #Correct number of assignments
            h += line.replace(str(nbaseAss),str(nbaseAss+len(hybout)-subAss)).replace(o_name,n_name)+"\n"

        elif (".ruleAss(" in line) and (").id" in line): #check for assignment rules to substitute
            if any(item in line for item in hybout):
                nhybAss=nhybAss-1 #reduced number of new hybrid assignments
                skip=1
            else:
                h += line.replace(o_name, n_name)+"\n"

        elif skip >0: #check if line should be skipped
            skip=skip-1

        else: #For all other lines, copy them to the new file
            if "% Events" in line:
                h += "\n"
            h += line.replace(o_name,n_name)+"\n"

    return [h, None]
