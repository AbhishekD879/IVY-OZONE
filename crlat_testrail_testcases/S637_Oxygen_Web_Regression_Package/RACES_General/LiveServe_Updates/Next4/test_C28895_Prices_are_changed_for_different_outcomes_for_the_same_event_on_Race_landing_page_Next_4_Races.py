import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C28895_Prices_are_changed_for_different_outcomes_for_the_same_event_on_Race_landing_page_Next_4_Races(Common):
    """
    TR_ID: C28895
    NAME: Prices are changed for different outcomes for the same event on <Race> landing page (Next 4 Races)
    DESCRIPTION: Note: changing several outcomes at a time is not possible on TST2
    PRECONDITIONS: **Updates are received in push notifications**
    PRECONDITIONS: To get SiteServer info about event use the following url:
    PRECONDITIONS: https://{openbet_env_link}/openbet-ssviewer/Drilldown/X.XX/NextNEventToOutcomeForClass/N/YYYY?simpleFilter=event.typeFlagCodes:intersects:UK,IE,INT&simpleFilter=event.isActive:isTrue&simpleFilter=market.templateMarketName:equals:|Win%20or%20Each%20Way|&priceHistory=true&simpleFilter=event.siteChannels:contains:M&existsFilter=event:simpleFilter:market.marketStatusCode:equals:A&simpleFilter=market.marketStatusCode:equals:A&simpleFilter=outcome.outcomeStatusCode:equals:A&simpleFilter=event.eventStatusCode:equals:A&simpleFilter=event.rawIsOffCode:notEquals:Y&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:1&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:2&limitRecords=outcome:4&translationLang=en&responseFormat=json
    PRECONDITIONS: Where
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: YYYY - class ID
    PRECONDITIONS: N - number of events
    PRECONDITIONS: Note: OB supports only values:3, 5, 7 or 12. Example, if CMS value > 12 then 12 events is set on UI, if CMS value <= 5 then 5 events is set on UI and etc.
    PRECONDITIONS: See attributes on market level to define price types for event:
    PRECONDITIONS: **'priceTypeCodes' **= 'LP'
    PRECONDITIONS: **'priceTypeCodes'** = 'LP, SP'
    PRECONDITIONS: Notice, Price updates on <Race> Landing Page is possible ONLY for 'Today' tab on 'Next 4 Races' module.
    PRECONDITIONS: For the rest tabs: 'Tomorrow' and 'Future' -> 'Next Races' module is not displayed there.
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: 
        """
        pass

    def test_002_tap_race_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Race> icon from the sports menu ribbon
        EXPECTED: <Race> Landing Page is opened
        """
        pass

    def test_003_in_the_next_races_module_find_event_withpricetypecodes_lp(self):
        """
        DESCRIPTION: In the 'Next Races' module find event with **'priceTypeCodes'**= 'LP'
        EXPECTED: Event is shown
        """
        pass

    def test_004_trigger_price_change_of_win_or_each_way_market_for_several_outcomes_for_event_with_lp_prices(self):
        """
        DESCRIPTION: Trigger price change of 'Win or Each Way' market for several outcomes for event with 'LP' prices
        EXPECTED: Corresponding 'Price/Odds' buttons immediately display new prices and for a few seconds they change their color to:
        EXPECTED: - blue color if price has decreased
        EXPECTED: - red color if price has increased
        EXPECTED: Previous Odds, under Price/Odds button, are updated/added respectively
        """
        pass

    def test_005_in_the_next_4_races_module_find_event_withpricetypecodes_lp_sp(self):
        """
        DESCRIPTION: In the 'Next 4 Races' module find event with **'priceTypeCodes'**= 'LP, SP'
        EXPECTED: Event is shown
        """
        pass

    def test_006_trigger_price_change_for_win_or_each_way_market_for_several_outcomes_for_event_with_lp_sp_prices(self):
        """
        DESCRIPTION: Trigger price change for 'Win or Each Way' market for several outcomes for event with 'LP, SP' prices
        EXPECTED: Corresponding 'Price/Odds' buttons immediately display new prices and for a few seconds they change their color to:
        EXPECTED: - blue color if price has decreased
        EXPECTED: - red color if price has increased
        EXPECTED: Previous Odds, under Price/Odds button, are updated/added respectively
        """
        pass
