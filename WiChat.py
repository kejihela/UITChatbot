from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.label import MDLabel
from kivymd.uix.spinner import MDSpinner
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.screen import Screen
from kivy.clock import Clock
from kivymd.uix.button import MDIconButton, MDRaisedButton
from kivymd.uix.card import MDCard
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield import MDTextField
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList
import torch
from transformers import AutoTokenizer, pipeline
from kivymd.uix.list import OneLineListItem






# Startup Screen
class StartupScreen(Screen):
    def on_enter(self):
        layout = BoxLayout(orientation='vertical', spacing=10, pos_hint={'center_x': 0.5, 'center_y': 0.5})

        self.spinner = MDSpinner(size_hint=(None, None), size=(50, 50), pos_hint={'center_x': 0.7}, active=True)
        title = MDLabel(text="WiChat", font_style="H4", halign="center", bold=True)
        version = MDLabel(text="Version 1.0", font_style="Caption", halign="center")

        layout.add_widget(self.spinner)
        layout.add_widget(title)
        layout.add_widget(version)
        self.add_widget(layout)

        Clock.schedule_once(self.switch_to_main, 5)  # Switch to main screen after 2.5 seconds

    def switch_to_main(self, dt):
        self.manager.current = "main"







# Login Screen
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", spacing=10)

        title = MDLabel(text="Login", halign="center", font_style="H4")
        layout.add_widget(title)

        # Username box
        self.username_input = MDTextField(hint_text="Username", size_hint=(None, None), pos_hint={"center_x": 0.5, "center_y": 0.5}, size=("300dp", "40dp"))
        layout.add_widget(self.username_input)

        # Password box
        self.password_input = MDTextField(hint_text="Password", password=True, size_hint=(None, None), pos_hint={"center_x": 0.5, "center_y": 0.5}, size=("300dp", "40dp"))
        layout.add_widget(self.password_input)

        # Login Button
        login_button = MDRaisedButton(text="Login", size_hint=(None, None), pos_hint={"center_x": 0.5, "center_y": 0.5},  size=("300dp", "40dp"))
        login_button.bind(on_release=self.login)
        layout.add_widget(login_button)

        # Back Button
        back_button = MDRaisedButton(text="Back", size_hint=(None, None), size=("300dp", "40dp"))
        back_button.bind(on_release=self.back_to_chat)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def login(self, instance):
        # Here you would implement the login logic
        print("Logging in with username and password:", self.username_input.text, self.password_input.text)


    def back_to_chat(self, instance):
        self.manager.current = "main"


# Signup Screen
class SignupScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", spacing=10)

        title = MDLabel(text="Sign Up", halign="center", font_style="H4")
        layout.add_widget(title)

        # Username
        self.username_input = MDTextField(hint_text="Username", size_hint=(None, None), pos_hint={"center_x": 0.5, "center_y": 0.5}, size=("300dp", "40dp"))
        layout.add_widget(self.username_input)

        # Email
        self.email_input = MDTextField(hint_text="Email", size_hint=(None, None), pos_hint={"center_x": 0.5, "center_y": 0.5}, size=("300dp", "40dp"))
        layout.add_widget(self.email_input)

        # Password
        self.password_input = MDTextField(hint_text="Password", password=True, size_hint=(None, None), pos_hint={"center_x": 0.5, "center_y": 0.5}, size=("300dp", "40dp"))
        layout.add_widget(self.password_input)

        # Sign Up Button
        signup_button = MDRaisedButton(text="Sign Up", size_hint=(None, None), pos_hint={"center_x": 0.5, "center_y": 0.8}, size=("300dp", "40dp"))
        signup_button.bind(on_release=self.signup)
        layout.add_widget(signup_button)

        # Back Button
        back_button = MDRaisedButton(text="Back", size_hint=(None, None), size=("300dp", "40dp"))
        back_button.bind(on_release=self.back_to_chat)
        layout.add_widget(back_button)

        self.add_widget(layout)


    def signup(self, instance):
        # Here you would implement the signup logic
        print("Signing up with username, email and password:", self.username_input.text, self.password_input.text, self.email_input.text)

    def back_to_chat(self, instance):
        self.manager.current = "main"





# Main Chatbot Screen
class ChatScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        # Toolbar
        toolbar = BoxLayout(size_hint_y=None, height="65dp", padding="10dp", spacing="10dp")
        self.menu_button = MDIconButton(icon="menu")
        self.menu_button.bind(on_release=self.show_menu)

        title = MDLabel(text="WiChat", halign="left", bold=True, font_size="20sp")
        self.account_button = MDIconButton(icon="account")
        self.account_button.bind(on_release=self.show_account)

        toolbar.add_widget(self.menu_button)
        toolbar.add_widget(title)
        toolbar.add_widget(self.account_button)
        layout.add_widget(toolbar)

        # Welcome Card
        md_card = MDCard(size_hint=(None, None), size=("700dp", "70dp"),
                         pos_hint={"center_x": 0.5, "center_y": 0.8}, elevation=5)
        md_label = MDLabel(text="Welcome!!! WiChat wants to know what's on your mind",
                           halign="center", theme_text_color="Secondary", bold=True)
        md_card.add_widget(md_label)
        layout.add_widget(md_card)

        # Chat Display
        self.chat_scroll = MDScrollView()
        self.chat_list = MDList()
        self.chat_scroll.add_widget(self.chat_list)
        layout.add_widget(self.chat_scroll)

        # Input and Send Button
        input_container = BoxLayout(size_hint=(None, None), size=("350dp", "50dp"),
                                    pos_hint={"center_x": 0.5, "y": 0.02}, spacing="10dp",)
        self.input_text = MDTextField(hint_text="Ask WiChat anything...", size_hint_x=0.7, multiline=False)
        send_button = MDRaisedButton(text="Send", size_hint_x=0.3, on_release=self.send_message)
        input_container.add_widget(self.input_text)
        input_container.add_widget(send_button)
        layout.add_widget(input_container)

        # Dropdown Menus
        self.menu_items = [
            {"viewclass": "OneLineListItem", "text": "Toggle Theme",
             "on_release": lambda x="Toggle Theme": self.menu_callback(x)},
            {"viewclass": "OneLineListItem", "text": "Clear Chat",
             "on_release": lambda x="Clear Chat": self.menu_callback(x)},
            {"viewclass": "OneLineListItem", "text": "Help", "on_release": lambda x="Help": self.menu_callback(x)},
        ]
        self.menu = MDDropdownMenu(caller=self.menu_button, items=self.menu_items, width_mult=4)

        self.account_items = [
            {"viewclass": "OneLineListItem", "text": "Login", "on_release": lambda x="Login": self.account_callback(x)},
            {"viewclass": "OneLineListItem", "text": "SignUp", "on_release": lambda x="SignUp": self.account_callback(x)},
        ]
        self.account = MDDropdownMenu(caller=self.account_button, items=self.account_items, width_mult=4)

        self.add_widget(layout)

        # Initialize the chatbot model
        self.chatbot_model = self.initialize_chatbot()

    def initialize_chatbot(self):
        model = "gpt2"
        tokenizer = AutoTokenizer.from_pretrained(model)
        chatbot_pipeline = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            torch_dtype=torch.float32,
        )
        return chatbot_pipeline


    def show_menu(self, obj):
        self.menu.open()

    def show_account(self, obj):
        self.account.open()

    def menu_callback(self, option):
        if option == "Toggle Theme":
            self.toggle_theme()
        elif option == "Clear Chat":
            self.clear_chat()
        elif option == "Help":
            print("Help Button Pressed")
        self.menu.dismiss()

    def account_callback(self, option):
        if option == "Login":
            self.manager.current = "login"
        elif option == "SignUp":
            self.manager.current = "signup"
        self.account.dismiss()

    def send_message(self, obj):
        user_message = self.input_text.text.strip()
        if user_message:
            self.chat_list.add_widget(MDLabel(text=user_message, halign="right", theme_text_color="Primary"))
            self.input_text.text = ""

            # Generate chatbot response
            chatbot_response = self.chatbot_model(
                user_message,
                max_length=100,
                do_sample=True
            )[0]['generated_text']
            bot_label = MDLabel(text=chatbot_response, halign="left")
            self.chat_list.add_widget(bot_label)

            self.chat_list.add_widget(MDLabel(text=f"WiChat: {chatbot_response}", halign="left", theme_text_color="Secondary"))

            # Scroll to the bottom after sending a message
            self.chat_scroll.scroll_y = 0  # Set to the bottom (0 means bottom)

    def clear_chat(self):
        self.chat_list.clear_widgets()

    def toggle_theme(self):
        MDApp.get_running_app().theme_cls.theme_style = "Dark" if MDApp.get_running_app().theme_cls.theme_style == "Light" else "Light"


# WiChat App
class WiChat(MDApp):
    def build(self):
        # Set the app's theme
        #self.theme_cls.primary_palette = "Teal"  # Choose your primary color
        #self.theme_cls.theme_style = "Light"  # You can also use "Dark" theme here

        sm = MDScreenManager()
        sm.add_widget(StartupScreen(name="startup"))
        sm.add_widget(ChatScreen(name="main"))
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(SignupScreen(name="signup"))
        return sm


if __name__ == "__main__":
    WiChat().run()









