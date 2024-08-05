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
class Test_C47660500_Verify_BOG_icon_Pop_up(Common):
    """
    TR_ID: C47660500
    NAME: Verify BOG icon Pop-up
    DESCRIPTION: This test case verifies that the BOG icon Pop-up
    PRECONDITIONS: * BOG has been enabled in CMS
    PRECONDITIONS: * Signposting toggle is Turn ON in the CMS
    PRECONDITIONS: * BOG Pop-up configured with Header, Pop-up text and Link in CMS (CMS > Promotions > Promotions)
    """
    keep_browser_open = True

    def test_001_tap_on_bog_icon_on_an_event_page(self):
        """
        DESCRIPTION: Tap on BOG icon on an event page
        EXPECTED: * BOG Pop-up window shown with overlay
        EXPECTED: * BOG Pop-up displayed with Header, Pop-Up Text and 2 buttons (Coral) / 1 button (Ladbrokes)
        EXPECTED: * Texts successfully retrieved from CMS
        """
        pass

    def test_002_tap_on_the_configured_link_inside_of_pop_up(self):
        """
        DESCRIPTION: Tap on the configured Link inside of Pop-Up
        EXPECTED: * User successfully redirected to the configured link
        """
        pass

    def test_003_click_on_more_button_on_promo_signposting_pop_up_coral_only(self):
        """
        DESCRIPTION: Click on 'MORE' button on Promo Signposting Pop-up (Coral only)
        EXPECTED: * Promo Signposting overlay is displayed
        """
        pass

    def test_004_tap_on_x_or_empty_area_outside_of_pop_up(self):
        """
        DESCRIPTION: Tap on [X] or empty area outside of Pop-Up
        EXPECTED: * Pop-Up successfully closed
        """
        pass

    def test_005_tap_on_bog_icon_on_bet_receipt(self):
        """
        DESCRIPTION: Tap on BOG icon on Bet Receipt
        EXPECTED: * BOG Pop-up window NOT shown
        """
        pass
