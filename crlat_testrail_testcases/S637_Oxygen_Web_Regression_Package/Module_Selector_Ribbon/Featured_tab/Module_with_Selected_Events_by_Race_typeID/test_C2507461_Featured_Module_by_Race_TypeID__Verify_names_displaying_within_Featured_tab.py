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
class Test_C2507461_Featured_Module_by_Race_TypeID__Verify_names_displaying_within_Featured_tab(Common):
    """
    TR_ID: C2507461
    NAME: Featured: Module by <Race> TypeID - Verify names displaying within Featured tab
    DESCRIPTION: This test case verifies whether event/selection names are displayed correctly on the frontend for Featured tab module by <Race> TypeID
    PRECONDITIONS: 1) Featured Module by <Race> TypeID is created in CMS. Module should contain at least 1 Event and 1 Selection with long name. Name can be modified in TI or in CMS Featured Module edit page.
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
    PRECONDITIONS: Virtual HR/GH events are supported as well for Featured module created by RaceTypeID
    """
    keep_browser_open = True

    def test_001_navigane_to_homepage_gt_featured_tab(self):
        """
        DESCRIPTION: Navigane to Homepage &gt; Featured tab
        EXPECTED: * Active Featured modules are displayed in Featured tab
        """
        pass

    def test_002_expand_featured_module_from_preconditions(self):
        """
        DESCRIPTION: Expand Featured Module from Preconditions
        EXPECTED: * Events are displayed within the module as per CMS configuration
        EXPECTED: * &lt;Race&gt; events' long names are cropped and followed with '...' before the price/odds buttons / scores (if available)
        EXPECTED: * &lt;Race&gt; selection name are cropped and followed with '...' before the price/odds buttons / scores (if available)
        """
        pass

    def test_003_verify_the_view_of_the_module(self):
        """
        DESCRIPTION: Verify the view of the module
        EXPECTED: **Coral** Module consists of:
        EXPECTED: - Header of the module with &lt;Name&gt; and 'See all' link (navigating to HR landing page)
        EXPECTED: - Below the header the next race information: time (eg. 14:10 ) / event name (eg. Fakenham)/ Each Way option (eg. E/W 1/4 odds - places 1-2") / places/ Start time (eg. Starts 13:18) / 'More' link (navigating the user to the specific race card)
        EXPECTED: - Race card with events and price odds buttons
        EXPECTED: - Any promo signposting icons (like 'Extra Place') are displayed at the top left corner of race card (NOT in the header of the module or on market level)
        EXPECTED: **Ladbrokes** Module consists of:
        EXPECTED: * Collapsible Header(Featured race) with 'See All' link navigating the user to the HR landing page
        EXPECTED: * Header with the Name, Time, countdown timer (when available), type of race, going and 'More' link navigating the user to the specific race card
        EXPECTED: * Below header goes E/W terms and watch icon (if the stream is available) at the top of race card
        EXPECTED: * Promo Icons when available (placed right above E/W terms) on the race card
        EXPECTED: * For each horse the full silk, Name of the horse, Name of the jockey and trainer, Form of the horse and odds button as per the design, and last 2 odds are displayed
        """
        pass

    def test_004_verify_names_displaying_for_virtual_horsesgreyhounds_within_featured_module(self):
        """
        DESCRIPTION: Verify names displaying for Virtual Horses/Greyhounds within Featured module
        EXPECTED: Expected result is the same as on step 3
        """
        pass
