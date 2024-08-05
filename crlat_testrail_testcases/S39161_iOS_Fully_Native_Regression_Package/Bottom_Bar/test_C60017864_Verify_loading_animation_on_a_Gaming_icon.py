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
class Test_C60017864_Verify_loading_animation_on_a_Gaming_icon(Common):
    """
    TR_ID: C60017864
    NAME: Verify loading animation on a "Gaming" icon.
    DESCRIPTION: This test case verifies that the "Gaming" icon has a loading animation when downloading ODR game.
    PRECONDITIONS: * Coral/Ladbrokes app is installed and launched
    PRECONDITIONS: Designs:
    PRECONDITIONS: Coral:
    PRECONDITIONS: https://app.zeplin.io/project/5db9a772249ee083943f7259/dashboard?seid=5dd26b3cd37ceb668c203655
    PRECONDITIONS: Ladbrokes:
    PRECONDITIONS: https://app.zeplin.io/project/5db9a6d44a45be834b98748a/dashboard?seid=5dce7ecbf6b7d53c087f3eb4
    """
    keep_browser_open = True

    def test_001_tap_on_gaming_icon(self):
        """
        DESCRIPTION: Tap on "Gaming" icon.
        EXPECTED: * Gaming page is opened.
        EXPECTED: * Gaming icon is highlighted.
        """
        pass

    def test_002__tap_on_any_game_and_start_downloading_it_tap_on_homepage_icon(self):
        """
        DESCRIPTION: * Tap on any game and start downloading it.
        DESCRIPTION: * Tap on "Homepage" icon.
        EXPECTED: * Homeapge icon is opened.
        EXPECTED: * Homepage icon is hightlighted.
        EXPECTED: * Loading spinner is shown on "Gaming" icon.
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/120999553)
        EXPECTED: Dark mode:
        EXPECTED: ![](index.php?/attachments/get/120999554)
        EXPECTED: Ladrbokes:
        EXPECTED: ![](index.php?/attachments/get/120999555)
        EXPECTED: Dark mode:
        EXPECTED: ![](index.php?/attachments/get/120999556)
        """
        pass
