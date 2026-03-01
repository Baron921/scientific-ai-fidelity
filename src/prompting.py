import ollama
from openai import OpenAI
import json
import nltk

# Configuration
client_openai = OpenAI(api_key="VOTRE_CLE_API_OPENAI")
MODEL_OLLAMA = "llama3"
MODEL_JUDGE = "gpt-4o"

def calculate_edit_ratio(p1, p2):
    """Calcule le taux de modification entre la source et la prédiction"""
    distance = nltk.edit_distance(p1, p2)
    ratio = 1 - (distance / max(len(p1), len(p2)))
    return round(ratio, 2)

def generate_improved_text(data, instructions, model):
    """Génère P2 via Ollama"""
    for article in data:
        p1 = article["Paragraphes"]
        for i,instruction in enumerate(instructions):
            llm_rewrite = ollama.chat(
                model=model, 
                messages=[
                        {
                            'role': 'user', 
                            'content': f"{instruction}\n\n Source paragraph : {p1}"
                        }
                        ]
            )
            article[f"Rew{i+1}"] = llm_rewrite['message']['content']

    return data

def llm_judge(p1, p2):
    """Juge le passage de P1 à P2 via GPT-4o"""
    prompt_judge = f"""
    En tant qu'expert en linguistique, compare le texte original (P1) et sa version améliorée (P2).
    
    P1 : "{p1}"
    P2 : "{p2}"
    
    Évalue sur 5 et réponds en JSON :
    1. gain_qualite (P2 est-il mieux écrit, plus clair ?)
    2. fidelite (Le sens de P1 est-il conservé ?)
    3. analyse (Courte explication)
    """
    
    response = client_openai.chat.completions.create(
        model=MODEL_JUDGE,
        messages=[{"role": "user", "content": prompt_judge}],
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)

# --- TEST ---
instructions = ["Improve this paragraph",
                "Improve this paragraph without changing the numbers or units.",
                "Improve this paragraph without changing any facts, figures, units, references, or proper names."]

""" with open("data/json/dataset_simple.json","r", encoding='utf-8') as file:
    data = json.load(file) """
data = [
    # {
    #     "Doi": "https://doi.org/10.57896/2024-tal-65_3_3",
    #     "Paragraphes": "For training, we use state-of-the-art encoder and decoder models developed for German. As encoders, we selected three pre-trained BERT (Devlin et al., 2018) models as many previous text classification experiments make use of Transformer-based architectures (Risch et al., 2021) which have been shown to be more effective than other approaches (Struß et al., 2019). We use the base versions of the cased 10 and uncased 11 pre-trained Digitale Bibliothek Münchener Digitalisierungszentrum (DBMDZ) BERT models. The two models were trained on Wikipedia, the EU Bookshop corpus, Open Subtitles, CommonCrawl, ParaCrawl and News Crawl. Additionally, we use Deepset’s base version of the German BERT model called GBERT 12 (Chan et al., 2020).",
    #     "Auteur": "Delphine Battistelli, Farah Benamara, Viviana Patti",
    #     "Date de publication": "2025",
    #     "URL": "https://aclanthology.org/2024.tal-3.4/",
    #     "Licence": "CC BY 4.0",
    #     "Domaine": "TALN"
    # },
    {
        "Doi": "https://doi.org/10.57896/2024-tal-65_3_1",
        "Paragraphes": "Cyberbullying can take many forms, with verbal abuse being prevalent among them. It may include harassment, which involves sending repetitive and offensive messages to a target, cyberstalking (sending repetitive threatening communications), flaming, which entails sending messages containing abusive and vulgar terms such as insults, gossip, or mockery, and denigration (Bauman, 2014; Tokunaga, 2010; Watts et al., 2017). Five types commonly encountered in written language are annotated here, and these are exclusively assigned to messages identified as OAG or CAG: 1.B 1.1 Blaming (BLM): This involves making the individual believe they are responsible for the abuse they are experiencing, attributing it to their actions, words, or behavior. Example: “on la traiterait pas de truie si elle avait pas autant de graisse” (“she wouldn’t be called a pig if she didn’t have so much fat”). 1.B 1.2 Name-calling (NCG): Refers to abusive, insulting, or derogatory language aimed at undermining the self-esteem, personal worth, and self-perception of the targeted individual. Example: “té qu1 putain de mongol” (“you’re such a fucking retard”).1.B 1.3 Threat (THR): These statements are intended to intimidate, control, or manipulate the victim, coercing them into submission. Example: “je vais venir en bas de chez toi, tu vas voir qui va plus parler” (“I’m going to come to your house, and you’ll see who won’t be talking anymore”). 1.B 1.4 Denigration (DNG): Disparaging remarks aimed at attacking the reputation of the targeted person, belittling, discrediting, and tarnishing their image. These remarks are deliberately hurtful, non-constructive, and malicious. Example: “les filles comme toi, ça me dégoûte” (“girls like you disgust me”). 1.B 1.5 Other aggression (OTH): Covers content that includes deliberately harmful, abusive, insulting, or derogatory language that does not align with the other defined categories. Example: “va crevé en enfer” (“go die in hell”).",
        "Auteur": "Delphine Battistelli, Farah Benamara, Viviana Patti",
        "Date de publication": "2025",
        "URL": "https://aclanthology.org/2024.tal-3.2/",
        "Licence": "CC BY 4.0",
        "Domaine": "TALN"
    }]

new_data = generate_improved_text(data, instructions, MODEL_OLLAMA)
with open('data/json/rewrites.json', 'w', encoding='utf-8') as f:
    json.dump(new_data, f, indent=4, ensure_ascii=False)