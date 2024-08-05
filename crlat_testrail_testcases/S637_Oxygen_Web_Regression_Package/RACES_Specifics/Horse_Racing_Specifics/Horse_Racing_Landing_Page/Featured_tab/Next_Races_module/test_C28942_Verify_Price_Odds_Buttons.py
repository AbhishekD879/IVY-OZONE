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
class Test_C28942_Verify_Price_Odds_Buttons(Common):
    """
    TR_ID: C28942
    NAME: Verify Price/Odds Buttons
    DESCRIPTION: This test case is for checking of odds for each event which is displayed in 'Next Races' module.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: Load Oxygen app
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) To get info about class events use link:
    PRECONDITIONS: https://{openbet_env_link}/openbet-ssviewer/Drilldown/X.XX/NextNEventToOutcomeForClass/N/YYYY?simpleFilter=event.typeFlagCodes:intersects:UK,IE,INT&simpleFilter=event.isActive:isTrue&simpleFilter=market.templateMarketName:equals:|Win%20or%20Each%20Way|&priceHistory=true&simpleFilter=event.siteChannels:contains:M&existsFilter=event:simpleFilter:market.marketStatusCode:equals:A&simpleFilter=market.marketStatusCode:equals:A&simpleFilter=outcome.outcomeStatusCode:equals:A&simpleFilter=event.eventStatusCode:equals:A&simpleFilter=event.rawIsOffCode:notEquals:Y&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:1&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:2&limitRecords=outcome:4&translationLang=en&responseFormat=json
    PRECONDITIONS: Where
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: YYYY - class ID
    PRECONDITIONS: N - number of events
    PRECONDITIONS: Note: OB supports only values:3, 5, 7 or 12. Example, if CMS value > 12 then 12 events is set on UI, if CMS value <= 5 then 5 events is set on UI and etc.
    PRECONDITIONS: 2) To get info about Extra place events use link:
    PRECONDITIONS: https://{openbet_env_link}/openbet-ssviewer/Drilldown/X.XX/NextNEventToOutcomeForClass/N/YYYY?simpleFilter=event.siteChannels:contains:M&simpleFilter=event.isFinished:isFalse&simpleFilter=event.isResulted:isFalse&simpleFilter=event.isStarted:isFalse&simpleFilter=event.isLiveNowEvent:isFalse&simpleFilter=event.rawIsOffCode:notEquals:Y&existsFilter=event:simpleFilter:market.drilldownTagNames:intersects:MKTFLAG_EPR&simpleFilter=market.templateMarketName:equals:|Win%20or%20Each%20Way|&racingForm=event&limitRecords=outcome:1&translationLang=en&responseFormat=json
    PRECONDITIONS: Where
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: YYYY - class ID
    PRECONDITIONS: N - number of events
    PRECONDITIONS: Note: OB supports only values:3, 5, 7 or 12. Example, if CMS value > 12 then 12 events is set on UI, if CMS value <= 5 then 5 events is set on UI and etc.
    PRECONDITIONS: Use attributes:
    PRECONDITIONS: -  **'priceTypeCodes'** to specify a type of price/odds buttons
    PRECONDITIONS: - **'priceDen' **and** ****'priceNum'** to specify price/odds value
    PRECONDITIONS: 3) To see what CMS is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: 4) Price type could be set in CMS (SP or LP)
    """
    keep_browser_open = True

    def test_001_navigate_to_horse_racing_landing_page(self):
        """
        DESCRIPTION: Navigate to 'Horse Racing' Landing page
        EXPECTED: * 'Horse Racing' Landing page is opened
        EXPECTED: * 'Featured' tab is opened by default
        EXPECTED: * 'Next Races' module is displayed
        """
        pass

    def test_002_verify_next_races_module(self):
        """
        DESCRIPTION: Verify 'Next Races' module
        EXPECTED: The 'Next Races' available events are shown
        """
        pass

    def test_003_from_the_site_server_find_event_where___pricetypecodes_sp_and_check_priceodds_in_the_next_races_module(self):
        """
        DESCRIPTION: From the Site Server find event where:
        DESCRIPTION: *   '**priceTypeCodes'** = 'SP, '
        DESCRIPTION: and check price/odds in the 'Next Races' module
        EXPECTED: 'SP' price/odds buttons are displayed next to each selection
        """
        pass

    def test_004_from_the_site_server_find_event_where___pricetypecodes_lp_and_check_priceodd_in_the_next_races_module(self):
        """
        DESCRIPTION: From the Site Server find event where:
        DESCRIPTION: *    **'priceTypeCodes'** = 'LP, '
        DESCRIPTION: and check price/odd in the 'Next Races' module
        EXPECTED: The 'LP' price/odd button is displayed in decimal or fractional format (depends upon the users chosen odds display preference)
        EXPECTED: Prices correspond to the **'priceNum'** and** 'priceDen'** attributes from the Site Server
        """
        pass

    def test_005_from_the_site_server_response_find_event_where___pricetypecodesp_lp____prices_are_availabe_for_outcomesand_check_priceodds_in_the_next_races_module(self):
        """
        DESCRIPTION: From the Site Server response find event where:
        DESCRIPTION: *   **'priceTypeCode'**='SP, LP, '
        DESCRIPTION: *   Prices ARE availabe for outcomes
        DESCRIPTION: and check price/odds in the 'Next Races' module
        EXPECTED: 'LP' price/odd buttons are displayed in fractional/decimal format next to each selection
        EXPECTED: Prices correspond to the **'priceNum'** and** 'priceDen'** attributes from the Site Server
        """
        pass

    def test_006_from_the_site_server_response_find_event_where___pricetypecodesp_lp____prices_are_not_availabe_for_outcomesand_check_priceodds_in_the_next_races_module(self):
        """
        DESCRIPTION: From the Site Server response find event where:
        DESCRIPTION: *   **'priceTypeCode'**='SP, LP, '
        DESCRIPTION: *   Prices are NOT availabe for outcomes
        DESCRIPTION: and check price/odds in the 'Next Races' module
        EXPECTED: 'SP' price/odds buttons are shown next to each selection
        """
        pass

    def test_007_for_mobile_and_tabletgo_to_the_homepage___tap_next_races_tab_from_the_module_selector_ribbon(self):
        """
        DESCRIPTION: **For Mobile and Tablet:**
        DESCRIPTION: Go to the homepage -> tap 'Next Races' tab from the module selector ribbon
        EXPECTED: **For Mobile and Tablet:**
        EXPECTED: 'Next Races' module is shown
        """
        pass

    def test_008_for_mobile_and_tabletrepeat_steps__4___6(self):
        """
        DESCRIPTION: **For Mobile and Tablet:**
        DESCRIPTION: Repeat steps # 4 - 6
        EXPECTED: 
        """
        pass

    def test_009_for_desktopgo_to_the_desktop_homepage___check_next_races_section_under_the_in_play_section(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Go to the desktop homepage -> check 'Next Races' section under the 'In-Play' section
        EXPECTED: **For Desktop:**
        EXPECTED: 'Next Races' section is shown
        """
        pass

    def test_010_for_desktoprepeat_steps__4___6(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Repeat steps # 4 - 6
        EXPECTED: 
        """
        pass
