import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_009_SPORT_Specifics.Football_Specifics.Football_Coupons.BaseCouponsTest import BaseCouponsTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.football
@pytest.mark.coupons
@pytest.mark.liveserv_updates
@pytest.mark.sports
@pytest.mark.low
@vtest
class Test_C492613_Verify_auto_hiding_coupons_accordions_on_Coupons_Page(BaseCouponsTest):
    """
    TR_ID: C492613
    VOL_ID: C9698003
    NAME: Verify auto hiding coupons accordions on Coupons Page
    """
    keep_browser_open = True
    autotest_coupon = 'Auto Hiding Test Coupon'

    def test_001_create_test_events(self):
        """
        DESCRIPTION: Add events to the following coupons: Football Autotest Coupon and Football Auto Test Coupon No Cashout
        """
        self.__class__.league_name = tests.settings.football_autotest_competition_league
        event_params = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.autotest_event_id, team1, team2 = event_params.event_id, event_params.team1, event_params.team2
        self.__class__.autotest_event_name = team1 + ' v ' + team2
        market_short_name = self.ob_config.football_config. \
            autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()
        autotest_match_result_market_id = self.ob_config.market_ids[self.autotest_event_id][market_short_name]
        self.ob_config.add_event_to_coupon(market_id=autotest_match_result_market_id, coupon_name=self.autotest_coupon)

        self.__class__.coupon_tab_name = self.get_sport_tab_name(
            self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.coupons,
            self.ob_config.football_config.category_id)

    def test_002_tap_football_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Football' icon on the Sports Menu Ribbon
        EXPECTED: Football Landing page is opened
        """
        self.site.open_sport(name='FOOTBALL')

    def test_003_select_coupons_tab(self):
        """
        DESCRIPTION: Select 'COUPONS' tab
        EXPECTED: 'COUPONS' tab is selected and highlighted
        EXPECTED: List of coupons is displayed on the Coupons Landing page
        """
        self.site.football.tabs_menu.click_button(self.coupon_tab_name)
        current_tab = self.site.football.tabs_menu.current
        self.assertEqual(current_tab, self.coupon_tab_name,
                         msg=f'Active tab is "{current_tab}" but "{self.coupon_tab_name}" is expected to be active')

    def test_004_check_coupon_is_present_on_page(self):
        """
        DESCRIPTION: Check 'Auto Hiding Test Coupon' is present on page
        """
        coupons = self.get_coupons_list_in_coupons_section(coupon_section=vec.coupons.POPULAR_COUPONS.upper())

        self.assertIn(self.autotest_coupon, coupons.keys(),
                      msg=f'"{self.autotest_coupon}" is not found in list of coupons "{coupons.keys()}"')

    def test_005_undisplay_all_events_in_any_of_coupon_group(self):
        """
        DESCRIPTION: Undisplay all events in any of Coupon group
        EXPECTED: All events are undisplayed
        """
        self.ob_config.change_event_state(event_id=self.autotest_event_id, displayed=False, active=True)

    def test_006_reload_the_page(self):
        """
        DESCRIPTION: Reload the page
        EXPECTED: The Coupon is no longer shown in the list
        """
        coupons = self.get_coupons_list_in_coupons_section(coupon_section=vec.coupons.POPULAR_COUPONS.upper())
        if self.autotest_coupon in coupons:
            self.device.refresh_page()
            self.site.wait_splash_to_hide()
        coupons = self.get_coupons_list_in_coupons_section(coupon_section=vec.coupons.POPULAR_COUPONS.upper())
        self.assertNotIn(self.autotest_coupon, coupons.keys(),
                         msg=f'"{self.autotest_coupon}" was found among available coupons "{coupons.keys()}"')

    def test_007_display_event(self):
        """
        DESCRIPTION: Change event's status to displayed and reload the page
        EXPECTED: Corresponding coupon is shown on page
        """
        self.ob_config.change_event_state(event_id=self.autotest_event_id, displayed=True, active=True)
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        coupons = self.get_coupons_list_in_coupons_section(coupon_section=vec.coupons.POPULAR_COUPONS.upper())
        if self.autotest_coupon not in coupons:
            self.device.refresh_page()
            self.site.wait_splash_to_hide()
        self.__class__.coupons = self.get_coupons_list_in_coupons_section(coupon_section=vec.coupons.POPULAR_COUPONS.upper())
        self.assertIn(self.autotest_coupon, self.coupons,
                      msg=f'"{self.autotest_coupon}" was found among available coupons "{self.coupons}"')

    def test_008_open_coupon(self):
        """
        DESCRIPTION: Open coupon
        EXPECTED: It is possible to navigate on Coupons Details page by tapping a row from the list
        """
        self.coupons[self.autotest_coupon].click()
        result = wait_for_result(lambda: self.site.coupon.name == self.site.coupon.name,
                                 timeout=3,
                                 name='Coupon name to be displayed')
        self.assertTrue(result, msg=f'Coupon name in subheader is not the same as expected "{self.autotest_coupon}"')

    def test_009_verify_accordion_with_event(self):
        """
        DESCRIPTION: Verify competition with created event is present
        """
        league_name = tests.settings.football_autotest_competition_league if self.brand != 'ladbrokes' \
            else tests.settings.football_autotest_competition_league.title()
        sections = self.site.coupon.tab_content.accordions_list.items_as_ordered_dict
        self.assertIn(league_name, sections,
                      msg='"%s" is not present in competitions "%s"'
                          % (league_name, ', '.join(sections.keys())))
        date_groups = sections[league_name].items_as_ordered_dict
        self.assertTrue(date_groups, msg='No date groups found on Coupon section %s' % league_name)
        self.assertIn(vec.coupons.COUPON_TIME_HEADER, date_groups,
                      msg='There is no "Today" date group in competition "%s"' % league_name)
        events = date_groups[vec.coupons.COUPON_TIME_HEADER].items_as_ordered_dict
        self.assertTrue(events, msg='No events found on Coupon details page in "Today" date group')
        self.assertIn(self.autotest_event_name, events,
                      msg='No event "%s" found on Coupon details page in date group "Today", found events: "%s"'
                          % (self.autotest_event_name, ', '.join(events.keys())))

    def test_010_undisplay_event(self):
        """
        DESCRIPTION: Undisplay all events in any of Coupon group
        """
        self.ob_config.change_event_state(event_id=self.autotest_event_id, displayed=False, active=True)

    def test_011_reload_the_page(self):
        """
        DESCRIPTION: Reload the page
        EXPECTED: The Coupon accordion is no longer shown in the list
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        no_events = self.site.coupon.tab_content.has_no_events_label()
        if not no_events:
            self.device.refresh_page()
            self.site.wait_splash_to_hide()
            no_events = self.site.coupon.tab_content.has_no_events_label()
        self.assertTrue(no_events, msg='"No events found" text label is not present')
