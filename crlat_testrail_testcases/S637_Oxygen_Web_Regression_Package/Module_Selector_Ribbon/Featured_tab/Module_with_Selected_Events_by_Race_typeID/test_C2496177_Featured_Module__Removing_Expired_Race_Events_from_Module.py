import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C2496177_Featured_Module__Removing_Expired_Race_Events_from_Module(Common):
    """
    TR_ID: C2496177
    NAME: Featured Module - Removing Expired <Race> Events from Module
    DESCRIPTION: This test case verifies that <Race> events are removed from displaying within Module on front-end
    PRECONDITIONS: 1) There are at least 2 <Race> (Select Events by - 'Race Type ID' in CMS) events in module section
    PRECONDITIONS: 2) CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: 3) To retrieve all events for verified Type: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForType/XXX?
    PRECONDITIONS: translationLang=LL
    PRECONDITIONS: XXX - the event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 4) To retrieve markets and outcomes for event use: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?
    PRECONDITIONS: translationLang=LL
    PRECONDITIONS: XXX - the event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: To complete event:
    PRECONDITIONS: - open the event page in TI;
    PRECONDITIONS: - set results for all markets (Set Results > Confirm Results > Settle).
    PRECONDITIONS: To make event expired:
    PRECONDITIONS: - open the event page in TI;
    PRECONDITIONS: - undisplay it and save changes.
    PRECONDITIONS: NOTE: This test case should check also Virtual Horses/Greyhounds events within Featured Module.
    """
    keep_browser_open = True

    def test_001_go_to_home_page__featured_module(self):
        """
        DESCRIPTION: Go to Home page > Featured module
        EXPECTED: Home page with Featured module is displayed
        """
        pass

    def test_002_find_module_with_racetypeid_events_from_preconditions(self):
        """
        DESCRIPTION: Find module with <Race>typeID) events from preconditions
        EXPECTED: Events are displayed with correct outcomes
        """
        pass

    def test_003_trigger_completionexpiration_one_of_the_verified_event(self):
        """
        DESCRIPTION: Trigger completion/expiration one of the verified event
        EXPECTED: Completed/expired event is removed from being published on front-end (attribute 'displayed="N"')
        """
        pass
