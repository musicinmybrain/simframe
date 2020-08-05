from functools import partial

from simframe.frame.abstractgroup import AbstractGroup
from simframe.frame.field import Field
from simframe.frame.intvar import IntVar
from simframe.frame.updater import Updater
from simframe.frame.heartbeat import Heartbeat

class Group(AbstractGroup):
    """Class for grouping data.
    Group is a data frame that has additional functionality for updating its attributes.
        
    Notes
    -----
    When <group>.update() is called the instructions of the group's heartbeat will be performed.
    The function that is determing the update operation needs the parent frame object as first positional argument.
    
    
    Examples
    --------
    >>> grp = Group(sim, description="My group")
    """
    
    __name__ = "Group"
    
    def __init__(self, owner, updater=None, description=""):
        """Parameters
        ----------
        owner : Frame
            Parent frame object to which the group belongs
        updater : Heartbeat, Updater, callable, list or None, optional, default : None
            Updater for group update. A Heartbeat object will be created from this.
        description : string, optional, default : ""
            Descriptive string for the group
            
        Notes
        -----
        The updater of groups can take a list of string with the attribute names that should be updated
        in the order in which they should be updated. It will create a callable function from that list."""
        self._description = description
        self._owner = owner
        self.updater = updater
            
    def __setattr__(self, name, value):
        """Function to set an attribute including fields.
        This function allows the user to change the value of fields instead of replacing them."""
        if isinstance(value, Field):
            self.__dict__[name] = value
        elif name in self.__dict__ and isinstance(self.__dict__[name], Field):
            self.__dict__[name]._setvalue(value)
        else:
            super().__setattr__(name, value)

    def __repr__(self):
        """Function to have good looking overview of the members of the group."""
    
        fields = {}
        groups = {}
        misc = {}

        # return value
        ret = ""
        
        for key, val in self.__dict__.items():        
            # Don't show private attributes
            if key.startswith("_"): continue
        
            # Sort attributes by group, field and else
            if isinstance(val, Field):
                fields[key] = val
            elif isinstance(val, Group):
                groups[key] = val
            else:
                misc[key] = val
        
        # Underlined headline. The length of the underline is off if there are hidden characters, like color.
        ret += self.__str__()+"\n"
        ret += "-" * (len(ret)-1) + "\n"
        
        # Printing all groups alphanumerically sorted by name
        if len(groups) > 0:
            for key in sorted(groups.keys(), key=str.casefold):
                if len(key) > 12:
                    name = key[:9]+"..."
                else:
                    name = key
                ret += "    {:12s} : {}\n".format(name, groups[key])
            ret += "  -----\n"
        
        # Printing all fields alphanumerically sorted by name
        if len(fields) > 0:
            for key in sorted(fields.keys(), key=str.casefold):
                if len(key) > 12:
                    name = key[:9]+"..."
                else:
                    name = key
                ret += "    {:12s} : {}\n".format(name, fields[key].__str__())
            ret += "  -----\n"
        
        # Printing everything else alphanumerically sorted
        if len(misc) > 0:
            for key in sorted(misc.keys(), key=str.casefold):
                if len(key) > 12:
                    name = key[:9]+"..."
                else:
                    name = key
                ret += "    {:12s} : {}\n".format(name, type(misc[key]).__name__)
            ret += "  -----\n"
        
        # The Frame object should have an integrator and writer which are displayed separately.
        # If the object has an integrator
        if "_integrator" in self.__dict__.keys():
            integrator = self.__dict__["_integrator"]
            # If not set, print warning
            txt = "\033[93mnot specified\033[0m"
            if integrator is not None:
                txt = integrator.__str__()
            ret += "    {:12s} : {}".format("Integrator", txt)
            ret += "\n"

        # If the object has a writer
        if "_writer" in self.__dict__.keys():
            writer = self.__dict__["_writer"]
            # If not set print warning
            txt = "\033[93mnot specified\033[0m"
            if writer is not None:
                txt = writer.__str__()
            ret += "    {:12s} : {}".format("Writer", txt)
            ret += "\n"
        
        return ret

    # We need to overwrite the updater property of AbstractGroup, because we want the group to be able
    # to take lists of attributes as value.
    @property
    def updater(self):
        return self._updater
    @updater.setter
    def updater(self, value):
        if isinstance(value, Heartbeat):
            self._updater = value
        elif isinstance(value, list):
            self._checkupdatelist(value)
            self._updater = Heartbeat(self._createupdatefromlist(value))
        else:
            self._updater = Heartbeat(value)
            
    def addfield(self, name, value, updater=None, differentiator=None, description="", constant=False):
        """Function to add a new field to the object.
        
        Parameters
        ----------
        name : string
            Name of the field
        value : number, array, string
            Initial value of the field. Needs to have already the correct type and shape
        updater : Heartbeat, Updater, callable or None, optional, default : None
            Updater for field update
        differentiator : Heartbeat, Updater, callable or None, optional, default : None
            Differentiator if the field has a derivative
        description : string, optional, default : ""
            Descriptive string for the field
        constant : boolean, optional, default : False
            True if the field is immutable
        """
        self.__dict__[name] = Field(self._owner, value, updater=updater, differentiator=differentiator, description=description, constant=constant)

    def addgroup(self, name, updater=None, description=""):
        """Function to add a new group to the object.
        
        Parameters
        ----------
        name : string
            Name of the group
        updater : Heartbeat, Updater, callable or None, optional, default : None
            Updater for field update
        description : string, optional, default : ""
            Descriptive string for the group
        """
        self.__dict__[name] = Group(self._owner, updater=updater, description=description)

    def addintegrationvariable(self, name, value, snapshots=[], updater=None, description=""):
        """Function to add a new field to the object that acts as integration variable.
        
        Parameters
        ----------
        name : string
            Name of the field
        value : number, array, string
            Initial value of the field. Needs to have already the correct type and shape
        updater : Heartbeat, Updater, callable or None, optional, default : None
            Updater for field update
        snapshots : list, ndarray, optional, default : []
            List of snapshots at which an output file should be written
        description : string, optional, default : ""
            Descriptive string for the field
        """
        self.__dict__[name] = IntVar(self._owner, value, updater=updater, snapshots=snapshots, description=description)

    def _checkupdatelist(self, ls):
        """This function checks if a list is suitable to be used as update.
        
        Parameters
        ----------
        ls : list
            list of string with the attribute names that should be updated in that order"""
        for val in ls:
            if not isinstance(val, str):
                raise ValueError("List has to be list of strings.")
        for val in ls:
            if val not in self.__dict__:
                msg = "\033[93mWarning:\033[0m {} is not an attribute of the group".format(val)
                print(msg)

    def _createupdatefromlist(self, ls):
        """This method creates an update method from a list.
        
        Parameters
        ----------
        ls : list
            list of group attributes that should be updated in that order
            
        Returns
        -------
        func : callable
            Function that is reduced by <self> and <ls>."""
        return partial(_dummyupdatewithlist, self, ls)


def _dummyupdatewithlist(grp, ls, owner, *args, **kwargs):
    """This method is a dummy method that updates all attributes given in ls.
    
    Parameters
    ----------
    grp : Group
        group to which the attributes belong
    ls : list
        List of string with attributes of group that should be updated in that order
    owner : Frame
        Parent frame object
    args : additional positional arguments
    kwargs : additional keyword arguments
    
    Notes
    -----
    args and kwargs are only passed to the updater of the Heartbeat, NOT systole or diastole."""
    for val in ls:
        grp.__dict__[val].update(*args, **kwargs)