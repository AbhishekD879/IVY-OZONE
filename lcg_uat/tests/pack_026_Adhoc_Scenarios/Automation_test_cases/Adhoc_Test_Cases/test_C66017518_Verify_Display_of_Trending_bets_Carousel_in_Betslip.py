
import pytest

import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
import voltron.environments.constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.mobile_only
@pytest.mark.trending_bets
@pytest.mark.adhoc_suite
@pytest.mark.adhoc24thJan24
@pytest.mark.navigation
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C66017518_Verify_Display_of_Trending_bets_Carousel_in_Betslip(BaseBetSlipTest):
    """
    TR_ID: C66017518
    NAME: Verify Display of Trending bets Carousel in Betslip
    DESCRIPTION: This test case verifies the Display of Trending bets Carousel in Betslip
    PRECONDITIONS: "1. Trending Bets Carousel is configured in the CMS
    PRECONDITIONS: 2. Navigation to CMS -&gt; Most Popular/Trending Bets -&gt; Bet slip -&gt; Enable -&gt; Bet receipt -&gt; Enable for Bet receipt -&gt; Enable for Quick Bet receipt"
    """
    keep_browser_open = True
    device_name = 'iPhone 6 Plus' if not tests.use_browser_stack else tests.mobile_safari_default
    selection_ids = []

    def test_000_preconditions(self):
        """
        DESCRIPTION: Login to Oxygen app
        DESCRIPTION: Find / create event for test
        EXPECTED: User is logged in
        EXPECTED: Event is found / created
        """
        ###### verify Trending bet carousel in bet slip is enable or not in CMS ##################
        trending_carousel_betslip = self.cms_config.get_most_popular_or_trending_bets_bet_slip_config().get('active')
        if not trending_carousel_betslip:
            self.cms_config.update_most_popular_or_trending_bets_bet_slip_config(active=True)

        events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                     number_of_events=3)
        race_event = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                            number_of_events=1)
        # selections from football
        for event in events:
            match_result_market = next((market['market'] for market in event['event']['children'] if
                                        market.get('market').get('templateMarketName') == 'Match Betting'), None)
            outcomes = match_result_market['children']
            all_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            selection_id = list(all_selection_ids.values())[0]
            self.selection_ids.append(selection_id)
        # selection from race
        for event in race_event:
            match_result_market = next((market['market'] for market in event['event']['children'] if
                                        market.get('market').get('templateMarketName') == 'Win or Each Way'), None)
            outcomes = match_result_market['children']
            all_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            self.__class__.race_selection_id = list(all_selection_ids.values())[0]
            self.__class__.race_name = list(all_selection_ids.keys())[0]

    def test_001_launch_the_application(self):
        """
        DESCRIPTION: Launch the Application
        EXPECTED: User should launch the application Successfully
        """
        self.site.login()

    def test_002_click_on_the_football_sport(self):
        """
        DESCRIPTION: Click on the Football Sport
        EXPECTED: Able to navigate to the Football landing page
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('football')

    def test_003_click_on_any_single_selection_and_click_on_add_to_betslip(self):
        """
        DESCRIPTION: Click on any Single Selection and Click on Add to Betslip
        EXPECTED: Single Selection is added to Betslip Successfully
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids[0])

    def test_004_navigate_to_betslip_and_check_trending_bets_carousel(self):
        """
        DESCRIPTION: Navigate to Betslip and Check Trending Bets carousel
        EXPECTED: Able to navigate to the Betslip and should see the Trending Bets carousel
        """
        self.assertTrue(self.site.betslip.has_trending_bet_carousel(),
                        msg=f'Trending Bets Carousel section is not available')

    def test_005_check_number_of_trending_bets_display_in_the_betslip(self):
        """
        DESCRIPTION: Check number of trending bets display in the Betslip
        EXPECTED: Top five trending bets should display in the Betslip
        """
        cms_trending_carousel_count = self.cms_config.get_most_popular_or_trending_bets_bet_slip_config().get('maxSelections')
        self.__class__.trending_bet = list(self.site.betslip.trending_bets_section.items_as_ordered_dict.values())
        self.assertEqual(cms_trending_carousel_count, len(self.trending_bet),
                         msg = f'actual trending carousel count from CMS: {cms_trending_carousel_count} is not equal to FE trending carousel count: {len(self.trending_bet)}')

    def test_006_click_and_add_any_trending_bet_selection_from_the_trending_bets_carousel(self):
        """
        DESCRIPTION: Click and add any trending bet selection from the Trending Bets carousel
        EXPECTED: User should able to add the trending bet selection to the bet slip
        """
        self.trending_bet[-1].scroll_to()
        self.__class__.trending_bet_event_name = self.trending_bet[-1].name
        self.trending_bet[-1].odd.click()

    def test_007_check_number_of_trending_bets_display_in_the_betslip(self):
        """
        DESCRIPTION: Check number of trending bets display in the Betslip
        EXPECTED: Now the next Five trending bets should display in the Betslip
        """
        adding_trending_bet_carousel = list(self.site.betslip.trending_bets_section.items_as_ordered_dict.values())
        after_trending_bet_carousel = []
        for i in range(0,len(adding_trending_bet_carousel)):
            after_trending_bet_carousel.append(adding_trending_bet_carousel[i].name)

        self.assertNotIn(self.trending_bet_event_name,after_trending_bet_carousel,
                         msg = f'After clicking this trending caurosel is :{self.trending_bet_event_name} is still showing in trending caurosel list {after_trending_bet_carousel}')

        cms_after_adding_trending_bet_caurosel = self.cms_config.get_most_popular_or_trending_bets_bet_slip_config().get('maxSelections')
        self.assertEqual(cms_after_adding_trending_bet_caurosel, len(after_trending_bet_carousel),
                         msg=f'actual trending carousel count from CMS: {cms_after_adding_trending_bet_caurosel} is not eequal to FE trending carousel count: {len(after_trending_bet_carousel)}')
        self.site.betslip.remove_all_button.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_REMOVE_ALL,timeout=30)
        dialog.continue_button.click()

    def test_008_add_more_than_two_selections_from_football_and_click_on_add_to_betslip(self):
        """
        DESCRIPTION: Add more than two Selections from football and Click on Add to Betslip
        EXPECTED: Added Selections were added to Betslip Successfully
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_ids,timeout=10)

    def test_009_navigate_to_betslip(self):
        """
        DESCRIPTION: Navigate to Betslip
        EXPECTED: Able to navigate to the Betslip and should see the Singles and Multiple Bets
        """
        # Covered in above step

    def test_010_check_trending_bets_carousel_in_betslip(self):
        """
        DESCRIPTION: Check Trending Bets carousel in Betslip
        EXPECTED: Trending Bets carousel should not display in Betslip
        """
        self.assertFalse(self.site.betslip.has_trending_bet_carousel(expected_result=False),
                         msg=f'Trending bet carousel still display in betslip')

    def test_011_add_any_selection_to_the_betslip_other_than_football_sport_and_navigate_to__betslip_page(self):
        """
        DESCRIPTION: Add any selection to the betslip other than football sport and Navigate to  Betslip Page
        EXPECTED: Able to add the selection to the bet slip and navigates to Betslip Page
        """
        # already covered to C665972741

    def test_012_check_trending_bets_carousel(self):
        """
        DESCRIPTION: Check Trending Bets carousel
        EXPECTED: Trending Bets carousel should not display
        """
        # already covered to C665972741

    def test_013_add_multiple_selections_from_multiple_sports_to_the_betslip_and_navigate_to__betslip_page(self):
        """
        DESCRIPTION: Add Multiple selections from Multiple sports to the betslip and Navigate to  Betslip Page
        EXPECTED: Able to add multiple selections to the betslip and navigates to Betslip Page
        """
        # already covered to C665972741

    def test_014_check_trending_bets_carousel_in_betslip(self):
        """
        DESCRIPTION: Check Trending Bets carousel in Betslip
        EXPECTED: Trending Bets carousel should not display in Betslip
        """
        # already covered to C665972741

    def test_015_add_one_selection_from_football_and_one_selection_from_races_or_any_other_sport_to_the_betslip_and_navigate_to__betslip_page(self):
        """
        DESCRIPTION: Add one selection from Football and one selection from Races or any other sport to the betslip and Navigate to  Betslip Page
        EXPECTED: Able to add multiple selections to the betslip and navigates to Betslip Page
        """
        # clear betslip
        self.site.betslip.remove_all_button.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_REMOVE_ALL,timeout=30)
        dialog.continue_button.click()
        # adding race selection and football selection in bet slip
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=(self.selection_ids[0], self.race_selection_id),timeout=10)

    def test_016_check_trending_bets_carousel_in_betslip(self):
        """
        DESCRIPTION: Check Trending Bets carousel in Betslip
        EXPECTED: Trending Bets carousel should not display in Betslip
        """
        self.assertFalse(self.site.betslip.has_trending_bet_carousel(expected_result=False),
                         msg=f'Trending bet carousel still display in betslip')

    def test_017_remove_the_races_or_any_other_sport_selection_from_the_betslip_and_verify_the_trending_bets_carousel(self):
        """
        DESCRIPTION: Remove the Races or any other sport selection from the betslip and verify the trending bets carousel
        EXPECTED: Able to remove the selection and can see the trending bets carousel
        """
        # removing race selection from bet slip
        singles_section = self.get_betslip_sections().Singles
        self.assertIn(self.race_name, singles_section,
                      msg=f'Horse name "{self.race_name}" is not present in "{singles_section.keys()}"')
        race_selection = singles_section[self.race_name]
        self.assertTrue(race_selection.remove_button.is_displayed(), msg='remove button is not display')
        race_selection.remove_button.click()

        # after removing race event trending bet carousel will display

        self.assertTrue(self.site.betslip.has_trending_bet_carousel(expected_result=True),
                         msg=f'betslip has trending_bet carousel which should not be available')

    def test_018_add_any_selection_from_virtuals_to_the_betslip_and_navigate_to_betslip_page(self):
        """
        DESCRIPTION: Add any selection from virtuals to the betslip and navigate to Betslip Page
        EXPECTED: Able to add Virtuals bets and navigates to Betslip Page
        """
        # already covered to C665972741

    def test_019_check_trending_bets_carousel_in_betslip(self):
        """
        DESCRIPTION: Check Trending Bets carousel in Betslip
        EXPECTED: Trending Bets carousel should not display in Betslip
        """
        # already covered to C665972741
