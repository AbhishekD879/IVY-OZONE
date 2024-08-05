import pytest

from voltron.utils.exceptions.cms_client_exception import CmsClientException

import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
import voltron.environments.constants as vec
from voltron.utils.helpers import normalize_name


@pytest.mark.crl_tst2  # Coral only
@pytest.mark.crl_stg2
@pytest.mark.crl_prod
@pytest.mark.crl_hl
@pytest.mark.football
@pytest.mark.favourites
@pytest.mark.desktop_only
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.login
@vtest
class Test_C2745940_Verify_Favourite_Widget_on_Desktop(BaseCashOutTest):
    """
    TR_ID: C2745940
    VOL_ID: C24331836
    NAME: Verify ‘Favourite’ Widget on Desktop
    DESCRIPTION: This Test Case verified ‘Favourite Matches’ Widget on Desktop for both logged out and logged in users
    PRECONDITIONS: User is NOT logged in
    """
    keep_browser_open = True
    device_name = tests.desktop_default
    cms_favourites_login_button_text = 'loginButtonText'
    cms_favourites_introductory_text_title = 'introductoryText'
    right_column = None
    favorites_widget = None
    event_details = None

    def check_widget_content(self, expected_count: int) -> None:
        """
        Verifies that 'FAVOURITES' widget contains expected events
        :param expected_count: expected count of event in 'FAVOURITES' widget
        """
        self.__class__.favorites_widget = self.site.favourites
        widget_odds_cards = self.favorites_widget.items_as_ordered_dict
        self.assertTrue(widget_odds_cards, msg='Favourites widget is empty')
        displayed_odds_cards = list(widget_odds_cards.keys())

        self.assertEqual(len(displayed_odds_cards), expected_count,
                         msg=f'Actual events count "{len(displayed_odds_cards)}" != Expected count "{expected_count}"')

        for event_name in displayed_odds_cards:
            self.assertIn(event_name, self.event_names,
                          msg=f'Wrong event "{event_name}" is present in "FAVOURITES" widget, '
                          f'but one of "{self.event_names}" has to be present')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create football events
        """
        if self.cms_config.get_widgets(widget_type='favourites')[0]['disabled']:
            raise CmsClientException('"Favourites" widget is disabled in CMS')

        self.__class__.favourites_widget_name = self.get_filtered_widget_name(cms_type='favourites')

        if tests.settings.backend_env == 'prod':
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         number_of_events=5)
            self.__class__.event_details = {event['event']['id']: normalize_name(event['event']['name']) for event in events}
            self.__class__.event_names = [normalize_name(event['event']['name']) for event in events]
        else:
            events = self.create_several_autotest_premier_league_football_events(number_of_events=5, is_live=True)
            self.__class__.event_details = {event.event_id: event.event_name for event in events}
            self.__class__.event_names = [event.event_name for event in events]

        self._logger.info(f'*** Found the following football events: "{self.event_details}"')

    def test_001_navigate_to_homepage(self):
        """
        DESCRIPTION: Navigate to Homepage
        EXPECTED: 'Favourite Matches' page/widget is displayed below Betslip widget
        """
        favorites_widget = self.site.favourites
        self.assertEqual(favorites_widget.name, self.favourites_widget_name,
                         msg=f'Actual widget name "{favorites_widget.name}" != Expected "{self.favourites_widget_name}"')
        self.__class__.favorites_widget = self.site.favourites
        self.assertTrue(self.favorites_widget.is_displayed(), msg='"FAVORITES" widget is not displayed')

        betslip_coordinates = self.get_betslip_content().location.get('y')
        favorites_widget_coordinates = self.favorites_widget.location.get('y')
        self.assertGreater(favorites_widget_coordinates, betslip_coordinates,
                           msg='\'Betslip\' widget is not displayed above \'FAVORITES\' widget')

    def test_002_verify_favourite_matches_widget_elements(self):
        """
        DESCRIPTION: Verify 'Favourite Matches' widget elements
        EXPECTED: *   Collapsible/Expandable accordion with title 'FAVORITES'
        EXPECTED: *   Introductory text is displayed as follows: **"To view and add matches into your favourites, please log in into your account." ** (text is taken from CMS)
        EXPECTED: *   'Log In' button (text is taken from CMS)
        """
        self.assertEqual(self.favorites_widget.section_header.title_text, self.favourites_widget_name,
                         msg=f'Accordion title "{self.favorites_widget.section_header.title_text}" is not the '
                         f'same as expected "{self.favourites_widget_name}"')
        self.favorites_widget.collapse()
        self.assertFalse(self.favorites_widget.is_expanded(expected_result=False),
                         msg='\'FAVORITES\' widget is not collapsed')
        self.favorites_widget.expand()
        self.assertTrue(self.favorites_widget.is_expanded(), msg='\'FAVORITES\' widget is not expanded')

        cms_favorites_text = self.get_initial_data_system_configuration().get('favoritesText')
        if not cms_favorites_text:
            cms_favorites_text = self.cms_config.get_system_configuration_item('favoritesText')
        self.assertTrue(all(cms_favorites_text), msg='Favorites text config data is not available')

        ui_introductory_text = self.favorites_widget.widget_text_not_logged
        self.assertEqual(ui_introductory_text, cms_favorites_text[self.cms_favourites_introductory_text_title],
                         msg='Introductory text \n"%s" is not the same as expected \n"%s"' %
                             (ui_introductory_text, cms_favorites_text[self.cms_favourites_introductory_text_title]))

        ui_login_button_text = self.favorites_widget.login_button.name
        self.assertEqual(ui_login_button_text, cms_favorites_text[self.cms_favourites_login_button_text],
                         msg='Login button text \n"%s" is not the same as expected \n"%s"' %
                             (ui_login_button_text, cms_favorites_text[self.cms_favourites_login_button_text]))

    def test_003_log_in_and_verify_favourite_matches_page_widget(self):
        """
        DESCRIPTION: Log In and verify 'Favourite Matches' page/widget
        EXPECTED: Introductory text is displayed as follows: **"You currently have no favourites added. Browse through the matches currently available and add them to your favourite list."**
        """
        self.site.login()

        ui_introductory_text = self.favorites_widget.widget_text_logged.strip()
        self.assertEqual(ui_introductory_text, vec.sb_desktop.NO_FAVOURITE_MATCHES,
                         msg='Introductory text \n"%s" is not the same as expected \n"%s"' %
                             (ui_introductory_text, vec.sb_desktop.NO_FAVOURITE_MATCHES))

    def test_004_add_football_event_to_favourites_and_verify_favourite_matches_pagewidget(self):
        """
        DESCRIPTION: Add Football event to Favourites and verify 'Favourite Matches' page/widget
        EXPECTED: *  Added event is displayed on 'Favourite Matches' page/widget
        """
        event_id, event_name = list(self.event_details.items())[0]

        self.navigate_to_edp(event_id=event_id)
        self.site.sport_event_details.favourite_icon.click()
        self.assertTrue(self.site.sport_event_details.favourite_icon.is_selected(),
                        msg='Favourite icon is not selected for "%s" event' % event_name)
        favorites_widget = self.site.favourites

        widget_odds_cards = favorites_widget.items_as_ordered_dict
        self.assertTrue(widget_odds_cards, msg='Favourites widget is empty')
        self.assertTrue(widget_odds_cards.get(event_name),
                        msg=f'Event "{event_name}" id not found between events "{widget_odds_cards.keys()}" in the favourites widget.')

    def test_005_add_4_football_events_to_favourites_widget_and_verify_show_all_link_displaying(self):
        """
        DESCRIPTION: Add 4 football events to Favourites widget and verify 'Show All' link displaying
        EXPECTED: * The first three events are displayed in the widget
        EXPECTED: * 'Show All' button appears below event cards
        """
        for event_id, event_name in list(self.event_details.items())[1:]:
            self.navigate_to_edp(event_id=event_id)
            self.site.sport_event_details.favourite_icon.click()
            self.assertTrue(self.site.sport_event_details.favourite_icon.is_selected(),
                            msg='Favourite icon is not selected for "%s" event' % event_name)
        self.check_widget_content(expected_count=3)

        self.assertTrue(self.favorites_widget.show_all_button.is_displayed(),
                        msg='\'Show All\' button is not displayed')

    def test_006_click_on_show_all_button(self):
        """
        DESCRIPTION: Click on 'Show All' button
        EXPECTED: * Widget expands downwards to show the full list of events
        EXPECTED: * 'Show All' changes to 'Show Less'
        """
        self.favorites_widget.show_all_button.click()

        self.check_widget_content(expected_count=5)

        self.assertTrue(self.favorites_widget.show_less_button.is_displayed(),
                        msg='\'Show Less\' button is not displayed')

    def test_007_click_on_show_less_button(self):
        """
        DESCRIPTION: Click on 'Show Less' button
        EXPECTED: * Widget collapses to show first 3 events
        EXPECTED: * 'Show Less' changes to 'Show All'
        """
        self.favorites_widget.show_less_button.click()

        self.check_widget_content(expected_count=3)

        self.assertTrue(self.favorites_widget.show_all_button.is_displayed(),
                        msg='\'Show All\' button is not displayed')
