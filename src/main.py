import flet as ft

def main(page: ft.Page):
    page.title = "ÁBACO con Makey Makey"
    page.bgcolor = ft.Colors.WHITE
    page.window_width = 540
    page.window_height = 420
    page.window_resizable = False
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # estado
    current_number = 1
    value1 = 0
    value2 = 0
    operation = "SUMA"
    num_balls = 9

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

    num1_label = ft.Container(ft.Text(" Número 1 ", weight=ft.FontWeight.BOLD), bgcolor=ft.Colors.GREY_200, padding=6)
    num2_label = ft.Container(ft.Text(" Número 2 ", weight=ft.FontWeight.BOLD), bgcolor=ft.Colors.GREY_200, padding=6)
    op_label = ft.Container(ft.Text(" Operación seleccionada: "), bgcolor=ft.Colors.GREY_100, padding=6)
    result_label = ft.Container(ft.Text(" Resultado: "), bgcolor=ft.Colors.GREY_100, padding=6)

    op_text = ft.Text(operation, weight=ft.FontWeight.BOLD)
    result_text = ft.Text("0", size=18, weight=ft.FontWeight.BOLD)
    value1_text = ft.Text(str(value1))
    value2_text = ft.Text(str(value2))

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
        hidden_tf.focus()  # mantener foco para Makey Makey

    def reset():
        nonlocal value1, value2, current_number, operation
        value1 = 0
        value2 = 0
        current_number = 1
        operation = "SUMA"
        refresh()

    def on_key(e):
        nonlocal value1, value2, current_number, operation
        key = getattr(e, "key", None) or getattr(e, "data", None)

        if key in ("ArrowUp", "Up"):
            current_number = 1
        elif key in ("ArrowDown", "Down"):
            current_number = 2
        elif key in ("ArrowRight", "Right"):
            if current_number == 1 and value1 < num_balls:
                value1 += 1
            elif current_number == 2 and value2 < num_balls:
                value2 += 1
        elif key in ("ArrowLeft", "Left"):
            if current_number == 1 and value1 > 0:
                value1 -= 1
            elif current_number == 2 and value2 > 0:
                value2 -= 1
        elif key in (" ", "Spacebar", "Space"):
            operation = "RESTA" if operation == "SUMA" else "SUMA"
        elif isinstance(key, str) and key.lower() == "r":
            reset()

        refresh()

    # Crear el TextField sin argumentos no compatibles
    hidden_tf = ft.TextField(visible=False, autofocus=True)
    try:
        hidden_tf.on_keyboard_event = on_key
    except Exception:
        # fallback si tu versión de Flet solo tiene on_change
        hidden_tf.on_change = lambda e: None

    controls = ft.Row(
        [
            ft.Column(
                [
                    ft.Text("Controles (clic o Makey Makey):", weight=ft.FontWeight.BOLD),
                    ft.Row([
                        ft.ElevatedButton("↑ Número 1", on_click=lambda _: on_key(ft.KeyboardEvent(key="ArrowUp"))),
                        ft.ElevatedButton("↓ Número 2", on_click=lambda _: on_key(ft.KeyboardEvent(key="ArrowDown"))),
                    ]),
                    ft.Row([
                        ft.ElevatedButton("← Quitar", on_click=lambda _: on_key(ft.KeyboardEvent(key="ArrowLeft"))),
                        ft.ElevatedButton("→ Añadir", on_click=lambda _: on_key(ft.KeyboardEvent(key="ArrowRight"))),
                    ]),
                    ft.Row([
                        ft.ElevatedButton("Espacio: + / -", on_click=lambda _: on_key(ft.KeyboardEvent(key="Space"))),
                        ft.ElevatedButton("R: Reset", on_click=lambda _: on_key(ft.KeyboardEvent(key="r"))),
                    ]),
                ]
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    page.add(
        ft.Column(
            [
                ft.Text("ÁBACO (Makey Makey Compatible)", size=22, weight=ft.FontWeight.BOLD),
                ft.Row([num1_label, row1, value1_text]),
                ft.Row([num2_label, row2, value2_text]),
                ft.Row([op_label, op_text, ft.Text("  "), result_label, result_text]),
                ft.Text("(Usa ↑ ↓ ← → espacio y R desde el Makey Makey)", italic=True, size=12),
                ft.Divider(),
                controls,
                hidden_tf,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        )
    )

    refresh()

ft.app(target=main)
