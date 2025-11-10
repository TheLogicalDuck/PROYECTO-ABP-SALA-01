import flet as ft
import random

def main(page: ft.Page):
    page.title = "ÁBACO con Teclado"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 580
    page.window_height = 550
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
    value1, value2, value3, value4, value5 = 0, 0, 0, 0, 0
    operation = "SUMA"
    num_balls = 15
    num_rows = 5

    # --- FUNCIÓN PARA REPRODUCIR SONIDO ---
    def play_sound():
        random.choice(audio_effects).play()

    # --- FUNCIONES PARA CREAR LA INTERFAZ ---
    def create_balls():
        """Crea la lista de contenedores de bolas para una fila."""
        return [
            ft.Container(
                width=38,
                height=38,
                content=ft.Image(
                    src="bola_gris.png",
                    fit=ft.ImageFit.CONTAIN,
                    opacity=0.5,
                ),
                # Esta animación se aplicará a cualquier cambio de propiedad, incluido el margen (margin)
                animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT_BACK),
            )
            for _ in range(num_balls)
        ]

    def create_abacus_row(balls_ui_row):
        """Crea una fila de ábaco completa con el palito detrás de las bolas."""
        rod = ft.Container(
            width=2500,
            height=6,
            bgcolor=ft.Colors.BROWN_400,
            border_radius=5,
        )
        
        return ft.Stack(
            [
                ft.Container(
                    content=rod,
                    alignment=ft.alignment.center,
                ),
                balls_ui_row,
            ]
        )

    # --- CREACIÓN DE LAS FILAS DE BOLAS ---
    balls_row1, balls_row2, balls_row3, balls_row4, balls_row5 = (create_balls() for _ in range(5))

    # --- CREACIÓN DE LAS FILAS DE UI (CON PALITOS) ---
    abacus_row1 = create_abacus_row(ft.Row(balls_row1, spacing=-15))
    abacus_row2 = create_abacus_row(ft.Row(balls_row2, spacing=-15))
    abacus_row3 = create_abacus_row(ft.Row(balls_row3, spacing=-15))
    abacus_row4 = create_abacus_row(ft.Row(balls_row4, spacing=-15))
    abacus_row5 = create_abacus_row(ft.Row(balls_row5, spacing=-15))

    # --- LABELS Y TEXTOS DE LA INTERFAZ ---
    num1_label = ft.Container(ft.Text(" Número 1 ", weight=ft.FontWeight.BOLD), bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.BLACK), padding=6, border_radius=5)
    num2_label = ft.Container(ft.Text(" Número 2 ", weight=ft.FontWeight.BOLD), bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.BLACK), padding=6, border_radius=5)
    num3_label = ft.Container(ft.Text(" Número 3 ", weight=ft.FontWeight.BOLD), bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.BLACK), padding=6, border_radius=5)
    num4_label = ft.Container(ft.Text(" Número 4 ", weight=ft.FontWeight.BOLD), bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.BLACK), padding=6, border_radius=5)
    num5_label = ft.Container(ft.Text(" Número 5 ", weight=ft.FontWeight.BOLD), bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.BLACK), padding=6, border_radius=5)
    
    op_label = ft.Container(ft.Text(" Operación: "), bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.BLACK), padding=6, border_radius=5)
    result_label = ft.Container(ft.Text(" Resultado: "), bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.BLACK), padding=6, border_radius=5)
    
    op_text = ft.Text(operation, weight=ft.FontWeight.BOLD)
    result_text = ft.Text("0", size=18, weight=ft.FontWeight.BOLD)
    value1_text, value2_text, value3_text, value4_text, value5_text = (ft.Text("0") for _ in range(5))

    # --- LÓGICA DE LA APLICACIÓN ---
    def update_balls(row_balls, value, active_image_src):
        """Mueve las bolas a la izquierda o derecha usando la propiedad 'margin'."""
        gap_pixels = 120  # Espacio en el centro del ábaco
        
        # El punto que divide las bolas activas de las inactivas
        split_index = num_balls - value

        for i in range(num_balls):
            ball_container = row_balls[i]
            ball_image = ball_container.content
            
            # Bolas inactivas a la izquierda
            if i < split_index:
                ball_container.margin = ft.margin.all(0) # Sin margen, se agrupan a la izquierda
                ball_image.src = "bola_gris.png"
                ball_image.opacity = 0.5
            # Bolas activas a la derecha
            else:
                # Si esta es la PRIMERA bola activa, le aplicamos un gran margen
                # para crear el espacio que empuja a todo el grupo a la derecha.
                if i == split_index:
                    ball_container.margin = ft.margin.only(left=gap_pixels)
                # Las demás bolas activas no necesitan margen extra
                else:
                    ball_container.margin = ft.margin.all(0)

                ball_image.src = active_image_src
                ball_image.opacity = 1


    def update_result():
        total = value1 + value2 + value3 + value4 + value5
        res = total if operation == "SUMA" else value1 - value2 - value3 - value4 - value5
        result_text.value = str(res)

    def refresh_ui():
        labels = [num1_label, num2_label, num3_label, num4_label, num5_label]
        colors = [ft.Colors.BLUE_900, ft.Colors.RED_900, ft.Colors.GREEN_900, ft.Colors.AMBER_900, ft.Colors.PURPLE_900]
        for i, label in enumerate(labels):
            label.bgcolor = ft.Colors.with_opacity(0.8, colors[i]) if current_number == i + 1 else ft.Colors.with_opacity(0.5, ft.Colors.BLACK)

        op_text.value = operation
        value1_text.value, value2_text.value, value3_text.value, value4_text.value, value5_text.value = str(value1), str(value2), str(value3), str(value4), str(value5)

        update_balls(balls_row1, value1, "bola_azul.png")
        update_balls(balls_row2, value2, "bola_roja.png")
        update_balls(balls_row3, value3, "bola_verde.png")
        update_balls(balls_row4, value4, "bola_amarilla.png")
        update_balls(balls_row5, value5, "bola_morada.png")
        
        update_result()
        page.update()

    def reset():
        nonlocal value1, value2, value3, value4, value5, current_number, operation
        value1, value2, value3, value4, value5, current_number, operation = 0, 0, 0, 0, 0, 1, "SUMA"
        all_sound.play()
        refresh_ui()

    # --- ACCIONES CONTROLADAS POR TECLADO ---
    def select_up():
        nonlocal current_number
        if current_number > 1:
            current_number -= 1
            select_sound.play()
            refresh_ui()

    def select_down():
        nonlocal current_number
        if current_number < num_rows:
            current_number += 1
            select_sound.play()
            refresh_ui()

    def increment():
        nonlocal value1, value2, value3, value4, value5
        values = [value1, value2, value3, value4, value5]
        if values[current_number - 1] < num_balls:
            values[current_number - 1] += 1
            value1, value2, value3, value4, value5 = values
            play_sound()
            refresh_ui()

    def decrement():
        nonlocal value1, value2, value3, value4, value5
        values = [value1, value2, value3, value4, value5]
        if values[current_number - 1] > 0:
            values[current_number - 1] -= 1
            value1, value2, value3, value4, value5 = values
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
        if action: action()

    page.on_keyboard_event = on_key

    # --- CONSTRUCCIÓN DE LA INTERFAZ PRINCIPAL ---
    abacus_container_width = 410
    content_column = ft.Column(
        [
            ft.Text("ÁBACO", size=24, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
            ft.Row([num1_label, ft.Container(content=abacus_row1, width=abacus_container_width), value1_text], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Row([num2_label, ft.Container(content=abacus_row2, width=abacus_container_width), value2_text], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Row([num3_label, ft.Container(content=abacus_row3, width=abacus_container_width), value3_text], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Row([num4_label, ft.Container(content=abacus_row4, width=abacus_container_width), value4_text], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Row([num5_label, ft.Container(content=abacus_row5, width=abacus_container_width), value5_text], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Row([op_label, op_text, result_label, result_text], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
            ft.Divider(),
            ft.Text("Usa el teclado:", weight=ft.FontWeight.BOLD),
            ft.Text(" 'W' y 'S': Seleccionar fila | 'A' y 'D': Mover bolas"),
            ft.Text(" 'Espacio': Cambiar operación | 'R': Resetear"),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=12,
    )
    
    page.add(
        ft.Stack(
            [
                ft.Image(src="bg.png", fit=ft.ImageFit.COVER, expand=True),
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

# --- INICIAR LA APLICACIÓN ---
ft.app(target=main, assets_dir="assets")