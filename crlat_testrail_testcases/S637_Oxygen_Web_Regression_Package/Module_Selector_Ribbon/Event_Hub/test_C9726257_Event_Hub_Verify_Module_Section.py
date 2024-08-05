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
class Test_C9726257_Event_Hub_Verify_Module_Section(Common):
    """
    TR_ID: C9726257
    NAME: Event Hub: Verify Module Section
    DESCRIPTION: This test case verifies Module Section on the Event Hub tab (mobile/tablet)
    PRECONDITIONS: 1) Ecent Hub is configured in CMS and there are more than one event/selection in the module section
    PRECONDITIONS: 2) CMS: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: 3) http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForType/XXX ?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 4) User is on Event Hub tab
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_001_verify_name_ofmodule(self):
        """
        DESCRIPTION: Verify name of **Module**
        EXPECTED: Module name corresponds to the name set in 'Module Title' field in CMS ('title' attribute)
        """
        pass

    def test_002_verify_default_state_of_module(self):
        """
        DESCRIPTION: Verify default state of Module
        EXPECTED: Module is expanded/collapsed depanding on value 'Expanded by default' selected in CMS ('showExpanded' attribute - true/false)
        """
        pass

    def test_003_verify_icons_on_module_accordion_header(self):
        """
        DESCRIPTION: Verify icons on module accordion (header)
        EXPECTED: * 'Special' or 'Enhanced' badge can be displayed if configured
        EXPECTED: OR
        EXPECTED: * # (YourCall) icon and/or 'Cash Out' icon can be displayed if available
        """
        pass

    def test_004_verify_footer_link_if_name_of_link_is_set_in_cms(self):
        """
        DESCRIPTION: Verify Footer link if name of link is set in CMS
        EXPECTED: *   Link is displayed at bottom of module section
        EXPECTED: *   Text of link corresponds to text set in 'Footer link text' field in CMS ('text' attribute)
        """
        pass

    def test_005_verify_footer_link_if_name_of_link_is_not_set_in_cms(self):
        """
        DESCRIPTION: Verify Footer link if name of link is NOT set in CMS
        EXPECTED: *   Link is displayed at bottom of module section
        EXPECTED: *   Footer link is shown in the format:
        EXPECTED: **View All &lt;number of all events&gt; &lt;name of module&gt; Events**
        """
        pass

    def test_006_verify_number_of_events(self):
        """
        DESCRIPTION: Verify Number of Events
        EXPECTED: It is number of all existing events for verified ID of **Type**/*Market/Class*... depending on value selected in 'Select Events by' and 'Max Events to Display' fields
        """
        pass

    def test_007_clicktap_footer_link(self):
        """
        DESCRIPTION: Click/Tap Footer link
        EXPECTED: User is redirected to the url set in 'Footer link URL' field in CMS ('url' attribute - e.g. football/today)
        """
        pass
