import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.promotions_banners_offers
@vtest
class Test_C3233956_Ladbrokes_Promotion_pop_up_for_Races(Common):
    """
    TR_ID: C3233956
    NAME: [Ladbrokes] Promotion pop-up for <Races>
    DESCRIPTION: This test case verifies promotion pop-up for <Races>
    PRECONDITIONS: - You should have <Race> events with each promotion from the list on market level:
    PRECONDITIONS: 1) Faller’s Insurance (available ONLY for Horse Racing)
    PRECONDITIONS: 2) Beaten by a Length (available for Horse Racing AND Greyhounds)
    PRECONDITIONS: 3) Extra Place Race (available ONLY for Horse Racing)
    PRECONDITIONS: - You should have link created in CMS > Promotions > Popup Text field with the URL that leads to the respective promotion in application
    PRECONDITIONS: - Make sure that there are promotions created in CMS and linked to active signposting promotions (by Market Flags)
    PRECONDITIONS: - Parameters (first one is Market level and second one is Event level):
    PRECONDITIONS: 1) MKTFLAG_FI, EVFLAG_FIN - Faller's Insurance
    PRECONDITIONS: 2) MKTFLAG_BBAL, EVFLAG_BBL - Beaten by a Length
    PRECONDITIONS: 3) MKTFLAG_EPR, EVFLAG_EPR - Extra Place Race
    PRECONDITIONS: NOTE: Information about promotions, available for the event, is received in <drilldownTagNames> attribute in SiteServer response for the event.
    PRECONDITIONS: In order for the icons to appear on the Race cards, they should be turned on on the Event level.
    """
    keep_browser_open = True

    def test_001___go_to_horse_racing_landing_page_and_open_the_event_with_promotion_signposting_enabled_on_market_level__tap_promo_icon_next_to_the_market_header_and_verify_promo_pop_up(self):
        """
        DESCRIPTION: - Go to Horse Racing landing page and open the event with promotion signposting enabled on market level
        DESCRIPTION: - Tap promo icon next to the market header and verify promo pop-up
        EXPECTED: - Pop-up is centered
        EXPECTED: - Pop-up's title is taken from CMS > Promotions > "Popup Title" field
        EXPECTED: - Pop-up's text is taken from > Promotions > "Popup Text" field
        EXPECTED: - There is "OK" button
        """
        pass

    def test_002_tap_ok_button(self):
        """
        DESCRIPTION: Tap "OK" button
        EXPECTED: Pop-up is closed and user stays on the same page
        """
        pass

    def test_003___tap_promo_icon_next_to_the_market_header_again_and_tap_on_a_configured_link_to_this_promotion__verify_the_correct_navigation(self):
        """
        DESCRIPTION: - Tap promo icon next to the market header again and tap on a configured link to this promotion
        DESCRIPTION: - Verify the correct navigation
        EXPECTED: User is navigated to the correct promotion page via provided URL
        """
        pass
