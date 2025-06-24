import yaml
from llm.llm_wrapper import LLMWrapper

class TeacherAgent:
    def __init__(self):
        """
        Initialisiert den TeacherAgent.
        """
        self.llm_wrapper = LLMWrapper()
        try:
            # Stelle sicher, dass der Pfad zur Konfigurationsdatei korrekt ist
            with open('config/settings.yaml', 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            # Lade die spezifische Rolle für den Lehrer
            self.system_prompt = config['agent_roles'].get('teacher', 'Du bist ein hilfreicher Lehrer.')
            print("TeacherAgent initialisiert mit System-Prompt.")
        except FileNotFoundError:
            print("Fehler: config/settings.yaml nicht gefunden. Nutze Standard-Prompt für Lehrer.")
            self.system_prompt = "Du bist ein hilfreicher Lehrer."
        except Exception as e:
            print(f"Ein Fehler ist beim Laden der Konfiguration für den TeacherAgent aufgetreten: {e}")
            self.system_prompt = "Du bist ein hilfreicher Lehrer."

    def respond(self, user_prompt: str) -> str:
        """
        Antwortet auf eine Nutzeranfrage aus der Perspektive des Lehrers.
        Diese Methode ist entscheidend und muss existieren.
        """
        print(f"TeacherAgent antwortet auf die Anfrage: '{user_prompt}'")
        return self.llm_wrapper.get_response(self.system_prompt, user_prompt)