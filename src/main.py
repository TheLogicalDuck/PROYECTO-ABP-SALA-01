import flet as ft
import random

def main(page: ft.Page):
    page.title = "ÁBACO con Teclado"
    page.bgcolor = ft.Colors.WHITE
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 540
    page.window_height = 380
    page.window_resizable = False
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    # NUEVO: Centra todo el contenido de la página horizontalmente.
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_focused = True

    # --- EFECTOS DE SONIDO ---

    audio_effects = [
        ft.Audio(src="1.wav", autoplay=False),
        ft.Audio(src="2.wav", autoplay=False),
        ft.Audio(src="3.wav", autoplay=False),
    ]
    switch_sound = ft.Audio(src="switch.wav", autoplay=False)
    all_sound = ft.Audio(src="all.wav", autoplay=False)
    select_sound = ft.Audio(src="select.wav", autoplay=False)

    page.overlay.extend(audio_effects)
    page.overlay.append(switch_sound)
    page.overlay.append(all_sound)
    page.overlay.append(select_sound)

    # --- ESTADO DE LA APLICACIÓN ---
    current_number = 1
    value1 = 0
    value2 = 0
    operation = "SUMA"
    num_balls = 15

    # --- FUNCIÓN PARA REPRODUCIR SONIDO ---
    def play_sound():
        random.choice(audio_effects).play()

    # --- FUNCIONES PARA CREAR LA INTERFAZ ---
    def create_row():
        return [
            ft.Container(
                width=38,
                height=38,
                content=ft.Image(
                    src="bola_gris.png",
                    fit=ft.ImageFit.CONTAIN,
                    opacity=0.5,
                ),
                animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT_BACK),
            )
            for _ in range(num_balls)
        ]

    balls_row1 = create_row()
    balls_row2 = create_row()

    row1_ui = ft.Row(balls_row1, spacing=-15)
    row2_ui = ft.Row(balls_row2, spacing=-15)

    # --- LABELS Y TEXTOS DE LA INTERFAZ ---
    # (Esta sección no cambia)
    num1_label = ft.Container(ft.Text(" Número 1 ", weight=ft.FontWeight.BOLD), bgcolor=ft.Colors.BLACK, padding=6)
    num2_label = ft.Container(ft.Text(" Número 2 ", weight=ft.FontWeight.BOLD), bgcolor=ft.Colors.BLACK, padding=6)
    op_label = ft.Container(ft.Text(" Operación seleccionada: "), bgcolor=ft.Colors.GREY_100, padding=6)
    result_label = ft.Container(ft.Text(" Resultado: "), bgcolor=ft.Colors.GREY_100, padding=6)

    op_text = ft.Text(operation, weight=ft.FontWeight.BOLD)
    result_text = ft.Text("0", size=18, weight=ft.FontWeight.BOLD)
    value1_text = ft.Text(str(value1))
    value2_text = ft.Text(str(value2))

    # --- LÓGICA DE LA APLICACIÓN ---
    def update_balls(row_balls, value, active_image_src):
        for i in range(num_balls):
            ball_container = row_balls[i]
            ball_image = ball_container.content

            if i < value:
                ball_container.margin = ft.margin.only(left=20)
                ball_image.src = active_image_src
                ball_image.opacity = 1
            else:
                ball_container.margin = ft.margin.all(0)
                ball_image.src = "bola_gris.png"
                ball_image.opacity = 0.5

    def update_result():
        res = value1 + value2 if operation == "SUMA" else value1 - value2
        result_text.value = str(res)

    def refresh_ui():
        num1_label.bgcolor = ft.Colors.BLUE_100 if current_number == 1 else ft.Colors.GREY_200
        num2_label.bgcolor = ft.Colors.RED_100 if current_number == 2 else ft.Colors.GREY_200
        op_text.value = operation
        value1_text.value = str(value1)
        value2_text.value = str(value2)
        update_balls(balls_row1, value1, "bola_azul.png")
        update_balls(balls_row2, value2, "bola_roja.png")
        update_result()
        page.update()

    def reset():
        nonlocal value1, value2, current_number, operation
        value1 = 0
        value2 = 0
        current_number = 1
        operation = "SUMA"
        all_sound.play()
        refresh_ui()

    # --- ACCIONES CONTROLADAS POR TECLADO ---
    # (Esta sección no cambia)
    def select_up():
        nonlocal current_number
        if current_number != 1:
            current_number = 1
            select_sound.play()
            refresh_ui()

    def select_down():
        nonlocal current_number
        if current_number != 2:
            current_number = 2
            select_sound.play()
            refresh_ui()

    def increment():
        nonlocal value1, value2
        if current_number == 1 and value1 < num_balls:
            value1 += 1
            play_sound()
        elif current_number == 2 and value2 < num_balls:
            value2 += 1
            play_sound()
        refresh_ui()

    def decrement():
        nonlocal value1, value2
        if current_number == 1 and value1 > 0:
            value1 -= 1
            play_sound()
        elif current_number == 2 and value2 > 0:
            value2 -= 1
            play_sound()
        refresh_ui()

    def toggle_operation():
        nonlocal operation
        operation = "RESTA" if operation == "SUMA" else "SUMA"
        switch_sound.play()
        refresh_ui()

    def on_key(e: ft.KeyboardEvent):
        key = (e.key or " ").lower()
        if key == "w":
            select_up()
        elif key == "s":
            select_down()
        elif key == "d":
            increment()
        elif key == "a":
            decrement()
        elif key == " ":
            toggle_operation()
        elif key == "r":
            reset()

    page.on_keyboard_event = on_key

    # --- CONSTRUCCIÓN DE LA INTERFAZ PRINCIPAL ---
    page.add(
        ft.Column(
            [
                ft.Text("ÁBACO", size=24, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                # MODIFICADO: Se centra la alineación de las filas.
                ft.Row([num1_label, row1_ui, ft.Column([ft.Text("  "), value1_text])], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([num2_label, row2_ui, ft.Column([ft.Text("  "), value2_text])], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([op_label, op_text, ft.Column([ft.Text("  "), result_label, result_text])], alignment=ft.MainAxisAlignment.CENTER),
                ft.Divider(),
                ft.Text("Usa el teclado:", weight=ft.FontWeight.BOLD),
                ft.Text(" 'W' y 'S': Seleccionar fila | 'A' y 'D': Quitar y Añadir bolita"),
                ft.Text(" 'Espacio': Cambiar operación | 'R': Resetear"),
            ],
            # MODIFICADO: La columna ahora centra su contenido horizontalmente.
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=12,
        )
    )

    refresh_ui()
    page.update()

# --- INICIAR LA APLICACIÓN ---
ft.app(target=main, assets_dir="assets")