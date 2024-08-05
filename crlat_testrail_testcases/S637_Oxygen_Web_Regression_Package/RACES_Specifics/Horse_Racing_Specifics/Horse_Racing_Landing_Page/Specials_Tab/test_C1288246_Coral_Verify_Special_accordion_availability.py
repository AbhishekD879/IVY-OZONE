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
class Test_C1288246_Coral_Verify_Special_accordion_availability(Common):
    """
    TR_ID: C1288246
    NAME: [Coral] Verify 'Special' accordion availability
    DESCRIPTION: This test case verifies availability of <Type> accordion if there are no corresponding special events, market or selections
    DESCRIPTION: Jira ticket:
    DESCRIPTION: BMA-24371: HR Specials: Re-design
    PRECONDITIONS: Event is set as special when typeFlagCodes: ‘SP’ on Event Level in SS response ('Specials' flag is checked on Type level in OB TI)
    PRECONDITIONS: To retrieve the information from the Site Server use the following link:
    PRECONDITIONS: https://ss-aka-ori.ladbrokes.com/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForClass/226,223?simpleFilter=event.siteChannels:contains:M&simpleFilter=event.typeFlagCodes:intersects:SP&simpleFilter=event.isStarted:isFalse&simpleFilter=event.suspendAtTime:greaterThan:2020-07-30T12:08:00.000Z&simpleFilter=event.isResulted:isFalse&limitRecords=outcome:1&limitRecords=market:1&translationLang=en&responseFormat=json&prune=event&prune=market
    PRECONDITIONS: limitRecords=outcome:1&limitRecords=market:1 - filter just for Ladbrokes brand, since outcomes (selections/odds) are not shown on 'Specials' tab there.
    """
    keep_browser_open = True

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Application is loaded
        """
        pass

    def test_002_tap_horse_racing_icon___specials_tab(self):
        """
        DESCRIPTION: Tap 'Horse Racing' icon -> 'Specials' tab
        EXPECTED: - 'Specials' tap is opened
        EXPECTED: - Available special events are displayed in sub accordions within corresponding <Type> accordions
        """
        pass

    def test_003_in_ti_set_eventmarketselectionss_to_undisplayed_within_a_corresponding_type(self):
        """
        DESCRIPTION: In TI: Set event/market/selections(s) to undisplayed within a corresponding Type
        EXPECTED: Event/market/selections(s) are undisplayed
        """
        pass

    def test_004_in_application_verify_availability_of_a_type_accordion_with_undisplayed_eventmarketselectionss(self):
        """
        DESCRIPTION: In application: Verify availability of a <Type> accordion with undisplayed event/market/selections(s)
        EXPECTED: <Type> accordion is NOT displayed
        """
        pass
