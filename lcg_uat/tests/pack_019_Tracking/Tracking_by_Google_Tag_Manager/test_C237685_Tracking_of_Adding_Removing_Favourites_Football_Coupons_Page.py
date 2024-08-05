import voltron.environments.constants as vec
import pytest
import tests
from tests.base_test import vtest
from tests.pack_009_SPORT_Specifics.Football_Specifics.Football_Coupons.BaseCouponsTest import BaseCouponsTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest


# @pytest.mark.crl_prod
# @pytest.mark.crl_hl
@pytest.mark.crl_tst2  # Coral Only
@pytest.mark.crl_stg2
@pytest.mark.google_analytics
@pytest.mark.favourites
@pytest.mark.coupons
@pytest.mark.other
@pytest.mark.low
@pytest.mark.login
@vtest
@pytest.mark.issue('https://jira.egalacoral.com/browse/VOL-3088')
class Test_C237685_Tracking_Of_Adding_Removing_Favourites_Football_Coupons_Page(BaseCouponsTest, BaseDataLayerTest):
    """
    TR_ID: C237685
    VOL_ID: C9697888
    NAME: Tracking of Adding/Removing Favourites on Football Coupons page
    """
    keep_browser_open = True
    event = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create event
        EXPECTED: Event is created
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event()
        market_short_name = self.ob_config.football_config.\
            autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()
        autotest_match_result_market_id = self.ob_config.market_ids[event_params.event_id][market_short_name]
        self.ob_config.add_event_to_coupon(market_id=autotest_match_result_market_id,
                                           coupon_name=vec.siteserve.EXPECTED_COUPON_NAME)
        self.__class__.event_name = event_params.team1 + ' v ' + event_params.team2

        self.__class__.coupon_tab_name = self.get_sport_tab_name(
            self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.coupons,
            self.ob_config.football_config.category_id)

    def test_001_login(self):
        """
        DESCRIPTION: Login to application
        EXPECTED: User is logged in
        """
        self.site.login(username=tests.settings.betplacement_user)

    def test_002_navigate_to_football_page_and_open_coupons_tab(self):
        """
        DESCRIPTION: Navigate to the Football Landing page
        EXPECTED: Football Landing page is shown
        """
        self.site.open_sport(name='FOOTBALL')
        self.site.football.tabs_menu.click_button(self.coupon_tab_name)
        self.assertEqual(self.site.football.tabs_menu.current, self.coupon_tab_name,
                         msg='COUPONS tab is not active')

    def test_003_find_event_and_add_it_to_favourites(self):
        """
        DESCRIPTION: Find created event on Football page and click on 'star' icon
        EXPECTED: 'Star' icon is highlighted
        """
        autotest_league = tests.settings.football_autotest_competition_league.title() if self.brand == 'ladbrokes' \
            and self.device_type == 'mobile' else tests.settings.football_autotest_competition_league
        self.find_coupon_and_open_it(coupon_section=vec.coupons.POPULAR_COUPONS.upper(), coupon_name=vec.siteserve.EXPECTED_COUPON_NAME)

        self.__class__.sections = self.site.coupon.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.sections, msg='No event groups found on Coupon page')
        self.assertIn(autotest_league, self.sections,
                      msg=f'"{autotest_league}" is not found in sections list "{self.sections.keys()}"')
        date_groups = self.sections[autotest_league].items_as_ordered_dict
        self.assertTrue(date_groups, msg=f'No data groups found in "{autotest_league}" section')
        self.assertIn(vec.sb.TABS_NAME_TODAY, date_groups.keys(),
                      msg=f'Today date group is not found among date groups "{date_groups.keys()}"')
        events = date_groups[vec.sb.TABS_NAME_TODAY].items_as_ordered_dict
        self.assertIn(self.event_name, events, msg=f'No event "{self.event_name}" found in events list "{events}"')
        self.__class__.event = events[self.event_name]
        self.event.favourite_icon.click()
        self.assertTrue(self.event.favourite_icon.is_selected(),
                        msg=f'Favourites icon is not highlighted for event "{self.event_name}"')

    def test_004_check_data_layer_response_for_adding_to_favourites_on_football_coupons_page(self):
        """
        DESCRIPTION: Check data layer response for adding to favourites on football coupons page
        EXPECTED: 'action' must be 'add', 'location' must be 'football coupons'
        """
        self.check_data_layer_favourites_response(object_key='eventAction', action='add', location='football coupons')

    def test_005_remove_event_from_favourites(self):
        """
        DESCRIPTION: Remove event from Favourites
        EXPECTED: Star icon is not highlighted
        """
        self.event.favourite_icon.click()
        self.assertFalse(self.event.favourite_icon.is_selected(expected_result=False),
                         msg=f'Favourites icon is still highlighted for event "{self.event_name}"')

    def test_006_check_data_layer_response_for_removing_from_favourites_on_football_coupons_page(self):
        """
        DESCRIPTION: Check data layer response for removing from favourites on football page
        EXPECTED: 'action' must be 'remove', 'location' must be 'football coupons'
        """
        self.check_data_layer_favourites_response(object_key='eventAction', action='remove',
                                                  location='football coupons')
