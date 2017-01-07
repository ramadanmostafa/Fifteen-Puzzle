"""
Cookie Clicker Simulator
"""

import simpleplot
import math

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self.__total_cookies__ = 0.0
        self.__current_cookies__ = 0.0
        self.__time__ = 0.0
        self.__cps__ = 1.0
        self.__history__ = [(0.0, None, 0.0, 0.0)] #(time, item, cost of item, total cookies)
        
    def __str__(self):
        """
        Return human readable state
        """
        return "total cookies:"+str(self.__total_cookies__)+" current cookies:"+str(self.__current_cookies__)+" time:"+str(self.get_time())+" cps:"+str(self.get_cps())+"\n history :"+ str(len(self.__history__))
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self.__current_cookies__
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self.__cps__
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self.__time__
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return list(self.__history__)

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if self.__current_cookies__ >= cookies:
            return 0.0
        return math.ceil( ( cookies - self.__current_cookies__ ) / self.__cps__)
        
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time <= 0.0 :
            return
        self.__time__ += time
        tmp = time * self.__cps__
        self.__total_cookies__ += tmp
        self.__current_cookies__ += tmp
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if cost > self.__current_cookies__:
            return
        self.__current_cookies__ -= cost
        self.__cps__ += additional_cps
        #(time, item, cost of item, total cookies)
        item = (self.__time__,item_name,cost,self.__total_cookies__)
        self.__history__.append(item)
        
    def tick(self):
        """
        update amount of cookies every sec by cps
        """
        self.__current_cookies__ += self.__cps__
        self.__total_cookies__ += self.__cps__
        self.__time__ += 1
        
   
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a 
    object corresponding to the final state of the game.
    """
    state = ClickerState()
    build_info2 = build_info.clone()
    while state.get_time() <= duration:
        item_name = strategy(state.get_cookies(),state.get_cps(),state.get_history(),duration - state.get_time(),build_info2)
        if item_name == None :
            break
        cost_cookies = build_info2.get_cost(item_name)
        time_expected = state.time_until(cost_cookies)
        if time_expected + state.get_time() > duration :
            break
        state.wait(time_expected)
        state.buy_item(item_name, cost_cookies, build_info2.get_cps(item_name))
        build_info2.update_item(item_name)
    
    time_still = duration - state.get_time()
    while  time_still > 0:
        state.tick()
        time_still -= 1
        
    return state
        
def classify(lst):
    """
    take a lst of #(time, item, cost of item, total cookies) and return 
    a dict (item ,count)
    """
    result = {None:1000000,"Cursor": 0,
                          "Grandma": 0,
                          "Farm": 0,
                          "Factory": 0,
                          "Mine": 0,
                          "Shipment": 0,
                          "Alchemy Lab": 0,
                          "Portal": 0,
                          "Time Machine": 0,
                          "Antimatter Condenser": 0}
    for item in lst:
        result[item[1]] += 1    
    return result
        


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
    items = build_info.build_items()
    min_item = ("",float("inf"))
    for item in items:
        if build_info.get_cost(item) < min_item[1]:
            min_item = (item,build_info.get_cost(item) )
    if min_item[1] <= (cookies + cps * time_left):
        return min_item[0]
    return None

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    items = build_info.build_items()
    max_item = (None,float("-inf"))
    for item in items:
        if build_info.get_cost(item) > max_item[1] and build_info.get_cost(item)<= (cookies + cps * time_left):
            max_item = (item,build_info.get_cost(item) )
    return max_item[0]

def min_count(dct):
    """
    take a dictionarry and return the key of the smallest value
    """
    result_key = None
    min_value = 100000
    for key,value in dct.items():
        if value <= min_value:
            min_value = value
            result_key = key
    return result_key

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    #(time, item, cost of item, total cookies)
    items_count = classify(history)
    cheapest_item = strategy_cheap(cookies, cps, history, time_left, build_info)
    if items_count[cheapest_item] <= 20:
        return cheapest_item
    else:
        result = min_count(items_count)
        if build_info.get_cost(result) <= cookies + cps * time_left:
            return result
        else:
            return strategy_expensive(cookies, cps, history, time_left, build_info)
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    #run_strategy("Cursor", 100, strategy_cursor_broken)
      
    # Add calls to run_strategy to run additional strategies
    # run_strategy("Cheap", SIM_TIME, strategy_cheap)
    # run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    
run()
    

