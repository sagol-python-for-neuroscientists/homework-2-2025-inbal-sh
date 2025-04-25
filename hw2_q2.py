from collections import namedtuple
from enum import Enum

Condition = Enum("Condition", ("CURE", "HEALTHY", "SICK", "DYING", "DEAD"))
Agent = namedtuple("Agent", ("name", "category"))


def meetup(agent_listing: tuple) -> list:
    """Model the outcome of the meetings of pairs of agents.

    The pairs of agents are ((a[0], a[1]), (a[2], a[3]), ...). If there's an uneven
    number of agents, the last agent will remain the same.

    Notes
    -----
    The rules governing the meetings were described in the question. The outgoing
    listing may change its internal ordering relative to the incoming one.

    Parameters
    ----------
    agent_listing : tuple of Agent
        A listing (tuple in this case) in which each element is of the Agent
        type, containing a 'name' field and a 'category' field, with 'category' being
        of the type Condition.

    Returns
    -------
    updated_listing : list
        A list of Agents with their 'category' field changed according to the result
        of the meeting.
    """
from itertools import islice
    
    def process_pair(a, b):
        """Process a pair of agents meeting and return the resulting agents."""
        # If either agent is HEALTHY or DEAD, they don't meet
        if a.category in (Condition.HEALTHY, Condition.DEAD) or b.category in (Condition.HEALTHY, Condition.DEAD):
            return [a, b]
        
        # CURE scenarios
        if a.category == Condition.CURE and b.category != Condition.CURE:
            new_b_category = (
                Condition.HEALTHY if b.category == Condition.SICK else
                Condition.SICK if b.category == Condition.DYING else
                b.category
            )
            return [a, Agent(b.name, new_b_category)]
        
        if b.category == Condition.CURE and a.category != Condition.CURE:
            new_a_category = (
                Condition.HEALTHY if a.category == Condition.SICK else
                Condition.SICK if a.category == Condition.DYING else
                a.category
            )
            return [Agent(a.name, new_a_category), b]
        
        if a.category == Condition.CURE and b.category == Condition.CURE:
            return [a, b]
        
        # SICK & SICK: both become DYING
        if a.category == Condition.SICK and b.category == Condition.SICK:
            return [Agent(a.name, Condition.DYING), Agent(b.name, Condition.DYING)]
        
        # SICK & DYING: Sick becomes Dying, Dying becomes Dead
        if a.category == Condition.SICK and b.category == Condition.DYING:
            return [Agent(a.name, Condition.DYING), Agent(b.name, Condition.DEAD)]
        
        if a.category == Condition.DYING and b.category == Condition.SICK:
            return [Agent(a.name, Condition.DEAD), Agent(b.name, Condition.DYING)]
        
        # DYING & DYING: both become Dead
        if a.category == Condition.DYING and b.category == Condition.DYING:
            return [Agent(a.name, Condition.DEAD), Agent(b.name, Condition.DEAD)]
        
        # Any other case - no change
        return [a, b]
    
    # Filter out HEALTHY and DEAD agents as they don't participate in meetings
    meeting_agents = [agent for agent in agent_listing if agent.category not in (Condition.HEALTHY, Condition.DEAD)]
    non_meeting_agents = [agent for agent in agent_listing if agent.category in (Condition.HEALTHY, Condition.DEAD)]
    
    result = []
    
    # Process meetings in pairs
    it = iter(meeting_agents)
    for agent1 in it:
        try:
            agent2 = next(it)
            # Process the meeting between the two agents
            result.extend(process_pair(agent1, agent2))
        except StopIteration:
            # Odd number of agents, the last one doesn't meet anyone
            result.append(agent1)
    
    # Add back the agents that didn't participate in meetings
    result.extend(non_meeting_agents)
    
    return result
    