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
class Test_C2765435_Verify_data_retrieving_for_EPOS2_barcodes(Common):
    """
    TR_ID: C2765435
    NAME: Verify data retrieving for EPOS2 barcodes
    DESCRIPTION: 
    PRECONDITIONS: Use postman collection EPOS2 for checking data sent from backend
    PRECONDITIONS: (collection is attached)
    PRECONDITIONS: Use https://coral-retail-bpp-dev.symphony-solutions.eu/swagger-ui.html#!/ to check correctness of PROXY responses
    """
    keep_browser_open = True

    def test_001__open_postrcombv3connect_submit_valid_epos2_barcode(self):
        """
        DESCRIPTION: * Open POST/rcomb/v3/connect
        DESCRIPTION: * Submit valid EPOS2 barcode
        EXPECTED: Data are retrieved correctly
        """
        pass

    def test_002__in_postman_run_request_get_betslip_by_receipt_with_barcode_number_as_parameter_compare_received_data_with_postrcombv3connect_response(self):
        """
        DESCRIPTION: * In Postman run request 'Get betslip by receipt' with barcode number as parameter
        DESCRIPTION: * Compare received data with 'POST/rcomb/v3/connect' response
        EXPECTED: 'POST/rcomb/v3/connect' response returns following parameters that correspond to 'Get betslip by receipt'  response:
        EXPECTED: * epos2EventId
        EXPECTED: * eventName
        EXPECTED: * marketId
        EXPECTED: * marketName
        EXPECTED: * outcomeName
        EXPECTED: * priceDen
        EXPECTED: * priceNum
        EXPECTED: * startTime
        EXPECTED: * stake
        EXPECTED: * payout
        EXPECTED: * betid
        """
        pass

    def test_003__in_postman_run_request_get_events_by_betid_with_betid_as_parameter_compare_received_data_with_postrcombv3connect_response(self):
        """
        DESCRIPTION: * In Postman run request 'Get Events By betId' with betid as parameter
        DESCRIPTION: * Compare received data with 'POST/rcomb/v3/connect' response
        EXPECTED: 'POST/rcomb/v3/connect' response returns following parameters that correspond to 'Get Events By betId'  response:
        EXPECTED: * eventTypeName
        EXPECTED: * currency
        EXPECTED: * stake
        EXPECTED: * isSettled
        EXPECTED: * settleDate
        EXPECTED: * payout
        EXPECTED: * potentialPayout
        EXPECTED: * cashoutValue (status, reason, amount)
        """
        pass

    def test_004__in_postman_run_request_get_amelco_event_id_by_df_event_id_with_dfevent_id_as_parameter_which_you_can_find_in__get_betslip_by_receipt__response(self):
        """
        DESCRIPTION: * In Postman run request 'Get Amelco event id by DF event id' with DFevent_id as parameter (which you can find in  'Get betslip by receipt'  response)
        EXPECTED: Amelco event id is returned in response correctly:
        EXPECTED: "externalEventReference": "Openbet Feed Format.OPENBET_FEED:EVENT:XXXXXXXX"
        EXPECTED: where XXXXXXXX is Amelco event id
        """
        pass

    def test_005_call_openbet_siteserver_using_amelco_event_idto_get_openbet_event_id_and_all_info_about_events_markets_outcomes_priceshttpbackoffice_tst2coralcoukopenbet_ssviewerdrilldown226eventtooutcomeforeventext_openbet20feed20formatopenbet_feedeventxxxxxxxxtranslationlangenincludeundisplayedtruewhere_xxxxxxxx_is_amelco_event_id(self):
        """
        DESCRIPTION: Call OpenBet SiteServer using Amelco event id
        DESCRIPTION: to get OpenBet event id (and all info about events markets, outcomes, prices):
        DESCRIPTION: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/2.26/EventToOutcomeForEvent/~ext-Openbet%20Feed%20Format.OPENBET_FEED:EVENT:XXXXXXXX?translationLang=en&includeUndisplayed=true
        DESCRIPTION: where XXXXXXXX is Amelco event id
        EXPECTED: Data are retrieved correctly, including OpenBet event_id
        """
        pass

    def test_006_call_openbet_siteserver_using_openbet_event_id__to_get_events_commentaryhttpbackoffice_tst2coralcoukopenbet_ssviewercommentary226commentaryforeventxxxxxxxincludeundisplayedtruewhere_xxxxxxx_is_openbet_event_id(self):
        """
        DESCRIPTION: Call OpenBet SiteServer using OpenBet event_id  to get events Commentary:
        DESCRIPTION: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Commentary/2.26/CommentaryForEvent/XXXXXXX?includeUndisplayed=true
        DESCRIPTION: where XXXXXXX is OpenBet event_id
        EXPECTED: Data are retrieved correctly: events period, score, cards, etc
        """
        pass

    def test_007__make_sure_at_least_on_event_on_submitted_barcode_is_in_play_compare_data_received_in_previous_step_with_postrcombv3connect_response(self):
        """
        DESCRIPTION: * Make sure at least on event on submitted barcode is in-play
        DESCRIPTION: * Compare data received in previous step with 'POST/rcomb/v3/connect' response
        EXPECTED: Data in section eventPeriod correspond to SiteServe Commentary
        """
        pass
