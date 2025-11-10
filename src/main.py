import flet as ft
import random

def main(page: ft.Page):
    page.title = "ÁBACO con Teclado"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 540
    page.window_height = 380
    page.window_resizable = False
    
    page.padding = 0
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
    num1_label = ft.Container(ft.Text(" Número 1 ", weight=ft.FontWeight.BOLD), bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.BLACK), padding=6, border_radius=5)
    num2_label = ft.Container(ft.Text(" Número 2 ", weight=ft.FontWeight.BOLD), bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.BLACK), padding=6, border_radius=5)
    op_label = ft.Container(ft.Text(" Operación seleccionada: "), bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.BLACK), padding=6, border_radius=5)
    result_label = ft.Container(ft.Text(" Resultado: "), bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.BLACK), padding=6, border_radius=5)
    
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
        num1_label.bgcolor = ft.Colors.with_opacity(0.8, ft.Colors.BLUE_900) if current_number == 1 else ft.Colors.with_opacity(0.5, ft.Colors.BLACK)
        num2_label.bgcolor = ft.Colors.with_opacity(0.8, ft.Colors.RED_900) if current_number == 2 else ft.Colors.with_opacity(0.5, ft.Colors.BLACK)
        op_text.value = operation
        value1_text.value = str(value1)
        value2_text.value = str(value2)
        update_balls(balls_row1, value1, "bola_azul.png")
        update_balls(balls_row2, value2, "bola_roja.png")
        update_result()
        page.update()

    def reset():
        nonlocal value1, value2, current_number, operation
        value1, value2, current_number, operation = 0, 0, 1, "SUMA"
        all_sound.play()
        refresh_ui()

    # --- ACCIONES CONTROLADAS POR TECLADO ---
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
        elif current_number == 2 and value2 < num_balls:
            value2 += 1
        play_sound()
        refresh_ui()

    def decrement():
        nonlocal value1, value2
        if current_number == 1 and value1 > 0:
            value1 -= 1
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
        key_map = {
            "w": select_up, "s": select_down,
            "d": increment, "a": decrement,
            " ": toggle_operation, "r": reset,
        }
        action = key_map.get((e.key or "").lower())
        if action:
            action()

    page.on_keyboard_event = on_key

    # --- CONSTRUCCIÓN DE LA INTERFAZ PRINCIPAL ---
    content_column = ft.Column(
        [
            ft.Text("ÁBACO", size=24, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
            ft.Row([num1_label, row1_ui, ft.Column([ft.Text("  "), value1_text])], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([num2_label, row2_ui, ft.Column([ft.Text("  "), value2_text])], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([op_label, op_text, ft.Column([ft.Text("  "), result_label, result_text])], alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(),
            ft.Text("Usa el teclado:", weight=ft.FontWeight.BOLD),
            ft.Text(" 'W' y 'S': Seleccionar fila | 'A' y 'D': Quitar y Añadir bolita"),
            ft.Text(" 'Espacio': Cambiar operación | 'R': Resetear"),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=12,
    )
    
    page.add(
        ft.Stack(
            [
                ft.Image(
                    src="bg.png",
                    fit=ft.ImageFit.COVER,
                    expand=True,
                ),
                
                ft.Container(
                    content=ft.Container(
                        content=content_column,
                        padding=20,
                        bgcolor=ft.Colors.with_opacity(0.7, ft.Colors.WHITE),
                        border_radius=10,
                    ),
                    alignment=ft.alignment.center,
                    expand=True,
                )
            ],
            expand=True,
        )
    )

    refresh_ui()
    page.update()

# --- INICIAR LA APLICACIÓN ---
ft.app(target=main, assets_dir="assets")