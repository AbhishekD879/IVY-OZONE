import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.native
@vtest
class Test_C59918226_Free_Bet_sign_posting(Common):
    """
    TR_ID: C59918226
    NAME: Free Bet sign posting
    DESCRIPTION: This test case describes displaying/closing Free Bet sign posting
    DESCRIPTION: Designs:
    DESCRIPTION: Coral: https://app.zeplin.io/project/5dc1abe9fefe5d837a9b93cd/dashboard?q=free&sid=5eada1f2d9cc2c193e409814
    DESCRIPTION: Ladbrokes: https://app.zeplin.io/project/5dc1abb838e1dd72b89d1a21/dashboard?sid=5ea99a214c42b7267ad5f237
    PRECONDITIONS: - user has a free bet available
    PRECONDITIONS: - qualifying selection is added to bet slip
    """
    keep_browser_open = True

    def test_001_expand_the_bet_slip(self):
        """
        DESCRIPTION: expand the bet slip
        EXPECTED: the bet slip is expanded
        EXPECTED: free bet signposting on a bet slip is displayed
        EXPECTED: ![](index.php?/attachments/get/119425535)
        EXPECTED: ![](index.php?/attachments/get/119425536)
        """
        pass

    def test_002_tap_on_use_free_bet_sign_posting(self):
        """
        DESCRIPTION: tap on Use Free Bet sign posting
        EXPECTED: free bet overlay which lists all the free bets available for user to use is opened
        EXPECTED: ![](index.php?/attachments/get/119425537)
        EXPECTED: ![](index.php?/attachments/get/119425538)
        """
        pass

    def test_003_close_overlay__by_tapping_the_close_buttonswipeing_away_from_overlay(self):
        """
        DESCRIPTION: close overlay  by tapping the close button/swipeing away from overlay
        EXPECTED: overlay is closed
        """
        pass
