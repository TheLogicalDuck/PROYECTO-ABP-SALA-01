import flet as ft

def main(page: ft.Page):
    page.title = "ÁBACO (Makey Makey compatible)"
    page.bgcolor = ft.Colors.WHITE
    page.window_width = 540
    page.window_height = 420
    page.window_resizable = False
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_focused = True

    # === Estado inicial ===
    current_number = 1
    value1 = 0
    value2 = 0
    operation = "SUMA"
    num_balls = 9

    # === Crear filas de bolitas ===
    def create_row():
        return [
            ft.Container(
                width=28,
                height=28,
                border_radius=28,
                bgcolor=ft.Colors.GREY_300,
                border=ft.border.all(1, ft.Colors.BLACK),
                margin=ft.margin.all(2),
            )
            for _ in range(num_balls)
        ]

    balls_row1 = create_row()
    balls_row2 = create_row()

    row1 = ft.Row(balls_row1, spacing=0)
    row2 = ft.Row(balls_row2, spacing=0)

    # === Labels y textos ===
    num1_label = ft.Container(ft.Text(" Número 1 ", weight=ft.FontWeight.BOLD), bgcolor=ft.Colors.GREY_200, padding=6)
    num2_label = ft.Container(ft.Text(" Número 2 ", weight=ft.FontWeight.BOLD), bgcolor=ft.Colors.GREY_200, padding=6)
    op_label = ft.Container(ft.Text(" Operación seleccionada: "), bgcolor=ft.Colors.GREY_100, padding=6)
    result_label = ft.Container(ft.Text(" Resultado: "), bgcolor=ft.Colors.GREY_100, padding=6)

    op_text = ft.Text(operation, weight=ft.FontWeight.BOLD)
    result_text = ft.Text("0", size=18, weight=ft.FontWeight.BOLD)
    value1_text = ft.Text(str(value1))
    value2_text = ft.Text(str(value2))

    # === Funciones de actualización ===
    def update_balls(row, val, color):
        for i in range(num_balls):
            row[i].bgcolor = color if i < val else ft.Colors.GREY_300

    def update_result():
        res = value1 + value2 if operation == "SUMA" else value1 - value2
        result_text.value = str(res)

    def refresh():
        num1_label.bgcolor = ft.Colors.BLUE_100 if current_number == 1 else ft.Colors.GREY_200
        num2_label.bgcolor = ft.Colors.RED_100 if current_number == 2 else ft.Colors.GREY_200
        op_text.value = operation
        value1_text.value = str(value1)
        value2_text.value = str(value2)
        update_balls(balls_row1, value1, ft.Colors.BLUE)
        update_balls(balls_row2, value2, ft.Colors.RED)
        update_result()
        page.update()

    def reset():
        nonlocal value1, value2, current_number, operation
        value1 = value2 = 0
        current_number = 1
        operation = "SUMA"
        refresh()

    # === Control por teclado (Makey Makey y normal) ===
    def on_key(e: ft.KeyboardEvent):
        nonlocal value1, value2, current_number, operation

        key = e.key.lower() if e.key else ""

        # ↑ o W = seleccionar número 1
        if key in ["arrowup", "w"]:
            current_number = 1

        # ↓ o S = seleccionar número 2
        elif key in ["arrowdown", "s"]:
            current_number = 2

        # → o D = mover bolita a la derecha (aumentar)
        elif key in ["arrowright", "d"]:
            if current_number == 1 and value1 < num_balls:
                value1 += 1
            elif current_number == 2 and value2 < num_balls:
                value2 += 1

        # ← o A = mover bolita a la izquierda (disminuir)
        elif key in ["arrowleft", "a"]:
            if current_number == 1 and value1 > 0:
                value1 -= 1
            elif current_number == 2 and value2 > 0:
                value2 -= 1

        # Espacio = cambiar suma/resta
        elif key in [" ", "space"]:
            operation = "RESTA" if operation == "SUMA" else "SUMA"

        # R = resetear
        elif key == "r":
            reset()

        refresh()

    # ✅ esta versión sí funciona bien en Flet 0.28.3
    page.on_keyboard = on_key

    # === Interfaz ===
    page.add(
        ft.Column(
            [
                ft.Text("ÁBACO", size=24, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.Row([num1_label, row1, value1_text], alignment=ft.MainAxisAlignment.START),
                ft.Row([num2_label, row2, value2_text], alignment=ft.MainAxisAlignment.START),
                ft.Row([op_label, op_text]),
                ft.Row([result_label, result_text]),
                ft.Divider(),
                ft.Text(
                    "Controles Makey Makey:\n"
                    "W = Número 1\nS = Número 2\nA/D = Mover bolitas\n"
                    "Espacio = Cambiar SUMA/RESTA\nR = Reset",
                    italic=True,
                    size=13,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            spacing=10,
        )
    )

    refresh()
    page.update()

ft.app(target=main)
