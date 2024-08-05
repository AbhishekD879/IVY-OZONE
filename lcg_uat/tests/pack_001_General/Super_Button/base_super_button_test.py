from crlat_core.request import InvalidResponseException
from crlat_cms_client.utils.exceptions import CMSException
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest


class BaseSuperButtonTest(BaseFeaturedTest):
    active_super_buttons = []

    @classmethod
    # Only one super button can be present in app
    def custom_setUp(cls, **kwargs):
        cms = cls.get_cms_config()
        super_buttons = cms.get_mobile_super_buttons()
        for super_button in super_buttons:
            if super_button['enabled']:
                try:
                    cms.update_mobile_super_button(name=super_button['title'], enabled=False)
                    cls.active_super_buttons.append(super_button)
                except (CMSException, InvalidResponseException) as e:
                    title = super_button['title']
                    cls._logger.warning(msg=f'Failed to deactivate existing super button "{title}" in CMS. '
                                            f'Probably there is something wrong with it. Error:\n{e}')

    @classmethod
    def custom_tearDown(cls):
        cms = cls.get_cms_config()
        for super_button in cls.active_super_buttons:
            cms.update_mobile_super_button(name=super_button['title'], enabled=True)
