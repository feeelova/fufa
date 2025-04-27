import flet as ft

def create_task_page(page: ft.Page, task_api, token: str):
    title_field = ft.TextField(label="Название", autofocus=True)
    description_field = ft.TextField(label="Описание", multiline=True)

    def go_back(e):
        page.go("/dashboard")

    def create_task(e):
        title = title_field.value.strip()
        description = description_field.value.strip()

        if not title:
            page.snack_bar = ft.SnackBar(ft.Text("Название обязательно!"), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return

        response, status = task_api.create_task(token, title, description)
        if status == 200:
            page.snack_bar = ft.SnackBar(ft.Text("Задача создана!"), bgcolor="green")
            page.snack_bar.open = True
            page.update()
            page.go("/dashboard")
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Ошибка создания задачи!"), bgcolor="red")
            page.snack_bar.open = True
            page.update()

    return ft.Column(
        [
            ft.Text("Создание новой задачи", size=24, weight="bold"),
            title_field,
            description_field,
            ft.Row(
                [
                    ft.ElevatedButton("Назад", on_click=go_back),
                    ft.ElevatedButton("Создать", on_click=create_task),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20
    )
