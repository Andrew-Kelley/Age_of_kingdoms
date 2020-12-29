

# Should I inherit from SelectedUnits?
# But being an army doesn't mean it is selected, so I don't think so.
class Army:
    """A collection of some units for military purposes."""
    # Needs to implement the method units (which is all units in this army)
    # and that method, called units, needs to be a property
    pass


# Should Group inherit from Army? Or should Group be more general than its
# docstring states and then have Army inherit from Group?
class Group:
    """A collection of villagers."""
    # Needs to implement the method units (which is all units in this army)
    # and that method, called units, needs to be a property
    pass
