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
class Test_C902622_Add_new_Signposting_Promotion_in_CMS(Common):
    """
    TR_ID: C902622
    NAME: Add new Signposting Promotion in CMS
    DESCRIPTION: This test case verifies adding and displaying new promotion
    DESCRIPTION: **Jira tickets:**
    DESCRIPTION: BMA-22866 CMS Additional Functionality for Promotional Signposting Phase 1
    DESCRIPTION: [BMA-33420 Promo / Signposting : CMS Story for Promo Title and Text] [1]
    DESCRIPTION: [FE: BOG (Best Odds Guaranteed) Signposting (Phase 1)] [2]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-33420
    DESCRIPTION: [2]: https://jira.egalacoral.com/browse/BMA-49331
    PRECONDITIONS: To load CMS use the next link:
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
    PRECONDITIONS: * **Priceboost** - MKTFLAG_PB
    PRECONDITIONS: * **MoneyBack** - MKTFLAG_MB
    PRECONDITIONS: * **#YourCall** - YOUR_CALL (YourCall is not configurable in OpenBet TI on market lvl)
    PRECONDITIONS: * **BOG** - MKTFLAG_BOG
    PRECONDITIONS: Event-level flags for different promotions:
    PRECONDITIONS: * **Double Your Winnings** - EVFLAG_DYW
    PRECONDITIONS: * **Faller’s Insurance** - EVFLAG_FIN
    PRECONDITIONS: * **Beaten by a Length** - EVFLAG_BBL
    PRECONDITIONS: * **Extra Place Race** - EVFLAG_EPR
    PRECONDITIONS: * **Priceboost** - EVFLAG_PB
    PRECONDITIONS: * **MoneyBack** - EVFLAG_MB
    PRECONDITIONS: * **#YourCall** - EVFLAG_YC
    PRECONDITIONS: * **BOG** - EVFLAG_BOG
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
        EXPECTED: * 'Pop-up title' field is present (empty by default / field is required if 'Is Signposting Promotion' checkbox is checked)
        EXPECTED: * 'Pop-up text' field is present (empty by default / field is required if 'Is Signposting Promotion' checkbox is checked)
        """
        pass

    def test_003_check_is_signposting_promotion_checkbox(self):
        """
        DESCRIPTION: Check 'Is Signposting Promotion' checkbox
        EXPECTED: 'Is Signposting Promotion' checkbox is checked
        """
        pass

    def test_004_fill_all_promo_signposting_fields_in_signposting_promotion_section_and_save_changes(self):
        """
        DESCRIPTION: Fill all Promo Signposting fields in 'Signposting Promotion' section and save changes
        EXPECTED: * All fields are filled
        EXPECTED: * Success message appears
        """
        pass

    def test_005_repeat_steps_3_4_for_fallers_insurance_promo_double_your_winnings_promo_beaten_by_a_length_promo_extra_place_race_promo_priceboost_promo_moneyback_promo_yourcall_bog_promo(self):
        """
        DESCRIPTION: Repeat steps 3-4 for:
        DESCRIPTION: * Faller's Insurance promo
        DESCRIPTION: * Double Your Winnings promo
        DESCRIPTION: * Beaten by a Length promo
        DESCRIPTION: * Extra Place Race promo
        DESCRIPTION: * Priceboost promo
        DESCRIPTION: * MoneyBack promo
        DESCRIPTION: * #YourCall
        DESCRIPTION: * BOG promo
        EXPECTED: 
        """
        pass
