import flet as ft
from frontend.api.client import AuthAPI
from frontend.api.taskapi import TaskAPI
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


def dashboard_page(page: ft.Page, auth_api: AuthAPI, task_api: TaskAPI):
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

        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.ListTile(
                        title=ft.Text(task_data['title'], weight="bold"),
                        subtitle=ft.Text(task_data['description'] or "-"),
                    ),
                    ft.Row([
                        ft.IconButton(
                            icon=ft.icons.DELETE_OUTLINE,
                            icon_color="red",
                            tooltip="Удалить",
                            on_click=delete_task
                        ),
                        ft.Switch(
                            value=is_done,
                            label="Выполнено" if is_done else "Не выполнено",
                            on_change=toggle_done
                        )
                    ], alignment=ft.MainAxisAlignment.END)
                ]),
                padding=10,
                width=400
            ),
            elevation=2,
            margin=ft.margin.symmetric(vertical=5)
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

    def logout_click(e):
        page.client_storage.remove("token")
        page.go("/")

    # Верхняя панель
    header = ft.Row(
        [
            ft.Text(
                f"Добро пожаловать, {user_data.get('email', '')}!",
                size=22,
                weight="bold",
                color=ft.colors.BLUE_800
            ),
            ft.ElevatedButton(
                "+ Новая задача",
                icon=ft.icons.ADD,
                on_click=lambda e: page.go("/create-task"),  # переход на страницу создания
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=8),
                    padding=20
                )
            )
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    content = ft.Column([
        header,
        ft.Divider(height=20),
        ft.Text("Активные задачи:", size=18, weight="bold"),
        pending_tasks,
        ft.Divider(height=20),
        ft.Text("Выполненные задачи:", size=18, weight="bold"),
        completed_tasks,
        ft.ElevatedButton(
            "Выйти из системы",
            icon=ft.icons.LOGOUT,
            on_click=logout_click,
            bgcolor=ft.colors.RED_100
        )
    ], spacing=20, expand=True)

    load_tasks()

    return ft.Container(
        content=content,
        padding=30,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[ft.colors.BLUE_50, ft.colors.LIGHT_BLUE_100]
        ),
        expand=True
    )


def logout_click(page: ft.Page):
    page.client_storage.remove("token")
    page.go("/")
    show_snackbar(page, "Вы успешно вышли из системы", "green")