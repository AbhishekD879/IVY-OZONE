import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_013_Retail_Connect_Features.Football_Bet_Filter.BaseFootballBetFilter import BaseFootballBetFilter
from voltron.utils.exceptions.cms_client_exception import CmsClientException


# @pytest.mark.tst2  # football filter has endpoints just for prod
# @pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.lad_beta2
@pytest.mark.bet_filter
@pytest.mark.football_bet_filter
@pytest.mark.retail
@pytest.mark.connect
@pytest.mark.medium
@pytest.mark.desktop
@vtest
class Test_C2161236_Verify_filtering_on_both_YOUR_TEAMS_and_THE_OPPOSITION_tabs(BaseFootballBetFilter):
    """
    TR_ID: C2161236
    NAME: Verify filtering on both YOUR TEAMS and THE OPPOSITION tabs
    DESCRIPTION: This test case verifies filtering from a few tabs simultaneously
    PRECONDITIONS: **Coral:**
    PRECONDITIONS: 1. Load SportBook
    PRECONDITIONS: 2. Select 'Connect' from header ribbon
    PRECONDITIONS: 3. Select 'Football Bet Filter' item
    PRECONDITIONS: **Ladbrokes:**
    PRECONDITIONS: Load SportBook > Go to Football > 'Coupons' tab > Select any coupon that contains events with 'Match result' market (In Console: search 'coupon' - find coupons with couponSortCode: "MR">)
    """
    keep_browser_open = True
    filters = {
        vec.retail.YOUR_TEAMS_TAB: ((vec.bet_finder.FB_BET_FILTER_KEY_TRENDS_TEXT, vec.bet_finder.FB_BET_FILTER_HIGH_SCORING),
                                    (vec.bet_finder.FB_BET_FILTER_KEY_TRENDS_TEXT, vec.bet_finder.FB_BET_FILTER_CLEAN_SHEET_LAST_GAME)),
        vec.retail.THE_OPPOSITION_TAB: ((vec.bet_finder.FB_BET_FILTER_LAST_GAME, vec.bet_finder.FB_BET_FILTER_OPPOSITION_LOSE),
                                        (vec.bet_finder.FB_BET_FILTER_OPPOSITION_KEY_TRENDS_TEXT, vec.bet_finder.FB_BET_FILTER_OPPOSITION_LEAKY_DEFENCE))
    }

    def test_001_verify_filters_default_value(self):
        """
        DESCRIPTION: Verify filters default value
        EXPECTED: None of the filters is selected
        """
        cms_config = self.get_initial_data_system_configuration().get('Connect', {})
        if not cms_config:
            cms_config = self.cms_config.get_system_configuration_item('Connect')
        if not cms_config.get('footballFilter'):
            raise CmsClientException('"Football Bet Filter" is disabled')
        self.__class__.coupon_name = self.open_bet_filter_via_coupon()
        self.__class__.bet_filter = self.site.football_bet_filter
        for tab in self.filters.keys():
            result = self.bet_filter.tab_menu.open_tab(tab)
            self.assertTrue(result, msg=f'"{tab}" is not active')
            filter_sections = self.site.football_bet_filter.tab_content.items_as_ordered_dict
            self.assertTrue(filter_sections, msg='Can not find any sections')
            for section_name, section in filter_sections.items():
                section_filters = section.items_as_ordered_dict
                self.assertTrue(section_filters, msg=f'There are no any filters under "{section_name}" section')
                for filter_name, filter_ in section_filters.items():
                    self.assertFalse(filter_.is_selected(expected_result=False),
                                     msg=f'"{tab}" tab: "{filter_name}" filter is selected')

    def test_002_check_off_a_few_random_filters_from_your_teams_and_the_opposition_tab(self):
        """
        DESCRIPTION: Check off a few random filters from YOUR TEAMS and THE OPPOSITION tab
        EXPECTED: The filters are checked off
        """
        for tab in self.filters.keys():
            result = self.bet_filter.tab_menu.open_tab(tab)
            self.assertTrue(result, msg=f'"{tab}" is not active')
            filter_sections = self.site.football_bet_filter.tab_content.items_as_ordered_dict
            self.assertTrue(filter_sections, msg='Can not find any sections')
            for section, fb_filter in self.filters[tab]:
                self.assertIn(section, filter_sections, msg=f'"{section}" filter section is not shown')
                section = filter_sections.get(section)
                filters = section.items_as_ordered_dict
                self.assertIn(fb_filter, filters, msg=f'"{fb_filter}" filter is not shown under "{section}" section')
                filter_ = filters.get(fb_filter)
                filter_.click()

    def test_003_switch_over_tabs(self):
        """
        DESCRIPTION: Switch over tabs
        EXPECTED: The ticks are present on pages during switching over tabs
        """
        for tab in self.filters.keys():
            result = self.bet_filter.tab_menu.open_tab(tab)
            self.assertTrue(result, msg=f'"{tab}" is not active')
            filter_sections = self.site.football_bet_filter.tab_content.items_as_ordered_dict
            self.assertTrue(filter_sections, msg='Can not find any sections')
            for section, fb_filter in self.filters[tab]:
                self.assertIn(section, filter_sections, msg=f'"{section}" filter section is not shown')
                section = filter_sections.get(section)
                filters = section.items_as_ordered_dict
                self.assertIn(fb_filter, filters, msg=f'"{fb_filter}" filter is not shown under "{section}" section')
                filter_ = filters.get(fb_filter)
                self.assertTrue(filter_.is_selected(), msg=f'"{tab}" tab: "{fb_filter}" filter is not selected')

    def test_004_check_details_on_find_bets_cta(self):
        """
        DESCRIPTION: Check details on 'Find Bets' CTA
        EXPECTED: 1. Results should show data from API CALL params according to the selected filters
        EXPECTED: 2. Verify the proper ResultCount at 'Find Bets' button. Button should read "{count#} SELECTIONS" (beneath its label)
        """
        self.__class__.expected_selections = \
            self.get_selections(coupon_name=self.coupon_name,
                                filters=[vec.bet_finder.FB_BET_FILTER_HIGH_SCORING.lower(),
                                         vec.bet_finder.FB_BET_FILTER_CLEAN_SHEET_LAST_GAME.lower()],
                                opposition_filters=[vec.bet_finder.FB_BET_FILTER_OPPOSITION_LEAKY_DEFENCE.lower()],
                                opp_last_game=vec.bet_finder.FB_BET_FILTER_OPPOSITION_LOSE.lower())
        self.verify_number_of_bets(expected_number_of_bets=len(self.expected_selections))

    def test_005_tap_find_bets(self):
        """
        DESCRIPTION: Tap 'Find Bets'
        EXPECTED: 1. Football Filter Results page is opened
        EXPECTED: 2. Results number is correct
        EXPECTED: 3. List of selections is correct and corresponds to filters applied on both tabs
        """
        if self.site.football_bet_filter.find_bets_button.is_enabled():
            self.site.football_bet_filter.find_bets_button.click()
            self.site.wait_content_state(state_name='FootballBetFilterResultsPage')
            bet_filter_results_page = self.site.football_bet_filter_results_page
            self.assertEqual(bet_filter_results_page.number_of_results, len(self.expected_selections),
                             msg=f'Results number "{bet_filter_results_page.number_of_results}" is not the same '
                                 f'as expected "{len(self.expected_selections)}"')
            expected_selection_names = [selection['selectionName'] for selection in self.expected_selections]
            bet_filter_results = [result.name.split(' @')[0] for result in bet_filter_results_page.items]
            self.assertListEqual(sorted(bet_filter_results), sorted(expected_selection_names),
                                 msg=f'List of selections: \n"{sorted(bet_filter_results)}" \nis not the same as '
                                     f'expected \n"{sorted(expected_selection_names)}"')
        else:
            self._logger.info('There is no bets that fits selected filter')
