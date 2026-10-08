import search

class CRSproblem(search.Problem):

    def __init__(self):
        self.initial = None
        self.S = None
        self.N = None
        self.tasks = []

    def load(self, fh):
        """Loads a problem from the opened file object fh."""
        lines = (
            line.strip()
            for line in fh
            if line.strip() and not line.startswith("#")
        )

        try:
            header = next(lines).split()
        except StopIteration as exc:
            raise ValueError("O ficheiro não contem o cabeçalho S N") from exc

        if len(header) != 2:
            raise ValueError("O cabeçalho deve conter exatamente S e N")

        try:
            cores, task_count = map(int, header)
        except ValueError as exc:
            raise ValueError("S e N devem ser inteiros") from exc

        if cores <= 0 or task_count < 0:
            raise ValueError("S deve ser positivo e N não pode ser negativo")

        tasks = []
        for index in range(task_count):
            try:
                values = next(lines).split()
            except StopIteration as exc:
                raise ValueError(f"Falta a tarefa {index}") from exc

            if len(values) != 4:
                raise ValueError(f"A tarefa {index} deve conter a, p, s e w")

            try:
                arrival, processing, size, weight = map(int, values)
            except ValueError as exc:
                raise ValueError(f"A tarefa {index} deve conter inteiros") from exc

            if arrival < 0 or processing <= 0 or size < 1 or size > cores or weight <= 0:
                raise ValueError(f"A tarefa {index} tem valores inválidos")

            tasks.append((arrival, processing, size, weight))

        if next(lines, None) is not None:
            raise ValueError("O ficheiro contem mais tarefas do que N")

        self.S = cores
        self.N = task_count
        self.tasks = tasks

    def cost(self, sol):
        """Compute cost of solution sol."""
        total = 0
        for index, (arrival, processing, _size, weight) in enumerate(self.tasks):
            start_time, _start_core = sol[index]
            completion = start_time + processing
            total += weight * (completion - arrival)
        return total

    def check(self, sol):
        """Checks if solution sol satisfies problem constraints."""
        if not isinstance(sol, (list, tuple)) or len(sol) != self.N:
            return False

        for index, placement in enumerate(sol):
            if not isinstance(placement, (list, tuple)) or len(placement) != 2:
                return False

            start_time, start_core = placement
            if not isinstance(start_time, int) or not isinstance(start_core, int):
                return False

            arrival, processing, size, _weight = self.tasks[index]
            if start_time < arrival or start_core < 0 or start_core + size > self.S:
                return False

            for previous in range(index):
                previous_time, previous_core = sol[previous]
                _arrival, previous_processing, previous_size, _weight = self.tasks[previous]

                times_overlap = (
                    start_time < previous_time + previous_processing
                    and previous_time < start_time + processing
                )
                cores_overlap = (
                    start_core < previous_core + previous_size
                    and previous_core < start_core + size
                )
                if times_overlap and cores_overlap:
                    return False

        return True
