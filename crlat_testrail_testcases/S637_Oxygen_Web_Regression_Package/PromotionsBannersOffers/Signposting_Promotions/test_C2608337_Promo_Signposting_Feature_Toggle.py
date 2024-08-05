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
class Test_C2608337_Promo_Signposting_Feature_Toggle(Common):
    """
    TR_ID: C2608337
    NAME: Promo Signposting Feature Toggle
    DESCRIPTION: This test case verifies Promo Signposting Feature Toggle
    DESCRIPTION: **Jira tickets:**
    DESCRIPTION: [BMA-35684 Promo/Signposting: Feature Toggle] [1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-35684
    PRECONDITIONS: * Promo Signposting should be configured in the CMS for all promotions (CMS -> Promotions -> Promotions -> Promotion's Title link or 'Create Promotion' button)
    PRECONDITIONS: * Promo Signposting should be added on event/market level for any Sport/Race for all promotions
    PRECONDITIONS: * Feature Toggle config should be added in the System Configuration for Promo Signposting (CMS -> System configuration -> Structure -> FeatureToggle -> PromoSignposting)
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
    """
    keep_browser_open = True

    def test_001_check_config_for_promo_signposting_feature_toggle(self):
        """
        DESCRIPTION: Check config for Promo Signposting Feature Toggle
        EXPECTED: 'Promo Signposting' config is added in 'Feature Toggle' System configuration
        """
        pass

    def test_002_check_promo_signposting_checkbox_and_save_changes(self):
        """
        DESCRIPTION: Check 'Promo Signposting' checkbox and save changes
        EXPECTED: * Changes are saved successfully
        EXPECTED: * 'Promo Signposting' checkbox is checked on CMS
        """
        pass

    def test_003_check_if_signposting_promotions_icons_are_present_for__extra_place_priceboost_moneyback_double_your_winnings_beaten_by_a_length_fallers_insurance(self):
        """
        DESCRIPTION: Check if Signposting Promotions icons are present for :
        DESCRIPTION: * 'Extra Place'
        DESCRIPTION: * 'Priceboost'
        DESCRIPTION: * 'MoneyBack'
        DESCRIPTION: * 'Double Your Winnings'
        DESCRIPTION: * 'Beaten by a Length'
        DESCRIPTION: * 'Faller's Insurance'
        EXPECTED: * All signposting promotion icons are shown on the app
        EXPECTED: * Promo Signposting feature works as expected (promo pop-up and overlay are appeared)
        """
        pass

    def test_004_uncheck_promo_signposting_checkbox_and_save_changes(self):
        """
        DESCRIPTION: Uncheck 'Promo Signposting' checkbox and save changes
        EXPECTED: * Changes are saved successfully
        EXPECTED: * 'Promo Signposting' checkbox is unchecked on CMS
        """
        pass

    def test_005_check_if_signposting_promotions_icons_are_present_for__extra_place_priceboost_moneyback_double_your_winnings_beaten_by_a_length_fallers_insurance(self):
        """
        DESCRIPTION: Check if Signposting Promotions icons are present for :
        DESCRIPTION: * 'Extra Place'
        DESCRIPTION: * 'Priceboost'
        DESCRIPTION: * 'MoneyBack'
        DESCRIPTION: * 'Double Your Winnings'
        DESCRIPTION: * 'Beaten by a Length'
        DESCRIPTION: * 'Faller's Insurance'
        EXPECTED: * All signposting promotion icons are **NOT** shown on the app
        """
        pass
