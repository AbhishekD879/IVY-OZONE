import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.promotions_banners_offers
@vtest
class Test_C918338_Verify_adding_and_displaying_new_Signposting_Promotions(Common):
    """
    TR_ID: C918338
    NAME: Verify adding and displaying new Signposting Promotions
    DESCRIPTION: This test case verifies adding and displaying new Signposting Promotion
    DESCRIPTION: AUTOTESTS https://ladbrokescoral.testrail.com/index.php?/suites/view/3779&group_by=cases:section_id&group_order=asc&group_id=739508
    PRECONDITIONS: * For verification on **Native** **Home** **page** (step 13) please create appropriate Featured tab module with Sport/Race events/selections
    PRECONDITIONS: * To load CMS use the next link:
    PRECONDITIONS: https://coral-cms- **CMS_ENDPOINT** .symphony-solutions.eu
    PRECONDITIONS: where CMS_ENDPOINT can be found using devlog
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    PRECONDITIONS: **Link to TST2 TI** (where is configurable promotions on event/market levels):
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/ti/hierarchy/event/xxxxxxx
    PRECONDITIONS: WHERE:
    PRECONDITIONS: xxxxxxx - OpenBet event ID
    PRECONDITIONS: **Link to response on TST2 endpoints:**
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/x.xx/EventToOutcomeForEvent/yyyyyyy?translationLang=en
    PRECONDITIONS: WHERE:
    PRECONDITIONS: x.xx is the current version of SiteServer
    PRECONDITIONS: yyyyyyy is the OpenBet event ID
    PRECONDITIONS: The variable is containing promotion flags for the event: <drilldownTagNames>
    PRECONDITIONS: Market-level flags for different promotions:
    PRECONDITIONS: * **Double Your Winnings** - MKTFLAG_DYW
    PRECONDITIONS: * **Faller’s Insurance** - MKTFLAG_FI
    PRECONDITIONS: * **Beaten by a Length** - MKTFLAG_BBAL
    PRECONDITIONS: * **Extra Place Race** - MKTFLAG_EPR
    PRECONDITIONS: * **#YourCall** - YOUR_CALL (YourCall is not configurable in OpenBet TI on event/market lvl's)
    PRECONDITIONS: * **Price Boost** - MKTFLAG_PB
    PRECONDITIONS: Event-level flags for different promotions:
    PRECONDITIONS: * **Double Your Winnings** - EVFLAG_DYW
    PRECONDITIONS: * **Faller’s Insurance** - EVFLAG_FIN
    PRECONDITIONS: * **Beaten by a Length** - EVFLAG_BBL
    PRECONDITIONS: * **Extra Place Race** - EVFLAG_EPR
    PRECONDITIONS: * **#YourCall** - EVFLAG_YC
    PRECONDITIONS: * **Price Boost** - EVFLAG_PB
    PRECONDITIONS: An example:
    PRECONDITIONS: "drilldownTagNames":"EVFLAG_FIN,EVFLAG_DYW,"
    """
    keep_browser_open = True

    def test_001_click_plus_create_promotion_button_on_promotion_section_in_cms(self):
        """
        DESCRIPTION: Click "+ Create Promotion" button on Promotion section in CMS
        EXPECTED: "Create Promotion" page is opened
        """
        pass

    def test_002_verify_promo_signposting_fields_in_signposting_promotion_section(self):
        """
        DESCRIPTION: Verify Promo Signposting fields in 'Signposting Promotion' section
        EXPECTED: * 'Is Signposting Promotion' checkbox is present (unchecked by default)
        EXPECTED: * 'Event-level flag' field is present (empty by default)
        EXPECTED: * 'Market-level flag' field is present (empty by default)
        EXPECTED: * 'Overlay BET NOW button url' field is present (empty by default)
        EXPECTED: * 'Include VIP Levels' field is present (empty by default)
        EXPECTED: * 'Opt In Request ID' field is present (empty by default)
        EXPECTED: * 'Show To Customer' drop-down selector is present (empty by default)
        EXPECTED: * 'Category' drop-down selector is present (empty by default)
        EXPECTED: * 'Pop-up title' field is present (empty by default / field is required if 'Is Signposting Promotion' checkbox is checked)
        EXPECTED: * 'Pop-up text' field is present (empty by default / field is required if 'Is Signposting Promotion' checkbox is checked)
        """
        pass

    def test_003_fill_all_required_fields(self):
        """
        DESCRIPTION: Fill all required fields
        EXPECTED: All required fields are filled
        """
        pass

    def test_004_check_is_signposting_promotion_checkbox_and_fill_all_fields_from_signposting_promotion_section_with_valid_data_and_save_changesfor_market_level_and_event_level_flags_use_values_from_preconditions(self):
        """
        DESCRIPTION: Check 'Is Signposting Promotion' checkbox and fill all fields from 'Signposting Promotion' section with valid data and save changes
        DESCRIPTION: (For Market-level and Event-level flags use values from preconditions)
        EXPECTED: * 'Is Signposting Promotion' checkbox is checked
        EXPECTED: * All fields are filled
        EXPECTED: * Success message appears
        """
        pass

    def test_005_navigate_to_the_promotions_page_and_verify_presence_of_just_added_promotions(self):
        """
        DESCRIPTION: Navigate to the 'Promotions' page and verify presence of just added Promotions
        EXPECTED: * 'Promotions' page is opened
        EXPECTED: * Just added Promotions is shown on 'Promotions' page
        EXPECTED: * Current Promotion is displayed within correct uploaded image
        EXPECTED: * All data is displayed according to CMS
        """
        pass

    def test_006_navigate_to_some_racesport_page_with_event_that_contain_current_promotion(self):
        """
        DESCRIPTION: Navigate to some <Race/Sport> page with Event that contain current Promotion
        EXPECTED: <Race/Sport> page is opened
        """
        pass

    def test_007_tap_on_a_promotion_icon_on_any_racesport_page(self):
        """
        DESCRIPTION: Tap on a Promotion icon on any <Race/Sport> page
        EXPECTED: * Promo Signposting Pop-up appear
        EXPECTED: * Pop-up title corresponds to the 'Pop-up title' section in CMS (for current promo CMS configuration)
        EXPECTED: * Pop-up text corresponds to the 'Pop-up text' section in CMS (for current promo CMS configuration)
        EXPECTED: * 'MORE' button is present on pop-up
        EXPECTED: * 'OK' button is present on pop-upc
        """
        pass

    def test_008_click_on_more_button_on_promo_signposting_pop_up(self):
        """
        DESCRIPTION: Click on 'MORE' button on Promo Signposting Pop-up
        EXPECTED: Promo Signposting overlay is displayed
        """
        pass

    def test_009_verify_fields_on_promo_signposting_overlay_that_related_to_the_signposting_promotion(self):
        """
        DESCRIPTION: Verify fields on Promo Signposting overlay that related to the 'Signposting Promotion'
        EXPECTED: * Short description is the same as on the 'Short Description' field in CMS (for current promo CMS configuration)
        EXPECTED: * Promotion Main content is the same as on the 'Description field in CMS (for current promo CMS configuration)
        EXPECTED: * 'BET NOW' button navigate to the same page what mentioned on the 'Overlay BET NOW button url' field in CMS (for current promo CMS configuration)
        """
        pass

    def test_010_close_the_promo_signposting_overlay(self):
        """
        DESCRIPTION: Close the Promo Signposting overlay
        EXPECTED: Promo Signposting overlay is closed
        """
        pass

    def test_011_tap_on_a_promotion_icon_again(self):
        """
        DESCRIPTION: Tap on a Promotion icon again
        EXPECTED: Promo Signposting Pop-up appear
        """
        pass

    def test_012_click_on_ok_button_on_promo_signposting_pop_up(self):
        """
        DESCRIPTION: Click on 'OK' button on Promo Signposting Pop-up
        EXPECTED: Promo Signposting Pop-up is closed
        """
        pass

    def test_013_repeat_steps_3_11_for_fallers_insurance_promo_double_your_winnings_promo_beaten_by_a_length_promo_extra_place_race_promo_yourcall_smart_boostprice_boost(self):
        """
        DESCRIPTION: Repeat steps 3-11 for:
        DESCRIPTION: * Faller's Insurance promo
        DESCRIPTION: * Double Your Winnings promo
        DESCRIPTION: * Beaten by a Length promo
        DESCRIPTION: * Extra Place Race promo
        DESCRIPTION: * #YourCall
        DESCRIPTION: * Smart Boost(Price Boost)
        EXPECTED: 
        """
        pass

    def test_014_repeat_steps_6_11_on_native_home_page(self):
        """
        DESCRIPTION: Repeat steps 6-11 on Native Home page
        EXPECTED: 
        """
        pass
