import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C9726397_Event_hub_Removing_Expired_Enhanced_Multiples_from_Module(Common):
    """
    TR_ID: C9726397
    NAME: Event hub: Removing Expired Enhanced Multiples from Module
    DESCRIPTION: This test case verifies that Enhanced Multiples are removed from displaying within Module on front-end
    PRECONDITIONS: 1) There are at least 2 Enhanced Multiples (Select Events by - 'Enhanced Multiples' in CMS) in module section
    PRECONDITIONS: 2) CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: 3) To retrieve all events for verified Type: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForType/XXX?translationLang=LL
    PRECONDITIONS: XXX - the event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 4) To retrieve markets and outcomes for event use: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - the event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: To complete event:
    PRECONDITIONS: - open the event page in TI;
    PRECONDITIONS: - set results for all markets (Set Results > Confirm Results > Settle).
    PRECONDITIONS: To make event expired:
    PRECONDITIONS: - open the event page in TI;
    PRECONDITIONS: - undisplay it and save changes.
    PRECONDITIONS: 5) User is on Homepage > Event hub tab
    """
    keep_browser_open = True

    def test_001_find_module_with_enhanced_multiples_from_preconditions(self):
        """
        DESCRIPTION: Find module with Enhanced Multiples from preconditions
        EXPECTED: Enhanced Multiples are displayed with correct outcome
        """
        pass

    def test_002_trigger_completionexpiration_one_of_the_enhanced_multiples(self):
        """
        DESCRIPTION: Trigger completion/expiration one of the Enhanced Multiples
        EXPECTED: The Enhanced Multiples of completed/expired event is removed from being published on front-end (attribute 'displayed="N"')
        """
        pass