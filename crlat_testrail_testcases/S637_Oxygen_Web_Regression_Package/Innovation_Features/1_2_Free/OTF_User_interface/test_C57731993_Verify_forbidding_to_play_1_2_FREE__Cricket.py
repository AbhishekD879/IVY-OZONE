import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C57731993_Verify_forbidding_to_play_1_2_FREE__Cricket(Common):
    """
    TR_ID: C57731993
    NAME: Verify forbidding to play 1-2-FREE / Cricket
    DESCRIPTION: This test case verifies forbidding to play 1-2-FREE
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: 1. The user is logged in https://m.ladbrokes.com
    PRECONDITIONS: 2. Quick link 'Play 1-2-FREE' /  'Play 1-2-FREE-4s' is available on Homepage
    PRECONDITIONS: 3. User has zero balance or account not verified
    """
    keep_browser_open = True

    def test_001_tap_on_play_1_2_free___play_1_2_free_4s_quick_link_on_homepage_or_aem_banner(self):
        """
        DESCRIPTION: Tap on 'Play 1-2-FREE' /  'Play 1-2-FREE-4s' quick link on Homepage or AEM banner
        EXPECTED: - User should see pop-up message:
        EXPECTED: "Only verified customers can play 1-2-Free - please revisit the promotion once verification has been successfully completed."
        EXPECTED: - App should not open
        """
        pass

    def test_002_re_login_with_user_which_has_positive_balance(self):
        """
        DESCRIPTION: Re-login with user which has positive balance
        EXPECTED: Successful login
        """
        pass

    def test_003_tap_on__play_1_2_free___play_1_2_free_4s_quick_link_on_homepage_or_aem_banner(self):
        """
        DESCRIPTION: Tap on  'Play 1-2-FREE' /  'Play 1-2-FREE-4s' quick link on Homepage or AEM banner
        EXPECTED: - Play 1-2-FREE should opens successfully
        """
        pass
