import flet as ft
from frontend.api.client import AuthAPI
from frontend.utils.helpers import validate_email, show_snackbar


class LoginRegisterPage:
    def __init__(self, page: ft.Page, auth_api: AuthAPI):
        self.page = page
        self.auth_api = auth_api

        # Общие стили для полей ввода
        field_style = {
            "width": 300,
            "height": 45,
            "border_radius": 10,
            "border_color": ft.colors.BLUE_GREY_200,
            "focused_border_color": ft.colors.LIGHT_BLUE_600,
            "cursor_color": ft.colors.LIGHT_BLUE_600,
            "content_padding": 10,
        }

        # Поля для входа
        self.email_login = ft.TextField(
            label="Email",
            keyboard_type=ft.KeyboardType.EMAIL,
            autofill_hints=[ft.AutofillHint.EMAIL],
            on_change=self.clear_login_errors,
            **field_style,
        )

        self.password_login = ft.TextField(
            label="Пароль",
            password=True,
            autofill_hints=[ft.AutofillHint.PASSWORD],
            on_change=self.clear_login_errors,
            **field_style,
        )

        # Поля для регистрации
        self.email_register = ft.TextField(
            label="Email",
            keyboard_type=ft.KeyboardType.EMAIL,
            on_change=self.clear_register_errors,
            **field_style,
        )

        self.password_register = ft.TextField(
            label="Пароль",
            password=True,
            autofill_hints=[ft.AutofillHint.NEW_PASSWORD],
            on_change=self.clear_register_errors,
            **field_style,
        )

        # Стили для кнопок
        button_style = {
            "height": 45,
            "style": ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=20,
            ),
        }

        # Контейнеры форм
        self.login_container = self._build_login_form(button_style)
        self.register_container = self._build_register_form(button_style)

        # Основной контейнер с центрированием
        self.view = ft.Container(
            content=ft.Column(
                [self.login_container, self.register_container],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=30,
            ),
            alignment=ft.alignment.center,
            expand=True,
            padding=20,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[
                    ft.colors.BLUE_50,
                    ft.colors.LIGHT_BLUE_100,
                ],
            ),
        )

    def _build_login_form(self, button_style):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("Вход", size=24, weight="bold", color=ft.colors.BLUE_800),
                    self.email_login,
                    self.password_login,
                    ft.ElevatedButton(
                        "Войти",
                        **button_style,
                        color=ft.colors.WHITE,
                        bgcolor=ft.colors.LIGHT_BLUE_600,
                        on_click=self.login_click,
                    ),
                    ft.TextButton(
                        "Нет аккаунта? Зарегистрироваться",
                        on_click=self.switch_form,
                        style=ft.ButtonStyle(color=ft.colors.BLUE_600),
                    ),
                ],
                spacing=15,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=30,
            bgcolor=ft.colors.WHITE,
            border_radius=15,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.colors.BLUE_GREY_100,
            ),
            width=400,
        )

    def _build_register_form(self, button_style):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Регистрация",
                        size=24,
                        weight="bold",
                        color=ft.colors.BLUE_800,
                    ),
                    self.email_register,
                    self.password_register,
                    ft.ElevatedButton(
                        "Зарегистрироваться",
                        **button_style,
                        color=ft.colors.WHITE,
                        bgcolor=ft.colors.CYAN_600,
                        on_click=self.register_click,
                    ),
                    ft.TextButton(
                        "Уже есть аккаунт? Войти",
                        on_click=self.switch_form,
                        style=ft.ButtonStyle(color=ft.colors.BLUE_600),
                    ),
                ],
                spacing=15,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=30,
            bgcolor=ft.colors.WHITE,
            border_radius=15,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.colors.BLUE_GREY_100,
            ),
            width=400,
            visible=False,
        )

    def clear_login_errors(self, e):
        self.email_login.error_text = ""
        self.password_login.error_text = ""
        self.page.update()

    def clear_register_errors(self, e):
        self.email_register.error_text = ""
        self.password_register.error_text = ""
        self.page.update()

    def switch_form(self, e):
        self.login_container.visible = not self.login_container.visible
        self.register_container.visible = not self.register_container.visible
        self.clear_fields()
        self.page.update()

    def clear_fields(self):
        self.email_login.value = ""
        self.password_login.value = ""
        self.email_register.value = ""
        self.password_register.value = ""
        self.email_login.error_text = ""
        self.password_login.error_text = ""
        self.email_register.error_text = ""
        self.password_register.error_text = ""
        self.page.snack_bar = None

    def login_click(self, e):
        email = self.email_login.value
        password = self.password_login.value

        if not email or not password:
            show_snackbar(self.page, "Все поля должны быть заполнены!", "orange")
            return

        if not validate_email(email):
            self.email_login.error_text = "Некорректный формат email"
            self.page.update()
            return

        self.page.splash = ft.ProgressBar()
        self.page.update()

        result, error = self.auth_api.login(email, password)
        self.page.splash = None

        if result:
            self.page.client_storage.set("token", result["access_token"])
            self.page.go("/dashboard")
        else:
            error_messages = {
                "Invalid credentials": "Неверная комбинация email и пароля",
                "User not found": "Пользователь не найден",
                "Inactive user": "Аккаунт деактивирован",
                "Connection error": "Ошибка соединения с сервером",
            }
            error_msg = error_messages.get(
                error, "Неизвестная ошибка. Попробуйте снова."
            )

            if error == "User not found":
                self.email_login.error_text = "Пользователь не найден"
            elif error == "Invalid credentials":
                self.password_login.error_text = "Неверный пароль"

            self.page.update()
            show_snackbar(self.page, error_msg, "red")

    def register_click(self, e):
        email = self.email_register.value
        password = self.password_register.value

        if not email or not password:
            show_snackbar(self.page, "Все поля должны быть заполнены!", "orange")
            return

        if not validate_email(email):
            self.email_register.error_text = "Некорректный формат email"
            self.page.update()
            return

        self.page.splash = ft.ProgressBar()
        self.page.update()

        success, error = self.auth_api.register(email, password)
        self.page.splash = None

        if success:
            result, error = self.auth_api.login(email, password)
            if result:
                show_snackbar(
                    self.page, "Регистрация успешна! Автоматический вход...", "green"
                )
                self.page.client_storage.set("token", result["access_token"])
                self.page.go("/dashboard")
            else:
                show_snackbar(
                    self.page, "Ошибка автоматического входа после регистрации", "red"
                )
        else:
            error_messages = {
                "Email already registered": "Email уже зарегистрирован",
                "Weak password": "Слишком простой пароль",
                "Connection error": "Ошибка соединения с сервером",
            }
            error_msg = error_messages.get(
                error, "Неизвестная ошибка. Попробуйте снова."
            )

            if error == "Email already registered":
                self.email_register.error_text = "Email уже используется"

            self.page.update()
            show_snackbar(self.page, error_msg, "red")


def dashboard_page(page: ft.Page, auth_api: AuthAPI):
    token = page.client_storage.get("token")
    if not token:
        page.go("/")
        return ft.Column()

    user_data, error = auth_api.get_profile(token)
    if error:
        show_snackbar(page, "Ошибка авторизации", "red")
        page.go("/")
        return ft.Column()

    welcome_text = ft.Text(
        f"Добро пожаловать, {user_data.get('email', '')}!",
        size=22,
        weight="bold",
        text_align=ft.TextAlign.CENTER,
        color=ft.colors.BLUE_800,
    )

    description = ft.Text(
        "Что вы хотите сделать?",
        size=16,
        color=ft.colors.BLUE_GREY_600,
        text_align=ft.TextAlign.CENTER,
    )

    budget_button = ft.ElevatedButton(
        "📊 Автоматическое распределение бюджета",
        icon=ft.icons.CALCULATE_OUTLINED,
        on_click=lambda e: page.go("/budget"),
        width=280,
        height=50,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=12),
            bgcolor=ft.colors.LIGHT_BLUE_600,
            color=ft.colors.WHITE,
        ),
    )

    logout_button = ft.ElevatedButton(
        "🚪 Выйти из аккаунта",
        icon=ft.icons.LOGOUT_OUTLINED,
        on_click=lambda e: logout_click(page),
        width=280,
        height=50,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=12),
            bgcolor=ft.colors.BLUE_GREY_100,
            color=ft.colors.BLUE_800,
        ),
    )

    card = ft.Container(
        content=ft.Column(
            [
                welcome_text,
                description,
                ft.Divider(),
                ft.Column(
                    [budget_button, logout_button],
                    spacing=20,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            spacing=25,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=30,
        bgcolor=ft.colors.WHITE,
        border_radius=20,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=12,
            color=ft.colors.BLUE_GREY_100,
            offset=ft.Offset(2, 4),
        ),
        width=350,
    )

    return ft.Row(
        [card],
        alignment=ft.MainAxisAlignment.CENTER,
    )


def logout_click(page: ft.Page):
    page.client_storage.remove("token")
    page.go("/")
    show_snackbar(page, "Вы успешно вышли из системы", "green")
