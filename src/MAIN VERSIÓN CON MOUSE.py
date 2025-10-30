import flet as ft

def main(page: ft.Page):
    page.title = "ÁBACO con Teclado"
    page.bgcolor = ft.Colors.WHITE
    page.window_width = 540
    page.window_height = 380
    page.window_resizable = False
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_focused = True

    # --- ESTADO DE LA APLICACIÓN ---
    current_number = 1  # 1 para la fila de arriba, 2 para la de abajo
    value1 = 0
    value2 = 0
    operation = "SUMA"
    num_balls = 10

    # --- FUNCIONES PARA CREAR LA INTERFAZ ---
    def create_row():
        """Crea una fila de 9 bolitas grises."""
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

    row1_ui = ft.Row(balls_row1, spacing=0)
    row2_ui = ft.Row(balls_row2, spacing=0)

    # --- LABELS Y TEXTOS DE LA INTERFAZ ---
    num1_label = ft.Container(ft.Text(" Número 1 ", weight=ft.FontWeight.BOLD), bgcolor=ft.Colors.GREY_200, padding=6)
    num2_label = ft.Container(ft.Text(" Número 2 ", weight=ft.FontWeight.BOLD), bgcolor=ft.Colors.GREY_200, padding=6)
    op_label = ft.Container(ft.Text(" Operación seleccionada: "), bgcolor=ft.Colors.GREY_100, padding=6)
    result_label = ft.Container(ft.Text(" Resultado: "), bgcolor=ft.Colors.GREY_100, padding=6)

    op_text = ft.Text(operation, weight=ft.FontWeight.BOLD)
    result_text = ft.Text("0", size=18, weight=ft.FontWeight.BOLD)
    value1_text = ft.Text(str(value1))
    value2_text = ft.Text(str(value2))

    # --- LÓGICA DE LA APLICACIÓN ---

    def update_balls(row_balls, value, color):
        """Actualiza el color de las bolitas según el valor."""
        for i in range(num_balls):
            row_balls[i].bgcolor = color if i < value else ft.Colors.GREY_300

    def update_result():
        """Calcula y muestra el resultado de la operación."""
        res = value1 + value2 if operation == "SUMA" else value1 - value2
        result_text.value = str(res)

    def refresh_ui():
        """Actualiza toda la interfaz gráfica para reflejar el estado actual."""
        # Resalta la fila seleccionada
        num1_label.bgcolor = ft.Colors.BLUE_100 if current_number == 1 else ft.Colors.GREY_200
        num2_label.bgcolor = ft.Colors.RED_100 if current_number == 2 else ft.Colors.GREY_200
        
        # Actualiza textos
        op_text.value = operation
        value1_text.value = str(value1)
        value2_text.value = str(value2)
        
        # Actualiza el color de las bolitas y el resultado
        update_balls(balls_row1, value1, ft.Colors.BLUE)
        update_balls(balls_row2, value2, ft.Colors.RED)
        update_result()
        
        page.update()

    def reset():
        """Resetea el ábaco a su estado inicial."""
        nonlocal value1, value2, current_number, operation
        value1 = 0
        value2 = 0
        current_number = 1
        operation = "SUMA"
        refresh_ui()

    # --- ACCIONES CONTROLADAS POR TECLADO ---

    def select_up():
        nonlocal current_number
        current_number = 1
        refresh_ui()

    def select_down():
        nonlocal current_number
        current_number = 2
        refresh_ui()

    def increment():
        nonlocal value1, value2
        if current_number == 1 and value1 < num_balls:
            value1 += 1
        elif current_number == 2 and value2 < num_balls:
            value2 += 1
        refresh_ui()

    def decrement():
        nonlocal value1, value2
        if current_number == 1 and value1 > 0:
            value1 -= 1
        elif current_number == 2 and value2 > 0:
            value2 -= 1
        refresh_ui()

    def toggle_operation():
        nonlocal operation
        operation = "RESTA" if operation == "SUMA" else "SUMA"
        refresh_ui()

    # --- MANEJADOR DE EVENTOS DE TECLADO ---
    
    def normalize_key(key: str) -> str:
        """Convierte la tecla a un formato estándar en minúsculas."""
        key = (key or "").lower()
        if key == " ":
            return "space"
        return key

    def on_key(e: ft.KeyboardEvent):
        """Maneja las pulsaciones de teclado para controlar el ábaco."""
        key = normalize_key(e.key)
        
        if key == "w":
            select_up()
        elif key == "s":
            select_down()
        elif key == "d":
            increment()
        elif key == "a":
            decrement()
        elif key == "space":
            toggle_operation()
        elif key == "r":
            reset()

    page.on_keyboard_event = on_key

    # --- CONSTRUCCIÓN DE LA INTERFAZ PRINCIPAL ---
    page.add(
        ft.Column(
            [
                ft.Text("ÁBACO", size=24, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.Row([num1_label, row1_ui, ft.Column([ft.Text("  "), value1_text])], alignment=ft.MainAxisAlignment.START),
                ft.Row([num2_label, row2_ui, ft.Column([ft.Text("  "), value2_text])], alignment=ft.MainAxisAlignment.START),
                ft.Row([op_label, op_text, ft.Column([ft.Text("  "), result_label, result_text])], alignment=ft.MainAxisAlignment.START),
                ft.Divider(),
                ft.Text("Usa el teclado:", weight=ft.FontWeight.BOLD),
                ft.Text(" 'W' y 'S': Seleccionar fila | 'A' y 'D': Quitar y Añadir bolita"),
                ft.Text(" 'Espacio': Cambiar operación | 'R': Resetear"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            spacing=12,
        )
    )

    # Inicializa la interfaz
    refresh_ui()
    page.update()

# --- INICIAR LA APLICACIÓN ---
ft.app(target=main)