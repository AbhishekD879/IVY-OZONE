import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.betslip
@vtest
class Test_C10669039_Featured_Bet_tracking_of_adding_selection_to_Betslip_from_Featured_module_by_Type_Id(Common):
    """
    TR_ID: C10669039
    NAME: Featured Bet: tracking of adding selection to Betslip from Featured module by Type Id
    DESCRIPTION: This test case verifies GA tracking of adding selection from Featured module by Type Id on home page to Betslip
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - Betslip GA tracking documentation: https://confluence.egalacoral.com/pages/viewpage.action?pageId=91091847
    PRECONDITIONS: - Quick bet should be enabled in CMS > System Configuration > Structure > quickBet
    PRECONDITIONS: - You should have a Featured module by Type Id
    PRECONDITIONS: - You should be on Home page > Featured tab in application
    """
    keep_browser_open = True

    def test_001_mobile__tap_odds_button_within_featured_module_by_type_id__tap_add_to_betslip_button__type_datalayer_in_browsers_console_and_verify_ga_tracking_record(self):
        """
        DESCRIPTION: **Mobile**
        DESCRIPTION: - Tap ODDS button within Featured module by Type Id > tap 'ADD TO BETSLIP' button
        DESCRIPTION: - Type 'dataLayer' in browser's console and verify GA tracking record
        EXPECTED: dataLayer.push{
        EXPECTED: event: "trackEvent"
        EXPECTED: eventAction: "add to betslip"
        EXPECTED: eventCategory: "quickbet"
        EXPECTED: eventLabel: "success"
        EXPECTED: ecommerce.add.products{
        EXPECTED: brand: "<<EVENT_MARKET>>"
        EXPECTED: category: "<<OPENBET_SPORT_CATEGORY_ID>>"
        EXPECTED: dimension60: "<<EVENT_ID>>"
        EXPECTED: dimension61: "<<SELECTION_ID>>"
        EXPECTED: dimension62: "<<IN-PLAY_STATUS>>"
        EXPECTED: dimension63: "<<CUSTOMER BUILT>>"
        EXPECTED: dimension64: "HOME. FEATURED"
        EXPECTED: dimension65: "featured bet"
        EXPECTED: name: "<<EVENT_NAME>>"
        EXPECTED: variant: "<<OPENBET_TYPE_ID>>"
        EXPECTED: }}
        """
        pass

    def test_002_mobile__tap_any_another_odds_button_within_featured_module_by_type_id__type_datalayer_in_browsers_console_and_verify_ga_tracking_record(self):
        """
        DESCRIPTION: **Mobile**
        DESCRIPTION: - Tap any another ODDS button within Featured module by Type Id
        DESCRIPTION: - Type 'dataLayer' in browser's console and verify GA tracking record
        EXPECTED: dataLayer.push{
        EXPECTED: event: "trackEvent"
        EXPECTED: eventAction: "add to betslip"
        EXPECTED: eventCategory: "betslip"
        EXPECTED: eventLabel: "success"
        EXPECTED: ecommerce.add.products{
        EXPECTED: brand: "<<EVENT_MARKET>>"
        EXPECTED: category: "<<OPENBET_SPORT_CATEGORY_ID>>"
        EXPECTED: dimension60: "<<EVENT_ID>>"
        EXPECTED: dimension61: "<<SELECTION_ID>>"
        EXPECTED: dimension62: "<<IN-PLAY_STATUS>>"
        EXPECTED: dimension63: "<<CUSTOMER BUILT>>"
        EXPECTED: dimension64: "HOME. FEATURED"
        EXPECTED: dimension65: "featured bet"
        EXPECTED: name: "<<EVENT_NAME>>"
        EXPECTED: variant: "<<OPENBET_TYPE_ID>>"
        EXPECTED: }}
        """
        pass

    def test_003_mobile_tablet_and_desktop__login_and_go_to_right_menu__settings__disabled_allow_quick_bet_or_go_to_cms__system_configuration__structure__quickbet_disable_quick_bet_functionality__remove_all_selections_from_betslip__tap_odds_button_within_featured_module_by_type_id__type_datalayer_in_browsers_console_and_verify_ga_tracking_record(self):
        """
        DESCRIPTION: **Mobile, Tablet and Desktop**
        DESCRIPTION: - Login and go to Right Menu > Settings > disabled 'Allow Quick Bet' or go to CMS > System Configuration > Structure > quickBet disable Quick Bet functionality
        DESCRIPTION: - Remove all selections from betslip
        DESCRIPTION: - Tap ODDS button within Featured module by Type Id
        DESCRIPTION: - Type 'dataLayer' in browser's console and verify GA tracking record
        EXPECTED: dataLayer.push{
        EXPECTED: event: "trackEvent"
        EXPECTED: eventAction: "add to betslip"
        EXPECTED: eventCategory: "betslip"
        EXPECTED: eventLabel: "success"
        EXPECTED: ecommerce.add.products{
        EXPECTED: brand: "<<EVENT_MARKET>>"
        EXPECTED: category: "<<OPENBET_SPORT_CATEGORY_ID>>"
        EXPECTED: dimension60: "<<EVENT_ID>>"
        EXPECTED: dimension61: "<<SELECTION_ID>>"
        EXPECTED: dimension62: "<<IN-PLAY_STATUS>>"
        EXPECTED: dimension63: "<<CUSTOMER BUILT>>"
        EXPECTED: dimension64: "HOME. FEATURED"
        EXPECTED: dimension65: "featured bet"
        EXPECTED: name: "<<EVENT_NAME>>"
        EXPECTED: variant: "<<OPENBET_TYPE_ID>>"
        EXPECTED: }}
        """
        pass
