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
class Test_C29374_Verify_Module_Section(Common):
    """
    TR_ID: C29374
    NAME: Verify Module Section
    DESCRIPTION: This test case verifies Module Section on the Feature tab (mobile/tablet) Featured section (desktop)
    PRECONDITIONS: - CMS https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=CMS-API+Endpoints
    PRECONDITIONS: - Ladbrokes OpenBet System https://confluence.egalacoral.com/display/SPI/Ladbrokes+OpenBet+System
    PRECONDITIONS: - Coral OpenBet System https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForType/XXX ?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: - There are more than one event/selection in the module section
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_go_to_module_selector_ribbon(self):
        """
        DESCRIPTION: Go to Module Selector Ribbon
        EXPECTED: **For mobile/tablet:**
        EXPECTED: 'Featured' tab is selected by default
        EXPECTED: **For desktop:**
        EXPECTED: Module Ribbon Tabs are transformed into sections displayed in the following order:
        EXPECTED: 1) Enhanced multiples carousel
        EXPECTED: 2) In-Play & Live Stream
        EXPECTED: 3) Next Races Carousel
        EXPECTED: 4) Featured area
        """
        pass

    def test_003_verifymodule_area(self):
        """
        DESCRIPTION: Verify **Module Area**
        EXPECTED: Module area contains **Modules**
        """
        pass

    def test_004_verify_name_ofmodule(self):
        """
        DESCRIPTION: Verify name of **Module**
        EXPECTED: Module name corresponds to the name set in 'Module Title' field in CMS ('title' attribute)
        """
        pass

    def test_005_verify_default_state_of_module(self):
        """
        DESCRIPTION: Verify default state of Module
        EXPECTED: Module is expanded/collapsed depanding on value 'Expanded by default' selected in CMS ('showExpanded' attribute - true/false)
        """
        pass

    def test_006_verify_icons_on_module_accordion_header(self):
        """
        DESCRIPTION: Verify icons on module accordion (header)
        EXPECTED: * 'Special' or 'Enhanced' badge can be displayed if configured
        EXPECTED: OR
        EXPECTED: * # (YourCall) icon and/or 'Cash Out' icon can be displayed if available
        """
        pass

    def test_007_verify_footer_link_if_name_of_link_is_set_in_cms(self):
        """
        DESCRIPTION: Verify Footer link if name of link is set in CMS
        EXPECTED: *   Link is displayed at bottom of module section
        EXPECTED: *   Text of link corresponds to text set in 'Footer link text' field in CMS ('text' attribute)
        """
        pass

    def test_008_verify_footer_link_if_name_of_link_is_not_set_in_cms(self):
        """
        DESCRIPTION: Verify Footer link if name of link is NOT set in CMS
        EXPECTED: *   Link is displayed at bottom of module section
        EXPECTED: *   Footer link is shown in the format:
        EXPECTED: **View All <number of all events> <name of module> Events**
        """
        pass

    def test_009_verify_number_of_events(self):
        """
        DESCRIPTION: Verify Number of Events
        EXPECTED: It is number of all existing events for verified ID of **Type**/*Market/Class*... depending on value selected in 'Select Events by' and 'Max Events to Display' fields
        """
        pass

    def test_010_clicktap_footer_link(self):
        """
        DESCRIPTION: Click/Tap Footer link
        EXPECTED: User is redirected to the url set in 'Footer link URL' field in CMS ('url' attribute - e.g. football/today)
        """
        pass
