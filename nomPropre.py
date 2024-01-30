import re
from collections import Counter
import nltk
# nltk.download('punkt')

# Définition de la fonction kwic pour le concordancier
def kwic(terme, taille_contexte, chemin_fichier):
    # Ouverture et lecture du fichier
    with open(chemin_fichier, 'r') as fichier:
        texte = fichier.read()
        mots = texte.split()

        # Parcours de chaque mot dans le texte
        for i, mot in enumerate(mots):
            # Vérification si le mot courant correspond au terme recherché
            if mot.lower() == terme.lower():
                # Extraction du contexte gauche
                contexte_gauche = ' '.join(mots[max(i - taille_contexte, 0):i])
                # Extraction du contexte droit
                contexte_droit = ' '.join(mots[i + 1:i + 1 + taille_contexte])
                # Affichage du terme avec son contexte
                print(f"{contexte_gauche} \033[1m{mot}\033[0m {contexte_droit}")

def add_capitalized_words(text):
    capitalized_words = Counter()
    mots = nltk.word_tokenize(text)
    for word in mots:
        if word.istitle():
            if len(word) > 1:
                capitalized_words[word] += 1
    return capitalized_words

def add_first_words(text):
    first_words = Counter()
    sentences = nltk.sent_tokenize(text)
    print(sentences)
            
    for sentence in sentences:
        words = nltk.word_tokenize(sentence)


        
        first_words[words[0]] += 1
    return first_words



# Point d'entrée principal du script
if __name__ == "__main__":
    filename = "Miserables1.txt"
    with open(filename, 'r', encoding='utf-8-sig') as file:
        text = file.read()

        lines = text.split('\n')
        for i in range(len(lines)):
            if lines[i].startswith('Chapitre') or lines[i].startswith('Livre') or lines[i].startswith('Tome') or lines[i].startswith('TABLE') or lines[i].startswith('LES'):
                lines[i] += '.'
            if lines[i].startswith('Chapitre'):
                lines[i+2] += '.'
        text = '\n'.join(lines)

        text = re.sub(r'(Chapitre \w+)', lambda match: match.group(1) + '.', text)

        text = re.sub(r'([.!?:;"])', " . ", text)
        text = re.sub(re.compile(r'_(.)'), lambda match: '' + match.group(1), text)
        text = re.sub(re.compile(r'(.)_'), lambda match: match.group(1) + ' . ', text)
        text = re.sub(r'--', " . ", text)
        text = re.sub(r'>>', " ", text)
        text = re.sub(r'»', " ", text)
        text = re.sub(r'<<', " ", text)
        text = re.sub(r'«', " ", text)
        
    capitalized_words = add_capitalized_words(text)
    first_words = add_first_words(text)

    first_capitalized = Counter()
    first_capitalized = first_words & capitalized_words

    middle_capitalized = Counter()
    middle_capitalized = capitalized_words - first_words

    proper_noun = middle_capitalized + (middle_capitalized & first_words)
    
    with open('result.txt', 'w') as f:
        for word, freq in proper_noun.most_common():
            f.write(f"{word}: {freq}\n")


    # exemple d'appel de la fonction kwic avec les paramètres spécifiés
    # kwic('La', 5, 'Miserables1.txt')