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
class Test_C60017862_Verify_that_Bottom_Bar_sticks_to_the_bottom_of_the_page_when_user_navigates_around_the_map(Common):
    """
    TR_ID: C60017862
    NAME: Verify that "Bottom Bar"  sticks to the bottom of the page when user navigates around the map
    DESCRIPTION: This test case verifies that "Bottom Bar"  sticks to the bottom of the page when user navigates around the map
    PRECONDITIONS: * Coral/Ladbrokes app is installed and launched
    PRECONDITIONS: Designs:
    PRECONDITIONS: Coral:
    PRECONDITIONS: https://app.zeplin.io/project/5db9a772249ee083943f7259/dashboard?seid=5dd26b3cd37ceb668c203655
    PRECONDITIONS: Ladbrokes:
    PRECONDITIONS: https://app.zeplin.io/project/5db9a6d44a45be834b98748a/dashboard?seid=5dce7ecbf6b7d53c087f3eb4
    """
    keep_browser_open = True

    def test_001_tap_on_in_play_icon(self):
        """
        DESCRIPTION: Tap on "In-play" icon.
        EXPECTED: * User is redirected to the In-play page.
        EXPECTED: * Bottom bar sticks to the bottom of the page.
        """
        pass

    def test_002_select_any_match(self):
        """
        DESCRIPTION: Select any match.
        EXPECTED: * User is redirected to the selected match.
        EXPECTED: * Bottom bar sticks to the bottom of the page.
        """
        pass
