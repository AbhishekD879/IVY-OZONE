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
class Test_C13339798_CMS_Verify_Enabling_Enable_International_Totepools_On_RaceCard_toggle(Common):
    """
    TR_ID: C13339798
    NAME: [CMS] Verify Enabling ‘Enable_International_Totepools_On_RaceCard' toggle
    DESCRIPTION: This Test case verifies enabling ‘Enable_International_Totepools_On_RaceCard' toggle in CMS
    PRECONDITIONS: Preconditions:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+link+International+Tote+events+with+Regular+Horse+Racing+events
    PRECONDITIONS: Regular Horse Racing event is linked to the International Tote event
    PRECONDITIONS: -  -  -  -
    PRECONDITIONS: * Checkbox Enable_ International_ Totepools is __disabled__
    PRECONDITIONS: * Checkbox Enable_International_Totepools_On_RaceCard is __disabled__
    PRECONDITIONS: * International Tote Carousel should not be shown on the Horse Races Landing Page within International section (below UK&IRE section)
    PRECONDITIONS: * Tote Pool Tabs on the Race card for the relevant races should not be shown
    """
    keep_browser_open = True

    def test_001__navigate_to_the_cms__system_config__internationaltotepool_enable_enable__international__totepools_checkbox_enable_enable__international__totepools_on_racecard_checkbox(self):
        """
        DESCRIPTION: * Navigate to the CMS > System Config > InternationalTotePool
        DESCRIPTION: * Enable 'Enable_ International_ Totepools' checkbox
        DESCRIPTION: * Enable 'Enable_ International_ Totepools_On_RaceCard' checkbox
        EXPECTED: * Changes are submitted successfully
        EXPECTED: * 'Enable_ International_ Totepools' and ''Enable_ International_ Totepools_On_RaceCard' ' are enabled within Oxygen app
        """
        pass

    def test_002__navigate_to_the_horse_races_landing_page_to_feature_tab_and_scroll_down_to_international_tote_section(self):
        """
        DESCRIPTION: * Navigate to the Horse Races Landing page to Feature tab and scroll down to International Tote section
        EXPECTED: * International Tote pool Carousel is displayed
        """
        pass

    def test_003__tap_on_any_event_of_the_international_tote_carousel_which_is_not_finished(self):
        """
        DESCRIPTION: * Tap on any event of the International Tote carousel (which is not finished)
        EXPECTED: * User is navigated to the Race card of respective Meeting
        EXPECTED: * 'Tote Pool' Tab should be selected
        EXPECTED: * First default pool should be selected and content is loaded
        """
        pass
