import ollama
import yaml
import base64

class LLMWrapper:
    def __init__(self, model_name=None):
        """
        Initialisiert den LLMWrapper. Kann optional einen spezifischen Modellnamen annehmen.
        """
        try:
            with open('config/settings.yaml', 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            # Wenn ein Modellname übergeben wird, nutze diesen. Sonst den aus der Config.
            self.model = model_name if model_name is not None else config.get('model', 'mistral')
            self.temperature = config.get('temperature', 0.7)
            print(f"LLM Wrapper initialisiert für Modell '{self.model}'.")
        except Exception as e:
            print(f"Fehler beim Laden der Konfiguration: {e}")
            self.model = model_name if model_name is not None else 'mistral'
            self.temperature = 0.7

    def get_response(self, system_prompt: str, user_prompt: str) -> str:
        """
        Sendet eine reine Text-Anfrage an das Ollama-Modell.
        """
        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': user_prompt},
                ]
            )
            return response['message']['content']
        except Exception as e:
            print(f"Fehler bei der Kommunikation mit Ollama (Text): {e}")
            return "Entschuldigung, es gab einen Fehler bei der Textverarbeitung."

    def get_response_with_image(self, system_prompt: str, user_prompt: str, image_path: str) -> str:
        """
        Sendet eine Anfrage mit Text und Bild an ein multimodales Ollama-Modell (wie llava).
        """
        try:
            with open(image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

            response = ollama.chat(
                model=self.model,
                messages=[
                    {
                        'role': 'user',
                        'content': user_prompt,
                        'images': [encoded_string]
                    },
                     {
                        'role': 'system',
                        'content': system_prompt,
                    }
                ]
            )
            return response['message']['content']
        except Exception as e:
            print(f"Fehler bei der Kommunikation mit Ollama (Bild): {e}")
            return "Entschuldigung, es gab einen Fehler bei der Bildverarbeitung."

