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
class Test_C403334_Anchored_Footer(Common):
    """
    TR_ID: C403334
    NAME: Anchored Footer
    DESCRIPTION: Test case verifies that Betslip Footer is Anchored to the App footer (mobile), and Anchored to Betslip Section Border ( Tablet) with
    DESCRIPTION: max size of 450 px in Landscape, 600 px in Portrait mode ( including Betslip Section header).
    DESCRIPTION: The Content of Betslip is Scrollable except Betslip Footer.
    DESCRIPTION: **JIRA tickets:**
    DESCRIPTION: BMA-11529 Bet Now button area Anchoring (footer)
    PRECONDITIONS: Make sure you have user account with registered credit cards
    """
    keep_browser_open = True

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_add_one_selection_to_a_betslip__open_betslip_only_mobile(self):
        """
        DESCRIPTION: Add one selection to a Betslip
        DESCRIPTION: -> Open Betslip (only mobile)
        EXPECTED: *mobile*
        EXPECTED: - Betslip is opened
        EXPECTED: - Footer is fully visible  and is displayed in the bottom:
        EXPECTED: Total Stake, Total Estimated Return, Bin icon and 'BET NOW' buttons
        EXPECTED: **From OX 99**
        EXPECTED: Coral: Total stake, Estimated Returns, is stuck to the bottom of the page
        EXPECTED: Ladbrokes: Total Stake, Potential Return, is displayed under the last selection in the betslip
        EXPECTED: - Only one Selection is visible
        EXPECTED: *tablet*
        EXPECTED: - Footer is fully visible  and is displayed in the bottom of  section:
        EXPECTED: Total Stake, Total Estimated Return, Bin icon and 'BET NOW' buttons
        EXPECTED: - Selection is fully visible
        EXPECTED: - Betslip section size  is based on selection and footer heights
        """
        pass

    def test_003_enter_stake_that_exceeds_max_stake_limit_for_current_selection(self):
        """
        DESCRIPTION: Enter Stake that exceeds max stake limit for current selection
        EXPECTED: - Footer is fully visible  and is displayed in the bottom
        EXPECTED: - Only one Selection is visible
        """
        pass

    def test_004_trigger_in_backoffice__overask_cancellation__overask_confirmation__overask_offer(self):
        """
        DESCRIPTION: Trigger in Backoffice:
        DESCRIPTION: - Overask Cancellation
        DESCRIPTION: - Overask Confirmation
        DESCRIPTION: - Overask Offer
        EXPECTED: - Footer is fully visible  and is displayed in the bottom:
        EXPECTED: Total Stake, Total Estimated Return, Bin icon disabled buttons
        EXPECTED: **From OX 99**
        EXPECTED: Coral: Total stake, Estimated Returns are stuck to the bottom of the page
        EXPECTED: Ladbrokes: Total Stake, Potential Returns are displayed under the last selection in the betslip
        EXPECTED: and
        EXPECTED: -'CONTINUE'/'CONFIRM'/'CANCEL' buttons in accordance to overask scenario
        EXPECTED: - Only one Selection is visible
        """
        pass

    def test_005_select_and__click_confirm(self):
        """
        DESCRIPTION: (Select and ) Click 'CONFIRM'
        EXPECTED: 
        """
        pass

    def test_006_add_few_selections__based_on_device__resolution_andat_least_one_selection_is_under_betslip_footer_to_a_betslip__open_betslip_only_mobile(self):
        """
        DESCRIPTION: Add few selections ( based on device  resolution and
        DESCRIPTION: at least one selection is under Betslip footer) to a Betslip
        DESCRIPTION: -> Open Betslip (only mobile)
        EXPECTED: *mobile*
        EXPECTED: - Betslip is opened
        EXPECTED: - Footer is fully visible  and is displayed in the bottom:
        EXPECTED: Total Stake, Total Estimated Return,  Bin icon and 'BET NOW' buttons
        EXPECTED: - Only Part of Selections are visible (those that take place above Footer)
        EXPECTED: **From OX 99**
        EXPECTED: Coral: Total stake, Estimated Returns are stuck to the bottom of the page.
        EXPECTED: Ladbrokes: Total Stake, Potential Return are displayed under the last selection in the betslip
        EXPECTED: *tablet*
        EXPECTED: - Footer is fully visible  and is displayed in the bottom of  section:
        EXPECTED: Total Stake, Total Estimated Return, Bin icon and 'BET NOW' buttons
        EXPECTED: - Only Part of Selections are visible (those that take place above Footer)
        EXPECTED: - Max Betslip section size  is  450px (landscape)/ 600px (portrait)
        """
        pass

    def test_007_scroll_to_the_last_selection_is_list(self):
        """
        DESCRIPTION: Scroll to the last selection is list
        EXPECTED: - All Selections are visible while scrolling
        EXPECTED: - Footer is fully visible  and is displayed in the bottom:
        EXPECTED: Total Stake, Total Estimated Return, Bin icon and 'BET NOW' buttons
        EXPECTED: - NO Selections on background of Footer
        EXPECTED: **From OX 99**
        EXPECTED: Coral: Total stake, Estimated Returns, 'PLACE BET" button are stuck to the bottom of the page.
        EXPECTED: Ladbrokes: Total Stake, Potential Return,  'PLACE BET" button are displayed under the last selection in the betslip
        """
        pass

    def test_008_na_after_ox_99click_bin_icon(self):
        """
        DESCRIPTION: **N/A after OX 99**
        DESCRIPTION: Click Bin icon
        EXPECTED: - Footer is fully visible  and is displayed in the bottom:
        EXPECTED: Total Stake, Total Estimated Return, 'CONFIRM CLEAR BETSLIP' and 'CANCEL' buttons
        EXPECTED: - Only Part of Selections are visible (those that take place above Footer)
        """
        pass

    def test_009_click_cancel_and_than_bet_now(self):
        """
        DESCRIPTION: Click 'CANCEL' and than 'BET NOW'
        EXPECTED: - Bet is placed and BET RECEIPT IS SHOWN
        EXPECTED: - Footer is fully visible  and is displayed in the bottom:
        EXPECTED: Total Stake, Total Estimated Return, 'REUSE SELECTION' and 'DONE' buttons
        EXPECTED: - Only Part of Selections are visible (those that take place above Footer)
        """
        pass

    def test_010_click_done(self):
        """
        DESCRIPTION: Click 'DONE'
        EXPECTED: 
        """
        pass

    def test_011_rotate_device_and_repeat_steps_2_10_portrait___landscape(self):
        """
        DESCRIPTION: Rotate Device and Repeat steps #2-10 Portrait <-> Landscape
        EXPECTED: 
        """
        pass

    def test_012_login_and_repeat_steps_1_11_for_logged_in_user(self):
        """
        DESCRIPTION: Login and Repeat steps #1-11 for Logged in user
        EXPECTED: 
        """
        pass
