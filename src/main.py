import flet as ft

def main(page: ft.Page):
    page.title = "ÁBACO"
    page.bgcolor = ft.Colors.WHITE
    page.window_width = 500
    page.window_height = 400
    page.window_resizable = False

    # Variables iniciales
    current_number = 1
    value1 = 0
    value2 = 0
    operation = "SUMA"

    num_balls = 9

    # Crear dos filas de bolitas
    def create_row():
        return [ft.Container(
            width=25,
            height=25,
            border_radius=25,
            bgcolor=ft.Colors.GREY_300,
            border=ft.border.all(1, ft.Colors.BLACK)
        ) for _ in range(num_balls)]

    balls_row1 = create_row()
    balls_row2 = create_row()

    row1 = ft.Row(balls_row1, spacing=5)
    row2 = ft.Row(balls_row2, spacing=5)

    # Textos dinámicos
    num1_label = ft.Container(ft.Text("Número 1:", weight=ft.FontWeight.BOLD), bgcolor=ft.Colors.BLUE_50, padding=5)
    num2_label = ft.Container(ft.Text("Número 2:", weight=ft.FontWeight.BOLD), bgcolor=ft.Colors.RED_50, padding=5)
    op_label = ft.Container(ft.Text("Operación seleccionada:"), bgcolor=ft.Colors.GREY_100, padding=5)
    result_label = ft.Container(ft.Text("Resultado:"), bgcolor=ft.Colors.GREY_100, padding=5)

    op_text = ft.Text(operation, weight=ft.FontWeight.BOLD)
    result_text = ft.Text("0", size=18, weight=ft.FontWeight.BOLD)

    # Función para actualizar colores de bolitas
    def update_balls(row, val):
        for i in range(num_balls):
            row[i].bgcolor = ft.Colors.BLUE if i < val else ft.Colors.GREY_300

    # Calcular resultado
    def update_result():
        res = value1 + value2 if operation == "SUMA" else value1 - value2
        result_text.value = str(res)

    # Refrescar toda la interfaz
    def refresh():
        num1_label.bgcolor = ft.Colors.BLUE_100 if current_number == 1 else ft.Colors.GREY_200
        num2_label.bgcolor = ft.Colors.RED_100 if current_number == 2 else ft.Colors.GREY_200
        op_text.value = operation

        update_balls(balls_row1, value1)
        update_balls(balls_row2, value2)
        update_result()
        page.update()

    # Reiniciar todo
    def reset():
        nonlocal value1, value2, current_number, operation
        value1 = value2 = 0
        current_number = 1
        operation = "SUMA"
        refresh()

    # Control con teclado
    def on_key(e: ft.KeyboardEvent):
        nonlocal value1, value2, current_number, operation
        if e.key == "ArrowUp":
            current_number = 1
        elif e.key == "ArrowDown":
            current_number = 2
        elif e.key == "ArrowRight":
            if current_number == 1 and value1 < num_balls:
                value1 += 1
            elif current_number == 2 and value2 < num_balls:
                value2 += 1
        elif e.key == "ArrowLeft":
            if current_number == 1 and value1 > 0:
                value1 -= 1
            elif current_number == 2 and value2 > 0:
                value2 -= 1
        elif e.key == " ":
            operation = "RESTA" if operation == "SUMA" else "SUMA"
        elif e.key.lower() == "r":
            reset()
        refresh()

    page.on_keyboard_event = on_key

    # Layout principal
    page.add(
        ft.Column(
            [
                ft.Text("ÁBACO", size=22, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.Row([num1_label, row1, ft.Text(lambda: str(value1))]),
                ft.Row([num2_label, row2, ft.Text(lambda: str(value2))]),
                ft.Row([op_label, op_text]),
                ft.Row([result_label, result_text]),
                ft.Text("(Usa ↑ ↓ → ←  espacio y R para controlar)", italic=True, size=12),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            spacing=10,
        )
    )

    refresh()

ft.app(target=main)
