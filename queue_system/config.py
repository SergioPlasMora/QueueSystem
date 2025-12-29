"""
Cargador de configuración desde YAML.

Lee config.yml y proporciona acceso tipado a todos los parámetros.
"""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
import yaml


@dataclass
class WorkersConfig:
    """Configuración de workers."""
    dataset: int = 4
    command: int = 2


@dataclass
class QueueConfig:
    """Configuración de una cola individual."""
    max_size: int = 100


@dataclass
class QueuesConfig:
    """Configuración de colas."""
    dataset: QueueConfig = field(default_factory=lambda: QueueConfig(max_size=100))
    command: QueueConfig = field(default_factory=lambda: QueueConfig(max_size=50))


@dataclass
class TimeoutsConfig:
    """Configuración de timeouts."""
    worker_poll: float = 0.5
    shutdown: float = 5.0
    enqueue: float = 0


@dataclass
class ProcessingConfig:
    """Configuración de procesamiento."""
    default_dataset_time: float = 1.0
    default_command_time: float = 0.1


@dataclass
class PrioritiesConfig:
    """Configuración de prioridades por defecto."""
    default_dataset: int = 2  # NORMAL
    default_command: int = 1  # HIGH


@dataclass
class MetricsConfig:
    """Configuración de métricas."""
    history_size: int = 100
    log_events: bool = True


@dataclass
class FloodConfig:
    """Configuración para comando flood."""
    min_time: float = 0.3
    max_time: float = 2.0


@dataclass
class CLIConfig:
    """Configuración del CLI."""
    rich_output: bool = True
    auto_start: bool = False
    flood: FloodConfig = field(default_factory=FloodConfig)


@dataclass
class Config:
    """Configuración completa del sistema."""
    workers: WorkersConfig = field(default_factory=WorkersConfig)
    queues: QueuesConfig = field(default_factory=QueuesConfig)
    timeouts: TimeoutsConfig = field(default_factory=TimeoutsConfig)
    processing: ProcessingConfig = field(default_factory=ProcessingConfig)
    priorities: PrioritiesConfig = field(default_factory=PrioritiesConfig)
    metrics: MetricsConfig = field(default_factory=MetricsConfig)
    cli: CLIConfig = field(default_factory=CLIConfig)
    
    @classmethod
    def load(cls, config_path: Optional[str] = None) -> "Config":
        """
        Carga configuración desde archivo YAML.
        
        Args:
            config_path: Ruta al archivo config.yml. 
                        Si es None, busca en el directorio del proyecto.
        
        Returns:
            Config con valores del archivo o defaults.
        """
        if config_path is None:
            # Buscar config.yml en el directorio padre del paquete
            package_dir = Path(__file__).parent.parent
            config_path = package_dir / "config.yml"
        else:
            config_path = Path(config_path)
        
        if not config_path.exists():
            print(f"⚠️  Config no encontrada en {config_path}, usando defaults")
            return cls()
        
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
            
            return cls._from_dict(data)
        
        except Exception as e:
            print(f"⚠️  Error leyendo config: {e}, usando defaults")
            return cls()
    
    @classmethod
    def _from_dict(cls, data: dict) -> "Config":
        """Construye Config desde diccionario."""
        config = cls()
        
        # Workers
        if "workers" in data:
            w = data["workers"]
            config.workers = WorkersConfig(
                dataset=w.get("dataset", 4),
                command=w.get("command", 2)
            )
        
        # Queues
        if "queues" in data:
            q = data["queues"]
            config.queues = QueuesConfig(
                dataset=QueueConfig(max_size=q.get("dataset", {}).get("max_size", 100)),
                command=QueueConfig(max_size=q.get("command", {}).get("max_size", 50))
            )
        
        # Timeouts
        if "timeouts" in data:
            t = data["timeouts"]
            config.timeouts = TimeoutsConfig(
                worker_poll=t.get("worker_poll", 0.5),
                shutdown=t.get("shutdown", 5.0),
                enqueue=t.get("enqueue", 0)
            )
        
        # Processing
        if "processing" in data:
            p = data["processing"]
            config.processing = ProcessingConfig(
                default_dataset_time=p.get("default_dataset_time", 1.0),
                default_command_time=p.get("default_command_time", 0.1)
            )
        
        # Priorities
        if "priorities" in data:
            pr = data["priorities"]
            config.priorities = PrioritiesConfig(
                default_dataset=pr.get("default_dataset", 2),
                default_command=pr.get("default_command", 1)
            )
        
        # Metrics
        if "metrics" in data:
            m = data["metrics"]
            config.metrics = MetricsConfig(
                history_size=m.get("history_size", 100),
                log_events=m.get("log_events", True)
            )
        
        # CLI
        if "cli" in data:
            c = data["cli"]
            flood_data = c.get("flood", {})
            config.cli = CLIConfig(
                rich_output=c.get("rich_output", True),
                auto_start=c.get("auto_start", False),
                flood=FloodConfig(
                    min_time=flood_data.get("min_time", 0.3),
                    max_time=flood_data.get("max_time", 2.0)
                )
            )
        
        return config
    
    def __repr__(self) -> str:
        return (
            f"Config(\n"
            f"  workers: dataset={self.workers.dataset}, command={self.workers.command}\n"
            f"  queues: dataset={self.queues.dataset.max_size}, command={self.queues.command.max_size}\n"
            f"  timeouts: poll={self.timeouts.worker_poll}s, shutdown={self.timeouts.shutdown}s\n"
            f")"
        )


# Singleton global para acceso fácil
_config: Optional[Config] = None


def get_config() -> Config:
    """Obtiene la configuración global (singleton)."""
    global _config
    if _config is None:
        _config = Config.load()
    return _config


def reload_config(config_path: Optional[str] = None) -> Config:
    """Recarga la configuración desde archivo."""
    global _config
    _config = Config.load(config_path)
    return _config
