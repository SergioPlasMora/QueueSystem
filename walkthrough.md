# 🎓 QueueSystem - Guía Completa

## Índice
1. [Visión General](#visión-general)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Componentes en Detalle](#componentes-en-detalle)
4. [Flujo de Datos](#flujo-de-datos)
5. [Conceptos Teóricos](#conceptos-teóricos)

---

## Visión General

### ¿Qué problema resuelve?

Imagina un restaurante:
- **Sin sistema de colas:** Un solo mesero atiende a todos. Si alguien pide un plato complicado, todos esperan.
- **Con sistema de colas:** Varios meseros trabajan en paralelo. Los pedidos urgentes (VIP) se atienden primero.

```
SIN COLAS (Secuencial)                    CON COLAS (Paralelo)
═══════════════════════                   ═══════════════════════

Tarea 1 ──────────────────►               Tarea 1 ──► Worker 1 ──►
          (espera)                        Tarea 2 ──► Worker 2 ──►
Tarea 2 ──────────────────►               Tarea 3 ──► Worker 3 ──►
          (espera)                        Tarea 4 ──► Worker 4 ──►
Tarea 3 ──────────────────►

Tiempo total: T1 + T2 + T3                Tiempo total: max(T1,T2,T3,T4)
```

---

## Arquitectura del Sistema

### Diagrama General

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              QueueManager                                    │
│                                                                             │
│   ┌─────────────────────────────┐     ┌─────────────────────────────┐      │
│   │      DATASET QUEUE          │     │     COMMAND QUEUE           │      │
│   │      (PriorityQueue)        │     │     (PriorityQueue)         │      │
│   │                             │     │                             │      │
│   │  ┌───┬───┬───┬───┬───┐     │     │  ┌───┬───┬───┐             │      │
│   │  │ 0 │ 1 │ 2 │ 2 │ 3 │     │     │  │ 0 │ 1 │ 1 │             │      │
│   │  └───┴───┴───┴───┴───┘     │     │  └───┴───┴───┘             │      │
│   │   ▲                         │     │   ▲                         │      │
│   │   │ Ordenado por prioridad  │     │   │ Ordenado por prioridad  │      │
│   └───┼─────────────────────────┘     └───┼─────────────────────────┘      │
│       │                                   │                                 │
│   ┌───┴───────────────────────┐     ┌───┴───────────────────────┐         │
│   │      WORKER POOL          │     │      WORKER POOL          │         │
│   │                           │     │                           │         │
│   │  W1 ●──► Procesando...   │     │  W1 ●──► Procesando...   │         │
│   │  W2 ●──► Procesando...   │     │  W2 ○    Idle            │         │
│   │  W3 ○    Idle            │     │                           │         │
│   │  W4 ●──► Procesando...   │     │                           │         │
│   └───────────────────────────┘     └───────────────────────────┘         │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │                         METRICS                                  │      │
│   │  Completadas: 33 | Fallidas: 0 | Throughput: 0.39/s             │      │
│   └─────────────────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Estructura de Archivos

```
QueueSystem/
├── queue_system/
│   ├── task.py              ← Define qué es una "tarea"
│   ├── priority_queue.py    ← Cola que ordena por prioridad
│   ├── worker_pool.py       ← Grupo de workers que procesan
│   ├── queue_manager.py     ← Coordinador central
│   └── metrics.py           ← Estadísticas
└── app_cli.py               ← Interfaz de usuario
```

---

## Componentes en Detalle

### 1️⃣ Task (Tarea)

**Archivo:** [task.py](file:///c:/Users/Usuario/Documents/GitHub/QueueSystem/queue_system/task.py)

Una **Task** es el "paquete de trabajo" que viaja por el sistema.

```python
@dataclass(order=True)  # ← Permite comparar tareas para ordenarlas
class Task:
    # Campos de ORDENAMIENTO (determinan posición en la cola)
    priority: TaskPriority      # 0=CRITICAL, 1=HIGH, 2=NORMAL, 3=LOW
    created_at: float           # Timestamp de creación
    
    # Campos de DATOS (no afectan el orden)
    task_id: str                # Identificador único
    name: str                   # Nombre descriptivo
    processing_time: float      # Tiempo simulado de trabajo
```

#### ¿Por qué `@dataclass(order=True)`?

Python genera automáticamente métodos de comparación:

```python
# Python genera esto automáticamente:
def __lt__(self, other):
    return (self.priority, self.created_at) < (other.priority, other.created_at)
```

Esto permite que `heapq` ordene las tareas correctamente:

```
Tarea A: priority=2, created_at=100
Tarea B: priority=1, created_at=200
Tarea C: priority=2, created_at=50

Orden resultante: B, C, A
                  ↑  ↑  ↑
                  │  │  └── priority=2, pero created_at=100 > 50
                  │  └───── priority=2, created_at=50
                  └──────── priority=1 (menor = más urgente)
```

---

### 2️⃣ PriorityQueue (Cola con Prioridades)

**Archivo:** [priority_queue.py](file:///c:/Users/Usuario/Documents/GitHub/QueueSystem/queue_system/priority_queue.py)

#### Concepto: Min-Heap

Un **heap** es una estructura de datos en forma de árbol donde:
- El elemento **más pequeño** siempre está en la raíz
- Inserción y extracción son O(log n)

```
        ┌───┐
        │ 0 │  ← Raíz (mínimo)
        └─┬─┘
      ┌───┴───┐
    ┌─┴─┐   ┌─┴─┐
    │ 1 │   │ 2 │
    └───┘   └───┘
    
heappush(3) →  El 3 "burbujea" hacia abajo
heappop()   →  Retorna 0, reorganiza el heap
```

#### Implementación Visual

```python
class PriorityQueue:
    def __init__(self):
        self._heap = []           # Lista que heapq mantiene ordenada
        self._lock = asyncio.Lock()     # Evita race conditions
        self._not_empty = asyncio.Event()  # Señal: "hay tareas disponibles"
```

**Operación PUT (añadir tarea):**

```
Estado inicial:          Después de put(Task(priority=1)):
┌───────────────┐        ┌───────────────┐
│ heap: [2, 3]  │        │ heap: [1,3,2] │  ← heapq reordena
│ not_empty: ✓  │        │ not_empty: ✓  │
└───────────────┘        └───────────────┘
```

```python
async def put(self, task):
    async with self._lock:              # 1. Adquirir lock
        heapq.heappush(self._heap, task)  # 2. Insertar ordenado
        self._not_empty.set()             # 3. Señalar "hay tareas"
```

**Operación GET (obtener tarea):**

```
Estado inicial:          Worker espera:          Después de get():
┌───────────────┐        ┌───────────────┐      ┌───────────────┐
│ heap: []      │        │ heap: [1,2,3] │ ──►  │ heap: [2,3]   │
│ not_empty: ✗  │        │ not_empty: ✓  │      │ Retorna: 1    │
└───────────────┘        └───────────────┘      └───────────────┘
     │                         ▲
     │   Worker bloqueado      │
     │   esperando...          │
     └─────────────────────────┘
          put() activa al worker
```

```python
async def get(self):
    await self._not_empty.wait()  # 1. Esperar señal (no bloquea event loop)
    async with self._lock:         # 2. Adquirir lock
        task = heapq.heappop(self._heap)  # 3. Extraer mínimo
        if not self._heap:
            self._not_empty.clear()  # 4. Si vacía, quitar señal
        return task
```

---

### 3️⃣ WorkerPool (Pool de Workers)

**Archivo:** [worker_pool.py](file:///c:/Users/Usuario/Documents/GitHub/QueueSystem/queue_system/worker_pool.py)

#### Concepto: Workers Paralelos

Cada worker es un **loop infinito** que:
1. Espera una tarea de la cola
2. La procesa
3. Notifica que terminó
4. Repite

```
┌──────────────────────────────────────────────────────────────────┐
│                         WorkerPool                                │
│                                                                  │
│   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐           │
│   │  Worker 1   │   │  Worker 2   │   │  Worker 3   │           │
│   │             │   │             │   │             │           │
│   │  ┌───────┐  │   │  ┌───────┐  │   │  ┌───────┐  │           │
│   │  │ Loop  │  │   │  │ Loop  │  │   │  │ Loop  │  │           │
│   │  │  ↓    │  │   │  │  ↓    │  │   │  │  ↓    │  │           │
│   │  │ get() │◄─┼───┼──┼ get() │◄─┼───┼──┼ get() │◄─┼───┐       │
│   │  │  ↓    │  │   │  │  ↓    │  │   │  │  ↓    │  │   │       │
│   │  │process│  │   │  │process│  │   │  │process│  │   │       │
│   │  │  ↓    │  │   │  │  ↓    │  │   │  │  ↓    │  │   │       │
│   │  │notify │  │   │  │notify │  │   │  │notify │  │   │       │
│   │  └───────┘  │   │  └───────┘  │   │  └───────┘  │   │       │
│   └─────────────┘   └─────────────┘   └─────────────┘   │       │
│                                                         │       │
│                    ┌────────────────┐                   │       │
│                    │ PriorityQueue  │◄──────────────────┘       │
│                    │  [T1, T2, T3]  │                           │
│                    └────────────────┘                           │
└──────────────────────────────────────────────────────────────────┘
```

#### El Loop del Worker

```python
async def _worker_loop(self, worker_id: str):
    while self.running:
        # 1. ESPERAR tarea (no bloquea otros workers)
        task = await self.queue.get(timeout=0.5)
        
        if task is None:
            continue  # Timeout, verificar si sigue running
        
        # 2. PROCESAR tarea
        task.mark_started(worker_id)
        await asyncio.sleep(task.processing_time)  # Simula trabajo
        task.mark_completed()
        
        # 3. NOTIFICAR
        await self.on_task_complete(task, worker_id, elapsed)
```

#### ¿Por qué `asyncio.sleep()` y no `time.sleep()`?

```
time.sleep(1)         →  BLOQUEA todo el programa
                          Ningún otro worker puede ejecutar

asyncio.sleep(1)      →  CEDE el control al event loop
                          Otros workers pueden ejecutar mientras tanto
```

```
Timeline con time.sleep (BLOQUEANTE):
┌─────────────────────────────────────────────┐
│ W1: ████████████████████                    │
│ W2:                     ████████████████████│
│ W3:                                         │ (esperando)
└─────────────────────────────────────────────┘
                Tiempo total: 2x

Timeline con asyncio.sleep (CONCURRENTE):
┌─────────────────────────────────────────────┐
│ W1: ████████████████████                    │
│ W2: ████████████████████                    │
│ W3: ████████████████████                    │
└─────────────────────────────────────────────┘
                Tiempo total: 1x
```

---

### 4️⃣ QueueManager (Coordinador Central)

**Archivo:** [queue_manager.py](file:///c:/Users/Usuario/Documents/GitHub/QueueSystem/queue_system/queue_manager.py)

El QueueManager es el **director de orquesta** que coordina todo:

```python
class QueueManager:
    def __init__(self):
        # DOS colas separadas
        self.dataset_queue = PriorityQueue(maxsize=100)
        self.command_queue = PriorityQueue(maxsize=50)
        
        # DOS pools de workers
        self.dataset_pool = WorkerPool(num_workers=4, queue=self.dataset_queue)
        self.command_pool = WorkerPool(num_workers=2, queue=self.command_queue)
        
        # Métricas compartidas
        self.metrics = QueueMetrics()
```

#### ¿Por qué dos colas?

```
PROBLEMA: Una sola cola
┌─────────────────────────────────────────────────────────────┐
│   Cola única: [Dataset(60s), Dataset(45s), Comando(0.1s)]  │
│                                                             │
│   El comando de 0.1s debe esperar 105 segundos! 😱         │
└─────────────────────────────────────────────────────────────┘

SOLUCIÓN: Dos colas separadas
┌─────────────────────────────────────────────────────────────┐
│   Dataset Queue: [Dataset(60s), Dataset(45s)]              │
│   → Workers 1-4 procesando...                               │
│                                                             │
│   Command Queue: [Comando(0.1s)]                           │
│   → Workers 1-2 procesan INMEDIATAMENTE                    │
└─────────────────────────────────────────────────────────────┘
```

---

## Flujo de Datos

### Flujo Completo: Del CLI al Resultado

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           FLUJO DE UN "add tarea 1"                         │
└─────────────────────────────────────────────────────────────────────────────┘

    Usuario                           
       │                              
       │ "add mi_tarea 1"             
       ▼                              
┌─────────────────┐                   
│    app_cli.py   │                   
│                 │                   
│ cmd_add()       │                   
│   │             │                   
│   ▼             │                   
│ Task(           │                   
│   priority=1,   │                   
│   name="mi.."   │                   
│ )               │                   
└────────┬────────┘                   
         │                            
         │ manager.enqueue(task)      
         ▼                            
┌─────────────────────────────────────────────────────────────────────────────┐
│                              QueueManager                                    │
│                                                                             │
│    enqueue(task)                                                            │
│         │                                                                   │
│         │ if task.type == DATASET                                           │
│         ▼                                                                   │
│    ┌─────────────────────────────────┐                                     │
│    │        dataset_queue.put()       │                                     │
│    │                                  │                                     │
│    │  Heap: [Task(1), Task(2), ...]  │                                     │
│    │                                  │                                     │
│    │  _not_empty.set() ─────────────────────┐                              │
│    └─────────────────────────────────┘      │                              │
│                                             │                              │
│    ┌─────────────────────────────────┐      │                              │
│    │         WorkerPool              │      │                              │
│    │                                 │      │ Señal "hay tareas"           │
│    │  W1: await queue.get() ◄───────────────┘                              │
│    │         │                       │                                     │
│    │         │ Recibe Task(1)        │                                     │
│    │         ▼                       │                                     │
│    │      process(task)              │                                     │
│    │         │                       │                                     │
│    │         │ await sleep(1.5s)     │                                     │
│    │         ▼                       │                                     │
│    │      on_task_complete() ────────────────┐                             │
│    └─────────────────────────────────┘       │                             │
│                                              │                             │
│    ┌─────────────────────────────────┐       │                             │
│    │          Metrics                │       │                             │
│    │                                 │◄──────┘                             │
│    │  record_completed()             │                                     │
│    │  tasks_completed += 1           │                                     │
│    └─────────────────────────────────┘                                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
         │
         │ Callback a CLI
         ▼
┌─────────────────┐
│    app_cli.py   │
│                 │
│ on_task_complete│
│   print(...)    │
└─────────────────┘
         │
         ▼
    "✓ Dataset-W1 completó mi_tarea en 1.50s"
```

---

## Conceptos Teóricos

### 1. Event Loop (Bucle de Eventos)

El **event loop** es el corazón de asyncio. Imagina un director de orquesta:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                             EVENT LOOP                                       │
│                                                                             │
│   "¿Quién necesita mi atención ahora?"                                      │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────┐       │
│   │  Cola de tareas listas para ejecutar                           │       │
│   │  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐                            │       │
│   │  │ W1  │  │ W2  │  │ W3  │  │ CLI │                            │       │
│   │  └──┬──┘  └──┬──┘  └──┬──┘  └──┬──┘                            │       │
│   │     │        │        │        │                                │       │
│   │     ▼        ▼        ▼        ▼                                │       │
│   │  Ejecuta  Ejecuta  Ejecuta  Ejecuta                            │       │
│   │  hasta    hasta    hasta    hasta                              │       │
│   │  await    await    await    await                              │       │
│   └─────────────────────────────────────────────────────────────────┘       │
│                                                                             │
│   Cuando alguien hace "await":                                              │
│   → Cede el control al event loop                                           │
│   → El event loop ejecuta otra tarea                                        │
│   → Cuando el await termina, retoma la tarea original                       │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2. Concurrencia vs Paralelismo

```
CONCURRENCIA (asyncio):
═══════════════════════
Un solo CPU, múltiples tareas intercaladas

CPU: ┌─W1─┐ ┌─W2─┐ ┌─W1─┐ ┌─W3─┐ ┌─W2─┐
     └────┘ └────┘ └────┘ └────┘ └────┘

→ Eficiente para I/O (esperar red, disco, BD)
→ Un worker "espera" mientras otros trabajan


PARALELISMO (multiprocessing):
══════════════════════════════
Múltiples CPUs, tareas simultáneas

CPU 1: ┌──────W1──────┐
CPU 2: ┌──────W2──────┐
CPU 3: ┌──────W3──────┐
CPU 4: ┌──────W4──────┐

→ Eficiente para CPU-bound (cálculos pesados)
→ Cada worker tiene su propio procesador
```

**Nuestro sistema usa CONCURRENCIA** porque las tareas simulan I/O (await sleep).

### 3. Race Conditions y Locks

**Problema:** Dos workers modifican la cola al mismo tiempo:

```
SIN LOCK:
═════════
W1: lee heap[0] = Task_A
                            W2: lee heap[0] = Task_A  (¡mismo task!)
W1: pop() → procesa Task_A
                            W2: pop() → ERROR o duplicado!
```

**Solución:** asyncio.Lock

```python
async with self._lock:  # Solo uno puede entrar a la vez
    task = heapq.heappop(self._heap)
```

```
CON LOCK:
═════════
W1: adquiere lock
W1: pop() → Task_A
W1: libera lock
                      W2: adquiere lock (ahora puede)
                      W2: pop() → Task_B
                      W2: libera lock
```

### 4. Events (Señales)

`asyncio.Event` es como un semáforo:

```python
event = asyncio.Event()

# Worker esperando
await event.wait()  # Bloqueado hasta que alguien haga set()

# Productor señala
event.set()  # ¡Despierta a todos los que esperan!
```

```
Estado: event.clear() (apagado)
┌────────────────┐
│     🔴         │  Workers esperando...
└────────────────┘

Estado: event.set() (encendido)
┌────────────────┐
│     🟢         │  ¡Workers despiertan!
└────────────────┘
```

---

## Resumen Visual Final

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        SISTEMA DE COLAS COMPLETO                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Usuario                 QueueManager               Salida                  │
│     │                         │                        │                    │
│     │  "add tarea 1"          │                        │                    │
│     ├────────────────────────►│                        │                    │
│     │                         │                        │                    │
│     │           ┌─────────────┴─────────────┐          │                    │
│     │           │                           │          │                    │
│     │           ▼                           ▼          │                    │
│     │    ╔═══════════╗              ╔═══════════╗      │                    │
│     │    ║  Dataset  ║              ║  Command  ║      │                    │
│     │    ║   Queue   ║              ║   Queue   ║      │                    │
│     │    ║ ┌─┬─┬─┬─┐ ║              ║ ┌─┬─┬─┐   ║      │                    │
│     │    ║ │0│1│2│3│ ║              ║ │0│1│2│   ║      │                    │
│     │    ║ └─┴─┴─┴─┘ ║              ║ └─┴─┴─┘   ║      │                    │
│     │    ╚═════╤═════╝              ╚═════╤═════╝      │                    │
│     │          │                          │            │                    │
│     │    ┌─────┴─────┐              ┌─────┴─────┐      │                    │
│     │    │  Workers  │              │  Workers  │      │                    │
│     │    │ W1 W2 W3 W4│              │   W1 W2   │      │                    │
│     │    │ ●  ●  ○  ● │              │   ●  ○    │      │                    │
│     │    └─────┬─────┘              └─────┬─────┘      │                    │
│     │          │                          │            │                    │
│     │          └──────────┬───────────────┘            │                    │
│     │                     │                            │                    │
│     │                     ▼                            │                    │
│     │              ╔════════════╗                      │                    │
│     │              ║  Metrics   ║                      │                    │
│     │              ║ completed  ║                      │                    │
│     │              ║ throughput ║                      │                    │
│     │              ╚══════╤═════╝                      │                    │
│     │                     │                            │                    │
│     │                     └───────────────────────────►│                    │
│     │                           "✓ W1 completó..."     │                    │
│     │                                                  │                    │
└─────┴──────────────────────────────────────────────────┴────────────────────┘

Leyenda:
  ● = Worker procesando
  ○ = Worker idle
  0,1,2,3 = Prioridades (menor = más urgente)
```

---

## ¿Qué Sigue?

Ahora que entiendes el sistema, el siguiente paso es **migrarlo al data-conector** donde:
- Las tareas serán **DoGet requests reales** (no simuladas)
- El procesamiento será **carga de datos desde BD**
- Los comandos serán **operaciones del sistema reales**
