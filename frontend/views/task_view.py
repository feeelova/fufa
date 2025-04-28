import flet as ft

def create_task_page(page: ft.Page, task_api, token: str):
    # Цветовая схема
    theme = {
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
        "border_radius": 8,
        "border_width": 1,
        "border_color": theme["secondary"],
        "focused_border_width": 2,
        "focused_border_color": theme["secondary"],
        "cursor_color": theme["secondary"],
        "cursor_width": 1.5,
        "content_padding": 15,
        "filled": True,
        "fill_color": ft.colors.WHITE,
        "text_size": 16,
        "label_style": ft.TextStyle(color=theme["text"], size=14)
    }

    # Поля ввода
    title_field = ft.TextField(label="Название", autofocus=True, **field_style)
    description_field = ft.TextField(label="Описание", multiline=True, **field_style)

    # Кнопка назад
    def go_back(e):
        page.go("/dashboard")

    # Создание задачи
    def create_task(e):
        title = title_field.value.strip()
        description = description_field.value.strip()

        if not title:
            page.snack_bar = ft.SnackBar(ft.Text("Название обязательно!"), bgcolor=theme["error"])
            page.snack_bar.open = True
            page.update()
            return

        response, status = task_api.create_task(token, title, description)
        if status == 200:
            page.snack_bar = ft.SnackBar(ft.Text("Задача создана!"), bgcolor=theme["secondary"])
            page.snack_bar.open = True
            page.update()
            page.go("/dashboard")
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Ошибка создания задачи!"), bgcolor=theme["error"])
            page.snack_bar.open = True
            page.update()

    # Структура страницы
    return ft.Container(
        content=ft.Column(
            [
                # Заголовок
                ft.Text(
                    "Создание новой задачи",
                    size=30,
                    weight="bold",
                    color=theme["primary"],
                ),
                ft.Divider(height=20),  # Разделитель между заголовком и полями

                # Поля для ввода
                title_field,
                description_field,

                # Кнопки
                ft.Row(
                    [
                        ft.ElevatedButton(
                            "Назад",
                            on_click=go_back,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=8),
                                padding=20,
                                bgcolor=theme["primary"],
                                color=ft.colors.WHITE
                            ),
                            height=50
                        ),
                        ft.ElevatedButton(
                            "Создать",
                            on_click=create_task,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=8),
                                padding=20,
                                bgcolor=theme["secondary"],
                                color=ft.colors.WHITE
                            ),
                            height=50
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    spacing=20
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=30,  # Расстояние между элементами
        ),
        padding=ft.padding.all(20),
        bgcolor=theme["background"]
    )
