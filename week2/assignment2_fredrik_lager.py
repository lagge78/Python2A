from abc import ABC, abstractmethod

class HasWeight(ABC):
    @property
    @abstractmethod
    def weight(self) -> int:
        pass

class Astronaut(HasWeight):
    def __init__(self, weight: int):
        if weight < 50 or weight > 95:
            raise ValueError("The astronaut's weight should be between 50 and 95")
        self._weight = weight

    @property
    def weight(self) -> int:
        return self._weight

class Propellant(HasWeight):
    @property
    @abstractmethod
    def efficiency(self) -> int:
        pass

    @property
    @abstractmethod
    def environmental_impact(self) -> int:
        pass

class AmmoniumDinitramide(Propellant):
    def __init__(self, weight: int):
        if weight < 1 or weight > 200:
            raise ValueError("The weight of the AmmoniumDinitramide should be between 1 and 200")
        self._weight = weight

    @property
    def weight(self) -> int:
        return self._weight

    @property
    def efficiency(self) -> int:
        return 3

    @property
    def environmental_impact(self) -> int:
        return 3

class Hydrazine(Propellant):
    def __init__(self, weight: int):
        if weight < 1 or weight > 200:
            raise ValueError("The weight of the Hydrazine should be between 1 and 200")
        self._weight = weight

    @property
    def weight(self) -> int:
        return self._weight

    @property
    def efficiency(self) -> int:
        return 10

    @property
    def environmental_impact(self) -> int:
        return 20

class Rocket(HasWeight):
    def __init__(self, initial_weight: int, max_weight: int):
        if initial_weight <= 0 or max_weight < initial_weight:
            raise ValueError("Initial weight can't be greater than max weight")
        self._weight = initial_weight
        self._max_weight = max_weight
        self._impact = 0
        self._capacity = 0

    @property
    def weight(self) -> int:
        return self._weight

    @property
    def max_weight(self) -> int:
        return self._max_weight

    def add_astronaut(self, astronaut: Astronaut):
        self._weight += astronaut.weight

    def add_propellant(self, propellant: Propellant):
        self._weight += propellant.weight
        self._capacity += propellant.efficiency * propellant.weight
        self._impact += propellant.environmental_impact * propellant.weight

    def launch(self):
        if self._weight <= min(self._max_weight, self._capacity):
            return self._impact

def create_rocket(astronauts):
    rocket = Rocket(500, 1000)
    for a in astronauts:
        rocket.add_astronaut(a)
    return rocket

def calculate_optimal(astronauts):
    """Minimize hydrazine"""
    rocket = create_rocket(astronauts)
    max_propellant_weight = rocket.max_weight - rocket.weight
    for hydrazine in range(1, max_propellant_weight + 1):
        for ammoniumDinitramide in range(1, max_propellant_weight - hydrazine + 1):
            rocket.add_propellant(AmmoniumDinitramide(ammoniumDinitramide))
            rocket.add_propellant(Hydrazine(hydrazine))
            impact = rocket.launch()
            if impact:
                return {
                    "impact": impact,
                    "ammoniumDinitramide": ammoniumDinitramide,
                    "hydrazine": hydrazine,
                }
            rocket = create_rocket(astronauts)

def main():
    print("Astronauts total weight 320 kg:")
    print(calculate_optimal([Astronaut(80) for _ in range(4)]))

    print("Astronauts total weight 350 kg:")
    print(calculate_optimal([Astronaut(86 + i) for i in range(4)]))

if __name__ == "__main__":
    main()
