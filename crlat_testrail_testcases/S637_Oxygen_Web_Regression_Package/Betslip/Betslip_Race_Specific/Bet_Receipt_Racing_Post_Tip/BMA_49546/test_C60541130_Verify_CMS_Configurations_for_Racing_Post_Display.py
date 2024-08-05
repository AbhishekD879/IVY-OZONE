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
class Test_C60541130_Verify_CMS_Configurations_for_Racing_Post_Display(Common):
    """
    TR_ID: C60541130
    NAME: Verify CMS Configurations for Racing Post Display
    DESCRIPTION: This test case verifies the display of Racing Post tip based on the CMS configurations
    PRECONDITIONS: 1: User should have CMS access
    PRECONDITIONS: 2: Tips should be available from Racing Post **upcell API should retrieve Racing Post Tip data from B2B Horses API**
    PRECONDITIONS: **Rules for Tip Display**
    PRECONDITIONS: 1: User should place only single Horse racing Bet
    PRECONDITIONS: **Racing Post Tip Display**
    PRECONDITIONS: * If there is a UK & Ireland race starting in the next 15 minutes, then the Next UK & Ireland race tip will be displayed (ONLY)
    PRECONDITIONS: * IF there are no UK & Ireland races available in the next 15 minutes, then the next International race tip will be displayed (ONLY)
    PRECONDITIONS: * IF there are no UK & Ireland OR International races TODAY, then the next race (Tomorrow) will be displayed in Racing Post Tip
    PRECONDITIONS: * IF there are no races at all (unlikely) - then Racing Post Tip will not be displayed
    PRECONDITIONS: * IF a tip for a specific race has already been displayed to a user, then the same tip will NOT be displayed again (a specific race tip is displayed only once per customer)
    PRECONDITIONS: Note: Only ACTIVE selections will be displayed. e.g. Non Runners will not be displayed within the Racing Post Tips
    PRECONDITIONS: Note: Races that a user has already bet on will not display within Racing Post Tip
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user_and_validate_the_configurations_for_racing_post_tipnavigate_to_cms__system_configuration__structure(self):
        """
        DESCRIPTION: Login to CMS as admin user and validate the configurations for Racing Post Tip
        DESCRIPTION: Navigate to CMS > System Configuration > Structure
        EXPECTED: * User should be logged in successfully
        EXPECTED: * Racing Post Tip configuration should be displayed
        EXPECTED: * Enable /Disable toggles for Racing Post Tip should be displayed
        """
        pass

    def test_002_enable_racing_post_tip__main_bet_receipt_quick_bet_receipt(self):
        """
        DESCRIPTION: Enable Racing Post Tip , Main Bet receipt, Quick Bet receipt
        EXPECTED: User should be able to make the changes successfully
        """
        pass

    def test_003_login_to_ladbrokes_coral(self):
        """
        DESCRIPTION: Login to Ladbrokes /Coral
        EXPECTED: User should be logged in successfully
        """
        pass

    def test_004_mobile__desktop_navigate_to_horse_racing_add_one_selection_from_any_horse_racing_event_to_bet_slip(self):
        """
        DESCRIPTION: **Mobile & Desktop**
        DESCRIPTION: * Navigate to Horse Racing
        DESCRIPTION: * Add one selection from any Horse Racing event to Bet slip
        EXPECTED: * User should be navigated to Horse Racing landing page
        EXPECTED: * Selection should be added successfully to Main Bet slip
        """
        pass

    def test_005__enter_stake_and_click_on_place_bet(self):
        """
        DESCRIPTION: * Enter Stake and click on Place Bet
        EXPECTED: * User should be able to Place Bet successfully
        EXPECTED: * Bet Receipt should be displayed
        """
        pass

    def test_006_validate_the_display_of_racing_post_on_main_bet_receiptindexphpattachmentsget130402606_indexphpattachmentsget130402607(self):
        """
        DESCRIPTION: Validate the display of Racing Post on Main Bet receipt
        DESCRIPTION: ![](index.php?/attachments/get/130402606) ![](index.php?/attachments/get/130402607)
        EXPECTED: * Racing Post Tip should be displayed
        EXPECTED: * Tip should be displayed from the Next available race (As mentioned in the Pre-conditions)
        EXPECTED: * View Full Race Card Link should be displayed
        EXPECTED: * If bespoke is available for the selection or Runner the same should be displayed in the bet receipt
        EXPECTED: * Race Time & Meeting name should be displayed
        EXPECTED: * Trainer or Jockey name (if available) should be displayed
        EXPECTED: * Summary should be displayed (should be same as the SPOTLIGHT text displayed in Race card page for the runner/horse)
        EXPECTED: * Odds/Price should be displayed ( Fractional/Decimal as per User's Global setting)
        EXPECTED: * Racing Post header should be displayed as per designs
        """
        pass

    def test_007_mobile_onlyrepeat_step_2__step_3_via_quick_bet(self):
        """
        DESCRIPTION: **Mobile Only**
        DESCRIPTION: Repeat Step 2 & Step 3 via Quick Bet
        EXPECTED: * User should be able to Place Bet successfully
        EXPECTED: * Quick Bet Receipt should be displayed
        """
        pass

    def test_008_mobile_onlyvalidate_the_display_of_racing_post_tip_on_quick_bet_receiptindexphpattachmentsget130402608_indexphpattachmentsget130402609(self):
        """
        DESCRIPTION: **Mobile Only**
        DESCRIPTION: Validate the display of Racing Post Tip on Quick Bet receipt
        DESCRIPTION: ![](index.php?/attachments/get/130402608) ![](index.php?/attachments/get/130402609)
        EXPECTED: * Racing Post Tip should be displayed
        EXPECTED: * Tip should be displayed from the Next available race (As mentioned in the Pre-conditions)
        EXPECTED: * View Full Race Card Link should be displayed
        EXPECTED: * If bespoke is available for the selection or Runner the same should be displayed in the bet receipt
        EXPECTED: * Race Time & Meeting name should be displayed
        EXPECTED: * Trainer or Jockey name (if available) should be displayed
        EXPECTED: * Summary should be displayed (should be same as the SPOTLIGHT text displayed in Race card page for the runner/horse)
        EXPECTED: * Odds/Price should be displayed ( Fractional/Decimal as per User's Global setting)
        EXPECTED: * Racing Post header should be displayed as per designs
        """
        pass

    def test_009_navigate_to_cms_and_change_the_configurations_asracing_post_tip_disable(self):
        """
        DESCRIPTION: Navigate to CMS and change the configurations as
        DESCRIPTION: Racing Post Tip disable
        EXPECTED: User should be able to make the changes successfully
        """
        pass

    def test_010_repeat_the_above_steps_34_5_and_validate_the_display_of_racing_post_tip(self):
        """
        DESCRIPTION: Repeat the above steps 3,4, 5 and validate the display of Racing Post Tip
        EXPECTED: * Racing Post tip should **NOT** be displayed
        """
        pass
