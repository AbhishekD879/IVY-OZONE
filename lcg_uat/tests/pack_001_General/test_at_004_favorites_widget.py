import pytest
import tests

from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.cms_client_exception import CmsClientException
import voltron.environments.constants as vec


# @pytest.mark.tablet # This functionality is no longer applicable from release 108
# @pytest.mark.widgets
# @pytest.mark.crl_prod
# @pytest.mark.crl_hl
# @pytest.mark.crl_tst2
# @pytest.mark.crl_stg2
# @pytest.mark.safari
# @pytest.mark.login
@pytest.mark.na
@vtest
class Test_AT_004_verify_right_column_favorites_widget(Common):
    """
    VOL_ID: C9697893
    NAME: Verify Right Column Favorites widget
    """
    keep_browser_open = True
    cms_favorites_text = None
    device_name = tests.tablet_default
    cms_favourites_login_button_text = 'loginButtonText'
    cms_favourites_introductory_text_title = 'introductoryText'
    go_to_matches_button = 'Go to Matches'
    go_to_inplay_button = 'Go to In-Play Matches'

    def test_001_verify_favorites_not_logged(self):
        """
        DESCRIPTION: Verify Favorites widget content for not logged user
        """
        if not self.get_favourites_enabled_status():
            raise CmsClientException('Favourites are disabled in CMS')

        favourites_widget_name = self.get_filtered_widget_name(cms_type='favourites')

        favorites_widget = self.site.favourites
        if not favorites_widget.is_expanded():
            favorites_widget.click()
        self.assertEqual(favorites_widget.name, favourites_widget_name,
                         msg=f'Actual widget name "{favorites_widget.name}" != Expected "{favourites_widget_name}"')
        self.assertTrue(favorites_widget.is_expanded(), msg='Favourites widget is not expanded')

        self.__class__.cms_favorites_text = self.get_initial_data_system_configuration().get('favoritesText')
        if not self.cms_favorites_text:
            self.cms_favorites_text = self.cms_config.get_system_configuration_item('favoritesText')
        if not self.cms_favorites_text:
            raise CmsClientException('"favoritesText" section is not added to System Config on CMS')
        self.assertTrue(all(self.cms_favorites_text), msg='Favorites text config data is not available')
        text = favorites_widget.widget_text_not_logged
        buttons = favorites_widget.widget_buttons

        self.assertIn(self.cms_favorites_text[self.cms_favourites_introductory_text_title], text,
                      'Widget text "%s" was not found in [%s]' %
                      (self.cms_favorites_text[self.cms_favourites_introductory_text_title], text))
        self.assertNotIn(vec.favourites.BROWSE_FAVOURITE_MATCHES, text,
                         'Widget text "%s" was found in [%s]' % (vec.favourites.BROWSE_FAVOURITE_MATCHES, text))

        self.assertIn(self.cms_favorites_text[self.cms_favourites_login_button_text], buttons,
                      '"%s" button was not found in [%s]' %
                      (self.cms_favorites_text[self.cms_favourites_login_button_text], buttons))
        self.assertNotIn(self.go_to_matches_button, buttons, '"%s" button was found' % self.go_to_matches_button)
        self.assertNotIn(self.go_to_inplay_button, buttons,
                         '"%s" button was found' % self.go_to_inplay_button)

    def test_002_verify_favorites_logged(self):
        """
        DESCRIPTION: Verify Favorites widget content for logged user
        """
        self.site.login(timeout_wait_for_dialog=2)

        favorites_widget = self.site.favourites
        favorites_widget.expand()
        self.assertTrue(favorites_widget.is_expanded(), msg='Favourites widget is not expanded')

        text = favorites_widget.widget_text_logged
        buttons = favorites_widget.widget_buttons

        self.assertNotIn(self.cms_favorites_text[self.cms_favourites_introductory_text_title], text,
                         msg='Widget text "%s" was found' %
                             self.cms_favorites_text[self.cms_favourites_introductory_text_title])
        self.assertIn(vec.favourites.BROWSE_FAVOURITE_MATCHES, text,
                      msg='Widget text "%s" was not found' % vec.favourites.BROWSE_FAVOURITE_MATCHES)

        self.assertNotIn(self.cms_favorites_text[self.cms_favourites_login_button_text], buttons,
                         msg='"%s" button was found' % self.cms_favorites_text[self.cms_favourites_login_button_text])
        self.assertIn(self.go_to_matches_button, buttons, msg='"%s" button was not found' % self.go_to_matches_button)
        self.assertIn(self.go_to_inplay_button, buttons, msg='"%s" button was not found' % self.go_to_inplay_button)
