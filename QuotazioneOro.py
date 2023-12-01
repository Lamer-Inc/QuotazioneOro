import requests
from bs4 import BeautifulSoup
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.core.window import Window

class QuotazioneOroApp(App):
    def build(self):
        self.url_sito_oro = 'https://www.bancodellorodivrea.it/quotazione-oro'
        self.oro_nella_pagina = None
        self.argento_nella_pagina = None

        
        Window.clearcolor = (0.2, 0.2, 0.7, 1)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self.aggiungi_descrizione(layout)
        self.aggiungi_bottoni(layout)

      
        Clock.schedule_interval(self.aggiorna_quotazioni, 5)

        return layout

    def aggiungi_descrizione(self, layout):
        descrizione = BoxLayout(orientation='vertical', spacing=10, padding=10, size_hint=(1, None), height=100)
        descrizione.add_widget(Label(text='Applicazione creata da @forzanapolifinoallafine:', halign='left', valign='middle', size_hint=(1, None), height=30))
        descrizione.add_widget(Label(text='Questa app mostra le quotazioni dell\'oro e dell\'argento '
                                            'aggiornate ogni 5 secondi da www.bancodellorodivrea.it', halign='left', valign='middle'))
        layout.add_widget(descrizione)

    def aggiungi_bottoni(self, layout):
        button_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.1))

        
        button = Button(text='Visualizza Quotazione Oro', on_press=self.visualizza_quotazione, background_color=(1, 0.8, 0, 1))
        button1 = Button(text='Visualizza Quotazione Argento', on_press=self.visualizza_quotazione1, background_color=(0.8, 0.8, 0.8, 1))
        button_exit = Button(text='Chiudi App', on_press=self.stop, background_color=(1, 0.5, 0.5, 1))
        button_layout.add_widget(button)
        button_layout.add_widget(button1)
        button_layout.add_widget(button_exit)
        layout.add_widget(button_layout)

        self.label = Label(text='', size_hint_y=None, height=44, halign='center', valign='middle')
        layout.add_widget(self.label)

    def visualizza_quotazione(self, instance):
        if self.oro_nella_pagina:
            testo_pulito = self.pulisci_testo(self.oro_nella_pagina)
            self.mostra_popup('Quotazione Oro', testo_pulito)

    def visualizza_quotazione1(self, instance):
        if self.argento_nella_pagina:
            testo_pulito = self.pulisci_testo(self.argento_nella_pagina)
            self.mostra_popup('Quotazione Argento', testo_pulito)

    def mostra_popup(self, title, content):
        popup_content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        popup_content.add_widget(Label(text=content, size_hint_y=None, height=44, halign='center', valign='middle'))
        popup_content.add_widget(Button(text='Chiudi', on_press=lambda x: self.popup.dismiss(), size_hint_y=None, height=44))

        self.popup = Popup(title=title, content=popup_content, size_hint=(None, None), size=(400, 200))
        self.popup.open()

    def aggiorna_quotazioni(self, dt):
        try:
            processa_sito = requests.get(self.url_sito_oro)
            processa_sito.raise_for_status()
            soup = BeautifulSoup(processa_sito.content, "html.parser")
            self.oro_nella_pagina = soup.find_all("div", class_="valore_oro")
            self.argento_nella_pagina = soup.find_all("div", class_="valore_argento")
        except requests.exceptions.RequestException as e:
            self.handle_error(f"Errore nella richiesta: {e}")

    def pulisci_testo(self, soup_elements):
        
        return ' '.join(element.get_text(strip=True) for element in soup_elements)

    def handle_error(self, error_message):
        popup_content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        popup_content.add_widget(Label(text=error_message, size_hint_y=None, height=44, halign='center', valign='middle'))
        popup_content.add_widget(Button(text='Chiudi', on_press=self.stop, size_hint_y=None, height=44))

        error_popup = Popup(title='Errore', content=popup_content, size_hint=(None, None), size=(300, 200))
        error_popup.open()

if __name__ == '__main__':
    QuotazioneOroApp().run()
