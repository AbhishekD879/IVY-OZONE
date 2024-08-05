import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C2297767_Tracking_of_Upgrade_your_account_dialog(Common):
    """
    TR_ID: C2297767
    NAME: Tracking of 'Upgrade your account' dialog
    DESCRIPTION: This test case verifies passing Upgrade Account Prompt data to Google Tag Manager
    PRECONDITIONS: The way to open upgrade dialog: Load SB app -> Log in as an in-shop user (5000000000979448/1234) for the first time (to emulate this clear local storage and cookies before Log in)
    PRECONDITIONS: Open dev tool -> Console -> type 'dataLayer' in Console ![](index.php?/attachments/get/22566)
    """
    keep_browser_open = True

    def test_001_log_in_as_an_in_shop_user_for_the_first_time_and_tap_upgrade_button_on_upgrade_dialog(self):
        """
        DESCRIPTION: Log in as an in-shop user for the first time and tap 'Upgrade' button on Upgrade dialog
        EXPECTED: There is the following information in the Console:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'cta',
        EXPECTED: 'eventAction' : 'upgrade account'
        EXPECTED: 'eventLabel' : 'yes - upgrade Account'
        EXPECTED: });
        """
        pass

    def test_002_log_in_as_an_in_shop_user_for_the_first_time_and_tap_no_thanks_link_on_upgrade_dialog(self):
        """
        DESCRIPTION: Log in as an in-shop user for the first time and tap 'No, thanks' link on Upgrade dialog
        EXPECTED: There is the following information in the Console:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'cta',
        EXPECTED: 'eventAction' : 'upgrade account'
        EXPECTED: 'eventLabel' : 'no thanks'
        EXPECTED: });
        """
        pass

    def test_003_log_in_as_an_in_shop_user_for_the_first_time_and_tap_close_button_x_on_upgrade_dialog(self):
        """
        DESCRIPTION: Log in as an in-shop user for the first time and tap close button 'X' on Upgrade dialog
        EXPECTED: There is no additional dataLayer.push with 'event': 'trackEvent' for close button 'X'
        """
        pass
