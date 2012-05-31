from eulfedora.models import DigitalObject, XmlDatastream, Relation
from eulfedora.rdfns import relsext
from eulxml.xmlmap import mods

from eulcm.xmlmap.mods import MODS


class Collection(DigitalObject):
    '''
    Fedora Collection 1.1.  Implicit collection with MODS descriptive
    metadata.  Objects that belong to collection 1.1 objects are
    expected to be related to via *isMemberOfCollection*.  Could be a
    sub-collection of another Collection 1.1.
    '''
    COLLECTION_CONTENT_MODEL = 'info:fedora/emory-control:Collection-1.1'
    'content model'
    CONTENT_MODELS = [ COLLECTION_CONTENT_MODEL ]

    mods = XmlDatastream('MODS', 'Descriptive Metadata (MODS)', MODS, defaults={
            'control_group': 'M',
            'format': mods.MODS_NAMESPACE,
            'versionable': True,
        })
    '''MODS :class:`~eulfedora.models.XmlDatastream` with content as
    :class:`eulxml.xmlmap.mods.MODS`; versionable, datastream ID
    ``MODS``'''

    collection = Relation(relsext.isMemberOfCollection,
                          type='self')  
    '''Parent :class:`Collection` that this collection is related to
    via `isMemberOfCollection` relation, for subcollections.
    '''

