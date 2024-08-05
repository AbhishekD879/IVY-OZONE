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
class Test_C1056142_Need_to_delete_after_OX_108Verify_Racing_Post_Verdict_Overview(Common):
    """
    TR_ID: C1056142
    NAME: [Need to delete after OX 108]Verify Racing Post Verdict Overview
    DESCRIPTION: This test case verifies 'Racing Post' logo and Overview displaying on Event Details page.
    DESCRIPTION: AUTOTEST [C1500841]
    PRECONDITIONS: update: After BMA-40744 implementation we'll receive needed data from DF api:
    PRECONDITIONS: -------------------------------------------------------------------
    PRECONDITIONS: **Racing Data Hub link:**
    PRECONDITIONS: - ___Coral DEV___ : cd-dev1.api.datafabric.dev.aws.ladbrokescoral.com/v4/sportsbook-api/categories/{categoryKey}/events/{eventKey}/content?locale=en-GB&api-key={api-key}
    PRECONDITIONS: - ___Ladbrokes DEV___ : https://ld-dev1.api.datafabric.dev.aws.ladbrokescoral.com/v4/sportsbook-api/categories/{categoryKey}/events/{eventKey}/content?locale=en-GB&api-key=LDaa2737afbeb24c3db274d412d00b6d3b
    PRECONDITIONS: https://sb-api-stg.coral.co.uk/v4/sportsbook-api/categories/21/events/13137995/content?locale=en-GB&api-key=CDd2396372409341029e905faba611713
    PRECONDITIONS: - ___Vanila___: https://sb-api-stg.coral.co.uk/v4/sportsbook-api/categories/21/events/13137995/content?locale=en-GB&api-key=CDd2396372409341029e905faba611713
    PRECONDITIONS: - ___URI___ : /v4/sportsbook-api/categories/{categoryKey}/events/{eventKey}/content?locale=en-GB&api-key={api-key}
    PRECONDITIONS: {categoryKey} : 21 - Horse racing, 19 - Greyhound
    PRECONDITIONS: {eventKey} : OB Event id
    PRECONDITIONS: -------------------------------------------------------------------
    PRECONDITIONS: **Open bet link:**
    PRECONDITIONS: - ___VANILLA___: - BETA: https://ss-aka-ori-dub.coral.co.uk/openbet-ssviewer/Drilldown/2.31/Class?translationLang=en&simpleFilter=class.categoryId:equals:21&simpleFilter=class.isActive&simpleFilter=class.siteChannels:contains:M
    PRECONDITIONS: - ___TST2___: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/ZZZZ
    PRECONDITIONS: where,
    PRECONDITIONS: X.XX - currently supported version of OpenBet release
    PRECONDITIONS: ZZZZ - an event id
    PRECONDITIONS: ------------------------------------------------------------------------------------
    PRECONDITIONS: **JIRA Ticket **: BMA-6587 'Racecard Layout Update - Race Information'
    PRECONDITIONS: To get an info about Event racing post overview use a link :
    PRECONDITIONS: ___tst2___ - http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/ZZZZ?racingForm=event&translationLang=LL;
    PRECONDITIONS: ___VANILLA___ - - ___Vanila___: https://sb-api-stg.coral.co.uk/v4/sportsbook-api/categories/21/events/13137995/content?locale=en-GB&api-key=CDd2396372409341029e905faba611713;
    PRECONDITIONS: where,
    PRECONDITIONS: *   *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *   *ZZZZ - an event ID*
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: See attribute **'overview'** to see whether racing post info is available for a selected event.
    """
    keep_browser_open = True

    def test_001_go_to_the_event_details_page(self):
        """
        DESCRIPTION: Go to the Event details page
        EXPECTED: 
        """
        pass

    def test_002_verify_racing_post_overview_section(self):
        """
        DESCRIPTION: Verify "Racing Post overview" section
        EXPECTED: Racing Post overview consists of:
        EXPECTED: **For mobile&tablet:**
        EXPECTED: *   Racing Post | Verdict labels
        EXPECTED: *   100 characters <Race> information for Horse is displayed, followed by 'Show More' link
        EXPECTED: *   Racing Post section is located above Media area
        EXPECTED: **For desktop:**
        EXPECTED: *   Racing Post | Verdict labels
        EXPECTED: *   The whole information text is displayed
        EXPECTED: *   The Racing Post section is located in the second column
        EXPECTED: *   The Racing Post section is expanded by default
        EXPECTED: *   User is able to collapse/expand section by pressing up/down arrow icon
        """
        pass

    def test_003_tap_on_show_more_link(self):
        """
        DESCRIPTION: Tap on 'Show More' link
        EXPECTED: *   The whole information text is shown
        EXPECTED: *   Link is changed to 'Show Less' link
        """
        pass

    def test_004_verify_racing_post__verdict_logo(self):
        """
        DESCRIPTION: Verify 'Racing Post | Verdict' logo
        EXPECTED: 'Racing Post | Verdict' logo is NOT hyperlinked
        """
        pass

    def test_005_tap_on_show_less_link(self):
        """
        DESCRIPTION: Tap on 'Show Less' link
        EXPECTED: Racing Post section is collapsed
        """
        pass
