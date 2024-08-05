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
class Test_C141199_Verify_displaying_of_suspended_selection_on_Race_Landing_page_Next_4_Races_when_it_is_added_to_the_betslip(Common):
    """
    TR_ID: C141199
    NAME: Verify displaying of suspended selection on <Race> Landing page ('Next 4 Races') when it is added to the betslip
    DESCRIPTION: This test case verifies displaying of suspended selection on <Race> Landing page ('Next Races') when it is added to the betslip
    PRECONDITIONS: To get SiteServer info about event use the following url:
    PRECONDITIONS: https://{openbet_env_link}/openbet-ssviewer/Drilldown/X.XX/NextNEventToOutcomeForClass/N/YYYY?simpleFilter=event.typeFlagCodes:intersects:UK,IE,INT&simpleFilter=event.isActive:isTrue&simpleFilter=market.templateMarketName:equals:|Win%20or%20Each%20Way|&priceHistory=true&simpleFilter=event.siteChannels:contains:M&existsFilter=event:simpleFilter:market.marketStatusCode:equals:A&simpleFilter=market.marketStatusCode:equals:A&simpleFilter=outcome.outcomeStatusCode:equals:A&simpleFilter=event.eventStatusCode:equals:A&simpleFilter=event.rawIsOffCode:notEquals:Y&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:1&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:2&limitRecords=outcome:4&translationLang=en&responseFormat=json
    PRECONDITIONS: Where
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: YYYY - class ID
    PRECONDITIONS: N - number of events
    PRECONDITIONS: Note: OB supports only values:3, 5, 7 or 12. Example, if CMS value > 12 then 12 events is set on UI, if CMS value <= 5 then 5 events is set on UI and etc.
    PRECONDITIONS: See attributes on market level to define price types for event:
    PRECONDITIONS: 'priceTypeCodes' = 'LP'
    PRECONDITIONS: 'priceTypeCodes' = 'LP, SP'
    PRECONDITIONS: Notice, Price updates on <Race> Landing Page is possible ONLY for 'Today' tab on 'Next 4 Races' module.
    PRECONDITIONS: For the rest tabs: 'Tomorrow' and 'Future' -> 'Next Races' module is not displayed there.
    """
    keep_browser_open = True

    def test_001_clicktap_on_race_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Click/Tap on <Race> icon from the sports menu ribbon
        EXPECTED: <Race> landing page is opened
        """
        pass

    def test_002_find_events_in_the_next_races_no_matter_what_price_type_it_has(self):
        """
        DESCRIPTION: Find events in the Next Races (no matter what price type it has)
        EXPECTED: Events are shown in the 'Next 4 Races' module
        """
        pass

    def test_003_clicktap_on_priceodds_button_and_check_its_displaying(self):
        """
        DESCRIPTION: Click/Tap on Price/Odds button and check it's displaying
        EXPECTED: Selected Price/Odds button is marked as added to Betslip (Becomes green)
        """
        pass

    def test_004_verify_that_selection_is_added_to_bet_slip(self):
        """
        DESCRIPTION: Verify that selection is added to Bet Slip
        EXPECTED: Selection is present in Bet Slip and counter is increased on header
        """
        pass

    def test_005_trigger_the_following_situation_for_selected_outcome_of_win_or_each_way_marketoutcomestatuscode__s(self):
        """
        DESCRIPTION: Trigger the following situation for selected outcome of 'Win or Each Way' market:
        DESCRIPTION: outcomeStatusCode = 'S'
        EXPECTED: 
        """
        pass

    def test_006_verify_outcome_for_the_event(self):
        """
        DESCRIPTION: Verify outcome for the event
        EXPECTED: * Price/Odds button for outcome is displayed immediately as greyed out and become disabled but still displaying the prices in case it is 'priceTypeCodes' = 'LP'
        EXPECTED: * Price/Odds button for outcome is displayed immediately as greyed out and become disabled but still displaying the SP in case it is 'priceTypeCodes' = 'SP'
        EXPECTED: * Price/Odds button is not marked as added to Betslip (is not green anymore)
        EXPECTED: * Suspended outcome disappears from the 'Next 4 Races' module after page reloading
        EXPECTED: * The list of outcomes is refreshed after page reloading
        """
        pass

    def test_007_trigger_the_following_situation_for_selected_outcome_of_win_or_each_way_marketoutcomestatuscode__a(self):
        """
        DESCRIPTION: Trigger the following situation for selected outcome of 'Win or Each Way' market:
        DESCRIPTION: outcomeStatusCode = 'A'
        EXPECTED: 
        """
        pass

    def test_008_verify_event_and_its_outcomes(self):
        """
        DESCRIPTION: Verify event and its outcomes
        EXPECTED: * Disappeared outcome will be shown on the 'Next Races' module after page reloading
        EXPECTED: * Price/Odds button of this event is no more disabled, they become active
        EXPECTED: * Price/Odds button is marked as added to Betslip (Becomes green)
        """
        pass
