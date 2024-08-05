import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C59925219_Verify_that_display_of_Next_Races_in_Bet_Receipt(Common):
    """
    TR_ID: C59925219
    NAME: Verify that display of Next Races in Bet Receipt
    DESCRIPTION: This Test case verifies the display of Next races in Bet Receipt (Main Bet Receipt & Quick Bet Receipt)
    DESCRIPTION: Only Next 3 Races should be displayed
    PRECONDITIONS: 1: Racing Post Tip should not be available and displayed
    PRECONDITIONS: 2: User should place single Bet on Horse racing
    PRECONDITIONS: 3: Next races should be available
    PRECONDITIONS: 4: Next Races toggle should be enabled in CMS
    PRECONDITIONS: Note: Racing post tip & Next Races should never be displayed at the same time.
    """
    keep_browser_open = True

    def test_001_login_to_ladbrokescoral_app(self):
        """
        DESCRIPTION: Login to Ladbrokes/Coral App
        EXPECTED: User should be able to login successfully
        """
        pass

    def test_002_mobile__desktop_navigate_to_horse_racing_add_one_selection_from_any_horse_racing_event_to_bet_slip(self):
        """
        DESCRIPTION: **Mobile & Desktop**
        DESCRIPTION: * Navigate to Horse Racing
        DESCRIPTION: * Add one selection from any Horse Racing event to Bet slip
        EXPECTED: * User should be navigated to Horse Racing landing page
        EXPECTED: * Selection should be added successfully to Main Bet slip
        """
        pass

    def test_003__enter_stake_and_click_on_place_bet(self):
        """
        DESCRIPTION: * Enter Stake and click on Place Bet
        EXPECTED: * User should be able to Place Bet successfully
        EXPECTED: * Bet Receipt should be displayed
        """
        pass

    def test_004_verify_the_display_of_next_races_panel_within_bet_receipt(self):
        """
        DESCRIPTION: Verify the display of Next Races panel within Bet receipt
        EXPECTED: * Next Races panel should be displayed as per the designs
        EXPECTED: * Only three races should be displayed
        EXPECTED: * Race Time and Meeting Name should be displayed
        EXPECTED: * Race Type and Distance should be displayed
        EXPECTED: * If there are UK & Irish races available in the next 15 minutes - Next Races Panel will display the next 3 available races
        EXPECTED: * IF there are no UK & IRELAND races available then the next international races will display
        EXPECTED: * If there are both UK & Irish and International races available in the next 15 minutes then Priority display will be for UK & Irish races ONLY
        EXPECTED: * If there is 1 race from UK & Irish and 2 races from International races available in the next 15 minutes then Next races panel should display both UK & Irish and International races
        EXPECTED: Note: IF there are no races at all (unlikely) - then Next Races will not be displayed
        """
        pass

    def test_005_verify_the_display_of_race_type_distance_displayed_in_the_next_races_panel(self):
        """
        DESCRIPTION: Verify the display of Race type, Distance displayed in the Next Races Panel
        EXPECTED: * Race Type and Distance should be displayed below the Race Time and Meeting name
        """
        pass

    def test_006_click_on_the_chevron_displayed_next_to_the_race(self):
        """
        DESCRIPTION: Click on the chevron displayed next to the race
        EXPECTED: * User should be navigated to Race Card details page
        """
        pass

    def test_007_only_mobilerepeat_23_via_quick_betvalidate_the_display_of_next_races_panel_in_the_bet_receipt(self):
        """
        DESCRIPTION: **Only Mobile**
        DESCRIPTION: Repeat 2,3 via Quick Bet
        DESCRIPTION: Validate the display of Next races Panel in the Bet Receipt
        EXPECTED: * Next Races panel should be displayed as per the designs
        EXPECTED: * Only three races should be displayed
        EXPECTED: * Race Time and Meeting Name should be displayed
        EXPECTED: * Race Type and Distance should be displayed
        EXPECTED: * If there are UK & Irish races available in the next 15 minutes - Next Races Panel will display the next 3 available races
        EXPECTED: * IF there are no UK & IRELAND races available then the next international races will display
        EXPECTED: * If there are both UK & Irish and International races available in the next 15 minutes then Priority display will be for UK & Irish races ONLY
        EXPECTED: * If there is 1 race from UK & Irish and 2 races from International races available in the next 15 minutes then Next races panel should display both UK & Irish and International races
        EXPECTED: Note: IF there are no races at all (unlikely) - then Next Races will not be displayed
        """
        pass
