"""
Cola con prioridades usando heapq.

heapq implementa un min-heap, donde el elemento más pequeño 
siempre está en la posición 0. Combinado con Task(order=True),
las tareas con menor prioridad (más urgentes) se procesan primero.
"""

import asyncio
import heapq
from typing import Optional
from .task import Task


class PriorityQueue:
    """
    Cola asíncrona con prioridades.
    
    Usa heapq internamente para mantener las tareas ordenadas.
    Thread-safe mediante asyncio.Lock.
    
    Ejemplo:
        queue = PriorityQueue(maxsize=100)
        await queue.put(Task(priority=TaskPriority.HIGH, name="urgente"))
        await queue.put(Task(priority=TaskPriority.LOW, name="puede esperar"))
        
        task = await queue.get()  # Retorna "urgente" primero
    """

    def __init__(self, maxsize: int = 100):
        """
        Args:
            maxsize: Tamaño máximo de la cola. 0 = sin límite.
        """
        self._heap: list[Task] = []
        self._maxsize = maxsize
        self._lock = asyncio.Lock()
        self._not_empty = asyncio.Event()
        self._not_full = asyncio.Event()
        self._not_full.set()  # Inicialmente no está llena

    @property
    def qsize(self) -> int:
        """Tamaño actual de la cola."""
        return len(self._heap)

    @property
    def maxsize(self) -> int:
        """Tamaño máximo de la cola."""
        return self._maxsize

    @property
    def is_empty(self) -> bool:
        """True si la cola está vacía."""
        return len(self._heap) == 0

    @property
    def is_full(self) -> bool:
        """True si la cola está llena."""
        return self._maxsize > 0 and len(self._heap) >= self._maxsize

    @property
    def fill_ratio(self) -> float:
        """Porcentaje de llenado (0.0 - 1.0)."""
        if self._maxsize == 0:
            return 0.0
        return len(self._heap) / self._maxsize

    async def put(self, task: Task, block: bool = True, timeout: float = None) -> bool:
        """
        Añade una tarea a la cola.
        
        Args:
            task: Tarea a añadir
            block: Si True, espera cuando la cola está llena
            timeout: Tiempo máximo de espera (None = infinito)
            
        Returns:
            True si se añadió, False si la cola está llena (cuando block=False)
        """
        if self._maxsize > 0:
            if block:
                try:
                    await asyncio.wait_for(self._not_full.wait(), timeout=timeout)
                except asyncio.TimeoutError:
                    return False
            elif self.is_full:
                return False

        async with self._lock:
            if self._maxsize > 0 and len(self._heap) >= self._maxsize:
                return False
            
            heapq.heappush(self._heap, task)
            self._not_empty.set()
            
            if self._maxsize > 0 and len(self._heap) >= self._maxsize:
                self._not_full.clear()
            
            return True

    async def get(self, timeout: float = None) -> Optional[Task]:
        """
        Obtiene la tarea de mayor prioridad.
        
        Bloquea hasta que haya una tarea disponible.
        
        Args:
            timeout: Tiempo máximo de espera (None = infinito)
            
        Returns:
            Task o None si timeout
        """
        try:
            await asyncio.wait_for(self._not_empty.wait(), timeout=timeout)
        except asyncio.TimeoutError:
            return None

        async with self._lock:
            if not self._heap:
                return None
            
            task = heapq.heappop(self._heap)
            
            if not self._heap:
                self._not_empty.clear()
            
            if self._maxsize > 0:
                self._not_full.set()
            
            return task

    async def peek(self) -> Optional[Task]:
        """
        Ve la tarea de mayor prioridad sin removerla.
        
        Returns:
            Task o None si la cola está vacía
        """
        async with self._lock:
            if self._heap:
                return self._heap[0]
            return None

    async def clear(self):
        """Vacía la cola."""
        async with self._lock:
            self._heap.clear()
            self._not_empty.clear()
            self._not_full.set()

    def get_all_tasks(self) -> list[Task]:
        """
        Retorna una copia de todas las tareas (para visualización).
        No thread-safe, usar solo para debugging.
        """
        return sorted(self._heap)

    def __len__(self) -> int:
        return len(self._heap)

    def __repr__(self) -> str:
        return f"PriorityQueue(size={self.qsize}/{self.maxsize})"
