# file eulcm/models/boda.py
# 
#   Copyright 2012 Emory University Libraries
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

'''
**Transitional Content Models**

These content models are currently in use but we hope to migrate to
more standard cmodels soon.


'''


from eulfedora.models import DigitalObject, FileDatastream, \
     XmlDatastream, Relation
from eulfedora.util import RequestFailed
from eulfedora.rdfns import relsext
from eulxml.xmlmap import mods

from eulcm.models.collection.v1_1 import Collection
from eulcm.xmlmap.boda import Rights, ArrangementMods, FileMasterTech


class Arrangement(DigitalObject):
    '''Subclass of :class:`eulfedora.models.DigitalObject` for
    "arrangement" content, i.e., born-digital materials which need to
    be processed and arranged into series before they can be made
    accessible to researchers.'''

    ARRANGEMENT_CONTENT_MODEL = 'info:fedora/emory-control:Arrangement-1.0'
    CONTENT_MODELS = [ ARRANGEMENT_CONTENT_MODEL ]

    rights = XmlDatastream("Rights", "Usage rights and access control metadata", Rights,
        defaults={
            'control_group': 'M',
            'versionable': True,
        })
    '''access control metadata :class:`~eulfedora.models.XmlDatastream`
    with content as :class:`Rights`; datastream id ``Rights``'''

    filetech = XmlDatastream("FileMasterTech", "File Technical Metadata", FileMasterTech ,defaults={
            'control_group': 'M',
            'versionable': True,
        })
    '''file technical metadata
    :class:`~eulfedora.models.XmlDatastream` with content as
    :class:`keep.common.models.FileMasterTech`; datastream ID
    ``FileMasterTech``'''

    mods = XmlDatastream('MODS', 'MODS Metadata', ArrangementMods, defaults={
            'control_group': 'M',
            'format': mods.MODS_NAMESPACE,
            'versionable': True,
        })
    '''MODS :class:`~eulfedora.models.XmlDatastream` with content as
    :class:`ArrangementMods`; datstream ID ``MODS``'''

    collection = Relation(relsext.isMemberOfCollection, type=Collection)
    ''':class:`~eulcm.models.collection.v1_1.Collection` that this
    object is a member of, via `isMemberOfCollection` relation.
    '''


