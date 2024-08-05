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
class Test_C64749890_Verify_ShowMore_check_for_Win_EWTop_finishto_finish_etc_tabs_also(Common):
    """
    TR_ID: C64749890
    NAME: Verify ShowMore (check for Win /EW,Top finish,to finish etc tabs also)
    DESCRIPTION: This testcase verifies ShowMore
    DESCRIPTION: feature
    PRECONDITIONS: User should have CMS access
    PRECONDITIONS: Greyhounds (GH) Racing Data Hub toggle is turned on: System-configuration > RacingDataHub > isEnabledForGreyhound = true
    PRECONDITIONS: when enabled - Racingpost info should be displayed.
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is loaded
        """
        pass

    def test_002_go_to_the_greyhounds_landing_page(self):
        """
        DESCRIPTION: Go to the Greyhounds landing page
        EXPECTED: Greyhounds landing page is opened
        """
        pass

    def test_003_select_event_with_raingpost_available_and_go_to_its_details_page(self):
        """
        DESCRIPTION: Select event with RaingPost available and go to its details page
        EXPECTED: Event details page is opened
        EXPECTED: * 'Win or E/W' market is selected by default
        """
        pass

    def test_004_go_to_selection_area_and_verify_for_the_description_of_the_eventverify_show_more_optionverify_show_less_option(self):
        """
        DESCRIPTION: Go to selection area and verify for the description of the event
        DESCRIPTION: *Verify 'Show More' option
        DESCRIPTION: *Verify 'Show Less' option
        EXPECTED: 4.'Show More' option is displayed
        EXPECTED: * 'Show More' option becomes 'Show Less' after tapping it
        EXPECTED: * All RacingPost Selection Summary is displayed after tapping 'Show More' option
        EXPECTED: * 'Show Less' option becomes 'Show More' after tapping it
        EXPECTED: * Part of RacingPost Selection Summary is collapsed after tapping 'Show Less' option
        """
        pass
