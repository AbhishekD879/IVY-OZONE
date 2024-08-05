import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod #Events with specific markets cannot created in Prod/Beta
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.mobile_only
@pytest.mark.market_switcher
@vtest
class Test_C60089555_Verify_MS_sticky_behavior_on_Matches_Tab_for_Boxing_SLP(Common):
    """
    TR_ID: C60089555
    NAME: Verify MS sticky behavior on Matches Tab for Boxing SLP
    DESCRIPTION: This test case verifies 'Market Selector' sticky behavior on Boxing  landing page
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Games Total (Over/Under)|,|Games Handicap (Handicap)|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Boxing  landing page -> 'Matches' tab
    PRECONDITIONS: 3. Make sure that 'Market Selector' is present on the page
    PRECONDITIONS: Note:
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following Market Template Names:
    PRECONDITIONS: |Fight Betting (WDW)| - "Fight Betting"
    PRECONDITIONS: 2) To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. Load the app
        PRECONDITIONS: 2. Go to the Boxing landing page -> 'Matches' tab
        PRECONDITIONS: 3. Make sure that 'Market Selector' is present on the page
        """
        all_sports_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports',
                                                                                     status=True)
        self.assertTrue(all_sports_status, msg='"All Sports" market switcher status is disabled')
        market_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='boxing', status=True)
        self.assertTrue(market_switcher_status, msg='Market switcher is disabled for Boxing sport')
        self.cms_config.verify_and_update_sport_config(sport_category_id=self.ob_config.boxing_config.category_id,
                                                       disp_sort_names='MR',
                                                       primary_markets='|Fight Betting|')
        self.ob_config.add_autotest_boxing_event()
        self.navigate_to_page(name='sport/boxing')
        self.site.wait_content_state_changed()
        current_tab_name = self.site.boxing.tabs_menu.current
        self.assertEqual(current_tab_name, vec.sb.TABS_NAME_FIGHTS.upper(),
                         msg=f'Default tab is "{current_tab_name}",instead of "{vec.sb.TABS_NAME_FIGHTS}"')
        self.__class__.boxing = self.site.boxing.tab_content
        has_market_selector = self.boxing.has_dropdown_market_selector()
        self.assertTrue(has_market_selector, msg=' "Market Selector" drop-down is not displayed on Fights tab in boxing')

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
        market = list(self.boxing.dropdown_market_selector.items_as_ordered_dict.keys())
        self.assertTrue(market, msg='No markets available in the market switcher dropdown')
        is_sticky = self.boxing.is_market_selector_sticky
        self.assertTrue(is_sticky, msg='"Market Selector" is not sticky in Fights tab for Boxing')
        drop_down_list = self.boxing.dropdown_market_selector
        drop_down_list.items_as_ordered_dict.get(market[0]).click()
        selected_market = self.boxing.dropdown_market_selector.value
        self.assertEqual(selected_market, market[0], msg=f'Actual Market: "{selected_market}" is not same as the'
                                                         f'Expected Market: "{market[0]}"')

    def test_002_verify_that_market_selector_is_sticky_when_scrolling_the_page_up(self):
        """
        DESCRIPTION: Verify that 'Market Selector' is sticky when scrolling the page up
        EXPECTED: Tablet/Mobile:
        EXPECTED: • 'Market Selector' is sticky. It remains at the top of the scrolling page
        EXPECTED: • Market selector functionality remains the same
        EXPECTED: **Note:**
        EXPECTED: For the Desktop 'Market Selector' is NOT sticky. It becomes hidden together with Date Selector panel
        """
        # Market selector functionality remains the same covered in step 1
        is_sticky = self.boxing.is_market_selector_sticky
        self.assertTrue(is_sticky, msg='"Market Selector" is not sticky in Fights tab for Boxing')
