# Copyright 2007-2008 Nanorex, Inc.  See LICENSE file for details. 
"""
FeatureDescriptor.py - descriptor objects for program features

@author: Bruce
@version: $Id$
@copyright: 2007-2008 Nanorex, Inc.  See LICENSE file for details. 
"""

# == constants

_KLUGE_PERMIT_INHERITED_CLASSNAMES = (
    "Command",
    "basicMode",
    
    "Select_basicCommand", # abstract, but has to be in this list
        # since it doesn't have its own featurename
    "Select_Command",
    "selectMode",

    "SelectChunks_Command",
    "selectMolsMode",

    "SelectAtoms_Command",
    "selectAtomsMode",
    
    "BuildAtoms_Command",
    "depositMode",

    "Move_Command",
    "modifyMode",

    "TemporaryCommand_preMixin", # (should this count as abstract?)

    "minimalCommand", # (ditto)
    "minimalUsefulMode",

    "Example_TemporaryCommand_useParentPM", # abstract, but doesn't have its own featurename
 )

_KLUGE_ABSTRACT_CLASSNAMES = (
    # todo: replace with per-class __abstract = True
    "EditCommand",
    "ExampleCommand", # (why printed twice, when not in this list?)
    "TemporaryCommand_Overdrawing",
 )

# == global state

_descriptor_for_feature_class = {}
    # maps feature class to FeatureDescriptor

_descriptor_for_featurename = {}
    # maps featurename (canonicalized) to FeatureDescriptor;
    # (used to warn about duplicate featurenames,
    #  other than by subclasses not overriding one from a superclass)

_feature_classes = {}
    # maps feature class (abstract class) to descriptor constructor for it;
    # only for the classes directly passed to register_abstract_feature_class
    # (with descriptors), not for their subclasses.

_feature_class_tuple = () # tuple of feature classes, to be passed to issubclass

# ==

def short_class_name( clas):
    # todo: refile into utilities.constants; has lots of inlined uses
    # todo: generalize to non-class things
    return clas.__name__.split('.')[-1]
        
def canonicalize_featurename( featurename, warn = False):
    # refile? does part of this function already exist elsewhere?

    featurename0 = featurename
    
    featurename = featurename.strip()

    # turn underscores to blanks [bruce 080717, to work around
    # erroneous underscores used in some featurename constants;
    # bad effect: it also removes at least one correct one,
    # in featurename = "Test Command: PM_Widgets Demo";
    # nonetheless this is necessary to make sure wiki help URLs
    # don't coincide (since those contain '_' in place of ' ')]
    
    featurename = featurename.replace('_', ' ')

    if warn and featurename != featurename0:
        msg = "developer warning: featurename %r was canonicalized to %r" % \
              ( featurename0, featurename )
        print msg

    return featurename

# ==

def register_abstract_feature_class( feature_class, descriptor_constructor = None ):
    global _feature_class_tuple
    if descriptor_constructor is None:
        # assert that we're a subclass of an existing feature class
        assert issubclass( feature_class, _feature_class_tuple )
        # record this class so we'll know it's abstract if we encounter it
        assert 0, "nim"
    else:
        _feature_classes[ feature_class ] = descriptor_constructor
        _feature_class_tuple = tuple( _feature_classes.keys() )
    return

# ==

def find_or_make_descriptor_for_possible_feature_object( thing):
    """
    @param thing: anything which might be found as a global value in some module

    @return: descriptor (found or made) for program feature represented
             by thing, or None if thing doesn't represent a program feature.
    @rtype: FeatureDescriptor or None
    """
    # so far, all features are represented by subclasses of
    # registered abstract feature classes.
    # (someday there might be other kinds of features,
    #  e.g. plugins discovered at runtime and represented
    #  by instance objects or separately created descriptors.)

    try:
        foundone = issubclass( thing, _feature_class_tuple )
    except:
        # not a class
        return None

    if not foundone:
        # not a subclass of a registered feature class
        return None

    # thing is a subclass of some class in _feature_class_tuple
    return find_or_make_FeatureDescriptor( thing)

# ==

def find_or_make_FeatureDescriptor( thing):
    """
    @param thing: the program object or class corresponding internally to a
                  specific program feature, or any object of the "same kind"
                  (presently, any subclass of an element of _feature_class_tuple)
    
    @return: FeatureDescriptor for thing (found or made),
             or None if thing does not describe a program feature.
    @rtype: FeatureDescriptor or None

    @note: fast, if descriptor is already known for thing

    @see: find_or_make_descriptor_for_possible_feature_object, for when
          you want to call something like this on an arbitrary Python object.
    """

    try:
        # note: thing is hashable, since it's a class
        return _descriptor_for_feature_class[thing]
    except KeyError:
        pass

    res = _determine_FeatureDescriptor( thing) # might be None
    
    # However we got the description (even if we're reusing one),
    # cache it, to optimize future calls and prevent redundant warnings.

    _descriptor_for_feature_class[thing] = res

    return res

def _determine_FeatureDescriptor( thing):
    """
    Determine (find or make) and return the FeatureDescriptor
    to use with thing.

    @param thing: an object or class corresponding internally
                  to a specific program feature, and for which
                  no descriptor is already cached
                  (though we might return one which was already
                   cached for a different thing, e.g. a superclass).

    @note: for now, this can only handle classes,
           and only if they have a superclass that has been registered
           with register_abstract_feature_class.
    """
    assert issubclass( thing, _feature_class_tuple), \
           "wrong kind of thing: %r" % (thing,)
        # note: this fails with some kind of exception for non-classes,
        # and with AssertionError for classes that aren't a subclass of
        # a registered class
    
    clas = thing
    del thing
    
    featurename = clas.featurename # note: not yet canonicalized

    # see if featurename is inherited

    inherited_from = None # might be changed below
    
    for base in clas.__bases__: # review: use mro?
        inherited_featurename = getattr( base, 'featurename', None)
        if inherited_featurename == featurename:
            inherited_from = base
            break

    short_name = short_class_name( clas)

    if inherited_from is not None:
        # decide whether this is legitimate (use inherited description),
        # or not (warn, and make up a new description).

        assert not clas in _feature_class_tuple

        legitimate = short_name in _KLUGE_PERMIT_INHERITED_CLASSNAMES
            # maybe: also add ways to register such classes,
            # and/or to mark them using __abstract = True
            # (made unique to that class by name-mangling).

            # maybe: point out in warning if it ends with Mode or Command
            # (but not with basicCommand) (probably not worth the trouble)

        if legitimate:
            return find_or_make_FeatureDescriptor( inherited_from)
                # return that even if it's None (meaning we're an abstract class)

        # make it unique
        featurename = canonicalize_featurename( featurename, warn = True)
        featurename = featurename + " " + short_name
        print "developer warning: auto-extending inherited featurename to make it unique:", featurename
        pass # use new featurename to make a new description, below

    else:
        # not inherited
        featurename = canonicalize_featurename( featurename, warn = True)
        assert not short_name in _KLUGE_PERMIT_INHERITED_CLASSNAMES, short_name
        pass

    # see if registered as abstract class
    
    if clas in _feature_class_tuple or short_name in _KLUGE_ABSTRACT_CLASSNAMES:
        return None

    # use featurename (perhaps modified above) to make a new description

    descriptor_constructor = _choose_descriptor_constructor( clas)

    descriptor = descriptor_constructor( clas, featurename )

    # warn if featurename is duplicated (but return it anyway)

    if _descriptor_for_featurename.has_key( featurename):
        print "developer warning: duplicate featurename %r for %r and %r" % \
              ( featurename,
                _descriptor_for_featurename[ featurename ].thing,
                descriptor.thing
               )
    else:
        _descriptor_for_featurename[ featurename] = descriptor

    return descriptor # from _determine_FeatureDescriptor

# ==

def _choose_descriptor_constructor( subclass):
    """
    subclass is a subclass of something in global _feature_classes
    (but not identical to anything in it);
    find the corresponding descriptor_constructor;
    if more than one matches, return the most specific (or error if we can't).
    """
    candidates = [(feature_class, descriptor_constructor)
                  for feature_class, descriptor_constructor in _feature_classes.iteritems()
                  if issubclass( subclass, feature_class )
                 ]
    assert candidates
    if len(candidates) == 1:
        return candidates[0][1]

    assert 0, "nim for multiple candidates (even when all values the same!): %r" % (candidates,)
    return candidates[0][1]

# ===

class FeatureDescriptor(object):
    """
    Abstract superclass for various kinds of feature descriptors.
    """
    def __init__(self, thing, featurename):
        self.thing = thing # rename?
        self.featurename = featurename
    pass

# ==

class basicCommand_Descriptor( FeatureDescriptor): # refile with basicCommand?
    """
    Descriptor for a command feature defined by any basicCommand subclass.
    """
    def __init__(self, command_class, featurename):
        FeatureDescriptor.__init__( self, command_class, featurename )
        ### TODO: initialize various metainfo

    def _get_command_class(self):
        return self.thing
    command_class = property( _get_command_class)

    def sort_key(self):
        # revise to group dna commands together, etc? or subcommands of one main command?
        # yes, when we have the metainfo to support that.
        
        return ( self.featurename, short_class_name( self.command_class) ) #e more?

    def print_plain(self):
        print "featurename:", self.featurename
        print "classname:", short_class_name( self.command_class)
        ### TODO: more
        
    pass

# end