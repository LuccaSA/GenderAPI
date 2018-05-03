import csv
import numpy as np
import sys

DATA_PATH = './data/'

# Fréd => FRED => 6 17 ...
def encode(input):
    maxFnameLen = 40 # nb de caractères max dans le prénom
    lettersToReplace = "ÀÁÂÃÄÅàáâãäåÒÓÔÕÖØòóôõöøÈÉÊËèéêëÌÍÎÏìíîïÙÚÛÜùúûüÿÑñÇç";
    replacementletters = "AAAAAAaaaaaaOOOOOOooooooEEEEeeeeIIIIiiiiUUUUuuuuyNnCc";

    # si prénom trop long on fait planter
    if (len(input) > maxFnameLen):
        print("Too big name detected : " + input)
        return;
        
    #Accent insensitive
    for i in range(0, len(lettersToReplace)):
        input = input.replace(lettersToReplace[i], replacementletters[i])
        
    fnameAdj = '{0: <{l}}'.format(input[::], l=maxFnameLen)[0:maxFnameLen].upper()
    result = []
    for c in fnameAdj:
        v = 1 + ord(c) - ord('A')
        if v < 0 or v > 26:
            v = 0
        result.append(v)
    return result

# save numpy arrays
def save_npy(name_of_set, X, Y):
    np.save("./npy/X_" + name_of_set + ".npy", X)
    np.save("./npy/Y_" + name_of_set + ".npy", Y)   

# open csv file
with open(DATA_PATH + 'genders.csv') as csvfile:
    X = []
    Y = []
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in spamreader:
        x = row[0] # Fréd
        y = row[1] # Mr
        xArranged = encode(x) # 6 17 ...
        yArranged = 0 if y == 'Mr' else 1 # 0
        X.append(xArranged)
        Y.append(yArranged)

# on prépare les indices pour le 80/10/10
indice_80 = int(len(X) * 0.8)
indice_90 = int(len(X) * 0.9)
print(len(X))
print(indice_80)
print(indice_90)

# on converti en npy arrays
X = np.asarray(X, dtype=np.uint8)
Y = np.asarray(Y, dtype=np.uint8)

# shuffle des indices
indices = np.arange(len(X))
np.random.shuffle(indices)
X = X[indices]
Y = Y[indices]

# save des jeux de données
save_npy('TRAIN', X[0:indice_80], Y[0:indice_80])
save_npy('VAL', X[indice_80:indice_90], Y[indice_80:indice_90])
save_npy('TEST', X[indice_90:len(X)], Y[indice_90:len(X)])



