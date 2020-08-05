import numpy as np
import os

from simframe.io.reader import Reader

class Writer(object):
    """Class for writing outputs
    
    Parameters
    ----------
    func : callable
        Function that is writing the outputs to file
    datadir : string, optional, default : "data"
        relative path to data directory
    filename : string, optional, default : "data"
        basic name of the files to be written
    zfill : int, optional, default : 4
        leading zeros of numbered files
    extension : string, optional, default : "out"
        filename extension of the data files
    overwrite : boolean, optional, default : False
        If existing files should be overwritten
    options : dict, optional, default : {}
        Optional keyword arguments that need to be passed to writing algorithm
    
    Example filename:
    <datadir>/<data>0001.<extension>"""

    __name__ = "Writer"

    _reader = None

    def __init__(self, func, datadir="data", filename="data", zfill=4, extension="out", overwrite=False, reader=None, description=None, options={}):
        self._func = func
        self.datadir = datadir
        self.filename = filename
        self.zfill = zfill
        self.extension = extension
        self.overwrite = overwrite
        self.description = description
        self.options = options
        self.read = reader(self)

    @property
    def overwrite(self):
        return self._overwrite
    @overwrite.setter
    def overwrite(self, value):
        if not isinstance(value, np.int):
            raise TypeError("<overwrite> has to be of type bool.")
        if value:
            self._overwrite = True
        else:
            self._overwrite = False

    @property
    def read(self):
        return self._reader
    @read.setter
    def read(self, value):
        print(value)
        if isinstance(value, Reader) or (value is None):
            self._reader = value
        else:
            raise TypeError("<reader> has to be of type Reader or None.")

    def checkdatadir(self, datadir=None, createdir=False):
        """Function checks if data directory exists and creates it if desired.
        
        Parameters
        ----------
        datadir : string, optinal, default : None
            Datadirectory to be checked. If None it assumes the data directory of the parent writer.
        createdir : boolen, optional, default : False
            If True function creates data directory if it does not exist.
            
        Returns
        -------
        datadirexists : boolean
            True if directory exists, False if not"""
        
        datadir = self.datadir if datadir is None else datadir

        if not os.path.exists(self.datadir) and createdir:
            msg = "Creating data directory '{:s}'.".format(self.datadir)
            print(msg)
            os.makedirs(self.datadir)

        return os.path.exists(self.datadir)

    def __str__(self):
        ret = str(self.__name__)
        if((self.description != "") and (self.description != None)):
            ret += " ({})".format(self.description)
        return ret

    def __repr__(self):
        ret = self.__str__()+"\n"
        ret += "-" * (len(ret)-1) + "\n"
        ret += "    Data directory : {}\n".format(self.datadir)
        ret += "    File names     : {}\n".format(self._getfilename(0))
        ret += "    Overwrite      : {}\n".format("\033[93m{}\033[0m".format(self.overwrite) if self.overwrite else self.overwrite)
        ret += "    options        : {}".format(self.options)
        return ret

    def _getfilename(self, i):
        """This function creates <path>/<filename> for a given output number

        Parameters
        ----------
        i : integer
            Number of output

        Returns
        -------
        filename : str
            The constructed filename"""

        # Removing . from extension if given
        ext = self.extension
        if ext[0] != ".":
            ext = "." + ext

        number = str(i).zfill(self.zfill)
        filename = self.filename + number + ext

        return os.path.join(self.datadir, filename)

    def write(self, sim, i, filename, forceoverwrite, **kwargs):
        """Writes output to file
        
        Parameters
        ----------
        filname : string
            Path to file to be written
        i : int
            Number of output
        filename : string
            If this is not "" the writer will use this filename instead of the standard scheme
        forceoverwrite : boolean
            If True it will forces and overwrite of the file if it exists."""
        
        if filename == "":
            filename = self._getfilename(i)
            self.checkdatadir(createdir=True)
        if not forceoverwrite:
            if not self.overwrite:
                if os.path.isfile(filename):
                    raise RuntimeError("File {} already exists.".format(filename))
        self._func(sim, filename, **self.options, **kwargs)
        msg = "Writing file \033[94m'{}'\033[0m".format(filename)
        print(msg)