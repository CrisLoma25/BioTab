import flet as ft
from pyairtable.formulas import match
from nube import Usuario  
import app as ap

def main(page: ft.Page):
    page.title = "Sistema Bioenergía"
    page.padding = 0
    page.spacing = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 1000
    page.window_height = 600
    page.window_resizable = True

    def show_message(text, color=ft.Colors.GREEN):
        snackbar = ft.SnackBar(content=None, bgcolor=color, show_close_icon=True)
        snackbar.content = ft.Text(text, color=ft.Colors.WHITE)
        page.open(snackbar)

    def clear_error(field):
        if field.error_text:
            field.error_text = ""
            page.update()

    def validate_register(e):
        error = False
        # Validación de campos requeridos
        for f, msg in [
            (nombre_field, "Ingrese su primer nombre"),
            (apellido_p_field, "Ingrese su apellido paterno"),
            (apellido_m_field, "Ingrese su apellido materno"),
            (usuario_reg_field, "Ingrese un usuario")
        ]:
            if not f.value or not f.value.strip():
                f.error_text = msg
                error = True
            else:
                f.error_text = ""

        # Validación de contraseña
        if not password_reg_field.value or len(password_reg_field.value) < 8:
            password_reg_field.error_text = "La contraseña debe tener mínimo 8 caracteres"
            error = True
        else:
            password_reg_field.error_text = ""

        # Validación de confirmación de contraseña
        if password_reg_field.value != confirmar_password_field.value:
            confirmar_password_field.error_text = "Las contraseñas no coinciden"
            error = True
        else:
            confirmar_password_field.error_text = ""

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

            # Limpiar campos
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

    def validate_login(e):
        error = False
        # Validación de campos de login
        for f, msg in [
            (usuario_login_field, "Ingrese su usuario"),
            (password_login_field, "Ingrese su contraseña"),
        ]:
            if not f.value or not f.value.strip():
                f.error_text = msg
                error = True
            else:
                f.error_text = ""

        # Validación de longitud mínima de contraseña de login
        if password_login_field.value and len(password_login_field.value) < 8:
            password_login_field.error_text = "La contraseña debe tener mínimo 8 caracteres"
            error = True

        page.update()

        if error:
            show_message("Corrija los errores para continuar.", ft.Colors.RED)
            return

        try:
            usuarios = list(Usuario.all(formula=match({"usuario": usuario_login_field.value.strip()})))
            if not usuarios:
                show_message("Usuario no encontrado.", ft.Colors.ORANGE)
                return
            usuario_obj = usuarios[0]

            if usuario_obj.contra != password_login_field.value:
                show_message("Contraseña incorrecta.", ft.Colors.ORANGE)
                return

            show_message(f"Bienvenido, {usuario_obj.nombre}!", ft.Colors.GREEN)

            page.clean()
            ap.usuario_main(page)

        except Exception as error:
            show_message(f"Error de Airtable: {repr(error)}", ft.Colors.RED)

    # ---------- Campos del Registro ----------
    nombre_field = ft.TextField(label="Primer nombre", width=300, border_radius=8, on_change=lambda e: clear_error(nombre_field))
    apellido_p_field = ft.TextField(label="Apellido paterno", width=300, border_radius=8, on_change=lambda e: clear_error(apellido_p_field))
    apellido_m_field = ft.TextField(label="Apellido materno", width=300, border_radius=8, on_change=lambda e: clear_error(apellido_m_field))
    usuario_reg_field = ft.TextField(label="Usuario", hint_text="ejemplo@email.com", width=300, border_radius=8, on_change=lambda e: clear_error(usuario_reg_field))
    password_reg_field = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, hint_text="Mínimo 8 caracteres", width=300, border_radius=8, on_change=lambda e: clear_error(password_reg_field))
    confirmar_password_field = ft.TextField(label="Confirmar contraseña", password=True, can_reveal_password=True, width=300, border_radius=8, on_change=lambda e: clear_error(confirmar_password_field))
    admin_checkbox = ft.Checkbox(label="¿Es administrador?")
    register_button = ft.ElevatedButton(text="Registrarme", width=300, height=45, on_click=validate_register)

    # ---------- Campos del Login ----------
    usuario_login_field = ft.TextField(label="Usuario", hint_text="ejemplo@email.com", width=300, border_radius=8, on_change=lambda e: clear_error(usuario_login_field), prefix_icon=ft.Icons.PERSON)
    password_login_field = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, hint_text="Mínimo 8 caracteres", width=300, border_radius=8, on_change=lambda e: clear_error(password_login_field), prefix_icon=ft.Icons.LOCK)
    login_button = ft.ElevatedButton(text="Iniciar sesión", width=300, height=45, on_click=validate_login)

    # ---------- Funciones para cambiar pantallas ----------

    def show_register(e=None):
        page.clean()
        page.add(
            ft.Row(
                controls=[
                    ft.ListView(
                        controls=[
                            ft.Text("Regístrate", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87, text_align=ft.TextAlign.CENTER),
                            ft.Text("Completa el formulario para crear una cuenta", size=14, color=ft.Colors.GREY_600, text_align=ft.TextAlign.CENTER),
                            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                            nombre_field,
                            apellido_p_field,
                            apellido_m_field,
                            usuario_reg_field,
                            password_reg_field,
                            confirmar_password_field,
                            admin_checkbox,
                            ft.Container(height=10),
                            register_button,
                            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                            ft.Row(
                                controls=[
                                    ft.Text("¿Ya tienes cuenta? ", color=ft.Colors.BLACK87),
                                    ft.TextButton("Inicia sesión", on_click=show_login)
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            )
                        ],
                        width=400,
                        padding=40,
                        spacing=10,
                    ),
                    ft.Image(
                        src="https://cdn.pixabay.com/photo/2018/07/09/18/40/nature-3526840_1280.jpg",
                        fit=ft.ImageFit.COVER,
                        expand=True,
                        opacity=0.9,
                    ),
                ],
                expand=True,
                spacing=0,
                vertical_alignment=ft.CrossAxisAlignment.STRETCH,
            )
        )

    def show_login(e=None):
        page.clean()
        page.add(
            ft.Row(
                controls=[
                    ft.Image(
                        src="https://cdn.pixabay.com/photo/2025/06/10/17/53/field-9652617_960_720.jpg",
                        fit=ft.ImageFit.COVER,
                        expand=True,
                        opacity=0.9,
                    ),
                    ft.ListView(
                        controls=[
                            ft.Column(
                                [
                                    ft.Row(
                                        [
                                            ft.Icon(ft.Icons.BOLT, size=60, color="green"),
                                            ft.Icon(ft.Icons.ECO, size=60, color="green"),
                                            ft.Icon(ft.Icons.BATTERY_FULL, size=60, color="green"),
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        spacing=10,
                                    ),
                                    ft.Text(
                                        "BioTab",
                                        size=30,
                                        weight=ft.FontWeight.W_900,
                                        color="green",
                                        font_family="Arial",
                                        text_align=ft.TextAlign.CENTER,
                                    ),
                                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                                    ft.Text(
                                        "Bienvenido de nuevo",
                                        size=24,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.BLACK87,
                                        text_align=ft.TextAlign.CENTER,
                                    ),
                                    ft.Text(
                                        "Inicia sesión para continuar",
                                        size=14,
                                        color=ft.Colors.GREY_600,
                                        text_align=ft.TextAlign.CENTER,
                                    ),
                                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                                    usuario_login_field,
                                    password_login_field,
                                    ft.Container(height=10),
                                    login_button,
                                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                                    ft.Row(
                                        controls=[
                                            ft.Text("¿No tienes cuenta? ", color=ft.Colors.BLACK87),
                                            ft.TextButton("Regístrate aquí", on_click=show_register)
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=10,
                            )
                        ],
                        width=400,
                        padding=40,
                        spacing=10,
                    ),
                ],
                expand=True,
                spacing=0,
                vertical_alignment=ft.CrossAxisAlignment.STRETCH,
            )
        )

    # Pantalla inicial
    show_login()

if __name__ == "__main__":
    ft.app(target=main,view=ft.AppView.WEB_BROWSER)
