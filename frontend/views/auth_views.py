import flet as ft
from frontend.api.client import AuthAPI
from frontend.api.taskapi import TaskAPI
from frontend.utils.helpers import validate_email, show_snackbar


class LoginRegisterPage:
    def __init__(self, page: ft.Page, auth_api: AuthAPI):
        self.page = page
        self.auth_api = auth_api

        # Цветовая схема
        self.theme = {
            "primary": "#2A2A2A",
            "secondary": "#4ECDC4",
            "accent": "#FF6B6B",
            "background": "#F8F9FA",
            "text": "#333333",
            "error": "#FF5252"
        }

        # Стили полей ввода
        field_style = {
            "height": 50,
            "border_radius": 0,
            "border_width": 0,
            "border_color": "transparent",
            "focused_border_width": 2,
            "focused_border_color": self.theme["secondary"],
            "cursor_color": self.theme["secondary"],
            "cursor_width": 1.5,
            "content_padding": 15,
            "filled": True,
            "fill_color": ft.colors.WHITE,
            "text_size": 16,
            "label_style": ft.TextStyle(color=self.theme["text"], size=14)
        }

        # Поля для входа
        self.email_login = ft.TextField(
            label="Email",
            keyboard_type=ft.KeyboardType.EMAIL,
            autofill_hints=[ft.AutofillHint.EMAIL],
            on_change=self.clear_login_errors,
            **field_style
        )

        self.password_login = ft.TextField(
            label="Пароль",
            password=True,
            autofill_hints=[ft.AutofillHint.PASSWORD],
            on_change=self.clear_login_errors,
            **field_style
        )

        # Поля для регистрации
        self.email_register = ft.TextField(
            label="Email",
            keyboard_type=ft.KeyboardType.EMAIL,
            on_change=self.clear_register_errors,
            **field_style
        )

        self.password_register = ft.TextField(
            label="Пароль",
            password=True,
            autofill_hints=[ft.AutofillHint.NEW_PASSWORD],
            on_change=self.clear_register_errors,
            **field_style
        )

        # Построение интерфейса
        self.login_form = self._build_login_form()
        self.register_form = self._build_register_form()

        self.view = ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=["#F8F9FA", "#E9ECEF"]
            ),
            content=ft.Row(
                [
                    # Левая панель с графикой
                    ft.Container(
                        width=400,
                        height=page.height,
                        content=ft.Column(
                            [
                                ft.Container(
                                    content=ft.Image(
                                        src="img.png",
                                        width=400,
                                        height=page.height,
                                        fit=ft.ImageFit.COVER,
                                        expand=True,
                                    ),
                                    alignment=ft.alignment.center,
                                    margin=0,
                                    padding=0,
                                    expand=True,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=0,
                            expand=True,
                        ),
                        bgcolor=ft.colors.WHITE,
                        padding=0,
                        margin=0,
                        alignment=ft.alignment.top_center,
                    ),

                    # Правая панель с формами
                    ft.Container(
                        expand=True,
                        content=ft.Stack(
                            [self.login_form, self.register_form],
                            width=400
                        ),
                        padding=ft.padding.only(top=80, right=100, left=100),
                        alignment=ft.alignment.top_center
                    )
                ],
                vertical_alignment=ft.CrossAxisAlignment.STRETCH
            ),
            expand=True
        )

    def _build_login_form(self):
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "Вход в систему",
                            size=24,
                            weight="bold",
                            color=self.theme["primary"]
                        ),
                        ft.Divider(height=30),
                        self.email_login,
                        self.password_login,
                        ft.ElevatedButton(
                            "Продолжить",
                            icon=ft.icons.ARROW_FORWARD,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=8),
                                padding=20,
                                bgcolor=self.theme["secondary"],
                                color=ft.colors.WHITE
                            ),
                            height=50,
                            on_click=self.login_click
                        ),
                        ft.TextButton(
                            "Создать новый аккаунт",
                            on_click=self.switch_form,
                            style=ft.ButtonStyle(
                                color=self.theme["accent"]
                            )
                        )
                    ],
                    spacing=20
                ),
                padding=40,
                width=400
            ),
            elevation=8,
            visible=True,
            animate_opacity=300
        )

    def _build_register_form(self):
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "Регистрация",
                            size=24,
                            weight="bold",
                            color=self.theme["primary"]
                        ),
                        ft.Divider(height=30),
                        self.email_register,
                        self.password_register,
                        ft.ElevatedButton(
                            "Создать аккаунт",
                            icon=ft.icons.PERSON_ADD,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=8),
                                padding=20,
                                bgcolor=self.theme["accent"],
                                color=ft.colors.WHITE
                            ),
                            height=50,
                            on_click=self.register_click
                        ),
                        ft.TextButton(
                            "Уже есть аккаунт? Войти",
                            on_click=self.switch_form,
                            style=ft.ButtonStyle(
                                color=self.theme["secondary"]
                            )
                        )
                    ],
                    spacing=20
                ),
                padding=40,
                width=400
            ),
            elevation=8,
            visible=False,
            animate_opacity=300
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
        self.login_form.visible = not self.login_form.visible
        self.register_form.visible = not self.register_form.visible
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
            error_msg = error_messages.get(error, "Неизвестная ошибка. Попробуйте снова.")

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
            error_msg = error_messages.get(error, "Неизвестная ошибка. Попробуйте снова.")

            if error == "Email already registered":
                self.email_register.error_text = "Email уже используется"

            self.page.update()
            show_snackbar(self.page, error_msg, "red")


def dashboard_page(page: ft.Page, auth_api: AuthAPI, task_api: TaskAPI):
    theme = {
        "primary": "#2A2A2A",  # основной цвет текста
        "secondary": "#4ECDC4",  # цвет акцентов
        "accent": "#FF6B6B",  # красный для ошибок и выделений
        "background": "#F8F9FA"  # светлый фон
    }

    token = page.client_storage.get("token")
    if not token:
        page.go("/")
        return ft.Column()

    user_data, error = auth_api.get_profile(token)
    if error:
        show_snackbar(page, "Ошибка авторизации", "red")
        page.go("/")
        return ft.Column()

    pending_tasks = ft.Column(spacing=10)
    completed_tasks = ft.Column(spacing=10)

    def build_task_card(task_data):
        task_id = task_data['id']
        is_done = task_data['is_done']

        def delete_task(e):
            response = task_api.delete_task(token, task_id)
            if response:
                show_snackbar(page, "Задача удалена!", "green")
                load_tasks()
            else:
                show_snackbar(page, "Ошибка удаления!", "red")

        def toggle_done(e):
            new_status = not is_done
            response = task_api.update_task(token, task_id, new_status)
            if response:
                show_snackbar(page, "Статус задачи обновлен!", "green")
                load_tasks()
            else:
                show_snackbar(page, "Ошибка обновления!", "red")

        return ft.Container(
            content=ft.ListTile(
                leading=ft.Checkbox(
                    value=is_done,
                    active_color=theme["secondary"],
                    on_change=toggle_done
                ),
                title=ft.Text(
                    task_data['title'],
                    color=theme["primary"],
                    weight="bold",
                    selectable=True
                ),
                subtitle=ft.Text(
                    task_data.get('description', '') or "Без описания",
                    color=ft.colors.GREY_600,
                    max_lines=2
                ),
                trailing=ft.IconButton(
                    icon=ft.icons.DELETE_OUTLINE,
                    icon_color=theme["accent"],
                    on_click=delete_task
                )
            ),
            bgcolor=ft.colors.WHITE,
            border_radius=12,
            padding=15,
            margin=ft.margin.symmetric(vertical=10),  # увеличены отступы
            shadow=ft.BoxShadow(
                spread_radius=0.5,
                blur_radius=10,
                color=ft.colors.with_opacity(0.1, ft.colors.BLACK)
            )
        )

    def load_tasks():
        pending_tasks.controls.clear()
        completed_tasks.controls.clear()

        tasks, status = task_api.get_tasks(token)
        if status == 200:
            for task in tasks:
                card = build_task_card(task)
                if task['is_done']:
                    completed_tasks.controls.append(card)
                else:
                    pending_tasks.controls.append(card)

        page.update()


    content = ft.Column(
        [
            ft.Row(
                [
                    ft.Text(
                        "Мои задачи",
                        size=24,
                        weight="bold",
                        color=theme["primary"]
                    ),
                    ft.IconButton(
                        icon=ft.icons.ADD,
                        icon_color=theme["accent"],
                        tooltip="Новая задача",
                        on_click=lambda e: page.go("/create-task"),
                        bgcolor=theme["secondary"],  # Цвет фона кнопки
                        alignment=ft.alignment.center  # Центрируем кнопку внутри контейнера
                    ),

                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            ft.Divider(height=20),
            ft.Column(
                [
                    ft.Text("Активные задачи:", size=18, weight="bold"),
                    pending_tasks,
                    ft.Divider(height=20),
                    ft.Text("Выполненные задачи:", size=18, weight="bold"),
                    completed_tasks
                ],
                spacing=15,
                expand=True,
                scroll=ft.ScrollMode.ADAPTIVE
            )
        ],
        spacing=20,
        expand=True
    )

    load_tasks()

    return ft.Container(
        content=ft.Column([content]),
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[theme["background"], ft.colors.WHITE]
        ),
        padding=30,
        expand=True
    )


def logout_click(page: ft.Page):
    page.client_storage.remove("token")
    page.go("/")
    show_snackbar(page, "Вы успешно вышли из системы", "green")