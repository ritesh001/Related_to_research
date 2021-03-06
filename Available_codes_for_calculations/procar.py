#!/usr/bin/python
# procar.py
#
# Developers:
#
# -Aldo Romero: hromero@mpi-halle.mpg.de
# -Francisco Munoz: fvmunoz@gmail.com
#


"""
Impemented:

 -UtilsProcar: handy methods, not intented to be used by the user

 -ProcarParser: reads data from a procar (may be compressed) and store
    them as arrays:
    -kpoint[kpointsCount][3]
    -bands[kpointsCount][bandsCount]
    -spd[kpoint][band][ispin][atom][orbital]

 -ProcarFileFilter: Filter/average a PROCAR, writing a new file with
    the changes. Useful methods
    -FilterOrbitals: write just some orbitals or combination of them
    -FilterAtoms: write just selected atoms (or add them)
    -FilterBands: Writes just selected bands.
    -FilterSpin: Write just selected ispin components (ie: density)

 -ProcarSelect: Select/averages the data yielding a bidimensional
  array ready to plot

"""
#basic modules. Should be present 
import numpy as np
import re
import logging
import matplotlib.pyplot as plt
import sys


class UtilsProcar:
  """
  This class is to store handy methods that do not fit in other place
  
  members:

  -Openfile: Tries to open a File, it has suitable values for PROCARs
   and can handle gzipped files
   
  -MergeFiles: concatenate two or more PROCAR files taking care of
   metadata and kpoint indexes. Useful for splitted bandstructures
   calculation.

  -FermiOutcar: it greps the Fermi Energy from a given outcar file.

  -RecLatOutcar: it greps the reciprocal lattice from the outcar.

  """
  def __init__(self, loglevel=logging.WARNING):
    self.log = logging.getLogger("UtilsProcar")
    self.log.setLevel(loglevel)
    self.ch = logging.StreamHandler()
    self.ch.setFormatter(logging.Formatter("%(name)s::%(levelname)s:"
                                           " %(message)s"))
    self.ch.setLevel(logging.DEBUG)
    self.log.addHandler(self.ch)
    self.log.debug("UtilsProcar()")
    self.log.debug("UtilsProcar()...done")
    return
  
  def OpenFile(self, FileName=None):
    """
    Tries to open a File, it has suitable values for PROCAR and can
    handle gzipped files

    Example: 

    >>> foo =  UtilsProcar.Openfile()
    Tries to open "PROCAR", then "PROCAR.gz"

    >>> foo = UtilsProcar.Openfile("../bar")
    Tries to open "../bar". If it is a directory, it will try to open
    "../bar/PROCAR" and if fails again "../bar/PROCAR.gz"

    >>> foo = UtilsProcar.Openfile("PROCAR-spd.gz")
    Tries to open a gzipped file "PROCAR-spd.gz"

    If unable to open a file, it raises a "IOError" exception.
"""
    import os
    import gzip
    
    self.log.debug("OpenFile()")
    self.log.debug("Filename :" + FileName)

    if FileName is None:
      FileName = "PROCAR"
      self.log.debug("Input was None, now is: "+ FileName)

    #checking if fileName is just a path and needs a "PROCAR to " be
    #appended
    elif os.path.isdir(FileName):
      self.log.info("The filename is a directory")
      if FileName[-1] != r"/":
        FileName += "/"
      FileName += "PROCAR"
      self.log.debug("I will try  to open :" + FileName)
    
    #checking that the file exist
    if os.path.isfile(FileName):
      self.log.debug("The File does exist")
      #Checking if compressed
      if FileName[-2:] == "gz":
        self.log.info( "A gzipped file found")
        inFile = gzip.open(FileName, "r")
      else: 
        self.log.debug("A normal file found")
        inFile = open(FileName, "r")
      return inFile

    #otherwise a gzipped version may exist
    elif os.path.isfile(FileName + ".gz"):
      self.log.info("File not found, however a .gz version does exist and will"
                    " be used")
      inFile = gzip.open(FileName + ".gz")

    else:
      self.log.debug("File not exist, neither a gzipped version")
      raise IOError("File not found")

    self.log.debug("OpenFile()...done")
    return inFile
  
  
  def MergeFiles(self, inFiles, outFile, gzipOut=False):
    """
    Concatenate two or more PROCAR files.
    This methods takes care of the k-indexes.

    Args:
    -inFiles: an iterable with files to be concatenated

    -outFile: a string with the outfile name.

    -gzipOut: whether gzip or not the outout file.

    Warning: spin polarized case is not Ok!
    """
    import gzip
    
    self.log.debug("MergeFiles()")
    self.log.debug("infiles: " " ,".join(inFiles))

    inFiles = [self.OpenFile(x) for x in inFiles]
    header = [x.readline() for x in inFiles]
    self.log.debug("All the input headers are: \n"+ "".join(header))
    metas = [x.readline() for x in inFiles]
    self.log.debug("All the input metalines are:\n "+ "".join(metas))
    #parsing metalines

    parsedMeta = [map(int, re.findall(r"#[^:]+:([^#]+)",x)) for x in metas]
    kpoints = [x[0] for x in parsedMeta]
    bands   = set([x[1] for x in parsedMeta])
    ions    = set([x[2] for x in parsedMeta])
    
    #checking that bands and ions macht (mind: bands & ions are 'sets'):    
    if len(bands) != 1 or len(ions) != 1:
      self.log.error("Number of bands/ions  do not match")
      raise RuntimeError("Files are incompatible")
    
    newKpoints = np.array(kpoints, dtype=int).sum()
    self.log.info("New number of Kpoints: " + str(newKpoints))
    newMeta = metas[0].replace(str(kpoints[0]), str(newKpoints), 1)
    self.log.debug("New meta line:\n" + newMeta)
    
    if gzipOut:
      self.log.debug("gzipped output")
      outFile = gzip.open(outFile, 'w')
    else:
      self.log.debug("normal output")
      outFile = open(outFile, 'w')
    outFile.write(header[0])
    outFile.write(newMeta)
    
    #embedded function to change old k-point indexes by the correct
    #ones. The `kreplace.k` syntax is for making the variable 'static'
    def kreplace(matchobj):
      #self.log.debug(print matchobj.group(0))
      kreplace.k += 1
      kreplace.localCounter += 1
      return matchobj.group(0).replace(str(kreplace.localCounter), 
                                       str(kreplace.k))

    kreplace.k = 0
    self.log.debug("Going to replace K-points indexes")
    for inFile in inFiles:
      lines = inFile.read()
      kreplace.localCounter = 0
      lines = re.sub('(\s+k-point\s*\d+\s*:)', kreplace, lines)
      outFile.write(lines)
    
    self.log.debug("Closing output file")
    outFile.close()
    self.log.debug("MergeFiles()...done")
    return
  
  
  def FermiOutcar(self, filename):
    """Just finds all E-fermi fields in the outcar file and keeps the
    last one (if more than one found).

    Args:
    -filename: the file name of the outcar to be readed

    """
    self.log.debug("FermiOutcar(): ...")
    self.log.debug("Input filename : " + filename)

    outcar = open(filename, "r").read()
    match = re.findall(r"E-fermi\s*:\s*(-?\d+.\d+)", outcar)[-1]
    self.log.info("Fermi Energy found : " + match)
    self.log.debug("FermiOutcar(): ...Done")
    return float(match)

  
  def RecLatOutcar(self, filename):
    """Finds and return the reciprocal lattice vectors, if more than
    one set present, it reutrn just the lasdt one.

    Args: 
    -filename: the name of the outcar file  to be read
    
    """
    self.log.debug("RecLatOutcar(): ...")
    self.log.debug("Input filename : " + filename)

    outcar = open(filename, "r").read()
    #just keeping the last component
    recLat = re.findall(r"reciprocal\s*lattice\s*vectors\s*([-.\s\d]*)",
                        outcar)[-1]
    self.log.debug("the match is : " + recLat)
    recLat = recLat.split()
    recLat = np.array(recLat, dtype=float)
    #up to now I have, both direct and rec. lattices (3+3=6 columns)
    recLat.shape = (3,6)
    recLat = recLat[:,3:]
    self.log.info("Reciprocal Lattice found :\n" + str(recLat))
    self.log.debug("RecLatOutcar(): ...Done")
    return recLat


  def ProcarRepair(self, infilename, outfilename):
    """It Tries to repair some stupid problems due the stupid fixed
    format of the stupid fortran.

    Up to now it only separes k-points as the following:
    k-point    61 :    0.00000000 0.5000000010.00000000 ...

    But as I found new stupid errors they should be fixed here.
    """
    self.log.debug("ProcarRepair(): ...")
    infile = self.OpenFile(infilename)
    fileStr = infile.read()
    infile.close()
    
    fileStr = re.sub(r'(\.\d{8})(\d{2}\.)', r'\1 \2', fileStr)
    fileStr = re.sub(r'(\d)-(\d)', r'\1 -\2', fileStr)
    
    fileStr = re.sub(r'\*+', r' -10.0000 ', fileStr)

    outfile = open(outfilename, 'w')
    outfile.write(fileStr)
    outfile.close()

    self.log.debug("ProcarRepair(): ...Done")
    return
    

class ProcarParser:
  """Parses a PROCAR file and store it in memory. It only deals with
  PROCAR files, that means no Fermi energy (UtilsProcar.FermiOutcar
  can help), and the reciprocal vectors should be supplied (if used).
  
  Members:
  

  Example:
  

  """
  def __init__(self, loglevel=logging.WARNING):
    # array with k-points, they have the following values
    # -None: if not parsed (yet) or parsed with a `permissive` flag on
    # -direct coordinates: if a recLattice was not supplied to the parser
    # -cartesian coords: if a recLattice was supplied to the parser.
    # In the later cases, self.kpoints.shape=(self.kpointsCount, 3)
    self.kpoints = None      
    #Nunber of kpoints, as given by the KPOINTS header
    self.kpointsCount = None

    # bands headers present in PROCAR file.
    # self.bands.shape=(self.kpointsCount,self.bandsCount)
    self.bands = None
    # Number of bands. For a spin polarized calculation the number of
    # bands is double (spin ip + spin down). On this array there is no
    # distinction between spin up and down
    self.bandsCount = None   

    #Number of ions+1 the +1 is the 'tot' field, ie: the sum over all atoms
    self.ionsCount = None

    self.fileStr = None      #the actual file, stored in memory
    self.spd = None          #the atom/orbital projected data
    self.orbitalName = ["s", "py", "pz", "px", "dxy", "dyz", "dz2", "dxz",
                        "dx2", "tot"]
    self.orbitalCount = None #number of orbitals

    # number of spin components (blocks of data), 1: non-magnetic non
    # polarized, 2: spin polarized collinear, 4: non-collinear
    # spin. Mind: before calling to `readOrbitals` the case '4' is
    # marked as '1'
    self.ispin = None        
    self.recLattice = None   #reciprocal lattice vectors
    self.utils = UtilsProcar()

    self.log = logging.getLogger("ProcarParser")
    self.log.setLevel(loglevel)
    self.ch = logging.StreamHandler()
    self.ch.setFormatter(logging.Formatter("%(name)s::%(levelname)s:"
                                           " %(message)s"))
    self.ch.setLevel(logging.DEBUG)
    self.log.addHandler(self.ch)
    #At last, one message to the logger.
    self.log.debug("Procar instanciated")
    return
  
  def readKpoints(self, permissive=False):
    """Reads the k-point headers. A typical k-point line is:
    k-point    1 :    0.00000000 0.00000000 0.00000000  weight = 0.00003704\n

    fills self.kpoint[kpointsCount][3]
    
    The weights are discarded (are they useful?)
    """
    self.log.debug("readKpoints")
    if not self.fileStr:
      log.warning("You should invoke `procar.read()` instead. Returning")
      return
    
    # finding all the K-points headers 
    self.kpoints = re.findall(r"k-point\s+\d+\s*:\s+([-.\d\s]+)", self.fileStr)
    self.log.debug(str(len(self.kpoints))+" K-point headers found")
    self.log.debug("The first match found is: " + str(self.kpoints[0]))
    
    # trying to build an array
    self.kpoints = [x.split() for x in self.kpoints]
    try:
      self.kpoints = np.array(self.kpoints, dtype=float)
    except ValueError:
      self.log.error("Ill-formatted data:")
      print '\n'.join([str(x) for x in self.kpoints])
      if permissive is True:
        # Discarding the kpoints list, however I need to set
        # self.ispin beforehand.
        if len(self.kpoints) == self.kpointsCount:
          self.ispin = 1
        elif len(self.kpoints) == 2*self.kpointsCount:
          self.ispin = 2
        else:
          raise ValueError("Kpoints do not match with ispin=1 or 2.")
        self.kpoints = None
        self.log.warning("K-points list is useless, setting it to `None`")
        return
      else:
        raise ValueError("Badly formated Kpoints headers, try `--permissive`")
    # if successful, go on

    # trying to identify an non-polarized or non-collinear case, a
    # polarized case or a defective file

    if len(self.kpoints) != self.kpointsCount:
      #if they do not match, may means two things a spin polarized
      #case or a bad file, lets check
      self.log.debug("Number of kpoints do not match, looking for a "
                     "spin-polarized case")
      # lets start testing if it is spin polarized, if so, there
      # should be 2 identical blocks of kpoints.
      up,down = np.vsplit(self.kpoints, 2)
      if (up == down).all():
        self.log.info("Spin-polarized calculation found")
        self.ispin = 2
        # just keeping one set of kpoints (the other will be
        # discarded)
        self.kpoints = up
      else:
        self.log.error("Number of K-points do not match! check them.")
        raise RuntimeError("Bad Kpoints list.")
    # if ISPIN != 2 setting ISPIN=1 (later for the non-collinear case 1->4)
    else:
      self.ispin = 1

    #checking again, for compatibility,
    if len(self.kpoints) != self.kpointsCount:
      raise RuntimeError("Kpoints number do not match with metadata")
      

    self.log.debug(str(self.kpoints))
    self.log.info("The kpoints shape is " + str(self.kpoints.shape))

    if self.recLattice is not None:
      self.log.info("Changing to cartesians coordinates")
      self.kpoints = np.dot(self.kpoints, self.recLattice)
      self.log.debug("New kpoints: \n" + str(self.kpoints))
    return

  def readBands(self):
    """Reads the bands header. A typical bands is:
    band   1 # energy   -7.11986315 # occ.  1.00000000
    
    fills self.bands[kpointsCount][bandsCount] 
    
    The occupation numbers are discarded (are they useful?)"""
    self.log.debug("readBands")
    if not self.fileStr:
      log.warning("You should invoke `procar.read()` instead. Returning")
      return
    
    # finding all bands 
    self.bands = re.findall(r"band\s*(\d+)\s*#\s*energy\s*([-.\d\s]+)",
                            self.fileStr)
    self.log.debug(str(len(self.bands)) + 
                   " bands headers found, bands*Kpoints = " +
                   str(self.bandsCount*self.kpointsCount))
    self.log.debug("The first match found is: " + str(self.bands[0]))

    # checking if the number of bands match

    if len(self.bands) != self.bandsCount*self.kpointsCount*self.ispin:
      self.log.Error("Number of bands headers do not match")
      raise RuntimeError("Number of bands don't match")

    # casting to array to manipulate the bands
    self.bands = np.array(self.bands, dtype=float)
    self.log.debug(str(self.bands))

    # Now I will deal with the spin polarized case. The goal is join
    # them like for a non-magnetic case
    if self.ispin == 2:
      # up and down are along the first axis
      up,down = np.vsplit(self.bands, 2)
      self.log.debug( "up   , "+ str(up.shape))
      self.log.debug( "down , "+ str(down.shape))
      
      # reshapping (the 2  means both band index and energy)
      up.shape   = (self.kpointsCount, self.bandsCount, 2)
      down.shape = (self.kpointsCount, self.bandsCount, 2)

      # setting the correct number of bands (up+down)
      self.bandsCount *=2
      self.log.debug("New number of bands : " + str(self.bandsCount))      
      
      # and joining along the second axis (axis=1), ie: bands-like
      self.bands = np.concatenate((up,down), axis=1)

    #otherwise just reshaping is needed
    else:
      self.bands.shape = (self.kpointsCount, self.bandsCount, 2)
      
    # Making a test if the broadcast is rigth, otherwise just print 
    test = [x.max()- x.min() for x in self.bands[:,:,0].transpose()]
    if np.array(test).any():
      self.log.warning("The indexes of bands do not match. CHECK IT. "
                       "Likely the data was wrongly broadcasted")
      self.log.warning(str(self.bands[:,:,0]))
    # Now safely removing the band index
    self.bands = self.bands[:,:,1]
    self.log.info("The bands shape is " + str(self.bands.shape))
    return

  def readOrbital(self):
    """Reads all the spd-projected data. A typical/expected block is:
    ion      s     py     pz     px    dxy    dyz    dz2    dxz    dx2    tot
      1  0.079  0.000  0.001  0.000  0.000  0.000  0.000  0.000  0.000  0.079
      2  0.152  0.000  0.000  0.000  0.000  0.000  0.000  0.000  0.000  0.152
      3  0.079  0.000  0.001  0.000  0.000  0.000  0.000  0.000  0.000  0.079
      4  0.188  0.000  0.000  0.000  0.000  0.000  0.000  0.000  0.000  0.188
      5  0.188  0.000  0.000  0.000  0.000  0.000  0.000  0.000  0.000  0.188
    tot  0.686  0.000  0.002  0.000  0.000  0.000  0.000  0.000  0.000  0.688
    (x2 for spin-polarized, x4 non-collinear).

    The data is stored in an array self.spd[kpoint][band][ispin][atom][orbital]

    Undefined behavior in case of phase factors.
    """
    self.log.debug("readOrbital")
    if not self.fileStr:
      log.warning("You should invoke `procar.read()` instead. Returning")
      return
    
    #finding all orbital headers 
    self.spd = re.findall(r"ion(.+)", self.fileStr)
    self.log.info("the first orbital match reads: " + self.spd[0])
    self.log.debug("And I found " + str(len(self.spd)) + " orbitals headers")

    # testing if the orbital names are known (the standard ones)
    FoundOrbs = self.spd[0].split()
    size = len(FoundOrbs)
    # only the first 'size' orbital
    StdOrbs =  self.orbitalName[:size-1] + self.orbitalName[-1:]
    if FoundOrbs != (StdOrbs):
      self.log.warning(str(size)+" orbitals. (Some of) They are unknow.")
    self.orbitalCount = size
    self.orbitalNames = self.spd[0].split()
    self.log.debug("Anyway, I will use the following set of orbitals: "
                   + str(self.orbitalNames))

    # Now reading the bulk of data
    self.log.debug("Now searching the values")
    # The case of just one atom is handled differently since the VASP
    # output is a little different
    if self.ionsCount is 1:
      self.spd = re.findall(r"^(\s*1\s+.+)$", self.fileStr, re.MULTILINE)
    else:
      self.spd = re.findall(r"([-.\d\se]+tot.+)\n", self.fileStr)
    # free the memory (could be a lot)
    self.fileStr = None
    self.log.debug("the first entry is \n" + self.spd[0])
    
    self.log.debug("Number of entries found: " + str(len(self.spd))  )
    expected = self.bandsCount*self.kpointsCount
    self.log.debug("The number of entries for a non magnetic calc. is: " + 
                   str(expected))
    if expected == len(self.spd):
      self.log.info("Both numbers match, ok")
    # catching a non-collinear calc.
    elif expected*4 == len(self.spd):
      self.log.info("non-collinear calculation found")
      # testing if previous ispin value is ok
      if self.ispin != 1:
        self.log.warning("Incompatible data: self.ispin= " + str(self.ispin) +
                         ". Now is 4")
      self.ispin = 4
    else:
      self.log.error("The parser or data is wrong!!!")
      self.log.info("bandsCount: " + str(self.bandsCount))
      self.log.info("KpointsCount: " + str(self.kpointsCount))
      raise RuntimeError("Shit happens")
    
    # checking for consistency
    for line in self.spd:
      if len(line.split()) != (self.ionsCount)*(self.orbitalCount+1):
        self.log.error( "Expected: "+str(self.ionsCount) + "*" + 
                        str(self.orbitalCount+1) + " = " + 
                        str((self.ionsCount)*(self.orbitalCount+1)) +
                        " Fields. Present block: " + str(len(line.split())))
        print line
        raise RuntimeError("Flats happens")

    # replacing the "tot", to allows a conversion to numpy
    self.spd = [x.replace('tot','0') for x in self.spd]
    self.spd = [x.split() for x in self.spd]
    self.spd = np.array(self.spd, dtype=float)
    self.log.debug("The spd array shape is:" + str(self.spd.shape))
    # the +1  at the end is to account for the atom index
    self.log.info(" old spd.shape= " + str(self.spd.shape))

    # handling collinear polarized case
    if self.ispin == 2:
      self.log.debug("Handling sp collinear case...")
      # splitting both spin components, now they are along k-points
      # axis (1st axis) but, then should be concatenated along the
      # bands.
      up,down = np.vsplit(self.spd, 2)
      # ispin = 1 for a while, we will made the distinction
      up.shape = (self.kpointsCount, self.bandsCount/2, 1,
                  self.ionsCount, self.orbitalCount+1)
      down.shape = (self.kpointsCount, self.bandsCount/2, 1,
                    self.ionsCount, self.orbitalCount+1)
      # concatenating bandwise. Density and magntization, their
      # meaning is obvious, and do uses 2 times more memory than
      # required, but I *WANT* to keep it as close as possible to the
      # non-collinear or non-polarized case
      density = np.concatenate((up, down), axis=1)
      magnet  = np.concatenate((up,-down), axis=1)
      #concatenated along 'ispin axis'
      self.spd = np.concatenate((density, magnet), axis=2)
      self.log.debug("polarized collinear spd.shape= " + str(self.spd.shape))
    
    #otherwise, just a reshping suffices
    else:
      self.spd.shape=(self.kpointsCount, self.bandsCount, self.ispin,
                      self.ionsCount, self.orbitalCount+1)
      
    self.log.info("spd array ready. Its shape is:" + str(self.spd.shape))
    return
  
  def readFile(self, procar=None, permissive=False, recLattice=None):
    """Reads and parses the whole PROCAR file. This method is a sort
    of metamethod: it opens the file, reads the meta data and call the
    respective functions for parsing kpoints, bands, and projected
    data.

    Args:

    -procar: The file name, if `None` or a directory the rigth thing
     will be done. Default=None
    
    -permissive: turn on (or off) some features to deal with badly
     written PROCAR files (stupid fortran), up to now just ignores the
     kpoints coordinates, which -as side effect- prevent he rigth
     space between kpoints. Default=False (off)


    -recLattice: a 3x3 array containing the reciprocal vectors, to
     change the Kpoints from rec. coordinates to cartesians. Rarely
     given by hand, see `UtilsProcar.RecLatProcar`. If given, the
     kpoints will be converted from direct coordinates to cartesian
     ones. Default=None

    """
    self.log.debug("readFile...")

    self.recLattice = recLattice

    self.log.debug("Opening file: '"+str(procar)+"'")
    f = self.utils.OpenFile(procar)
    # Line 1: PROCAR lm decomposed
    f.readline()  # throwaway
    # Line 2: # of k-points:  816   # of bands:  52   # of ions:   8
    metaLine = f.readline() # metadata
    self.log.debug("The metadata line is: "+ metaLine)
    re.findall(r"#[^:]+:([^#]+)", metaLine)
    self.kpointsCount, self.bandsCount, self.ionsCount = \
        map(int, re.findall(r"#[^:]+:([^#]+)", metaLine))
    self.log.info("kpointsCount = " + str(self.kpointsCount));
    self.log.info("bandsCount = " + str(self.bandsCount));
    self.log.info("ionsCount = " + str(self.ionsCount));
    if self.ionsCount is 1:
      self.log.warning("Special case: only one atom found. The program may not work as expected")
    else:
      self.log.debug("An extra ion will be the total value")
      self.ionsCount = self.ionsCount + 1

    #reading all the rest of the file to be parsed below
    self.fileStr = f.read()
    self.readKpoints(permissive)
    self.readBands()
    self.readOrbital()
    self.log.debug("readfile...done")
    return


class ProcarFileFilter:
  """Process a PROCAR file fields line-wise, specially useful for HUGE
  files.

  Example:

  -To group the "s", "p" y "d" orbitals from the file PROCAR and write
   them in PROCAR-spd:
   
   >>> a = procar.ProcarFileFilter("PROCAR", "PROCAR-new")
   >>> a.FilterOrbitals([[0],[1,2,3],[4,5,6,7,8]], ['s','p', 'd'])
   
  -To group the atoms 1,2,3,4 and 5,6,7,8 from PROCAR and write them
   in PROCAR-new:

   >>> a = procar.ProcarFileFilter("PROCAR", "PROCAR-new")
   >>> a.FilterAtoms([[0,1,2,3],[4,5,6,7]])

   -To select just the total density from PROCAR and write it in
    POTCAR-new:

   >>> a = procar.ProcarFileFilter("PROCAR", "PROCAR-new")
   >>> a.FilterSpin([0])
    

  """
  def __init__(self, infile=None, outfile=None, loglevel=logging.WARNING):
    """Initialize the class.

    Params: `infile=None`, input fileName
    """
    self.infile = infile
    self.outfile = outfile
    
    #We want a logging to tell us what is happening
    self.log = logging.getLogger("ProcarFileFilter")
    self.log.setLevel(loglevel)
    #This is a handler for logging, by now just keep it
    #untouched. Dont really matters its usage
    self.ch = logging.StreamHandler()
    self.ch.setFormatter(logging.Formatter("%(name)s::%(levelname)s:"
                                           " %(message)s"))
    self.ch.setLevel(logging.DEBUG)
    self.log.addHandler(self.ch)
    #At last, one message to the logger.
    self.log.debug("ProcarFileFilter instanciated")
    return
  
  def setInFile(self, infile):
    """Sets a input file `infile`, it can contains the path to the file"""
    self.infile = infile
    self.log.info("Input File: " + infile)
    return
  
  def setOutFile(self, outfile):
    """Sets a output file `outfile`, it can contains the path to the file"""
    self.outfile = outfile
    self.log.info("Out File: " + outfile)
    return
  
  def FilterOrbitals(self, orbitals, orbitalsNames):
    """
    Reads the file already set by SetInFile() and writes a new
    file already set by SetOutFile(). The new file only has the
    selected/grouped orbitals.

    Args: 

    -orbitals: nested iterable with the orbitals indexes to be
      considered. For example: [[0],[2]] means select the first
      orbital ("s") and the second one ("pz").
      [[0],[1,2,3],[4,5,6,7,8]] is ["s", "p", "d"].

    -orbitalsNames: The name to be put in each new orbital field (of a
      orbital line). For example ["s","p","d"] is a good
      `orbitalsName` for the `orbitals`=[[0],[1,2,3],[4,5,6,7,8]]. 
      However, ["foo", "bar", "baz"] is equally valid.

    Note: 
      -The atom index is not counted as the first field.
      -The last column ('tot') is so important that it is always
       included. Do not needs to be called
    """
    # setting iostuff, this method -and class- should not made any
    # checking about IO, that is the job of the caller
    self.log.info("In File: " + self.infile)
    self.log.info("Out File: " + self.outfile)
    # open the files
    fout = open(self.outfile, 'w')
    fopener = UtilsProcar()
    fin = fopener.OpenFile(self.infile)
    for line in fin:
      if re.match(r"\s*ion\s*", line):
        #self.log.debug("orbital line found: " + line)
        line = " ".join(['ion'] + orbitalsNames + ['tot']) + "\n"
          
      elif re.match(r"\s*\d+\s*", line) or re.match(r"\s*tot\s*", line):
        #self.log.debug("data line found: " + line)
        line = line.split()
        #all floats to an array
        data = np.array(line[1:], dtype=float)
        #setting a new line, keeping just the first value
        line = line[:1]
        for orbset in orbitals:
          line.append(data[orbset].sum())
        #the last value ("tot") always  should be written
        line.append(data[-1])
        #converting to str
        line =  [str(x) for x in line] 
        line = " ".join(line) + "\n"
      fout.write(line)
        
    return
  
  def FilterAtoms(self, atomsGroups):
    """
    Reads the file already set by SetInFile() and writes a new
    file already set by SetOutFile(). The new file only has the
    selected/grouped atoms.

    Args: 

    -atomsGroups: nested iterable with the atoms indexes (0-based) to
      be considered. For example: [[0],[2]] means select the first and
      the second atoms. While [[1,2,3],[4,5,6,7,8]] means select the
      contribution of atoms 1+2+3 and 4+5+6+7+8

    Note: 
      -The atom index is c-based (or python) beginning with 0
      -The output has a dummy atom index, without any intrisic meaning
    
    """
    # setting iostuff, this method -and class- should not made any
    # checking about IO, that is the job of the caller
    self.log.info("In File: " + self.infile)
    self.log.info("Out File: " + self.outfile)
    # open the files
    fout = open(self.outfile, 'w')
    fopener = UtilsProcar()
    with fopener.OpenFile(self.infile) as fin:
      # I need to change the numbers of ions, it will needs the second
      # line. The first one is not needed
      fout.write(fin.readline())
      line = fin.readline()
      line = line.split()
      # the very last value needs to be changed
      line[-1] = str(len(atomsGroups))
      line = ' '.join(line)
      fout.write(line + '\n')
      
      # now parsing the rest of the file
      data = []
      for line in fin:
        # if line has data just capture it
        if re.match(r"\s*\d+\s*", line):
          # self.log.debug("atoms line found: " + line)
          data.append(line)
        # if `line` is a end of th block (begins with 'tot'), do the
        # work. And clean up data then
        elif re.match(r"\s*tot\s*", line):
          # self.log.debug("tot line found: " + line)
          # making an array
          data = [x.split() for x in data]
          data = np.array(data, dtype=float)
          # iterating on the atoms groups
          for index in range(len(atomsGroups)):
            atoms = atomsGroups[index]
            # summing colum-wise
            atomLine = data[atoms].sum(axis=0)
            atomLine = [str(x) for x in atomLine]
            # the atom index should not be averaged (anyway now is
            # meaningless)
            atomLine[0] = str(index+1)
            atomLine = ' '.join(atomLine) 
            fout.write(atomLine + '\n' )
          
          # clean the buffer
          data = []
          # and write the `tot` line
          fout.write(line)
        # otherwise just write this line
        else:
          fout.write(line)

    return

  def FilterBands(self, Min, Max):
    """
    Reads the file already set by SetInFile() and writes a new
    file already set by SetOutFile(). The new file only has the
    selected bands.

    Args: 

    -Min, Max:
      the minimum/maximum band  index to be considered, the indexes 
      are the same used by vasp (ie written in the file).


    Note: -Since bands are somewhat disordered in vasp you may like to
      consider a large region and made some trial and error
    
    """
    # setting iostuff, this method -and class- should not made any
    # checking about IO, that is the job of the caller
    self.log.info("In File: " + self.infile)
    self.log.info("Out File: " + self.outfile)
    # open the files
    fout = open(self.outfile, 'w')
    fopener = UtilsProcar()
    fin = fopener.OpenFile(self.infile)

    # I need to change the numbers of kpoints, it will needs the second
    # line. The first one is not needed
    fout.write(fin.readline())
    line = fin.readline()
    # the third value needs to be changed, however better print it
    self.log.debug("The line contaning bands number is " + line)
    line = line.split()
    self.log.debug("The number of bands is: " + line[7])
    line[7] = str(Max-Min+1)
    line = ' '.join(line)
    fout.write(line + '\n')
    
    # now parsing the rest of the file
    write = True
    for line in fin:
      if re.match(r"\s*band\s*", line):
        # self.log.debug("bands line found: " + line)
        band = int(re.match(r"\s*band\s*(\d+)", line).group(1)) 
        if band < Min or band > Max:
          write = False
        else:
          write = True
      if re.match(r"\s*k-point\s*", line):
        write = True
      if write:
        fout.write(line)
    return
  
  def FilterSpin(self, components):
    """
    Reads the file already set by SetInFile() and writes a new
    file already set by SetOutFile(). The new file only has the
    selected part of the density (sigma_i).

    Args: 

    -components: The spin component block, for instante [0] menas just
      the density, while [1,2] would be the the sigma_x and sigma_y
      for a non-collinear calculation.

    """
    # setting iostuff, this method -and class- should not made any
    # checking about IO, that is the job of the caller
    self.log.info("In File: " + self.infile)
    self.log.info("Out File: " + self.outfile)
    # open the files
    fout = open(self.outfile, 'w')
    fopener = UtilsProcar()
    with fopener.OpenFile(self.infile) as fin:
      counter = 0
      for line in fin:
        # if any data found 
        if re.match(r"\s*\d", line):
          # check if should be written
          if counter in components:
            fout.write(line)
        elif re.match(r"\s*tot", line):
          if counter in components:
            fout.write(line)
          # the next block will belong to other component
          counter += 1
        elif re.match(r"\s*ion", line):
          fout.write(line)
          counter = 0
        else:
          fout.write(line)
    return



class ProcarSelect:
  """
  Reduces the dimensionality of the data making it uselful to
  plot bands.

  The main data to manipulate is the projected electronic structure. 
  Its shape original is:

  spd[kpoint][band][ispin][atom][orbital].

  The selection of components should be done in order, says, first
  "ispin", then "atom", and at last "orbital". 

  Note: once any selection has been performed, the data itself
  changes. Say, if you want compare atom [0] and [1,2], you need two
  instances of this class.


  Example to compare the bandstructure of two set of atoms
  >>>

  """
  def __init__(self, ProcarData=None, deepCopy=True, loglevel=logging.WARNING):
    
    self.spd = None
    self.bands = None
    self.kpoints = None

    # We want a logging to tell us what is happening
    self.log = logging.getLogger("ProcarSelect")
    self.log.setLevel(loglevel)
    self.ch = logging.StreamHandler()
    self.ch.setFormatter(logging.Formatter("%(name)s::%(levelname)s:"
                                           " %(message)s"))
    self.ch.setLevel(logging.DEBUG)
    self.log.addHandler(self.ch)
    # At last, one message to the logger.
    self.log.debug("ProcarSelect: instanciated")

    if ProcarData is not None:
      self.setData(ProcarData,deepCopy)
    return
  
  def setData(self, ProcarData, deepCopy=True):
    """
    The data from ProcarData is deepCopy-ed by default (ie: their
    elements are not modified by this class.   

    Args:

    -ProcarData: is a ProcarParser instance (or anything with similar
     functionality, duck typing)

    -deepCopy=True: If false a shallow copy will be made (saves memory).
    """
    self.log.debug("setData: ...")
    if deepCopy is True:
      self.spd     = ProcarData.spd.copy()
      self.bands   = ProcarData.bands.copy()
      self.kpoints = ProcarData.kpoints.copy()
    else:
      self.spd = ProcarData.spd
      self.bands = ProcarData.bands
      self.kpoints = ProcarData.kpoints
    self.log.debug("setData: ... Done")
    return
  
  def selectIspin(self, value):
    """
    value is a list with the values of Ispin to select.

    Example:
    >>> foo = ProcarParser()
    >>> foo.readFile("PROCAR")
    >>> bar = ProcarSelect(foo)
    >>> bar.selectIspin([0]) #just the density
    """
    #all kpoint, all bands, VALUE spin, all the rest
    self.log.debug("selectIspin: ...")
    self.log.debug( "old spd shape =" + str(self.spd.shape))
    self.spd = self.spd[:,:,value]
    self.spd = self.spd.sum(axis=2)
    self.log.info("new spd shape =" + str(self.spd.shape))
    self.log.debug("selectIspin: ...Done")
    return

  def selectAtoms(self, value, fortran=False):
    """
    value is a list with the values of Atoms to select. The optional
    `fortran` argument indicates whether a c-like 0-based indexing
    (`=False`, default) or a fortran-like 1-based (`=True`) is
    provided in `value`.

    Example:
    >>> foo = ProcarParser()
    >>> foo.readFile("PROCAR")
    >>> bar = ProcarSelect(foo)
    >>> bar.selectIspin([...])
    >>> bar.selectAtoms([0,1,2]) #atom0+atom1+atom2
    
    Note: this method should be called after select.Ispin
    """
    self.log.debug("selectAtoms: ...")

    #taking care about stupid fortran indexing
    if fortran is True:
      value = [ x-1 for x in value]

    #all kpoint, all bands, VALUE atoms, all the rest
    self.log.debug( "old shape =" + str(self.spd.shape))
    self.spd = self.spd[:,:,value]
    self.spd = self.spd.sum(axis=2)
    self.log.info( "new shape =" + str(self.spd.shape))
    self.log.debug("selectAtoms: ...Done")
    return

  def selectOrbital(self, value):
    """
    value is a list with the values of orbital to select.

    Example:
    >>> foo = ProcarParser()
    >>> foo.readFile("PROCAR")
    >>> bar = ProcarSelect(foo)
    >>> bar.selectIspin([...])
    >>> bar.selectAtoms([...])
    >>> bar.selectOrbital([-1]) #the last (`tot`) field
    
    to select "p" orbitals just change the argument in the last line
    to [2,3,4] or as needed

    Note: this method should be called after `select.Ispin` and
    `select.Atoms`
    """
    self.log.debug("selectOrbital: ...")
    self.log.debug("Changing the orbital `values` to have a 0-based indexes")
    #Mind: the first orbital field is the atoms number, which is not
    #an orbital, therefore the orbital index is an affective 1-based
    #therefore all `value` indexes += 1 (well, negative values do not
    #change )
    for i in range(len(value)):
      if value[i] >= 0:
        value[i] += 1

    self.log.debug("New values (indexes to select) :" + str(value))

    #all kpoint, all bands, VALUE orbitals, nothing else?
    self.spd = self.spd[:,:,value]
    self.log.debug( "old shape =" + str(self.spd.shape))
    self.spd = self.spd.sum(axis=2)
    self.log.info( "new shape =" + str(self.spd.shape))
    self.log.debug("selectOrbital: ...Done")
    return


class ProcarPlot:
  def __init__(self, bands, spd, kpoints=None):
    self.bands = bands.transpose()
    self.spd = spd.transpose()
    self.kpoints = kpoints
    return

  def plotBands(self, size=None, marker='o', ticks=None):
    if size is not None:
      size = size/2
    if self.kpoints is not None:
      xaxis = [0]
      for i in range(1,len(self.kpoints)):
        d = self.kpoints[i-1]-self.kpoints[i]
        d = np.sqrt(np.dot(d,d))
        xaxis.append(d+xaxis[-1])
      xaxis = np.array(xaxis)
    else:
      xaxis = np.arange(len(self.bands))
    print "self.kpoints: ", self.kpoints.shape
    print "xaxis.shape : ", xaxis.shape
    print "bands.shape : ", self.bands.shape
    plot = plt.plot(xaxis,self.bands.transpose(), 'r-', marker=marker, 
                    markersize=size)
    plt.xlim(xaxis.min(), xaxis.max())

    #handling ticks
    if ticks:
      ticks, ticksNames = zip(*ticks)
      ticks = [xaxis[x] for x in ticks]
      plt.xticks(ticks, ticksNames)
    
    return plot

  def scatterPlot(self, size=50, mask=None, cmap='hot_r', vmax=None, vmin=None,
                  marker='o', ticks=None):
    bsize, ksize = self.bands.shape
    print bsize, ksize

    if self.kpoints is not None:
      xaxis = [0]
      for i in range(1,len(self.kpoints)):
        d = self.kpoints[i-1]-self.kpoints[i]
        d = np.sqrt(np.dot(d,d))
        xaxis.append(d+xaxis[-1])
      xaxis = np.array(xaxis)
    else:
      xaxis = np.arange(ksize)

    xaxis.shape=(1,ksize)
    xaxis = xaxis.repeat(bsize, axis=0)
    if mask is not None:
      mbands = np.ma.masked_array(self.bands, np.abs(self.spd) < mask)
    else:
      mbands = self.bands
    plot = plt.scatter(xaxis, mbands, c=self.spd, s=size, linewidths=0,
                       cmap=cmap, vmax=vmax, vmin=vmin, marker=marker,
                       edgecolors='none')
    plt.xlim(xaxis.min(), xaxis.max())

    #handling ticks
    if ticks:
      ticks, ticksNames = zip(*ticks)
      ticks = [xaxis[0,x] for x in ticks]
      plt.xticks(ticks, ticksNames)

    return plot
    
  def parametricPlot(self, cmap='hot_r', vmin=None, vmax=None, mask=None, 
                     ticks=None):
    from matplotlib.collections import LineCollection
    import matplotlib
    fig = plt.figure()
    gca = fig.gca()
    bsize, ksize = self.bands.shape

    #print self.bands
    if mask is not None:
      mbands = np.ma.masked_array(self.bands, np.abs(self.spd) < mask)
    else:
      #Faking a mask, all elemtnet are included
      mbands = np.ma.masked_array(self.bands, False)
    #print mbands
    
    if vmin is None:
      vmin = self.spd.min()
    if vmax is None:
      vmax = self.spd.max()
    print "normalizing to: ", (vmin,vmax)
    norm = matplotlib.colors.Normalize(vmin, vmax)

    if self.kpoints is not None:
      xaxis = [0]
      for i in range(1,len(self.kpoints)):
        d = self.kpoints[i-1]-self.kpoints[i]
        d = np.sqrt(np.dot(d,d))
        xaxis.append(d+xaxis[-1])
      xaxis = np.array(xaxis)
    else:
      xaxis = np.arange(ksize)

    for y,z in zip(mbands,self.spd):
      #print xaxis.shape, y.shape, z.shape
      points = np.array([xaxis, y]).T.reshape(-1, 1, 2)
      segments = np.concatenate([points[:-1], points[1:]], axis=1)
      lc = LineCollection(segments, cmap=plt.get_cmap(cmap), norm=norm, 
                          alpha=0.8)
      lc.set_array(z)
      lc.set_linewidth(2)
      gca.add_collection(lc)
    plt.colorbar(lc)
    plt.xlim(xaxis.min(), xaxis.max())
    plt.ylim(mbands.min(), mbands.max())

    #handling ticks
    if ticks:
      ticks, ticksNames = zip(*ticks)
      ticks = [xaxis[x] for x in ticks]
      plt.xticks(ticks, ticksNames)

    return fig

  def atomicPlot(self, cmap='hot_r', vmin=None, vmax=None):
    """
    Just a handler to parametricPlot. Useful to plot energy levels. 

    It adds a fake k-point. Shouldn't be invoked with more than one
    k-point
    """

    print "Atomic plot: bands.shape  :", self.bands.shape
    print "Atomic plot: spd.shape    :", self.spd.shape
    print "Atomic plot: kpoints.shape:", self.kpoints.shape

    self.bands = np.hstack((self.bands, self.bands))
    self.spd = np.hstack((self.spd, self.spd))
    self.kpoints = np.vstack((self.kpoints, self.kpoints))
    self.kpoints[0][-1] += 1
    print "Atomic plot: bands.shape  :", self.bands.shape
    print "Atomic plot: spd.shape    :", self.spd.shape
    print "Atomic plot: kpoints.shape:", self.kpoints.shape

    print self.kpoints
    
    fig = self.parametricPlot(cmap, vmin, vmax)
    plt.gca().xaxis.set_major_locator(plt.NullLocator())

    # labels on each band
    for i in range(len(self.bands[:,0])):
      # print i, self.bands[i]
      plt.text(0, self.bands[i,0], str(i+1), fontsize=15)
    
    return fig


class FermiSurface:
  def __init__(self, kpoints, bands, spd, recbasis, loglevel=logging.WARNING):
    # Original Kpoints list (the PROCAR's default is in Direct coords!)
    self.kpoints  = kpoints  
    self.bands    = bands
    self.spd      = spd
    self.RecBasis = recbasis # Basis Vectors (Rec. Space), see Rec2Cart
    self.kcart    = None     # Kpoints in Cartesian coords (filled in Rec2Cart)
    self.useful   = None     # List of useful bands (filled in findEnergy)
    self.inversion = False
    self.order     = 1
    self.energy    = None

    self.log = logging.getLogger("FermiSurface")
    self.log.setLevel(loglevel)
    self.ch = logging.StreamHandler()
    self.ch.setFormatter(logging.Formatter("%(name)s::%(levelname)s: "
                                           "%(message)s"))
    self.ch.setLevel(logging.DEBUG)
    self.log.addHandler(self.ch)

    self.log.debug("FermiSurface: ...")
    self.log.info("Kpoints : " + str(self.kpoints))
    self.log.info("bands   : " + str(self.bands.shape))
    self.log.info("spd     : " + str(self.spd.shape))
    self.log.debug("FermiSurface: ...Done")
    return

  def Rec2Cart(self):
    self.log.debug("Rec2Cart: ...")
    self.kcart = self.kpoints.dot(self.RecBasis)
    self.log.debug("Rec2Cart: ...Done")
    
  def FindEnergy(self, energy):
    self.log.debug("FindEnergy: ...")
    self.energy = energy
    self.log.info("Energy   : " + str(energy))
    bands = self.bands.transpose()
    #searching bands who has a value at energy
    self.useful = np.where(np.logical_and(bands.min(axis=1)<energy,
                                          bands.max(axis=1)>energy))
    self.log.debug("set of useful bands    : " + str(self.useful))
    bands = bands[self.useful]
    self.log.debug("new bands.shape : " + str(bands.shape))
    self.log.debug("FindEnergy: ...Done")
    return

  def SetInversion(self, value=True):
    self.log.debug("SetInversion: ...")
    self.log.info("Applying inversion symmetry to the K-mesh")
    self.inversion = value
    self.log.debug("SetInversion: ...Done")
    return

  def SetRotAxis(self, order, axis="z"):
    self.log.debug("SetRotAxis: ...")
    self.log.info("axis     : " + str(axis))
    if axis not in ["x" ,"y", "z"]:
      self.log.error("Wrong axis argument")
      raise RuntimeError("axis is wrong!")
    
    self.log.info("rotational order : " + str(order))
    if order not in [1,2,3,4,6]:
      self.log.error("Wrong rotational order!")
      raise RuntimeError("rotational order is wrong")

    self.order = order
    self.log.debug("SetRotAxis: ...Done")
    return
  
  def ApplySymm(self, x, y, z):
    """Note that z does not rotates, only is repeated.  Also the 1st
    axis of z is a list of bands, and the second are their values.
    
    """
    
    self.log.debug("ApplySymm(): ...")
    #initialization
    xnew = x
    ynew = y
    znew = z
    self.log.debug("x.shape : " + str(x.shape))
    self.log.debug("y.shape : " + str(y.shape))
    self.log.debug("z.shape : " + str(z.shape))

    if self.order > 1: 
      self.log.info("Applying rotation symmetry, order :" + str(self.order))
    #The first rotation (no rotation) is already in the initailization
    for i in range(self.order-1):
      c,s = np.cos(2*np.pi/self.order), np.sin(2*np.pi/self.order)
      xnew,ynew = xnew*c - ynew*s,  xnew*s + ynew*c
      x = np.concatenate((x, xnew))
      y = np.concatenate((y, ynew))
      z = np.concatenate((z, znew), axis=1)
    self.log.debug("new x,y,z shapes : " + 
                   str(x.shape) + str(y.shape) + str(z.shape))

    if self.inversion: 
      self.log.info("Applying rotation symmetry : ")
      x = np.concatenate((x, -x))
      y = np.concatenate((y, -y))
      z = np.concatenate((z,  z), axis=1)
    

    self.log.debug("ApplySymm(): ...Done")
    return (x,y,z)


  def Plot(self, interpolation=200, mask=None):
    """Only 2D layer geometry along z"""
    self.log.debug("Plot: ...")
    from scipy.interpolate import griddata, interp2d
    
    if self.kcart is None:
      self.Rec2Cart()

    if self.useful is None:
      raise RuntimeError("FindEnergy must be called before Interpolate")


    #selecting components of K-points
    x,y = self.kcart[:,0], self.kcart[:,1]
    self.log.debug( "k_x[:10], k_y[:10] values" +  str([x[:10],y[:10]]))

    bands = self.bands.transpose()[self.useful]
    (x,y,bands) = self.ApplySymm(x,y, bands)


    #and new, interpolated component
    xmax,xmin = x.max(), x.min()
    ymax,ymin = y.max(), y.min()
    self.log.debug(      "xlim = " + str([xmin, xmax]) 
                    +  "  ylim = " + str([ymin, ymax]))
    xnew, ynew = np.mgrid[xmin:xmax:interpolation*1j, 
                          ymin:ymax:interpolation*1j]

    #interpolation
    bnew = []
    # spd = self.spd.transpose()[self.useful]
    # if mask is not None:
    #   to_mask = np.where(np.abs(spd) < mask)
    #   bands[to_mask] = np.nan
      
    for band in bands:
      #print x.shape, y.shape, band.shape
      self.log.debug("Interpolating ...")
      bnew.append( griddata((x,y), band, (xnew, ynew) ) )
      #print "interpolated data shape : ", bnew[-1].shape

    for i in range(1): # self.order):
      #print "going to plot"
      [plt.contour(xnew, ynew, z, [self.energy], linewidths=0.5,colors='k',
                   linestyles='solid') for z in bnew]

      # if self.inversion:
      #   [plt.contour(-xnew, -ynew, z, [self.energy], linewidths=0.5,colors='k',
      #                 linestyles='solid') for z in bnew]

      # c,s = np.cos(2*np.pi/self.order), np.sin(2*np.pi/self.order)
      
      # xnew,ynew = xnew*c - ynew*s,  xnew*s + ynew*c

    plt.axis("equal")

    #storing values
    self.log.debug("Plot: ...Done")
    return

  def st(self, sx, sy, sz, interpolation=200):
    """Only 2D layer geometry along z. It is like a enhanced version
    of 'plot' method."""
    self.log.debug("st: ...")
    from scipy.interpolate import griddata, interp2d, BivariateSpline
    
    if self.kcart is None:
      self.Rec2Cart()
    if self.useful is None:
      raise RuntimeError("FindEnergy must be called before")

    #selecting components of K-points
    xold,yold = self.kcart[:,0], self.kcart[:,1]

    bands = self.bands.transpose()[self.useful]
    (x,y,bands) = self.ApplySymm(xold,yold, bands)

    sx = sx.transpose()[self.useful]
    sy = sy.transpose()[self.useful]
    sz = sz.transpose()[self.useful]
    (x,y,sx) = self.ApplySymm(xold,yold, sx)
    (x,y,sy) = self.ApplySymm(xold,yold, sy)
    (x,y,sz) = self.ApplySymm(xold,yold, sz)

    #and new, interpolated component
    xmax,xmin = x.max(), x.min()
    ymax,ymin = y.max(), y.min()
    self.log.debug(      "xlim = " + str([xmin, xmax]) 
                    +  "  ylim = " + str([ymin, ymax]))
    xnew, ynew = np.mgrid[xmin:xmax:interpolation*1j, 
                          ymin:ymax:interpolation*1j]

    #interpolation
    bnew = []
    for band in bands:
      self.log.debug("Interpolating ...")
      bnew.append( griddata((x,y), band, (xnew, ynew) ) )

    cont = [plt.contour(xnew, ynew, z, [self.energy], linewidths=0.5,
                        colors='k', linestyles='solid') for z in bnew]
    plt.axis("equal")

    for (contour, spinX, spinY, spinZ) in zip(cont, sx, sy, sz):
      # The previous interp. yields the level curves, nothing more is
      # useful from there
      paths = contour.collections[0].get_paths()
      verts = [xx.vertices for xx in paths]
      points = np.concatenate(verts) 
      print "Fermi surf. points.shape", points.shape
      

      newSx = griddata((x,y), spinX, (points[:,0], points[:,1]))
      newSy = griddata((x,y), spinY, (points[:,0], points[:,1]))
      newSz = griddata((x,y), spinZ, (points[:,0], points[:,1]))
      
      print "newSx.shape: ", newSx.shape

      import matplotlib.colors as colors
      
      plt.quiver(points[::6,0], points[::6,1], newSx[::6], newSy[::6],
                 newSz[::6],scale_units='xy', angles='xy',
                 norm=colors.normalize(-0.5,0.5))
      plt.colorbar()
    plt.axis("equal")


    self.log.debug("st: ...Done")
    return



def scriptCat(args):
  if args.quiet is False:
    print   "Concatenating:"
    print   "Input         : ", ', '.join(args.inFiles)
    print   "Output        : ", args.outFile
    if args.gz:
      print "out compressed: True"
    if args.verbose > 2:
      args.verbose = 2
    if args.verbose:
      print "verbosity     : ", args.verbose 
  
  if args.gz and args.outFile[-3:] is not '.gz':
    args.outFile += '.gz'
    if args.quiet is False:
      print ".gz extension appended to the outFile"
  
  loglevel = {0:logging.WARNING, 1:logging.INFO, 2:logging.DEBUG}[args.verbose]
  handler = UtilsProcar(loglevel)
  handler.MergeFiles(args.inFiles, args.outFile, gzipOut=args.gz)
  return


def scriptFilter(args):
  if args.quiet is False:
    print "Input file  :", args.inFile
    print "Output file :", args.outFile
  if args.verbose:
    if args.verbose > 2:
      args.verbose = 2
    print "atoms       :", args.atoms
    if args.atoms:
      print "human_atoms :", args.human_atoms
    print "orbitals    :", args.orbitals
    if args.orbitals:
      print "orb. names  :", args.orbital_names
    print "bands       :", args.bands
    print "spins       :", args.spin



  loglevel = {0:logging.WARNING, 1:logging.INFO, 2:logging.DEBUG}[args.verbose]
  FileFilter = ProcarFileFilter(args.inFile, args.outFile, loglevel=loglevel)

  if args.atoms:
    if args.quiet is False:
      print "Manipulating the atoms"
    
    if args.human_atoms:
      args.atoms = [[y-1 for y in x] for x in args.atoms]
      if args.verbose:
        print "new atoms list :", args.atoms

    #Now just left to call the driver member
    FileFilter.FilterAtoms(args.atoms)
  
  elif args.orbitals:
    if args.quiet is False:
      print "Manipulating the orbitals"
    #If orbitals orbital_names is None, it needs to be filled
    if args.orbital_names is None:
      args.orbital_names = ["o"+str(x) for x in range(len(args.orbitals))]
      if args.quiet is False:
        print "New orbitals names (default): ", args.orbital_names
    #testing if makes sense
    if len(args.orbitals) != len(args.orbital_names):
      raise RuntimeError("length of orbitals and orbitals names do not match")
    
    FileFilter.FilterOrbitals(args.orbitals, args.orbital_names)

  elif args.bands:
    if args.quiet is False:
      print "Manipulating the bands"
    
    bmin = args.bands[0]
    bmax = args.bands[1]
    if bmax < bmin:
      bmax, bmin = bmin, bmax
      if args.quiet is False:
        print "New bands limits: ", bmin, " to ", bmax

    FileFilter.FilterBands(bmin,bmax)
    

  elif args.spin:
    if args.quiet is False:
      print "Manipulating the spin"

    FileFilter.FilterSpin(args.spin)

  return


def scriptBandsplot(args):

  if args.atoms is None:
    args.atoms = [-1]
    if args.human_atoms is True:
      print "WARNING: `--human_atoms` option given without atoms list!!!!!"
  if args.orbitals is None:
    args.orbitals = [-1]
    
  if args.verbose:
    print "Script initiated"
    print "input file    : ", args.file
    print "Mode          : ", args.mode
    
    print "spin comp.    : ", args.spin
    print "atoms list.   : ", args.atoms
    print "orbs. list.   : ", args.orbitals

  if args.fermi is None and args.outcar is None:
    print "Fermi Energy not set!!!" 
    args.fermi = 0

  if args.verbose:
    print "Fermi Ener.   : ", args.fermi
    print "Energy range  : ", args.elimit

    if args.mask is not None:
      print "masking thres.: ", args.mask
      
    print "Colormap      : ", args.cmap
    print "MarkerSize    : ", args.markersize
      
    print "Permissive    : ", args.permissive
    if args.permissive and args.quiet is False:
      print "Permissive flag is on! Be careful"
    print "vmax          : ", args.vmax
    print "vmin          : ", args.vmin
    print "grid enabled  : ", args.grid 
    if args.human_atoms is not None:
      print "human_atoms   : ", args.human_atoms
    print "Savefig       : ", args.savefig
    print "kticks        : ", args.kticks
    print "kticksnames   : ", args.kticksnames
    print "title         : ", args.title

    print "outcar        : ", args.outcar

  if args.kticks is not None and args.kticksnames is not None:
    ticks = zip(args.kticks,args.kticksnames)
  else:
    ticks = None

  if args.verbose > 2:
    args.verbose = 2
  loglevel = {0:logging.WARNING, 1:logging.INFO, 2:logging.DEBUG}[args.verbose]


  #first parse the outcar if given
  recLat = None #Will contain reciprocal vectors, if necessary
  if args.outcar:
    outcarparser = UtilsProcar(loglevel=loglevel)
    if args.fermi is None:
      args.fermi = outcarparser.FermiOutcar(args.outcar)
      if args.quiet is False:
        print "Fermi energy found in outcar file = " + str(args.fermi)
    recLat = outcarparser.RecLatOutcar(args.outcar)

  # parsing the PROCAR file
  procarFile = ProcarParser(loglevel=loglevel)
  procarFile.readFile(args.file, args.permissive, recLat)

  # processing the data
  data = ProcarSelect(procarFile, deepCopy=False, loglevel=loglevel)
  data.selectIspin([args.spin])
  # fortran flag is equivalent to human_atoms, 
  # but the later seems more human-friendly
  data.selectAtoms(args.atoms, fortran=args.human_atoms)
  data.selectOrbital(args.orbitals)

  ## Perpendicular to K: uncomment the following lines

  # dataX = ProcarSelect(procarFile, deepCopy=True, loglevel=loglevel)
  # dataX.selectIspin([1])
  # dataX.selectAtoms(args.atoms, fortran=args.human_atoms)
  # dataX.selectOrbital(args.orbitals)  
  # dataY = ProcarSelect(procarFile, deepCopy=True, loglevel=loglevel)
  # dataY.selectIspin([2])
  # dataY.selectAtoms(args.atoms, fortran=args.human_atoms)
  # dataY.selectOrbital(args.orbitals)
  # angle = np.arctan(dataX.kpoints[:,1]/(dataX.kpoints[:,0]+0.000000001))
  # sin = np.sin(angle)
  # cos = np.cos(angle)
  # sin.shape = (sin.shape[0],1)
  # cos.shape = (cos.shape[0],1)
  # #print angle*180/np.pi
  # #print sin, cos
  # #print dataX.spd.shape, sin.shape
  # #print sin*dataX.spd
  # data.spd = -sin*dataX.spd + cos*dataY.spd

  ## Perpendicular to K: end!

  # Plotting the data
  data.bands = (data.bands.transpose() - np.array(args.fermi)).transpose()
  plot = ProcarPlot(data.bands, data.spd, data.kpoints)

  ###### start of mode dependent options #########

  if args.mode == "scatter":
    plot.scatterPlot(mask=args.mask, size=args.markersize,
                     cmap=args.cmap, vmin=args.vmin,
                     vmax=args.vmax, marker=args.marker, ticks=ticks)
    plt.colorbar()
    plt.ylabel(r"Energy [eV]")
    if args.elimit is not None:
      plt.ylim(args.elimit)

  elif args.mode == "plain":
    plot.plotBands(args.markersize, marker=args.marker, ticks=ticks)
    plt.ylabel(r"Energy [eV]")
    if args.elimit:
      plt.ylim(args.elimit)
      
  elif args.mode == "parametric":
    plot.parametricPlot(cmap=args.cmap, vmin=args.vmin, vmax=args.vmax,
                        ticks=ticks)
    plt.ylabel(r"Energy [eV]")
    if args.elimit is not None:
      plt.ylim(args.elimit)

  elif args.mode == "atomic":
    plot.atomicPlot(cmap=args.cmap, vmin=args.vmin, vmax=args.vmax)
    plt.ylabel(r"Energy [eV]")
    if args.elimit is not None:
      plt.ylim(args.elimit)
  ###### end of mode dependent options ###########

  if args.grid:
    plt.grid()
  
  if args.title:
    plt.title(args.title)

  if args.savefig:
    plt.savefig(args.savefig,  bbox_inches=0)
  else:
    plt.show()

  return


def scriptFermi2D(args):
  if args.atoms is None:
    args.atoms = [-1]
    if args.human_atoms is True:
      print "WARNING: `--human_atoms` option given without atoms list!!!!!"

  if args.orbitals is None:
    args.orbitals = [-1]

  if args.rec_basis != None:
    args.rec_basis = np.array(args.rec_basis)
    args.rec_basis.shape = (3,3)

  if args.quiet is False:
    print "file           : ", args.file
    print "atoms          : ", args.atoms
    print "orbitals       : ", args.orbitals
    print "spin comp.     : ", args.spin
    print "energy         : ", args.energy
    print "fermi energy   : ", args.fermi
    print "Rec. basis     : ", args.rec_basis
    print "inversion sym. : ", args.inversion
    print "rot. symmetry  : ", args.rotation
    print "masking thres. : ", args.mask
    print "save figure    : ", args.savefig
    print "outcar         : ", args.outcar
    print "st             : ", args.st

  if args.verbose > 2:
    args.verbose = 2
  loglevel = {0:logging.WARNING, 1:logging.INFO, 2:logging.DEBUG}[args.verbose]

  #first parse the outcar if given
  if args.rec_basis is None and args.outcar:
    outcarparser = UtilsProcar(loglevel=loglevel)
    if args.fermi is None:
      args.fermi = outcarparser.FermiOutcar(args.outcar)
      if args.quiet is False:
        print "Fermi energy found in outcar file = " + str(args.fermi)
    args.rec_basis = outcarparser.RecLatOutcar(args.outcar)


  #parsing the file
  procarFile = ProcarParser(loglevel)
  procarFile.readFile(args.file)

  if args.st is not True:

    # processing the data
    data = ProcarSelect(procarFile, deepCopy=False, loglevel=loglevel)
    data.selectIspin([args.spin])
    # fortran flag is equivalent to human_atoms,
    # but the later seems more human-friendly
    data.selectAtoms(args.atoms, fortran=args.human_atoms)
    data.selectOrbital(args.orbitals)

  else:
    # first get the sdp reduced array for all spin components.
    stData = []
    for i in [1,2,3]:
      data = ProcarSelect(procarFile, deepCopy=False, loglevel=loglevel)
      data.selectIspin([i])
      data.selectAtoms(args.atoms, fortran=args.human_atoms)
      data.selectOrbital(args.orbitals)
      stData.append(data.spd)


  # plotting the data
  fs = FermiSurface(data.kpoints, data.bands-args.fermi, data.spd, 
                    recbasis=args.rec_basis, loglevel=loglevel)
  fs.FindEnergy(args.energy)
  
  # going to real space and interpolating
  # now applying all symmetry operations
  fs.SetRotAxis(args.rotation,"z")
  fs.SetInversion(args.inversion)
  if not args.st:
    fs.Plot(mask=args.mask, interpolation=300)
  else:
    fs.st(sx=stData[0], sy=stData[1], sz=stData[2])
  
  if args.savefig:
    plt.savefig(args.savefig)
  else:
    plt.show()
    


  return


def scriptVector(args):
  if args.quiet is False:
    print "Input File    : ", args.infile
    print "Bands         : ", args.bands
    print "Energy        : ", args.energy
    print "Fermi         : ", args.fermi
    print "outcar        : ", args.outcar
    print "atoms         : ", args.atoms
    print "orbitals      : ", args.orbitals
    print "scale factor  : ", args.scale

  if args.bands is [] and args.energy is None:
    raise RuntimeError("You must provide the bands or energy.")
  if args.fermi == None and args.outcar == None:
    print "WARNING: Fermi's Energy not set"
  if args.verbose > 2:
    args.verbose = 2
  loglevel = {0:logging.WARNING, 1:logging.INFO, 2:logging.DEBUG}[args.verbose]

  #first parse the outcar if given
  recLat = None #Will contain reciprocal vectors, if necessary
  if args.outcar:
    outcarparser = UtilsProcar(loglevel=loglevel)
    if args.fermi is None:
      args.fermi = outcarparser.FermiOutcar(args.outcar)
      if args.quiet is False:
        print "Fermi energy found in outcar file = " + str(args.fermi)
    recLat = outcarparser.RecLatOutcar(args.outcar)

  if args.atoms is None:
    args.atoms = [-1]
  if args.orbitals is None:
    args.orbitals = [-1]
  

  #parsing the file
  procarFile = ProcarParser(loglevel=loglevel)
  procarFile.readFile(args.infile, recLattice=recLat)

  #processing the data
  sx = ProcarSelect(procarFile, deepCopy=True, loglevel=loglevel)
  sx.selectIspin([1])
  sx.selectAtoms(args.atoms)
  sx.selectOrbital(args.orbitals)

  sy = ProcarSelect(procarFile, deepCopy=True, loglevel=loglevel)
  sy.selectIspin([2])
  sy.selectAtoms(args.atoms)
  sy.selectOrbital(args.orbitals)

  sz = ProcarSelect(procarFile, deepCopy=True, loglevel=loglevel)
  sz.selectIspin([3])
  sz.selectAtoms(args.atoms)
  sz.selectOrbital(args.orbitals)

  x = sx.kpoints[:,0]
  y = sx.kpoints[:,1]
  z = sx.kpoints[:,2]

  #if energy was given I need to find the bands indexes crossing it
  if args.energy != None:
    FerSurf = FermiSurface(sx.kpoints, sx.bands-args.fermi,
                           sx.spd, recLat, loglevel)
    FerSurf.FindEnergy(args.energy)
    args.bands = list(FerSurf.useful[0])
    print "Bands indexes crossing Energy  ", args.energy, ", are: ", args.bands
  

  from mayavi import mlab

  fig = mlab.figure(bgcolor=(1,1,1))

  for band in args.bands:
    #z = sx.bands[:,band]-args.fermi
    u = sx.spd[:, band]
    v = sy.spd[:, band]
    w = sz.spd[:, band]
    scalar = w

    vect = mlab.quiver3d(x, y, z, u, v, w, scale_factor=args.scale,
                  scale_mode='vector', scalars=scalar, mode='arrow',
                  colormap='jet')
    vect.glyph.color_mode = 'color_by_scalar'
    vect.scene.parallel_projection = True
    vect.scene.z_plus_view()

    #tube= mlab.plot3d(x,y,z, tube_radius=0.0050, color=(0.5,0.5,0.5))
  mlab.show()


def scriptRepair(args):
  if args.quiet is False:
    print "Input File    : ", args.infile
    print "Output File   : ", args.outfile
  
  if args.verbose > 2:
    args.verbose = 2
  loglevel = {0:logging.WARNING, 1:logging.INFO, 2:logging.DEBUG}[args.verbose]

  #parsing the file
  handler = UtilsProcar(loglevel=loglevel)
  handler.ProcarRepair(args.infile, args.outfile)



if __name__ == "__main__":
  import argparse

  description = ("procar.py: a python library/script to manipulate and "
                 "plot VASP's PROCAR files.")
  #A top-level parser 
  parser = argparse.ArgumentParser(description=description)
  subparsers   = parser.add_subparsers(help='sub-command')

  ############## cat #####################
  phelp = ("concatenation of PROCARs files, they should be compatible (ie: "
           "joining parts of a large bandstructure calculation).")
  parserCat = subparsers.add_parser('cat', help=phelp)

  phelp = ("Input files. They can be compressed")
  parserCat.add_argument('inFiles', nargs='+', help=phelp)

  phelp = ("Output file.")
  parserCat.add_argument('outFile', help=phelp)

  phelp = ("Writes a gzipped outfile (if needed a .gz extension automatically "
           "will be added)")
  parserCat.add_argument('--gz', help=phelp , action='store_true')

  VerbCat = parserCat.add_mutually_exclusive_group()
  VerbCat.add_argument("-v", "--verbose", action="count", default=0)
  VerbCat.add_argument("-q", "--quiet", action="store_true")

  parserCat.set_defaults(func=scriptCat)

  ############## filter ###################
  phelp = ("Filters (manipulates) the data of the input file (PROCAR-like) and"
           " it yields a new file (PROCAR-like too) with the changes. This "
           "method can do only one manipulation at time (ie: spin, atoms, "
           "bands or orbitals).")
  parserFilter = subparsers.add_parser('filter', help=phelp)

  phelp = ("Input file. Can be compressed")
  parserFilter.add_argument('inFile' , help=phelp)

  phelp = ('Output file.')
  parserFilter.add_argument('outFile', help=phelp)

  VerbFilter = parserFilter.add_mutually_exclusive_group()
  VerbFilter.add_argument("-v", "--verbose", action="count", default=0)
  VerbFilter.add_argument("-q", "--quiet", action="store_true")

  OptFilter = parserFilter.add_mutually_exclusive_group()
  phelp =  ("List of atoms to group (add) as a new single entry. Each group of"
            " atoms should be specified in a different `--atoms` option. "
            "Example: `procar.py filter in out -a 0 1 -a 2` will group the 1st"
            " and 2nd atoms, while keeping the 3rd atom in `out` (any atom "
            "beyond the 3rd will be discarded). Mind the last atomic field "
            "present on a PROCAR file, is not an atom, is the 'tot' value (sum"
            " of all atoms), this field always is included in the outfile and "
            "it always is the 'tot' value from infile, regardless the selection"
            " of atoms.")
  OptFilter.add_argument("-a", "--atoms", type=int, nargs='+', action='append',
                         help=phelp)

  phelp = ("List of orbitals to group as a single entry. Each group of "
           "orbitals needs a different `--orbitals` list. By instance, to "
           "group orbitals in 's','p', 'd' it is needed `-o 0 -o 1 2 3 -o 4 5 "
           "6 7 8`. Where 0=s, 1,2,3=px,py,pz, 4...9=dxx...dyz. Mind the last "
           "value (aka) 'tot' always is written.")
  OptFilter.add_argument("-o", "--orbitals", help=phelp, type=int, nargs='+',
                         action='append')
  
  phelp = ("Keeps only the bands between `min` and `max` indexes. To keep the "
           "bands from 120 to 150 you should give `-b 120 150 `. It is not "
           "obvious which indexes are in the interest region, therefore I "
           "recommend you trial and error ")
  OptFilter.add_argument("-b", "--bands", help=phelp,  type=int, nargs=2)

  phelp = ("Which spin components should be written: 0=density, 1,2,3=Sx,Sy,Sz."
           " They are not averaged.")
  OptFilter.add_argument("-s", "--spin", help=phelp, type=int, nargs='+')


  phelp = ("enable to give atoms list in a more human, 1-based order (say the"
           " 1st is 1, 2nd is 2 and so on ). Mind: this only holds for atoms.")
  parserFilter.add_argument("--human_atoms", help=phelp, action="store_true")

  phelp = ("List of names of new 'orbitals' to appear in the new file, eg. "
           "(`--orbital_names s p d` for a 's', 'p', 'd'). Only meaningful "
           "when manipulating the orbitals, ie: using `-o` ")
  parserFilter.add_argument("--orbital_names", help=phelp, nargs='+' )

  parserFilter.set_defaults(func=scriptFilter)


  ############## bandsplot ###################
  phelp =("Bandstructure plot. This kind of plot can be fairly complex, "
          "therefore its worth to explore all options. If the file is large "
          "(>100MB) you should consider use the `filter` command before. Mind "
          " not all option are meaningful (even considered) for all `modes`")
  parserBandsplot = subparsers.add_parser('bandsplot', help=phelp)

  phelp = ("Input file. It can be compressed")
  parserBandsplot.add_argument('file' , help=phelp)

  VerbBandsPlot = parserBandsplot.add_mutually_exclusive_group()
  VerbBandsPlot.add_argument("-v", "--verbose", action="count", default=0)
  VerbBandsPlot.add_argument("-q", "--quiet", action="store_true")

  phelp = ("Mode of plot: 'scatter' is a points plot with the color given by "
           "the chosen projection. 'parametric' is like scatter, but with "
           "lines instead of points (bands crossings are not handled, and some"
           " unphysical 'jumps' can be present). 'plain' is a featureless "
           "bandstructure ignoring all data about projections.")
  choices = ["scatter","plain","parametric", "atomic"]
  parserBandsplot.add_argument("-m", "--mode", help=phelp, default="scatter",
                               choices=choices)
  
  phelp = ("Spin component to be used: for non-polarized calculations density "
           "is '-s 0'. Non-collinear calculation: density=0, sx=1, sy=2, sz=3."
           "Collinear polarized calculation is not suported yet. Default: s=0")
  parserBandsplot.add_argument("-s", "--spin" , type=int, choices=[0,1,2,3],
                               default=0, help=phelp)

  phelp = ("List of atoms to be used (0-based): ie. '-a 0 2' to select the 1st"
           " and 3rd. It defaults to the last one (-a -1 the 'tot' entry)")
  parserBandsplot.add_argument("-a", "--atoms" , type=int, nargs='+', 
                               help=phelp)

  phelp = ("Orbital index(es) to be used 0-based. Take a look to the PROCAR "
           "file. Its default is the last field (ie: 'tot'). From a standard "
           "PROCAR: `-o 0`='s', `-o 1 2 3`='p', `-o 4 5 6 7 8`='d'.")
  parserBandsplot.add_argument("-o", "--orbitals" , type=int, nargs='+',
                               help=phelp)

  phelp = ("Set the Fermi energy (or any reference energy) as zero. To get it "
           "you should `grep E-fermi` the self-consistent OUTCAR. See "
           "`--outcar`. Also a set of k-dependant 'fermi energies' are accepted"
           ", this is useful to compare several systems")
  parserBandsplot.add_argument("-f", "--fermi" , type=float, help=phelp,
                               nargs='+')

  phelp = ("Min/Max energy to be ploted. To plot [-1,1] centered in E_F: "
           "`--elimit -1 1`")
  parserBandsplot.add_argument("--elimit" , type=float, nargs=2, help=phelp)

  phelp = ("If set, masks(hides) values lowers than it. Useful to remove "
           "unwanted bands. For instance, if you project the bandstructure on"
           " a 'surface' atom -with the default colormap- some white points "
           "can appear, they shows that there are bands with almost no "
           "contribution to the 'surface', to hide these bands use `--mask "
           "0.08` (or some other small value). Mind: it works with the "
           "absolute value of projection (no problem with spin texture)")
  parserBandsplot.add_argument("--mask" , type=float, help=phelp)

  phelp = ("Size of markers, if used. Mind each mode has it own scale, "
           "therefore you should test them")
  parserBandsplot.add_argument("--markersize", type=float, help=phelp, 
                               default=10)

  phelp = ("colormap name (google 'matplotlib colormap'). For spin-texture"
           "I recommend 'seismic'. Reverse a scale append a '_r' ie: "
           "'seismic'->'seismic_r'")
  parserBandsplot.add_argument("--cmap" , help=phelp, default="hot_r")

  phelp = ("max. value of the parameter (ie: projection on something given by "
           "-a, -o or -s) to plot (ie: 1). There is no default, so if to "
           "compare two plots with the same scale, this is the way to do it")
  parserBandsplot.add_argument("--vmax" , type=float, help=phelp)

  phelp = ("min. value of the parameter to plot. See `--vmax` ")
  parserBandsplot.add_argument("--vmin" , type=float, help=phelp)  

  phelp = ("switch on/off the grid. Default is 'on'")
  parserBandsplot.add_argument("--grid", type=bool, help=phelp, default=True)

  phelp = ("set the marker shape, ie: 'o'=circle, 's'=square,\ '-'=line"
           "(only mode `plain`)")
  parserBandsplot.add_argument("--marker", type=str, help=phelp, default='o')

  phelp = ("Some fault tolerance for ill-formatted files (stupid fortran)"
           "But be careful, something could be messed up and don't work (at "
           "least as expected)")
  parserBandsplot.add_argument("--permissive", help=phelp, action='store_true')

  phelp = ("Enable human-like 1-based order (ie 1st is 1, 2nd is 2, and so "
           "on). Mind: this only works for atoms!")
  parserBandsplot.add_argument("--human_atoms", help=phelp,action="store_true")

  phelp = ("Saves the figure, instead of display it on screen. Anyway, you can"
           " save from the screen too. Any file extension supported by "
           "`matplotlib.savefig` is valid (if you are too lazy to google it, "
           "trial and error also works)")
  parserBandsplot.add_argument('--savefig' , help=phelp)

  phelp = ("list of ticks along the kpoints axis (x axis). For instance a "
           "bandstructure G-X-M with 10 point by segment should be: "
           "`--kticks 0 9 19` ")
  parserBandsplot.add_argument('--kticks' , help=phelp, nargs='+', type=int)

  phelp = ("Names of the points given in `--kticks`. In the `kticks` example "
           "they should be `--kticksnames \"\$Gamma\$\" X M`. As you can see "
           "LaTeX stuff works with a minimal mess (extra \\s)")
  parserBandsplot.add_argument('--kticksnames' , help=phelp, nargs='+', 
                               type=str)

  phelp = ("Title, to use several words, use quotation marks\"\" or ''. Latex"
           " works if you scape the special characteres, ie: $\\alpha$ -> "
           "\$\\\\alpha\$")
  parserBandsplot.add_argument('-t', '--title' , help=phelp, type=str)

  phelp = ("OUTCAR file where to find the reciprocal lattice vectors and "
           "perhaps E_fermi. Mind: '--fermi' has precedence, remember that the"
           " E-fermi should correspond to a self-consistent run, not a "
           "bandstructure! (however, this is irrelevant for basis vectors)")
  parserBandsplot.add_argument('--outcar', help=phelp)


  parserBandsplot.set_defaults(func=scriptBandsplot)

  ################# Fermi ####################


  phelp = ("Plot the Fermi surface for a 2D Brillouin zone (layer-wise)"
           " along z")
  parserFermi2D  = subparsers.add_parser('fermi2D', help=phelp)

  phelp = ("Input file. It Can be compressed")
  parserFermi2D.add_argument('file' , help=phelp)


  VerbFermi2D = parserFermi2D.add_mutually_exclusive_group()
  VerbFermi2D.add_argument("-v", "--verbose", action="count", default=0)
  VerbFermi2D.add_argument("-q", "--quiet", action="store_true")


  phelp = ("Spin component to be used: for non-polarized calculations density "
           "is '-s 0'. Non-collinear calculation: density=0, sx=1, sy=2, sz=3."
           "Collinear polarized calculation is not suported yet. Default: s=0")
  parserFermi2D.add_argument("-s", "--spin" , type=int, choices=[0,1,2,3], 
                             default=0, help=phelp)

  phelp = ("List of atoms to be used (0-based): ie. '-a 0 2' to select the 1st"
           " and 3rd. It defaults to the last one (-a -1 the 'tot' entry)")
  parserFermi2D.add_argument("-a", "--atoms", type=int, nargs='+', help=phelp)

  phelp = ("Orbital index(es) to be used 0-based. Take a look to the PROCAR "
           "file. Its default is the last field (ie: 'tot'). From a standard "
           "PROCAR: `-o 0`='s', `-o 1 2 3`='p', `-o 4 5 6 7 8`='d'.")
  parserFermi2D.add_argument("-o", "--orbitals", type=int, nargs='+', 
                             help=phelp)

  phelp = ("Energy for the surface. To plot the Fermi surface at Fermi Energy "
           "`-e 0`")
  parserFermi2D.add_argument("-e", "--energy", help=phelp, type=float,
                             required=True)

  phelp = ("Set the Fermi energy (or any reference energy) as zero. To get it "
           "you should `grep E-fermi` the self-consistent OUTCAR. See "
           "`--outcar`")
  parserFermi2D.add_argument("-f", "--fermi", help=phelp, type=float)

  phelp = ("reciprocal space basis vectors. 9 number are required b1x b1y ... "
           " b3z. This option is quite involved, so I recommend you to use "
           "`--outcar`")
  parserFermi2D.add_argument("--rec_basis", help=phelp, type=float, nargs=9)

  phelp = ("Switch on (apply it) inversion symmetry (just to the plot, after "
           "interpolation the data)")
  parserFermi2D.add_argument("-i", "--inversion", help=phelp, 
                             action="store_true")

  phelp = ("Switch on (apply it) rotational symmetry to the plot. It requires "
           "the order of the rotation")
  parserFermi2D.add_argument("-r", "--rotation", help=phelp, type=int, default=1)

  phelp = ("enable to give atoms list"
                             " in a more human, 1-based way (say the 1st is 1,"
                             " 2nd is 2 and so on )")
  parserFermi2D.add_argument("--human_atoms", help=phelp, action="store_true")

  phelp = ("If set, masks(hides)"
                             " values lowers than it. Useful to remove "
                             "unwanted bands.")
  parserFermi2D.add_argument("--mask" , type=float, help=phelp)

  phelp = ("Saves the figure, instead of "
                             "display it on screen. Anyway, you can save from"
                             " the screen too. Any file extension supported by"
                             "matplotlib.savefig is valid (if you are too lazy"
                             " to google it, trial and error also works)")
  parserFermi2D.add_argument('--savefig' , help=phelp)
  
  phelp = ("OUTCAR file where to find the reciprocal lattice vectors and "
           "perhaps E_fermi. Mind: '--fermi' has precedence, remember that the"
           " E-fermi should correspond to a self-consistent run, not a "
           "bandstructure! (however, this is irrelevant for basis vectors)")
  parserFermi2D.add_argument('--outcar', help=phelp)
  
  phelp = ("Plot of the spin texture (ie: spin arrows) on the Fermi's surface."
           " This option works quite indepentent of another options.")
  parserFermi2D.add_argument('--st', help=phelp, action='store_true')

  parserFermi2D.set_defaults(func=scriptFermi2D)


  ################## vector #################
  
  #only for non-collinear bandstructures

  phelp = ("Plots the bands (some of them) as a vector field. It uses Mayavi.")
  parserVector = subparsers.add_parser('Vector', help=phelp)

  phelp = ("Input file. Can be compressed")
  parserVector.add_argument('infile' , help=phelp)

  VerbVector = parserVector.add_mutually_exclusive_group()
  VerbVector.add_argument("-v", "--verbose", action="count", default=0)
  VerbVector.add_argument("-q", "--quiet", action="store_true")

  EnVector = parserVector.add_mutually_exclusive_group()
  phelp = ("Band(s) to plot, by bands index")
  EnVector.add_argument("-b", "--bands", nargs='+', type=int, help=phelp)
  phelp = ("Band(s) to plot, by Energy")
  EnVector.add_argument("-e", "--energy", type=float, help=phelp)

  phelp = ("Fermi level. All energies will be referred to it as zero")
  parserVector.add_argument('-f ', '--fermi', type=float, help=phelp)
 
  phelp = ("List of atoms to consider (add their contribution)")
  parserVector.add_argument('-a ', '--atoms', type=int, nargs='+', help=phelp)

  phelp = ("List of orbital to consider (add their proj.)")
  parserVector.add_argument('-o ', '--orbitals', type=int, nargs='+', 
                            help=phelp)

  phelp = ("OUTCAR file where to grep the reciprocal lattice vectors and "
           "perhaps E_fermi. Mind: '--fermi' has precedence, remember that "
           "the E-fermi should correspond to a self-consistent run, not a "
           "bandstructure!")
  parserVector.add_argument('--outcar', help=phelp)

  phelp = ("Scale factor, to avoid too large arrows")
  parserVector.add_argument('--scale', type=float, default=0.1, help=phelp)


  parserVector.set_defaults(func=scriptVector)

  
  ################## repair #################

  phelp = ("Attemp to repair a Procar file form some fixed format problems.")
  parserRepair = subparsers.add_parser('repair', help=phelp)

  phelp = ("Input file. Can be compressed")
  parserRepair.add_argument('infile' , help=phelp)

  phelp = ("Output file")
  parserRepair.add_argument('outfile' , help=phelp)

  VerbRepair = parserRepair.add_mutually_exclusive_group()
  VerbRepair.add_argument("-v", "--verbose", action="count", default=0)
  VerbRepair.add_argument("-q", "--quiet", action="store_true")

  parserRepair.set_defaults(func=scriptRepair)



  args = parser.parse_args()
  args.func(args)
  

