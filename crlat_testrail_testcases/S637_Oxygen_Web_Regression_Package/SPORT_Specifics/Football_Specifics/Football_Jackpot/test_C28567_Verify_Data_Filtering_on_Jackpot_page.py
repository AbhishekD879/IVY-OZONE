import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C28567_Verify_Data_Filtering_on_Jackpot_page(Common):
    """
    TR_ID: C28567
    NAME: Verify Data Filtering on 'Jackpot' page
    DESCRIPTION: This test case verifies Data Filtering on 'Jackpot' page
    PRECONDITIONS: 1) To retrieve a list of Football Jackpot pools please use the following request in Siteserver:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Pool?simpleFilter=pool.type:equals:V15&simpleFilter=pool.isActive&translationLang=LL
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 2) To view all events being used within the Football Jackpot please use the following request in Siteserver:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForMarket/YYY?translationLang=LL
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   YYY - comma separated list of 15 market id's of Football Jackpot pool
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **NOTE**:
    PRECONDITIONS: *   'Jackpot' tab is available for both logged out and logged in users, if Football Pool Data available
    PRECONDITIONS: *   **any changes are applied **(displaying/removing of  'Jackpot' tab or changing Jackpot pool that is displayed to another) **on page refresh ONLY**
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tapfootball_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Football' icon on the Sports Menu Ribbon
        EXPECTED: Desktop:
        EXPECTED: * <Sport> Landing Page is opened
        EXPECTED: * 'Matches'->'Today' sub tab is opened by default
        EXPECTED: Mobile:
        EXPECTED: * <Sport> Landing Page is opened
        EXPECTED: * 'Matches' tab is opened by default
        """
        pass

    def test_003_tap_jackpot_tab(self):
        """
        DESCRIPTION: Tap 'Jackpot' tab
        EXPECTED: Football Jackpot Page is opened
        """
        pass

    def test_004_verify_number_of_displayed_jackpot_pools(self):
        """
        DESCRIPTION: Verify number of displayed Jackpot pools
        EXPECTED: Only **ONE **Football Jackpot pool at any one time is displayed
        """
        pass

    def test_005_verify_present_jackpot_pool(self):
        """
        DESCRIPTION: Verify present Jackpot pool
        EXPECTED: *   Pool is only shown if it has attributes '**type="V15"**' and '**isActive="true"**' and does NOT have any events with attribute 'isStarted="true"'
        EXPECTED: *   Displayed pool should be removed once first/earliest event within has the attribute 'isStarted="true"
        """
        pass

    def test_006_verify_list_of_present_events_within_the_present_jackpot_pool(self):
        """
        DESCRIPTION: Verify list of present events within the present Jackpot pool
        EXPECTED: Corresponding 15 events for present Jackpot pool is shown (use second link from Preconditions)
        """
        pass
