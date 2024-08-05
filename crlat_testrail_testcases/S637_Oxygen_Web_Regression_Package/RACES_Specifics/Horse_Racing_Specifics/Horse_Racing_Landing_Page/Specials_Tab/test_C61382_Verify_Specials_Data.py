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
class Test_C61382_Verify_Specials_Data(Common):
    """
    TR_ID: C61382
    NAME: Verify Specials Data
    DESCRIPTION: This test case is for checking the data which should be displayed on Specials tab
    PRECONDITIONS: In order to get a list of specials events available use link:
    PRECONDITIONS: <domain>/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForClass/226,223?simpleFilter=event.siteChannels:contains:M&simpleFilter=event.typeFlagCodes:intersects:SP&simpleFilter=event.isStarted:isFalse&simpleFilter=event.suspendAtTime:greaterThan:2020-07-30T12:08:00.000Z&simpleFilter=event.isResulted:isFalse&limitRecords=outcome:1&limitRecords=market:1&translationLang=en&responseFormat=json&prune=event&prune=market
    PRECONDITIONS: limitRecords=outcome:1&limitRecords=market:1 - filter just for Ladbrokes brand, since outcomes (selections/odds) are not shown on 'Specials' tab there.
    PRECONDITIONS: Note, event is set as special when typeFlagCodes: ‘SP’ on Event Level in SS response ('Specials' flag is checked on Type level in OB TI)
    PRECONDITIONS: Where, domain is:
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk - for TST2 environment
    PRECONDITIONS: https://ss-aka-ori-stg2.coral.co.uk - for STG2 environment
    PRECONDITIONS: https://ss-aka-ori.coral.co.uk - for HL and PROD environments
    """
    keep_browser_open = True

    def test_001_load_oxygen(self):
        """
        DESCRIPTION: Load Oxygen
        EXPECTED: Oxygen app is opened
        """
        pass

    def test_002_tap_horse_racing_icon___specials_tab(self):
        """
        DESCRIPTION: Tap 'Horse Racing' icon -> 'Specials' tab
        EXPECTED: 'Specials' tap is opened
        """
        pass

    def test_003_verify_events_which_are_shown_on_the_specials_tabs(self):
        """
        DESCRIPTION: Verify events which are shown on the Specials tabs
        EXPECTED: Only events (with typeFlagCodes: ‘SP’) are available
        EXPECTED: Only events which do NOT have attribute isStarted = true are shown
        EXPECTED: Only events which do NOT have attribute isResulted="true" are shown
        """
        pass

    def test_004_check_special_events_which_are_not_related_to_classid__226_or_227_eg_horse_racing_special_events_daily_racing_special_events(self):
        """
        DESCRIPTION: Check special events which are not related to classID = 226 or 227 (e.g. horse racing special events, daily racing special events)
        EXPECTED: Event is displayed
        EXPECTED: All events with special flag which are related to Horse Racing category are shown
        """
        pass

    def test_005_check_special_event_displaying_for_events_which_are_not_related_to_any_of_the_following_groups__uk__ie__int__vr(self):
        """
        DESCRIPTION: Check special event displaying for events which are NOT related to any of the following groups:
        DESCRIPTION: - UK
        DESCRIPTION: - IE
        DESCRIPTION: - INT
        DESCRIPTION: - VR
        EXPECTED: Event is displayed
        EXPECTED: All events with special flag which are related to Horse Racing category are shown
        """
        pass
