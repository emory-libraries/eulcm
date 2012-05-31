# file eulcm/xmlmap/boda.py
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
Custom XML for transitional born-digital content models
(:mod:`eulcm.models.boda`).

**Transitional** - the XML here is to support transitional content
models which are currently in use, but are intended to be migrated.

'''


from eulxml import xmlmap
from eulxml.xmlmap import mods


class _BaseRights(xmlmap.XmlObject):
    'Base class for Rights metadata objects'
    ROOT_NS = 'http://pid.emory.edu/ns/2010/rights'
    'xml namespace'
    ROOT_NAMESPACES = { 'rt': ROOT_NS }

class AccessStatus(_BaseRights):
    ':class:`~eulxml.xmlmap.XmlObject` for :class:`Rights` access status'
    ROOT_NAME = 'accessStatus'
    code = xmlmap.StringField('@code', required=True)
    'access code'
    text = xmlmap.StringField('text()')
    'text description of rights access code'


##
## Rights
##
class Rights(_BaseRights):
    'Rights metadata'
    ROOT_NAME = 'rights'

    access_status = xmlmap.NodeField('rt:accessStatus', AccessStatus,
        required=True,
        help_text='File access status, as determined by analysis of copyright, donor agreements, permissions, etc.')
    ':class:`AccessStatus`'
    
    copyright_holder_name = xmlmap.StringField('rt:copyrightholderName',
        required=False,
        help_text='Name of a copyright holder in last, first order')
    'name of the copyright holder'
    
    copyright_date = xmlmap.StringField('rt:copyrightDate[@encoding="w3cdtf"]',
        required=False,
        help_text='Date of copyright')
    'copyright date (string)'
    
    access_restriction_expiration = xmlmap.StringField('rt:accessRestrictionExperation[@encoding="w3cdtf"]',
        required=False,
        help_text='Date of when restrictions on an item might expire')
    'access restriction expiration date (string)'

    block_external_access = xmlmap.SimpleBooleanField('rt:externalAccess',
        'deny', None,
        help_text='''Deny external access (override Access Status).''')
    '''block external access. If this is True then refuse access to
    this item irrespective of :attr:`access_status`.'''
    # NOTE: users have also requested a <rt:externalAccess>allow</rt:externalAccess>
    # to allow access irrespective of access_status. when we implement
    # that, we'll probably want to incorporate it into this property and
    # rename

    ip_note = xmlmap.StringField('rt:ipNotes', required=False, verbose_name='IP Note',
        help_text='Additional information about the intellectual property rights of the associated work.')
    # NOTE: eventually should be repeatable/StringListField



class Series_Base(mods.RelatedItem):
    '''Base class for Series information; subclass of
    :class:`eulxml.xmlmap.mods.RelatedItem`.'''

    uri = xmlmap.StringField('mods:identifier[@type="uri"]',
            required=False, verbose_name='URI Identifier')
    'URI identifier'

    base_ark = xmlmap.StringField('mods:identifier[@type="base_ark"]',
            required=False, verbose_name='base ark target of document')
    'base ARK of target document'

    full_id = xmlmap.StringField('mods:identifier[@type="full_id"]',
            required=False, verbose_name='full id of this node')
    'full id' # ? 

    short_id = xmlmap.StringField('mods:identifier[@type="short_id"]',
            required=False, verbose_name='short id of this node')
    'short id'

# FIXME: what is the difference between series 1 and 2?

class Series2(Series_Base):
    '''Subseries'''
    series = xmlmap.NodeField("mods:relatedItem[@type='series']", Series_Base,
        required=False,
        help_text='subseries')

class Series1(Series_Base):
    '''Subseries (?)'''
    series = xmlmap.NodeField("mods:relatedItem[@type='series']", Series2,
        required=False,
        help_text='subseries')

class ArrangementMods(mods.MODS):
    '''Subclass of :class:`eulxml.xmlmap.mods.MODS` with mapping for
    series information.'''
    series = xmlmap.NodeField("mods:relatedItem[@type='series']", Series1,
        required=False,
        help_text='series')
    'series'



class FileMasterTech_Base(xmlmap.XmlObject):
    '''Base class for technical file metadata'''
    
    ROOT_NS = 'http://pid.emory.edu/ns/2011/filemastertech'
    'xml namespace'
    ROOT_NAMESPACES = {'fs': ROOT_NS }
    ROOT_NAME = 'file'

    BROWSABLE_COMPUTERS = ('Performa 5400','Performa 5300c')
    'computers available for browse'  # ?

    local_id = xmlmap.StringField('fs:localId')
    'local id'
    md5 = xmlmap.StringField('fs:md5')
    'MD5 checksum'
    computer = xmlmap.StringField('fs:computer')
    'computer name'
    path = xmlmap.StringField('fs:path')
    'file path'
    rawpath = xmlmap.StringField('fs:rawpath')
    'raw file path'    # encoded ? 
    attributes = xmlmap.StringField('fs:attributes')
    'file system attributes'
    #created = DateField('fs:created')
    #modified = DateField('fs:modified')
    created = xmlmap.StringField('fs:created')
    'date created'
    modified = xmlmap.StringField('fs:modified')
    'date last modified'
    type = xmlmap.StringField('fs:type')
    'type'
    creator = xmlmap.StringField('fs:creator')
    'creator'

    def browsable(self):
        '''Check if this file is browsable, based on :attr:`computer`
        and the list of :attr:`BROWSABLE_COMPUTERS`.'''
        return self.computer in self.BROWSABLE_COMPUTERS

    def dir_parts(self):
        '''
        Directory parts based on path.    
        '''
        # FIXME: redundant code with rushdie webapp ?
        # TODO: document what this actually does...
        
        raw_parts = self.path.split('/')

        base = '/'
        # path is absolute, so raw_parts[0] is empty. skip it. also skip
        # raw_parts[-1] for special handling later
        for part in raw_parts[1:-1]:
            yield _DirPart(self.computer, base, part)
            base = base + part + '/'

    def name(self):
        '''file name (last portion of the file path)'''
        return self.path.split('/')[-1]

class FileMasterTech(xmlmap.XmlObject):
    ''':class:`~eulxml.models.XmlObject` for representing technical
    file metadata'''
    
    ROOT_NS = 'http://pid.emory.edu/ns/2011/filemastertech'  # redundant ? 
    ROOT_NAMESPACES = {'fs': ROOT_NS }	# redundant? 
    ROOT_NAME = 'document'
    file = xmlmap.NodeListField("fs:file", FileMasterTech_Base,
                                required=False)		# why separate? 
    'file information; instance of :class:`FileMasterTech_Base`'  
    
