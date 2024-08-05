import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.navigation
@vtest
class Test_C1683269_Super_button_when_two_buttons_are_set_up_in_CMS(Common):
    """
    TR_ID: C1683269
    NAME: Super button when two buttons are set up in CMS
    DESCRIPTION: This test case verifies Super button when two buttons are set up in CMS
    PRECONDITIONS: * Two Super buttons should be added and enabled in CMS
    PRECONDITIONS: https://{domain}/sports-pages/homepage
    PRECONDITIONS: where domain may be
    PRECONDITIONS: coral-cms-dev1.symphony-solutions.eu - Local env
    PRECONDITIONS: coral-cms-dev0.symphony-solutions.eu - Develop
    PRECONDITIONS: * Two Super buttons should be set up to be shown on the same Home Tab, Sport/Race page and Big Competition
    PRECONDITIONS: * Big Competition should be added, set up in CMS
    PRECONDITIONS: * To check ordering open DevTools -> network tab -> XHR -> set 'mobile' filter -> select GET /cms/api/bma/initial-data/mobile request
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_go_to_home_tab_for_which_two_super_buttons_are_set_up(self):
        """
        DESCRIPTION: Go to Home tab for which two Super buttons are set up
        EXPECTED: The first valid Super button that received in **navigationPoints** array in GET response (see preconditions) is displayed in Oxygen app ONLY
        """
        pass

    def test_003_go_to_sportrace_for_which_two_super_buttons_are_set_up(self):
        """
        DESCRIPTION: Go to Sport/Race for which two Super buttons are set up
        EXPECTED: The first valid Super button that received in **navigationPoints** array in GET response (see preconditions) is displayed in Oxygen app ONLY
        """
        pass

    def test_004_go_to_big_competition_page_for_which_two_super_buttons_are_set_up(self):
        """
        DESCRIPTION: Go to Big Competition page for which two Super buttons are set up
        EXPECTED: The first valid Super button that received in **navigationPoints** array in GET response (see preconditions) is displayed in Oxygen app ONLY
        """
        pass
