from eulxml import xmlmap
from eulxml.xmlmap import mods


class MODS(mods.MODS):
    '''Extend base :class:`eulxml.xmlmap.mods.MODS` with short-cut
    fields for identifiers and access conditions with custom types.'''
    
    ark = xmlmap.StringField('mods:identifier[@type="ark"]')
    '''ARK (Archival Resource Key) identifier, short form'''
    ark_uri = xmlmap.StringField('mods:identifier[@type="uri"][contains(., "ark:")]')
    '''ARK (Archival Resource Key) identifier as a full, resolvable URL'''


    source_id = xmlmap.IntegerField("mods:identifier[@type='local_source_id']")
    ''':type integer: local source id
    ``mods:identifier[@type="local_source_id"]``'''
    short_name = xmlmap.StringField("mods:identifier[@type='local_short_name']")
    ''':type string: local short name identifier
    ``mods:identifier[@type="local_short_name"]``'''
    
    restrictions_on_access = xmlmap.NodeField('mods:accessCondition[@type="restrictions on access"]',
                                              mods.AccessCondition)
    ':class:`eulxml.xmlmap.mods.AccessCondition` with type "restrictions on access"'
    use_and_reproduction = xmlmap.NodeField('mods:accessCondition[@type="use and reproduction"]',
                                              mods.AccessCondition)
    ':class:`eulxml.xmlmap.mods.AccessCondition` with type "use and reproduction"'


