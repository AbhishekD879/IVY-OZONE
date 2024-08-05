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
class Test_C2604508_Verify_just_added_Signposting_Promotion(Common):
    """
    TR_ID: C2604508
    NAME: Verify just added Signposting Promotion
    DESCRIPTION: This test case verifies adding and displaying new promotion
    DESCRIPTION: **Jira tickets:**
    DESCRIPTION: BMA-22866 CMS Additional Functionality for Promotional Signposting Phase 1
    DESCRIPTION: [BMA-33420 Promo / Signposting : CMS Story for Promo Title and Text] [1]
    DESCRIPTION: [FE: BOG (Best Odds Guaranteed) Signposting (Phase 1)] [2]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-33420
    DESCRIPTION: [2]: https://jira.egalacoral.com/browse/BMA-49331
    PRECONDITIONS: * Promo Signposting should be configured in the CMS
    PRECONDITIONS: * Promo Signposting should be added on event/market level for any Sport/Race
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
    PRECONDITIONS: * **Double Your Winnings** - MKTFLAG_DYW (Coral only)
    PRECONDITIONS: * **Faller’s Insurance** - MKTFLAG_FIN
    PRECONDITIONS: * **Beaten by a Length** - MKTFLAG_BBAL (Coral only)
    PRECONDITIONS: * **Extra Place Race** - MKTFLAG_EPR
    PRECONDITIONS: * **Priceboost** - MKTFLAG_PB
    PRECONDITIONS: * **MoneyBack** - MKTFLAG_MB
    PRECONDITIONS: * **#YourCall** - YOUR_CALL (YourCall is not configurable in OpenBet TI on market lvl)  (Coral only)
    PRECONDITIONS: * **BOG** - MKTFLAG_BOG
    PRECONDITIONS: Event-level flags for different promotions:
    PRECONDITIONS: * **Double Your Winnings** - EVFLAG_DYW (Coral only)
    PRECONDITIONS: * **Faller’s Insurance** - EVFLAG_FIN
    PRECONDITIONS: * **Beaten by a Length** - EVFLAG_BBL  (Coral only)
    PRECONDITIONS: * **Extra Place Race** - EVFLAG_EPR
    PRECONDITIONS: * **Priceboost** - EVFLAG_PB
    PRECONDITIONS: * **MoneyBack** - EVFLAG_MB
    PRECONDITIONS: * **#YourCall** - EVFLAG_YC (Coral only)
    PRECONDITIONS: * **BOG** - EVFLAG_BOG
    PRECONDITIONS: An example:
    PRECONDITIONS: "drilldownTagNames":"EVFLAG_FIN,EVFLAG_DYW,"
    """
    keep_browser_open = True

    def test_001_navigate_to_the_promotions_page_and_verify_presence_of_just_added_promotions(self):
        """
        DESCRIPTION: Navigate to the 'Promotions' page and verify presence of just added Promotions
        EXPECTED: * 'Promotions' page is opened
        EXPECTED: * Just added Promotions is shown on 'Promotions' page
        EXPECTED: * Current Promotion is displayed within correct uploaded image
        EXPECTED: * All data is displayed according to CMS
        """
        pass

    def test_002_navigate_to_some_racesport_page_with_event_that_contain_current_promotion(self):
        """
        DESCRIPTION: Navigate to some <Race/Sport> page with Event that contain current Promotion
        EXPECTED: <Race/Sport> page is opened
        """
        pass

    def test_003_tap_on_a_promotion_icon_on_any_racesport_page(self):
        """
        DESCRIPTION: Tap on a Promotion icon on any <Race/Sport> page
        EXPECTED: * Promo Signposting Pop-up appear
        EXPECTED: * Pop-up title corresponds to the 'Pop-up title' section in CMS (for current promo CMS configuration)
        EXPECTED: * Pop-up text corresponds to the 'Pop-up text' section in CMS (for current promo CMS configuration)
        EXPECTED: * 'MORE' button is present on pop-up  (Coral only)
        EXPECTED: * 'OK' button is present on pop-up
        """
        pass

    def test_004_click_on_more_button_on_promo_signposting_pop_up__coral_only(self):
        """
        DESCRIPTION: Click on 'MORE' button on Promo Signposting Pop-up  (Coral only)
        EXPECTED: Promo Signposting overlay is displayed
        """
        pass

    def test_005_verify_fields_on_promo_signposting_overlay_that_related_to_the_signposting_promotion__coral_only(self):
        """
        DESCRIPTION: Verify fields on Promo Signposting overlay that related to the 'Signposting Promotion'  (Coral only)
        EXPECTED: * Short description is the same as on the 'Short Description' field in CMS (for current promo CMS configuration)
        EXPECTED: * Promotion Main content is the same as on the 'Description field in CMS (for current promo CMS configuration)
        EXPECTED: * 'BET NOW' button navigate to the same page what mentioned on the 'Overlay BET NOW button url' field in CMS (for current promo CMS configuration)
        """
        pass

    def test_006_close_the_promo_signposting_overlay(self):
        """
        DESCRIPTION: Close the Promo Signposting overlay
        EXPECTED: Promo Signposting overlay is closed
        """
        pass

    def test_007_tap_on_a_promotion_icon_again(self):
        """
        DESCRIPTION: Tap on a Promotion icon again
        EXPECTED: Promo Signposting Pop-up appear
        """
        pass

    def test_008_click_on_ok_button_on_promo_signposting_pop_up(self):
        """
        DESCRIPTION: Click on 'OK' button on Promo Signposting Pop-up
        EXPECTED: Promo Signposting Pop-up is closed
        """
        pass

    def test_009_repeat_steps_8_17_for_fallers_insurance_promo_double_your_winnings_promo_coral_only_beaten_by_a_length_promo_coral_only_extra_place_race_promo_priceboost_promo_moneyback_promo_yourcall_coral_only_bog_promo(self):
        """
        DESCRIPTION: Repeat steps 8-17 for:
        DESCRIPTION: * Faller's Insurance promo
        DESCRIPTION: * Double Your Winnings promo (Coral only)
        DESCRIPTION: * Beaten by a Length promo (Coral only)
        DESCRIPTION: * Extra Place Race promo
        DESCRIPTION: * Priceboost promo
        DESCRIPTION: * Moneyback promo
        DESCRIPTION: * #YourCall (Coral only)
        DESCRIPTION: * BOG promo
        EXPECTED: 
        """
        pass
