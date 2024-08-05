import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@vtest
class Test_C9346564_Verify_Football_Competitions_Landing_Page_Functionality(Common):
    """
    TR_ID: C9346564
    NAME: Verify Football Competitions Landing Page Functionality
    DESCRIPTION: This test case verified Football Competitions Landing Page Functionality
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to Football Landing page
    PRECONDITIONS: 3. Make sure that the 'Competition' tab is available
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1. The Class accordions on Competitions page are CMS configurable
    PRECONDITIONS: 2. To set classes in CMS navigate to 'System-configuration' -> 'Competitions Football' and put class ID's in 'InitialClassIDs' and/or 'A-ZClassIDs' field
    PRECONDITIONS: 3. To verify the availability of events in class please use the following link:
    PRECONDITIONS: https://ss-aka-ori.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Class?translationLang=en&simpleFilter=class.categoryId:equals:6&simpleFilter=class.isActive&simpleFilter=class.siteChannels:contains:M&simpleFilter=class.hasOpenEvent
    PRECONDITIONS: * X.XX - currently supported version of OpenBet release
    PRECONDITIONS: 4. IDs that are typically set in **'A-ZClassIDs'** field: 115,592,591,595,100,109,104,103,102,101,108,106,105,136,137,134,135,138,139,548,133,132,131,130,145,146,147,148,149,140,142,141,144,143,118,119,116,117,114,112,113,111,110,127,128,129,123,124,125,126,120,652,122,121,584,179,178,172,173,170,171,176,177,174,175,587,586,589,181,182,183,180,159,158,157,154,155,152,153,150,151,168,167,169,163,164,165,166,160,161,162,69,68,715,73,74,71,72,70,724,79,76,75,78,77,82,83,84,85,80,81,730,89,88,87,86,739,91,92,90,95,96,93,94,743,744,745,740,741,742,98,97,99,603,16291
    PRECONDITIONS: 5. IDs that are typically set in **'InitialClassIDs'** field:
    PRECONDITIONS: * International (Class ID = 115)
    PRECONDITIONS: * UEFA Club Comps (Class ID = 165)
    PRECONDITIONS: * England (Class ID = 97)
    PRECONDITIONS: * Scotland (Class ID=158)
    PRECONDITIONS: * Spain (Class ID=166)
    PRECONDITIONS: * Italy (Class ID=120)
    PRECONDITIONS: * Germany (Class ID=105)
    PRECONDITIONS: * France (Class ID=102)
    PRECONDITIONS: * Netherlands (Class ID=140)
    PRECONDITIONS: * USA (Class ID=176)
    PRECONDITIONS: **(!)** 'CompetitionsFootball' request is sent each time Competitions page(tab) is loaded(opened). Values from JSON response on this request are used to get the Class Accordion data from Openbet TI.
    PRECONDITIONS: 6. When user navigates to ant type (Competitions Detailed page), events data is received in EventToOutcomeForType request to SS which should include only markets listed in request. For example:
    PRECONDITIONS: https://ss-aka-ori.ladbrokes.com/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForType/500?simpleFilter=event.eventSortCode:notIntersects:TNMT,TR01,TR02,TR03,TR04,TR05,TR06,TR07,TR08,TR09,TR10,TR11,TR12,TR13,TR14,TR15,TR16,TR17,TR18,TR19,TR20&simpleFilter=market.templateMarketName:intersects:|Match%20Betting|,|Over/Under%20Total%20Goals|,|Both%20Teams%20to%20Score|,|To%20Qualify|,|Draw%20No%20Bet|,|First-Half%20Result|,|Next%20Team%20to%20Score|,|Extra-Time%20Result|,Match%20Betting,Over/Under%20Total%20Goals,Both%20Teams%20to%20Score,To%20Qualify,Draw%20No%20Bet,First-Half%20Result,Next%20Team%20to%20Score,Extra-Time%20Result,Match%20Result%20and%20Both%20Teams%20To%20Score,|Match%20Result%20and%20Both%20Teams%20To%20Score|&translationLang=en&responseFormat=json&prune=event&prune=market&childCount=event
    """
    keep_browser_open = True

    def test_001_verify_layout_of_competitions_tab(self):
        """
        DESCRIPTION: Verify layout of 'Competitions' tab
        EXPECTED: **For Mobile/Tablet:**
        EXPECTED: * The 'Popular' class accordions are loaded based on settings in 'InitialClassIDs' field at CMS
        EXPECTED: * The A-Z' class accordions are loaded based on settings in 'A-ZClassIDs' field at CMS
        EXPECTED: * 'A-Z COMPETITIONS' label is displayed above the 'A-Z' class accordions
        EXPECTED: **For Desktop:**
        EXPECTED: * Competition Quick Links are displayed below Sports Subtabs
        EXPECTED: * 'Popular' and 'A-Z' switchers are displayed below Sports Sub Tabs
        EXPECTED: * 'Popular' switcher is selected by default and highlighted
        EXPECTED: * The 'Popular' class accordions are loaded based on settings in 'InitialClassIDs' fields at CMS
        """
        pass

    def test_002_for_mobiletabletcheck_popular_class_accordionsfor_desktopcheck_popular_class_accordions_when_popular_switcher_is_selected(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Check 'Popular' class accordions
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Check 'Popular' class accordions when 'Popular' switcher is selected
        EXPECTED: * 'Popular' accordions for classes that are set in 'InitialClassIDs' at CMS are displayed
        EXPECTED: * The First accordion is expanded by default
        EXPECTED: * 'Popular' class accordions  are ordered according to settings is CMS
        """
        pass

    def test_003_for_mobiletabletcheck_a_z_class_accordionsfor_desktopcheck_a_z_class_accordions_when_a_z_switcher_is_selected(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Check 'A-Z' class accordions
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Check 'A-Z' class accordions when 'A-Z' switcher is selected
        EXPECTED: **For Mobile/Tablet:**
        EXPECTED: * 'A-Z' accordions are loaded based on settings in 'A-ZClassIDs' at CMS
        EXPECTED: * All accordions are collapsed by default
        EXPECTED: * 'A-Z' class accordions are ordered alphabetically
        EXPECTED: **For Desktop:**
        EXPECTED: * 'A-Z' switcher is selected and highlighted
        EXPECTED: * 'A-Z' accordions are loaded based on settings in 'A-ZClassIDs' at CMS
        EXPECTED: * The First accordion is expanded by default
        EXPECTED: * 'A-Z' class accordions are ordered alphabetically
        """
        pass

    def test_004_expand_any_class_accordion_with_available_competitions(self):
        """
        DESCRIPTION: Expand any class accordion with available competitions
        EXPECTED: **For mobile/Tablet:**
        EXPECTED: * The leagues (types) are displayed in the list view
        EXPECTED: * Type ID's are ordered by OpenBet display order (lowest display order at the top)
        EXPECTED: **For Desktop:**
        EXPECTED: * The leagues (types) are displayed in Horizontal position
        EXPECTED: * Type ID's are ordered by OpenBet display order (starting with lowest one)
        """
        pass

    def test_005_clicktap_on_league_type(self):
        """
        DESCRIPTION: Click/Tap on League (Type)
        EXPECTED: **For mobile/Tablet:**
        EXPECTED: * User navigates to the 'Competition Details' page
        EXPECTED: * Events from the relevant league (type) are displayed
        EXPECTED: * There are 3 tabs (navigation buttons) on the page: 'Matches', 'Results', 'Outrights'
        EXPECTED: * 'Matches' tab is selected by default
        EXPECTED: **For Desktop:**
        EXPECTED: * User navigates to the 'Competition Details' page
        EXPECTED: * Events from the relevant league (type) are displayed
        EXPECTED: * There are 'Matches and 'Outrights' switchers
        EXPECTED: * 'Matches' switcher is selected by default
        EXPECTED: * 'Results' and 'League Table' widgets are displayed if available
        """
        pass
