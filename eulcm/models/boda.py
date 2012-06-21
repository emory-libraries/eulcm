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

import email

from eulfedora import models as fedora_models
from eulfedora.util import RequestFailed
from eulfedora.rdfns import relsext
from eulxml.xmlmap import mods, cerp

from eulcm.models.collection.v1_1 import Collection
from eulcm.xmlmap.boda import Rights, ArrangementMods, FileMasterTech


class Arrangement(fedora_models.DigitalObject):
    '''Subclass of :class:`eulfedora.models.DigitalObject` for
    "arrangement" content, i.e., born-digital materials which need to
    be processed and arranged into series before they can be made
    accessible to researchers.'''

    ARRANGEMENT_CONTENT_MODEL = 'info:fedora/emory-control:Arrangement-1.0'
    CONTENT_MODELS = [ ARRANGEMENT_CONTENT_MODEL ]

    rights = fedora_models.XmlDatastream("Rights", "Usage rights and access control metadata", Rights,
        defaults={
            'control_group': 'M',
            'versionable': True,
        })
    '''access control metadata :class:`~eulfedora.models.XmlDatastream`
    with content as :class:`Rights`; datastream id ``Rights``'''

    filetech = fedora_models.XmlDatastream("FileMasterTech", "File Technical Metadata", FileMasterTech ,defaults={
            'control_group': 'M',
            'versionable': True,
        })
    '''file technical metadata
    :class:`~eulfedora.models.XmlDatastream` with content as
    :class:`keep.common.models.FileMasterTech`; datastream ID
    ``FileMasterTech``'''

    mods = fedora_models.XmlDatastream('MODS', 'MODS Metadata', ArrangementMods, defaults={
            'control_group': 'M',
            'format': mods.MODS_NAMESPACE,
            'versionable': True,
        })
    '''MODS :class:`~eulfedora.models.XmlDatastream` with content as
    :class:`ArrangementMods`; datstream ID ``MODS``'''

    collection = fedora_models.Relation(relsext.isMemberOfCollection, type=Collection)
    ''':class:`~eulcm.models.collection.v1_1.Collection` that this
    object is a member of, via `isMemberOfCollection` relation.
    '''



### email folder and message objects


class Mailbox(fedora_models.DigitalObject):
    ''':class:`rushdieweb.fedorabase.models.DocumentObject` subclass
    to represent an email mailbox.

    Has an auto-generated :class:`eulfedora.models.ReverseRelation`
    **messages** with a list of :class:`EmailMessage` objects that are
    part of this mailbox.

    Has an auto-generated :class:`eulfedora.models.ReverseRelation`
    **constituent_files** with a list of :class:`RushdieFile` objects
    that are the constituent files of this mailbox (i.e., index and
    data files).
    
    '''
    MAILBOX_CONTENT_MODEL = 'info:fedora/emory-control:Rushdie-CerpMailbox-1.0'
    CONTENT_MODELS = [ MAILBOX_CONTENT_MODEL ]

    # auto-generated reverse relations: messages, constituent_files


class EmailMessageDatastreamObject(fedora_models.DatastreamObject):
    ''':class:`eulfedora.models.DatastreamObject` subclass for
    handling email message datastreams.
    '''
    default_mimetype = 'message/rfc822'
    'default mimetype for message datastreams'
    
    def _convert_content(self, data, url):
        return email.message_from_string(data)

    def _bootstrap_content(self):
        return email.Message()


class EmailMessageDatastream(fedora_models.Datastream):
    ''':class:`eulfedora.models.Datastream` subclass for handling
    email message datastreams.  Uses :class:`EmailMessageDatastreamObject`
    for actual content handling.
    '''
    _datastreamClass = EmailMessageDatastreamObject


class EmailMessage(Arrangement):
    ''':class:`Arrangement` subclass to represent a single email
    message.  (Does not have :attr:`Arrangement.file_tech`.)
    ''' 
    EMAIL_MESSAGE_CMODEL = 'info:fedora/emory-control:Rushdie-MailboxEntry-1.0'
    CONTENT_MODELS = [ EMAIL_MESSAGE_CMODEL , Arrangement.ARRANGEMENT_CONTENT_MODEL ]

    mime_data = EmailMessageDatastream('MIME', 'MIME message data',
        defaults={'versionable':True})
    ''':class:`EmailMessageDatastream` for MIME message data, with
    datastream id **MIME**''' 
    
    cerp = fedora_models.XmlDatastream('CERP', 'CERP XML metadata', cerp.Message,
        defaults={'versionable':True})
    ''':class:`~eulfedora.models.XmlDatastream` for email content in
    CERP xml format, with datastream id **CERP** '''

    mailbox = fedora_models.Relation(relsext.isPartOf, Mailbox,
                                     related_name='messages')
    ''':class:`Mailbox` this email message belongs to, via ``isPartOf`` relation'''
    # NOTE: first batch of messages created (Performa 5400) have rels-ext
    # relations in both directions, but we are not preserving that.

    def update_cerp(self):
        '''
        Generate CERP xml for :attr:`EmailMessage.cerp.content` based
        on :attr:`EmailMessage.mime_data.content`.  Convenience
        wrapper around :meth:`eulxml.xmlmap.cerp.Message.from_email_message`.
        '''
        self.cerp.content = cerp.Message.from_email_message(self.mime_data.content)


### basic file object
    
class RushdieFile(Arrangement):
    '''File object; extends :class:`Arrangement` and adds an
    :attr:`original` datastream and optional :attr:`pdf` datastream.
    '''
    RUSHDIE_FILE_CMODEL = 'info:fedora/emory-control:Rushdie-MarblMacFile-1.0'
    
    CONTENT_MODELS = [ RUSHDIE_FILE_CMODEL, Arrangement.ARRANGEMENT_CONTENT_MODEL ]
 
    pdf = fedora_models.FileDatastream("PDF", "pdf datastream", defaults={
            'mimetype': 'application/pdf',
            'versionable': True,
        })
    '''pdf :class:`~eulfedora.models.FileDatastream` with datastream
    id **PDF**'''

    original = fedora_models.FileDatastream("ORIGINAL", "original datastream", defaults={
            'mimetype': 'application/',
            'versionable': True,
        })
    '''original file content :class:`~eulfedora.models.FileDatastream`
    with datastream id **ORIGINAL**'''

    mailbox = fedora_models.Relation(relsext.isConstituentOf, Mailbox,
                                     related_name='constituent_files')
    ''':class:`Mailbox` that this file is a constituent part of (i.e.,
    email folder data or index file), via ``isConstituentOf`` relation'''
    # NOTE: first batch of messages created (Performa 5400) have rels-ext
    # relations in both directions, but we are not preserving that.





