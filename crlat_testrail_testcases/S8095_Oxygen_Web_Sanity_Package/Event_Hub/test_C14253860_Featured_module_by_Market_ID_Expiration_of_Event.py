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
class Test_C14253860_Featured_module_by_Market_ID_Expiration_of_Event(Common):
    """
    TR_ID: C14253860
    NAME: Featured module by Market ID: Expiration of Event
    DESCRIPTION: This test case verifies that Featured module by Market ID is removed when an event is expired
    PRECONDITIONS: 1. Event Hub is created in CMS > Sport Pages > Event Hub.
    PRECONDITIONS: 2. Featured module by Market ID (Only primary markets, outright markets, Win or Each Way markets supported) is created in the previously created EventHub and it's expanded by default. (Sports Pages > EventHub > Featured events > 'Create Featured Tab Module')
    PRECONDITIONS: 3. Should be also created Module Ribbon tab related to the created Event Hub (from step1) - CMS->Module Ribbon Tabs->Create Module Ribbon Tab (choose 'Event Hub' in the 'Directive Name' dropdown and created Event Hub (from step1) in 'Event Hub Name' dropdown)
    PRECONDITIONS: 4. A user is on Homepage > EventHub tab
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: * CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: * To retrieve all events for verified Type: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForType/XXX?translationLang=LL
    PRECONDITIONS: XXX - the event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: To retrieve markets and outcomes for event use: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL XXX - the event ID X.XX - currently supported version of OpenBet release LL - language (e.g. en, ukr)
    PRECONDITIONS: To complete the event:
    PRECONDITIONS: * open the event page in TI;
    PRECONDITIONS: * set results for all markets (Set Results > Confirm Results > Settle).
    PRECONDITIONS: To make event expired:
    PRECONDITIONS: * open the event page in TI;
    PRECONDITIONS: * undisplay it and save changes.
    """
    keep_browser_open = True

    def test_001_navigate_to_the_module_from_preconditions(self):
        """
        DESCRIPTION: Navigate to the module from preconditions
        EXPECTED: The event is displayed with correct outcomes
        """
        pass

    def test_002_trigger_completionexpiration_one_of_the_verified_event(self):
        """
        DESCRIPTION: Trigger completion/expiration one of the verified event
        EXPECTED: Module from Step 1 is undisplayed
        EXPECTED: Message 'No events found' is displayed
        """
        pass
