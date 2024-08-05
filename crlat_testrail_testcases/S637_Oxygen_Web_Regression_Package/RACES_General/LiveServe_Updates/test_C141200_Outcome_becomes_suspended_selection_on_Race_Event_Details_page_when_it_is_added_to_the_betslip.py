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
class Test_C141200_Outcome_becomes_suspended_selection_on_Race_Event_Details_page_when_it_is_added_to_the_betslip(Common):
    """
    TR_ID: C141200
    NAME: Outcome becomes suspended selection on <Race> Event Details page when it is added to the betslip
    DESCRIPTION: This test case verifies displaying of suspended selection on <Race> Event Details Page when it is added to the betslip
    DESCRIPTION: Applies to mobile, tablet and desktop
    DESCRIPTION: AUTOTEST [C2009763]
    PRECONDITIONS: To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/YYYYYYY?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: X.XX - current supported version of OpenBet SiteServer
    PRECONDITIONS: YYYYYYY - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes on market level to define price types for event:
    PRECONDITIONS: 'priceTypeCodes' = 'LP'
    PRECONDITIONS: 'priceTypeCodes' = 'LP, SP'
    PRECONDITIONS: Notice, Price updates on <Race> Landing Page is possible ONLY for 'Today' tab on 'Next 4 Races' module.
    PRECONDITIONS: For the rest tabs: 'Tomorrow' and 'Future' -> 'Next 4 Races' module is not displayed there.
    """
    keep_browser_open = True

    def test_001_open_event_details_page_where_event_has_lp_price_type(self):
        """
        DESCRIPTION: Open event details page where event has LP price type
        EXPECTED: Event details page is opened
        """
        pass

    def test_002_tap_on_priceodds_button(self):
        """
        DESCRIPTION: Tap on Price/Odds button
        EXPECTED: * Selected Price/Odds button is marked as added to Betslip and displayed as green
        EXPECTED: * Selection is present in Bet Slip and counter is increased on header (Betslip is closed)
        """
        pass

    def test_003_in_ti_suspend_selected_outcome_outcomestatuscode__s___navigate_to_application_and_observe_changes(self):
        """
        DESCRIPTION: In TI: Suspend selected outcome:
        DESCRIPTION: ( **'outcomeStatusCode'** = 'S' ) > Navigate to application and observe changes
        EXPECTED: * Price/Odds button for outcome is immediately  displayed as greyed out and become disabled but still displaying the prices
        EXPECTED: * Price/Odds button is not marked as added to Betslip (is not green anymore)
        """
        pass

    def test_004_in_ti_unsuspend_selected_outcome_outcomestatuscode__a___navigate_to_application_and_observe_changes(self):
        """
        DESCRIPTION: In TI: UnSuspend selected outcome:
        DESCRIPTION: ( **'outcomeStatusCode'** = 'A' ) > Navigate to application and observe changes
        EXPECTED: * Price/Odds button is no more disabled, they become active
        EXPECTED: * Price/Odds button is marked as added to Betslip and displayed as green
        """
        pass

    def test_005_repeat_steps__3_6_for_event_where_price_type_is_splpsp(self):
        """
        DESCRIPTION: Repeat steps # 3-6 for event where price type is 'SP'/'LP,SP'
        EXPECTED: 
        """
        pass
