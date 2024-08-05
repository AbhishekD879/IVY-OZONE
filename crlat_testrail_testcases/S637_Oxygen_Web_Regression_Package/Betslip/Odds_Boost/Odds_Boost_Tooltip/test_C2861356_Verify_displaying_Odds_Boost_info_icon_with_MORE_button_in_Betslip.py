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
class Test_C2861356_Verify_displaying_Odds_Boost_info_icon_with_MORE_button_in_Betslip(Common):
    """
    TR_ID: C2861356
    NAME: Verify displaying Odds Boost info icon  with MORE button in Betslip
    DESCRIPTION: This test case verifies that odds boost info icon is shown with MORE button in Betslip
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: Odds Boost tokens is added for USER1 using instruction - https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: 'More Link' is configured in CMS for Odds Boost section (e.g. /oddsboost: in this case user will be redirected to Odds Boost page)
    PRECONDITIONS: **Note:** Selection appropriate for odds boost should have 'Enhance Odds available' checked on all hierarchy level
    PRECONDITIONS: Login with User1
    PRECONDITIONS: Add selection to the Betslip
    """
    keep_browser_open = True

    def test_001_navigate_to_betslipverify_that_i_icon_is_displaying_in_odds_boost_section(self):
        """
        DESCRIPTION: Navigate to Betslip
        DESCRIPTION: Verify that 'i' icon is displaying in odds boost section
        EXPECTED: Betslip is shown with appropriate elements:
        EXPECTED: - 'BOOST' button
        EXPECTED: - Odds Boost header text
        EXPECTED: - Tap to Boost your betslip text with 'i' icon
        """
        pass

    def test_002_tap_i_iconverify_that_the_tooltip_style_popup_is_displayed(self):
        """
        DESCRIPTION: Tap 'i' icon
        DESCRIPTION: Verify that the tooltip style popup is displayed
        EXPECTED: Popup with appropriate elements:
        EXPECTED: - Hardcoded text is shown: 'Hit Boost to increase the odds of the bets in your betslip! You can boost up to (currency)XXX.XX total stake.'
        EXPECTED: - 'Ok' button
        EXPECTED: - 'More' button
        """
        pass

    def test_003_tap_ok_buttonverify_that_popup_is_closed(self):
        """
        DESCRIPTION: Tap 'OK' button
        DESCRIPTION: Verify that popup is closed
        EXPECTED: Popup is closed
        """
        pass

    def test_004_tap_i_icon_one_more_time(self):
        """
        DESCRIPTION: Tap 'i' icon one more time
        EXPECTED: Popup with appropriate elements:
        EXPECTED: - Hardcoded text is shown: 'Hit Boost to increase the odds of the bets in your betslip! You can boost up to (currency)XXX.XX total stake.'
        EXPECTED: - 'OK' button
        EXPECTED: - 'More' button
        """
        pass

    def test_005_tap_more_buttonverify_that_user_is_redirected_to_appropriate_page(self):
        """
        DESCRIPTION: Tap 'MORE' button
        DESCRIPTION: Verify that user is redirected to appropriate page
        EXPECTED: User is rediredted to Odds Bosst page (in case 'More Link' is configured in CMS as /oddsboost)
        """
        pass
