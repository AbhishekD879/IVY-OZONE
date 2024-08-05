import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C59049718_Verify_events_filtering_when_marketName_marketTemplateName(Common):
    """
    TR_ID: C59049718
    NAME: Verify events filtering when marketName != marketTemplateName
    DESCRIPTION: This test case verifies events filtering when marketName != marketTemplateName.
    PRECONDITIONS: **OB Configurations:**
    PRECONDITIONS: The event should contain the following settings:
    PRECONDITIONS: **OB Configurations:**
    PRECONDITIONS: - marketName != marketTemplateName (for example: marketName = |Some Market| and marketTemplateName = |Money Line|
    PRECONDITIONS: **CMS Configurations:**
    PRECONDITIONS: **Note:**
    PRECONDITIONS: - To verify events availability on 'In-Play' tab please navigate to Dev Tools > Network > WS > wss://inplay-publisher-dev0.coralsports.dev.cloud.ladbrokescoral.com/websocket/?EIO=3&transport=websocket
    PRECONDITIONS: - To verify events availability on 'In-Play' module please navigate to Dev Tools > Network > WS > wss://featured-sports-dev0.coralsports.dev.cloud.ladbrokescoral.com/websocket/?EIO=3&transport=websocket
    PRECONDITIONS: - To verify queries from Front-end to SiteServe for data availability checking for different tabs use the following instruction:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+get+data+from+Openbet+Site+Server
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to the Sport Landing page
    PRECONDITIONS: 3. Choose the 'Matches' tab
    """
    keep_browser_open = True

    def test_001___navigate_to_the_matches_tab__verify_displaying_of_the_event_when_marketname__markettemplatename(self):
        """
        DESCRIPTION: - Navigate to the 'Matches' tab.
        DESCRIPTION: - Verify displaying of the event when marketName != marketTemplateName
        EXPECTED: - Event is displayed on the page
        EXPECTED: - Selections from the Primary Market are displayed on the event card
        EXPECTED: - Event is received in <EventToOutcomeForClass> response from the SS
        """
        pass

    def test_002___navigate_to_the_matches_tab___in_play_module__verify_displaying_of_the_event_when_marketname__markettemplatename(self):
        """
        DESCRIPTION: - Navigate to the 'Matches' tab -> 'In-Play' module.
        DESCRIPTION: - Verify displaying of the event when marketName != marketTemplateName
        EXPECTED: - Event is displayed on the page
        EXPECTED: - Selections from the Primary Market are displayed on the event card
        EXPECTED: - Event is received in WS from 'featured-sports' MS
        """
        pass

    def test_003___navigate_to_the_competitions_tab__verify_displaying_of_the_event_when_marketname__markettemplatename(self):
        """
        DESCRIPTION: - Navigate to the 'Competitions' tab.
        DESCRIPTION: - Verify displaying of the event when marketName != marketTemplateName
        EXPECTED: - Event is displayed on the page
        EXPECTED: - Selections from the Primary Market are displayed on the event card
        EXPECTED: - Event is received in <EventToOutcomeForType> response from the SS
        """
        pass

    def test_004___navigate_to_the_coupons_tab__verify_displaying_of_the_event_when_marketname__markettemplatename(self):
        """
        DESCRIPTION: - Navigate to the 'Coupons' tab.
        DESCRIPTION: - Verify displaying of the event when marketName != marketTemplateName
        EXPECTED: - Event is displayed on the page
        EXPECTED: - Selections from the Primary Market are displayed on the event card
        EXPECTED: - Event is received in <Coupon> response from the SS
        """
        pass

    def test_005___navigate_to_the_in_play_tab__verify_displaying_of_the_event_when_marketname__markettemplatename(self):
        """
        DESCRIPTION: - Navigate to the 'In-Play' tab.
        DESCRIPTION: - Verify displaying of the event when marketName != marketTemplateName
        EXPECTED: - Event is displayed on the page
        EXPECTED: - Selections from the Primary Market are displayed on the event card
        EXPECTED: - Event is received in WS from 'inplay-publisher' MS
        """
        pass
