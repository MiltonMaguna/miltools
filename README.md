# nukeRepo - Setup portable para Nuke

Este repo ya quedo preparado para usarse en distintas computadoras sin rutas fijas.

## 1) Como instalarlo en cada maquina

1. Copia o clona este repo en cualquier ruta local.
2. Asegurate de que el archivo `init.py` en la raiz del repo este dentro de tu `NUKE_PATH` o dentro de tu carpeta `.nuke`.
3. Nuke va a resolver automaticamente la ruta relativa a `nuke_repo`.

## 2) Activar y desactivar tools facilmente

Edita `nuke_repo/config.json`.

- En `paths` prendes/apagas bloques de rutas (`gizmos`, `scripts`, `toolsets`, `plugins`, etc.).
- En `menu` prendes/apagas modulos de menu (`shortcuts`, `callbacks`, `pimba_tools`, etc.).
- En `extra_plugin_paths` puedes agregar rutas extra (relativas a `nuke_tools` o absolutas).

Ejemplo:

```json
{
  "paths": {
    "scripts_stamps": false,
    "cattery_vitmatte": false
  },
  "menu": {
    "nuke_grab": false
  },
  "extra_plugin_paths": [
    "scripts/custom_projects"
  ]
}
```

## 3) Config por computadora (sin tocar el repo)

Puedes usar una config diferente por equipo con variable de entorno:

- Variable: `NUKE_REPO_CONFIG`
- Valor: ruta absoluta a un JSON de config

Ejemplo en Windows (PowerShell):

```powershell
$env:NUKE_REPO_CONFIG = "D:\\nuke-configs\\workstationA.json"
```

Asi mantienes un solo repo compartido y cada maquina con su propio perfil de tools.

## 4) Que cambio en el codigo

- `init.py` (raiz): elimina ruta hardcodeada y usa ruta relativa.
- `nuke_repo/init.py`: carga paths condicionalmente desde `config.json`.
- `nuke_repo/menu.py`: importa modulos de forma segura y con toggles.
- `nuke_repo/repo_config.py`: helper de lectura/merge de configuracion.

## 5) Como agregar una tool nueva

Ejemplo: quieres agregar una tool en `./scripts/hotbox`.

1. Crea la carpeta dentro del repo:
   - `nuke_repo/nuke_tools/scripts/hotbox`
2. Copia ahi tu tool (archivos `.py`, `menu.py`, iconos, etc.).
3. Agrega la ruta en `nuke_repo/config.json` dentro de `extra_plugin_paths`:

```json
{
  "extra_plugin_paths": [
    "scripts/hotbox"
  ]
}
```

4. Reinicia Nuke.

Para deshabilitarla, elimina `scripts/hotbox` de `extra_plugin_paths`.

### Opcion con toggle dedicado (true/false)

Si prefieres activar/desactivar desde un switch en `paths`:

1. En `nuke_repo/config.json`, agrega:

```json
{
  "paths": {
    "scripts_hotbox": true
  }
}
```

2. En `nuke_repo/init.py`, agrega una linea de carga:

```python
add_plugin_path("scripts/hotbox", "scripts_hotbox", "hotbox")
```

Asi luego solo cambias `true/false` para habilitar o deshabilitar.

### Nota importante

Agregar un path no siempre crea menu automaticamente. Si la tool necesita inicializacion, debe incluir su `menu.py`/`init.py` o el modulo de arranque correspondiente.
