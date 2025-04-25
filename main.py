from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
import base64
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

class EmailForm(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.nome_input = TextInput(hint_text='Seu Nome', multiline=False)
        self.numero_input = TextInput(hint_text='Seu Número +55...', multiline=False)
        self.msg_label = Label(text='')
        self.send_button = Button(text='Enviar E-mail')
        self.send_button.bind(on_press=self.enviar_email)

        self.add_widget(self.nome_input)
        self.add_widget(self.numero_input)
        self.add_widget(self.send_button)
        self.add_widget(self.msg_label)

    def enviar_email(self, instance):
        try:
            creds = InstalledAppFlow.from_client_secrets_file(
                'credentials.json',
                scopes=['https://www.googleapis.com/auth/gmail.send']
            ).run_local_server(port=0)

            service = build('gmail', 'v1', credentials=creds)

            nome = self.nome_input.text
            numero = self.numero_input.text

            corpo = f"""Olá equipe do WhatsApp,

Minha conta vinculada ao número {numero} foi banida e acredito que foi um engano.

Gostaria de entender a razão e, se possível, recuperar o acesso.
Caso eu tenha violado alguma política sem saber, estou disposto a corrigir isso.

Atenciosamente,
{nome}
"""
            mensagem = MIMEText(corpo)
            mensagem['to'] = 'support@support.whatsapp.com'
            mensagem['subject'] = 'Minha conta foi banida por engano'

            raw_msg = {'raw': base64.urlsafe_b64encode(mensagem.as_bytes()).decode()}
            service.users().messages().send(userId="me", body=raw_msg).execute()

            self.msg_label.text = "✅ E-mail enviado com sucesso!"
        except Exception as e:
            self.msg_label.text = f"Erro: {e}"

class EmailApp(App):
    def build(self):
        return EmailForm()

if __name__ == '__main__':
    EmailApp().run()
