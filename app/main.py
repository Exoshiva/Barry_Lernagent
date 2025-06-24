import gradio as gr
import time
from agents.teacher import TeacherAgent
from agents.coach import CoachAgent
from agents.manager import ManagerAgent
from db.init_db import init_db

# Datenbank initialisieren
init_db()

# Wir initialisieren ALLE Agenten beim Start
print("Initialisiere Agenten...")
try:
    teacher = TeacherAgent()
    coach = CoachAgent()
    manager = ManagerAgent()
    print("Agenten erfolgreich initialisiert.")
except Exception as e:
    print(f"Fehler bei der Initialisierung der Agenten: {e}")
    teacher = None
    coach = None
    manager = None

def barry_responds(history, image_path):
    """
    Die zentrale Logik-Funktion, die Anfragen an den richtigen Agenten weiterleitet.
    """
    user_message = history[-1][0] if history else ""
    
    management_keywords = ['fortschritt', 'status', 'stand', 'abgeschlossen', 'fertig mit', 'gelernt', 'hinzufügen', 'füge', 'neues thema']
    is_management_task = any(keyword in user_message.lower() for keyword in management_keywords)
    
    if is_management_task:
        if not manager:
            history[-1][1] = "Fehler: Der ManagerAgent ist nicht verfügbar."
            return history, None
        response = manager.respond(user_message)
    elif image_path:
        if not coach:
            history[-1][1] = "Fehler: Der CoachAgent ist nicht verfügbar."
            return history, None
        response = coach.respond_with_image(user_message, image_path)
    else:
        if not teacher:
            history[-1][1] = "Fehler: Der TeacherAgent ist nicht verfügbar."
            return history, None
        response = teacher.respond(user_message)

    history[-1][1] = ""
    for char in response:
        history[-1][1] += char
        time.sleep(0.01)
        yield history, None # Wichtig: Gibt None zurück, um die Bild-Vorschau zu leeren

def add_message_to_history(user_message, history):
    """Fügt die Nachricht des Benutzers sofort dem Chatverlauf hinzu."""
    return history + [[user_message, None]]

def clear_textbox():
    """Leert die Textbox nach dem Senden."""
    return ""

# Aufbau der neuen, klar gegliederten Benutzeroberfläche
with gr.Blocks(css="static/css/style.css", theme=gr.themes.Base(), title="Barry") as app:
    
    with gr.Column(elem_id="app-container"):
        # --- HEADER-BLOCK ---
        with gr.Row(elem_id="header-container"):
            gr.Image("static/images/barry.png", height=40, width=40, show_label=False, interactive=False, elem_id="header-avatar")
            gr.Markdown("<h1 id='header-title'>Barry</h1>")
        
        # --- CHAT-FENSTER-BLOCK ---
        chatbot = gr.Chatbot(
            [],
            elem_id="chatbot",
            avatar_images=(None, "static/images/barry.png") 
        )

        # --- EINGABE-BLOCK ---
        with gr.Column(elem_id="input-container"):
             with gr.Row(elem_id="input-area"):
                # --- HIER DIE ÄNDERUNG: gr.Image statt UploadButton ---
                # Diese Komponente zeigt eine Vorschau an.
                image_box = gr.Image(type="filepath", elem_id="image-upload-box", height=80, width=80)

                with gr.Column(scale=4, elem_classes="input-text-container"):
                    txt = gr.Textbox(
                        show_label=False,
                        placeholder="Sende eine Nachricht an Barry...",
                        container=False,
                    )
                    submit_btn = gr.Button("➤", elem_id="submit-button")

    # Event-Logik
    txt.submit(
        add_message_to_history, [txt, chatbot], [chatbot]
    ).then(
        clear_textbox, [], [txt]
    ).then(
        barry_responds, [chatbot, image_box], [chatbot, image_box]
    )
    
    submit_btn.click(
        add_message_to_history, [txt, chatbot], [chatbot]
    ).then(
        clear_textbox, [], [txt]
    ).then(
        barry_responds, [chatbot, image_box], [chatbot, image_box]
    )
    
    chat_state = gr.State([])
    chat_state.change(lambda x: x, chat_state, chatbot, queue=False)

if __name__ == "__main__":
    print("Starte Gradio-Interface...")
    app.launch()
