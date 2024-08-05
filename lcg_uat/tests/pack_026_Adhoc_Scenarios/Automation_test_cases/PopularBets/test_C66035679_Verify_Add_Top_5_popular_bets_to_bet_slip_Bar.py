import pytest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.base_test import vtest
import voltron.environments.constants as vec

@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.popular_bets
@pytest.mark.reg167_fix
@pytest.mark.reg_170_fix
@pytest.mark.adhoc_suite
@pytest.mark.football
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C66035679_Verify_Add_Top_5_popular_bets_to_bet_slip_Bar(BaseBetSlipTest):
    """
    TR_ID: C66035679
    NAME: Verify "Add Top 5 popular bets to bet slip" Bar
    DESCRIPTION: This test case verifies the "Add Top 5 popular bets to bet slip" Bar
    PRECONDITIONS: Configure Popular bets tab in CMS (CMS>Sports pages>Popular bets)
    """
    keep_browser_open = True
    Popular_bets = vec.sb.TABS_NAME_POPULAR_BETS
    _accumulator = None

    def get_sport_tab_status(self, tab):
        """
        Check the status of a sport tab.
        Args:
            tab (dict): The tab information.
        Returns:
            bool: True if the tab is enabled and has events; False otherwise.
        Raises:
            ValueError: If check_events or has_events parameters are missing in the tab.
        """
        check_events = tab.get("checkEvents")
        has_events = tab.get("hasEvents")
        enabled = tab.get("enabled")
        if not enabled:
            return False
        if check_events is None or has_events is None:
            raise ValueError(
                f"check_events: {check_events} and has_events: {has_events} are missing in the tab parameters.")
        if check_events and not has_events:
            return False
        return True

    def test_000_preconditions(self):
        """
        TR_ID: C66035679
        NAME: Verify "Add Top 5 popular bets to bet slip" Bar
        DESCRIPTION: This test case verifies the "Add Top 5 popular bets to bet slip" Bar
        PRECONDITIONS: Configure Popular bets tab in CMS (CMS>Sports pages>Popular bets)
        """
        all_sub_tabs_for_football = self.cms_config.get_sport_tabs(sport_id=16)
        popular_bets_tab = next(
            (tab for tab in all_sub_tabs_for_football if tab.get("name") == "popularbets"),
            None)
        self.assertTrue(popular_bets_tab, msg="Popular bets tab not found")
        popular_bets_tab_status = self.get_sport_tab_status(popular_bets_tab)
        self.assertTrue(popular_bets_tab_status, msg="Popular bets tab does not have event")
        self.__class__.tab_name, self.__class__.popular_bets_tab_name = next(
            ([popular_bets_tab['displayName'].upper(), sub_tab['trendingTabName'].upper()]
             for sub_tab in popular_bets_tab['trendingTabs'] for inner_sub_tab in sub_tab['popularTabs']
             if inner_sub_tab['popularTabName'] == 'Popular_tab' and inner_sub_tab['enabled'] and sub_tab['enabled']),None)
        self.assertTrue(self.popular_bets_tab_name, msg=f'popular bets sub tab was not configured in cms')

    def test_001_launch_the_application(self):
        """
        DESCRIPTION: Launch the Application
        EXPECTED: Application is launched Successfully
        """
        # Log in to the site
        self.site.login()
        # Wait for the content state to be "HOMEPAGE"
        self.site.wait_content_state("HOMEPAGE")

    def test_002_click_on_the_football_sport(self):
        """
        DESCRIPTION: Click on the Football Sport
        EXPECTED: Able to navigate to the Football landing page
        """
        # Open the sports section for football
        self.site.open_sport("football")
        # Wait for the content state to be "football" (assuming this is a specific state related to football content)
        self.site.wait_content_state("football")

    def test_003_verify_the_display_of_popular_bets_section(self):
        """
        DESCRIPTION: Verify the display of Popular Bets section
        EXPECTED: User can able to see the Popular Bets section
        """
        # Get the tabs available on the Football page as an ordered dictionary
        tabs = self.site.football.tabs_menu.items_as_ordered_dict

        # Check if any tabs are found on the Football page
        self.assertTrue(tabs, msg='No tabs found on Football page')

    def test_004_click_on_popular_bets_section(self):
        """
        DESCRIPTION: Click on Popular Bets section
        EXPECTED: Able to navigate to the Popular Bets section successfully
        """
        # Click on the button associated with the specified tab name
        result = self.site.football.tabs_menu.click_button(button_name=self.tab_name, timeout=10)

        # Check if the tab is successfully opened
        self.assertTrue(result, msg=f'"{result}" tab is not opened')
        current_tab = self.site.football.tab_content.grouping_buttons.current
        if current_tab != self.popular_bets_tab_name.upper():
            self.site.football.tab_content.grouping_buttons.click_button(button_name=self.popular_bets_tab_name.upper(), timeout=5)

    def test_005_verify_the_display_of_add_top_5_most_backed_bets_to_betslip_bar(self):
        """
        DESCRIPTION: Verify the Display of "Add Top 5 Most backed bets to betslip" Bar
        EXPECTED: User should be displayed with "Add Top 5 Most backed bets to betslip" Bar right under 5th Popular bet and above the 6th popular bet
        """
        # Check if the top five backed card is present
        top_five_backed_card = self.site.football.tab_content.accordions_list.has_add_to_betslip_bar()
        self.assertTrue(top_five_backed_card, "TopFiveBackedCard not found")

        # Find the add to betslip button
        add_to_betslip_button = self.site.football.tab_content.accordions_list.add_to_betslip_button
        self.assertTrue(add_to_betslip_button, "Add to betslip button not found")

        self.__class__.payout_text = self.site.football.tab_content.accordions_list.payout_desc

        self.assertTrue(self.payout_text, f'unable to find payout text on page.')

        # Click on the add to betslip button
        add_to_betslip_button.click()

    def test_006_verify_add_top_5_most_backed_bets_to_betslip_bar_under_popular_bets(self):
        """
        DESCRIPTION: Verify Add Top 5 Most backed bets to betslip Bar under popular bets
        EXPECTED: User can able to see Add Top 5 Most backed bets to betslip Bar and the Add to bet slip CTA button in it.
        """
        # Covered in above step

    def test_007_click_on_add_to_bet_slip_cta_button(self):
        """
        DESCRIPTION: Click on Add to bet slip CTA button
        EXPECTED: all the top 5 popular bets selections odds should be in selected mode in green color and added to betslip successfully.
        """
        # Covered in above step

    def test_008_verify_the_display_pay_out_in_add_to_top5_bar(self):
        """
        DESCRIPTION: Verify the Display Pay out in Add to Top5 Bar
        EXPECTED: 1. User should be displayed with the Payout if all the top5 bets in the popular bets list make a 5 fold ACCA
        EXPECTED: 2. User should be displayed with the Payout as NA, if the top 5 popular bets doesn't make a 5 fold ACCA
        EXPECTED: 3. User should be displayed with the Payout as NA if any bet is suspended from the top 5 popular bets which are added to the top4 betslip bar
        """
        self.site.open_betslip()
        self.assertTrue(self.site.has_betslip_opened(), msg='Failed to open Betslip')

        # Get the betslip sections
        betslip_sections = self.get_betslip_sections(multiples=True)

        if betslip_sections.Multiples and betslip_sections.Multiples.get(vec.betslip.ACC5):
            self.assertNotEqual(self.payout_text, "N/A", msg="Payout text not found ")
            pattern = r'[£$€]\d+ pays [£$€]\d+'
            self.assertRegex(self.payout_text.lower(), pattern,
                             msg=f'Incorrect payout text format. Actual Text : "{self.payout_text}" is not matches with regular expression : "{pattern}"')
        else:
            self.assertEqual(self.payout_text, "N/A", msg="Payout text not found ")

    def test_009_verify_the_payout_text(self):
        """
        DESCRIPTION: Verify the Payout text
        EXPECTED: Payout text should be displayed "&Atilde;&sbquo;&Acirc;&pound;10 Pays &Atilde;&sbquo;&Acirc;&pound;100"
        """
        # covered in above step
