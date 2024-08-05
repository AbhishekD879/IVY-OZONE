import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.retail
@vtest
class Test_C2765439_Verify_retrieving_Scoreboard_info_for_in_play_events(Common):
    """
    TR_ID: C2765439
    NAME: Verify retrieving Scoreboard info for in-play events
    DESCRIPTION: This test case verify retrieving Scoreboard info for in-play events
    PRECONDITIONS: * Request creation of SSBT bet
    PRECONDITIONS: * Information about score and other match incidents is available while game is in play and 30 min after game is finished
    PRECONDITIONS: Use [DX postman collection](https://confluence.egalacoral.com/download/attachments/53838690/DX.postman_collection.json?version=1&modificationDate=1509720767000&api=v2) to get SSBT betslips data from DX service (turn on VPN)
    PRECONDITIONS: Open following requests:
    PRECONDITIONS: [GET /rcomb/v2/barcode](https://coral-retail-bpp-dev.symphony-solutions.eu/swagger-ui.html#!/rcomb_endpoints/getBetsBySlipAndBarcodeUsingGET)
    PRECONDITIONS: [GET /rcomb/v2/barcodes](https://coral-retail-bpp-dev.symphony-solutions.eu/swagger-ui.html#!/rcomb_endpoints/getBetsBySlipAndBarcodesUsingGET)
    """
    keep_browser_open = True

    def test_001__run_getfootballscoreboard_request_from_dx_postman_collectionset_into__sportsbookeventkey_event_id_from_your_test_coupon_ssbt_event_keymake_sure_your_test_event_is_in_play(self):
        """
        DESCRIPTION: * Run 'getfootballscoreboard' request from 'DX postman collection'
        DESCRIPTION: (set into  <sportsbookEventKey> Event id from your test coupon ("SSBT_EVENT_KEY"))
        DESCRIPTION: *Make sure your test event is in play*
        EXPECTED: Scoreboard data are retrieved correctly
        """
        pass

    def test_002_run_get_rcombv2barcodehttpscoral_retail_bpp_devsymphony_solutionseuswagger_uihtmlrcomb_endpointsgetbetsbyslipandbarcodeusingget_using_barcode_without_letter_b_as_parameter(self):
        """
        DESCRIPTION: Run [GET /rcomb/v2/barcode](https://coral-retail-bpp-dev.symphony-solutions.eu/swagger-ui.html#!/rcomb_endpoints/getBetsBySlipAndBarcodeUsingGET) using Barcode (without letter 'B') as parameter
        EXPECTED: Response with bets information is received
        """
        pass

    def test_003_verify_bet___leg___sportsleg___legpart___eventperiod_data(self):
        """
        DESCRIPTION: Verify (bet -> leg -> sportsLeg -> legPart ->) "eventPeriod" data
        EXPECTED: * "eventPeriod" contains data while game is in play and 30 min afterward
        EXPECTED: * General information about each events period
        EXPECTED: * All events incidents (score, cards etc ...) are listed  for each events period separately in the same sequence they have occurred
        """
        pass

    def test_004_verify_events_incidents_data_correspond_to_data_received_from_dx_service(self):
        """
        DESCRIPTION: Verify events incidents data correspond to data received from DX service
        EXPECTED: * 'eventParticipantId' contain 0 (Home) if incident is taken from <footballTeam1> tag and 1 (Away) if it's from <footballTeam2>
        EXPECTED: * 'incidentCode' and 'description' correspond to  <statistic>/<statisticType> tag
        EXPECTED: * Incident is assigned to the correct match halt <--  data are taken from tag <statistic>/<firstHalf> or <secondHalf> (tag contains quantity of incidents of particular type)
        EXPECTED: * 'relativeTime' (represented in seconds) is taken from <statistic>/<firstHalfTime> or <secondHalfTime> (could contains several, coma separated, values if there were several similar incidents during one event period (the last one goes first))
        """
        pass

    def test_005_verify_bet___leg___sportsleg___legpart___eventparticipants_data(self):
        """
        DESCRIPTION: Verify (bet -> leg -> sportsLeg -> legPart ->) "eventParticipants" data
        EXPECTED: * Participant id, name, role, score are displayed correctly for each participant separately (data are derived in the same way as in previous step)
        EXPECTED: * During match and 30 min afterward data are taken using 'getfootballscoreboard' request
        EXPECTED: * Afterward final score is taken using 'BetSlipTracker' request, score is taken from Even Name (<leg>/<part>/<partSelection>/ <eventName>0:2 HOME TEAM - AWAY TEAM</eventName>)
        EXPECTED: * "eventParticipants" data should be available at least 1 day after game (after that they are not sent from DX)
        """
        pass
