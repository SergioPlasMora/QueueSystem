"""
Métricas en memoria para monitoreo del sistema de colas.
"""

from dataclasses import dataclass, field
from collections import deque
import time


@dataclass
class QueueMetrics:
    """
    Métricas agregadas del sistema de colas.
    
    Mantiene contadores y un historial reciente para calcular
    promedios y tasas.
    """
    
    # Contadores globales
    tasks_enqueued: int = 0
    tasks_completed: int = 0
    tasks_failed: int = 0
    tasks_rejected: int = 0  # Rechazadas por cola llena
    
    # Tiempos acumulados
    total_wait_time: float = 0.0       # Tiempo total en cola
    total_processing_time: float = 0.0  # Tiempo total de procesamiento
    
    # Historial reciente (últimas N tareas)
    _recent_wait_times: deque = field(default_factory=lambda: deque(maxlen=100))
    _recent_processing_times: deque = field(default_factory=lambda: deque(maxlen=100))
    
    # Stats por prioridad
    tasks_by_priority: dict = field(default_factory=lambda: {0: 0, 1: 0, 2: 0, 3: 0})
    
    # Stats por worker
    tasks_by_worker: dict = field(default_factory=dict)
    
    # Timestamp de inicio
    started_at: float = field(default_factory=time.time)

    def record_enqueued(self, priority: int):
        """Registra una tarea encolada."""
        self.tasks_enqueued += 1
        self.tasks_by_priority[priority] = self.tasks_by_priority.get(priority, 0) + 1

    def record_completed(self, worker_id: str, wait_time: float, processing_time: float):
        """Registra una tarea completada."""
        self.tasks_completed += 1
        self.total_wait_time += wait_time
        self.total_processing_time += processing_time
        
        self._recent_wait_times.append(wait_time)
        self._recent_processing_times.append(processing_time)
        
        self.tasks_by_worker[worker_id] = self.tasks_by_worker.get(worker_id, 0) + 1

    def record_failed(self, worker_id: str):
        """Registra una tarea fallida."""
        self.tasks_failed += 1

    def record_rejected(self):
        """Registra una tarea rechazada por cola llena."""
        self.tasks_rejected += 1

    @property
    def avg_wait_time(self) -> float:
        """Tiempo promedio de espera (últimas 100 tareas)."""
        if not self._recent_wait_times:
            return 0.0
        return sum(self._recent_wait_times) / len(self._recent_wait_times)

    @property
    def avg_processing_time(self) -> float:
        """Tiempo promedio de procesamiento (últimas 100 tareas)."""
        if not self._recent_processing_times:
            return 0.0
        return sum(self._recent_processing_times) / len(self._recent_processing_times)

    @property
    def throughput(self) -> float:
        """Tareas completadas por segundo desde el inicio."""
        elapsed = time.time() - self.started_at
        if elapsed <= 0:
            return 0.0
        return self.tasks_completed / elapsed

    @property
    def success_rate(self) -> float:
        """Tasa de éxito (0.0 - 1.0)."""
        total = self.tasks_completed + self.tasks_failed
        if total == 0:
            return 1.0
        return self.tasks_completed / total

    @property
    def pending_tasks(self) -> int:
        """Tareas encoladas menos completadas/fallidas."""
        return self.tasks_enqueued - self.tasks_completed - self.tasks_failed

    @property
    def uptime_seconds(self) -> float:
        """Segundos desde el inicio."""
        return time.time() - self.started_at

    def reset(self):
        """Reinicia todas las métricas."""
        self.tasks_enqueued = 0
        self.tasks_completed = 0
        self.tasks_failed = 0
        self.tasks_rejected = 0
        self.total_wait_time = 0.0
        self.total_processing_time = 0.0
        self._recent_wait_times.clear()
        self._recent_processing_times.clear()
        self.tasks_by_priority = {0: 0, 1: 0, 2: 0, 3: 0}
        self.tasks_by_worker.clear()
        self.started_at = time.time()

    def to_dict(self) -> dict:
        """Exporta métricas como diccionario."""
        return {
            "tasks_enqueued": self.tasks_enqueued,
            "tasks_completed": self.tasks_completed,
            "tasks_failed": self.tasks_failed,
            "tasks_rejected": self.tasks_rejected,
            "pending_tasks": self.pending_tasks,
            "avg_wait_time": round(self.avg_wait_time, 3),
            "avg_processing_time": round(self.avg_processing_time, 3),
            "throughput": round(self.throughput, 2),
            "success_rate": round(self.success_rate * 100, 1),
            "uptime_seconds": round(self.uptime_seconds, 1),
            "tasks_by_priority": self.tasks_by_priority,
            "tasks_by_worker": self.tasks_by_worker,
        }

    def __repr__(self) -> str:
        return f"QueueMetrics(completed={self.tasks_completed}, failed={self.tasks_failed}, throughput={self.throughput:.2f}/s)"
