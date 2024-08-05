import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.virtual_sports
@vtest
class Test_C869684_Bet_Placement_on_Virtual_Racing(Common):
    """
    TR_ID: C869684
    NAME: Bet Placement on Virtual Racing
    DESCRIPTION: This test case verifies bet placement on  Virtual Racing
    DESCRIPTION: AUTOTEST [C9770826]
    PRECONDITIONS: Login with user account that has positive balance
    """
    keep_browser_open = True

    def test_001_load_oxygen_application_and_tap_virtual_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Load Oxygen application and tap 'Virtual' icon from the Sports Menu Ribbon
        EXPECTED: Virtual Sports successfully opened
        """
        pass

    def test_002_select_two_priceodds_button_for_verified_event(self):
        """
        DESCRIPTION: Select two 'Price/Odds' button for verified event
        EXPECTED: - Selected 'Price/Odds' buttons are highlighted in green
        EXPECTED: - Betslip icon with bet indicator appears
        """
        pass

    def test_003_open_betslip(self):
        """
        DESCRIPTION: Open Betslip
        EXPECTED: - Selections with bet details is displayed in the Betlsip
        EXPECTED: - 2 (Two) Selections are present in Section 'Singles (2)'
        """
        pass

    def test_004_set_stake_for_singles2_and_click_bet_now_button(self):
        """
        DESCRIPTION: Set 'Stake' for 'Singles(2)' and click 'Bet Now' button
        EXPECTED: - Bet is placed
        EXPECTED: - Bet receipt appears in Betslip
        EXPECTED: - 'Reuse selections' and 'Done' buttons are present in footer
        """
        pass

    def test_005_click_reuse_selections_button(self):
        """
        DESCRIPTION: Click 'Reuse selections' button
        EXPECTED: - Betslip contains all the same selections
        """
        pass

    def test_006_click__done_button(self):
        """
        DESCRIPTION: Click ' Done' button
        EXPECTED: - Betslip is empty with no selections
        """
        pass

    def test_007_for_hrgreyhounds_before_ox_98select_two_priceodds_button_for_verified_event(self):
        """
        DESCRIPTION: **For HR/Greyhounds (before OX 98)**
        DESCRIPTION: Select two 'Price/Odds' button for verified event
        EXPECTED: - Selected 'Price/Odds' buttons are highlighted in green
        EXPECTED: - Betslip icon with bet indicator appears
        """
        pass

    def test_008_open_betslip(self):
        """
        DESCRIPTION: Open Betslip
        EXPECTED: - Selections with bet details is displayed in the Betlsip
        EXPECTED: - Selections are present in Section 'Singles (2)'
        EXPECTED: - Forecast/Tricast section is present
        """
        pass

    def test_009_set_stake_for_singles2_and_forecasttricast_section_and_click_bet_now_button(self):
        """
        DESCRIPTION: Set 'Stake' for 'Singles(2)' and 'Forecast/Tricast' section and click 'Bet Now' button
        EXPECTED: - Bet is placed
        EXPECTED: - Bet receipt appears in Betslip
        EXPECTED: - 'Reuse selections' and 'Done' buttons are present in footer
        """
        pass

    def test_010_click_reuse_selections_button(self):
        """
        DESCRIPTION: Click 'Reuse selections' button
        EXPECTED: - Betslip contains all the same selections
        """
        pass

    def test_011_click__done_button(self):
        """
        DESCRIPTION: Click ' Done' button
        EXPECTED: - Betslip is empty with no selections
        """
        pass

    def test_012_for_horse_racinggreyhounds_after_ox98navigate_to_forecasttricast_tabselect_1st2nd3rd_or_any_runners(self):
        """
        DESCRIPTION: **For Horse Racing/Greyhounds (after OX98)**
        DESCRIPTION: Navigate to Forecast/Tricast tab
        DESCRIPTION: Select 1st/2/nd/3rd or ANY runners
        EXPECTED: - Selected buttons are highlighted in green
        EXPECTED: - 'ADD TO BETSLIP' button is enabled
        """
        pass

    def test_013_for_horse_racinggreyhounds_after_ox98tap_add_to_betslip_buttonnavigate_to_betslip(self):
        """
        DESCRIPTION: **For Horse Racing/Greyhounds (after OX98)**
        DESCRIPTION: Tap 'ADD TO BETSLIP' button
        DESCRIPTION: Navigate to betslip
        EXPECTED: - 'Forecast/Tricast' selections are shown in Betslip with details
        """
        pass

    def test_014_repeat_this_test_case_for_all_virtual_racesvirtual_motorsports_class_id_288virtual_cycling_class_id_290virtual_horse_racing_class_id_285virtual_greyhound_racing_class_id_286virtual_grand_national_class_id_26604(self):
        """
        DESCRIPTION: Repeat this test case for all Virtual Races:
        DESCRIPTION: Virtual Motorsports (Class ID 288)
        DESCRIPTION: Virtual Cycling (Class ID 290)
        DESCRIPTION: Virtual Horse Racing (Class ID 285)
        DESCRIPTION: Virtual Greyhound Racing (Class ID 286)
        DESCRIPTION: Virtual Grand National (Class ID 26604)
        EXPECTED: 
        """
        pass
