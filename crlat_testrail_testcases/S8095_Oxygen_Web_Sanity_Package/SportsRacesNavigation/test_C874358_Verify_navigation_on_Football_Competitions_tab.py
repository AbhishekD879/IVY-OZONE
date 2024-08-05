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
class Test_C874358_Verify_navigation_on_Football_Competitions_tab(Common):
    """
    TR_ID: C874358
    NAME: Verify navigation on Football Competitions tab
    DESCRIPTION: This test case verifies 'Competitions' tab on the Football sport page
    DESCRIPTION: AUTOTEST [C57119745] - HL/PROD only
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to Football Landing page
    PRECONDITIONS: 3. Click/Tap on the 'Competition' tab
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
    """
    keep_browser_open = True

    def test_001_navigate_to_football_landing_page(self):
        """
        DESCRIPTION: Navigate to Football landing page
        EXPECTED: Football sport page is shown. 'Matches' tab is opened by default and highlighted
        """
        pass

    def test_002_tapclick_competitions_tab(self):
        """
        DESCRIPTION: Tap/click 'Competitions' tab
        EXPECTED: **For Mobile/Tablet:**
        EXPECTED: List of sub-categories (Classes) is loaded according to set ID's in CMS
        EXPECTED: **For Desktop:**
        EXPECTED: * Competition Quick Links are displayed below Sports Subtabs
        EXPECTED: * 'Popular' and 'A-Z' switchers are displayed below Sports Sub Tabs
        EXPECTED: * 'Popular' switcher is selected by default and highlighted
        EXPECTED: * List of sub-categories (Classes) is loaded according to set ID's in CMS
        EXPECTED: * The sub-categories (Classes) accordions are ordered according to settings in the CMS
        """
        pass

    def test_003_tapclick_on_sub_category_class_id_with_type_ids(self):
        """
        DESCRIPTION: Tap/click on sub-category (Class ID) with Type ID's
        EXPECTED: List of Competitions (Type ID) displayed
        """
        pass

    def test_004_tapclick_on_any_competition_name_type(self):
        """
        DESCRIPTION: Tap/click on any Competition name (Type)
        EXPECTED: * 'Competition Details' page is opened
        EXPECTED: * Events from the relevant league (Type) are displayed
        EXPECTED: **For mobile/Tablet:**
        EXPECTED: * There are 4 tabs (navigation buttons) on the page: 'Matches', 'Outrights', 'Results', 'Standings' (when available)
        EXPECTED: * 'Matches' tab is default
        EXPECTED: **For Desktop:**
        EXPECTED: * There are 'Matches and 'Outrights' switchers
        EXPECTED: * 'Matches' switcher is selected by default
        EXPECTED: * "Results' are presented in a separate widget
        """
        pass

    def test_005_check_results_sectionwidget_content(self):
        """
        DESCRIPTION: Check Results section/widget content
        EXPECTED: - Latest results for events are displayed
        EXPECTED: - Tab is not shown - In case results are absent for whole section **for Mobile/tablet**
        EXPECTED: - 'Results' widget is not shown in case results are absent **for Desktop**
        """
        pass

    def test_006_check_outrights_section_content(self):
        """
        DESCRIPTION: Check Outrights section content
        EXPECTED: - A list of Outright events available for the selected competition is shown
        EXPECTED: - Tab is not shown - In case events are absent for whole section
        """
        pass

    def test_007_check_standings_tab_mobiletablet_for_desktop_standings_are_presented_on_league_table_widget_that_is_shown_on_matches_and_outrights(self):
        """
        DESCRIPTION: Check Standings tab (mobile/tablet)
        DESCRIPTION: * for Desktop Standings are presented on League Table widget that is shown on Matches and Outrights
        EXPECTED: - Statistics table is shown for the selected league for current season
        EXPECTED: - There is a possibility to navigate between seasons (e.g. Premier League 2018/2019 > Premier League 2017/2018 ) using navigation arrows
        EXPECTED: - Tab is not shown when statistics are not received
        """
        pass

    def test_008_check_matches_tab(self):
        """
        DESCRIPTION: Check 'Matches' tab
        EXPECTED: - A list of MATCH events available for selected competition is shown
        EXPECTED: - 'No events found' message - in case events are absent for selected competition for **Desktop**
        EXPECTED: * 'Matches' tab is not shown in case events are absent for selected competition for **Mobile**
        """
        pass

    def test_009_verify_matches_section_content(self):
        """
        DESCRIPTION: Verify 'Matches' section content
        EXPECTED: - Market selector with list of markets which are available for events is displayed
        EXPECTED: - Events with selected market is displayed
        """
        pass
