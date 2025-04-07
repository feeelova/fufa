import flet as ft
from frontend.utils.helpers import show_snackbar


class BudgetPage:
    def __init__(self, page: ft.Page, go_back):
        self.page = page
        self.go_back = go_back  # функция для возврата

        # Стили
        field_style = {
            "width": 300,
            "height": 45,
            "border_radius": 10,
            "border_color": ft.colors.GREY_400,
            "content_padding": 10,
        }

        button_style = {
            "height": 45,
            "style": ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        }

        # Поле для дохода
        self.income_input = ft.TextField(
            label="Ваш ежемесячный доход (₽)",
            keyboard_type=ft.KeyboardType.NUMBER,
            **field_style,
        )

        # Кнопка расчёта
        self.calculate_button = ft.ElevatedButton(
            "Рассчитать бюджет",
            icon=ft.icons.CALCULATE,
            **button_style,
            on_click=self.calculate_budget,
            bgcolor=ft.colors.BLUE_700,
            color=ft.colors.WHITE,
        )

        # Кнопка назад
        self.back_button = ft.ElevatedButton(
            "Назад",
            icon=ft.icons.ARROW_BACK,
            **button_style,
            on_click=lambda e: self.go_back(),
            bgcolor=ft.colors.GREY_200,
            color=ft.colors.BLACK,
        )

        # Колонка для результатов
        self.results_column = ft.Column(spacing=10)

        # Контейнер с интерфейсом
        self.view = ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Автоматическое распределение бюджета",
                        size=24,
                        weight="bold",
                        color=ft.colors.BLUE_900,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Row([self.income_input], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row(
                        [self.calculate_button], alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Divider(),
                    # Контейнер для результатов со скроллом
                    ft.Container(
                        content=ft.Column(
                            [
                                self.results_column,
                                ft.Row(
                                    [self.back_button],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                            ],
                            spacing=20,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            scroll=ft.ScrollMode.AUTO,
                        ),
                        width=500,
                        height=300,  # Ограничим высоту, чтобы всё помещалось
                        padding=10,
                        bgcolor=ft.colors.GREY_100,
                        border_radius=10,
                    ),
                ],
                spacing=30,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=30,
            bgcolor=ft.colors.WHITE,
            border_radius=15,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.colors.BLUE_100,
            ),
        )

    def calculate_budget(self, e):
        try:
            total_income = float(self.income_input.value)
            if total_income <= 0:
                raise ValueError
        except:
            show_snackbar(self.page, "Введите корректную сумму дохода", "red")
            return

        # Категории по 50/30/20
        categories = [
            {"name": "Обязательные расходы", "percent": 50},
            {"name": "Желания и развлечения", "percent": 30},
            {"name": "Сбережения и инвестиции", "percent": 20},
        ]

        results = []
        for cat in categories:
            amount = (total_income * cat["percent"]) / 100
            results.append(
                ft.Container(
                    content=ft.ListTile(
                        title=ft.Text(cat["name"], weight="bold"),
                        subtitle=ft.Text(f"{cat['percent']}%"),
                        trailing=ft.Text(
                            f"{amount:.2f} ₽", color=ft.colors.GREEN_700, weight="bold"
                        ),
                        bgcolor=ft.colors.GREY_50,
                    ),
                    width=450,
                )
            )

        self.results_column.controls = [
            ft.Text("Результаты распределения бюджета:", size=18, weight="bold"),
            *results,
            ft.Divider(),
            ft.Container(
                content=ft.ListTile(
                    title=ft.Text("Общий доход", weight="bold"),
                    trailing=ft.Text(
                        f"{total_income:.2f} ₽", color=ft.colors.BLUE_700, weight="bold"
                    ),
                    bgcolor=ft.colors.BLUE_50,
                ),
                width=450,
            ),
        ]
        self.page.update()
