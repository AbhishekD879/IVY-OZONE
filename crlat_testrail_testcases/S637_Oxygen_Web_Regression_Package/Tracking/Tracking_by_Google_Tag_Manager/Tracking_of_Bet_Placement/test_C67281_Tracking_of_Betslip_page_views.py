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
class Test_C67281_Tracking_of_Betslip_page_views(Common):
    """
    TR_ID: C67281
    NAME: Tracking of Betslip page views
    DESCRIPTION: This test case verifies tracking of Betslip page views
    PRECONDITIONS: 1. User is logged out
    PRECONDITIONS: 2. Betslip is empty
    PRECONDITIONS: 3. Open console
    PRECONDITIONS: 4. Test case should be run on Mobile only
    PRECONDITIONS: 5. In order to add selection to Betslip via deep link enter in URL:
    PRECONDITIONS: domain/betslip/add/outcome_ID,outcome_ID
    PRECONDITIONS: where domain is:
    PRECONDITIONS: invictus.coral.co.uk
    PRECONDITIONS: bet-tst2.coral.co.uk
    PRECONDITIONS: bet-stg2.coral.co.uk
    PRECONDITIONS: bet.coral.co.uk
    PRECONDITIONS: outcome_ID can be find in SS response:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: - XXX - the event ID
    PRECONDITIONS: - X.XX - current supported version of OpenBet release
    PRECONDITIONS: - LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_load_oxygen_app_on_mobile_device(self):
        """
        DESCRIPTION: Load Oxygen app on Mobile device
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_open_slide_out_betslip(self):
        """
        DESCRIPTION: Open slide-out Betslip
        EXPECTED: - Betslip is opened
        EXPECTED: - No selections are present in the Betslip
        """
        pass

    def test_003_type_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console **'dataLayer'**, tap 'Enter' and check the response
        EXPECTED: The next static parameters are present:
        EXPECTED: dataLayer.push( {
        EXPECTED: 'event' : 'trackPageview',
        EXPECTED: 'virtualUrl' : '/betslip-receipt' });
        """
        pass

    def test_004_clear_slide_out_betslip(self):
        """
        DESCRIPTION: Clear slide-out Betslip
        EXPECTED: 
        """
        pass

    def test_005_open_new_browser_tab(self):
        """
        DESCRIPTION: Open new browser tab
        EXPECTED: 
        """
        pass

    def test_006_add_selection_from_some_sportrace_and_open_slide_out_betslip(self):
        """
        DESCRIPTION: Add selection from some <Sport>/<Race> and open slide-out Betslip
        EXPECTED: - Betslip is opened
        EXPECTED: - Selection is added to Betslip successfully
        """
        pass

    def test_007_repeat_step_3___5(self):
        """
        DESCRIPTION: Repeat step #3 - 5
        EXPECTED: 
        """
        pass

    def test_008_add_selection_from_some_sportrace__to_betslip_via_deep_link(self):
        """
        DESCRIPTION: Add selection from some <Sport>/<Race>  to Betslip via **deep link**
        EXPECTED: - Betslip is opened
        EXPECTED: - Selection is added to Betslip successfully
        """
        pass

    def test_009_repeat_step_3___5(self):
        """
        DESCRIPTION: Repeat step #3 - 5
        EXPECTED: 
        """
        pass

    def test_010_add_selection_from_inspired_virtual_sports_and_open_slide_out_betslip(self):
        """
        DESCRIPTION: Add selection from **Inspired Virtual Sports** and open slide-out Betslip
        EXPECTED: 
        """
        pass

    def test_011_repeat_step_3_5(self):
        """
        DESCRIPTION: Repeat step #3-5
        EXPECTED: 
        """
        pass

    def test_012_add_race_selection_from_next_module_from_race_landing_page(self):
        """
        DESCRIPTION: Add <Race> selection from **Next module** from <Race> Landing page
        EXPECTED: - Betslip is opened automatically
        EXPECTED: - Selection is added to Betslip successfully
        """
        pass

    def test_013_repeat_step_3(self):
        """
        DESCRIPTION: Repeat step #3
        EXPECTED: 
        """
        pass

    def test_014_add_race_selection_from_next_races_tab_from_module_selector_ribbon_on_homepage(self):
        """
        DESCRIPTION: Add <Race> selection from **Next Races tab** from Module Selector ribbon on Homepage
        EXPECTED: - Slide-out Betslip is opened automatically
        EXPECTED: - Selection is added to Betslip successfully
        """
        pass

    def test_015_repeat_step_3(self):
        """
        DESCRIPTION: Repeat step #3
        EXPECTED: 
        """
        pass

    def test_016_log_in_and_repeat_steps_2_17(self):
        """
        DESCRIPTION: Log in and repeat steps #2-17
        EXPECTED: 
        """
        pass
