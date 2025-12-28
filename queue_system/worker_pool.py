"""
Pool de workers asíncronos para procesamiento paralelo.

Cada worker es un asyncio.Task que consume tareas de una cola
y las procesa de forma independiente.
"""

import asyncio
from typing import Callable, Awaitable
from enum import Enum
from .task import Task
from .priority_queue import PriorityQueue


class WorkerState(Enum):
    """Estado de un worker."""
    IDLE = "idle"
    PROCESSING = "processing"
    STOPPED = "stopped"


class Worker:
    """Representa un worker individual con su estado."""
    
    def __init__(self, worker_id: str):
        self.worker_id = worker_id
        self.state = WorkerState.IDLE
        self.current_task: Task | None = None
        self.tasks_completed = 0
        self.total_processing_time = 0.0


class WorkerPool:
    """
    Pool de workers que procesan tareas en paralelo.
    
    Ejemplo:
        pool = WorkerPool(num_workers=4, queue=my_queue)
        pool.on_task_start = my_start_callback
        pool.on_task_complete = my_complete_callback
        
        await pool.start()
        # ... workers procesan tareas ...
        await pool.stop()
    """

    def __init__(
        self, 
        num_workers: int, 
        queue: PriorityQueue,
        name: str = "Pool"
    ):
        """
        Args:
            num_workers: Número de workers a crear
            queue: Cola de donde tomar tareas
            name: Nombre del pool (para logs)
        """
        self.num_workers = num_workers
        self.queue = queue
        self.name = name
        
        self.workers: dict[str, Worker] = {}
        self._tasks: list[asyncio.Task] = []
        self.running = False
        
        # Callbacks para eventos
        self.on_task_start: Callable[[Task, str], Awaitable[None]] | None = None
        self.on_task_complete: Callable[[Task, str, float], Awaitable[None]] | None = None
        self.on_task_error: Callable[[Task, str, Exception], Awaitable[None]] | None = None

    @property
    def active_workers(self) -> int:
        """Número de workers actualmente procesando."""
        return sum(1 for w in self.workers.values() if w.state == WorkerState.PROCESSING)

    @property
    def idle_workers(self) -> int:
        """Número de workers en espera."""
        return sum(1 for w in self.workers.values() if w.state == WorkerState.IDLE)

    async def start(self):
        """Inicia todos los workers."""
        if self.running:
            return
            
        self.running = True
        
        for i in range(self.num_workers):
            worker_id = f"{self.name}-W{i+1}"
            self.workers[worker_id] = Worker(worker_id)
            
            task = asyncio.create_task(
                self._worker_loop(worker_id),
                name=worker_id
            )
            self._tasks.append(task)

    async def stop(self, wait: bool = True, timeout: float = 5.0):
        """
        Detiene todos los workers.
        
        Args:
            wait: Si True, espera a que terminen las tareas actuales
            timeout: Tiempo máximo de espera
        """
        self.running = False
        
        for worker in self.workers.values():
            if worker.state != WorkerState.PROCESSING:
                worker.state = WorkerState.STOPPED
        
        if wait and self._tasks:
            try:
                await asyncio.wait_for(
                    asyncio.gather(*self._tasks, return_exceptions=True),
                    timeout=timeout
                )
            except asyncio.TimeoutError:
                # Cancelar tareas pendientes
                for task in self._tasks:
                    task.cancel()
        
        self._tasks.clear()
        
        for worker in self.workers.values():
            worker.state = WorkerState.STOPPED

    async def _worker_loop(self, worker_id: str):
        """
        Loop principal de cada worker.
        
        1. Espera una tarea de la cola
        2. La procesa (simula trabajo)
        3. Notifica completion
        4. Repite
        """
        worker = self.workers[worker_id]
        
        while self.running:
            try:
                # Esperar tarea con timeout para poder verificar self.running
                task = await self.queue.get(timeout=0.5)
                
                if task is None:
                    continue
                
                # Marcar worker como procesando
                worker.state = WorkerState.PROCESSING
                worker.current_task = task
                task.mark_started(worker_id)
                
                # Callback de inicio
                if self.on_task_start:
                    try:
                        await self.on_task_start(task, worker_id)
                    except Exception:
                        pass  # No fallar por callback
                
                start_time = asyncio.get_event_loop().time()
                
                try:
                    # ========================================
                    # AQUÍ ES DONDE SE PROCESA LA TAREA
                    # Por ahora simulamos trabajo con sleep
                    # En producción aquí irían las operaciones reales
                    # ========================================
                    await asyncio.sleep(task.processing_time)
                    
                    task.mark_completed()
                    elapsed = asyncio.get_event_loop().time() - start_time
                    
                    # Actualizar stats del worker
                    worker.tasks_completed += 1
                    worker.total_processing_time += elapsed
                    
                    # Callback de completion
                    if self.on_task_complete:
                        try:
                            await self.on_task_complete(task, worker_id, elapsed)
                        except Exception:
                            pass
                    
                except Exception as e:
                    task.mark_failed(str(e))
                    
                    if self.on_task_error:
                        try:
                            await self.on_task_error(task, worker_id, e)
                        except Exception:
                            pass
                
                finally:
                    worker.state = WorkerState.IDLE
                    worker.current_task = None
                    
            except asyncio.CancelledError:
                break
            except Exception:
                # Error inesperado, continuar
                worker.state = WorkerState.IDLE
                worker.current_task = None
        
        worker.state = WorkerState.STOPPED

    def get_worker_status(self) -> list[dict]:
        """Retorna el estado de todos los workers."""
        result = []
        for worker in self.workers.values():
            result.append({
                "id": worker.worker_id,
                "state": worker.state.value,
                "current_task": worker.current_task.task_id if worker.current_task else None,
                "tasks_completed": worker.tasks_completed,
                "avg_time": (
                    worker.total_processing_time / worker.tasks_completed 
                    if worker.tasks_completed > 0 else 0
                )
            })
        return result

    def __repr__(self) -> str:
        return f"WorkerPool({self.name}, workers={self.num_workers}, active={self.active_workers})"
