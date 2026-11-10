import search

class CRSproblem(search.Problem):

    def __init__(self):
        self.initial = None
        self.S = None
        self.N = None
        self.tasks = []


    def result(self, state, action):
        """Returns the state that results from executing the given action
        in the given state"""
        i, u, v = action
        new_state_list = list(state)
        try:
            new_state_list[i] = (u, v)
        except IndexError as exc:
            raise IndexError("i da ação deve estar dentro do tamanho do state") from exc
        return tuple(new_state_list)
    
    def actionCabe(self, state, i,u,v):
        a, p, s, w = self.tasks[i]
        for j in range(self.N):
            if state[j] != (-1, -1):
                uj,vj = state[j]
                pj,sj = self.tasks[j][1], self.tasks[j][2]
                
                if( u<uj+pj and uj < u + p and v < vj + sj and vj < v + s):
                    return False
        return True    

    def actions(self, state):
        actions = []
        agendadas = [
            (j, state[j][0], state[j][1])
            for j in range(self.N)
            if state[j] != (-1, -1)
        ]
        tarefas_iguais = set()

        for i in range(self.N):
            if state[i] != (-1, -1):
                continue

            a, p, s, w = self.tasks[i]
            tarefa = (a, p, s, w)
            if tarefa in tarefas_iguais:
                continue
            tarefas_iguais.add(tarefa)

            tempos = {a}
            for j, uj, vj in agendadas:
                fim = uj + self.tasks[j][1]
                if fim >= a:
                    tempos.add(fim)

            for u in sorted(tempos):
                ativas = [
                    (vj, vj + self.tasks[j][2])
                    for j, uj, vj in agendadas
                    if u < uj + self.tasks[j][1] and uj < u + p
                ]
                cores = {0}
                for inicio, fim in ativas:
                    cores.add(fim)

                acoes_u = []
                for v in sorted(cores):
                    if v + s > self.S:
                        continue
                    if all(v + s <= inicio or fim <= v for inicio, fim in ativas):
                        acoes_u.append((i, u, v))

                if acoes_u:
                    actions.extend(acoes_u)
                    break   # só o primeiro instante em que a tarefa cabe

        return actions

    def goal_test(self, state):
        """Returns True if the state is a goal"""
        for s in state:
            if s == (-1, -1): return False
        return True

    def path_cost(self, c, state1, action, state2):
        """Returns the cost of a path that arrives at state2 from state1
        via action, assuming cost c to get up to state1"""
        i, u, v = action
        a, p, _, w = self.tasks[i]
        return c + w * (u + p - a)

    def solve(self):
        """Calls the uninformed search algorithm chosen.
        Returns a solution using the specified format"""
        node = search.uniform_cost_search(self)
        if node is None:
            raise ValueError("não foi encontrada uma solução")
        for s in node.state:
            if s == (-1, -1):
                raise ValueError("solução tem que estar toda preenchida com (u, v), u, v >= 0")
        return list(node.state)


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
        self.initial = ((-1, -1),)*self.N
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
