import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod #Events with specific markets cannot be created in Prod/Beta
@pytest.mark.market_switcher
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C60089509_Verify_MS_sticky_behavior_on_Matches_Tab_for_Basketball_SLP(BaseSportTest):
    """
    TR_ID: C60089509
    NAME: Verify MS sticky behavior on Matches Tab for Basketball SLP
    DESCRIPTION: This test case verifies 'Market Selector' sticky behavior on Basketball landing page
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Games Total (Over/Under)|,|Games Handicap (Handicap)|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Basketball Landing page -> 'Matches' tab
    PRECONDITIONS: 3. Make sure that 'Market Selector' is present on the page
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following Market Template Names:
    PRECONDITIONS: * |Money Line (WW)| - "Money Line"
    PRECONDITIONS: * |Total Points (Over/Under)| - "Total Points"
    PRECONDITIONS: * |Handicap 2-way (Handicap)| - "Handicap"
    PRECONDITIONS: * |Home Team Total Points (Over/Under)| - "Home Team Total Points"
    PRECONDITIONS: * |Away Team Total Points (Over/Under)| - "Away Team Total Points"
    PRECONDITIONS: 2) To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True
    expected_market_selector_options = [vec.siteserve.EXPECTED_MARKETS_NAMES.money_line,
                                        vec.siteserve.EXPECTED_MARKETS_NAMES.total_points,
                                        vec.siteserve.EXPECTED_MARKETS_NAMES.handicap_2_way,
                                        vec.siteserve.EXPECTED_MARKETS_NAMES.home_team_total_points,
                                        vec.siteserve.EXPECTED_MARKETS_NAMES.away_team_total_points]
    event_markets = [
        ('total_points',),
        ('handicap_2_way',),
        ('home_team_total_points',),
        ('away_team_total_points',)]

    def verify_sticky_behavior(self, market):
        is_sticky = self.basketball_tab_content.is_market_selector_sticky
        self.assertTrue(is_sticky, msg='"Market Selector" is not sticky in Basketball Sport Page')
        drop_down_list = self.basketball_tab_content.dropdown_market_selector
        drop_down_list.items_as_ordered_dict.get(market).click()
        selected_market = self.basketball_tab_content.dropdown_market_selector.value
        self.assertEqual(selected_market, market, msg=f'Actual Market: "{selected_market}" is not same as'
                                                      f'Expected Market: "{market}", Market selector functionality is not same')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Basketball events  with scores
        EXPECTED: Event is successfully created
        """
        all_sport_MS_Status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports',
                                                                                       status=True)
        self.assertTrue(all_sport_MS_Status, msg='Market switcher is disabled for all sports')
        market_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='basketball',
                                                                                          status=True)
        self.assertTrue(market_switcher_status, msg='Market switcher is disabled for basketball sport')
        self.__class__.section_name = tests.settings.basketball_us_league
        self.cms_config.verify_and_update_sport_config(
            sport_category_id=self.ob_config.backend.ti.basketball.category_id,
            disp_sort_names='HL,WH,HH',
            primary_markets='|Money Line|,|Total Points|,'
                            '|Home team total points|,|Away team total points|,'
                            '|Half Total Points|,|Quarter Total Points|,'
                            '|Handicap 2-way|')
        self.ob_config.add_basketball_event_to_us_league(markets=self.event_markets)
        self.__class__.market_selector_default_value = vec.siteserve.EXPECTED_MARKETS_NAMES.money_line
        self.navigate_to_page(name='sport/basketball')
        self.site.wait_content_state(state_name='basketball')
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                    self.ob_config.basketball_config.category_id)
        current_tab_name = self.site.contents.tabs_menu.current
        self.assertEqual(current_tab_name, expected_tab_name,
                         msg=f'Actual tab: "{current_tab_name}" is not same as'
                             f'Expected tab: "{expected_tab_name}".')
        self.__class__.basketball_tab_content = self.site.basketball.tab_content
        self.assertTrue(self.basketball_tab_content.has_dropdown_market_selector(),
                        msg='"Market Selector" drop-down is not displayed on basketball landing page')

    def test_001_verify_that_market_selector_is_sticky_when_scrolling_the_page_down(self):
        """
        DESCRIPTION: Verify that 'Market Selector' is sticky when scrolling the page down
        EXPECTED: Tablet/Mobile:
        EXPECTED: • 'Market Selector' is sticky. It remains at the top of the scrolling page
        EXPECTED: • Market selector functionality remains the same
        EXPECTED: **Note:**
        EXPECTED: For the Desktop 'Market Selector' is NOT sticky. It becomes hidden together with Date Selector panel
        """
        self.site.contents.scroll_to_bottom()
        self.__class__.markets = list(self.basketball_tab_content.dropdown_market_selector.items_as_ordered_dict.keys())
        self.assertTrue(self.markets, msg='Markets not found')
        self.verify_sticky_behavior(self.markets[1])

    def test_002_verify_that_market_selector_is_sticky_when_scrolling_the_page_up(self):
        """
        DESCRIPTION: Verify that 'Market Selector' is sticky when scrolling the page up
        EXPECTED: Tablet/Mobile:
        EXPECTED: • 'Market Selector' is sticky. It remains at the top of the scrolling page
        EXPECTED: • Market selector functionality remains the same
        EXPECTED: **Note:**
        EXPECTED: For the Desktop 'Market Selector' is NOT sticky. It becomes hidden together with Date Selector panel
        """
        self.site.contents.scroll_to_top()
        self.verify_sticky_behavior(self.markets[2])
