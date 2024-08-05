import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from time import sleep


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # can't grant free bet on prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.betslip
@vtest
class Test_C15950379_From_OX_99_Verify_Free_Bet_Tooltip_in_Betslip(BaseBetSlipTest):
    """
    TR_ID: C15950379
    NAME: [From OX 99] Verify Free Bet Tooltip in Betslip
    DESCRIPTION: This test case verifies Free Bets tooltip in the Betslip
    DESCRIPTION: **FROM OX105 (BMA-52025) - tooltip is shown only once - steps should be updated**
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * User has Free Bets available on their account
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create an event
        EXPECTED: Event is created
        """
        event1 = self.ob_config.add_volleyball_event_to_austrian_league()
        self.__class__.selection_id1 = list(event1.selection_ids.values())[0]
        self.__class__.selection_id2 = list(event1.selection_ids.values())[1]
        self.__class__.selection_ids = event1.selection_ids
        self.__class__.team1 = event1.team1
        self.__class__.team2 = event1.team2

        event2 = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.selection_ids = event2.selection_ids
        self.__class__.team3 = event2.team1
        self.__class__.team4 = event2.team2
        self.__class__.username = tests.settings.betplacement_user
        self.ob_config.grant_freebet(self.username)
        self.site.login(username=self.username)

    def test_001_add_selection_to_the_betslip_and_open_betslip(self):
        """
        DESCRIPTION: Add selection to the Betslip and open Betslip
        EXPECTED: Betslip is open
        EXPECTED: Free Bet Tooltip is shown
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id1)
        sleep(3)
        selections = self.get_betslip_sections().Singles
        self.__class__.selection = selections.get(self.team1, None)
        self.assertTrue(self.selection.has_freebet_tooltip(), msg='"Use Free Bet" link not found')

    def test_002_tap_on_any_part_of_the_betslip(self):
        """
        DESCRIPTION: Tap on any part of the Betslip
        EXPECTED: * Free Bet Tooltip is closed
        EXPECTED: * *OX.freeBetTooltipSeen-username* key (Local Storage) is set as true
        """
        self.selection.freebet_tooltip.click()
        sleep(3)
        self.assertFalse(self.selection.has_freebet_tooltip(), msg='"Use Free Bet" link found')
        cookie_name = 'OX.freeBetTooltipSeenBetslip-'
        self.__class__.cookie_name = cookie_name + (self.username)

        cookie = self.get_local_storage_cookie_value_as_dict(cookie_name=self.cookie_name)
        self.assertTrue(cookie, msg="OX.freeBetTooltipSeen-username* key (Local Storage) is not set as true")

    def test_003_add_more_selections_to_the_betslip_and_open_it(self):
        """
        DESCRIPTION: Add more selections to the Betslip and open it
        EXPECTED: Free Bet Tooltip is NOT shown
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id2)
        sleep(3)
        selections = self.get_betslip_sections().Singles
        selection = selections.get(self.team2, None)
        self.assertFalse(selection.has_freebet_tooltip(), msg='"Use Free Bet" link not found')

    def test_004_remove_all_selections_and_add_a_new_ones(self):
        """
        DESCRIPTION: Remove all selections and add a new one(s)
        EXPECTED: Free Bet Tooltip is NOT shown
        """
        self.clear_betslip()
        self.open_betslip_with_selections(selection_ids=self.selection_id1)
        sleep(3)
        selections = self.get_betslip_sections().Singles
        selection = selections.get(self.team1, None)
        self.assertFalse(selection.has_freebet_tooltip(), msg='"Use Free Bet" link not found')

    def test_005_remove_all_selections_from_the_betslipremove_oxfreebettooltipseen_username_keyadd_selection_to_the_betslip_and_open_betslip(self):
        """
        DESCRIPTION: Remove all selections from the Betslip
        DESCRIPTION: Remove *OX.freeBetTooltipSeen-username* key
        DESCRIPTION: Add selection to the Betslip and open Betslip
        EXPECTED: Betslip is open
        EXPECTED: Free Bet Tooltip is shown
        """
        self.clear_betslip()
        self.set_local_storage_cookie_value(cookie_name=self.cookie_name, value=False)
        self.open_betslip_with_selections(selection_ids=self.selection_id1)
        sleep(3)
        selections = self.get_betslip_sections().Singles
        self.__class__.selection = selections.get(self.team1, None)
        self.assertTrue(self.selection.has_freebet_tooltip(), msg='"Use Free Bet" link not found')

    def test_006_tap_on_any_part_of_the_betslip(self):
        """
        DESCRIPTION: Tap on any part of the Betslip
        EXPECTED: * Free Bet Tooltip is closed
        EXPECTED: * *OX.freeBetTooltipSeen-username* key (Local Storage) is set as true
        """
        self.selection.freebet_tooltip.click()
        sleep(3)
        self.assertFalse(self.selection.has_freebet_tooltip(), msg='"Use Free Bet" link found')
        cookie = self.get_local_storage_cookie_value_as_dict(cookie_name=self.cookie_name)
        self.assertTrue(cookie, msg="'OX.freeBetTooltipSeen-username* key (Local Storage) is not set as true'")
