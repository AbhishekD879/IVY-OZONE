import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_009_SPORT_Specifics.Football_Specifics.Football_Coupons.BaseCouponsTest import BaseCouponsTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest


# @pytest.mark.crl_tst2
# @pytest.mark.crl_stg2
# @pytest.mark.crl_prod
@pytest.mark.football
@pytest.mark.coupons
@pytest.mark.goalscorer
@pytest.mark.google_analytics
@pytest.mark.other
@pytest.mark.low
@pytest.mark.quarantine
@pytest.mark.issue('https://jira.egalacoral.com/browse/VOL-3330')
@pytest.mark.login
@vtest
class Test_C1390536_Verify_tracking_of_Goalscorer_Coupon(BaseCouponsTest, BaseDataLayerTest):
    """
    TR_ID: C1390536
    VOL_ID: C1497918
    NAME: Verify tracking of Goalscorer Coupon
    DESCRIPTION: This Test Case verified tracking in the Google Analytic's data Layer when visit the goalscorer coupon
    PRECONDITIONS: Test case should be run on Mobile, Tablet, Desktop and Wrappers
    PRECONDITIONS: Browser console should be opened
    """
    keep_browser_open = True
    autotest_league = tests.settings.football_autotest_competition_league
    goalscorer_coupon = vec.coupons.GOALSCORER_COUPON
    markets = [
        ('anytime_goalscorer', {'cashout': False}),
        ('first_goalscorer', {'cashout': False}),
        ('last_goalscorer', {'cashout': False})
    ]
    coupon = None
    event = None

    def test_000_add_event(self):
        """
        DESCRIPTION: Add 'Football' events and additional market
        """
        event_params1 = self.ob_config.add_autotest_premier_league_football_event(markets=self.markets)

        self.__class__.event_id, self.__class__.team1, self.__class__.team2, self.__class__.selection_ids = \
            event_params1.event_id, event_params1.team1, event_params1.team2, event_params1.selection_ids

        self.__class__.event_name = self.team1 + ' v ' + self.team2

        anytime_goalscorer_id = self.ob_config.market_ids[self.event_id]['anytime_goalscorer']
        first_goalscorer_id = self.ob_config.market_ids[self.event_id]['first_goalscorer']
        last_goalscorer_id = self.ob_config.market_ids[self.event_id]['last_goalscorer']

        self.ob_config.add_event_to_coupon(market_id=anytime_goalscorer_id, coupon_name=self.goalscorer_coupon)
        self.ob_config.add_event_to_coupon(market_id=first_goalscorer_id, coupon_name=self.goalscorer_coupon)
        self.ob_config.add_event_to_coupon(market_id=last_goalscorer_id, coupon_name=self.goalscorer_coupon)

        self.__class__.coupon_tab_name = self.get_sport_tab_name(
            self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.coupons,
            self.ob_config.football_config.category_id)

    def test_001_tap_sport(self):
        """
        DESCRIPTION: Tap '<Sport>' icon on the Sports Menu Ribbon
        """
        self.site.open_sport(name='FOOTBALL')

    def test_002_tap_coupons_tab(self):
        """
        DESCRIPTION: Open coupons tab
        """
        coupons = self.site.football.tabs_menu.click_button(self.coupon_tab_name)
        self.assertTrue(coupons, msg='Coupons page was not opened')

    def test_003_select_goalscorer_coupon(self):
        """
        DESCRIPTION: Select 'Goalscorer coupon'
        EXPECTED: 'Goalscorer coupon' page is opened
        """
        self.find_coupon_and_open_it(coupon_section=vec.coupons.POPULAR_COUPONS.upper(), coupon_name=self.goalscorer_coupon)

    def test_004_expand_event_with_selections(self):
        """
        DESCRIPTION: Scrolls down the page and find the event where 'Show All' is available
        """
        leagues = self.site.coupon.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(leagues, msg='No leagues found on Coupon page')
        events = leagues[self.autotest_league].items_as_ordered_dict
        self.assertTrue(self.event_name.upper() in events,
                        msg='"%s" event not found in list "%s"' % (self.event_name.upper(), events))
        self.__class__.event = events[self.event_name.upper()]
        self.event.expand()
        self.assertTrue(self.event.is_expanded(), msg=f'Event {self.event_name} is not expanded after click')

    def test_005_click_on_the_show_all_link(self):
        """
        DESCRIPTION: Click on the 'Show All' link
        EXPECTED: All existing selections are shown
        """
        self.assertTrue(self.event.has_show_all_button, msg=f'"Show all" button is not present for {self.event_name}')
        self.event.show_all_button.click()

    def test_006_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'goalscorer coupon',
        EXPECTED: 'eventAction' : 'show more',
        EXPECTED: 'eventLabel' : '<< EVENT >>'
        EXPECTED: })
        """
        expected_response = {
            'event': 'trackEvent',
            'eventCategory': 'goalscorer coupon',
            'eventAction': 'show all',
            'eventLabel': self.event_name
        }
        actual_response = self.get_data_layer_specific_object(object_key='eventCategory',
                                                              object_value='goalscorer coupon')
        self.compare_json_response(actual_response, expected_response)

    def test_007_click_on_the_go_to_event_link(self):
        """
        DESCRIPTION: Click on the 'Go to Event' link
        EXPECTED: Event details page is opened
        """

        self.assertTrue(self.event.has_go_to_event_link(), msg='"Show all" button is not present')
        self.event.go_to_event_link.click()
        self.site.wait_content_state(state_name='EventDetails')

    def test_008_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter
        EXPECTED: 1. 'Event details' page is opened
        EXPECTED: 2. The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'goalscorer coupon',
        EXPECTED: 'eventAction' : 'go to event',
        EXPECTED: 'eventLabel' : '<< EVENT >>'
        EXPECTED: })
        """
        expected_response = {
            'event': 'trackEvent',
            'eventCategory': 'goalscorer coupon',
            'eventAction': 'go to event',
            'eventLabel': self.event_name
        }
        actual_response = self.get_data_layer_specific_object(object_key='eventCategory',
                                                              object_value='goalscorer coupon')
        self.compare_json_response(actual_response, expected_response)

    def test_009_repeat_steps_1_9_for_logged_in_user(self):
        """
        DESCRIPTION: Repeat steps 1-9 for Logged In user
        EXPECTED:
        """
        self.navigate_to_page(name='/')
        self.site.wait_content_state(state_name='HomePage')
        self.site.login(username=tests.settings.betplacement_user)
        self.test_001_tap_sport()
        self.test_002_tap_coupons_tab()
        self.test_003_select_goalscorer_coupon()
        self.test_004_expand_event_with_selections()
        self.test_005_click_on_the_show_all_link()
        self.test_006_type_in_browser_console_datalayer_and_tap_enter()
        self.test_007_click_on_the_go_to_event_link()
        self.test_008_type_in_browser_console_datalayer_and_tap_enter()
