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
class Test_C48473969_Verify_CMS_configuration_for_BOG_signposting_and_Pop_up(Common):
    """
    TR_ID: C48473969
    NAME: Verify CMS configuration for BOG signposting and  Pop-up
    DESCRIPTION: This test case verifies configuration for BOG signposting and  Pop-up
    DESCRIPTION: **Jira ticket:**
    DESCRIPTION: [https://jira.egalacoral.com/browse/BMA-49331]
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_go_to_cms__system_configuration__config_sectioncreate_new_config_with_configurations__field_name_bogtoggle__field_type_checkbox__set_default_value_to_truesave_changes(self):
        """
        DESCRIPTION: Go to 'CMS > System-configuration > Config' section
        DESCRIPTION: Create New Config with configurations:
        DESCRIPTION: - Field Name 'bogToggle'
        DESCRIPTION: - Field Type 'checkbox'
        DESCRIPTION: - Set 'Default value' to True
        DESCRIPTION: Save Changes
        EXPECTED: Config is created and saved successfully
        """
        pass

    def test_002_go_to_cms__promotions__promotions_sectioncreate_new_promotion_with_configurations__set_checkbox_for_is_signposting_promotion_to_true__enter_evflag_bog_value_for_event_level_flag__enter_mktflag_bog_value_for_market_level_flag__fill_in_popup_title_field__fill_in_popup_text_fieldsave_changes(self):
        """
        DESCRIPTION: Go to 'CMS > Promotions > Promotions' section
        DESCRIPTION: Create New Promotion with configurations:
        DESCRIPTION: - Set checkbox for 'Is Signposting Promotion' to True
        DESCRIPTION: - Enter 'EVFLAG_BOG' value for 'Event-level flag'
        DESCRIPTION: - Enter 'MKTFLAG_BOG' value for 'Market-level flag'
        DESCRIPTION: - Fill in 'Popup Title' field
        DESCRIPTION: - Fill in 'Popup Text' field
        DESCRIPTION: Save Changes
        EXPECTED: Promotion is created and saved successfully
        """
        pass

    def test_003_verify_displaying_bog_on_coralladbrokes_ui(self):
        """
        DESCRIPTION: Verify displaying BOG on Coral/Ladbrokes UI
        EXPECTED: BOG icon is displayed on Horse Racing Grids, Horse Racing EDP, Bet Receipt and
        EXPECTED: Cash out, Open bets, Settle bets in My Bets
        """
        pass
