"""
Definición de tareas con prioridades para el sistema de colas.

Las tareas se ordenan automáticamente por:
1. Prioridad (menor número = más urgente)
2. Tiempo de creación (FIFO dentro de la misma prioridad)
"""

from enum import IntEnum
from dataclasses import dataclass, field
from typing import Any
import time
import uuid


class TaskPriority(IntEnum):
    """
    Prioridades de tareas.
    Menor número = mayor prioridad (se procesa primero).
    """
    CRITICAL = 0  # Emergencias, comandos del sistema críticos
    HIGH = 1      # Tareas urgentes, usuarios VIP
    NORMAL = 2    # Solicitudes normales
    LOW = 3       # Tareas batch, reportes no urgentes

    def __str__(self) -> str:
        return self.name
    
    @classmethod
    def from_int(cls, value: int) -> "TaskPriority":
        """Convierte un entero a TaskPriority, con validación."""
        if value < 0:
            return cls.CRITICAL
        if value > 3:
            return cls.LOW
        return cls(value)


class TaskType(IntEnum):
    """Tipos de tareas para routing a diferentes colas."""
    DATASET = 1   # Operaciones de datos (pesadas)
    COMMAND = 2   # Comandos del sistema (ligeros)

    def __str__(self) -> str:
        return self.name


@dataclass(order=True)
class Task:
    """
    Tarea con prioridad para la cola.
    
    El decorador @dataclass(order=True) genera automáticamente
    __lt__, __le__, __gt__, __ge__ basándose en los campos con compare=True.
    
    Esto permite que heapq ordene las tareas correctamente.
    """
    # Campos de ordenamiento (compare=True)
    priority: TaskPriority = field(compare=True)
    created_at: float = field(default_factory=time.time, compare=True)
    
    # Campos de datos (compare=False, no afectan el orden)
    task_id: str = field(
        default_factory=lambda: str(uuid.uuid4())[:8], 
        compare=False
    )
    task_type: TaskType = field(default=TaskType.DATASET, compare=False)
    name: str = field(default="", compare=False)
    payload: Any = field(default_factory=dict, compare=False)
    processing_time: float = field(default=1.0, compare=False)
    
    # Estado (para tracking)
    started_at: float | None = field(default=None, compare=False)
    completed_at: float | None = field(default=None, compare=False)
    worker_id: str | None = field(default=None, compare=False)
    error: str | None = field(default=None, compare=False)

    def __post_init__(self):
        """Asegurar que priority sea TaskPriority."""
        if isinstance(self.priority, int):
            self.priority = TaskPriority.from_int(self.priority)

    @property
    def wait_time(self) -> float:
        """Tiempo de espera en cola (segundos)."""
        if self.started_at:
            return self.started_at - self.created_at
        return time.time() - self.created_at

    @property
    def execution_time(self) -> float | None:
        """Tiempo de ejecución (segundos)."""
        if self.started_at and self.completed_at:
            return self.completed_at - self.started_at
        return None

    @property
    def is_completed(self) -> bool:
        return self.completed_at is not None

    @property
    def is_failed(self) -> bool:
        return self.error is not None

    def mark_started(self, worker_id: str):
        """Marca la tarea como iniciada."""
        self.started_at = time.time()
        self.worker_id = worker_id

    def mark_completed(self):
        """Marca la tarea como completada."""
        self.completed_at = time.time()

    def mark_failed(self, error: str):
        """Marca la tarea como fallida."""
        self.completed_at = time.time()
        self.error = error

    def __repr__(self) -> str:
        return f"Task({self.task_id}, {self.name!r}, {self.priority.name})"
