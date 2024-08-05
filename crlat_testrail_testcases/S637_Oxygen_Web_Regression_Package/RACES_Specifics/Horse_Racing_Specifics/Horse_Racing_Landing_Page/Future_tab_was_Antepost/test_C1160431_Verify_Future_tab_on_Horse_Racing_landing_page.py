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
class Test_C1160431_Verify_Future_tab_on_Horse_Racing_landing_page(Common):
    """
    TR_ID: C1160431
    NAME: Verify 'Future' tab on 'Horse Racing' landing page
    DESCRIPTION: This test case verifies 'Future' tab on 'Horse Racing' landing page
    DESCRIPTION: AUTOTEST: [C1792286]
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to 'Horse Racing' landing page ('Future' tab is available)
    PRECONDITIONS: **OB configurations:**
    PRECONDITIONS: In order to create HR Future event use TI tool http://backoffice-tst2.coral.co.uk/ti/
    PRECONDITIONS: 1) 'Antepost' check box should be checked on event level ('drilldownTagNames'='EVFLAG_AP' in SS response)
    PRECONDITIONS: with only one of the following:
    PRECONDITIONS: - 'Flat' check box should be checked on event level ('drilldownTagNames'='EVFLAG_FT' in SS response)
    PRECONDITIONS: OR
    PRECONDITIONS: - 'National Hunt' check box should be checked on event level ('drilldownTagNames'='EVFLAG_NH' in SS response)
    PRECONDITIONS: OR
    PRECONDITIONS: - 'International' check box should be checked on event level ('drilldownTagNames'='EVFLAG_IT' in SS response)
    PRECONDITIONS: 2) 'Antepost' checkbox should be checked on market level (Market Template= 'Outright' with name 'Ante-post')
    PRECONDITIONS: 3) Event start time should be in the future (like 2 days from now)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: - If flags 'Flat', 'National Hunt', 'International' are not checked on event level, events are not displayed on the landing page
    PRECONDITIONS: - If flag 'Antepost' is not checked on market level, new designs do not apply on HR EDP
    PRECONDITIONS: - For checking info regarding event use the following link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/ZZZZ
    PRECONDITIONS: where,
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: ZZZZ - an event id
    PRECONDITIONS: Request to check data:
    PRECONDITIONS: https://ss-aka-ori.ladbrokes.com/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForClass/226,223?simpleFilter=event.siteChannels:contains:M&simpleFilter=event.startTime:greaterThanOrEqual:2020-08-09T00:00:00.000Z&simpleFilter=event.suspendAtTime:greaterThan:2020-08-07T11:22:30.000Z&simpleFilter=event.classId:notIntersects:227&simpleFilter=event.drilldownTagNames:intersects:EVFLAG_FT,EVFLAG_IT,EVFLAG_NH&simpleFilter=event.drilldownTagNames:contains:EVFLAG_AP&externalKeys=event&limitRecords=outcome:1&limitRecords=market:1&translationLang=en&responseFormat=json&prune=event&prune=market
    """
    keep_browser_open = True

    def test_001_clicktap_on_future_tab(self):
        """
        DESCRIPTION: Click/Tap on 'Future' tab
        EXPECTED: - 'Future' tab is opened
        EXPECTED: - Switchers are displayed: 'Flat', 'National Hunt' and 'International' (if containing at least one event that meets Preconditions, otherwise a switcher is not displayed). Default opened switcher tab setups in CMS (if not the first switcher is opened by default)
        EXPECTED: - If no events are available: "No events found" text is shown
        """
        pass

    def test_002_navigate_among_available_switchers_eg_flat_national_hunt_international(self):
        """
        DESCRIPTION: Navigate among available switchers (e.g 'Flat', 'National Hunt', 'International')
        EXPECTED: - Corresponding events (that meet Preconditions are available) are displayed within one of the switchers (e.g 'Flat', 'National Hunt', 'International')
        EXPECTED: - Events are grouped by 'Type'
        EXPECTED: - Accordions are ordered by 'dispTypeOrder' (from SS)
        EXPECTED: - Title of each accordion corresponds to 'typeName' from SS response
        EXPECTED: - First accordion is expanded by default, other ones are collapsed
        EXPECTED: - All accordions are collapsed/expanded once tapped
        """
        pass

    def test_003_verify_events_within_a_type_accordion(self):
        """
        DESCRIPTION: Verify events within a 'Type' accordion
        EXPECTED: - Events within the same 'Type' accordion are ordered by 'startTime' in asc order
        EXPECTED: - Each event contains:
        EXPECTED: *** DD-MM-YYYY|HH:MM (corresponds to 'startDate' in SS response)
        EXPECTED: *** 'typeName' from SS response e.g. ASCOT
        EXPECTED: *** Event 'name' (corresponds to 'name' of the event in SS response)
        EXPECTED: *** '>' icon
        EXPECTED: - Each event area is clickable
        EXPECTED: On tablet:
        EXPECTED: - Events are displayed in two columns within an accordion
        EXPECTED: On desktop:
        EXPECTED: - Events are displayed in three columns within an accordion
        """
        pass
