import flet as ft

def main(page: ft.Page):
    page.title = "ÁBACO"
    page.bgcolor = ft.Colors.WHITE
    page.window_width = 540
    page.window_height = 420
    page.window_resizable = False
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_focused = True

    # estado
    current_number = 1
    value1 = 0
    value2 = 0
    operation = "SUMA"
    num_balls = 9

    # crear bolitas (Containers)
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

    # labels / textos
    num1_label = ft.Container(ft.Text(" Número 1 ", weight=ft.FontWeight.BOLD), bgcolor=ft.Colors.GREY_200, padding=6)
    num2_label = ft.Container(ft.Text(" Número 2 ", weight=ft.FontWeight.BOLD), bgcolor=ft.Colors.GREY_200, padding=6)
    op_label = ft.Container(ft.Text(" Operación seleccionada: "), bgcolor=ft.Colors.GREY_100, padding=6)
    result_label = ft.Container(ft.Text(" Resultado: "), bgcolor=ft.Colors.GREY_100, padding=6)

    op_text = ft.Text(operation, weight=ft.FontWeight.BOLD)
    result_text = ft.Text("0", size=18, weight=ft.FontWeight.BOLD)
    value1_text = ft.Text(str(value1))
    value2_text = ft.Text(str(value2))

    # actualizar bolitas y resultado
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
        value1 = 0
        value2 = 0
        current_number = 1
        operation = "SUMA"
        refresh()

    # acciones (para botones)
    def select_up(e=None):
        nonlocal current_number
        current_number = 1
        refresh()

    def select_down(e=None):
        nonlocal current_number
        current_number = 2
        refresh()

    def inc(e=None):
        nonlocal value1, value2
        if current_number == 1 and value1 < num_balls:
            value1 += 1
        elif current_number == 2 and value2 < num_balls:
            value2 += 1
        refresh()

    def dec(e=None):
        nonlocal value1, value2
        if current_number == 1 and value1 > 0:
            value1 -= 1
        elif current_number == 2 and value2 > 0:
            value2 -= 1
        refresh()

    def toggle_op(e=None):
        nonlocal operation
        operation = "RESTA" if operation == "SUMA" else "SUMA"
        refresh()

    # manejador de teclado
    def on_key(e):
        nonlocal value1, value2, current_number, operation
        try:
            key = getattr(e, "key", None) or getattr(e, "data", None) or str(e)
            if isinstance(key, dict) and "key" in key:
                key = key["key"]
        except Exception:
            key = None

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

    # vincular teclado
    attached = False
    try:
        if hasattr(page, "on_keyboard"):
            page.on_keyboard = on_key
            attached = True
    except Exception:
        attached = False

    if not attached:
        try:
            if hasattr(page, "on_keyboard_event"):
                page.on_keyboard_event = on_key
                attached = True
        except Exception:
            attached = False

    hidden_tf = None
    if not attached:
        try:
            hidden_tf = ft.TextField(
                value="",
                width=0,
                height=0,
                visible=False,
                autofocus=True,
            )
            try:
                hidden_tf.on_keyboard_event = on_key
            except Exception:
                try:
                    hidden_tf.on_change = lambda e: None
                except Exception:
                    pass
            page.add(hidden_tf)
            attached = True
        except Exception:
            attached = False

    # Controles de botones
    controls = ft.Row(
        [
            ft.Column(
                [
                    ft.Text("Controles (clic):", weight=ft.FontWeight.BOLD),
                    ft.Row(
                        [
                            ft.ElevatedButton("↑ Seleccionar N1", on_click=select_up),
                            ft.ElevatedButton("↓ Seleccionar N2", on_click=select_down),
                        ],
                        spacing=10,
                    ),
                    ft.Row(
                        [
                            ft.ElevatedButton("← Quitar", on_click=dec),
                            ft.ElevatedButton("→ Añadir", on_click=inc),
                        ],
                        spacing=10,
                    ),
                    ft.Row(
                        [
                            ft.ElevatedButton("Espacio: Cambiar + / -", on_click=toggle_op),
                            ft.ElevatedButton("R: Reset", on_click=lambda e: reset()),
                        ],
                        spacing=10,
                    ),
                ],
                spacing=8,
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # Interfaz principal
    page.add(
        ft.Column(
            [
                ft.Text("ÁBACO", size=24, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.Row([num1_label, row1, ft.Column([ft.Text("  "), value1_text])], alignment=ft.MainAxisAlignment.START),
                ft.Row([num2_label, row2, ft.Column([ft.Text("  "), value2_text])], alignment=ft.MainAxisAlignment.START),
                ft.Row([op_label, op_text, ft.Column([ft.Text("  "), result_label, result_text])], alignment=ft.MainAxisAlignment.START),
                ft.Text("Usa el teclado: ↑ ↓ → ← espacio y R", italic=True, size=12),
                ft.Divider(),
                ft.Text("Estado de captura de teclado: " + ("✅ conectado" if attached else "❌ no conectado"), italic=True, size=12),
                controls,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            spacing=12,
        )
    )

    refresh()
    page.update()


ft.app(target=main)