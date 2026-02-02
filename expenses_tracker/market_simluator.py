import numpy as np

class MarketSimulator:
    def __init__(
        self,
        base_demand=120,
        elasticity=0.08,
        competitor_price=100,
        max_inventory=500
    ):
        self.base_demand = base_demand
        self.elasticity = elasticity
        self.competitor_price = competitor_price
        self.max_inventory = max_inventory
        self.reset()

    def reset(self):
        self.inventory = self.max_inventory
        self.time = 0
        return self._get_state()

    def _get_state(self):
        return {
            "inventory": self.inventory,
            "time": self.time,
            "competitor_price": self.competitor_price
        }

    def step(self, price):
        # demand calculation
        demand = (
            self.base_demand
            * np.exp(-self.elasticity * (price - self.competitor_price))
        )

        noise = np.random.uniform(0.8, 1.2)
        demand = int(demand * noise)

        units_sold = min(demand, self.inventory)
        revenue = units_sold * price

        self.inventory -= units_sold
        self.time += 1

        done = self.inventory <= 0 or self.time >= 50

        info = {
            "demand": demand,
            "units_sold": units_sold,
            "revenue": revenue
        }

        return self._get_state(), revenue, done, info
