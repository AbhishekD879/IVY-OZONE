import pytest
from time import sleep
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


@pytest.mark.uat
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C44870209_Verify_Market_selector_is_displayed_for_football_only(Common):
    """
    TR_ID: C44870209
    NAME: Verify Market selector is displayed for football only
    DESCRIPTION: "Check Market selector is only displayed for football
    DESCRIPTION: - Football Landing pages for the upcoming section
    DESCRIPTION: - In-Play tab on the FB landing page
    DESCRIPTION: - FB competition type page - Matches tab
    DESCRIPTION: - FB coupons detail page
    DESCRIPTION: Verify user sees drop down when clicks on the market selector in below order
    DESCRIPTION: - Match Result
    DESCRIPTION: - Next Team to Score - design updated. Small tweak needed to show Xth goal
    DESCRIPTION: - Extra Time Result (need designs) Updated design below:
    DESCRIPTION: - Total Goals Over/Under 2.5
    DESCRIPTION: -  Both Teams to Score
    DESCRIPTION: - To Win & Both Teams to Score
    DESCRIPTION: - Draw No Bet
    DESCRIPTION: -  1st Half Result
    DESCRIPTION: - To Qualify
    DESCRIPTION: Verify display of the page with the new market template when user changes to a different market from market selector
    DESCRIPTION: Verify dropdown with the list of markets should be made scrollable
    DESCRIPTION: Verify user sees sticky market selector when scrolls through the upcoming module "
    """
    keep_browser_open = True

    def navigate_to_league(self, league_category, league_name):
        if self.device_type == 'mobile':
            category = self.football_sport.tab_content.all_competitions_categories.items_as_ordered_dict.get(
                league_category)
        else:
            category = self.football_sport.tab_content.accordions_list.items_as_ordered_dict.get(league_category)
        self.assertTrue(category, msg='category is not displayed')
        if not category.is_expanded():
            category.expand()
        league = category.items_as_ordered_dict.get(league_name)
        league.click()
        self.assertTrue(self.football_sport.tab_content.has_dropdown_market_selector(),
                        msg='"Market Selector" drop-down is not displayed for Football')

    def test_001_launch_oxygen_application(self):
        """
        DESCRIPTION: Launch oxygen application
        EXPECTED: HomePage opened
        """
        self.site.wait_content_state('Homepage')

    def test_002_go_to_football__competition__premier_league__market_selector_is_displayed_for_football(self):
        """
        DESCRIPTION: Go to Football > competition > premier league > Market selector is displayed for football
        EXPECTED: Market selector is displayed
        """
        self.navigate_to_page(name='sport/football')
        self.__class__.football_sport = self.site.football
        self.football_sport.tabs_menu.click_button(vec.SB.TABS_NAME_COMPETITIONS.upper())
        if self.brand == 'ladbrokes' and self.device_type == 'desktop':
            self.navigate_to_league(league_category=vec.siteserve.ENGLAND.title(),
                                    league_name=vec.siteserve.PREMIER_LEAGUE_NAME)
        else:
            self.navigate_to_league(league_category=vec.siteserve.ENGLAND, league_name=vec.siteserve.PREMIER_LEAGUE_NAME)

    def test_003_verify_match_result_market_is_selected_by_default(self):
        """
        DESCRIPTION: verify Match result market is selected by default
        EXPECTED: Match result market is selected by default
        """
        # covered in step 004
        pass

    def test_004_verify_user_can_change_the_market_from_drop_down(self):
        """
        DESCRIPTION: verify user can change the market from drop down
        EXPECTED: user can change the market displayed in drop down
        EXPECTED: -Match Result
        EXPECTED: -Total Goals Over/Under
        EXPECTED: -Both teams to Score
        EXPECTED: -To Win & Both teams to score
        EXPECTED: -Draw no Bet
        EXPECTED: -1st Half Result
        """
        self.assertTrue(self.football_sport.tab_content.has_dropdown_market_selector(),
                        msg='"Market Selector" drop-down is not displayed')
        options = self.site.competition_league.tab_content.dropdown_market_selector
        match_result = options.selected_market_selector_item
        if self.brand == 'ladbrokes' and self.device_type == 'desktop':
            self.assertEqual(match_result, vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default.upper(),
                             msg=f'Actual market: "{match_result}" not same as '
                                 f'"{vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default.upper()}"')
        else:
            self.assertEqual(match_result, vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default,
                             msg=f'Actual market: "{match_result}" not same as '
                                 f'"{vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default}"')
        markets_dropdown_list = list(options.items_as_ordered_dict.keys())
        for market in markets_dropdown_list:
            options.select_value(value=market)
            sleep(3)
            actual_market = options.selected_market_selector_item
            self.assertEqual(actual_market.upper(), market.upper(),
                             msg=f'Actual market: "{actual_market.upper()}" is not same as '
                                 f'Expected market: "{market.upper()}"')
            if markets_dropdown_list[-1] != market:
                options = self.site.competition_league.tab_content.dropdown_market_selector
        self.site.contents.scroll_to_bottom()
        footer_logo = self.site.footer.footer_section_bottom.items_as_ordered_dict.items()
        self.assertTrue(footer_logo, msg='footer logo is not displayed')

    def test_005_verify_display_of_the_page_with_the_new_market_template_when_user_changes_to_a_different_market_from_market_selector(self):
        """
        DESCRIPTION: Verify display of the page with the new market template when user changes to a different market from market selector
        EXPECTED: Fixture is displayed as per the selected market
        """
        # covered in step 004
        pass

    def test_006_verify_dropdown_with_the_list_of_markets_should_be_made_scrollable(self):
        """
        DESCRIPTION: Verify dropdown with the list of markets should be made scrollable
        EXPECTED: Drop down list of Events for the available markets are displayed and scrollable
        """
        # covered in step 004
        pass

    def test_007_verify_user_can_change_the_competition_and_repeat_step_3_to_7_for_all_competition(self):
        """
        DESCRIPTION: Verify user can change the competition and repeat step #3 to #6 for all competition
        """
        self.device.go_back()
        if self.brand == 'ladbrokes' and self.device_type == 'desktop':
            self.navigate_to_league(league_category=vec.siteserve.ENGLAND.title(),
                                    league_name=vec.siteserve.CHAMPIONSHIP)
        else:
            self.navigate_to_league(league_category=vec.siteserve.ENGLAND, league_name=vec.siteserve.CHAMPIONSHIP)
        self.test_004_verify_user_can_change_the_market_from_drop_down()
        self.device.go_back()
        if self.brand == 'ladbrokes' and self.device_type == 'desktop':
            self.navigate_to_league(league_category=vec.siteserve.SPAIN.title(), league_name=vec.siteserve.LALIGA)
        else:
            self.navigate_to_league(league_category=vec.siteserve.SPAIN, league_name=vec.siteserve.LALIGA)
        self.test_004_verify_user_can_change_the_market_from_drop_down()
