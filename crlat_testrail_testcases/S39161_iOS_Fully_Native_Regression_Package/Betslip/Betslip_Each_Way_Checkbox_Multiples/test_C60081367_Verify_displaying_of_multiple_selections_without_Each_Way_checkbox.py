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
class Test_C60081367_Verify_displaying_of_multiple_selections_without_Each_Way_checkbox(Common):
    """
    TR_ID: C60081367
    NAME: Verify displaying of multiple selections without "Each Way" checkbox
    DESCRIPTION: This test case verifies displaying of multiple selections without "Each Way" checkbox
    PRECONDITIONS: Light Theme is enabled on tested device (Setting -> Display & Brightness -> Select "Light" theme)
    PRECONDITIONS: Install native app
    PRECONDITIONS: Open the app
    PRECONDITIONS: User is on Home page
    PRECONDITIONS: Betslip is empty
    PRECONDITIONS: Ladbrokes https://app.zeplin.io/project/5dc1abb838e1dd72b89d1a21/screen/5ea98b5819ca0523e33bb464
    PRECONDITIONS: Coral https://app.zeplin.io/project/5dc1abe9fefe5d837a9b93cd/screen/5dc2a5d581baec82fe5baa11
    """
    keep_browser_open = True

    def test_001__select_a_few_selections_of_the_event_where_each_way_option_is_not_available_eg_events_from_horse_racinggreyhounds_etc_expand_the_betlslip(self):
        """
        DESCRIPTION: * Select a few selections of the event where "Each Way" option is not available (e.g. Events from Horse Racing,Greyhounds etc.).
        DESCRIPTION: * Expand the betlslip.
        EXPECTED: * Betslip is expanded.
        EXPECTED: * Selections don't have the "Each Way" checkbox below the stake field.
        """
        pass

    def test_002_enable_dark_theme_on_device(self):
        """
        DESCRIPTION: Enable "Dark" theme on device
        EXPECTED: * "Dark" theme on the device is enabled
        EXPECTED: * Betslip remains expanded with the current selection
        EXPECTED: * "Each Way" checkbox is not displayed below the "Stake" field
        """
        pass
