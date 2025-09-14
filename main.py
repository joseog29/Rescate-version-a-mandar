from typing import List, Dict, Optional

class Task:
    def __init__(self, id: str, description: str, duration: int, dependencies: Optional[List[str]] = None):
        self.id = id
        self.description = description
        self.duration = duration
        self.dependencies = dependencies or []
        self.start_time = None
        self.end_time = None
        self.assigned_technicians = 0

class Technician:
    def __init__(self, id: int):
        self.id = id
        self.available_at = 0

class CPMProject:
    def __init__(self, total_time: int, technicians: int):
        self.total_time = total_time
        self.tasks: Dict[str, Task] = {}
        self.technicians = [Technician(i) for i in range(technicians)]

    def add_task(self, task: Task):
        self.tasks[task.id] = task

    def schedule(self):
        scheduled = set()
        current_time = 0
        while len(scheduled) < len(self.tasks):
            for task in self.tasks.values():
                if task.id in scheduled:
                    continue
                if all(dep in scheduled for dep in task.dependencies):
                    # Resource constraints
                    if task.id in ['E', 'F']:
                        # Only one server recovery at a time
                        if any(t.id in ['E', 'F'] and t.start_time is not None and t.end_time > current_time for t in self.tasks.values()):
                            continue
                    # Assign technicians
                    needed = min(3, 1 if task.id in ['E', 'F'] else 3)
                    available_techs = [t for t in self.technicians if t.available_at <= current_time]
                    if len(available_techs) < needed:
                        continue
                    for tech in available_techs[:needed]:
                        tech.available_at = current_time + task.duration
                    task.assigned_technicians = needed
                    task.start_time = current_time
                    task.end_time = current_time + task.duration
                    scheduled.add(task.id)
            current_time += 1

    def print_schedule(self):
        print("Objetivo del Proyecto: Rescatar los datos críticos en 120 minutos antes del reinicio del sistema.")
        print("\nCronograma y dependencias:")
        for task in sorted(self.tasks.values(), key=lambda t: t.start_time or 0):
            print(f"Tarea {task.id}: {task.description}")
            print(f"  Inicio: {task.start_time} min, Fin: {task.end_time} min, Técnicos asignados: {task.assigned_technicians}")
            print(f"  Depende de: {', '.join(task.dependencies) if task.dependencies else 'Ninguna'}\n")
        print("Nivelación de recursos: Uso óptimo de 3 técnicos, recuperación de servidores secuencial.")
        print("Comunicación de crisis: Informe preliminar, comunicación a clientes, coordinación legal y plan de contingencia tras validación de datos.")

def main():
    project = CPMProject(total_time=120, technicians=3)
    project.add_task(Task('A', 'Identificar servidores afectados', 15))
    project.add_task(Task('B', 'Priorizar datos críticos', 20, ['A']))
    project.add_task(Task('C', 'Activar protocolo de recuperación', 10, ['B']))
    project.add_task(Task('D', 'Asignar técnicos a servidores', 5, ['C']))
    project.add_task(Task('E', 'Recuperar datos de servidor 1', 30, ['D']))
    project.add_task(Task('F', 'Recuperar datos de servidor 2', 25, ['D', 'E']))
    project.add_task(Task('G', 'Validar integridad de datos recuperados', 15, ['E', 'F']))
    project.add_task(Task('H', 'Generar informe preliminar para dirección', 10, ['G']))
    project.add_task(Task('I', 'Comunicar a clientes afectados', 20, ['G']))
    project.add_task(Task('J', 'Coordinar con equipo legal', 15, ['G']))
    project.add_task(Task('K', 'Preparar plan de contingencia', 25, ['G']))
    project.schedule()
    project.print_schedule()

if __name__ == "__main__":
    main()