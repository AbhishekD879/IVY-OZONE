import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.homepage_featured
@vtest
class Test_C2507415_Featured_Module_by_Enhanced_Multiples_ID__Verify_names_displaying_within_Featured_tab(Common):
    """
    TR_ID: C2507415
    NAME: Featured: Module by Enhanced Multiples ID - Verify names displaying within Featured tab
    DESCRIPTION: This test case verifies whether selection names are displayed correctly on the frontend for Featured tab module by Enhanced Multiples TypeID
    PRECONDITIONS: 1) Featured Module by Enhanced Multiples TypeID is created in CMS. Module should contain at least 1 selection with long name. Name can be modified in TI.
    PRECONDITIONS: 2) CMS, TI: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: (check <CMS_ENDPOINT> via 'devlog' function)
    PRECONDITIONS: 3) http://{domain}/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForType/XXX?translationLang=LL
    PRECONDITIONS: XXX - the event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: Where, domain is:
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk - for TST2 environment
    PRECONDITIONS: https://ss-aka-ori-stg2.coral.co.uk - for STG2 environment
    PRECONDITIONS: https://ss-aka-ori.coral.co.uk - for HL and PROD environments
    PRECONDITIONS: NOTE: For caching needs Akamai service is used, so after saving changes in CMS there could be delay up to 5-10 mins before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_001_navigane_to_homepage__featured_tab(self):
        """
        DESCRIPTION: Navigane to Homepage > Featured tab
        EXPECTED: * Active Featured modules are displayed in Featured tab
        """
        pass

    def test_002_expand_featured_module_from_preconditions(self):
        """
        DESCRIPTION: Expand Featured Module from Preconditions
        EXPECTED: * EM Selections are shown within the module as per CMS configuration
        EXPECTED: * Enhanced Multiples selection's long names are NOT cropped and are fully shown in several rows
        """
        pass
