import yaml
from llm.llm_wrapper import LLMWrapper

class CoachAgent:
    def __init__(self):
        """
        Initialisiert den CoachAgent.
        Dieser Agent wird ein anderes Modell (llava) für die Bildanalyse verwenden.
        """
        # Wir erstellen eine separate Wrapper-Instanz für das Bild-Modell
        self.llm_wrapper = LLMWrapper(model_name='llava')
        try:
            with open('config/settings.yaml', 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            self.system_prompt = config['agent_roles'].get('coach', 'Du bist ein praktischer Coach, der bei Code hilft.')
            print("CoachAgent initialisiert.")
        except FileNotFoundError:
            print("Fehler: config/settings.yaml nicht gefunden. Nutze Standard-Prompt für Coach.")
            self.system_prompt = "Du bist ein praktischer Coach, der bei Code hilft."
        except Exception as e:
            print(f"Ein Fehler ist beim Laden der Konfiguration für den CoachAgent aufgetreten: {e}")
            self.system_prompt = "Du bist ein praktischer Coach, der bei Code hilft."

    def respond_with_image(self, user_prompt: str, image_path: str) -> str:
        """
        Antwortet auf eine Anfrage, die Text und ein Bild enthält.
        """
        print(f"CoachAgent antwortet auf: '{user_prompt}' mit Bild: {image_path}")
        # Rufe die spezielle Methode im Wrapper auf, die Bilder verarbeiten kann
        return self.llm_wrapper.get_response_with_image(self.system_prompt, user_prompt, image_path)
