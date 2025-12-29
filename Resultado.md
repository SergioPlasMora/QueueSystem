8 workers para dataset
4 workers para comandos

Resultados:

(venv) C:\Users\sergi\OneDrive\Documentos\GitHub\QueueSystem>python app_cli.py
╔══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║ 🚀 QueueSystem - CLI Interactiva                                                                                                                         ║
║ Sistema de Colas de Alto Rendimiento                                                                                                                     ║
╚══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝

╭──────────────────────────────────────────────────────────────────────── ❓ Ayuda ────────────────────────────────────────────────────────────────────────╮
│                                                                                                                                                          │
│ Comandos disponibles:                                                                                                                                    │
│                                                                                                                                                          │
│   start              Iniciar todos los workers                                                                                                           │
│   stop               Detener todos los workers                                                                                                           │
│   add <name>   Añadir tarea (prio: 0=CRITICAL, 1=HIGH, 2=NORMAL, 3=LOW)                                                                                  │
│   cmd <name>   Añadir comando del sistema                                                                                                                │
│   flood <n>          Añadir N tareas aleatorias                                                                                                          │
│   status             Mostrar estado actual                                                                                                               │
│   clear              Limpiar pantalla                                                                                                                    │
│   help               Mostrar esta ayuda                                                                                                                  │
│   quit               Salir de la aplicación                                                                                                              │
│                                                                                                                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

> start
✓ Workers iniciados
> flood 100
✓ Añadidas 100/100 tareas
>   → Dataset-W1 procesando export_report_1 (CRITICAL)
  → Dataset-W2 procesando load_data_6 (CRITICAL)
  → Dataset-W3 procesando load_data_11 (CRITICAL)
  → Dataset-W4 procesando calculate_metrics_15 (CRITICAL)
  → Dataset-W5 procesando load_data_20 (CRITICAL)
  → Dataset-W6 procesando load_data_29 (CRITICAL)
  → Dataset-W7 procesando calculate_metrics_30 (CRITICAL)
  → Dataset-W8 procesando sync_db_35 (CRITICAL)
  ✓ Dataset-W7 completó calculate_metrics_30 en 0.63s
  → Dataset-W7 procesando calculate_metrics_41 (CRITICAL)
  ✓ Dataset-W6 completó load_data_29 en 0.71s
  → Dataset-W6 procesando query_sales_44 (CRITICAL)
  ✓ Dataset-W5 completó load_data_20 en 0.99s
  → Dataset-W5 procesando load_data_47 (CRITICAL)
  ✓ Dataset-W3 completó load_data_11 en 1.12s
  → Dataset-W3 procesando load_data_53 (CRITICAL)
  ✓ Dataset-W4 completó calculate_metrics_15 en 1.40s
  → Dataset-W4 procesando sync_db_57 (CRITICAL)
  ✓ Dataset-W8 completó sync_db_35 en 1.53s
  → Dataset-W8 procesando calculate_metrics_62 (CRITICAL)
  ✓ Dataset-W2 completó load_data_6 en 1.62s
  → Dataset-W2 procesando calculate_metrics_63 (CRITICAL)
  ✓ Dataset-W5 completó load_data_47 en 0.68s
  → Dataset-W5 procesando query_sales_68 (CRITICAL)
  ✓ Dataset-W7 completó calculate_metrics_41 en 1.17s
  → Dataset-W7 procesando export_report_73 (CRITICAL)
  ✓ Dataset-W3 completó load_data_53 en 0.70s
  → Dataset-W3 procesando load_data_83 (CRITICAL)
  ✓ Dataset-W1 completó export_report_1 en 1.88s
  → Dataset-W1 procesando load_data_84 (CRITICAL)
  ✓ Dataset-W6 completó query_sales_44 en 1.32s
  → Dataset-W6 procesando sync_db_94 (CRITICAL)
  ✓ Dataset-W3 completó load_data_83 en 0.80s
  → Dataset-W3 procesando query_sales_96 (CRITICAL)
  ✓ Dataset-W5 completó query_sales_68 en 0.98s
  → Dataset-W5 procesando export_report_97 (CRITICAL)
  ✓ Dataset-W2 completó calculate_metrics_63 en 1.05s
  → Dataset-W2 procesando query_sales_99 (CRITICAL)
  ✓ Dataset-W1 completó load_data_84 en 0.81s
  → Dataset-W1 procesando calculate_metrics_0 (HIGH)
  ✓ Dataset-W7 completó export_report_73 en 1.01s
  → Dataset-W7 procesando query_sales_2 (HIGH)
  ✓ Dataset-W8 completó calculate_metrics_62 en 1.68s
  → Dataset-W8 procesando load_data_3 (HIGH)
  ✓ Dataset-W4 completó sync_db_57 en 1.96s
  → Dataset-W4 procesando export_report_7 (HIGH)
  ✓ Dataset-W5 completó export_report_97 en 0.75s
  → Dataset-W5 procesando export_report_8 (HIGH)
  ✓ Dataset-W2 completó query_sales_99 en 1.20s
  → Dataset-W2 procesando export_report_13 (HIGH)
  ✓ Dataset-W3 completó query_sales_96 en 1.29s
  → Dataset-W3 procesando export_report_16 (HIGH)
  ✓ Dataset-W6 completó sync_db_94 en 1.95s
  → Dataset-W6 procesando sync_db_18 (HIGH)
  ✓ Dataset-W7 completó query_sales_2 en 1.42s
  → Dataset-W7 procesando query_sales_19 (HIGH)
  ✓ Dataset-W1 completó calculate_metrics_0 en 1.75s
  → Dataset-W1 procesando load_data_21 (HIGH)
  ✓ Dataset-W4 completó export_report_7 en 1.11s
  → Dataset-W4 procesando load_data_23 (HIGH)
  ✓ Dataset-W3 completó export_report_16 en 1.00s
  → Dataset-W3 procesando export_report_24 (HIGH)
  ✓ Dataset-W7 completó query_sales_19 en 0.71s
  → Dataset-W7 procesando load_data_25 (HIGH)
  ✓ Dataset-W8 completó load_data_3 en 2.00s
  → Dataset-W8 procesando calculate_metrics_26 (HIGH)
  ✓ Dataset-W5 completó export_report_8 en 1.95s
  → Dataset-W5 procesando export_report_27 (HIGH)
  ✓ Dataset-W4 completó load_data_23 en 1.20s
  → Dataset-W4 procesando query_sales_32 (HIGH)
  ✓ Dataset-W2 completó export_report_13 en 1.89s
  → Dataset-W2 procesando load_data_36 (HIGH)
  ✓ Dataset-W6 completó sync_db_18 en 1.89s
  → Dataset-W6 procesando sync_db_37 (HIGH)
  ✓ Dataset-W1 completó load_data_21 en 1.65s
  → Dataset-W1 procesando load_data_40 (HIGH)
  ✓ Dataset-W3 completó export_report_24 en 1.38s
  → Dataset-W3 procesando query_sales_42 (HIGH)
  ✓ Dataset-W2 completó load_data_36 en 0.59s
  → Dataset-W2 procesando query_sales_43 (HIGH)
  ✓ Dataset-W7 completó load_data_25 en 1.42s
  → Dataset-W7 procesando query_sales_45 (HIGH)
  ✓ Dataset-W8 completó calculate_metrics_26 en 1.32s
  → Dataset-W8 procesando query_sales_48 (HIGH)
  ✓ Dataset-W6 completó sync_db_37 en 0.71s
  → Dataset-W6 procesando query_sales_50 (HIGH)
  ✓ Dataset-W3 completó query_sales_42 en 0.31s
  → Dataset-W3 procesando load_data_55 (HIGH)
  ✓ Dataset-W1 completó load_data_40 en 1.00s
  → Dataset-W1 procesando calculate_metrics_56 (HIGH)
  ✓ Dataset-W5 completó export_report_27 en 1.78s
  → Dataset-W5 procesando query_sales_58 (HIGH)
  ✓ Dataset-W7 completó query_sales_45 en 0.81s
  → Dataset-W7 procesando load_data_67 (HIGH)
  ✓ Dataset-W8 completó query_sales_48 en 1.02s
  → Dataset-W8 procesando export_report_69 (HIGH)
  ✓ Dataset-W4 completó query_sales_32 en 2.01s
  → Dataset-W4 procesando query_sales_70 (HIGH)
  ✓ Dataset-W5 completó query_sales_58 en 0.70s
  → Dataset-W5 procesando query_sales_71 (HIGH)
  ✓ Dataset-W2 completó query_sales_43 en 1.50s
  → Dataset-W2 procesando load_data_75 (HIGH)
  ✓ Dataset-W1 completó calculate_metrics_56 en 1.03s
  → Dataset-W1 procesando load_data_80 (HIGH)
  ✓ Dataset-W6 completó query_sales_50 en 1.85s
  → Dataset-W6 procesando query_sales_81 (HIGH)
  ✓ Dataset-W3 completó load_data_55 en 1.84s
  → Dataset-W3 procesando export_report_82 (HIGH)
  ✓ Dataset-W4 completó query_sales_70 en 0.78s
  → Dataset-W4 procesando export_report_88 (HIGH)
  ✓ Dataset-W8 completó export_report_69 en 1.20s
  → Dataset-W8 procesando query_sales_89 (HIGH)
  ✓ Dataset-W7 completó load_data_67 en 1.67s
  → Dataset-W7 procesando query_sales_92 (HIGH)
  ✓ Dataset-W4 completó export_report_88 en 0.53s
  → Dataset-W4 procesando sync_db_98 (HIGH)
  ✓ Dataset-W6 completó query_sales_81 en 0.57s
  → Dataset-W6 procesando sync_db_4 (NORMAL)
  ✓ Dataset-W5 completó query_sales_71 en 1.20s
  → Dataset-W5 procesando load_data_10 (NORMAL)
  ✓ Dataset-W1 completó load_data_80 en 1.06s
  → Dataset-W1 procesando query_sales_12 (NORMAL)
  ✓ Dataset-W3 completó export_report_82 en 0.76s
  → Dataset-W3 procesando sync_db_17 (NORMAL)
  ✓ Dataset-W8 completó query_sales_89 en 0.47s
  → Dataset-W8 procesando query_sales_46 (NORMAL)
  ✓ Dataset-W2 completó load_data_75 en 1.65s
  → Dataset-W2 procesando query_sales_52 (NORMAL)
  ✓ Dataset-W4 completó sync_db_98 en 0.70s
  → Dataset-W4 procesando query_sales_54 (NORMAL)
  ✓ Dataset-W8 completó query_sales_46 en 0.73s
  → Dataset-W8 procesando load_data_64 (NORMAL)
  ✓ Dataset-W7 completó query_sales_92 en 1.24s
  → Dataset-W7 procesando load_data_72 (NORMAL)
  ✓ Dataset-W6 completó sync_db_4 en 1.15s
  → Dataset-W6 procesando sync_db_74 (NORMAL)
  ✓ Dataset-W8 completó load_data_64 en 0.39s
  → Dataset-W8 procesando export_report_76 (NORMAL)
  ✓ Dataset-W1 completó query_sales_12 en 1.28s
  → Dataset-W1 procesando query_sales_79 (NORMAL)
  ✓ Dataset-W5 completó load_data_10 en 1.73s
  → Dataset-W5 procesando export_report_85 (NORMAL)
  ✓ Dataset-W7 completó load_data_72 en 0.70s
  → Dataset-W7 procesando export_report_93 (NORMAL)
  ✓ Dataset-W1 completó query_sales_79 en 0.39s
  → Dataset-W1 procesando export_report_5 (LOW)
  ✓ Dataset-W3 completó sync_db_17 en 1.70s
  → Dataset-W3 procesando export_report_9 (LOW)
  ✓ Dataset-W2 completó query_sales_52 en 1.46s
  → Dataset-W2 procesando sync_db_14 (LOW)
  ✓ Dataset-W6 completó sync_db_74 en 0.98s
  → Dataset-W6 procesando sync_db_22 (LOW)
  ✓ Dataset-W3 completó export_report_9 en 0.39s
  → Dataset-W3 procesando query_sales_28 (LOW)
  ✓ Dataset-W1 completó export_report_5 en 0.61s
  → Dataset-W1 procesando query_sales_31 (LOW)
  ✓ Dataset-W4 completó query_sales_54 en 1.79s
  → Dataset-W4 procesando sync_db_33 (LOW)
  ✓ Dataset-W6 completó sync_db_22 en 0.56s
  → Dataset-W6 procesando load_data_34 (LOW)
  ✓ Dataset-W4 completó sync_db_33 en 0.51s
  → Dataset-W4 procesando query_sales_38 (LOW)
  ✓ Dataset-W8 completó export_report_76 en 1.65s
  → Dataset-W8 procesando export_report_39 (LOW)
  ✓ Dataset-W2 completó sync_db_14 en 1.09s
  → Dataset-W2 procesando calculate_metrics_49 (LOW)
  ✓ Dataset-W7 completó export_report_93 en 1.34s
  → Dataset-W7 procesando export_report_51 (LOW)
  ✓ Dataset-W5 completó export_report_85 en 1.48s
  → Dataset-W5 procesando query_sales_59 (LOW)
  ✓ Dataset-W3 completó query_sales_28 en 1.15s
  → Dataset-W3 procesando sync_db_60 (LOW)
  ✓ Dataset-W6 completó load_data_34 en 0.90s
  → Dataset-W6 procesando query_sales_61 (LOW)
  ✓ Dataset-W2 completó calculate_metrics_49 en 0.70s
  → Dataset-W2 procesando load_data_65 (LOW)
  ✓ Dataset-W7 completó export_report_51 en 0.72s
  → Dataset-W7 procesando export_report_66 (LOW)
  ✓ Dataset-W5 completó query_sales_59 en 0.64s
  → Dataset-W5 procesando calculate_metrics_77 (LOW)
  ✓ Dataset-W4 completó query_sales_38 en 0.90s
  → Dataset-W4 procesando calculate_metrics_78 (LOW)
  ✓ Dataset-W6 completó query_sales_61 en 0.33s
  → Dataset-W6 procesando export_report_86 (LOW)
  ✓ Dataset-W8 completó export_report_39 en 1.06s
  → Dataset-W8 procesando load_data_87 (LOW)
  ✓ Dataset-W3 completó sync_db_60 en 0.89s
  → Dataset-W3 procesando calculate_metrics_90 (LOW)
  ✓ Dataset-W1 completó query_sales_31 en 1.95s
  → Dataset-W1 procesando query_sales_91 (LOW)
  ✓ Dataset-W2 completó load_data_65 en 1.03s
  → Dataset-W2 procesando load_data_95 (LOW)
  ✓ Dataset-W8 completó load_data_87 en 0.79s
  ✓ Dataset-W3 completó calculate_metrics_90 en 0.94s
  ✓ Dataset-W6 completó export_report_86 en 1.50s
  ✓ Dataset-W5 completó calculate_metrics_77 en 1.65s
  ✓ Dataset-W7 completó export_report_66 en 1.70s
  ✓ Dataset-W4 completó calculate_metrics_78 en 1.67s
  ✓ Dataset-W1 completó query_sales_91 en 1.23s
  ✓ Dataset-W2 completó load_data_95 en 1.25s

> status

                           📊 Estado de Colas
╭─────────────────┬──────────────┬──────────────┬──────────────────────╮
│ Cola            │    Tamaño    │  Capacidad   │       Llenado        │
├─────────────────┼──────────────┼──────────────┼──────────────────────┤
│ 📦 Dataset      │      0       │     100      │    ░░░░░░░░░░ 0%     │
│ ⚙️  Command      │      0       │      50      │    ░░░░░░░░░░ 0%     │
╰─────────────────┴──────────────┴──────────────┴──────────────────────╯

                                👷 Workers
╭─────────────────┬─────────────────┬──────────────────────┬──────────────╮
│ ID              │     Estado      │ Tarea Actual         │  Completadas │
├─────────────────┼─────────────────┼──────────────────────┼──────────────┤
│ Dataset-W1      │     🟡 idle     │ -                    │           12 │
│ Dataset-W2      │     🟡 idle     │ -                    │           12 │
│ Dataset-W3      │     🟡 idle     │ -                    │           14 │
│ Dataset-W4      │     🟡 idle     │ -                    │           12 │
│ Dataset-W5      │     🟡 idle     │ -                    │           12 │
│ Dataset-W6      │     🟡 idle     │ -                    │           13 │
│ Dataset-W7      │     🟡 idle     │ -                    │           13 │
│ Dataset-W8      │     🟡 idle     │ -                    │           12 │
│ Command-W1      │     🟡 idle     │ -                    │            0 │
│ Command-W2      │     🟡 idle     │ -                    │            0 │
│ Command-W3      │     🟡 idle     │ -                    │            0 │
│ Command-W4      │     🟡 idle     │ -                    │            0 │
╰─────────────────┴─────────────────┴──────────────────────┴──────────────╯

╭────────────────────────────────────────────────────────────────────── 📈 Métricas ───────────────────────────────────────────────────────────────────────╮
│ Completadas: 100  │  Fallidas: 0  │  Rechazadas: 0                                                                                                       │
│ Throughput: 3.22/s  │  Tiempo Prom: 1.16s  │  Uptime: 31s                                                                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯


4 workers para dataset y 2 para comandos

Resultados:

(venv) C:\Users\sergi\OneDrive\Documentos\GitHub\QueueSystem>python app_cli.py
╔══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║ 🚀 QueueSystem - CLI Interactiva                                                                                                                         ║
║ Sistema de Colas de Alto Rendimiento                                                                                                                     ║
╚══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝

╭──────────────────────────────────────────────────────────────────────── ❓ Ayuda ────────────────────────────────────────────────────────────────────────╮
│                                                                                                                                                          │
│ Comandos disponibles:                                                                                                                                    │
│                                                                                                                                                          │
│   start              Iniciar todos los workers                                                                                                           │
│   stop               Detener todos los workers                                                                                                           │
│   add <name>   Añadir tarea (prio: 0=CRITICAL, 1=HIGH, 2=NORMAL, 3=LOW)                                                                                  │
│   cmd <name>   Añadir comando del sistema                                                                                                                │
│   flood <n>          Añadir N tareas aleatorias                                                                                                          │
│   status             Mostrar estado actual                                                                                                               │
│   clear              Limpiar pantalla                                                                                                                    │
│   help               Mostrar esta ayuda                                                                                                                  │
│   quit               Salir de la aplicación                                                                                                              │
│                                                                                                                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

> start
✓ Workers iniciados
> flood 100
✓ Añadidas 100/100 tareas
>   → Dataset-W1 procesando load_data_2 (CRITICAL)
  → Dataset-W2 procesando export_report_5 (CRITICAL)
  → Dataset-W3 procesando load_data_8 (CRITICAL)
  → Dataset-W4 procesando query_sales_9 (CRITICAL)
  ✓ Dataset-W4 completó query_sales_9 en 0.53s
  → Dataset-W4 procesando sync_db_10 (CRITICAL)
  ✓ Dataset-W2 completó export_report_5 en 0.58s
  → Dataset-W2 procesando export_report_16 (CRITICAL)
  ✓ Dataset-W3 completó load_data_8 en 0.80s
  → Dataset-W3 procesando export_report_18 (CRITICAL)
  ✓ Dataset-W4 completó sync_db_10 en 0.70s
  → Dataset-W4 procesando calculate_metrics_20 (CRITICAL)
  ✓ Dataset-W1 completó load_data_2 en 1.33s
  → Dataset-W1 procesando load_data_22 (CRITICAL)
  ✓ Dataset-W4 completó calculate_metrics_20 en 0.41s
  → Dataset-W4 procesando query_sales_23 (CRITICAL)
  ✓ Dataset-W1 completó load_data_22 en 0.43s
  → Dataset-W1 procesando load_data_27 (CRITICAL)
  ✓ Dataset-W2 completó export_report_16 en 1.39s
  → Dataset-W2 procesando export_report_30 (CRITICAL)
  ✓ Dataset-W4 completó query_sales_23 en 0.56s
  → Dataset-W4 procesando export_report_33 (CRITICAL)
  ✓ Dataset-W2 completó export_report_30 en 0.42s
  → Dataset-W2 procesando sync_db_41 (CRITICAL)
  ✓ Dataset-W3 completó export_report_18 en 1.79s
  → Dataset-W3 procesando sync_db_47 (CRITICAL)
  ✓ Dataset-W4 completó export_report_33 en 1.02s
  → Dataset-W4 procesando calculate_metrics_49 (CRITICAL)
  ✓ Dataset-W1 completó load_data_27 en 1.94s
  → Dataset-W1 procesando calculate_metrics_54 (CRITICAL)
  ✓ Dataset-W3 completó sync_db_47 en 1.22s
  → Dataset-W3 procesando sync_db_55 (CRITICAL)
  ✓ Dataset-W2 completó sync_db_41 en 1.83s
  → Dataset-W2 procesando export_report_56 (CRITICAL)
  ✓ Dataset-W4 completó calculate_metrics_49 en 1.27s
  → Dataset-W4 procesando sync_db_61 (CRITICAL)
  ✓ Dataset-W1 completó calculate_metrics_54 en 1.37s
  → Dataset-W1 procesando export_report_69 (CRITICAL)
  ✓ Dataset-W4 completó sync_db_61 en 0.58s
  → Dataset-W4 procesando query_sales_72 (CRITICAL)
  ✓ Dataset-W2 completó export_report_56 en 1.06s
  → Dataset-W2 procesando calculate_metrics_75 (CRITICAL)
  ✓ Dataset-W3 completó sync_db_55 en 1.54s
  → Dataset-W3 procesando load_data_77 (CRITICAL)
  ✓ Dataset-W1 completó export_report_69 en 0.46s
  → Dataset-W1 procesando calculate_metrics_85 (CRITICAL)
  ✓ Dataset-W1 completó calculate_metrics_85 en 0.34s
  → Dataset-W1 procesando load_data_87 (CRITICAL)
  ✓ Dataset-W2 completó calculate_metrics_75 en 0.73s
  → Dataset-W2 procesando query_sales_88 (CRITICAL)
  ✓ Dataset-W4 completó query_sales_72 en 0.96s
  → Dataset-W4 procesando sync_db_89 (CRITICAL)
  ✓ Dataset-W3 completó load_data_77 en 1.04s
  → Dataset-W3 procesando query_sales_92 (CRITICAL)
  ✓ Dataset-W4 completó sync_db_89 en 0.41s
  → Dataset-W4 procesando sync_db_0 (HIGH)
  ✓ Dataset-W2 completó query_sales_88 en 0.67s
  → Dataset-W2 procesando query_sales_1 (HIGH)
  ✓ Dataset-W3 completó query_sales_92 en 0.46s
  → Dataset-W3 procesando calculate_metrics_11 (HIGH)
  ✓ Dataset-W4 completó sync_db_0 en 0.59s
  → Dataset-W4 procesando query_sales_12 (HIGH)
  ✓ Dataset-W3 completó calculate_metrics_11 en 0.40s
  → Dataset-W3 procesando load_data_14 (HIGH)
  ✓ Dataset-W1 completó load_data_87 en 1.96s
  → Dataset-W1 procesando load_data_17 (HIGH)
  ✓ Dataset-W1 completó load_data_17 en 0.76s
  → Dataset-W1 procesando query_sales_19 (HIGH)
  ✓ Dataset-W2 completó query_sales_1 en 1.97s
  → Dataset-W2 procesando query_sales_24 (HIGH)
  ✓ Dataset-W4 completó query_sales_12 en 1.82s
  → Dataset-W4 procesando export_report_26 (HIGH)
  ✓ Dataset-W2 completó query_sales_24 en 0.31s
  → Dataset-W2 procesando export_report_34 (HIGH)
  ✓ Dataset-W3 completó load_data_14 en 1.82s
  → Dataset-W3 procesando export_report_35 (HIGH)
  ✓ Dataset-W2 completó export_report_34 en 0.48s
  → Dataset-W2 procesando calculate_metrics_36 (HIGH)
  ✓ Dataset-W1 completó query_sales_19 en 0.93s
  → Dataset-W1 procesando load_data_42 (HIGH)
  ✓ Dataset-W2 completó calculate_metrics_36 en 0.52s
  → Dataset-W2 procesando export_report_43 (HIGH)
  ✓ Dataset-W3 completó export_report_35 en 1.08s
  → Dataset-W3 procesando load_data_44 (HIGH)
  ✓ Dataset-W4 completó export_report_26 en 1.39s
  → Dataset-W4 procesando sync_db_52 (HIGH)
  ✓ Dataset-W1 completó load_data_42 en 0.91s
  → Dataset-W1 procesando load_data_57 (HIGH)
  ✓ Dataset-W2 completó export_report_43 en 0.52s
  → Dataset-W2 procesando query_sales_66 (HIGH)
  ✓ Dataset-W3 completó load_data_44 en 1.10s
  → Dataset-W3 procesando load_data_74 (HIGH)
  ✓ Dataset-W1 completó load_data_57 en 0.86s
  → Dataset-W1 procesando export_report_79 (HIGH)
  ✓ Dataset-W4 completó sync_db_52 en 1.33s
  → Dataset-W4 procesando query_sales_82 (HIGH)
  ✓ Dataset-W2 completó query_sales_66 en 1.27s
  → Dataset-W2 procesando query_sales_90 (HIGH)
  ✓ Dataset-W2 completó query_sales_90 en 0.57s
  → Dataset-W2 procesando load_data_91 (HIGH)
  ✓ Dataset-W3 completó load_data_74 en 1.14s
  → Dataset-W3 procesando query_sales_93 (HIGH)
  ✓ Dataset-W1 completó export_report_79 en 1.38s
  → Dataset-W1 procesando load_data_94 (HIGH)
  ✓ Dataset-W4 completó query_sales_82 en 1.18s
  → Dataset-W4 procesando load_data_97 (HIGH)
  ✓ Dataset-W3 completó query_sales_93 en 0.97s
  → Dataset-W3 procesando export_report_98 (HIGH)
  ✓ Dataset-W2 completó load_data_91 en 1.14s
  → Dataset-W2 procesando sync_db_13 (NORMAL)
  ✓ Dataset-W1 completó load_data_94 en 0.98s
  → Dataset-W1 procesando load_data_15 (NORMAL)
  ✓ Dataset-W2 completó sync_db_13 en 0.58s
  → Dataset-W2 procesando sync_db_21 (NORMAL)
  ✓ Dataset-W2 completó sync_db_21 en 0.42s
  → Dataset-W2 procesando calculate_metrics_25 (NORMAL)
  ✓ Dataset-W1 completó load_data_15 en 0.77s
  → Dataset-W1 procesando calculate_metrics_28 (NORMAL)
  ✓ Dataset-W4 completó load_data_97 en 1.70s
  → Dataset-W4 procesando sync_db_31 (NORMAL)
  ✓ Dataset-W3 completó export_report_98 en 1.16s
  → Dataset-W3 procesando query_sales_32 (NORMAL)
  ✓ Dataset-W2 completó calculate_metrics_25 en 1.18s
  → Dataset-W2 procesando sync_db_37 (NORMAL)
  ✓ Dataset-W2 completó sync_db_37 en 0.64s
  → Dataset-W2 procesando export_report_38 (NORMAL)
  ✓ Dataset-W4 completó sync_db_31 en 1.92s
  → Dataset-W4 procesando sync_db_40 (NORMAL)
  ✓ Dataset-W1 completó calculate_metrics_28 en 1.94s
  → Dataset-W1 procesando sync_db_48 (NORMAL)
  ✓ Dataset-W3 completó query_sales_32 en 1.92s
  → Dataset-W3 procesando export_report_51 (NORMAL)
  ✓ Dataset-W1 completó sync_db_48 en 1.25s
  → Dataset-W1 procesando export_report_53 (NORMAL)
  ✓ Dataset-W4 completó sync_db_40 en 1.41s
  → Dataset-W4 procesando query_sales_58 (NORMAL)
  ✓ Dataset-W2 completó export_report_38 en 1.91s
  → Dataset-W2 procesando calculate_metrics_63 (NORMAL)
  ✓ Dataset-W3 completó export_report_51 en 1.88s
  → Dataset-W3 procesando sync_db_65 (NORMAL)
  ✓ Dataset-W1 completó export_report_53 en 0.69s
  → Dataset-W1 procesando load_data_67 (NORMAL)
  ✓ Dataset-W4 completó query_sales_58 en 0.85s
  → Dataset-W4 procesando export_report_70 (NORMAL)
  ✓ Dataset-W3 completó sync_db_65 en 1.05s
  → Dataset-W3 procesando export_report_71 (NORMAL)
  ✓ Dataset-W1 completó load_data_67 en 1.16s
  → Dataset-W1 procesando sync_db_73 (NORMAL)
  ✓ Dataset-W2 completó calculate_metrics_63 en 1.61s
  → Dataset-W2 procesando load_data_78 (NORMAL)
  ✓ Dataset-W3 completó export_report_71 en 0.98s
  → Dataset-W3 procesando load_data_80 (NORMAL)
  ✓ Dataset-W4 completó export_report_70 en 1.84s
  → Dataset-W4 procesando calculate_metrics_81 (NORMAL)
  ✓ Dataset-W2 completó load_data_78 en 0.97s
  → Dataset-W2 procesando export_report_83 (NORMAL)
  ✓ Dataset-W1 completó sync_db_73 en 1.77s
  → Dataset-W1 procesando sync_db_95 (NORMAL)
  ✓ Dataset-W4 completó calculate_metrics_81 en 0.82s
  → Dataset-W4 procesando load_data_99 (NORMAL)
  ✓ Dataset-W3 completó load_data_80 en 1.40s
  → Dataset-W3 procesando load_data_3 (LOW)
  ✓ Dataset-W2 completó export_report_83 en 1.15s
  → Dataset-W2 procesando query_sales_4 (LOW)
  ✓ Dataset-W4 completó load_data_99 en 0.68s
  → Dataset-W4 procesando export_report_6 (LOW)
  ✓ Dataset-W2 completó query_sales_4 en 0.45s
  → Dataset-W2 procesando load_data_7 (LOW)
  ✓ Dataset-W2 completó load_data_7 en 0.45s
  → Dataset-W2 procesando sync_db_29 (LOW)
  ✓ Dataset-W1 completó sync_db_95 en 1.60s
  → Dataset-W1 procesando query_sales_39 (LOW)
  ✓ Dataset-W3 completó load_data_3 en 1.30s
  → Dataset-W3 procesando export_report_45 (LOW)
  ✓ Dataset-W4 completó export_report_6 en 1.81s
  → Dataset-W4 procesando sync_db_46 (LOW)
  ✓ Dataset-W1 completó query_sales_39 en 1.49s
  → Dataset-W1 procesando export_report_50 (LOW)
  ✓ Dataset-W2 completó sync_db_29 en 1.75s
  → Dataset-W2 procesando sync_db_59 (LOW)
  ✓ Dataset-W4 completó sync_db_46 en 0.87s
  → Dataset-W4 procesando load_data_60 (LOW)
  ✓ Dataset-W1 completó export_report_50 en 0.57s
  → Dataset-W1 procesando load_data_62 (LOW)
  ✓ Dataset-W3 completó export_report_45 en 1.98s
  → Dataset-W3 procesando calculate_metrics_64 (LOW)
  ✓ Dataset-W2 completó sync_db_59 en 0.98s
  → Dataset-W2 procesando calculate_metrics_68 (LOW)
  ✓ Dataset-W4 completó load_data_60 en 1.16s
  → Dataset-W4 procesando calculate_metrics_76 (LOW)
  ✓ Dataset-W1 completó load_data_62 en 1.24s
  → Dataset-W1 procesando load_data_84 (LOW)
  ✓ Dataset-W4 completó calculate_metrics_76 en 0.45s
  → Dataset-W4 procesando load_data_86 (LOW)
  ✓ Dataset-W2 completó calculate_metrics_68 en 1.05s
  → Dataset-W2 procesando calculate_metrics_96 (LOW)
  ✓ Dataset-W3 completó calculate_metrics_64 en 1.72s
  ✓ Dataset-W1 completó load_data_84 en 0.70s
  ✓ Dataset-W2 completó calculate_metrics_96 en 0.63s
  ✓ Dataset-W4 completó load_data_86 en 1.92s

> status

                           📊 Estado de Colas
╭─────────────────┬──────────────┬──────────────┬──────────────────────╮
│ Cola            │    Tamaño    │  Capacidad   │       Llenado        │
├─────────────────┼──────────────┼──────────────┼──────────────────────┤
│ 📦 Dataset      │      0       │     100      │    ░░░░░░░░░░ 0%     │
│ ⚙️  Command      │      0       │      50      │    ░░░░░░░░░░ 0%     │
╰─────────────────┴──────────────┴──────────────┴──────────────────────╯

                                👷 Workers
╭─────────────────┬─────────────────┬──────────────────────┬──────────────╮
│ ID              │     Estado      │ Tarea Actual         │  Completadas │
├─────────────────┼─────────────────┼──────────────────────┼──────────────┤
│ Dataset-W1      │     🟡 idle     │ -                    │           24 │
│ Dataset-W2      │     🟡 idle     │ -                    │           29 │
│ Dataset-W3      │     🟡 idle     │ -                    │           21 │
│ Dataset-W4      │     🟡 idle     │ -                    │           26 │
│ Command-W1      │     🟡 idle     │ -                    │            0 │
│ Command-W2      │     🟡 idle     │ -                    │            0 │
╰─────────────────┴─────────────────┴──────────────────────┴──────────────╯

╭────────────────────────────────────────────────────────────────────── 📈 Métricas ───────────────────────────────────────────────────────────────────────╮
│ Completadas: 100  │  Fallidas: 0  │  Rechazadas: 0                                                                                                       │
│ Throughput: 1.67/s  │  Tiempo Prom: 1.09s  │  Uptime: 60s                                                                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

>