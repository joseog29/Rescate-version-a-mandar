from typing import List, Dict, Optional

class Tarea:
    def __init__(self, id: str, descripcion: str, duracion: int, dependencias: Optional[List[str]] = None):
        self.id = id
        self.descripcion = descripcion
        self.duracion = duracion
        self.dependencias = dependencias or []
        self.empezar = None
        self.terminar = None
        self.tecnicos_asignados = 0

class Tecnico:
    def __init__(self, id: int):
        self.id = id
        self.disponible_en = 0

class CPM:
    def __init__(self, tiempo_total: int, tecnicos: int):
        self.tiempo_total = tiempo_total
        self.tareas: Dict[str, Tarea] = {}
        self.tecnicos = [Tecnico(i) for i in range(tecnicos)]

    def add_tarea(self, tarea: Tarea):
        self.tareas[tarea.id] = tarea

    def programa(self):
        programadas = set()
        tiempo_actual = 0
        while len(programadas) < len(self.tareas):
            for tarea in self.tareas.values():
                if tarea.id in programadas:
                    continue
                if all(dep in programadas for dep in tarea.dependencias):
                    # Resource constraints
                    if tarea.id in ['E', 'F']:
                        # Only one server recovery at a time
                        if any(t.id in ['E', 'F'] and t.empezar is not None and t.terminar > tiempo_actual for t in self.tareas.values()):
                            continue
                    # Assign technicians
                    needed = min(1, 1 if tarea.id in ['E', 'F'] else 3)
                    tecnicos_disponibles = [t for t in self.tecnicos if t.disponible_en <= tiempo_actual]
                    if len(tecnicos_disponibles) < needed:
                        continue
                    for tecnico in tecnicos_disponibles[:needed]:
                        tecnico.disponible_en = tiempo_actual + tarea.duracion
                    tarea.tecnicos_asignados = needed
                    tarea.empezar = tiempo_actual
                    tarea.terminar = tiempo_actual + tarea.duracion
                    programadas.add(tarea.id)
            tiempo_actual += 1

    def print_schedule(self):
        print("Objetivo del Proyecto: Rescatar los datos críticos en 120 minutos antes del reinicio del sistema.")
        print("\nCronograma y dependencias:")
        for task in sorted(self.tareas.values(), key=lambda t: t.empezar or 0):
            print(f"Tarea {task.id}: {task.descripcion}")
            print(f"  Inicio: {task.empezar} min, Fin: {task.terminar} min, Técnicos asignados: {task.tecnicos_asignados}")
            print(f"  Depende de: {', '.join(task.dependencias) if task.dependencias else 'Ninguna'}\n")
        print("Nivelación de recursos: Uso óptimo de 3 técnicos, recuperación de servidores secuencial.")
        print("Comunicación de crisis: Informe preliminar, comunicación a clientes, coordinación legal y plan de contingencia tras validación de datos.")

def main():
    project = CPM(tiempo_total=120, tecnicos=3)
    project.add_tarea(Tarea('A', 'Identificar servidores afectados', 15))
    project.add_tarea(Tarea('B', 'Priorizar datos críticos', 20))
    project.add_tarea(Tarea('C', 'Activar protocolo de recuperación', 10, ['A']))
    project.add_tarea(Tarea('D', 'Asignar técnicos a servidores', 5, ['B']))
    project.add_tarea(Tarea('E', 'Recuperar datos de servidor 1', 30, ['D']))
    project.add_tarea(Tarea('F', 'Recuperar datos de servidor 2', 25, ['E']))
    project.add_tarea(Tarea('G', 'Validar integridad de datos recuperados', 15, ['E', 'F']))
    project.add_tarea(Tarea('I', 'Comunicar a clientes afectados', 20, ['G']))
    project.add_tarea(Tarea('J', 'Coordinar con equipo legal', 15, ['G']))
    project.add_tarea(Tarea('K', 'Preparar plan de contingencia', 25, ['G']))
    project.add_tarea(Tarea('H', 'Generar informe preliminar para dirección', 10, ['J']))
    project.programa()
    project.print_schedule()

if __name__ == "__main__":
    main()