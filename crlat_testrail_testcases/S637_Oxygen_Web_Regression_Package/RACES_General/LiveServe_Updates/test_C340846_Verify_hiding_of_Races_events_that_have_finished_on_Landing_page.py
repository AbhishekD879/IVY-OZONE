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
class Test_C340846_Verify_hiding_of_Races_events_that_have_finished_on_Landing_page(Common):
    """
    TR_ID: C340846
    NAME: Verify hiding of <Races> events that have finished on Landing page
    DESCRIPTION: 
    PRECONDITIONS: 1. To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/YYYYY?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: X.XX - current supported version of OpenBet SiteServer
    PRECONDITIONS: YYYYYYY- event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes on market level to define price types for event:
    PRECONDITIONS: 'priceTypeCodes' = 'LP'
    PRECONDITIONS: 'priceTypeCodes' = 'LP, SP'
    PRECONDITIONS: Note: Price updates on <Race> Landing Page is possible ONLY for 'Today' tab on 'Next 4 Races' module.
    PRECONDITIONS: For the rest tabs: 'Tomorrow' and 'Future' -> 'Next 4 Races' module is not displayed there.
    PRECONDITIONS: 2. Use http://backoffice-tst2.coral.co.uk/ti/ for triggering events undisplaying or setting results.
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_race_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Race> icon from the Sports Menu Ribbon
        EXPECTED: * <Race> landing page is opened
        EXPECTED: * 'Next 4 Races' module is shown
        EXPECTED: * Events off time sections are displayed
        """
        pass

    def test_003_set_results_for_any_event(self):
        """
        DESCRIPTION: Set results for any event
        EXPECTED: * [displayed:"N"] or [result_conf:"Y"] attributes are received in LIVE SERV push
        EXPECTED: * Event off time tab is displayed as Resulted for certain event
        """
        pass

    def test_004_change_date_to_future_for_any_event(self):
        """
        DESCRIPTION: Change date to future for any event
        EXPECTED: Event off time tab disappears from event off time section on 'Today' page only after page refresh
        """
        pass
