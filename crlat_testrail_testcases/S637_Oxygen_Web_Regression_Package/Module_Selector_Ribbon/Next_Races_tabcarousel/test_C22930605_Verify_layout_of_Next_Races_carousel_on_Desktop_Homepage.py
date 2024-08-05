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
class Test_C22930605_Verify_layout_of_Next_Races_carousel_on_Desktop_Homepage(Common):
    """
    TR_ID: C22930605
    NAME: Verify layout of  'Next Races' carousel on Desktop Homepage
    DESCRIPTION: This test case verifies layout of 'Next Races' carousel on Desktop Homepage
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Scroll the homepage to 'Next Races' carousel
    PRECONDITIONS: 3. Recent events are available for the current day
    PRECONDITIONS: Note:
    PRECONDITIONS: 1) 'Next Races' is CMS configurable, please look at the https://ladbrokescoral.testrail.com/index.php?/cases/view/29371 test case where this process is described.
    PRECONDITIONS: 2) The number of events and selections are CMS configurable too. CMS -> system-configuration -> structure -> NextRaces.
    PRECONDITIONS: 3) If in CMS: Horse Racing (HR) Racing Data Hub toggle is turned on : System-configuration > RacingDataHub > isEnabledForHorseRacing = true than some data (Jockey Name, Trainer Name, Silks, Runner Number, Draw, Form) is received from Racing Data Hub in response:
    PRECONDITIONS: e.g. https://ld-prd1.api.datafabric.prod.aws.ladbrokescoral.com/v4/sportsbook-api/categories/21/events/228859733,228864955,228859734,228863900,228865712,228859736/content?locale=en-GB&api-key=LD755f5f6b195b4688969e7e976df86855
    PRECONDITIONS: else if System-configuration > RacingDataHub > isEnabledForHorseRacing = false than some data (Jockey Name, Trainer Name, Silks, Runner Number, Draw, Form) is received from 'racingFormEvent' section in SS response
    """
    keep_browser_open = True

    def test_001_verify_next_races_carousel_header(self):
        """
        DESCRIPTION: Verify 'Next Races' carousel Header
        EXPECTED: * 'Next Races' carousel Header is clickable and allows to expand/collapse carousel after clicking on it
        EXPECTED: * 'Next Races' carousel Header consists of:
        EXPECTED: * 'Next Races' title
        EXPECTED: * Expand/Collapse arrows (Expand arrow only for Ladbrokes)
        """
        pass

    def test_002_verify_event_cards_layout(self):
        """
        DESCRIPTION: Verify 'Event Cards' layout
        EXPECTED: * Event cards are displayed one by one into the horizontal carousel
        EXPECTED: * Event Card consists of:
        EXPECTED: * Header
        EXPECTED: * Subheader
        EXPECTED: * Event Card main body
        """
        pass

    def test_003_verify_event_card_header_layout(self):
        """
        DESCRIPTION: Verify 'Event Card' header layout
        EXPECTED: * Event Card header consists of:
        EXPECTED: * Event name in the next format: 'HH:MM typeName' e.g. '11:40 VAAL'
        EXPECTED: * 'More' link with chevron
        EXPECTED: * 'Going' status e.g. 'Good to Firm' (Ladbrokes only if available)
        EXPECTED: * 'Distance' value in the next format: XXm XXf XXy (Ladbrokes only if available)
        EXPECTED: * 'Countdown timer' in the next format: 'Starts in mm:ss'
        """
        pass

    def test_004_verify_event_card_subheader_layout_ladbrokes_only(self):
        """
        DESCRIPTION: Verify 'Event Card' subheader layout (Ladbrokes only)
        EXPECTED: * Event Card subheader consists of:
        EXPECTED: * 'Each Way' terms in the next format: e.g. E/W 1/5 Places 1-2-3 (if available)
        EXPECTED: * 'Signposting Promotion' icon (if available)
        EXPECTED: * 'WATCH' icon (if available)
        """
        pass

    def test_005_verify_event_card_body_layout(self):
        """
        DESCRIPTION: Verify 'Event Card' body layout
        EXPECTED: * Event Card body consists of:
        EXPECTED: * Runner Number
        EXPECTED: * Draw Number
        EXPECTED: * Silk
        EXPECTED: * Horse Name
        EXPECTED: * Jockey/Trainer Information
        EXPECTED: * Form information, e.g. 'Form: 761731' (for Ladbrokes only if available)
        EXPECTED: * 'Price/Odds' button
        EXPECTED: * Previous price
        """
        pass

    def test_006_verify_next_races_carousel_footer(self):
        """
        DESCRIPTION: Verify 'Next Races' carousel Footer
        EXPECTED: * 'Next Races' carousel Footer is clickable and redirects to 'Horse Racing' page after clicking on it
        EXPECTED: * 'Next Races' carousel Footer consists of:
        EXPECTED: * 'View all horse racing events' link with chevron
        """
        pass
