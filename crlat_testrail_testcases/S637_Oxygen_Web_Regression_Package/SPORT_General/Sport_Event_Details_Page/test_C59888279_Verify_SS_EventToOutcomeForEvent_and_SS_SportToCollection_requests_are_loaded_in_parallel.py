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
class Test_C59888279_Verify_SS_EventToOutcomeForEvent_and_SS_SportToCollection_requests_are_loaded_in_parallel(Common):
    """
    TR_ID: C59888279
    NAME: Verify SS EventToOutcomeForEvent and SS SportToCollection requests are loaded in parallel
    DESCRIPTION: This test case verifies that SS EventToOutcomeForEvent and SS SportToCollection requests are loaded in parallel after navigation to EDP.
    DESCRIPTION: NOTE: before implementation of https://jira.egalacoral.com/browse/BMA-55035 SS SportToCollection request was made after response from SS EventToOutcomeForEvent, but after BMA-55035 these two requests are made in parallel to optimize page loading time.
    PRECONDITIONS: 1. Login to Oxygen application under User with positive balance
    PRECONDITIONS: 2. Find any Event and place 3 different bets within same Event
    PRECONDITIONS: 3. Make full cashout of one of the Bets from Step 2.
    PRECONDITIONS: 4. Open browser Dev Tools -> Network tab
    PRECONDITIONS: 3. Navigate to any Event Details Page from Step 2.
    """
    keep_browser_open = True

    def test_001_check_browser_network_tab_and_verify_following_requests__eventtooutcomeforevent__sporttocollection__edp_markets_cms_request__yc_leagues_cms_request__getbetsplacedeventideventid__getbetdetailscashoutbets__getbetdetailreturnpartialcashoutdetails(self):
        """
        DESCRIPTION: Check browser Network tab and verify following requests:
        DESCRIPTION: - EventToOutcomeForEvent
        DESCRIPTION: - SportToCollection
        DESCRIPTION: - /edp-markets CMS request
        DESCRIPTION: - /yc-leagues CMS request
        DESCRIPTION: - /getBetsPlaced?eventId={eventId}
        DESCRIPTION: - /getBetDetails?cashoutBets
        DESCRIPTION: - /getBetDetail?returnPartialCashoutDetails
        EXPECTED: * Page is refreshed
        EXPECTED: * EventToOutcomeForEvent request is loaded and valid data is received
        EXPECTED: * SportToCollection request is is loaded and valid data is received
        EXPECTED: * EDP is loaded and displayed with valid information
        EXPECTED: * /edp-markets CMS request is loaded with and valid information is received
        EXPECTED: * /yc-leagues CMS request is loaded with and valid information is received
        EXPECTED: **Coral only**
        EXPECTED: * /getBetsPlaced?eventId={eventId} BPP request is loaded with and valid information is received
        EXPECTED: * /getBetDetails?cashoutBets and /getBetDetail?returnPartialCashoutDetails BPP requests are loaded and valid data is received
        """
        pass

    def test_002_block_eventtooutcomeforevent_request_urleg_httpbackoffice_tst2coralcoukopenbet_ssviewerdrilldownxxxeventtooutcomeforevent_on_browser_request_blocking_tabindexphpattachmentsget118653672(self):
        """
        DESCRIPTION: Block EventToOutcomeForEvent request url
        DESCRIPTION: (e.g. http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/) on browser request blocking tab
        DESCRIPTION: ![](index.php?/attachments/get/118653672)
        EXPECTED: 
        """
        pass

    def test_003_refresh_the_page_and_verify_following_requests__eventtooutcomeforevent__sporttocollection__edp_markets_cms_request__yc_leagues_cms_request__getbetsplacedeventideventid__getbetdetailscashoutbets__getbetdetailreturnpartialcashoutdetails__initial_datadesktopmobile(self):
        """
        DESCRIPTION: Refresh the page and verify following requests:
        DESCRIPTION: - EventToOutcomeForEvent
        DESCRIPTION: - SportToCollection
        DESCRIPTION: - /edp-markets CMS request
        DESCRIPTION: - /yc-leagues CMS request
        DESCRIPTION: - /getBetsPlaced?eventId={eventId}
        DESCRIPTION: - /getBetDetails?cashoutBets
        DESCRIPTION: - /getBetDetail?returnPartialCashoutDetails
        DESCRIPTION: - /initial-data/{desktop/mobile}
        EXPECTED: * EventToOutcomeForEvent request is failed
        EXPECTED: * SportToCollection request is loaded and valid data is received
        EXPECTED: * "Oops! We are having trouble loading this page. Please check your connection" message and 'Try Again' buttons are displayed
        EXPECTED: ![](index.php?/attachments/get/118653673)
        EXPECTED: * /edp-markets CMS request is loaded with and valid information is received
        EXPECTED: * /yc-leagues CMS request is loaded with and valid information is received
        EXPECTED: * /initial-data/{desktop/mobile} CMS request is loaded with and valid information is received
        EXPECTED: **Coral only**
        EXPECTED: * /getBetsPlaced?eventId={eventId} BPP request is loaded with and valid information is received
        EXPECTED: * /getBetDetails?cashoutBets and /getBetDetail?returnPartialCashoutDetails BPP requests are loaded and valid data is received
        """
        pass

    def test_004_unblock_eventtooutcomeforevent_request_url_and_block_sporttocollection_request_urlhttpbackoffice_tst2coralcoukopenbet_ssviewerdrilldownxxxsporttocollection_browser_dev_tools(self):
        """
        DESCRIPTION: Unblock EventToOutcomeForEvent request url and block SportToCollection request url(http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/SportToCollection) browser Dev tools
        EXPECTED: 
        """
        pass

    def test_005_press_try_again_button_and_verify_following_requests__eventtooutcomeforevent__sporttocollection__edp_markets_cms_request__yc_leagues_cms_request__getbetsplacedeventideventid__getbetdetailscashoutbets__getbetdetailreturnpartialcashoutdetails(self):
        """
        DESCRIPTION: Press 'Try Again' button and verify following requests:
        DESCRIPTION: - EventToOutcomeForEvent
        DESCRIPTION: - SportToCollection
        DESCRIPTION: - /edp-markets CMS request
        DESCRIPTION: - /yc-leagues CMS request
        DESCRIPTION: - /getBetsPlaced?eventId={eventId}
        DESCRIPTION: - /getBetDetails?cashoutBets
        DESCRIPTION: - /getBetDetail?returnPartialCashoutDetails
        EXPECTED: * Page is refreshed
        EXPECTED: * EventToOutcomeForEvent request is loaded and valid data is received
        EXPECTED: * SportToCollection request is failed
        EXPECTED: * "Oops! We are having trouble loading this page. Please check your connection" message and 'Try Again' buttons are displayed
        EXPECTED: * /edp-markets CMS request is loaded with and valid information is received
        EXPECTED: * /yc-leagues CMS request is loaded with and valid information is received
        EXPECTED: **Coral only**
        EXPECTED: * /getBetsPlaced?eventId={eventId} BPP request is loaded with and valid information is received
        EXPECTED: * /getBetDetails?cashoutBets and /getBetDetail?returnPartialCashoutDetails BPP requests are loaded and valid data is received
        """
        pass

    def test_006_log_out_unblock_all_requests_refresh_the_page_and_verify_following_requests__eventtooutcomeforevent__sporttocollection__edp_markets_cms_request__yc_leagues_cms_request__getbetsplacedeventideventid__getbetdetailscashoutbets__getbetdetailreturnpartialcashoutdetails__initial_datadesktopmobile(self):
        """
        DESCRIPTION: Log out. Unblock all requests, refresh the page and verify following requests:
        DESCRIPTION: - EventToOutcomeForEvent
        DESCRIPTION: - SportToCollection
        DESCRIPTION: - /edp-markets CMS request
        DESCRIPTION: - /yc-leagues CMS request
        DESCRIPTION: - /getBetsPlaced?eventId={eventId}
        DESCRIPTION: - /getBetDetails?cashoutBets
        DESCRIPTION: - /getBetDetail?returnPartialCashoutDetails
        DESCRIPTION: - /initial-data/{desktop/mobile}
        EXPECTED: * Page is refreshed
        EXPECTED: * EventToOutcomeForEvent request is loaded and valid data is received
        EXPECTED: * SportToCollection request is loaded and valid data is received
        EXPECTED: * /edp-markets CMS request is loaded with and valid information is received
        EXPECTED: * /yc-leagues CMS request is loaded with and valid information is received
        EXPECTED: * /initial-data/{desktop/mobile} CMS request is loaded with and valid information is received
        EXPECTED: **Coral only**
        EXPECTED: * /getBetsPlaced?eventId={eventId} BPP request is NOT loaded resent in Network
        EXPECTED: * /getBetDetails?cashoutBets and /getBetDetail?returnPartialCashoutDetails are NOT present in Network
        """
        pass
