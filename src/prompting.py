import ollama
import json

MODEL_OLLAMA = "llama3.2"

instructions = ["Improve this paragraph",
                "Improve this paragraph without changing the numbers or units.",
                "Improve this paragraph without changing any facts, figures, units, references, or proper names."]

def generate_improved_text(data, instructions, model):
    """Génère plusieurs réécritures via Ollama"""
    for article in data:
        p1 = article.get("Paragraphes", "")
        for i, instruction in enumerate(instructions):
            content = f"""
                        {instruction}
                        Return ONLY the improved paragraph.
                        Do NOT add explanations.
                        Do NOT add comments.
                        Do NOT add introductory sentences.
                        Output the rewritten text only.
                        If you add anything else, your answer is invalid.
                        Paragraph:
                        {p1}
                    """
            response = ollama.chat(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": content
                    }
                ],
            options = {
                "temperature": 0.3,  # sortie stable
                "num_predict": 512    # correspond environ à 500 mots
                     }
                )
            
            article[f"Rew{i+1}"] = response["message"]["content"].split("\n\n", 1)[-1]

    return data


    """Génère plusieurs réécritures pour un article"""
    p1 = article.get("Paragraphes", "")
    for i, instruction in enumerate(instructions):
        content = f"""
            {instruction}
            Return ONLY the improved paragraph.
            Do NOT add explanations.
            Do NOT add comments.
            Do NOT add introductory sentences.
            Output the rewritten text only.
            If you add anything else, your answer is invalid.
            Paragraph:
            {p1}
        """
        response = ollama.chat(
            model=model,
            messages=[{"role": "user", "content": content}],
            options={
                "temperature": 0.3,
                "num_predict": 512  
            }
        )
        article[f"Rew{i+1}"] = response["message"]["content"].split("\n\n", 1)[-1]
    return article
data = [
    {
        "Doi": "https://doi.org/10.57896/2024-tal-65_3_3",
        "Paragraphes": "A Hidden Markov Model (HMM) is a classical statistical model [32] that embodies a set of statistical assumptions concerning the generation of sample data (and similar data from a larger population). It is often used in NLP for tagging [33, 34]. It can be applied to speech recognition, part-of-speech tagging and various bioinformatics applications inter alia. Given an input sequence of n signs X = (x1, …, xn) and a possible output transliteration Y = (y1, …, yn), an HMM provides the probability p(X, Y). Thus, given a sequence of signs X = (x1, …, xn), we can choose the transliteration  that maximizes .",
        "Auteur": "Delphine Battistelli, Farah Benamara, Viviana Patti",
        "Date de publication": "2025",
        "URL": "https://aclanthology.org/2024.tal-3.4/",
        "Licence": "CC BY 4.0",
        "Domaine": "TALN"
    }
]

# with open("data/json/dataset_simple.json","r" , encoding='utf-8') as file:
#     data = json.load(file)

new_data = generate_improved_text(data, instructions, MODEL_OLLAMA)

with open('data/json/rewrites.json', 'w', encoding='utf-8') as f:
    json.dump(new_data, f, indent=4, ensure_ascii=False)