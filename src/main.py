import flet as ft
import random
from math import pi

def main(page: ft.Page):
    page.title = "ÁBACO con Teclado"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 620
    page.window_height = 500
    page.window_resizable = False
    page.padding = 0
    page.bgcolor = ft.Colors.TRANSPARENT
    page.window_bgcolor = ft.Colors.TRANSPARENT

    # --- WIDGETS QUE CAMBIARÁN CON EL TEMA ---
    # Definidos aquí para que la función de cambio de tema pueda acceder a ellos.
    title_text = ft.Text(
        "ÁBACO EN MAKEY MAKEY",
        size=28,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLACK
    )

    background_image = ft.Image(
        src="bg.png",
        fit=ft.ImageFit.COVER,
        expand=False,
        offset=ft.Offset(0, 0.05),
        scale=1.2,
    )

    # --- FUNCIÓN PARA CAMBIAR EL TEMA ---
    def toggle_dark_mode(e):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            title_text.color = ft.Colors.WHITE
            background_image.src = "bgdark.png"
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            title_text.color = ft.Colors.BLACK
            background_image.src = "bg.png"
        page.update()

    # --- BOTÓN DE MODO OSCURO ---
    theme_button = ft.IconButton(
        icon=ft.Icons.BRIGHTNESS_4_OUTLINED,
        on_click=toggle_dark_mode,
        tooltip="Cambiar tema"
    )

    # --- EFECTOS DE SONIDO ---
    audio_effects = [
        ft.Audio(src="1.wav", autoplay=False),
        ft.Audio(src="2.wav", autoplay=False),
        ft.Audio(src="3.wav", autoplay=False),
    ]
    switch_sound = ft.Audio(src="switch.wav", autoplay=False)
    all_sound = ft.Audio(src="all.wav", autoplay=False)
    select_sound = ft.Audio(src="select.wav", autoplay=False)
    page.overlay.extend(audio_effects + [switch_sound, all_sound, select_sound])

    # --- ESTADO DE LA APLICACIÓN ---
    current_number = 1
    value1, value2, value3, value4, value5 = 0, 0, 0, 0, 0
    operation = "SUMA"
    num_balls = 10
    num_rows = 5

    # --- COLORES Y ESTILOS ---
    ROW_COLORS = [ft.Colors.BLUE, ft.Colors.RED, ft.Colors.GREEN, ft.Colors.ORANGE, ft.Colors.PURPLE]
    BALL_IMAGES = ["bola_azul.png", "bola_roja.png", "bola_verde.png", "bola_amarilla.png", "bola_morada.png"]
    SHADOW_EFFECT = ft.BoxShadow(
        spread_radius=1,
        blur_radius=10,
        color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
        offset=ft.Offset(2, 2),
    )

    # --- FUNCIÓN PARA SONIDO ---
    def play_sound():
        random.choice(audio_effects).play()

    # --- CREACIÓN DE BOLAS ---
    def create_balls():
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
                shadow=SHADOW_EFFECT,
                border_radius=ft.border_radius.all(20)
            )
            for _ in range(num_balls)
        ]

    # --- CREACIÓN DE FILA DEL ÁBACO ---
    def create_abacus_row(balls_ui_row):
        balls_width = num_balls * 38 + (num_balls - 1) * 2
        rod_width = balls_width + 136

        rod = ft.Container(
            width=rod_width,
            height=6,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[ft.Colors.GREY_700, ft.Colors.GREY_900],
            ),
            border_radius=5,
        )

        return ft.Stack(
            [
                rod,
                ft.Row(
                    controls=balls_ui_row.controls,
                    spacing=2,
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ],
            alignment=ft.alignment.center,
        )

    # --- FILAS DE BOLAS ---
    all_ball_rows_ui = [ft.Row(create_balls(), spacing=0) for _ in range(num_rows)]
    all_abacus_ui_rows = [create_abacus_row(row) for row in all_ball_rows_ui]

    # --- LABELS Y TEXTOS ---
    all_labels = [
        ft.Container(
            content=ft.Text(f"Número {i+1}", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            width=100,
            alignment=ft.alignment.center,
            padding=8,
            border_radius=8,
            shadow=SHADOW_EFFECT,
            animate_scale=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
        ) for i in range(num_rows)
    ]

    op_text = ft.Text(operation, weight=ft.FontWeight.BOLD, size=16)
    result_text = ft.Text("0", size=24, weight=ft.FontWeight.BOLD)
    all_value_texts = [ft.Text("0", weight=ft.FontWeight.BOLD, size=16) for _ in range(num_rows)]

    # --- ACTUALIZAR BOLAS ---
    def update_balls(row_index, value):
        gap_pixels = 120
        split_index = num_balls - value
        ball_row = all_ball_rows_ui[row_index].controls

        for i, ball_container in enumerate(ball_row):
            ball_image = ball_container.content
            if i < split_index:
                ball_container.margin = ft.margin.all(0)
                ball_image.src = "bola_gris.png"
                ball_image.opacity = 0.5
            else:
                ball_container.margin = ft.margin.only(left=gap_pixels) if i == split_index else ft.margin.all(0)
                ball_image.src = BALL_IMAGES[row_index]
                ball_image.opacity = 1

    # --- CÁLCULO DE RESULTADO ---
    def update_result():
        values = [int(v.value) for v in all_value_texts]
        total = sum(values)
        res = total if operation == "SUMA" else values[0] - sum(values[1:])
        result_text.value = str(res)

    def refresh_ui():
        nonlocal value1, value2, value3, value4, value5
        values = [value1, value2, value3, value4, value5]
        for i in range(num_rows):
            label = all_labels[i]
            if current_number == i + 1:
                label.bgcolor = ROW_COLORS[i]
                label.scale = 1.1
            else:
                label.bgcolor = ft.Colors.with_opacity(0.5, ft.Colors.BLACK)
                label.scale = 1.0
            all_value_texts[i].value = str(values[i])
            update_balls(i, values[i])
        op_text.value = operation
        update_result()
        page.update()

    def reset():
        nonlocal value1, value2, value3, value4, value5, current_number, operation
        value1, value2, value3, value4, value5 = 0, 0, 0, 0, 0
        current_number = 1
        operation = "SUMA"
        all_sound.play()
        refresh_ui()

    # --- CONTROLES DE TECLADO ---
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

    def update_value(delta):
        nonlocal value1, value2, value3, value4, value5
        values = [value1, value2, value3, value4, value5]
        new_value = values[current_number - 1] + delta
        if 0 <= new_value <= num_balls:
            values[current_number - 1] = new_value
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
            "d": lambda: update_value(1), "a": lambda: update_value(-1),
            " ": toggle_operation, "r": reset,
        }
        action = key_map.get(e.key.lower())
        if action:
            action()

    page.on_keyboard_event = on_key

    # --- DISEÑO DE LA INTERFAZ ---
    abacus_rows_with_labels = []
    for i in range(num_rows):
        abacus_rows_with_labels.append(
            ft.Row(
                [
                    all_labels[i],
                    ft.Container(content=all_abacus_ui_rows[i], expand=True),
                    ft.Container(all_value_texts[i], width=30, alignment=ft.alignment.center_right)
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

    content_column = ft.Column(
        [
            title_text,
            ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
            *abacus_rows_with_labels,
            ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
            ft.Card(
                content=ft.Container(
                    content=ft.Row(
                        [
                            ft.Text("Operación:", size=16), op_text,
                            ft.VerticalDivider(width=20),
                            ft.Text("Resultado:", size=16), result_text
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    padding=15,
                )
            ),
            ft.Image(src="instrucciones.png")
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
    )

    # --- ESTRUCTURA PRINCIPAL DE LA PÁGINA ---
    page.add(
        ft.Stack(
            [
                background_image,
                ft.Container(
                    content=content_column,
                    expand=False,
                    padding=ft.padding.symmetric(horizontal=30, vertical=10),
                    margin=15,
                    border_radius=15,
                    border=ft.border.all(2, ft.Colors.with_opacity(0, ft.Colors.WHITE)),
                    bgcolor=ft.Colors.with_opacity(0, ft.Colors.BLACK),
                    shadow=ft.BoxShadow(
                        blur_radius=30,
                        color=ft.Colors.with_opacity(0, ft.Colors.BLACK)
                    )
                ),
                ft.Container(
                    content=theme_button,
                    top=10,
                    right=10
                )
            ],
            expand=False,
        )
    )

    refresh_ui()

# --- EJECUTAR APLICACIÓN ---
ft.app(target=main, assets_dir="assets")