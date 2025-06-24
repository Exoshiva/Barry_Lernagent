import yaml
from llm.llm_wrapper import LLMWrapper
# Importiert die neuen Datenbank-Helferfunktionen
from db.database_helpers import get_all_progress, update_progress_status, add_new_topic

class ManagerAgent:
    def __init__(self):
        """
        Initialisiert den ManagerAgent.
        """
        # Der Manager nutzt den Standard-Text-Wrapper für seine Antworten
        self.llm_wrapper = LLMWrapper(model_name='mistral')
        try:
            with open('config/settings.yaml', 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            self.system_prompt = config['agent_roles'].get('manager', 'Du bist ein Lern-Manager, der Wissen organisiert.')
            print("ManagerAgent initialisiert.")
        except Exception as e:
            print(f"Fehler bei der Initialisierung des ManagerAgent: {e}")
            self.system_prompt = "Du bist ein Lern-Manager, der Wissen organisiert."

    def show_progress(self) -> str:
        """
        Ruft den Lernfortschritt aus der Datenbank ab und formatiert ihn als Text.
        """
        print("ManagerAgent: Rufe Lernfortschritt ab...")
        progress_items = get_all_progress()
        
        if not progress_items:
            return "Ich konnte keinen Lernfortschritt in der Datenbank finden. Sieht aus, als hättest du noch nicht angefangen."

        # Formatiere die Datenbank-Ergebnisse in einen schönen, lesbaren Text.
        response_text = "Hier ist dein aktueller Lernfortschritt:\n\n"
        for item in progress_items:
            status_de = self._translate_status(item['status'])
            response_text += f"- **Thema:** {item['topic']}\n  - **Status:** {status_de}\n"
            
        return response_text

    def mark_as_completed(self, topic: str) -> str:
        """
        Versucht, ein Thema als 'abgeschlossen' zu markieren und gibt eine Bestätigung zurück.
        """
        print(f"ManagerAgent: Versuche, '{topic}' als abgeschlossen zu markieren...")
        success = update_progress_status(topic, 'completed')
        
        if success:
            return f"Super! Ich habe das Thema '{topic}' für dich als abgeschlossen markiert. Tolle Arbeit!"
        else:
            return f"Entschuldigung, ich konnte das Thema '{topic}' nicht als abgeschlossen markieren. Überprüfe bitte, ob der Themenname korrekt ist."

    def add_topic(self, topic: str) -> str:
        """
        Fügt ein neues Lernthema hinzu und gibt eine Bestätigung zurück.
        """
        print(f"ManagerAgent: Füge neues Thema '{topic}' hinzu...")
        success = add_new_topic(topic)
        if success:
            return f"Alles klar, ich habe das neue Lernthema '{topic}' zu deinem Plan hinzugefügt."
        else:
            return f"Entschuldigung, beim Hinzufügen von '{topic}' ist ein Fehler aufgetreten."

    def _translate_status(self, status: str) -> str:
        """Eine private Hilfsfunktion, um den Datenbank-Status zu übersetzen."""
        translations = {
            'not_started': 'Noch nicht begonnen',
            'in_progress': 'In Bearbeitung',
            'completed': 'Abgeschlossen'
        }
        return translations.get(status, 'Unbekannt')

    def respond(self, user_prompt: str) -> str:
        """
        Analysiert die Nutzeranfrage und entscheidet, welche Aktion ausgeführt werden soll.
        """
        prompt_lower = user_prompt.lower()
        
        # Logik zum Anzeigen des Fortschritts
        if "fortschritt" in prompt_lower or "status" in prompt_lower or "stand" in prompt_lower:
            return self.show_progress()
            
        # Logik zum Hinzufügen eines neuen Themas
        if "hinzufügen" in prompt_lower or "füge" in prompt_lower or "neues thema" in prompt_lower:
            try:
                # Extrahiert das Thema aus dem Prompt (einfache Methode)
                topic_to_add = prompt_lower.split("thema")[-1].strip()
                if "hinzufügen" in topic_to_add:
                    topic_to_add = topic_to_add.replace("hinzufügen", "").strip()
                return self.add_topic(topic_to_add.capitalize())
            except Exception:
                return "Ich habe nicht verstanden, welches Thema ich hinzufügen soll. Bitte sage z.B.: 'Füge das Thema Datenbanken hinzu'."

        # Logik zum Abschließen eines Themas
        if "abgeschlossen" in prompt_lower or "fertig mit" in prompt_lower:
            try:
                # Extrahiert das Thema aus dem Prompt (einfache Methode)
                topic_to_update = prompt_lower.split("markiere")[-1].split("als")[0].strip()
                
                # Finde das Thema in der Datenbank (unabhängig von Groß-/Kleinschreibung)
                known_topics = [item['topic'] for item in get_all_progress()]
                found_topic = next((t for t in known_topics if t.lower() == topic_to_update.lower()), None)
                
                if found_topic:
                    return self.mark_as_completed(found_topic)
                else:
                    return f"Ich kenne das Thema '{topic_to_update}' nicht. Du kannst es zuerst mit 'Füge das Thema ... hinzu' anlegen."
            except Exception:
                 return "Ich bin mir nicht sicher, welches Thema du meinst. Bitte formuliere es so: 'Markiere [Themenname] als abgeschlossen'."

        # Standardantwort, wenn keine Aktion erkannt wird
        return "Ich bin der Manager. Du kannst mich nach deinem Fortschritt fragen, Themen als abgeschlossen markieren oder neue Themen hinzufügen."
