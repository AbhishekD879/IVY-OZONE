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
class Test_C28894_Prices_are_changed_for_different_events_on_Race_landing_page_Next_Races_Module(Common):
    """
    TR_ID: C28894
    NAME: Prices are changed for different events on <Race> landing page ('Next  Races' Module)
    DESCRIPTION: Note: changing several outcomes at a time is not possible on TST2
    PRECONDITIONS: **Updates are received in push notifications**
    PRECONDITIONS: To get info about class events use link:
    PRECONDITIONS: https://{openbet_env_link}/openbet-ssviewer/Drilldown/X.XX/NextNEventToOutcomeForClass/N/YYYY?simpleFilter=event.typeFlagCodes:intersects:UK,IE,INT&simpleFilter=event.isActive:isTrue&simpleFilter=market.templateMarketName:equals:|Win%20or%20Each%20Way|&priceHistory=true&simpleFilter=event.siteChannels:contains:M&existsFilter=event:simpleFilter:market.marketStatusCode:equals:A&simpleFilter=market.marketStatusCode:equals:A&simpleFilter=outcome.outcomeStatusCode:equals:A&simpleFilter=event.eventStatusCode:equals:A&simpleFilter=event.rawIsOffCode:notEquals:Y&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:1&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:2&limitRecords=outcome:4&translationLang=en&responseFormat=json
    PRECONDITIONS: Where
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: YYYY - class ID
    PRECONDITIONS: N - number of events
    PRECONDITIONS: Note: OB supports only values:3, 5, 7 or 12. Example, if CMS value > 12 then 12 events is set on UI, if CMS value <= 5 then 5 events is set on UI and etc.
    PRECONDITIONS: To get info about Extra place events use link:
    PRECONDITIONS: https://{openbet_env_link}/openbet-ssviewer/Drilldown/X.XX/NextNEventToOutcomeForClass/N/YYYY?simpleFilter=event.siteChannels:contains:M&simpleFilter=event.isFinished:isFalse&simpleFilter=event.isResulted:isFalse&simpleFilter=event.isStarted:isFalse&simpleFilter=event.isLiveNowEvent:isFalse&simpleFilter=event.rawIsOffCode:notEquals:Y&existsFilter=event:simpleFilter:market.drilldownTagNames:intersects:MKTFLAG_EPR&simpleFilter=market.templateMarketName:equals:|Win%20or%20Each%20Way|&racingForm=event&limitRecords=outcome:1&translationLang=en&responseFormat=json
    PRECONDITIONS: Where
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: YYYY - class ID
    PRECONDITIONS: N - number of events
    PRECONDITIONS: Note: OB supports only values:3, 5, 7 or 12. Example, if CMS value > 12 then 12 events is set on UI, if CMS value <= 5 then 5 events is set on UI and etc.
    PRECONDITIONS: See attributes on market level to define price types for event:
    PRECONDITIONS: **'priceTypeCodes' **= 'LP'
    PRECONDITIONS: **'priceTypeCodes'** = 'LP, SP'
    PRECONDITIONS: Notice, Price updates on <Race> Landing Page is possible ONLY for 'Today' tab on 'Next Races' module.
    PRECONDITIONS: For the rest tabs: 'Tomorrow' and 'Future' -> 'Next Races' module is not displayed there.
    """
    keep_browser_open = True

    def test_001_load_the_application(self):
        """
        DESCRIPTION: Load the application
        EXPECTED: 
        """
        pass

    def test_002_tap_race_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Race> from the sports menu ribbon
        EXPECTED: <Race> landing page is opened
        """
        pass

    def test_003_in_the_next_races_module_find_a_few_events_withpricetypecodes_lp(self):
        """
        DESCRIPTION: In the 'Next Races' module find a few events with **'priceTypeCodes'**= 'LP'
        EXPECTED: Event is shown
        """
        pass

    def test_004_trigger_price_change_for_win_or_each_way_market_outcome_events_with_lp_prices(self):
        """
        DESCRIPTION: Trigger price change for 'Win or Each Way' market outcome events with 'LP' prices
        EXPECTED: Corresponding 'Price/Odds' buttons immediately display new prices and for a few seconds they change their color to:
        EXPECTED: - blue color if price has decreased
        EXPECTED: - red color if price has increased
        EXPECTED: Previous Odds, under Price/Odds button, are updated/added respectively
        """
        pass

    def test_005_in_the_next_races_module_find_a_few_events_withpricetypecodes_lp_sp(self):
        """
        DESCRIPTION: In the 'Next Races' module find a few events with **'priceTypeCodes'**= 'LP, SP'
        EXPECTED: Events are shown
        """
        pass

    def test_006_trigger_price_changes_of_lp_part_for_win_or_each_way_market_outcomes_for_events_with_lp_sp_prices(self):
        """
        DESCRIPTION: Trigger price changes of LP part for 'Win or Each Way' market outcomes for events with 'LP, SP' prices
        EXPECTED: Corresponding 'Price/Odds' buttons immediately display new prices and for a few seconds they change their color to:
        EXPECTED: - blue color if price has decreased
        EXPECTED: - red color if price has increased
        EXPECTED: Previous Odds, under Price/Odds button, are updated/added respectively
        """
        pass
