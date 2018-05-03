import sys

input = sys.argv[1]
maxFnameLen = 40 # nb de caractères max dans le prénom
lettersToReplace = "ÀÁÂÃÄÅàáâãäåÒÓÔÕÖØòóôõöøÈÉÊËèéêëÌÍÎÏìíîïÙÚÛÜùúûüÿÑñÇç";
replacementletters = "AAAAAAaaaaaaOOOOOOooooooEEEEeeeeIIIIiiiiUUUUuuuuyNnCc";

for i in range(0, len(lettersToReplace)):
    input = input.replace(lettersToReplace[i], replacementletters[i])

# si prénom trop long on fait planter
if (len(input) > maxFnameLen):
    print("Too big name detected : " + input)
    sys.exit()
fnameAdj = '{0: <{l}}'.format(input[::], l=maxFnameLen)[0:maxFnameLen].upper()
result = []
for c in fnameAdj:
    v = 1 + ord(c) - ord('A')
    if v < 0:
        v = 0
    result.append(v)
print(result)