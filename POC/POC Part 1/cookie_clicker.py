"""
Cookie Clicker Simulator
"""

import simpleplot

# Used to increase the timeout, if necessary
import codeskulptor, math
codeskulptor.set_timeout(4)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0


class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._total_cookies = 0.0
        self._current_cookies = 0
        self._current_time = 0.0
        self._cps = 1.0
        self._item = None
        self._cost = 0.0
        self._lst = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        return "Time: " + str(self._current_time) + " Current Cookies: " + str(self._current_cookies) + " CPS: " + str(self._cps) + " Total Cookies: " + str(self._total_cookies)
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return self._lst

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if cookies <= self._current_cookies:
            return 0.0
        else:
            return float((cookies - self._current_cookies) / self._cps)
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time >= 0.0:    
            self._current_time += time
            self._current_cookies += (self._cps * time)
            self._total_cookies += (self._cps * time)
        
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self._current_cookies >= cost:
            self._current_cookies -= cost
            self._cps += additional_cps
            self._item = item_name
            self._cost = cost
            self._lst.append((self._current_time, self._item, self._cost, self._total_cookies))


def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """
    obj_bi = build_info

    obj_cs = ClickerState()
    
    while obj_cs.get_time() <= duration:
        
        #print obj_cs.get_time()
        
        if obj_cs.get_time() > duration: # step 1
            break
        
        time_left = duration - obj_cs.get_time()
        strat = strategy(obj_cs.get_cookies(), obj_cs.get_cps(), obj_cs.get_history(),
                     time_left, build_info) # step 2.a
        
        if strat == None: # step 2.b
            obj_cs.wait(duration)
            break
        
        time_elapse = obj_cs.time_until(obj_bi.get_cost(strat)) # step 3.a    
        #print time_elapse, obj_cs.get_time(), time_left

        if (time_elapse + obj_cs.get_time()) > duration: #step 3.b
            obj_cs.wait((time_left))
            break    
        
        obj_cs.wait(math.ceil(time_elapse)) #step 4
        
        obj_cs.buy_item(strat, obj_bi.get_cost(strat), obj_bi.get_cps(strat)) # step 5, 6
        obj_bi.update_item(strat)
        
    # Replace with your code
    print (obj_cs.get_history())
    return obj_cs


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"


def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None


def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    obj_bi = build_info
    obj_cs = ClickerState()
    
    lowest_price = float('inf')
    for item in obj_bi.build_items():
        if obj_bi.get_cost(item) < lowest_price:
            lowest_price = obj_bi.get_cost(item)
            cheapest_item = item
    
    obj_cs.wait(time_left)
    cookies = obj_cs.get_cookies()    
    
    if cookies < lowest_price:
        return None
    return cheapest_item


def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    obj_bi = build_info
    obj_cs = ClickerState()
    obj_cs.wait(time_left)
    cookies += obj_cs.get_cookies()    

    highest_price = float('-inf')
    for item in obj_bi.build_items():
        
        print obj_bi.get_cost(item), cookies, highest_price
        
        if obj_bi.get_cost(item) > highest_price:
            if obj_bi.get_cost(item) <= cookies:
                highest_price = obj_bi.get_cost(item)
                most_expensive_item = item
    
    
    if highest_price == float('-inf'):
        return None
    #if cookies > highest_price:
        #return None
    return most_expensive_item


def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    return None


def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    history = state.get_history()
    history = [(item[0], item[3]) for item in history]
    simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

    
def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)

    # Add calls to run_strategy to run additional strategies
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    
#run()
