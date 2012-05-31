from eulfedora.models import DigitalObject, XmlDatastream, Relation
from eulfedora.rdfns import relsext
from eulxml.xmlmap import mods

# TODO: make control pidspace configurable

class Collection(DigitalObject):
    '''
    Fedora Collection 1.0.  Implicit collection with Dublin Core
    descriptive metadata. Objects that belong to collection 1.1 objects are
    expected to be related to via *isMemberOfCollection*.  Could be a
    sub-collection of another Collection 1.0.
    '''
    COLLECTION_CONTENT_MODEL = 'info:fedora/emory-control:Collection-1.0'
    'content model'
    CONTENT_MODELS = [ COLLECTION_CONTENT_MODEL ]

    collection = Relation(relsext.isMemberOfCollection,
                          type='self')  
    '''Parent :class:`Collection` that this collection is related to
    via `isMemberOfCollection` relation, for subcollections.
    '''

