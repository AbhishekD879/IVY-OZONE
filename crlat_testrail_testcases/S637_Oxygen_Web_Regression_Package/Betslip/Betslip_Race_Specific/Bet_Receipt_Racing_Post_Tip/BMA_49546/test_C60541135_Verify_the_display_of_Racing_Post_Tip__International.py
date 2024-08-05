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
class Test_C60541135_Verify_the_display_of_Racing_Post_Tip__International(Common):
    """
    TR_ID: C60541135
    NAME: Verify the display of Racing Post Tip - International
    DESCRIPTION: This test case verifies the display of Racing Post tip in Bet receipt (Both Main bet receipt and Quick Bet Receipt) from International Races when there are no UK & Irish races or all Tips are displayed from UK & Irish
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

    def test_005_validate_the_racing_post_tip_is_displayed_from_international_racesuk__irish_races_are_not_availableall_tips_are_already_displayed_from_uk__irish_to_the_userinternational_races_are_available(self):
        """
        DESCRIPTION: Validate the Racing Post Tip is displayed from International races
        DESCRIPTION: **UK & Irish Races are NOT Available**
        DESCRIPTION: **All tips are already displayed from UK & Irish to the User**
        DESCRIPTION: **International Races are available**
        EXPECTED: * Racing Post Tip should be displayed from International races(Races are available Today in International Races)
        EXPECTED: * Tips should be displayed from the next available race (In Next 15 mins is given the priority)
        EXPECTED: * There are no UK & Irish races for Today or all tips from UK & Irish races are already displayed to the User
        """
        pass

    def test_006_if_there_are_no_races_today_and_tomorrow_in_uk__irishand_no_tips_available_from_international_races_today_but_available_for_tomorrow_races(self):
        """
        DESCRIPTION: **If there are no races Today and Tomorrow in UK & Irish**
        DESCRIPTION: **And no Tips available from International races today but available for Tomorrow races**
        EXPECTED: * Racing Post Tip should be displayed from International races (From Tomorrow races)(Priority to the first available race)
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
