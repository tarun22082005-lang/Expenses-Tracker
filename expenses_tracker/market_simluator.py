import numpy as np
class MarketSimulator:
    """
    Simple market simulation for testing pricing strategies.
    """

    def __init__(
        self,
        base_demand=120,
        price_elasticity=0.08,
        competitor_price=100,
        max_inventory=500
    ):

        
        self.base_demand = base_demand
        self.price_elasticity = price_elasticity
        self.competitor_price = competitor_price
        self.max_inventory = max_inventory

        
        self.reset()
        
    def reset(self):
        self.inventory = self.max_inventory
        self.current_step = 0

        return self.get_state()

    def get_state(self):

        state = {
            "inventory": self.inventory,
            "step": self.current_step,
            "competitor_price": self.competitor_price
        }

        return state

    def step(self, price):
        """
        Simulate one time step using given price.
        """
        expected_demand = self.base_demand * np.exp(
            -self.price_elasticity * (price - self.competitor_price)
        )        
        random_factor = np.random.uniform(0.8, 1.2)
        demand = int(expected_demand * random_factor)
        units_sold = min(demand, self.inventory)        
        revenue = units_sold * price        
        self.inventory -= units_sold
        self.current_step += 1        
        done = self.inventory <= 0 or self.current_step >= 50
        info = {
            "demand": demand,
            "units_sold": units_sold,
            "revenue": revenue
        }

        return self.get_state(), revenue, done, info
