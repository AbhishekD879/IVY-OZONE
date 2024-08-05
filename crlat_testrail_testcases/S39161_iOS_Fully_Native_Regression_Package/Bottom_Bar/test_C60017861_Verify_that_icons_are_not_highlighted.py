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
class Test_C60017861_Verify_that_icons_are_not_highlighted(Common):
    """
    TR_ID: C60017861
    NAME: Verify that icons are not highlighted
    DESCRIPTION: This test case verifies that when user is not on the following pages: "Homepage, In-Play Page, My Bets, Account or Gaming"
    PRECONDITIONS: * Coral/Ladbrokes app is installed and launched
    PRECONDITIONS: Designs:
    PRECONDITIONS: Coral:
    PRECONDITIONS: https://app.zeplin.io/project/5db9a772249ee083943f7259/dashboard?seid=5dd26b3cd37ceb668c203655
    PRECONDITIONS: Ladbrokes:
    PRECONDITIONS: https://app.zeplin.io/project/5db9a6d44a45be834b98748a/dashboard?seid=5dce7ecbf6b7d53c087f3eb4
    """
    keep_browser_open = True

    def test_001_go_to_any_sports_page_ex_football(self):
        """
        DESCRIPTION: Go to any Sports page (e.x Football)
        EXPECTED: No icons are highlighted in the Bottom Bar.
        """
        pass
