import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C65969140_Verify_Greyhounds_data_is_loading_in_the_Future_tab(Common):
    """
    TR_ID: C65969140
    NAME: Verify Greyhounds data is loading in the Future tab.
    DESCRIPTION: This test case verifies Greyhounds data loading in Future tab.
    PRECONDITIONS: Load the application.
    PRECONDITIONS: Navigate to the Greyhound landing page -&gt; Select 'FUTURE' tab.
    """
    keep_browser_open = True

    def test_001_load_the_ladbrokes_coral_application(self):
        """
        DESCRIPTION: Load the Ladbrokes/ Coral application.
        EXPECTED: The application should be loaded successfully.
        """
        pass

    def test_002_tap_greyhounds_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap Greyhounds icon from the Sports Menu Ribbon.
        EXPECTED: Greyhounds landing page is opened.
        """
        pass

    def test_003_tap_future_tab(self):
        """
        DESCRIPTION: Tap 'Future' tab.
        EXPECTED: 1.'Future' tab is opened.
        EXPECTED: 2.'By Meeting' sorting type is selected by default.
        """
        pass

    def test_004_verify_future_tab(self):
        """
        DESCRIPTION: Verify 'Future' tab.
        EXPECTED: 1.Two sorting types are present: 'By Meeting' and 'By Time'.
        EXPECTED: 2.Race Meeting sections are collapsed by default.
        """
        pass

    def test_005_check_data_which_is_displayed_in_future_tab(self):
        """
        DESCRIPTION: Check data which is displayed in 'Future' tab.
        EXPECTED: A list of all future's racing is displayed.
        EXPECTED: Data corresponds to the Site Server response.
        EXPECTED: Event start times correspond to day after tomorrow's date and further (see 'startTime' attribute).
        """
        pass
