from datetime import date
from datetime import datetime
from datetime import timedelta
from fractions import Fraction

import pytest
from dateutil.parser import parse

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.hl
# @pytest.mark.prod  # can't modify coupons on prod/hl
@pytest.mark.football
@pytest.mark.coupons
@pytest.mark.low
@pytest.mark.desktop
# we can not run such test simultaneously with other coupons
@pytest.mark.consequent
@vtest
class Test_C440334_Verify_events_grouping_on_Coupons_Details_page(BaseBetSlipTest, BaseSportTest):
    """
    TR_ID: C440334
    NAME: Verify events grouping on Coupons Details page
    DESCRIPTION: This test case verifies events grouping on Coupons Details page
    PRECONDITIONS: 1) In order to get a list of coupons use the following link:
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Coupon?existsFilter=coupon:simpleFilter:event.startTime:greaterThanOrEqual:2017-07-04T21:00:00.000Z&existsFilter=coupon:simpleFilter:event.suspendAtTime:greaterThan:2017-07-05T13:09:30.000Z&existsFilter=coupon:simpleFilter:event.isStarted:isFalse&simpleFilter=coupon.siteChannels:contains:M&existsFilter=coupon:simpleFilter:event.categoryId:intersects:16&existsFilter=coupon:simpleFilter:event.cashoutAvail:equals:Y&translationLang=en
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 2) In order to get an information about particular coupon use the following link:
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/CouponToOutcomeForCoupon/XXX?simpleFilter=event.startTime:lessThan:2017-07-15T09:01:00.000Z&simpleFilter=event.categoryId:intersects:16&simpleFilter=event.siteChannels:contains:M&simpleFilter=event.isStarted:isFalse&simpleFilter=event.startTime:greaterThanOrEqual:2017-07-09T21:00:00.000Z&simpleFilter=event.suspendAtTime:greaterThan:2017-07-10T09:01:00.000Z&translationLang=en
    PRECONDITIONS: XXX - coupon's id
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 3) In order to create coupons use the following instruction https://confluence.egalacoral.com/display/SPI/How+to+create+a+Coupon+in+OB+and+TI+system
    """
    keep_browser_open = True
    current_date_tab = vec.sb.TABS_NAME_TODAY
    tomorrow_date_tab = vec.sb.TABS_NAME_TOMORROW
    current_year = date.today().year
    autotest_league = tests.settings.football_autotest_competition_league
    expected_day_format_pattern = '%d %b %Y'
    expected_day_time_format_pattern = '%d %b %I:%M %p'
    uk_coupon_name = 'UK Coupon'

    def check_events_date(self, event_name, date_group=current_date_tab):
        events = self.date_sections[date_group].items_as_ordered_dict
        self.assertTrue(events, msg=f'No event found for {date_group} date/time grouping')
        self.assertIn(event_name, events, msg=f'No event "{event_name}" found in events list "{events.keys()}"')
        event = events[event_name]
        self.compare_date_time(item_time_ui=event.event_time, event_date_time_ob=self.event1_time,
                               format_pattern=self.event_card_today_time_format_pattern,
                               dayfirst=False) \
            if date_group == self.current_date_tab else \
            self.compare_date_time(item_time_ui=event.event_time, event_date_time_ob=self.event5days_time,
                                   format_pattern=self.expected_day_time_format_pattern,
                                   dayfirst=False)

    def test_000_preconditions(self):
        """
        DESCRIPTION: Adds football events with a coupon
        """
        if self.brand == 'ladbrokes' and self.device_type == 'desktop':
            self.__class__.current_date_tab = self.current_date_tab.title()
            self.__class__.tomorrow_date_tab = self.tomorrow_date_tab.title()
        event_params = self.ob_config.add_autotest_premier_league_football_event()
        market_short_name = self.ob_config.football_config. \
            autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()
        self.__class__.team1, self.__class__.team2 = event_params.team1, event_params.team2
        autotest_match_result_market_id = self.ob_config.market_ids[event_params.event_id][market_short_name]
        self.ob_config.add_event_to_coupon(market_id=autotest_match_result_market_id, coupon_name=self.uk_coupon_name)
        self.__class__.event1_name = '%s v %s' % (self.team1, self.team2)
        self.__class__.selection_ids = event_params.selection_ids
        self.__class__.event1_time = event_params.event_date_time

        event_params_5days = self.ob_config.add_autotest_premier_league_football_event(
            start_time=self.get_date_time_formatted_string(days=5))
        self.__class__.team1_2, self.__class__.team2_2 = event_params_5days.team1, event_params_5days.team2
        self.__class__.event_5days_name = '%s v %s' % (self.team1_2, self.team2_2)
        autotest_5days_match_result_market_id = self.ob_config.market_ids[event_params_5days.event_id][market_short_name]
        self.ob_config.add_event_to_coupon(market_id=autotest_5days_match_result_market_id,
                                           coupon_name=self.uk_coupon_name)
        self.__class__.event5days_time = event_params_5days.event_date_time

        self.__class__.coupon_tab_name = self.get_sport_tab_name(
            self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.coupons,
            self.ob_config.football_config.category_id)

    def test_001_navigate_to_football_page(self):
        """
        DESCRIPTION: Navigate to Football page
        EXPECTED: 'Matches' tab is opened by default and highlighted
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('Football')
        result = self.site.football.tabs_menu.current
        self.assertTrue(result, msg=f'"{self.expected_sport_tabs.matches}" tab was not opened')

    def test_002_tap_coupons_tab(self):
        """
        DESCRIPTION: Open coupons tab
        """
        self.site.football.tabs_menu.click_button(self.coupon_tab_name)
        current_tab = self.site.football.tabs_menu.current
        self.assertEqual(current_tab, self.coupon_tab_name,
                         msg=f'Coupons tab is not active, active is "{current_tab}"')

    def test_003_select_coupons_tab(self):
        """
        DESCRIPTION: Select 'Coupons' tab
        EXPECTED: * 'Coupons' tab is selected and highlighted
        EXPECTED: * Coupons Landing page is loaded
        EXPECTED: * List of coupons is displayed on the Coupons Landing page
        """
        coupon_categories = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(coupon_categories, msg='Can not find any coupon category')

        # Popular Coupons
        popular_coupons = coupon_categories.get(vec.coupons.POPULAR_COUPONS.upper(), None)
        self.assertTrue(popular_coupons, msg=f'Can not find: "{vec.coupons.POPULAR_COUPONS.upper()}" coupon')

        self.__class__.coupons_list = popular_coupons.items_as_ordered_dict
        self.assertTrue(self.coupons_list, msg='Can not find any coupon')

    def test_004_navigate_to_uk_coupon(self):
        """
        DESCRIPTION: Navigate to UK Coupon
        EXPECTED: * Events for selected coupon are displayed on Coupons Details page
        """
        self.assertIn(self.uk_coupon_name, self.coupons_list.keys(),
                      msg=f'"{self.uk_coupon_name}" is not found in list of coupons "{self.coupons_list.keys()}"')
        self.coupons_list.get(self.uk_coupon_name).click()
        self.site.wait_content_state('CouponPage')
        self.__class__.sections = self.site.coupon.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.sections, msg='No event groups found on Coupon page')

    def test_005_verify_event_section(self):
        """
        DESCRIPTION: Verify event section
        EXPECTED: First **three** accordions are expanded by default, remaining are collapsed
        EXPECTED: Event name and prices are the same as configured in TI
        """
        if self.brand == 'ladbrokes' and self.device_type == 'mobile':
            self.__class__.autotest_league = self.autotest_league.title()
        self.__class__.date_sections = self.sections[self.autotest_league].items_as_ordered_dict
        self.assertTrue(self.date_sections, msg='No date sections found in "%s" section'
                                                % self.autotest_league)
        self.assertIn(self.current_date_tab, self.date_sections,
                      msg=f'No "{self.current_date_tab}" date group found in list of dates "{self.date_sections.keys()}"')
        self.__class__.other_day = self.get_date_time_formatted_string(time_format='%-d %b', days=5)
        if self.brand == 'ladbrokes' and self.device_type == 'mobile':
            self.__class__.other_day = self.other_day.upper()
        self.assertIn(self.other_day, self.date_sections,
                      msg=f'No "{self.other_day}" date group found in list of dates "{self.date_sections.keys()}"')

        today_events = self.date_sections[self.current_date_tab].items_as_ordered_dict
        self.assertTrue(today_events, msg='No Today events found')
        self.assertIn(self.event1_name, today_events,
                      msg=f'No event "{self.event1_name}" found in events list "{today_events.keys()}"')
        event = today_events[self.event1_name]
        self.verify_event_time_is_present(event)
        self.__class__.all_prices = event.get_active_prices()
        self.assertListEqual(sorted(list(self.all_prices.keys())), sorted(list(self.selection_ids.keys())))
        prices = {outcome_name: outcome.outcome_price_text for outcome_name, outcome in self.all_prices.items()}
        self.assertEqual(prices[self.team1], self.ob_config.event.prices['odds_home'],
                         msg=f'Home team price "{prices[self.team1]}" '
                             f'is not the same as expected "{self.ob_config.event.prices["odds_home"]}"')
        self.assertEqual(prices[self.team2], self.ob_config.event.prices['odds_away'],
                         msg=f'Home team price "{prices[self.team2]}" '
                             f'is not the same as expected "{ self.ob_config.event.prices["odds_away"]}"')
        self.assertEqual(float(Fraction(prices['Draw']) + 1), float(Fraction(self.ob_config.event.prices['odds_draw']) + 1),
                         msg=f'Home team price "{prices["Draw"]}" '
                             f'is not the same as expected "{self.ob_config.event.prices["odds_draw"]}"')

    def test_006_verify_event_start_time(self):
        """
        DESCRIPTION: Verify Event Start Time of the list of events, should be present events only for 5 next days
        """
        self.check_events_date(event_name=self.event1_name, date_group=self.current_date_tab)
        self.check_events_date(event_name=self.event_5days_name, date_group=self.other_day)
        self.assertIn(self.other_day, self.date_sections,
                      msg=f'No "{self.other_day}" date group found in list of dates "{self.date_sections.keys()}"')
        for day_name, day in self.date_sections.items():
            events = day.items_as_ordered_dict
            self.assertTrue(events, msg=f'No event found for "{day_name}" date/time grouping')
            if day_name in [self.current_date_tab, self.tomorrow_date_tab]:
                for event_name, event in events.items():
                    date_converted = datetime.strptime(event.event_time, self.event_card_today_time_format_pattern)
                    self.assertTrue(date_converted <= datetime.now() + timedelta(days=5),
                                    msg=f'Event "{event_name}" date "{date_converted}" is more than 5 days after today')
            else:
                day_name_converted = parse('%s %s' % (day_name, self.current_year))
                self.assertTrue(day_name_converted <= datetime.now() + timedelta(days=5),
                                msg=f'Date "{day_name_converted}" is more than 5 days after today')
                for event_name, event in events.items():
                    date_time_converted = parse(event.event_time)
                    self.assertTrue(date_time_converted <= datetime.now() + timedelta(days=5),
                                    msg=f'Event name "{event_name}" date "{date_time_converted}"'
                                        f' is more than 5 days after today')

    def test_007_tap_back_button(self):
        """
        DESCRIPTION: Tap 'Back' button
        EXPECTED: * Coupons Landing page is loaded
        EXPECTED: * List of coupons is displayed
        """
        self.site.back_button_click()

        current_tab = self.site.football.tabs_menu.current
        self.assertEqual(current_tab, self.coupon_tab_name,
                         msg=f'Active tab is {current_tab} but Coupons is expected to be active')
