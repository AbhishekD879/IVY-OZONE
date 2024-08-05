import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod - Event creation can not be done on PROD
@pytest.mark.market_switcher
@pytest.mark.desktop
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C60089652_Verify_No_MS_should_be_displayed_for_Tennis(Common):
    """
    TR_ID: C60089652
    NAME: Verify No MS should be displayed for Tennis
    DESCRIPTION: This test case verifies undisplaying of market switcher should be displayed for Tennis
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Tennis Landing page -> Matches, Inplay and Competitions  tab
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) Markets should be created in OB system
    PRECONDITIONS: 2) To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 3. Toggle should not be configured in CMS
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Create Tennis event
        EXPECTED: Event is created
        """
        self.ob_config.add_tennis_event_to_autotest_trophy()

    def test_001_navigate_to_tennis___click_on_matches_tab(self):
        """
        DESCRIPTION: Navigate to Tennis -> Click on Matches Tab
        EXPECTED: Market Switcher dropdown should not be displayed
        """
        self.navigate_to_page(name='sport/tennis')
        self.site.wait_content_state('tennis')
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                    self.ob_config.tennis_config.category_id)
        current_tab_name = self.site.sports_page.tabs_menu.current
        if current_tab_name != expected_tab_name:
            self.site.sports_page.tabs_menu.items_as_ordered_dict.get(expected_tab_name).click()
            current_tab_name = self.site.sports_page.tabs_menu.current
        self.assertEqual(current_tab_name, expected_tab_name,
                         msg=f'Actual tab: "{current_tab_name}" is not same as Expected Tab: "{expected_tab_name}"')
        has_market_selector = self.site.sports_page.tab_content.has_dropdown_market_selector()
        self.assertFalse(has_market_selector, msg=' "Market selector" is available for Tennis -> Matches')

    def test_002_navigate_to_tennis___click_on_inplay_tab(self):
        """
        DESCRIPTION: Navigate to Tennis -> Click on Inplay Tab
        EXPECTED: Market Switcher dropdown should not be displayed
        """
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.in_play,
                                                    self.ob_config.tennis_config.category_id)
        self.site.sports_page.tabs_menu.items_as_ordered_dict.get(expected_tab_name).click()
        current_tab_name = self.site.sports_page.tabs_menu.current
        self.assertEqual(current_tab_name, expected_tab_name,
                         msg=f'Actual tab: "{current_tab_name}" is not same as Expected Tab: "{expected_tab_name}"')
        has_market_selector = self.site.sports_page.tab_content.has_dropdown_market_selector()
        self.assertFalse(has_market_selector, msg=' "Market selector" is available for Tennis - > In Play')

    def test_003_navigate_to_tennis___click_on_competition_tab(self):
        """
        DESCRIPTION: Navigate to Tennis -> Click on Competition Tab
        EXPECTED: Market Switcher dropdown should not be displayed
        """
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                                    self.ob_config.tennis_config.category_id)
        self.site.sports_page.tabs_menu.items_as_ordered_dict.get(expected_tab_name).click()
        current_tab_name = self.site.sports_page.tabs_menu.current
        self.assertEqual(current_tab_name, expected_tab_name,
                         msg=f'Actual tab: "{current_tab_name}" is not same as Expected Tab: "{expected_tab_name}"')
        has_market_selector = self.site.sports_page.tab_content.has_dropdown_market_selector()
        self.assertFalse(has_market_selector, msg=' "Market selector" is available for Tennis -> Competition')
