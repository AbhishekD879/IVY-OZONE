import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.streaming
@vtest
class Test_C11779828_Launching_Stream_when_connection_is_lost(Common):
    """
    TR_ID: C11779828
    NAME: Launching Stream when connection is lost
    DESCRIPTION: This test case verifies launching Stream when the connection is lost
    PRECONDITIONS: 1. SiteServer event should be configured to support Perform streaming (**'typeFlagCodes'**='PVA , ... ' AND **'drilldownTagNames'**='EVFLAG_PVM' flags should be set) and should be mapped to Perform stream event
    PRECONDITIONS: 2. Event should have the following attributes:
    PRECONDITIONS: * isStarted = "true"
    PRECONDITIONS: * isMarketBetInRun = "true"
    PRECONDITIONS: 3. User should be logged in and have a bet placed on a selection from primary market within event that is higher or equal to 1 GBP.
    PRECONDITIONS: 4. Ukraine should be whitelisted by Perform
    PRECONDITIONS: * Endpoints of Optin MS:
    PRECONDITIONS: * https://optin-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/video/igame/{eventID} - dev0 Coral
    PRECONDITIONS: * https://optin-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com/api/video/igame/{eventID} - dev0 Ladbrokes
    PRECONDITIONS: * https://optin-tst0.coralsports.nonprod.cloud.ladbrokescoral.com/api/video/igame/{eventID} - tst2 Coral
    PRECONDITIONS: * https://optin-tst0.ladbrokesoxygen.prod.cloud.ladbrokescoral.com/video/igame/{eventID} - tst2 Ladbrokes
    PRECONDITIONS: * https://optin-prd0.coralsports.prod.cloud.ladbrokescoral.com/api/video/igame/{eventID} - prod Coral
    PRECONDITIONS: * https://optin-prd0.ladbrokesoxygen.prod.cloud.ladbrokescoral.com/video/igame/{eventID} - prod Ladbrokes
    PRECONDITIONS: * https://optin-hlv1.coralsports.nonprod.cloud.ladbrokescoral.com/api/video/igame/{eventID} - beta Coral
    """
    keep_browser_open = True

    def test_001_open_event_details_page_of_any_sportrace_for_the_event_with_perform_stream_mapped(self):
        """
        DESCRIPTION: Open Event Details page of any <Sport>/<Race> for the event with Perform stream mapped
        EXPECTED: * Event Details page is opened
        EXPECTED: * Stream button is present
        """
        pass

    def test_002_for_browser_desktoptabletmobile_responsive_viewstrigger_loss_of_internet_connection_and_clicktap_stream_button(self):
        """
        DESCRIPTION: For Browser (Desktop/Tablet/Mobile Responsive views):
        DESCRIPTION: Trigger loss of internet connection and click/tap Stream button
        EXPECTED: * Request to OptIn MS is NOT sent
        EXPECTED: * Stream is not launched
        EXPECTED: * App does not crash
        EXPECTED: Following message is shown below/above the clicked/tapped button:
        EXPECTED: **'Server is unavailable at the moment, please try again later.'**
        EXPECTED: -
        EXPECTED: Following pop-up appears after 15 seconds of internet connection loss:
        EXPECTED: *'NO INTERNET CONNECTION'*
        EXPECTED: *You are currently experiencing issues connecting to the internet. Please check your internet connection and try again.*
        """
        pass

    def test_003_for_mobile_apps_tabletmobiletrigger_loss_of_internet_connection_and_tap_stream_button(self):
        """
        DESCRIPTION: For Mobile Apps (Tablet/Mobile):
        DESCRIPTION: Trigger loss of internet connection and tap Stream button
        EXPECTED: Following pop-up appears as soon as internet connection is lost (**and can't be closed till internet connection is restored**):
        EXPECTED: *Poor network connection*
        EXPECTED: *Please check your connection settings*
        EXPECTED: -
        EXPECTED: * Request to OptIn MS is NOT sent
        EXPECTED: * Stream is not launched
        EXPECTED: * App does not crash
        """
        pass

    def test_004_repeat_steps_1_3_for_events_with_following_mapped_streams_providers_img_igamemedia_ruk_atr_rpgtv(self):
        """
        DESCRIPTION: Repeat steps #1-3 for events with following mapped streams (providers):
        DESCRIPTION: * IMG
        DESCRIPTION: * iGameMedia
        DESCRIPTION: * RUK
        DESCRIPTION: * ATR
        DESCRIPTION: * RPGTV
        EXPECTED: 
        """
        pass
