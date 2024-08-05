import pytest

import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_013_Retail_Connect_Features.Football_Bet_Filter.BaseFootballBetFilter import BaseFootballBetFilter
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.voltron_exception import VoltronException


# @pytest.mark.tst2  # football filter has endpoints just for prod
# @pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.lad_beta2
@pytest.mark.medium
@pytest.mark.bet_filter
@pytest.mark.football_bet_filter
@pytest.mark.connect
@pytest.mark.retail
@pytest.mark.desktop
@pytest.mark.adhoc_suite
@pytest.mark.football_specific
@pytest.mark.sports_specific
@vtest
# this test case covers C65949643
class Test_C2064791_Verify_general_view_of_Football_bet_filter_screen(BaseFootballBetFilter):
    """
    TR_ID: C2064791
    NAME: Verify general view of Football bet filter screen
    DESCRIPTION: This test case verifies general view of Football bet filter screen
    """
    keep_browser_open = True
    expected_bet_filter_tabs = [vec.retail.YOUR_TEAMS_TAB, vec.retail.THE_OPPOSITION_TAB, vec.retail.SAVED_FILTERS_TAB]

    def test_000_preconditions(self):
        """
        DESCRIPTION: Make sure Football Bet Filter feature is turned on in CMS: System configuration -> Connect -> football Filter
        DESCRIPTION: **Coral:**
        DESCRIPTION: 1. Load SportBook
        DESCRIPTION: 2. Select 'Connect' from header ribbon
        DESCRIPTION: 3. Select 'Football Bet Filter' item
        DESCRIPTION: **Ladbrokes:**
        DESCRIPTION: Load SportBook > Go to Football > 'Coupons' tab > Select any coupon that contains events with 'Match result' market (In Console: search 'coupon' - find coupons with couponSortCode: "MR">)
        """
        cms_config = self.get_initial_data_system_configuration().get('Connect', {})
        if not cms_config:
            cms_config = self.cms_config.get_system_configuration_item('Connect')
        if not cms_config.get('footballFilter'):
            raise CmsClientException('"Football Bet Filter" is disabled')
        self.navigate_to_page('sport/football/coupons')
        self.site.wait_content_state(state_name='Football')

        types_of_coupons = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        if not types_of_coupons:
            raise VoltronException('Coupons are not available')

        featured_coupons_type_name, featured_coupons_type = next(
            ([type_name, type_obj] for type_name, type_obj in types_of_coupons.items() if
             type_name.upper() != 'POPULAR COUPONS'), [None, None])
        popular_coupons_type_name, popular_coupons_type = next(
            ([type_name, type_obj] for type_name, type_obj in types_of_coupons.items() if
             type_name.upper() == 'POPULAR COUPONS'), [None, None])

        # featured coupons , popular  coupons
        popular_coupons_location_status = popular_coupons_type.location.get('y') > featured_coupons_type.location.get(
            'y')
        self.assertTrue(popular_coupons_location_status, f'popular coupons are not in correct location')

        self.__class__.coupon_name = self.open_bet_filter_via_coupon()

        bet_filter = self.site.football_bet_filter
        result = bet_filter.tab_menu.open_tab(vec.retail.YOUR_TEAMS_TAB)
        self.assertTrue(result, msg=f'"{vec.retail.YOUR_TEAMS_TAB}" tab is not active')

    def test_001_verify_the_sub_header_section(self):
        """
        DESCRIPTION: Verify the sub header section
        EXPECTED: **Coral:**
        EXPECTED: - [<] back button in the left is displayed
        EXPECTED: - 'FOOTBALL BET FILTER' near back button
        EXPECTED: - 'For online bets only' label - if user selected online betting before opening Bet Filter page
        EXPECTED: - 'For in-shop bets only' - if user selected in-shop betting before opening Bet Filter page
        EXPECTED: - [reset icon] + RESET label - resetting all filters to their default values
        EXPECTED: **Ladbrokes:**
        EXPECTED: - [<] back button in the left is displayed (Mobile only, in the header)
        EXPECTED: - 'FOOTBALL BET FILTER' in the left on the black background
        EXPECTED: - 'Reset filters' link in the right on the black background - resetting all filters to their default values
        """
        if not (self.brand == 'ladbrokes' and self.device_type == 'desktop'):
            self.assertTrue(self.site.football_bet_filter.header_line.back_button.is_displayed(),
                            msg='Back button is not displayed')
        if self.brand == 'bma':
            page_title = self.site.football_bet_filter.header_line.page_title.title
        else:
            page_title = self.site.football_bet_filter.sub_header.title
        self.assertEqual(page_title, vec.retail.FB_BET_FILTER_NAME,
                         msg=f'Page title "{page_title}" is not the same as expected "{vec.retail.FB_BET_FILTER_NAME}"')

        if self.brand == 'bma':
            headers_titles = [vec.retail.FOR_IN_SHOP_BETS_ONLY, vec.retail.FOR_ONLINE_BETS_ONLY]
            page_sub_header = self.site.football_bet_filter.sub_header.title
            self.assertIn(page_sub_header, headers_titles,
                          msg=f'Sub title "{page_sub_header}" is not one from expected "{headers_titles}"')

            self.assertTrue(self.site.football_bet_filter.sub_header.has_refresh_icon(),
                            msg='Can not find refresh button')

            refresh_button_name = self.site.football_bet_filter.sub_header.refresh_button.name
            reset_title = vec.retail.RESET_TEXT if self.brand != 'ladbrokes' else vec.bet_finder.RESET_FILTERS
            self.assertEqual(refresh_button_name, reset_title,
                             msg=f'Refresh button name "{refresh_button_name}" is not the same as expected "{reset_title}"')

    def test_002_verify_three_horizontal_tabs(self):
        """
        DESCRIPTION: Verify three horizontal tabs
        EXPECTED: - YOUR TEAMS (selected by default)
        EXPECTED: - THE OPPOSITION
        EXPECTED: - SAVED FILTERS
        """
        self.__class__.tabs = self.site.football_bet_filter.tab_menu
        self.assertTrue(self.tabs.items_as_ordered_dict, msg='Can not find any tabs menu')
        self.assertEqual(self.tabs.current, vec.retail.YOUR_TEAMS_TAB,
                         msg=f'Current tab {self.tabs.current} is not equal to expected {vec.retail.YOUR_TEAMS_TAB}')
        for tab in self.expected_bet_filter_tabs:
            self.assertIn(tab, list(self.tabs.items_as_ordered_dict.keys()),
                          msg=f'"{tab}" is not equal to'
                          f'expected "{list(self.tabs.items_as_ordered_dict.keys())}"')

    def test_003_verify_info_section_beneath_your_teams_tab(self):
        """
        DESCRIPTION: Verify info section beneath YOUR TEAMS tab
        EXPECTED: **Coral:**
        EXPECTED: - 'Select criteria for teams you wish to bet on' text and 'i' icon next to it
        EXPECTED: - Tapping 'i' icon expands the text area that says:
        EXPECTED: High Scoring [bold] - Teams ranked in the top half of their division by most goals scored.
        EXPECTED: Mean Defence [bold] - Teams ranked in the top half of their division by fewest goals conceded.
        EXPECTED: Favourite [bold] - Teams priced shorter than their opponents to win their match.
        EXPECTED: Outsider [bold] - Teams priced longer than their opponents to win their match.
        EXPECTED: **Ladbrokes:**
        EXPECTED: - 'Create your search below
        EXPECTED: For online bets only [bold]
        EXPECTED: Use the below filters to find the bet that suits you best. Save your selections so you can quickly browse your runners in the future.' text
        EXPECTED: Select criteria for the teams you wish to bet on' text and 'i' icon next to it
        EXPECTED: - Tapping 'i' icon expands the grey text area that says:
        EXPECTED: High Scoring [bold] - Teams ranked in the top half of their division by most goals scored.
        EXPECTED: Mean Defence [bold] - Teams ranked in the top half of their division by fewest goals conceded.
        EXPECTED: Favourite [bold] - Teams priced shorter than their opponents to win their match.
        EXPECTED: Outsider [bold] - Teams priced longer than their opponents to win their match.
        """
        info_section = self.site.football_bet_filter.info_accordion
        info_text = vec.bet_finder.SELECT_CRITERIA_FOR_TEAMS_TEXT if self.brand != 'ladbrokes' else vec.bet_finder.YOUR_TEAMS_INFO
        self.assertEqual(info_section.info_text, info_text,
                         msg=f'"{info_section.info_text}" info text is not equal to expected '
                             f'"{info_text}"')
        if self.brand == 'bma':
            self.assertTrue(info_section.info_icon.is_displayed(), msg='Can not find Info icon')
            info_section.info_icon.click()
        else:
            self.assertTrue(info_section.show_more.is_displayed(), msg='Show more link is not displayed')
            info_section.show_more.click()

        self.assertEqual(info_section.info_text_details, vec.bet_finder.YOUR_TEAMS_CRITERIA_INFO,
                         msg=f'"{info_section.info_text_details}" '
                             f'is not equal to expected "{vec.bet_finder.YOUR_TEAMS_CRITERIA_INFO}"')

    def test_004_verify_info_section_beneath_the_opposition_tab(self):
        """
        DESCRIPTION: Verify info section beneath THE OPPOSITION tab
        EXPECTED: **Coral:**
        EXPECTED: - 'Select criteria for the teams you wish to bet against' text and 'i' icon next to it
        EXPECTED: - Tapping 'i' icon expands the text area that says:
        EXPECTED: High Scoring [bold] - Teams ranked in the top half of their division by most goals scored.
        EXPECTED: Leaky Defence [bold] - Teams ranked in the bottom half of their division by fewest goals conceded.
        EXPECTED: **Ladbrokes:**
        EXPECTED: - 'Create your search below
        EXPECTED: For online bets only [bold]
        EXPECTED: Use the below filters to find the bet that suits you best. Save your selections so you can quickly browse your runners in the future.' text
        EXPECTED: Select criteria for the teams you wish to bet against' text and 'i' icon next to it
        EXPECTED: - Tapping 'i' icon expands the grey text area that says:
        EXPECTED: High Scoring [bold] - Teams ranked in the top half of their division by most goals scored.
        EXPECTED: Leaky Defence [bold] - Teams ranked in the bottom half of their division by fewest goals conceded.
        """
        self.tabs.open_tab(tab_name=vec.retail.THE_OPPOSITION_TAB)
        self.__class__.tabs = self.site.football_bet_filter.tab_menu
        self.assertTrue(self.tabs.items_as_ordered_dict, msg='Can not find any tabs menu')
        self.assertEqual(self.tabs.current, vec.retail.THE_OPPOSITION_TAB,
                         msg=f'Default selected tab is "{self.tabs.current}" but expected "{vec.retail.THE_OPPOSITION_TAB}"')

        info_section = self.site.football_bet_filter.info_accordion
        info_text = vec.bet_finder.SELECT_CRITERIA_FOR_OPPOSITION_TEXT if self.brand != 'ladbrokes' else vec.bet_finder.THE_OPPOSITION_INFO
        self.assertEqual(info_section.info_text, info_text,
                         msg=f'"{info_section.info_text}" info text is not equal to expected '
                             f'"{info_text}"')
        if self.brand == 'bma':
            self.assertTrue(info_section.info_icon.is_displayed(), msg='Can not find Info icon')
        else:
            self.assertTrue(info_section.show_less.is_displayed(), msg='Show less link is not displayed')
        self.assertEqual(info_section.info_text_details, vec.bet_finder.THE_OPPOSITION_CRITERIA_INFO,
                         msg=f'"{info_section.info_text_details}" '
                             f'is not equal to expected "{vec.bet_finder.THE_OPPOSITION_CRITERIA_INFO}"')

    def test_005_verify_your_teams_tab_filters(self):
        """
        DESCRIPTION: Verify YOUR TEAMS tab filters
        EXPECTED: Tab contains:
        EXPECTED: PLAYING AT filter with following options:
        EXPECTED: * HOME
        EXPECTED: * AWAY
        EXPECTED: LAST GAME filter with following options:
        EXPECTED: * WIN
        EXPECTED: * DRAW
        EXPECTED: * LOSE
        EXPECTED: LAST 6 GAMES POINT TOTAL filter with following options:
        EXPECTED: * 0-6 POINTS
        EXPECTED: * 7-12 POINTS
        EXPECTED: * 13-18 POINTS
        EXPECTED: KEY TRENDS filter with following options:
        EXPECTED: * HIGH SCORING
        EXPECTED: * MEAN DEFENCE
        EXPECTED: * CLEAN SHEET LAST GAME
        EXPECTED: LEAGUE POSITIONS filter with following options:
        EXPECTED: * TOP HALF
        EXPECTED: * BOTTOM HALF
        EXPECTED: * ABOVE OPPOSITION
        EXPECTED: ODDS filter with following options:
        EXPECTED: * FAVOURITE
        EXPECTED: * OUTSIDER
        """
        self.tabs.open_tab(tab_name=vec.retail.YOUR_TEAMS_TAB)
        selections = self.site.football_bet_filter.tab_content.items_as_ordered_dict
        self.assertTrue(selections, msg='Can not find any selection')
        categories = []
        for key, value in selections.items():
            categories.append(key)
            [categories.append(k) for k, v in value.items_as_ordered_dict.items()]
        self.assertListEqual(categories, vec.bet_finder.EXPECTED_EXPECTED_LIST_OF_YOUR_TEAMS_CATEGORIES,
                             msg=f'"{categories}" is not equal '
                             f'to expected "{vec.bet_finder.EXPECTED_EXPECTED_LIST_OF_YOUR_TEAMS_CATEGORIES}"')

    def test_006_verify_the_opposition_tab_filters(self):
        """
        DESCRIPTION: Verify THE OPPOSITION tab filters
        EXPECTED: Tab contains:
        EXPECTED: LAST GAME filter with following options:
        EXPECTED: * WIN
        EXPECTED: * DRAW
        EXPECTED: * LOSE
        EXPECTED: LAST 6 GAMES POINT TOTAL filter with following options:
        EXPECTED: * 0-6 POINTS
        EXPECTED: * 7-12 POINTS
        EXPECTED: * 13-18 POINTS
        EXPECTED: KEY TRENDS filter with following options:
        EXPECTED: * HIGH SCORING
        EXPECTED: * LEAKY DEFENCE
        EXPECTED: * CONCEDED 2+ LAST GAME
        EXPECTED: LEAGUE POSITIONS filter with following options:
        EXPECTED: * TOP HALF
        EXPECTED: * BOTTOM HALF
        EXPECTED: * ABOVE OPPOSITION
        """
        self.tabs.open_tab(tab_name=vec.retail.THE_OPPOSITION_TAB)
        selections = self.site.football_bet_filter.tab_content.items_as_ordered_dict
        self.assertTrue(selections, msg='Can not find any selection')
        categories = []
        for key, value in selections.items():
            categories.append(key)
            [categories.append(k) for k, v in value.items_as_ordered_dict.items()]
        self.assertListEqual(categories, vec.bet_finder.EXPECTED_LIST_OF_OPPOSITION_CATEGORIES,
                             msg=f'"{categories}" is not equal '
                             f'to expected "{vec.bet_finder.EXPECTED_LIST_OF_OPPOSITION_CATEGORIES}"')

    def test_007_verify_find_bets_x_button(self):
        """
        DESCRIPTION: Verify 'FIND BETS (X)' button
        EXPECTED: - Green button, enabled by default
        EXPECTED: - X - value that shows how many selections are available and changes after filtering applied
        EXPECTED: - The footer panel is sticky and always visible to a user
        """
        self.assertFalse(self.site.football_bet_filter.find_bets_button.has_spinner_icon(expected_result=False, timeout=5),
                         msg='Spinner has not disappeared from Find Bets button')
        self.assertTrue(self.site.football_bet_filter.find_bets_button.is_enabled(), msg='Find Bets button is disabled')
        self.verify_number_of_bets(expected_number_of_bets=len(self.get_all_selections(coupon_name=self.coupon_name)))
        self.site.football_bet_filter.save_filters_button.is_enabled(expected_result=False)

    def test_008_add_many_filters_so_that_no_selections_are_found(self):
        """
        DESCRIPTION: Add many filters, so that no selections are found
        EXPECTED: - "FIND BETS" gets disabled (pale gray according to coral design)
        EXPECTED: - "FIND BETS (0)" button. (X) gets '0' value
        """
        self.tabs.open_tab(tab_name=vec.retail.YOUR_TEAMS_TAB)
        selections = self.site.football_bet_filter.tab_content.items_as_ordered_dict
        self.assertTrue(selections, msg='Can not find any selection')

        self.change_state_of_selection(category_name=vec.bet_finder.FB_BET_FILTER_LAST_GAME_TEXT,
                                       selection_name=vec.bet_finder.FB_BET_FILTER_LOSE)

        self.change_state_of_selection(category_name=vec.bet_finder.FB_BET_FILTER_KEY_TRENDS_TEXT,
                                       selection_name=vec.bet_finder.FB_BET_FILTER_CLEAN_SHEET_LAST_GAME)
        self.verify_number_of_bets(expected_number_of_bets=0)

    def test_009_check_save_filters_button(self):
        """
        DESCRIPTION: Check SAVE FILTERS button
        EXPECTED: The button is unavailable until at least one filter is selected
        """
        # disabled state verified on step 7
        self.site.football_bet_filter.save_filters_button.is_enabled()
        refresh_button = self.site.football_bet_filter.sub_header.refresh_button
        refresh_button.click()

        selections = self.site.football_bet_filter.tab_content.items_as_ordered_dict
        self.assertTrue(selections, msg='Can not find any selection')

        category_name = selections.get(vec.bet_finder.FB_BET_FILTER_LAST_GAME_TEXT)
        selection_names = category_name.items_as_ordered_dict
        selection = selection_names.get(vec.bet_finder.FB_BET_FILTER_LOSE)
        self.assertFalse(selection.is_selected(), f'Still Selected after Clicking on RESET')

        category_name = selections.get(vec.bet_finder.FB_BET_FILTER_KEY_TRENDS_TEXT)
        selection_names = category_name.items_as_ordered_dict
        selection = selection_names.get(vec.bet_finder.FB_BET_FILTER_CLEAN_SHEET_LAST_GAME)
        self.assertFalse(selection.is_selected(), f'Still Selected after Clicking on RESET')

