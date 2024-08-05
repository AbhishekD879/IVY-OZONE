import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.promotions_banners_offers
@vtest
class Test_C1682746_Cookie_banner_style_depends_on_GDPR_switcher_state(Common):
    """
    TR_ID: C1682746
    NAME: Cookie banner style depends on GDPR switcher state
    DESCRIPTION: 
    PRECONDITIONS: All cookies and cache are cleared
    PRECONDITIONS: GDPR is switcher on CMS:
    PRECONDITIONS: System Configuration > GDPR "enable" checkbox
    PRECONDITIONS: Cookie banner text static block on CMS:
    PRECONDITIONS: Static blocks > Cookie banner
    PRECONDITIONS: Zeplin design https://app.zeplin.io/project/5ac37e9d4ac0ecde47797e8d/screen/5acf2227b6c6d88484ad572c
    PRECONDITIONS: Make sure that Cookie Banner **is NOT DISPLAYED** on Coral iOS wrapper v.5.1.1 build 1157 and higher regardless of the CMS configuration (BMA-46701).
    """
    keep_browser_open = True

    def test_001_load_oxygen_app_when_gdpr_switcher_id_off(self):
        """
        DESCRIPTION: Load Oxygen app when GDPR switcher id OFF
        EXPECTED: Homepage is opened and Cookie banner is shown and old Cookie banner is shown as described in test case [C46541] [1]
        EXPECTED: [1]:https://ladbrokescoral.testrail.com/index.php?/cases/view/46541
        """
        pass

    def test_002_switch_gdpr_feature_on_and_refresh_the_app(self):
        """
        DESCRIPTION: Switch GDPR feature ON and refresh the app
        EXPECTED: New Cookie banner styling is applied
        """
        pass

    def test_003_verify_new_cookie_banner_styling(self):
        """
        DESCRIPTION: Verify new Cookie banner styling
        EXPECTED: - Header "Updated Policies"
        EXPECTED: - CMS configurable text
        EXPECTED: - Accept button
        """
        pass

    def test_004_tap_accept_button(self):
        """
        DESCRIPTION: Tap Accept button
        EXPECTED: Cookie banner is closed
        """
        pass
