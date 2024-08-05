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
class Test_C41492501_Verify_the_first_switcher_tab_is_opened_by_default_if_its_Name_is_wrong_configured_in_CMS(Common):
    """
    TR_ID: C41492501
    NAME: Verify the first switcher tab is opened by default if its Name is wrong configured in CMS
    DESCRIPTION: This test case verifies the first switcher tab is opened by default if its Name is wrong configured in CMS
    PRECONDITIONS: 1. Make sure the wrong switcher tab name (e.g. 'National HAnt') is default in CMS
    PRECONDITIONS: 2. Load the app
    PRECONDITIONS: 3. Navigate to Horse Racing landing page ('Future' tab is available)
    PRECONDITIONS: **OB configurations:**
    PRECONDITIONS: 1) To create HR Future event use TI tool:
    PRECONDITIONS: a) 'Antepost' check box should be checked on event level ('drilldownTagNames'='EVFLAG_AP' in SS response)
    PRECONDITIONS: with only one of the following:
    PRECONDITIONS: - 'Flat' check box should be checked on event level ('drilldownTagNames'='EVFLAG_FT' in SS response)
    PRECONDITIONS: OR
    PRECONDITIONS: - 'National Hunt' check box should be checked on event level ('drilldownTagNames'='EVFLAG_NH' in SS response)
    PRECONDITIONS: OR
    PRECONDITIONS: - 'International' check box should be checked on event level ('drilldownTagNames'='EVFLAG_IT' in SS response)
    PRECONDITIONS: b) 'Antepost' check box should be checked on market level (Market Template= 'Outright' with name 'Ante-post')
    PRECONDITIONS: c) Event start time should be in the future (like 2 days from now)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: - If flags 'Flat', 'National Hunt', 'International' are not checked on event level, events are not displayed on the landing page
    PRECONDITIONS: - If flag 'Antepost' is not checked on market level, new designs do not apply on HR EDP
    PRECONDITIONS: **CMS configurations:**
    PRECONDITIONS: To setup default switcher tab use CMS:
    PRECONDITIONS: System configuration -> structure -> defaultAntepostTab -> tabName -> **'tab name'**
    PRECONDITIONS: where
    PRECONDITIONS: **'tab name'** - should be the same as existing switcher tab name (e.g. Flat, National Hunt, International)
    PRECONDITIONS: Request to check data on 'Future' tab:
    PRECONDITIONS: https://ss-aka-ori.ladbrokes.com/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForClass/226,223?simpleFilter=event.siteChannels:contains:M&simpleFilter=event.startTime:greaterThanOrEqual:2020-08-09T00:00:00.000Z&simpleFilter=event.suspendAtTime:greaterThan:2020-08-07T11:22:30.000Z&simpleFilter=event.classId:notIntersects:227&simpleFilter=event.drilldownTagNames:intersects:EVFLAG_FT,EVFLAG_IT,EVFLAG_NH&simpleFilter=event.drilldownTagNames:contains:EVFLAG_AP&externalKeys=event&limitRecords=outcome:1&limitRecords=market:1&translationLang=en&responseFormat=json&prune=event&prune=market
    """
    keep_browser_open = True

    def test_001_navigate_to_future_tab(self):
        """
        DESCRIPTION: Navigate to 'Future' tab
        EXPECTED: * Future' tab is opened
        EXPECTED: * Switchers are displayed: 'Flat', 'National Hunt' and 'International' (if containing at least one event that meets Preconditions)
        EXPECTED: * the first switcher tab is opened by default
        """
        pass

    def test_002_leave_the_name_field_empty_eg_flat_international_in_cmssystem_configuration___structure___defaultanteposttab___tabname___tab_nameand_repeat_step_1(self):
        """
        DESCRIPTION: Leave the Name field empty (e.g. Flat, International) in CMS
        DESCRIPTION: (System configuration -> structure -> defaultAntepostTab -> tabName -> **'tab name'**)
        DESCRIPTION: and repeat step 1
        EXPECTED: * Future' tab is opened
        EXPECTED: * Switchers are displayed: 'Flat', 'National Hunt' and 'International' (if containing at least one event that meets Preconditions)
        EXPECTED: * the first switcher tab is opened by default
        """
        pass
