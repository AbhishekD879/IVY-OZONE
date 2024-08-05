import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C60017860_Verify_Highlighting_Icons_on_Bottom_Bar(Common):
    """
    TR_ID: C60017860
    NAME: Verify Highlighting Icons on Bottom Bar
    DESCRIPTION: This test case verifies that any Bottom Bar icon is highlighted when the user is on the corresponded page.
    PRECONDITIONS: * Coral/Ladbrokes app is installed and launched
    PRECONDITIONS: Designs:
    PRECONDITIONS: Coral:
    PRECONDITIONS: https://app.zeplin.io/project/5db9a772249ee083943f7259/dashboard?seid=5dd26b3cd37ceb668c203655
    PRECONDITIONS: Ladbrokes:
    PRECONDITIONS: https://app.zeplin.io/project/5db9a6d44a45be834b98748a/dashboard?seid=5dce7ecbf6b7d53c087f3eb4
    """
    keep_browser_open = True

    def test_001_tap_on_any_of_icon_on_in_the_bottom_bar_ex_in_play(self):
        """
        DESCRIPTION: Tap on any of icon on in the Bottom Bar (e.x In-play)!
        EXPECTED: In-play icon is highlighted
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/120999549)
        EXPECTED: Dark mode:
        EXPECTED: ![](index.php?/attachments/get/120999552)
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/120999550)
        EXPECTED: Dark mode:
        EXPECTED: ![](index.php?/attachments/get/120999551)
        """
        pass

    def test_002_repeat_1_step_with_the_others_icons_homepage_my_bets_account_or_gaming(self):
        """
        DESCRIPTION: Repeat 1 step with the others icons: Homepage, My Bets, Account or Gaming
        EXPECTED: Each icon is highlighed when users taps on it.
        """
        pass
