import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C2989897_Verify_New_Relic_script_is_present_on_build(Common):
    """
    TR_ID: C2989897
    NAME: Verify New Relic script is present on build
    DESCRIPTION: This test case verifies whether NewRelic is integrated with the application
    PRECONDITIONS: Browser console is opened
    PRECONDITIONS: In CMS make sure 'newRelic' group>'interceptAjax' is enabled in System Configuration
    """
    keep_browser_open = True

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_type_in_browser_console_newrelicevents___and_tap_enter_go_to_some_page_and_type_in_console_newrelicevents(self):
        """
        DESCRIPTION: Type in browser console "newRelicEvents = {}" and tap 'Enter', go to some page and type in console 'newRelicEvents'
        EXPECTED: New Relic object is shown in console output
        """
        pass
