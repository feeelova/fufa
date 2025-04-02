import flet as ft


def main(page: ft.Page):
    page.title = "Kolpr App"
    page.add(ft.Text("Hello from Flet!"))
    page.update()


ft.app(target=main)
