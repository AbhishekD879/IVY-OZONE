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
class Test_C2492849_Verify_GA_tracking_on_adding_codes(Common):
    """
    TR_ID: C2492849
    NAME: Verify GA tracking on adding codes
    DESCRIPTION: jira tickets:
    DESCRIPTION: HMN-3676 - Web - Implement new Tags
    PRECONDITIONS: Request/generate cashoutable OTC & SSBT codes
    PRECONDITIONS: 1. Load SportBook
    PRECONDITIONS: 2. Go to Connect via header ribbon
    PRECONDITIONS: 3. Tap 'Shop Bet Tracker'
    """
    keep_browser_open = True

    def test_001_on_the_bettracker_page_manually_enter_valid_otc_codeverify_chrome__console__datalayer(self):
        """
        DESCRIPTION: On the bettracker page MANUALLY enter
        DESCRIPTION: >> VALID OTC code
        DESCRIPTION: Verify Chrome > Console > dataLayer
        EXPECTED: Verify we send out:
        EXPECTED: betType: **"otc"**
        EXPECTED: event: "trackEvent"
        EXPECTED: eventAction: "Success"
        EXPECTED: eventCategory: "Track Bet"
        EXPECTED: eventLabel: "XXX-XXXX"
        EXPECTED: gtm.uniqueEventId: [int]
        EXPECTED: method: **"manual input"**
        """
        pass

    def test_002_only_for_native_appon_the_bettracker_page_scan_valid_otc_codeverify_chrome__console__datalayer(self):
        """
        DESCRIPTION: (only for Native App)
        DESCRIPTION: On the bettracker page SCAN
        DESCRIPTION: >> VALID OTC code
        DESCRIPTION: Verify Chrome > Console > dataLayer
        EXPECTED: Verify we send out:
        EXPECTED: betType: **"otc"**
        EXPECTED: event: "trackEvent"
        EXPECTED: eventAction: "Success"
        EXPECTED: eventCategory: "Track Bet"
        EXPECTED: eventLabel: "XXX-XXXX"
        EXPECTED: gtm.uniqueEventId: [int]
        EXPECTED: method: **"scanner"**
        """
        pass

    def test_003_on_the_bettracker_page_manually_enter__scan_here_method_is_ignored_invalid_otc_codeverify_chrome__console__datalayer(self):
        """
        DESCRIPTION: On the bettracker page MANUALLY enter / SCAN (here method is ignored)
        DESCRIPTION: >> INVALID OTC code
        DESCRIPTION: Verify Chrome > Console > dataLayer
        EXPECTED: Verify we send out:
        EXPECTED: betType: **"otc"**
        EXPECTED: event: "trackEvent"
        EXPECTED: eventAction: **"Error"**
        EXPECTED: eventCategory: "Track Bet"
        EXPECTED: eventLabel: **"The coupon code/number entered is incorrect.. OR other message that we show to user"**
        EXPECTED: gtm.uniqueEventId: [int]
        """
        pass

    def test_004_on_the_bettracker_page_manually_enter_valid_ssbt_codeverify_chrome__console__datalayer(self):
        """
        DESCRIPTION: On the bettracker page MANUALLY enter
        DESCRIPTION: >> VALID SSBT code
        DESCRIPTION: Verify Chrome > Console > dataLayer
        EXPECTED: Verify we send out:
        EXPECTED: betType: **"betstation"**
        EXPECTED: event: "trackEvent"
        EXPECTED: eventAction: "Success"
        EXPECTED: eventCategory: "Track Bet"
        EXPECTED: eventLabel: "1234567890123"
        EXPECTED: gtm.uniqueEventId: [int]
        EXPECTED: method: **"manual input"**
        """
        pass

    def test_005_only_for_native_appon_the_bettracker_page_scan_valid_ssbt_codeverify_chrome__console__datalayer(self):
        """
        DESCRIPTION: (only for Native App)
        DESCRIPTION: On the bettracker page SCAN
        DESCRIPTION: >> VALID SSBT code
        DESCRIPTION: Verify Chrome > Console > dataLayer
        EXPECTED: Verify we send out:
        EXPECTED: betType: **"betstation"**
        EXPECTED: event: "trackEvent"
        EXPECTED: eventAction: "Success"
        EXPECTED: eventCategory: "Track Bet"
        EXPECTED: eventLabel: "1234567890123"
        EXPECTED: gtm.uniqueEventId: [int]
        EXPECTED: method: **"scanner"**
        """
        pass

    def test_006_on_the_bettracker_page_manually_enter__scan_here_method_is_ignored_invalid_otc_codeverify_chrome__console__datalayer(self):
        """
        DESCRIPTION: On the bettracker page MANUALLY enter / SCAN (here method is ignored)
        DESCRIPTION: >> INVALID OTC code
        DESCRIPTION: Verify Chrome > Console > dataLayer
        EXPECTED: Verify we send out:
        EXPECTED: betType: **"betstation"**
        EXPECTED: event: "trackEvent"
        EXPECTED: eventAction: **"Error"**
        EXPECTED: eventCategory: "Track Bet"
        EXPECTED: eventLabel: **"The coupon code/number entered is incorrect.. OR other message that we show to user"**
        EXPECTED: gtm.uniqueEventId: [int]
        """
        pass

    def test_007_on_the_bettracker_page_delete_any_coupon_codeverify_chrome__console__datalayer(self):
        """
        DESCRIPTION: On the bettracker page delete any Coupon Code
        DESCRIPTION: Verify Chrome > Console > dataLayer
        EXPECTED: Verify we send out:
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'Bet View',
        EXPECTED: 'eventAction' : 'Remove'
        """
        pass

    def test_008_verify_tags_are_tracked_in_gaevents_section__filter_by_eventcategory_or_other(self):
        """
        DESCRIPTION: Verify Tags are tracked in GA.
        DESCRIPTION: Events section > filter by eventCategory (or other)
        EXPECTED: NB: GA update takes up to 24h
        """
        pass
