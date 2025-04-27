import flet as ft
from api.client import AuthAPI
from api.taskapi import TaskAPI
from views.auth_views import LoginRegisterPage, dashboard_page
from views.task_view import create_task_page  # <-- добавляем импорт


def main(page: ft.Page):
    # Initialize API client
    auth_api = AuthAPI()
    task_api = TaskAPI()

    # Configure page settings
    page.title = "Мое крутое приложение"
    page.padding = 30
    page.window_width = 400
    page.window_height = 600
    page.window_resizable = False

    def route_change(e):
        page.views.clear()

        token = page.client_storage.get("token")

        if e.route == "/dashboard":
            view = ft.View("/dashboard", [dashboard_page(page, auth_api, task_api)])
        elif e.route == "/create-task":
            if not token:
                page.go("/")
                return
            view = ft.View("/create-task", [create_task_page(page, task_api, token)])
        else:
            view = ft.View("/", [LoginRegisterPage(page, auth_api).view])

        page.views.append(view)
        page.update()

    page.on_route_change = route_change
    page.go(page.route)


if __name__ == "__main__":
    ft.app(target=main)
