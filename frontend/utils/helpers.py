import re
import flet as ft


def validate_email(email: str) -> bool:
    return (
        re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email) is not None
    )


def show_snackbar(page: ft.Page, message: str, color: str):
    page.snack_bar = ft.SnackBar(ft.Text(message), bgcolor=color, duration=2000)
    page.snack_bar.open = True
    page.update()
