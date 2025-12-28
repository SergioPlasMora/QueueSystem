# QueueSystem - Sistema de Colas de Alto Rendimiento

Proyecto de aprendizaje para entender sistemas de colas con prioridades, workers paralelos y procesamiento asíncrono.

## Instalación

```bash
pip install -r requirements.txt
```

## Uso

```bash
python app_cli.py
```

## Comandos CLI

- `start` - Iniciar workers
- `stop` - Detener workers
- `add <nombre> [prioridad]` - Añadir tarea (prioridad: 0-3)
- `flood <n>` - Añadir N tareas aleatorias
- `status` - Ver estado de colas
- `quit` - Salir