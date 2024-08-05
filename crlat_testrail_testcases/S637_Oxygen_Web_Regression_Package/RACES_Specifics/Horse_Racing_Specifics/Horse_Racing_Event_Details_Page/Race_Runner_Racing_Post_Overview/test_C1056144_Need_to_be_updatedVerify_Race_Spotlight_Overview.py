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
class Test_C1056144_Need_to_be_updatedVerify_Race_Spotlight_Overview(Common):
    """
    TR_ID: C1056144
    NAME: [Need to be updated]Verify Race Spotlight Overview
    DESCRIPTION: This test case verifies Horse Racing post overview
    DESCRIPTION: Applies to mobile, tablet & desktop
    DESCRIPTION: AUTOTEST: [C1937656]
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
    PRECONDITIONS: See attributes :
    PRECONDITIONS: 'courseDistanceWinner', 'age', 'weight', 'officialRating' (under 'racingFormOutcome')
    """
    keep_browser_open = True

    def test_001_go_to_the_event_details_page_for_the_event_which_has_silks_available(self):
        """
        DESCRIPTION: Go to the event details page for the Event which has SILKS available
        EXPECTED: * Generic Silks are displayed for missed mappings
        EXPECTED: * Correct silks are displayed for mapped selections (silkName)
        EXPECTED: * Runner number and Draw are correct and displayed only if not = '0' and are present in response (runnerNumber, draw)
        EXPECTED: * Horse name (name)
        EXPECTED: *  Jockey/Trainer
        EXPECTED: *  Form (formGuide)
        EXPECTED: *  Course (C), Course and Distance (CD) or Distance (D) winner badge (courseDistanceWinner)
        """
        pass

    def test_002_go_to_the_event_selection_area_and_tap_within_the_area_or_on_the_arrow_on_the_right_side(self):
        """
        DESCRIPTION: Go to the Event selection area and tap within the area (or on the arrow on the right side)
        EXPECTED: *   Horse information is expanded showing information about the runner
        EXPECTED: *   OR (officialRating)
        EXPECTED: *   Age # yo (age)
        EXPECTED: *   Weight
        EXPECTED: **For mobile&tablet:**
        EXPECTED: * Information is located above the Spotlight summary
        EXPECTED: **For desktop:**
        EXPECTED: * Information is aligned from left side
        """
        pass

    def test_003_verify_info_for_spotlight_section(self):
        """
        DESCRIPTION: Verify info for 'Spotlight' section
        EXPECTED: **For mobile&tablet:**
        EXPECTED: *   100 characters <Race> information for Horse is displayed, followed by 'Show More' link
        EXPECTED: *   Tapping on 'Show More' link, shows the whole information text, link is changed to 'Show Less'
        EXPECTED: *   Information corresponds to the one in **'overview'** attribute
        EXPECTED: **For desktop:**
        EXPECTED: * The whole information text is shown
        """
        pass

    def test_004_verify_priceodds_buttons(self):
        """
        DESCRIPTION: Verify 'Price/Odds' buttons
        EXPECTED: Price / odds buttons are shown near each selection
        EXPECTED: 3 types of price type can be shown near selection:
        EXPECTED: *   SP
        EXPECTED: *   LP
        EXPECTED: *   S
        """
        pass
