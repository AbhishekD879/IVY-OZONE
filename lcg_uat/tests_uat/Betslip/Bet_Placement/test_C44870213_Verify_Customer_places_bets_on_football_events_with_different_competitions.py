import pytest
import time
from tests.base_test import vtest
from voltron.environments import constants as vec
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from selenium.common.exceptions import ElementClickInterceptedException


@pytest.mark.uat
@pytest.mark.prod
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.sports
@vtest
class Test_C44870213_Verify_Customer_places_bets_on_football_events_with_different_competitions(BaseBetSlipTest):
    """
    TR_ID: C44870213
    NAME: "Verify Customer places bets on football events with different competitions
    DESCRIPTION: ".Customer places bets on football events with different competitions
    DESCRIPTION: a)Premier league
    DESCRIPTION: b)Champion ship
    DESCRIPTION: c)League One
    DESCRIPTION: d)League Two"
    PRECONDITIONS: UserName: goldenbuild1   Password: password1
    """
    keep_browser_open = True

    def navigate_to_league(self, league_category, league_name):
        if self.device_type == 'mobile':
            category = self.football.tab_content.all_competitions_categories.items_as_ordered_dict.get(league_category)
        else:
            category = self.football.tab_content.accordions_list.items_as_ordered_dict.get(league_category)
        self.assertTrue(category, msg='category is not displayed')
        if not category.is_expanded():
            category.expand()
        league = category.items_as_ordered_dict.get(league_name)
        league.click()
        time.sleep(2)
        if self.device_type == 'mobile' or self.brand == 'ladbrokes':
            title = self.site.competition_league.title_section.type_name.text
            self.assertEqual(title, league_name,
                             msg=f'Actual title "{title}" is not same as'
                                 f'Expected title "{league_name.upper()}"')
        else:
            title = self.football.header_line.page_title.sport_title
            self.assertEqual(title, league_name.upper(),
                             msg=f'Actual title "{title}" is not same as'
                                 f'Expected title "{league_name.upper()}"')

    def test_001_launch_oxygen_application(self):
        """
        DESCRIPTION: Launch oxygen application
        EXPECTED: HomePage opened
        """
        self.site.login()

    def test_002_go_to_football__competition__english__premier_league(self):
        """
        DESCRIPTION: Go to Football > competition > English > premier league
        EXPECTED: Premier league EDP displayed
        """
        self.navigate_to_page(name='sport/football')
        self.__class__.football = self.site.football
        self.football.tabs_menu.click_button(vec.SB.TABS_NAME_COMPETITIONS.upper())
        if self.brand == 'ladbrokes' and self.device_type == 'desktop':
            self.navigate_to_league(league_category=vec.siteserve.ENGLAND.title(), league_name=vec.siteserve.PREMIER_LEAGUE_NAME)
        else:
            self.navigate_to_league(league_category=vec.siteserve.ENGLAND, league_name=vec.siteserve.PREMIER_LEAGUE_NAME)

    def test_003_verify_match_result_market_is_selected_by_defaultverify_user_can_change_the_market_from_drop_down(self):
        """
        DESCRIPTION: verify Match result market is selected by default
        DESCRIPTION: verify user can change the market from drop down
        EXPECTED: user can change the market displayed in drop down
        EXPECTED: - Match Result
        EXPECTED: - Next Team to Score - design updated. Small tweak needed to show Xth goal
        EXPECTED: - Extra Time Result (need designs) Updated design below:
        EXPECTED: - Total Goals Over/Under 2.5
        EXPECTED: - Both Teams to Score
        EXPECTED: - To Win & Both Teams to Score
        EXPECTED: - Draw No Bet
        EXPECTED: - 1st Half Result
        EXPECTED: - To Qualify
        """
        self.assertTrue(self.football.tab_content.has_dropdown_market_selector(),
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
            time.sleep(2)
            actual_market = options.selected_market_selector_item
            self.assertEqual(actual_market.upper(), market.upper(),
                             msg=f'Actual market: "{actual_market.upper()}" is not same as '
                                 f'Expected market: "{market.upper()}"')
            if markets_dropdown_list[-1] != market:
                options = self.site.competition_league.tab_content.dropdown_market_selector

    def test_004_make_a_selection_and_add_to_betslip(self):
        """
        DESCRIPTION: Make a selection and add to betslip
        EXPECTED: Selection added
        """
        bet_buttons_list = self.site.home.bet_buttons
        self.assertTrue(bet_buttons_list, msg='No bet buttons on UI')
        length = len(bet_buttons_list)
        for selection in range(0, length):
            selection_btn = bet_buttons_list[selection]
            self.site.contents.scroll_to_we(selection_btn)
            if selection_btn.is_enabled():
                try:
                    selection_btn.click()
                    break
                except ElementClickInterceptedException:
                    self._logger.info('ElementClickInterceptedException ..')
                    continue
            else:
                continue

    def test_005_verify_bet_is_placed(self):
        """
        DESCRIPTION: Verify bet is placed
        EXPECTED: Bet placed successfully
        """
        if self.device_type == 'mobile':
            self.site.wait_for_quick_bet_panel()
            self.site.quick_bet_panel.add_to_betslip_button.click()
            self.site.wait_quick_bet_overlay_to_hide()
            self.site.open_betslip()
        self.__class__.bet_amount = 1
        self.place_and_validate_single_bet()
        self.site.bet_receipt.footer.click_done()

    def test_006_verify_user_can_change_the_competition_to_national_league_league_1_league_2_etc_and_repeat_step_2_to_57_for_all_competition(self):
        """
        DESCRIPTION: Verify user can change the competition to National league, league 1 League 2 etc and repeat step #2 to 57 for all competition
        """
        self.device.go_back()
        if self.brand == 'ladbrokes' and self.device_type == 'desktop':
            self.navigate_to_league(league_category=vec.siteserve.ENGLAND.title(), league_name=vec.siteserve.CHAMPIONSHIP)
        else:
            self.navigate_to_league(league_category=vec.siteserve.ENGLAND, league_name=vec.siteserve.CHAMPIONSHIP)
        self.test_003_verify_match_result_market_is_selected_by_defaultverify_user_can_change_the_market_from_drop_down()
        self.test_004_make_a_selection_and_add_to_betslip()
        self.test_005_verify_bet_is_placed()
        self.device.go_back()
        if self.brand == 'ladbrokes' and self.device_type == 'desktop':
            self.navigate_to_league(league_category=vec.siteserve.SPAIN.title(), league_name=vec.siteserve.LALIGA)
        else:
            self.navigate_to_league(league_category=vec.siteserve.SPAIN, league_name=vec.siteserve.LALIGA)
        self.test_003_verify_match_result_market_is_selected_by_defaultverify_user_can_change_the_market_from_drop_down()
        self.test_004_make_a_selection_and_add_to_betslip()
        self.test_005_verify_bet_is_placed()
