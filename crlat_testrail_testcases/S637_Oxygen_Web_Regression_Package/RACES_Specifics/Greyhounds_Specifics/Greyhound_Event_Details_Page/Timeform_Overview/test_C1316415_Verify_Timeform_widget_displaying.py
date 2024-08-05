import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C1316415_Verify_Timeform_widget_displaying(Common):
    """
    TR_ID: C1316415
    NAME: Verify Timeform widget displaying
    DESCRIPTION: This test case verifies Timeform widget on Greyhounds Event Details page in Desktop mode
    PRECONDITIONS: update: After BMA-40744 implementation we'll use RDH feature toggle:
    PRECONDITIONS: Greyhounds (GH) Racing Data Hub toggle is turned on: System-configuration > RacingDataHub > isEnabledForGreyhound = true
    PRECONDITIONS: when enabled - TimeForm info will NOT be displayed.
    PRECONDITIONS: we'll receive needed data from DF api:
    PRECONDITIONS: Racing Data Hub link:
    PRECONDITIONS: Coral DEV : cd-dev1.api.datafabric.dev.aws.ladbrokescoral.com/v4/sportsbook-api/categories/{categoryKey}/events/{eventKey}/content?locale=en-GB&api-key={api-key}
    PRECONDITIONS: Ladbrokes DEV : https://ld-dev1.api.datafabric.dev.aws.ladbrokescoral.com/v4/sportsbook-api/categories/{categoryKey}/events/{eventKey}/content?locale=en-GB&api-key=LDaa2737afbeb24c3db274d412d00b6d3b
    PRECONDITIONS: URI : /v4/sportsbook-api/categories/{categoryKey}/events/{eventKey}/content?locale=en-GB&api-key={api-key}
    PRECONDITIONS: {categoryKey} : 21 - Horse racing, 19 - Greyhound
    PRECONDITIONS: {eventKey} : OB Event id
    PRECONDITIONS: -----
    """
    keep_browser_open = True

    def test_001_load_oxygen_app_in_desktop_mode_with_resolution_of_970px(self):
        """
        DESCRIPTION: Load Oxygen app in Desktop mode with resolution of 970px
        EXPECTED: Homepage is loaded
        """
        pass

    def test_002_go_to_the_greyhounds_landing_page(self):
        """
        DESCRIPTION: Go to the Greyhounds landing page
        EXPECTED: Greyhounds landing page is opened
        """
        pass

    def test_003_select_event_with_timeform_available_and_go_to_its_details_page(self):
        """
        DESCRIPTION: Select event with timeform available and go to its details page
        EXPECTED: * Event details page is opened
        EXPECTED: * Timeform widget is located in Main Column under selections list
        EXPECTED: * Timeform is expanded by default
        """
        pass

    def test_004_verify_timeform_widget(self):
        """
        DESCRIPTION: Verify Timeform widget
        EXPECTED: Timeworm consists of:
        EXPECTED: * 'Timeform' logo
        EXPECTED: * TFPick' label and name of dog
        EXPECTED: * Expandable / collapsible arrow
        EXPECTED: * Timeform summary
        EXPECTED: * Timeform Summary Information for 3 dogs
        """
        pass

    def test_005_verify_timeform_summary_information_for_each_dog(self):
        """
        DESCRIPTION: Verify Timeform Summary Information for each dog
        EXPECTED: Timeform Summary Information for each dog consists of:
        EXPECTED: * Dog image
        EXPECTED: * Name of dog
        EXPECTED: * 'Trainer' label and name of trainer
        EXPECTED: * 'Rating' label and Stars rating
        """
        pass

    def test_006_verify_expandablecollapsible_arrow(self):
        """
        DESCRIPTION: Verify expandable/collapsible arrow
        EXPECTED: It's possible to expand/collapse Timeform widget by clicking on the arrow
        """
        pass

    def test_007_change_resolution_from_970px_to_1025px(self):
        """
        DESCRIPTION: Change resolution from 970px to 1025px
        EXPECTED: Timeform widget stays located in Main Column under selections list
        """
        pass

    def test_008_change_resolution_from_1025px_to_1280px(self):
        """
        DESCRIPTION: Change resolution from 1025px to 1280px
        EXPECTED: Timeform widget is located in the Third Column below Event Ribbon
        """
        pass

    def test_009_change_resolution_from_1280px_to_1600px(self):
        """
        DESCRIPTION: Change resolution from 1280px to 1600px
        EXPECTED: Timeform widget stays located in the Third Column below Event Ribbon
        """
        pass

    def test_010_verify_timeform_widget_when_no_data_is_returned_from_timeform_microservice_response(self):
        """
        DESCRIPTION: Verify Timeform widget when no data is returned from Timeform microservice response
        EXPECTED: Timeform widget is NOT displayed
        """
        pass
