import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C66113524_Verify_padding_of_status_tracking_aligned_with_all_selections_when_atleast_one_selection_has_tracking_for_Single_Multiple_Bets_in_My_BetsOpen_Cash_outSettled(Common):
    """
    TR_ID: C66113524
    NAME: Verify padding of status tracking aligned with all selections when atleast one selection has tracking  for Single/Multiple Bets in My Bets(Open, Cash out,Settled)
    DESCRIPTION: This testcase verifies padding of status tracking aligned with all selections when atleast one selection has tracking  for Single/Multiple Bets in My Bets(Open, Cash out,Settled)
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_000_load_oxygen_application(self):
        """
        DESCRIPTION: Load oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_001_login_to_the_application_with_valid_credentials(self):
        """
        DESCRIPTION: Login to the application with valid credentials
        EXPECTED: User is logged in
        """
        pass

    def test_002_tap_on_my_bets_item_on_top_menu(self):
        """
        DESCRIPTION: Tap on 'My bets' item on top menu
        EXPECTED: My bets page/Betslip widget is opened.By default user will be on open tab
        """
        pass

    def test_003_place_any_acca_bet_using_multiple_sellections_from_different_events_which_includes_atleast_one_inplay_selection(self):
        """
        DESCRIPTION: Place any acca bet using multiple sellections from different events which includes atleast one inplay selection
        EXPECTED: Bet placed successfully
        """
        pass

    def test_004_verift_acca_bet_placed_in_step4(self):
        """
        DESCRIPTION: verift acca bet placed in step4
        EXPECTED: Status tracking icon  should be displayed for selection of inplay event as per figma provided
        EXPECTED: ![](index.php?/attachments/get/a6ddcb73-b6a9-4d6d-a6d3-8afb8a7476d1)
        """
        pass

    def test_005_verify_selections_of_preplay_event_which_includes_in_acca_bet(self):
        """
        DESCRIPTION: Verify selections of preplay event which includes in acca bet
        EXPECTED: No icons should be displayed for the selections of preplay events.
        EXPECTED: ![](index.php?/attachments/get/60e837f1-49ab-4840-bcdb-bc5349681c06)
        """
        pass

    def test_006_repeat_4_6_in_cash_out_tab(self):
        """
        DESCRIPTION: Repeat 4-6 in Cash out tab
        EXPECTED: result should be same
        EXPECTED: ![](index.php?/attachments/get/0a6a0aad-6e89-418a-a1c7-229edd286d38)
        """
        pass

    def test_007_repeat_4_6_in_settled_tab(self):
        """
        DESCRIPTION: Repeat 4-6 in Settled tab
        EXPECTED: Result should be same
        EXPECTED: ![](index.php?/attachments/get/c73619a7-f6c7-42db-a318-dd2d92ab7a1e)
        """
        pass
