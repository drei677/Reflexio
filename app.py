from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = "reflexio_secret_key_123" 

# ---------------------------
# BASE DE QUESTIONS (135)
# ---------------------------
# Format : "category_key": [ (question_text, [choice0,choice1,choice2,choice3], "CorrectLetter"), ... 15 items ...]
QUESTIONS = {
    "fonctions_relations": [
        ("Une fonction est…", ["Plusieurs sorties","Une seule sortie","Une droite verticale","Une suite"], "B"),
        ("L’équation d’une parabole est de la forme :", ["y = mx + b","y = ax^2 + bx + c","y = 1/x","y = a^3"], "B"),
        ("Le sommet d’une parabole représente :", ["Le point le plus haut ou le plus bas","Le point où la parabole coupe l'axe des x","Le centre d'un cercle","Le milieu d'un segment"], "A"),
        ("Une droite horizontale a une pente :", ["0","1","-1","Indéfinie"], "A"),
        ("Une droite verticale a une pente :", ["0","1","Indéfinie","-2"], "C"),
        ("Le domaine d'une fonction représente :", ["Les valeurs possibles de x","Les valeurs possibles de y","Le sommet","L'axe de symétrie"], "A"),
        ("L’image (range) représente :", ["Les valeurs possibles de x","Les valeurs possibles de y","Le coefficient directeur","L'ordonnée à l'origine"], "B"),
        ("Dans y = -3x + 5, la pente est :", ["-3","5","3","-5"], "A"),
        ("Une parabole concave vers le haut a a :", ["positif","négatif","nul","inconnu"], "A"),
        ("Une relation qui n'est pas une fonction :", ["Passe le test de la droite verticale","Ne passe PAS le test de la droite verticale","A une pente nulle","Est une parabole"], "B"),
        ("Si une droite monte de gauche à droite, sa pente est :", ["positive","négative","nulle","indéfinie"], "A"),
        ("Dans une table de valeurs, une fonction n'est pas valide si :", ["Deux x ont le même y","Deux x ont y différents","Un x se répète avec deux y","Toutes les y sont positives"], "C"),
        ("Le y-intercept correspond à :", ["L'intersection avec l'axe x","La pente","L'intersection avec l'axe y","La dérivée"], "C"),
        ("Une relation inverse est souvent de forme :", ["y = k/x","y = mx + b","y = ax^2","y = √x"], "A"),
        ("Si b augmente, la droite :", ["se déplace vers le haut","se déplace vers le bas","devient plus inclinée","devient plus horizontale"], "A"),
    ],

    "algebre": [
        ("3x + 5x = ?", ["3x²","8x","8","15x"], "B"),
        ("Développer (x + 3)(x + 2) donne :", ["x² + 5x + 6","x² + 6x + 5","x² + x + 6","5x + 6"], "A"),
        ("Factoriser x² - 9 donne :", ["(x + 3)²","(x - 3)²","(x + 3)(x - 3)","Impossible"], "C"),
        ("Si x + 7 = 15, x = ?", ["7","15","22","8"], "D"),
        ("2(3x - 4) = ?", ["6x - 8","5x - 4","6x + 8","2x - 4"], "A"),
        ("Si 5x = 40, x = ?", ["5","-5","8","200"], "C"),
        ("4a² - a² = ?", ["3a","3a²","a²","5a²"], "B"),
        ("Pour garder l'égalité dans une équation on doit :", ["Faire la même opération des deux côtés","Multiplier par 0","Toujours ajouter","Inverser les signes"], "A"),
        ("Factoriser x² + 7x + 12 donne :", ["(x + 4)(x + 3)","(x + 6)(x + 2)","(x + 12)(x - 1)","Impossible"], "A"),
        ("(x - 5)² = ?", ["x² - 25","x² + 25 - 10x","x² - 10x + 25","x² + 10x + 25"], "C"),
        ("7x⁰ vaut :", ["7","1","0","x"], "A"),
        ("2x - 3 = 11, x=?", ["8","1","7","11"], "C"), 
        ("Le terme constant de 4x² + 3x - 9 est :", ["4","3","-9","Aucun"], "C"),
        ("Une équation du 2e degré peut avoir :", ["une seule solution","toujours deux","0, 1 ou 2 solutions","aucune solution réelle"], "C"),
        ("PEMDAS commence par :", ["Multiplication","Parenthèses","Soustraction","Division"], "B"),
    ],

    "geo_analytique": [
        ("La pente entre (2,3) et (4,7) est :", ["2","3","4","1"], "A"),
        ("La distance entre deux points utilise le théorème de :", ["Thalès","Pythagore","Newton","Pascal"], "B"),
        ("La forme d'une équation de droite est :", ["y = mx + b","y = ax² + c","y = √x","y = k/x"], "A"),
        ("Le point milieu entre (0,0) et (4,4) est :", ["(4,4)","(2,2)","(1,1)","(8,8)"], "B"),
        ("Deux droites parallèles ont :", ["la même pente","des pentes opposées","une pente nulle","une pente indéfinie"], "A"),
        ("Deux droites perpendiculaires ont des pentes :", ["égales","multipliées par 2","opposées","inverses et négatives"], "D"),
        ("Si une droite descend, sa pente est :", ["positive","négative","0","indéfinie"], "B"),
        ("Le y-intercept correspond à :", ["le point où la droite touche l'axe x","le point où la droite touche l'axe y","le sommet","le point milieu"], "B"),
        ("Pour trouver la distance entre (x1,y1) et (x2,y2), on utilise :", ["√((x2-x1)² + (y2-y1)²)","x2-x1","|x| + |y|","(y2-y1)(x2-x1)"], "A"),
        ("Le point (0,b) représente :", ["un x-intercept","un y-intercept","la pente","l'origine"], "B"),
        ("Le point (a,0) représente :", ["un x-intercept","un y-intercept","la pente","le centre"], "A"),
        ("Une droite verticale a pour équation :", ["x = k","y = k","y = mx + b","x = y"], "A"),
        ("Une droite horizontale a pour équation :", ["x = k","y = k","y = mx + b","y = ax²"], "B"),
        ("Si deux points ont le même x, la droite est :", ["horizontale","verticale","parabolique","perpendiculaire"], "B"),
        ("Le plan cartésien est divisé en :", ["2 quadrants","3 quadrants","4 quadrants","6 quadrants"], "C"),
    ],

    "chimie": [
        ("Quelle loi dit que la masse des réactifs est égale à la masse des produits ?", ["Loi d'Ohm","Loi de Newton","Loi de conservation de la masse","Loi de Boyle"], "C"),
        ("Quelle particule détermine le numéro atomique ?", ["neutrons","protons","électrons de valence","masse atomique"], "B"),
        ("Le Cl⁻ est un exemple de :", ["cation","anion","molécule","isotope"], "B"),
        ("Une liaison covalente implique…", ["un transfert d'électrons","un partage d'électrons","une perte de protons","une fusion d'atomes"], "B"),
        ("Quelle est la formule correcte de l'eau ?", ["HO","H₂O","O₂H₂","O₂"], "B"),
        ("Lors d'une dilution, la concentration…", ["augmente","diminue","reste identique","devient nulle"], "B"),
        ("2H₂ + O₂ → 2H₂O. Combien de molécules d'eau sont produites ?", ["1","2","4","3"], "B"),
        ("Un changement chimique se reconnaît par…", ["un changement de forme","une nouvelle substance formée","un changement d'état","une augmentation de température seulement"], "B"),
        ("Le pH 2 est…", ["neutre","légèrement basique","fortement acide","légèrement acide"], "C"),
        ("L'ion Mg²⁺ a…", ["gagné 2 électrons","perdu 2 électrons","gagné 1 électron","perdu 1 électron"], "B"),
        ("Une solution très concentrée est :", ["riche en soluté","pauvre en soluté","pure","solide"], "A"),
        ("Le tableau périodique est organisé principalement selon :", ["le nombre de neutrons","la masse atomique","le numéro atomique","le nombre d'isotopes"], "C"),
        ("Quel changement indique un changement physique ?", ["formation d'un gaz","apparition d'un précipité","dissolution du sucre","changement de couleur"], "C"),
        ("Un isotope est…", ["un atome qui a perdu des protons","un atome avec un nombre différent de neutrons","un cation","une molécule"], "B"),
        ("La stœchiométrie permet de…", ["mesurer le pH","prévoir les quantités de produits","identifier les précipités","mesurer la masse atomique"], "B"),
    ],

    "physique": [
        ("La relation de la loi d'Ohm est :", ["P = VI","V = IR","I = Pt","R = Vt"], "B"),
        ("L'unité de résistance est :", ["Volt","Ampère","Ohm","Watt"], "C"),
        ("Dans un circuit en série, le courant…", ["est le même partout","se divise","est nul","dépend du fil utilisé"], "A"),
        ("Une augmentation de tension provoque :", ["baisse du courant","hausse du courant","zéro courant","aucune différence"], "B"),
        ("Dans une lentille convergente, l'image peut être…", ["seulement virtuelle","seulement réelle","réelle ou virtuelle","inexistante"], "C"),
        ("La fréquence se mesure en :", ["watts","joules","hertz","ohms"], "C"),
        ("Le courant électrique correspond à…", ["un mouvement de protons","un mouvement d'électrons","un mouvement de neutrons","un mouvement de molécules"], "B"),
        ("Quelle grandeur représente une différence de potentiel ?", ["Le courant","La tension","La charge","La résistance"], "B"),
        ("Une ampoule en parallèle sur une autre…", ["réduit l'éclat total","augmente le courant dans chaque ampoule","reste allumée si l'autre brûle","ne fonctionne pas"], "C"),
        ("Une onde mécanique nécessite :", ["un milieu matériel","le vide","un conducteur","une charge"], "A"),
        ("Quand la fréquence d'une onde augmente…", ["la longueur d'onde augmente","la longueur d'onde diminue","l'amplitude double","rien ne change"], "B"),
        ("La puissance électrique se calcule avec :", ["P = VI","P = IR","P = V/t","P = I²R"], "A"),
        ("Le son est…", ["une onde électromagnétique","une onde mécanique","une onde lumineuse","une onde thermique"], "B"),
        ("La réfraction se produit quand…", ["une onde rebondit","une onde change de milieu","une onde est absorbée","une onde disparaît"], "B"),
        ("Une lentille divergente…", ["rapproche les rayons","les éloigne","les réfléchit","ne change rien"], "B"),
    ],

    "biologie": [
        ("L'ADN se trouve dans…", ["le cytoplasme","le noyau","la membrane","les ribosomes"], "B"),
        ("Une cellule qui se divise en deux cellules identiques fait…", ["la méiose","la mitose","la fécondation","la duplication"], "B"),
        ("Un gène correspond à…", ["un chromosome entier","un segment d'ADN","une protéine","un organe"], "B"),
        ("Le génotype correspond…", ["à l'apparence physique","aux gènes","au comportement","à la reproduction"], "B"),
        ("La photosynthèse produit…", ["CO₂","O₂","N₂","H₂"], "B"),
        ("Quel organite produit l'énergie (ATP) ?", ["Chloroplaste","Réticulum","Mitochondrie","Appareil de Golgi"], "C"),
        ("Les chromosomes sont composés de…", ["lipides","ADN","protéines","acides aminés"], "B"),
        ("Les allèles dominants s'écrivent :", ["en minuscules","en majuscules","avec des chiffres","en double"], "B"),
        ("La respiration cellulaire nécessite :", ["CO₂ et eau","O₂ et glucose","N₂ et énergie","lipides et chaleur"], "B"),
        ("Un écosystème inclut…", ["seulement les êtres vivants","seulement les non-vivants","vivants + non-vivants","uniquement les plantes"], "C"),
        ("La méiose permet de produire :", ["des cellules identiques","des cellules haploïdes","des cellules diploïdes","des cellules somatiques"], "B"),
        ("Un producteur dans un écosystème est…", ["un animal","une plante","un décomposeur","un prédateur"], "B"),
        ("La sélection naturelle est liée à…", ["la reproduction asexuée","la survie des individus les mieux adaptés","la fécondation interne","la diversité chromosomique"], "B"),
        ("La chromatine se condense pour devenir…", ["un chloroplaste","un ribosome","un chromosome","un gène"], "C"),
    ],

    "histoire_1760_1867": [
        ("En quelle année a lieu la Conquête britannique ?", ["1759","1760","1763","1774"], "B"),
        ("Quel traité met fin à la guerre de Sept Ans ?", ["Acte de Québec","Traité de Versailles","Traité de Paris","Acte constitutionnel"], "C"),
        ("L'Acte de Québec (1774) accorde aux Canadiens :", ["l'anglais obligatoire","la liberté de religion","la conscription","le droit de vote pour les femmes"], "B"),
        ("Quel événement influence l'Acte de Québec ?", ["la Révolution américaine","les Rébellions","l'industrialisation","la Confédération"], "A"),
        ("L'Acte constitutionnel de 1791 divise :", ["les États-Unis","le Haut-Canada et le Bas-Canada","l'Ouest et l'Est","le parlement britannique"], "B"),
        ("Les Rébellions de 1837-1838 sont liées à :", ["trop d'immigrants","manque de terres","conflits politiques entre députés et gouverneurs","problèmes militaires"], "C"),
        ("Qui rédige le Rapport Durham ?", ["Louis-Joseph Papineau","John A. Macdonald","Lord Durham","Georges-Étienne Cartier"], "C"),
        ("Que propose Durham ?", ["diviser le Canada en trois","la Confédération immédiate","l'assimilation des Canadiens français","l'indépendance"], "C"),
        ("Quel est l'objectif de l'Acte d'Union (1840) ?", ["unir les Provinces maritimes","punir les loyalistes","unir le Haut et le Bas-Canada","séparer les francophones et anglophones"], "C"),
        ("Le gouvernement responsable est obtenu en :", ["1791","1840","1848","1867"], "C"),
        ("La première phase d'industrialisation repose surtout sur :", ["le textile et le bois","le pétrole","l'aluminium","l'aérospatial"], "A"),
        ("Quel moyen de transport devient important vers 1850 ?", ["avion","métro","train","automobile"], "C"),
        ("Pourquoi veut-on la Confédération en 1867 ?", ["les USA menacent d'envahir","le bois manque","les taxes sont trop basses","le Canada veut éliminer la monnaie"], "A"),
        ("Quel homme joue un rôle central dans la Confédération ?", ["Papineau","Laurier","Macdonald","Durham"], "C"),
        ("La date de la Confédération est :", ["1848","1867","1875","1880"], "B"),
    ],

    "histoire_1867_1945": [
        ("La Politique nationale est lancée par :", ["Wilfrid Laurier","John A. Macdonald","Louis Riel","Mackenzie King"], "B"),
        ("La Politique nationale inclut :", ["une taxe scolaire","des tarifs douaniers","la conscription","l'interdiction d'immigration"], "B"),
        ("Quel peuple est particulièrement touché par les politiques de l'Ouest ?", ["les Inuit","les Premières Nations","les Italiens","les Loyalistes"], "B"),
        ("La deuxième phase d'industrialisation repose sur :", ["bois & textile","aluminium, pâtes et papiers, mines","agriculture seulement","rien"], "B"),
        ("La Première Guerre mondiale commence en :", ["1898","1905","1914","1918"], "C"),
        ("Quelle bataille est liée au Canada durant la Première Guerre mondiale ?", ["Vimy","Normandie","Hong Kong","Dieppe"], "A"),
        ("La crise de la conscription au Canada a lieu en :", ["1914","1917","1929","1939"], "B"),
        ("La crise économique de 1929 commence avec :", ["une guerre","le krach boursier","une révolution","une épidémie"], "B"),
        ("Les années 1930 sont marquées par :", ["du plein emploi","du chômage élevé","un boom économique","une grande immigration"], "B"),
        ("La Seconde Guerre mondiale débute en :", ["1929","1933","1939","1945"], "C"),
        ("Le Canada participe fortement à la bataille :", ["D'Ortona","D'Hiroshima","De Stalingrad","De Pearl Harbor"], "A"),
        ("En 1944, il y a :", ["un 2e référendum","une crise de la conscription","une rébellion","une révolution sociale"], "B"),
        ("Durant la Seconde Guerre mondiale, les femmes :", ["perdent le droit de vote","travaillent massivement en usine","sont exclues des emplois","sont envoyées au front en majorité"], "B"),
        ("Quel premier ministre est associé à la Seconde Guerre mondiale ?", ["Macdonald","St-Laurent","Borden","Mackenzie King"], "D"),
        ("Le Canada finit la Seconde Guerre mondiale en :", ["1943","1945","1947","1950"], "B"),
    ],

    "histoire_1945_aujourdhui": [
        ("Quelle période suit immédiatement 1945 ?", ["Le Baby-boom","Le Moyen Âge","La Grande Noirceur","La Révolution tranquille"], "A"),
        ("Maurice Duplessis est associé à :", ["la laïcisation","l'État-providence","la Grande Noirceur","les référendums"], "C"),
        ("La Révolution tranquille débute en :", ["1940","1955","1960","1970"], "C"),
        ("Un élément majeur de la Révolution tranquille est :", ["l'industrialisation","la nationalisation de l'électricité","le retour à l'agriculture","la prohibition"], "B"),
        ("Quel parti est lié à l'indépendantisme québécois ?", ["PLQ","PC","PQ","Alliance"], "C"),
        ("Le premier référendum a lieu en :", ["1967","1976","1980","1995"], "C"),
        ("La crise d'Oka se déroule en :", ["1960","1972","1990","2002"], "C"),
        ("Quel phénomène marque le Québec après 1945 ?", ["la dépopulation","la baisse de natalité après le baby-boom","le retour au féodalisme","l'interdiction d'immigration"], "B"),
        ("Quel premier ministre est lié à la Charte canadienne en 1982 ?", ["Trudeau père","Mulroney","Bourassa","Lévesque"], "A"),
        ("En 1995, le camp du Oui obtient environ :", ["20 %","35 %","49 %","60 %"], "C"),
        ("La mondialisation entraîne :", ["moins de commerce","plus d'échanges économiques","la fin de l'industrie","l'abolition des frontières"], "B"),
        ("L'ALÉNA est un accord entre :", ["Canada–France–Belgique","Canada–USA–Mexique","Québec–Ontario–Colombie","USA–Chine–Japon"], "B"),
        ("Quel secteur est central dans l'économie moderne du Québec ?", ["Mines seulement","Technologie & services","Agriculture seulement","Or et argent uniquement"], "B"),
        ("Quel problème environnemental est devenu très important ?", ["Disparition du froid","Réchauffement climatique","Surplus de neige","Augmentation des continents"], "B"),
        ("L'immigration moderne au Québec vise surtout :", ["Des travailleurs qualifiés","Des agriculteurs seulement","Des enfants uniquement","Des touristes"], "A"),
    ],
}

# Mapping pour les sous-catégories (pour l'interface)
SUBJECT_MAP = {
    "math": [
        ("Fonctions & relations", "fonctions_relations"),
        ("Algèbre", "algebre"),
        ("Géométrie analytique", "geo_analytique"),
    ],
    "science": [
        ("Chimie", "chimie"),
        ("Physique", "physique"),
        ("Biologie", "biologie"),
    ],
    "histoire": [
        ("1760–1867", "histoire_1760_1867"),
        ("1867–1945", "histoire_1867_1945"),
        ("1945–aujourd'hui", "histoire_1945_aujourdhui"),
    ]
}

# ---------------------------
# ROUTES
# ---------------------------

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/categories/<subject>")
def categories(subject):
    if subject not in SUBJECT_MAP:
        return "Sujet inconnu.", 404
    return render_template("categories.html", subject=subject, subs=SUBJECT_MAP[subject])

@app.route("/start_quiz/<category_key>")
def start_quiz(category_key):
    if category_key not in QUESTIONS:
        return "Catégorie inconnue.", 404

    pool = QUESTIONS[category_key]
    selected = random.sample(pool, 5) if len(pool) >= 5 else pool.copy()

    # initialiser session
    session["category_key"] = category_key
    session["questions"] = selected
    session["current"] = 0
    session["answers_letters"] = []   # stocke les lettres A/B/C/D
    session["answers_texts"] = []     # stocke le texte choisi (pour affichage final)
    session["last_feedback"] = None   # utilisé pour afficher feedback après réponse

    return redirect(url_for("question"))

@app.route("/question", methods=["GET", "POST"])
def question():
    # sécurité
    if "questions" not in session:
        return redirect(url_for("index"))

    questions = session["questions"]
    current = session.get("current", 0)

    # POST = l'utilisateur a cliqué "Répondre" (action=answer) ou "Prochain" (action=next)
    if request.method == "POST":
        action = request.form.get("action")

        if action == "answer":
            # on enregistre la réponse mais on ne passe pas à la question suivante (pour montrer feedback)
            chosen_letter = request.form.get("choice")  # A/B/C/D
            if not chosen_letter:
                # pas de choix — on redemande la même page
                return redirect(url_for("question"))

            # stocke lettre et texte
            idx = "ABCD".index(chosen_letter)
            q_text, choices, correct_letter = questions[current]
            chosen_text = choices[idx]

            session["answers_letters"].append(chosen_letter)
            session["answers_texts"].append(chosen_text)

            is_correct = (chosen_letter == correct_letter)
            # préparer feedback (sera affiché sur la même page)
            session["last_feedback"] = {
                "is_correct": is_correct,
                "chosen_letter": chosen_letter,
                "chosen_text": chosen_text,
                "correct_letter": correct_letter,
                "correct_text": choices["ABCD".index(correct_letter)]
            }

            # renderer la page GET avec feedback (donc ne pas incrémenter current)
            return redirect(url_for("question"))

        elif action == "next":
            # incrémenter la question
            session["current"] = current + 1
            session["last_feedback"] = None

            # si terminé → résultat
            if session["current"] >= len(session["questions"]):
                return redirect(url_for("result"))
            else:
                return redirect(url_for("question"))

    # GET : afficher la question courante (et feedback s'il y a)
    current = session.get("current", 0)
    if current >= len(session["questions"]):
        return redirect(url_for("result"))

    q_text, choices, correct_letter = session["questions"][current]
    feedback = session.get("last_feedback")

    return render_template(
        "question.html",
        qnum=current + 1,
        total=len(session["questions"]),
        question_text=q_text,
        choices=choices,
        feedback=feedback
    )

@app.route("/result")
def result():
    if "questions" not in session:
        return redirect(url_for("index"))

    questions = session["questions"]
    letters = session.get("answers_letters", [])
    texts = session.get("answers_texts", [])

    corrections = []
    score = 0
    for i in range(len(questions)):
        q_text, choices, correct_letter = questions[i]
        user_letter = letters[i] if i < len(letters) else None
        user_text = texts[i] if i < len(texts) else None
        correct_text = choices["ABCD".index(correct_letter)]
        is_correct = (user_letter == correct_letter)
        if is_correct:
            score += 1
        corrections.append({
            "question": q_text,
            "user_letter": user_letter,
            "user_text": user_text,
            "correct_letter": correct_letter,
            "correct_text": correct_text,
            "is_correct": is_correct
        })

    # Nettoyer la session après affichage (optionnel)
    # session.clear()

    return render_template("result.html", score=score, total=len(questions), corrections=corrections)

# ---------------------------
# Lancer l'app
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)

