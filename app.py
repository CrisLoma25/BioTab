import flet as ft
from pyairtable.formulas import match
from nube import Usuario  
from nube import Bioenergia
import main as mn

# --- Pantalla de Registro ---

def registro_main(page: ft.Page):
    page.title = "Registro de Usuario - BioTab"
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 20
    page.spacing = 15
    page.theme_mode = ft.ThemeMode.LIGHT

    COLOR_PRIMARIO = "#2E7D32"
    COLOR_BORDE = "#C8E6C9"

    def show_message(text, color=ft.Colors.GREEN):
        snackbar = ft.SnackBar(content=None, bgcolor=color, show_close_icon=True)
        snackbar.content = ft.Text(text, color=ft.Colors.WHITE)
        page.open(snackbar)

    def set_borde_normal(control):
        control.border_color = COLOR_BORDE
        control.focused_border_color = COLOR_PRIMARIO

    def clear_error(field):
        if field.error_text:
            field.error_text = ""
            set_borde_normal(field)
            page.update()

    def build_header():
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        tooltip="Regresar al menú principal",
                        on_click=go_back,
                        icon_color=COLOR_PRIMARIO,
                        icon_size=30,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10),
                            padding=10
                        )
                    ),
                    ft.Text(
                        "Registrar nuevo usuario",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color=COLOR_PRIMARIO,
                        font_family="Roboto"
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            ),
            padding=ft.padding.only(bottom=15),
            border=ft.border.only(bottom=ft.border.BorderSide(2, COLOR_BORDE))
        )

    def validate_register(e):
        error = False
        for f, msg in [
            (nombre_field, "Ingrese su primer nombre"),
            (apellido_p_field, "Ingrese su apellido paterno"),
            (apellido_m_field, "Ingrese su apellido materno"),
            (usuario_reg_field, "Ingrese un usuario")
        ]:
            if not f.value or not f.value.strip():
                f.error_text = msg
                f.border_color = ft.Colors.RED_600
                f.focused_border_color = ft.Colors.RED_600
                error = True
            else:
                f.error_text = ""
                set_borde_normal(f)

        if not password_reg_field.value or len(password_reg_field.value) < 8:
            password_reg_field.error_text = "La contraseña debe tener mínimo 8 caracteres"
            password_reg_field.border_color = ft.Colors.RED_600
            password_reg_field.focused_border_color = ft.Colors.RED_600
            error = True
        else:
            password_reg_field.error_text = ""
            set_borde_normal(password_reg_field)

        if password_reg_field.value != confirmar_password_field.value:
            confirmar_password_field.error_text = "Las contraseñas no coinciden"
            confirmar_password_field.border_color = ft.Colors.RED_600
            confirmar_password_field.focused_border_color = ft.Colors.RED_600
            error = True
        else:
            confirmar_password_field.error_text = ""
            set_borde_normal(confirmar_password_field)

        page.update()

        if error:
            show_message("Corrija los errores para continuar.", ft.Colors.RED)
            return

        try:
            usuarios_existentes = list(Usuario.all(formula=match({"usuario": usuario_reg_field.value.strip()})))
            if usuarios_existentes:
                show_message("Usuario ya registrado.", ft.Colors.ORANGE)
                return

            nuevo_usuario = Usuario(
                nombre=nombre_field.value.strip(),
                apellidopaterno=apellido_p_field.value.strip(),
                apellidomaterno=apellido_m_field.value.strip(),
                usuario=usuario_reg_field.value.strip(),
                contra=password_reg_field.value,
                admin=admin_checkbox.value or False,
            )
            nuevo_usuario.save()

            show_message(f"Usuario '{usuario_reg_field.value.strip()}' registrado correctamente.", ft.Colors.GREEN)

            nombre_field.value = ""
            apellido_p_field.value = ""
            apellido_m_field.value = ""
            usuario_reg_field.value = ""
            password_reg_field.value = ""
            confirmar_password_field.value = ""
            admin_checkbox.value = False
            page.update()

        except Exception as error:
            show_message(f"Error al registrar usuario: {repr(error)}", ft.Colors.RED)

    def go_back(e):
        page.clean()
        usuario_main(page)

    nombre_field = ft.TextField(label="Primer nombre", width=350, border_radius=8, on_change=lambda e: clear_error(nombre_field))
    apellido_p_field = ft.TextField(label="Apellido paterno", width=350, border_radius=8, on_change=lambda e: clear_error(apellido_p_field))
    apellido_m_field = ft.TextField(label="Apellido materno", width=350, border_radius=8, on_change=lambda e: clear_error(apellido_m_field))
    usuario_reg_field = ft.TextField(label="Usuario", hint_text="ejemplo@email.com", width=350, border_radius=8, on_change=lambda e: clear_error(usuario_reg_field))
    password_reg_field = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, hint_text="Mínimo 8 caracteres", width=350, border_radius=8, on_change=lambda e: clear_error(password_reg_field))
    confirmar_password_field = ft.TextField(label="Confirmar contraseña", password=True, can_reveal_password=True, width=350, border_radius=8, on_change=lambda e: clear_error(confirmar_password_field))
    admin_checkbox = ft.Checkbox(label="¿Es administrador?")

    register_button = ft.ElevatedButton(
        text="Registrar",
        icon=ft.Icons.PERSON_ADD,
        width=370,
        height=50,
        style=ft.ButtonStyle(
            bgcolor=COLOR_PRIMARIO,
            color=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=20,
        ),
        on_click=validate_register
    )

    page.clean()
    page.add(
        ft.Column(
            [
                build_header(),
                ft.Container(
                    content=ft.Card(
                        content=ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("Completa el formulario para crear una cuenta",
                                            size=16, color=ft.Colors.GREY_700, weight=ft.FontWeight.BOLD),
                                    nombre_field,
                                    apellido_p_field,
                                    apellido_m_field,
                                    usuario_reg_field,
                                    password_reg_field,
                                    confirmar_password_field,
                                    ft.Row(
                                        controls=[admin_checkbox],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                    ),
                                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                                    register_button,
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=15,
                            ),
                            padding=20,
                            border_radius=10,
                        ),
                        elevation=5,
                        color=ft.Colors.WHITE,
                    ),
                    expand=False,
                ),
            ],
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

# --- Pantalla de Registro Bioenergía ---

def registrar_biomasa(page: ft.Page):
    page.title = "Registro de Biomasa - BioTab"
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 20
    page.spacing = 15
    page.theme_mode = ft.ThemeMode.LIGHT

    COLOR_PRIMARIO = "#2E7D32"
    COLOR_BORDE = "#C8E6C9"

    errores = {
        "cultivo": False, "parte": False, "cantidad": False,
        "humedad": False, "area": False, "municipio": False, "coordenadas": False
    }

    def build_header():
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        tooltip="Regresar al menú principal",
                        on_click=go_back,
                        icon_color=COLOR_PRIMARIO,
                        icon_size=30,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10),
                            padding=10
                        )
                    ),
                    ft.Text(
                        "Registro de Biomasa",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color=COLOR_PRIMARIO,
                        font_family="Roboto"
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            ),
            padding=ft.padding.only(bottom=15),
            border=ft.border.only(bottom=ft.border.BorderSide(2, COLOR_BORDE))
        )

    def show_message(text, color=ft.Colors.GREEN):
        snackbar = ft.SnackBar(content=None, bgcolor=color, show_close_icon=True)
        snackbar.content = ft.Text(text, color=ft.Colors.WHITE)
        page.open(snackbar)

    def set_borde_normal(control):
        control.border_color = COLOR_BORDE
        control.focused_border_color = COLOR_PRIMARIO

    # Campos
    cultivo = ft.TextField(label="Cultivo de origen", width=350)
    parte = ft.Dropdown(
        label="Parte aprovechada",
        options=[ft.dropdown.Option(op) for op in ["Hoja", "Tallo", "Cáscara", "Bagazo", "Rastrojo"]],
        width=350
    )
    cantidad = ft.TextField(label="Cantidad (piezas)", keyboard_type=ft.KeyboardType.NUMBER, width=350)
    humedad = ft.TextField(label="Porcentaje de humedad (%)", keyboard_type=ft.KeyboardType.NUMBER, width=350)
    area = ft.TextField(label="Área cultivada (hectáreas)", keyboard_type=ft.KeyboardType.NUMBER, width=350)
    municipio = ft.Dropdown(
        label="Municipio",
        options=[ft.dropdown.Option(m) for m in [
            "Balancán", "Cárdenas", "Centla", "Centro", "Comalcalco",
            "Cunduacán", "Emiliano Zapata", "Huimanguillo", "Jalapa",
            "Jalpa de Méndez", "Jonuta", "Macuspana", "Nacajuca",
            "Paraíso", "Tacotalpa", "Teapa", "Tenosique"
        ]],
        width=350
    )
    latitud = ft.TextField(label="Latitud (°)", keyboard_type=ft.KeyboardType.NUMBER, width=170)
    longitud = ft.TextField(label="Longitud (°)", keyboard_type=ft.KeyboardType.NUMBER, width=170)

    def validar_campo(campo_key, control):
        def on_change(e):
            if control.value and (campo_key != "coordenadas" or (latitud.value and longitud.value)):
                errores[campo_key] = False
                set_borde_normal(control)
                page.update()
        return on_change

    cultivo.on_change = validar_campo("cultivo", cultivo)
    parte.on_change = validar_campo("parte", parte)
    cantidad.on_change = validar_campo("cantidad", cantidad)
    humedad.on_change = validar_campo("humedad", humedad)
    area.on_change = validar_campo("area", area)
    municipio.on_change = validar_campo("municipio", municipio)
    latitud.on_change = validar_campo("coordenadas", latitud)
    longitud.on_change = validar_campo("coordenadas", longitud)

    def guardar_biomasa(e):
        hay_error = False

        def validar(campo, control):
            nonlocal hay_error
            if not control.value:
                errores[campo] = True
                control.border_color = ft.Colors.RED_600
                control.focused_border_color = ft.Colors.RED_600
                hay_error = True
            else:
                errores[campo] = False
                set_borde_normal(control)

        validar("cultivo", cultivo)
        validar("parte", parte)
        validar("cantidad", cantidad)
        validar("humedad", humedad)
        validar("area", area)
        validar("municipio", municipio)

        if not latitud.value or not longitud.value:
            errores["coordenadas"] = True
            latitud.border_color = ft.Colors.RED_600
            longitud.border_color = ft.Colors.RED_600
            hay_error = True
        else:
            errores["coordenadas"] = False
            set_borde_normal(latitud)
            set_borde_normal(longitud)

        page.update()

        if hay_error:
            show_message("Faltan campos por completar", ft.Colors.RED_600)
            return

        try:
            nuevo_registro = Bioenergia(
                cultivo=cultivo.value.strip(),
                parte=parte.value,
                cantidad=float(cantidad.value),
                humedad=float(humedad.value),
                area=float(area.value),
                municipio=municipio.value,
                latitud=float(latitud.value),
                longitud=float(longitud.value)
            )
            nuevo_registro.save()
            show_message("¡Registro guardado exitosamente!", ft.Colors.GREEN_600)

            cultivo.value = parte.value = municipio.value = ""
            cantidad.value = humedad.value = area.value = ""
            latitud.value = longitud.value = ""
            page.update()
        except Exception as ex:
            show_message(f"Error: {ex}", ft.Colors.RED_600)

    def go_back(e):
        page.clean()
        usuario_main(page)

    form_inputs = ft.Column([
        ft.Text("Complete todos los campos para registrar la biomasa",
                size=16, color=ft.Colors.GREY_700, weight=ft.FontWeight.BOLD),
        cultivo, parte, cantidad, humedad, area, municipio,
        ft.Row([latitud, longitud], spacing=20, alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
        ft.ElevatedButton(
            text="GUARDAR REGISTRO",
            icon=ft.Icons.SAVE,
            width=370,
            height=50,
            style=ft.ButtonStyle(
                bgcolor=COLOR_PRIMARIO,
                color=ft.Colors.WHITE,
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=20
            ),
            on_click=guardar_biomasa
        )
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15)

    page.clean()
    page.add(
        ft.Column(
            [
                build_header(),
                ft.Container(
                    content=ft.Card(
                        content=ft.Container(
                            content=form_inputs,
                            padding=20,
                            border_radius=10
                        ),
                        elevation=5,
                        color=ft.Colors.WHITE
                    ),
                    expand=False
                )
            ],
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

# --- Pantalla de consulta de usuarios ---

def consultar_usuarios(page: ft.Page):
    page.title = "Consultar Usuarios - BioTab"
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 20
    page.spacing = 15
    page.theme_mode = ft.ThemeMode.LIGHT

    COLOR_PRIMARIO = "#2E7D32"
    COLOR_SECUNDARIO = "#66BB6A"
    COLOR_TEXTO = ft.Colors.BLACK
    COLOR_FONDO_ENCABEZADO = "#E8F5E9"
    COLOR_BORDE = "#C8E6C9"
    COLOR_HOVER = "#F1F8E9"

    filtro_actual = ""

    def build_header():
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        tooltip="Regresar al menú principal",
                        on_click=go_back,
                        icon_color=COLOR_PRIMARIO,
                        icon_size=30,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10),
                            padding=10
                        )
                    ),
                    ft.Text(
                        "Consulta de Usuarios",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color=COLOR_PRIMARIO,
                        font_family="Roboto"
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            ),
            padding=ft.padding.only(bottom=15),
            border=ft.border.only(bottom=ft.border.BorderSide(2, COLOR_BORDE))
        )

    search_field = ft.TextField(
        label="Buscar usuario...",
        hint_text="Puedes buscar usuario por nombre",
        width=600,
        height=50,
        border_radius=10,
        border_color=COLOR_BORDE,
        focused_border_color=COLOR_PRIMARIO,
        autofocus=True,
        suffix_icon=ft.Icons.SEARCH,
        text_size=14,
        on_change=lambda e: on_search_change(),
        content_padding=15,
        filled=True,
        fill_color=ft.Colors.WHITE,
        cursor_color=COLOR_PRIMARIO,
        label_style=ft.TextStyle(color=COLOR_PRIMARIO),
        hint_style=ft.TextStyle(color=ft.Colors.GREY_600)
    )

    encabezado = [
        ft.DataColumn(ft.Text("Nombre", weight=ft.FontWeight.BOLD, color=COLOR_TEXTO)),
        ft.DataColumn(ft.Text("Apellido Paterno", weight=ft.FontWeight.BOLD, color=COLOR_TEXTO)),
        ft.DataColumn(ft.Text("Apellido Materno", weight=ft.FontWeight.BOLD, color=COLOR_TEXTO)),
        ft.DataColumn(ft.Text("Usuario", weight=ft.FontWeight.BOLD, color=COLOR_TEXTO)),
        ft.DataColumn(ft.Text("Contraseña", weight=ft.FontWeight.BOLD, color=COLOR_TEXTO)),
        ft.DataColumn(ft.Text("Admin", weight=ft.FontWeight.BOLD, color=COLOR_TEXTO)),
    ]

    tabla = ft.DataTable(
        columns=encabezado,
        rows=[],
        column_spacing=25,
        heading_row_color=COLOR_FONDO_ENCABEZADO,
        heading_row_height=50,
        heading_text_style=ft.TextStyle(
            color=COLOR_PRIMARIO,
            weight=ft.FontWeight.BOLD,
            font_family="Roboto"
        ),
        data_row_color={
            "": ft.Colors.WHITE,
            "hovered": COLOR_HOVER
        },
        border=ft.border.all(1, COLOR_BORDE),
        horizontal_lines=ft.border.BorderSide(1, COLOR_BORDE),
        vertical_lines=ft.border.BorderSide(1, COLOR_BORDE),
        expand=True,
        divider_thickness=1,
        show_checkbox_column=False,
    )

    def cargar_tabla(filtro=""):
        # Limpiar filas antes de cargar
        tabla.rows.clear()

        try:
            usuarios = list(Usuario.all())

            # Filtro parcial, respetando mayúsculas/minúsculas
            if filtro:
                filtro = filtro.strip()
                usuarios = [
                    u for u in usuarios if filtro in (u.nombre or "")
                ]

            # Evitar duplicados exactos por nombre
            usuarios_unicos = []
            nombres_vistos = set()
            for u in usuarios:
                if u.nombre not in nombres_vistos:
                    usuarios_unicos.append(u)
                    nombres_vistos.add(u.nombre)

            # Si no hay resultados
            if not usuarios_unicos:
                tabla.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(
                                ft.Text(
                                    "Usuario por nombre no encontrado",
                                    color="red",
                                    italic=True
                                )
                            )
                        ] + [ft.DataCell(ft.Text("")) for _ in range(5)],
                        color=ft.Colors.WHITE
                    )
                )
            else:
                for u in usuarios_unicos:
                    fila = ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(u.nombre, color=COLOR_TEXTO)),
                            ft.DataCell(ft.Text(u.apellidopaterno or "-", color=COLOR_TEXTO)),
                            ft.DataCell(ft.Text(u.apellidomaterno or "-", color=COLOR_TEXTO)),
                            ft.DataCell(ft.Text(u.usuario, color=COLOR_TEXTO)),
                            ft.DataCell(ft.Text("••••••••", color=COLOR_TEXTO)),
                            ft.DataCell(
                                ft.Icon(
                                    ft.Icons.CHECK_CIRCLE if u.admin else ft.Icons.CANCEL,
                                    color=COLOR_PRIMARIO if u.admin else ft.Colors.RED_700,
                                    tooltip="Administrador" if u.admin else "Usuario normal",
                                    size=20
                                )
                            ),
                        ],
                        on_select_changed=lambda e, fila_id=u.usuario: resaltar_fila_hover(e, fila_id),
                        color=ft.Colors.WHITE
                    )
                    tabla.rows.append(fila)

            page.update()

        except Exception as e:
            mostrar_error(f"Error al cargar usuarios: {e}")


    def resaltar_fila_hover(e, fila_id):
        if e.data == "true":
            e.control.color = ft.Colors.LIGHT_GREEN_100
        else:
            e.control.color = ft.Colors.WHITE
        e.control.update()


    def on_search_change():
        nonlocal filtro_actual
        filtro_actual = search_field.value.strip()
        cargar_tabla(filtro_actual)

    def mostrar_error(mensaje):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(mensaje, color=ft.Colors.WHITE),
            bgcolor=ft.Colors.RED_700,
            behavior=ft.SnackBarBehavior.FLOATING,
            elevation=10,
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=15
        )
        page.snack_bar.open = True
        page.update()

    def go_back(e):
        page.clean()
        usuario_main(page)  

    page.clean()
    page.add(
        ft.Column(
            [
                build_header(),
                ft.Container(
                    content=search_field,
                    padding=ft.padding.symmetric(vertical=20),
                ),
                ft.Container(
                    content=ft.Card(
                        content=ft.Container(
                            content=tabla,
                            padding=10,
                            border_radius=10
                        ),
                        elevation=5,
                        color=ft.Colors.WHITE
                    ),
                    expand=True
                )
            ],
            expand=True,
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

    cargar_tabla()

# --- Pantalla de Consulta Biomasa ---  

def consultar_biomasa(page: ft.Page):
    page.title = "Consulta de Biomasa - BioTab"
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 20
    page.spacing = 15
    page.theme_mode = ft.ThemeMode.LIGHT

    COLOR_PRIMARIO = "#2E7D32"
    COLOR_TEXTO = ft.Colors.BLACK
    COLOR_FONDO_ENCABEZADO = "#E0F2F1"
    COLOR_BORDE = "#B2DFDB"
    COLOR_HOVER = "#E0F7FA"

    filtro_actual = ""

    colores_municipio = {
        # Rojo
        "Centro": "#D32F2F",
        "Jalpa de Méndez": "#D32F2F",
        "Nacajuca": "#D32F2F",
        # Amarillo
        "Cárdenas": "#FBC02D",
        "Comalcalco": "#FBC02D",
        "Cunduacán": "#FBC02D",
        "Huimanguillo": "#FBC02D",
        "Paraíso": "#FBC02D",
        # Verde
        "Jalapa": "#2E7D32",
        "Tacotalpa": "#2E7D32",
        "Teapa": "#2E7D32",
        # Turquesa
        "Balancán": "#26A69A",
        "Emiliano Zapata": "#26A69A",
        "Tenosique": "#26A69A",
        "Macuspana": "#26A69A",
        "Centla": "#26A69A",
        "Jonuta": "#26A69A",
    }

    def build_header():
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        tooltip="Regresar al menú principal",
                        on_click=go_back,
                        icon_color=COLOR_PRIMARIO,
                        icon_size=30,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10),
                            padding=10
                        )
                    ),
                    ft.Text(
                        "Consulta de Biomasa",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color=COLOR_PRIMARIO,
                        font_family="Roboto"
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            ),
            padding=ft.padding.only(bottom=15),
            border=ft.border.only(bottom=ft.border.BorderSide(2, COLOR_BORDE))
        )

    search_field = ft.TextField(
        label="Buscar por cultivo...",
        hint_text="Escribe para filtrar por cultivo",
        width=600,
        height=50,
        border_radius=10,
        border_color=COLOR_BORDE,
        focused_border_color=COLOR_PRIMARIO,
        autofocus=True,
        suffix_icon=ft.Icons.SEARCH,
        text_size=14,
        on_change=lambda e: on_search_change(),
        content_padding=15,
        filled=True,
        fill_color=ft.Colors.WHITE,
        cursor_color=COLOR_PRIMARIO,
        label_style=ft.TextStyle(color=COLOR_PRIMARIO),
        hint_style=ft.TextStyle(color=ft.Colors.GREY_600)
    )

    encabezado = [
        ft.DataColumn(ft.Text("Cultivo", weight=ft.FontWeight.BOLD, color=COLOR_TEXTO)),
        ft.DataColumn(ft.Text("Parte aprovechada", weight=ft.FontWeight.BOLD, color=COLOR_TEXTO)),
        ft.DataColumn(ft.Text("Cantidad recojida (piezas)", weight=ft.FontWeight.BOLD, color=COLOR_TEXTO)),
        ft.DataColumn(ft.Text("Humedad del suelo (%)", weight=ft.FontWeight.BOLD, color=COLOR_TEXTO)),
        ft.DataColumn(ft.Text("Área sembrada (hectáreas)", weight=ft.FontWeight.BOLD, color=COLOR_TEXTO)),
        ft.DataColumn(ft.Text("Municipio", weight=ft.FontWeight.BOLD, color=COLOR_TEXTO)),
        ft.DataColumn(ft.Text("Latitud", weight=ft.FontWeight.BOLD, color=COLOR_TEXTO)),
        ft.DataColumn(ft.Text("Longitud", weight=ft.FontWeight.BOLD, color=COLOR_TEXTO)),
    ]

    tabla = ft.DataTable(
        columns=encabezado,
        rows=[],
        column_spacing=25,
        heading_row_color=COLOR_FONDO_ENCABEZADO,
        heading_row_height=50,
        heading_text_style=ft.TextStyle(
            color=COLOR_PRIMARIO,
            weight=ft.FontWeight.BOLD,
            font_family="Roboto"
        ),
        data_row_color={
            "": ft.Colors.WHITE,
            "hovered": COLOR_HOVER
        },
        border=ft.border.all(1, COLOR_BORDE),
        horizontal_lines=ft.border.BorderSide(1, COLOR_BORDE),
        vertical_lines=ft.border.BorderSide(1, COLOR_BORDE),
        expand=True,
        divider_thickness=1,
        show_checkbox_column=False,
    )

    def cargar_tabla(filtro=""):
        tabla.rows.clear()
        try:
            registros = list(Bioenergia.all())  

            if filtro:
                filtro_lower = filtro.strip().lower()
                registros = [r for r in registros if filtro_lower in (r.cultivo or "").lower()]

            if not registros:
                tabla.rows.append(
                    ft.DataRow(
                        cells=[ft.DataCell(
                            ft.Text("No se encontraron registros", color="red", italic=True)
                        )] + [ft.DataCell(ft.Text("")) for _ in range(len(encabezado)-1)],
                        color=ft.Colors.WHITE
                    )
                )
            else:
                for r in registros:
                    color_mun = colores_municipio.get(r.municipio, ft.Colors.BLACK)
                    fila = ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(r.cultivo or "-", color=COLOR_TEXTO)),
                            ft.DataCell(ft.Text(r.parte or "-", color=COLOR_TEXTO)),
                            ft.DataCell(ft.Text(str(r.cantidad), color=COLOR_TEXTO)),
                            ft.DataCell(ft.Text(str(r.humedad), color=COLOR_TEXTO)),
                            ft.DataCell(ft.Text(str(r.area), color=COLOR_TEXTO)),
                            ft.DataCell(ft.Text(r.municipio or "-", color=color_mun, weight=ft.FontWeight.BOLD)),
                            ft.DataCell(ft.Text(str(r.latitud), color=COLOR_TEXTO)),
                            ft.DataCell(ft.Text(str(r.longitud), color=COLOR_TEXTO)),
                        ],
                        color=ft.Colors.WHITE
                    )
                    tabla.rows.append(fila)

            page.update()
        except Exception as e:
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Error al cargar registros: {e}", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.RED_700,
                behavior=ft.SnackBarBehavior.FLOATING,
                elevation=10,
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=15
            )
            page.snack_bar.open = True
            page.update()

    def on_search_change():
        nonlocal filtro_actual
        filtro_actual = search_field.value
        cargar_tabla(filtro_actual)

    def go_back(e):
        page.clean()
        usuario_main(page) 

    page.clean()
    page.add(
        ft.Column([
            build_header(),
            ft.Container(
                content=search_field,
                padding=ft.padding.symmetric(vertical=20)
            ),
            ft.Container(
                content=ft.Card(
                    content=ft.Container(
                        content=tabla,
                        padding=10,
                        border_radius=10
                    ),
                    elevation=5,
                    color=ft.Colors.WHITE
                ),
                expand=True
            ),
        ],
        spacing=0,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True)
    )

    cargar_tabla()

# --- Pantalla de Usuario Principal ---

def usuario_main(page: ft.Page):
    COLOR_PRIMARIO = "#2E7D32"
    COLOR_BLANCO = "#FFFFFF"

    page.title = "BioTab - Gestión de Bioenergías"
    page.bgcolor = "#f5f5f5"
    page.padding = 0
    page.fonts = {
        "Roboto": "https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap",
        "Montserrat": "https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap"
    }
    page.theme = ft.Theme(
        font_family="Roboto",
        color_scheme=ft.ColorScheme(
            primary=COLOR_PRIMARIO,
            primary_container="#388E3C",
            secondary="#FFC107",
            secondary_container="#FFD54F",
            surface="#FFFFFF",
            background="#F5F5F5"
        )
    )

    def abrir_registro(e):
        page.clean()
        registro_main(page)

    colors = {
        "primary": COLOR_PRIMARIO,
        "primary_light": "#4CAF50",
        "primary_dark": "#1B5E20",
        "secondary": "#FFC107",
        "background": "#F5F5F5",
        "text_primary": "#212121",
        "text_secondary": "#757575",
        "white": COLOR_BLANCO
    }

    background = ft.Stack(
        [
            ft.Image(
                src="https://images.unsplash.com/photo-1508514177221-188b1cf16e9d?q=80&w=2072&auto=format&fit=crop",
                width=page.width,
                height=page.height,
                fit=ft.ImageFit.COVER,
                opacity=0.7
            ),
            ft.Container(
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_center,
                    end=ft.alignment.bottom_center,
                    colors=["#00000060", "#00000090"]
                ),
                width=page.width,
                height=page.height
            )
        ]
    )

    def on_resize(e):
        background.controls[0].width = page.width
        background.controls[0].height = page.height
        background.controls[1].width = page.width
        background.controls[1].height = page.height
        background.update()

    page.on_resize = on_resize

    header = ft.Container(
        content=ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.BOLT, size=30, color=COLOR_BLANCO),
                        ft.Icon(ft.Icons.ECO, size=30, color=COLOR_BLANCO),
                        ft.Icon(ft.Icons.BATTERY_FULL, size=30, color=COLOR_BLANCO),
                        ft.Text("BioTab",
                               size=24,
                               weight=ft.FontWeight.BOLD,
                               color=COLOR_BLANCO),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=10,
                    expand=True
                ),
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(text="Cerrar sesión", icon=ft.Icons.LOGOUT),
                    ],
                    icon=ft.Icons.MENU,
                    icon_color=COLOR_BLANCO,
                    tooltip="Menú de administrador",
                    on_select=lambda e: mn.main(page)
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        ),
        bgcolor=COLOR_PRIMARIO,
        height=70,
        padding=ft.padding.symmetric(horizontal=20),
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color=ft.Colors.BLACK12)
    )

    welcome_card = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("Bienvenido, ", size=24, weight="bold", color=colors["white"]),
                        ft.Text("a BioTab", size=24, weight="bold", color=colors["secondary"]),
                    ],
                    spacing=5
                ),
                ft.Divider(height=10, color="transparent"),
                ft.Text(
                    "Control total en la gestión de bioenergías de Tabasco",
                    size=18,
                    color=colors["white"]
                ),
                ft.Divider(height=20, color="transparent"),
                ft.Text(
                    "BioTab es un sistema digital diseñado para centralizar y simplificar la administración de proyectos y recursos de bioenergía en Tabasco. A través de una interfaz intuitiva, permite registrar, consultar y gestionar información clave, fomentando la transparencia, la eficiencia y el uso responsable de la energía renovable.",
                    size=16,
                    color=colors["white"]
                ),
                ft.Divider(height=20, color="transparent"),
                ft.Container(
                    content=ft.Text(
                        '"Gestionando hoy la energía del mañana."',
                        size=16,
                        italic=True,
                        color=colors["secondary"]
                    ),
                    padding=ft.padding.symmetric(horizontal=20, vertical=10),
                    border=ft.border.all(1, colors["secondary"]),
                    border_radius=20
                )
            ],
            spacing=5
        ),
        padding=30,
        width=min(page.width * 0.85, 800),
        bgcolor="#00000080",
        border_radius=15,
        margin=ft.margin.symmetric(vertical=10),
        alignment=ft.alignment.center
    )

    features = [
        {
            "title": "Inicio de sesión",
            "icon": ft.Icons.LOGIN,
            "description": "Acceso seguro para usuarios autorizados",
            "color": "#2E7D32",
            "action": lambda e: mn.main(page)
        },
        {
            "title": "Registro de usuario",
            "icon": ft.Icons.PERSON_ADD_ALT_1,
            "description": "Alta de cuentas con roles definidos",
            "color": "#388E3C",
            "action": lambda e: abrir_registro(page)
        },
        {
            "title": "Agregar bioenergía",
            "icon": ft.Icons.ADD_BUSINESS,
            "description": "Registro completo de proyectos",
            "color": "#43A047",
            "action":lambda e: registrar_biomasa(page)
        },
        {
            "title": "Consultar usuarios",
            "icon": ft.Icons.PEOPLE_ALT,
            "description": "Lista y datos detallados de usuarios",
            "color": "#4CAF50",
            "action":lambda e: consultar_usuarios(page)
        },
        {
            "title": "Consultar bioenergías",
            "icon": ft.Icons.ENERGY_SAVINGS_LEAF,
            "description": "Listado filtrado de bioenergías",
            "color": "#66BB6A",
            "action":lambda e: consultar_biomasa(page)
        }
    ]

    def hover_animation(e):
        if e.data == "true":
            e.control.bgcolor = f"{e.control.bgcolor[:-2]}FF"
            e.control.scale = ft.Scale(scale=1.03)
        else:
            e.control.bgcolor = f"{e.control.bgcolor[:-2]}CC"
            e.control.scale = ft.Scale(scale=1.0)
        e.control.update()

    features_grid = ft.GridView(
        runs_count=5,
        max_extent=200,
        child_aspect_ratio=1,
        spacing=15,
        run_spacing=15,
        padding=20,
        expand=True
    )

    for feature in features:
        action = feature.get("action", lambda e, t=feature["title"]: print(f"Botón '{t}' presionado"))
        features_grid.controls.append(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(feature["icon"], size=36, color=colors["white"]),
                        ft.ElevatedButton(
                            text=feature["title"],
                            style=ft.ButtonStyle(
                                bgcolor=ft.Colors.TRANSPARENT,
                                color=colors["white"],
                                overlay_color=colors["primary_light"],
                                shape=ft.RoundedRectangleBorder(radius=8)
                            ),
                            on_click=action,
                            expand=False
                        ),
                        ft.Divider(height=5, color="transparent"),
                        ft.Text(
                            feature["description"],
                            size=12,
                            text_align="center",
                            color=colors["white"],
                            weight="w400"
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                    alignment=ft.MainAxisAlignment.CENTER,
                    expand=True
                ),
                padding=20,
                alignment=ft.alignment.center,
                bgcolor=f"{feature['color']}CC",
                border_radius=12,
                animate=ft.Animation(300, "easeInOut"),
                animate_scale=ft.Animation(300, "easeInOut"),
                on_hover=hover_animation,
            )
        )

    main_content = ft.Column(
        [
            welcome_card,
            features_grid
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10
    )

    footer = ft.Container(
        content=ft.Row(
            [
                ft.Text("© 2025 BioTab - UJAT", color=colors["white"], size=12),
                ft.Text("Versión 1.0.0", color=colors["white"], size=12)
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=15,
        bgcolor="#00000040",
        border_radius=ft.border_radius.only(top_left=10, top_right=10)
    )

    page.add(
        ft.Stack(
            [
                background,
                ft.Column(
                    [
                        header,
                        ft.Container(
                            content=main_content,
                            expand=True,
                            padding=ft.padding.symmetric(horizontal=20)
                        ),
                        footer
                    ],
                    spacing=0,
                    expand=True
                )
            ],
            expand=True
        )
    )

if __name__ == "__main__":
    ft.app(target=mn.main,view=ft.AppView.WEB_BROWSER)
