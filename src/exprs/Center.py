"""
$Id$

will be renamed or merged

maybe rename to transforms.py, include things like Rotate and Closer

see also Rotated and Closer in testdraw1, for sample opengl code, showing how simple it ought to be
(except that makes no provision for highlighting, which i need to do using move methods or the equiv)
"""

##k [obs cmt, or not? guess not:] it doesn't work yet to actually delegate, eg for lbox attrs,
# so I don't think using an Overlay inside another one would work right now

from basic import *
from basic import _self

from OpenGL.GL import glTranslatef ###e later do this thru glpane object

###e [semiobs cmt:]
# these vec routines are not best.. what's best is to turn into (not away from) numeric arrays, for their convenience.
# guess: convention should be to always pass 3dim numeric arrays, and keep 3dim bboxes.
# let 2d routines not use z but still have it, that way same code can do 2d & 3d stuff, no constant checks for len 2 vecs, etc.
# but the above is nim in this code.

def tuple3_from_vec(vec): #stub, but might be enough for awhile
    "turn all kinds of 2D or 3D vecs (tuples or Numeric arrays of ints or floats) into 3-tuples (of ints or floats)"
    try:
        x,y,z = vec
    except:
        x,y = vec
        z = 0
    return x,y,z

def tuple2_from_vec(vec):
    x,y,z = tuple3_from_vec(vec)
    return x,y

class Translate(Widget, DelegatingMixin):
    "Translate(thing, vec) translates thing (and its bounding box, 2D or 3D) by vec (2 or 3 components)."
    # 3D aspect might be nim
    # lbox effect might be nim
    thing = Arg(Widget)
    delegate = _self.thing
    vec = Arg(Vector)
    # methods needed by all layout primitives: move & draw (see Column) & maybe kid (needed for highlighting, maybe not yet called)
    def move(self, i, j):
        "move from i to j, where both indices are encoded as None = self and 0 = self.thing"
        #e we might decide to only bother defining the i is None cases, in the API for this, only required for highlighting;
        # OTOH if we use it internally we might need both cases here
        x,y,z = tuple3_from_vec(self.vec)
        if i is None and j == 0:
            glTranslatef(x,y,z)
        elif i == 0 and j is None:
            glTranslatef(-x, -y, -z)
        return
    def kid(self, i):
        assert i == 0
        return self.thing
    ###e note: as said in notesfile, the indices for these drawn kids *could differ* from these arg indices if I wanted...
    # or I could instead define a dict...
    def draw(self):
        self.move(None, 0)
        self.thing.draw()
            # draw kid number 0 -- ##k but how did we at some point tell that kid that it's number 0, so it knows its ipath??
            ##k is it worth adding index or ipath as a draw-arg? (I doubt it, seems inefficient for repeated drawing)
        self.move(0, None)
        return
    pass

class Center(InstanceMacro):
    "Center(thing) draws as thing (a Widget2D [#e should make work for 3D too]), but is centered on the origin"
    # args
    thing = Arg(Widget2D)
    # internal formulas - decide how much to translate thing
    dx = (thing.bright - thing.bleft)/2.0
    dy = (thing.btop - thing.bbottom)/2.0
    # value
    ###k for now, use V_expr instead of V when it has expr args... not sure we can get around this (maybe redef of V will be ok??)
    _value = Translate(thing, -V_expr(dx,dy,0)) # this translates both thing and [nim] its layout box ###k might not work with V(expr...)
    pass

# status of Center, 061111:
# - untested
# - bbox motion in translate is nim, might matter later, not much for trivial tests tho
