import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.betslip
@vtest
class Test_C2988037_Verify_index_handicap_changing_in_Betslip_for_boosted_bet(Common):
    """
    TR_ID: C2988037
    NAME: Verify index/handicap changing in Betslip for boosted bet
    DESCRIPTION: This test case verifies index/handicap changing in Betslip for bet that is selected for an odds boost
    PRECONDITIONS: Enable Odds Boost in CMS
    PRECONDITIONS: Load Application
    PRECONDITIONS: Login into App by user with Odds boost token generated
    PRECONDITIONS: How to generate Odds Boost: https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: Add selection to Betslip where handicap is available
    PRECONDITIONS: Tap 'Boost' button
    """
    keep_browser_open = True

    def test_001_change_indexhandicap_value_for_added_selectionhttpsbackoffice_tst2coralcouktiverify_that_messaging_is_shown_to_the_user_with_live_push(self):
        """
        DESCRIPTION: Change index/handicap value for added selection
        DESCRIPTION: (https://backoffice-tst2.coral.co.uk/ti)
        DESCRIPTION: Verify that messaging is shown to the user with live push
        EXPECTED: - Handicap value is updated to reflect the changed value
        EXPECTED: - Error message: 'Handicap value changed from OLD To NEW' should be displayed
        EXPECTED: **After OX99**
        EXPECTED: ![](index.php?/attachments/get/33755)
        EXPECTED: ![](index.php?/attachments/get/33754)
        """
        pass

    def test_002_verify_that_the_boost_remains_selected(self):
        """
        DESCRIPTION: Verify that the boost remains selected
        EXPECTED: The boost remains selected
        """
        pass

    def test_003_verify_that_the_boosted_price_is_displayed(self):
        """
        DESCRIPTION: Verify that the boosted price is displayed
        EXPECTED: The boosted price is displayed
        """
        pass

    def test_004_verify_that_the_non_boosted_price_is_displayed(self):
        """
        DESCRIPTION: Verify that the non-boosted price is displayed
        EXPECTED: The non-boosted price is displayed
        """
        pass

    def test_005_verify_button_changed_to_accept__place_bet(self):
        """
        DESCRIPTION: Verify button changed to 'ACCEPT & PLACE BET''
        EXPECTED: The button is shown:
        EXPECTED: Coral: 'ACCEPT & PLACE BET'
        EXPECTED: Ladbrokes: 'ACCEPT AND PLACE BET'
        """
        pass
