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
class Test_C28849_Verify_Race_Each_Way_Terms(Common):
    """
    TR_ID: C28849
    NAME: Verify <Race> Each Way Terms
    DESCRIPTION: This test case is for checking terms on the event details page for all available markets.
    PRECONDITIONS: To retrieve data from the Site Server use steps:
    PRECONDITIONS: 1) To get Class IDs use a link
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Class?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *XX - sport category id*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: Horse Racing category id =21
    PRECONDITIONS: Greyhound category id = 19
    PRECONDITIONS: 2) To get all 'Events' for the classes use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/YYYY?simpleFilter=market.dispSortName:equals:MR&simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: Where:
    PRECONDITIONS: *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *XX - sport category id*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: *YYYY - a comma separated values of class ID's (e.g. 97 or 97, 98)*
    PRECONDITIONS: See attributes:
    PRECONDITIONS: - **'name'** attribute in the market level to see market name
    PRECONDITIONS: - '**isEachWayAvaiable' **to check whether terms will be displayed;
    PRECONDITIONS: - **'eachWayFactorNum'**,** 'eachWayFactorDen **and** 'eachWayPlaces'** to verify terms correctness.
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: 
        """
        pass

    def test_002_go_to_the_race_landing_page(self):
        """
        DESCRIPTION: Go to the <Race> landing page
        EXPECTED: <Race> landing page is opened
        """
        pass

    def test_003_navigate_to_the_event_details_page(self):
        """
        DESCRIPTION: Navigate to the event details page
        EXPECTED: Event details page is opened
        EXPECTED: 'Win or E/W' tab is opened by default
        """
        pass

    def test_004_check_terms_displaying(self):
        """
        DESCRIPTION: Check terms displaying
        EXPECTED: Each-way terms are displayed if **'isEachWayAvailable'** = 'true' attribute is present from SiteServer response
        EXPECTED: Each-way terms are displayed above the list of selection
        """
        pass

    def test_005_verify_terms_correctness(self):
        """
        DESCRIPTION: Verify terms correctness
        EXPECTED: Terms correspond to the **'eachWayFactorNum'**, **'eachWayFactorDen'** and** 'eachWayPlaces'** attributes from the Site Server
        """
        pass

    def test_006_check_terms_format(self):
        """
        DESCRIPTION: Check terms format
        EXPECTED: Terms are displayed in the following format:
        EXPECTED: ***" Each Way: x/y odds - places z,j,k"***
        EXPECTED: where:
        EXPECTED: x = eachWayFactorNum
        EXPECTED: y= eachWayFactorDen
        EXPECTED: z,j,k = eachWayPlaces
        """
        pass

    def test_007_tap_win_only_tab(self):
        """
        DESCRIPTION: Tap 'Win Only' tab
        EXPECTED: 'Win Only' tab is opened
        EXPECTED: 'Win Only' market with all its selection is shown
        """
        pass

    def test_008_repeat_steps__4___7(self):
        """
        DESCRIPTION: Repeat steps # 4 - 7
        EXPECTED: 
        """
        pass

    def test_009_tap_betting_wo_tab(self):
        """
        DESCRIPTION: Tap 'Betting WO' tab
        EXPECTED: 'Betting WO' tab is opened
        EXPECTED: The list of all available markets is shown
        """
        pass

    def test_010_repeat_steps__4___7(self):
        """
        DESCRIPTION: Repeat steps # 4 - 7
        EXPECTED: 
        """
        pass

    def test_011_tap_more_markets_tab(self):
        """
        DESCRIPTION: Tap 'More Markets' tab
        EXPECTED: 'More Markets' tab is opened
        EXPECTED: The list of all available markets is shown
        """
        pass

    def test_012_repeat_steps__4___7(self):
        """
        DESCRIPTION: Repeat steps # 4 - 7
        EXPECTED: 
        """
        pass

    def test_013_verify_event_wich_has_markets_where_attribute_iseachwayavailabletrue_is_absent(self):
        """
        DESCRIPTION: Verify event wich has markets where attribute **'isEachWayAvailable'**='true' is absent
        EXPECTED: Terms are not displayed for those markets
        """
        pass
