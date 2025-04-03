import flet as ft
from api.client import AuthAPI
from views.auth_views import LoginRegisterPage, dashboard_page


def main(page: ft.Page):
    # Initialize API client
    auth_api = AuthAPI()

    # Configure page settings
    page.title = "Мое крутое приложение"
    page.padding = 30
    page.window_width = 400
    page.window_height = 600
    page.window_resizable = False

    # Routing system
    def route_change(e):
        page.views.clear()

        if e.route == "/dashboard":
            view = ft.View("/dashboard", [dashboard_page(page, auth_api)])
        else:
            view = ft.View("/", [LoginRegisterPage(page, auth_api).view])

        page.views.append(view)
        page.update()

    page.on_route_change = route_change
    page.go(page.route)


if __name__ == "__main__":
    ft.app(target=main)
