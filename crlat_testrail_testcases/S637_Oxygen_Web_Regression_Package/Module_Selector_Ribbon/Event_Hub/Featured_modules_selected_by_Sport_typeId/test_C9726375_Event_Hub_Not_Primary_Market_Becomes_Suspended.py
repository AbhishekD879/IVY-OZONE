import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C9726375_Event_Hub_Not_Primary_Market_Becomes_Suspended(Common):
    """
    TR_ID: C9726375
    NAME: Event Hub: Not Primary Market Becomes Suspended
    DESCRIPTION: This test case verifies situation when market/markets become suspended on event landing page on the 'Event Huv' tab (mobile/tablet)
    PRECONDITIONS: To get into SiteServer use this link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: *   Z.ZZ  - current supported version of OpenBet SiteServer
    PRECONDITIONS: *   XXXX - event ID
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: ***Boosted selection - this is ******an ******event****** with only one selection which is shown on the 'Featured' tab. ***
    PRECONDITIONS: ***On CMS it  is configured as event shown by selection id.***
    PRECONDITIONS: **NOTE:** **LivePrice updates are NOT applicable for Outrights and Enhanced Multiples events**
    """
    keep_browser_open = True

    def test_001_in_the_event_hub_tab_find_boosted_selection(self):
        """
        DESCRIPTION: In the Event hub tab find boosted selection
        EXPECTED: Event with a boosted selection is shown
        """
        pass

    def test_002_trigger_the_following_situation_for_this_eventmarketstatuscodesfor_market_type_boosted_selection_belongs_to(self):
        """
        DESCRIPTION: Trigger the following situation for this event:
        DESCRIPTION: **marketStatusCode="S"**
        DESCRIPTION: for  market type boosted selection belongs to
        EXPECTED: 
        """
        pass

    def test_003_verify_outcome_for_the_event(self):
        """
        DESCRIPTION: Verify outcome for the event
        EXPECTED: *   Price/Odds button of this event immediately start displaying "S"
        EXPECTED: *   Price/Odds button is disabled
        """
        pass

    def test_004_change_attribute_for_this_eventmarketstatuscodeafor_market_type_boosted_selection_belongs_to(self):
        """
        DESCRIPTION: Change attribute for this event:
        DESCRIPTION: **marketStatusCode="A"**
        DESCRIPTION: for market type boosted selection belongs to
        EXPECTED: 
        """
        pass

    def test_005_verify_outcome_for_the_event(self):
        """
        DESCRIPTION: Verify outcome for the event
        EXPECTED: *   Price/Odds button of this event is not disabled anymore
        EXPECTED: *   Price / Odds button displays prices immediately
        """
        pass
