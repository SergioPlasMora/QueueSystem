"""
Gestor central del sistema de colas.

Coordina las colas de datasets y comandos con sus respectivos
pools de workers.
"""

import asyncio
from typing import Callable, Awaitable

from .task import Task, TaskType, TaskPriority
from .priority_queue import PriorityQueue
from .worker_pool import WorkerPool
from .metrics import QueueMetrics


class QueueManager:
    """
    Gestor central del sistema de colas dual.
    
    Maneja dos colas separadas:
    - dataset_queue: Para operaciones de datos (pesadas)
    - command_queue: Para comandos del sistema (ligeros)
    
    Ejemplo:
        manager = QueueManager(dataset_workers=4, command_workers=2)
        
        # Callbacks opcionales
        manager.on_task_complete = my_callback
        
        await manager.start()
        
        # Encolar tareas
        task = Task(priority=TaskPriority.NORMAL, name="test")
        await manager.enqueue(task)
        
        # ... esperar procesamiento ...
        
        await manager.stop()
    """

    def __init__(
        self,
        dataset_workers: int = 4,
        command_workers: int = 2,
        dataset_queue_size: int = 100,
        command_queue_size: int = 50,
    ):
        """
        Args:
            dataset_workers: Número de workers para cola de datasets
            command_workers: Número de workers para cola de comandos
            dataset_queue_size: Tamaño máximo de cola de datasets
            command_queue_size: Tamaño máximo de cola de comandos
        """
        # Colas separadas por tipo
        self.dataset_queue = PriorityQueue(maxsize=dataset_queue_size)
        self.command_queue = PriorityQueue(maxsize=command_queue_size)
        
        # Pools de workers
        self.dataset_pool = WorkerPool(
            num_workers=dataset_workers,
            queue=self.dataset_queue,
            name="Dataset"
        )
        self.command_pool = WorkerPool(
            num_workers=command_workers,
            queue=self.command_queue,
            name="Command"
        )
        
        # Métricas globales
        self.metrics = QueueMetrics()
        
        # Estado
        self.running = False
        
        # Callbacks externos
        self.on_task_start: Callable[[Task, str], Awaitable[None]] | None = None
        self.on_task_complete: Callable[[Task, str, float], Awaitable[None]] | None = None
        self.on_task_error: Callable[[Task, str, Exception], Awaitable[None]] | None = None
        
        # Conectar callbacks internos
        self._setup_callbacks()

    def _setup_callbacks(self):
        """Configura callbacks internos para métricas."""
        
        async def on_start(task: Task, worker_id: str):
            if self.on_task_start:
                await self.on_task_start(task, worker_id)
        
        async def on_complete(task: Task, worker_id: str, elapsed: float):
            self.metrics.record_completed(worker_id, task.wait_time, elapsed)
            if self.on_task_complete:
                await self.on_task_complete(task, worker_id, elapsed)
        
        async def on_error(task: Task, worker_id: str, error: Exception):
            self.metrics.record_failed(worker_id)
            if self.on_task_error:
                await self.on_task_error(task, worker_id, error)
        
        # Asignar a ambos pools
        for pool in [self.dataset_pool, self.command_pool]:
            pool.on_task_start = on_start
            pool.on_task_complete = on_complete
            pool.on_task_error = on_error

    async def start(self):
        """Inicia ambos pools de workers."""
        if self.running:
            return
        
        self.running = True
        await self.dataset_pool.start()
        await self.command_pool.start()

    async def stop(self, wait: bool = True, timeout: float = 5.0):
        """Detiene ambos pools de workers."""
        self.running = False
        await self.dataset_pool.stop(wait=wait, timeout=timeout)
        await self.command_pool.stop(wait=wait, timeout=timeout)

    async def enqueue(self, task: Task) -> bool:
        """
        Encola una tarea en la cola apropiada según su tipo.
        
        Args:
            task: Tarea a encolar
            
        Returns:
            True si se encoló, False si la cola está llena
        """
        if task.task_type == TaskType.DATASET:
            queue = self.dataset_queue
        else:
            queue = self.command_queue
        
        success = await queue.put(task, block=False)
        
        if success:
            self.metrics.record_enqueued(int(task.priority))
        else:
            self.metrics.record_rejected()
        
        return success

    async def enqueue_dataset(
        self,
        name: str,
        priority: TaskPriority = TaskPriority.NORMAL,
        processing_time: float = 1.0,
        payload: dict = None
    ) -> Task | None:
        """
        Crea y encola una tarea de tipo DATASET.
        
        Returns:
            La tarea creada, o None si la cola está llena
        """
        task = Task(
            priority=priority,
            task_type=TaskType.DATASET,
            name=name,
            payload=payload or {},
            processing_time=processing_time
        )
        
        if await self.enqueue(task):
            return task
        return None

    async def enqueue_command(
        self,
        name: str,
        priority: TaskPriority = TaskPriority.HIGH,
        processing_time: float = 0.1,
        payload: dict = None
    ) -> Task | None:
        """
        Crea y encola una tarea de tipo COMMAND.
        
        Returns:
            La tarea creada, o None si la cola está llena
        """
        task = Task(
            priority=priority,
            task_type=TaskType.COMMAND,
            name=name,
            payload=payload or {},
            processing_time=processing_time
        )
        
        if await self.enqueue(task):
            return task
        return None

    def get_status(self) -> dict:
        """Retorna el estado completo del sistema."""
        return {
            "running": self.running,
            "dataset_queue": {
                "size": self.dataset_queue.qsize,
                "maxsize": self.dataset_queue.maxsize,
                "fill_ratio": round(self.dataset_queue.fill_ratio * 100, 1),
            },
            "command_queue": {
                "size": self.command_queue.qsize,
                "maxsize": self.command_queue.maxsize,
                "fill_ratio": round(self.command_queue.fill_ratio * 100, 1),
            },
            "dataset_workers": self.dataset_pool.get_worker_status(),
            "command_workers": self.command_pool.get_worker_status(),
            "metrics": self.metrics.to_dict(),
        }

    def __repr__(self) -> str:
        return (
            f"QueueManager("
            f"datasets={self.dataset_queue.qsize}/{self.dataset_queue.maxsize}, "
            f"commands={self.command_queue.qsize}/{self.command_queue.maxsize})"
        )
