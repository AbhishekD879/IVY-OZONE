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
class Test_C60541128_Verify_the_display_of_View_Full_Race_Card_Link(Common):
    """
    TR_ID: C60541128
    NAME: Verify the display of View Full Race Card Link
    DESCRIPTION: This test case verifies the display of View Full Race Card Link in  Racing Post tip - Bet receipt (Both Main bet receipt and Quick Bet Receipt)  and navigation to Race Card details page
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
        EXPECTED: * View Full Race Card Link should be displayed
        """
        pass

    def test_005_click_on__view_full_race_card_link(self):
        """
        DESCRIPTION: Click on  View Full Race Card Link
        EXPECTED: * User should be navigated to Race Card Detail page (EDP) of that race
        EXPECTED: * View Full Race Card link should be displayed as mentioned in the designs
        """
        pass

    def test_006_only_mobilerepeat_the_above_steps_for_quick_bet___place_bet_via_quick_bet_and_validate_the_quick_bet_receipt(self):
        """
        DESCRIPTION: **Only Mobile**
        DESCRIPTION: Repeat the above steps for Quick Bet - Place bet via Quick bet and Validate the Quick Bet Receipt
        EXPECTED: * User should be navigated to Race Card Detail page (EDP) of that race on clicking View Full Race Card in Quick Bet Receipt
        """
        pass
