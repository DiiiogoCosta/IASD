class CRSproblem:
    """Representa um problema de Scheduling de Recursos (CRS)."""

    def __init__(self):
        self.S = None
        self.N = None
        self.tasks = []

    def load(self, fh):
        """Carrega um problema CRS a partir de um ficheiro .dat."""
        lines = (
            line.strip()
            for line in fh
            if line.strip() and not line.startswith("#")
        )

        try:
            header = next(lines).split()
        except StopIteration as exc:
            raise ValueError("O ficheiro não contém o cabeçalho S N") from exc

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

            if arrival < 0 or processing <= 0 or not 1 <= size <= cores or weight <= 0:
                raise ValueError(f"A tarefa {index} tem valores inválidos")

            tasks.append((arrival, processing, size, weight))

        if next(lines, None) is not None:
            raise ValueError("O ficheiro contém mais tarefas do que N")

        self.S = cores
        self.N = task_count
        self.tasks = tasks

    def cost(self, sol):
        """Calcula o custo de uma solução."""
        total = 0
        for index, (arrival, processing, _size, weight) in enumerate(self.tasks):
            start_time, _start_core = sol[index]
            completion = start_time + processing
            total += weight * (completion - arrival)
        return total

    def check(self, sol):
        """Verifica se uma solução é válida."""
        if not isinstance(sol, (list, tuple)) or len(sol) != self.N:
            """Verifica se a solução é uma lista ou tupla com o tamanho correto (Se a solução tem N elementos)."""
            return False

        for index, placement in enumerate(sol):
            if not isinstance(placement, (list, tuple)) or len(placement) != 2:
                """Verifica se cada elemento da solução é uma lista ou tupla com exatamente dois elementos (start_time, start_core)."""
                return False

            start_time, start_core = placement
            if not isinstance(start_time, int) or not isinstance(start_core, int):
                """Verifica se start_time e start_core são inteiros."""
                return False

            arrival, processing, size, _weight = self.tasks[index]
            if start_time < arrival or start_core < 0 or start_core + size > self.S:
                """Verifica se start_time é maior ou igual a arrival, start_core é não-negativo e start_core + size não excede o número total de núcleos S."""
                return False

            for previous in range(index):
                """Verifica se a tarefa atual não sobrepõe no tempo e nos núcleos com tarefas anteriores."""
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
