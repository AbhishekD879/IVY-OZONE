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
class Test_C60541132_Verify_Racing_Post_Tip_is_Not_Repeated_to_User(Common):
    """
    TR_ID: C60541132
    NAME: Verify Racing Post Tip is Not Repeated to User
    DESCRIPTION: This test case verifies the display of Racing Post tip in Bet receipt (Both Main bet receipt and Quick Bet Receipt)
    DESCRIPTION: Racing Post Tip is not repeated for User
    PRECONDITIONS: 1: Racing Post Tip should be enabled in CMS (Main Bet Receipt and Quick Bet Receipt)
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

    def test_001_login_to_ladbrokes_coral(self):
        """
        DESCRIPTION: Login to Ladbrokes /Coral
        EXPECTED: User should be logged in successfully
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

    def test_004_validate_the_display_of_racing_post_on_main_bet_receiptindexphpattachmentsget130402606_indexphpattachmentsget130402607(self):
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

    def test_005_place_more_single_horse_racing_bets_and_validate_the_tip_display(self):
        """
        DESCRIPTION: Place more single Horse racing bets and Validate the Tip display
        EXPECTED: * Racing Post Tip should be displayed as per the Pre-conditions mentioned
        EXPECTED: * Same Tip should **NOT** be displayed to the User (Not Repeated)
        EXPECTED: * Tip should not be displayed from the races where User has already placed bets
        """
        pass

    def test_006_login_with_a_different_user_and_repeat_steps___2345(self):
        """
        DESCRIPTION: Login with a different User and repeat Steps - 2,3,4,5
        EXPECTED: * User should be able to login
        EXPECTED: * User should be able to place bets
        EXPECTED: * Tips can be displayed which were displayed to the previous user but Tips should not be repeated for the same User
        EXPECTED: **IF a tip for a specific race has already been displayed to a user, then the same tip will NOT be displayed again (a specific race tip is displayed only once per customer)**
        """
        pass

    def test_007_mobile_onlyrepeat_above_via_quick_bet(self):
        """
        DESCRIPTION: **Mobile Only**
        DESCRIPTION: Repeat above via Quick Bet
        EXPECTED: * User should be able to Place Bet successfully
        EXPECTED: * Quick Bet Receipt should be displayed
        """
        pass

    def test_008__login_with_a_user_in_a_device_and_place_single_horse_racing_bet_login_with_the_same_user_and_in_different_device_and_place_single_horse_racing_bet(self):
        """
        DESCRIPTION: * Login with a User in a device and Place single Horse Racing bet
        DESCRIPTION: * Login with the same user and in different device and place Single Horse Racing Bet
        EXPECTED: **Device 1**
        EXPECTED: * User should be logged in and place bet successfully
        EXPECTED: * Racing Post Tip should be displayed
        EXPECTED: **Device 2**
        EXPECTED: * User should be logged in and place bet successfully
        EXPECTED: * Racing Post Tip should be displayed
        EXPECTED: * Racing Post Tip displayed in device 1 should not be displayed in device 2
        """
        pass

    def test_009_repeat_above_with_quick_bet(self):
        """
        DESCRIPTION: Repeat above with Quick Bet
        EXPECTED: 
        """
        pass
