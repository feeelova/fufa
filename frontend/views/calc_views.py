import flet as ft
from frontend.utils.helpers import show_snackbar


class BudgetPage:
    def __init__(self, page: ft.Page, go_back):
        self.page = page
        self.go_back = go_back
        self.categories = []
        self.selected_template = "custom"

        # Стили
        field_style = {
            "width": 200,
            "height": 45,
            "border_radius": 10,
            "border_color": ft.colors.GREY_400,
            "content_padding": 10,
            "focused_border_color": ft.colors.TEAL_700,
        }

        button_style = {
            "height": 45,
            "style": ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        }

        # Элементы управления
        self.income_input = ft.TextField(
            label="Ежемесячный доход (₽)",
            keyboard_type=ft.KeyboardType.NUMBER,
            **{**field_style, "width": 250},
        )

        self.new_category_name = ft.TextField(label="Название категории", **field_style)
        self.new_category_percent = ft.TextField(
            label="Процент",
            keyboard_type=ft.KeyboardType.NUMBER,
            **{**field_style, "width": 120},
        )

        self.add_category_btn = ft.ElevatedButton(
            "Добавить",
            icon=ft.icons.ADD,
            **button_style,
            on_click=self.add_category,
            bgcolor=ft.colors.TEAL_700,
            color=ft.colors.WHITE,
        )

        self.category_list = ft.ListView(expand=True, spacing=10)

        # Форма добавления категорий
        self.add_category_row = ft.Row(
            [
                self.new_category_name,
                self.new_category_percent,
                self.add_category_btn,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
            visible=False,
        )

        self.template_selector = ft.Dropdown(
            options=[
                ft.dropdown.Option("50/30/20", "Классический (50/30/20)"),
                ft.dropdown.Option("60/30/10", "Экономный (60/30/10)"),
                ft.dropdown.Option("custom", "Пользовательский"),
            ],
            value="custom",
            width=250,
            on_change=self.apply_template,
        )

        # Верхняя панель с настройками
        self.top_panel = ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        content=self.template_selector,
                        padding=10,
                        bgcolor=ft.colors.PURPLE_50,
                        border_radius=10,
                    ),
                    ft.VerticalDivider(width=20, color=ft.colors.PURPLE_100),
                    ft.Container(
                        content=self.income_input,
                        padding=10,
                        bgcolor=ft.colors.TEAL_50,
                        border_radius=10,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            ),
            margin=ft.margin.symmetric(vertical=10),
        )

        self.view = ft.Container(
            content=ft.Column(
                [
                    # Шапка
                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.icons.ARROW_BACK,
                                on_click=lambda e: self.go_back(),
                                icon_color=ft.colors.PURPLE_900,
                                tooltip="Назад",
                            ),
                            ft.Text(
                                "📊 Умный бюджет",
                                size=26,
                                weight=ft.FontWeight.W_700,
                                color=ft.colors.PURPLE_900,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    ft.Divider(height=20, color=ft.colors.PURPLE_100),
                    # Верхняя панель
                    self.top_panel,
                    # Основное содержимое
                    ft.Container(
                        content=ft.Column(
                            [
                                self.add_category_row,
                                ft.Container(
                                    content=self.category_list,
                                    height=300,
                                    padding=10,
                                    bgcolor=ft.colors.GREY_50,
                                    border_radius=10,
                                    shadow=ft.BoxShadow(
                                        spread_radius=1,
                                        blur_radius=5,
                                        color=ft.colors.PURPLE_100,
                                    ),
                                ),
                            ],
                            scroll=ft.ScrollMode.AUTO,
                            spacing=15,
                        ),
                        expand=True,
                    ),
                    # Нижняя панель
                    ft.Container(
                        content=ft.ElevatedButton(
                            "🧮 Рассчитать бюджет",
                            icon=ft.icons.CALCULATE_OUTLINED,
                            **button_style,
                            on_click=self.calculate_budget,
                            bgcolor=ft.colors.PURPLE_700,
                            color=ft.colors.WHITE,
                        ),
                        padding=ft.padding.only(top=20),
                        alignment=ft.alignment.center,
                    ),
                ],
                spacing=15,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            ),
            padding=30,
            bgcolor=ft.colors.WHITE,
            border_radius=20,
            shadow=ft.BoxShadow(
                spread_radius=2,
                blur_radius=20,
                color=ft.colors.PURPLE_100,
                offset=ft.Offset(0, 4),
            ),
            expand=True,
        )

        # Инициализация начального состояния
        self.apply_template(None, initial=True)

    def apply_template(self, e, initial=False):
        template = self.template_selector.value
        self.categories.clear()

        if template == "50/30/20":
            self.categories = [
                {"name": "🏠 Обязательные расходы", "percent": 50},
                {"name": "🎉 Желания", "percent": 30},
                {"name": "💰 Сбережения", "percent": 20},
            ]
        elif template == "60/30/10":
            self.categories = [
                {"name": "🏠 Обязательные расходы", "percent": 60},
                {"name": "🎉 Желания", "percent": 30},
                {"name": "💰 Сбережения", "percent": 10},
            ]

        self.add_category_row.visible = template == "custom"
        self.update_category_list()

        if not initial:
            self.page.update()

    def add_category(self, e):
        name = self.new_category_name.value.strip()
        percent = self.new_category_percent.value.strip()

        if not name or not percent:
            show_snackbar(self.page, "Заполните все поля категории", "red")
            return

        try:
            percent = float(percent)
            if percent <= 0:
                raise ValueError
        except:
            show_snackbar(self.page, "Некорректное значение процента", "red")
            return

        total = sum(cat["percent"] for cat in self.categories) + percent
        if total > 100:
            show_snackbar(
                self.page,
                f"Превышена сумма процентов (осталось {100 - total + percent}%)",
                "red",
            )
            return

        self.categories.append({"name": name, "percent": percent})
        self.update_category_list()
        self.new_category_name.value = ""
        self.new_category_percent.value = ""
        self.page.update()

    def update_category_list(self):
        self.category_list.controls = []

        try:
            income = float(self.income_input.value)
        except:
            income = 0

        distributed_total = 0

        for idx, cat in enumerate(self.categories):
            allocated = (cat["percent"] / 100) * income
            distributed_total += allocated

            self.category_list.controls.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text(
                                        cat["name"],
                                        size=16,
                                        weight="bold",
                                        color=ft.colors.PURPLE_900,
                                    ),
                                    ft.Text(
                                        f"{cat['percent']}% → {allocated:.2f}₽",
                                        color=ft.colors.TEAL_700,
                                    ),
                                    ft.ProgressBar(
                                        value=cat["percent"] / 100,
                                        width=200,
                                        color=ft.colors.PURPLE_300,
                                        bgcolor=ft.colors.GREY_200,
                                    ),
                                ],
                                spacing=5,
                                expand=True,
                            ),
                            ft.IconButton(
                                icon=ft.icons.DELETE_FOREVER_ROUNDED,
                                icon_color=ft.colors.RED_700,
                                tooltip="Удалить категорию",
                                on_click=lambda e, idx=idx: self.remove_category(idx),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    bgcolor=ft.colors.WHITE,
                    padding=10,
                    border_radius=10,
                    border=ft.border.all(1, ft.colors.PURPLE_100),
                    margin=ft.margin.symmetric(vertical=3),
                )
            )

        remaining = income - distributed_total
        summary = ft.Container(
            content=ft.Column(
                [
                    ft.Divider(height=20, color=ft.colors.PURPLE_100),
                    ft.Row(
                        [
                            ft.Text(
                                "📈 Общий доход:",
                                size=16,
                                color=ft.colors.PURPLE_900,
                                weight="bold",
                            ),
                            ft.Text(
                                f"{income:.2f}₽",
                                size=16,
                                color=ft.colors.TEAL_700,
                                weight="bold",
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Row(
                        [
                            ft.Text(
                                "📤 Распределено:", size=16, color=ft.colors.PURPLE_900
                            ),
                            ft.Text(
                                f"{distributed_total:.2f}₽",
                                color=ft.colors.TEAL_700,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Row(
                        [
                            ft.Text("🕳 Остаток:", size=16, color=ft.colors.PURPLE_900),
                            ft.Text(
                                f"{remaining:.2f}₽",
                                color=(
                                    ft.colors.RED_700
                                    if remaining > 0
                                    else ft.colors.GREEN_700
                                ),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ],
                spacing=8,
            ),
            padding=10,
            bgcolor=ft.colors.PURPLE_50,
            border_radius=10,
        )

        self.category_list.controls.append(summary)

    def remove_category(self, index):
        del self.categories[index]
        self.update_category_list()
        self.page.update()

    def calculate_budget(self, e):
        try:
            income = float(self.income_input.value)
            if income <= 0:
                raise ValueError
        except:
            show_snackbar(self.page, "Введите корректную сумму дохода", "red")
            return

        if not self.categories:
            show_snackbar(self.page, "Добавьте хотя бы одну категорию", "red")
            return

        total_percent = sum(cat["percent"] for cat in self.categories)
        if total_percent > 100:
            show_snackbar(
                self.page,
                f"Сумма процентов превышает 100% (сейчас {total_percent}%)",
                "red",
            )
            return

        self.update_category_list()
        show_snackbar(self.page, "✅ Бюджет успешно рассчитан!", "green")
        self.page.update()
