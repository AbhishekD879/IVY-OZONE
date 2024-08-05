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
class Test_C2492850_Verify_GA_tracking_on_cashouting_codes(Common):
    """
    TR_ID: C2492850
    NAME: Verify GA tracking on cashouting codes
    DESCRIPTION: jira tickets:
    DESCRIPTION: HMN-3676 - Web - Implement new Tags
    PRECONDITIONS: Request/generate cashoutable OTC & SSBT codes
    """
    keep_browser_open = True

    def test_001_load_connect_appconnect_device__via_chromeinspect__safarydevelop_review_calls_we_make_on_the_bettracker_page(self):
        """
        DESCRIPTION: Load Connect app.
        DESCRIPTION: Connect device & via Chrome://inspect || (Safary.develop) review calls we make on the Bettracker page
        EXPECTED: 
        """
        pass

    def test_002_on_the_bettracker_page_enter_valid_otc_cashoutable_code_for_game_in_progresstap_cash_out_buttonverify_chrome__console__datalayer(self):
        """
        DESCRIPTION: On the bettracker page enter
        DESCRIPTION: >> VALID OTC cashoutable code [for game in progress]
        DESCRIPTION: tap CASH OUT button
        DESCRIPTION: Verify Chrome > Console > dataLayer
        EXPECTED: Verify we send out:
        EXPECTED: betType: **"otc"**
        EXPECTED: betValue: **"£00.00"**[cashouted value]
        EXPECTED: event: "trackEvent"
        EXPECTED: eventAction: **"Request"**
        EXPECTED: eventCategory: **"Cash Out"**
        EXPECTED: eventLabel: "Full" || "Partial"
        EXPECTED: gtm.uniqueEventId: [int]
        """
        pass

    def test_003_tap_confirmon_cashout_succeededverify_chrome__console__datalayer(self):
        """
        DESCRIPTION: Tap CONFIRM
        DESCRIPTION: (on_cashout_succeeded)
        DESCRIPTION: Verify Chrome > Console > dataLayer
        EXPECTED: Verify we send out:
        EXPECTED: betType: **"otc"**
        EXPECTED: betValue: **"£00.00"**[cashouted value]
        EXPECTED: event: "trackEvent"
        EXPECTED: eventAction: **"Success"**
        EXPECTED: eventCategory: **"Cash Out"**
        EXPECTED: eventLabel: "Full" || "Partial"
        EXPECTED: gtm.uniqueEventId: [int]
        """
        pass

    def test_004_on_the_bettracker_page_enter_valid_otc_cashoutable_code_for_game_in_progresstap_cash_out_button__confirmsuspend_the_event_so_that_cashout_failsverify_chrome__console__datalayer(self):
        """
        DESCRIPTION: On the bettracker page enter
        DESCRIPTION: >> VALID OTC cashoutable code [for game in progress]
        DESCRIPTION: tap CASH OUT button & CONFIRM
        DESCRIPTION: **suspend the event so that Cashout FAILS**
        DESCRIPTION: Verify Chrome > Console > dataLayer
        EXPECTED: Verify we send out:
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'Cash Out',
        EXPECTED: 'eventAction' : 'Error',
        EXPECTED: 'eventLabel' : '<<ERROR MESSAGE>>' //The error message displayed to the user
        """
        pass

    def test_005_repeat_steps_2_3_for_ssbt_codes(self):
        """
        DESCRIPTION: Repeat Steps #2-3 for SSBT codes
        EXPECTED: Verify the same tags are sent out.
        EXPECTED: The only diff would be
        EXPECTED: betType: **"otc"** => betType: **"betstation"**
        """
        pass

    def test_006_verify_tags_are_tracked_in_gaevents_section__filter_by_eventcategory_or_other(self):
        """
        DESCRIPTION: Verify Tags are tracked in GA.
        DESCRIPTION: Events section > filter by eventCategory (or other)
        EXPECTED: NB: GA update takes up to 24h
        """
        pass
