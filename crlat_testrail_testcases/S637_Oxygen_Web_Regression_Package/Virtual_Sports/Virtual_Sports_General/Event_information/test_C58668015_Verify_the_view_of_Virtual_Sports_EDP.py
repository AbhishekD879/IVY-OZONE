import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.virtual_sports
@vtest
class Test_C58668015_Verify_the_view_of_Virtual_Sports_EDP(Common):
    """
    TR_ID: C58668015
    NAME: Verify the view of Virtual Sports EDP
    DESCRIPTION: This test case verifies the view of Virtual Sports EDP
    PRECONDITIONS: Get SiteServer response to verify data:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/x.xx/EventToOutcomeForClass/285?simpleFilter=class.categoryId:equals:39&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: x.xx - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 1. Open Coral/Ladbrokes test environment
    """
    keep_browser_open = True

    def test_001_navigate_to_the_virtual_sport_page(self):
        """
        DESCRIPTION: Navigate to the Virtual sport page
        EXPECTED: Page loads in order:
        EXPECTED: First Sport > First child sport > Next available event
        EXPECTED: EDP template automatically chosen according to sport and displayed with the below
        EXPECTED: details:
        EXPECTED: -  The event being displayed should be highlighted
        EXPECTED: -  Time of the event with the name of the event
        EXPECTED: -  Count down timer if the event hasn't started yet
        EXPECTED: -  List of the markets
        EXPECTED: -  CTA at the bottom of the page
        EXPECTED: Design:
        EXPECTED: https://app.zeplin.io/project/5d64f0e582415f9b2a7045aa/screen/5dee3f51be0bb316723dcf29
        """
        pass

    def test_002_verify_markets_on_edp(self):
        """
        DESCRIPTION: Verify markets on EDP
        EXPECTED: List of the markets with the name of the market as the collapsible header and the first market expanded sorted by SiteServer display order
        """
        pass

    def test_003_tap_on_cta_at_the_bottom(self):
        """
        DESCRIPTION: Tap on CTA at the bottom
        EXPECTED: - User redirected to another site URL
        EXPECTED: - Button text and link configured in CMS > Virtual Sports > [createdSport] > 'Button text', 'Cross-sell URL' fields
        """
        pass
