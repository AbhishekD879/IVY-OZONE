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
class Test_C2779831_Verify_multiple_signposting_icons_rules(Common):
    """
    TR_ID: C2779831
    NAME: Verify multiple signposting icons rules
    DESCRIPTION: This test case verifies multiple signposting icons rules
    PRECONDITIONS: * Promo Signposting should be configured in the CMS
    PRECONDITIONS: * Promo Signposting should be added for event where:
    PRECONDITIONS: (1) **ONLY** Extra Place promo available on Race Event level
    PRECONDITIONS: (2) Extra Place promo **AND** some of promo signposting icon (or CashOut) are available on Race Event level
    PRECONDITIONS: (3) **ONLY** CashOut icon is available on Race Event
    PRECONDITIONS: (4) CashOut icon **AND** some of promo signposting icon are available on Race Event
    PRECONDITIONS: (5) **ONLY** BYB available for Sport Event (Coral only)
    PRECONDITIONS: (6) BYB **AND** some of promo signposting icon are available on Sport Event level (Coral only)
    PRECONDITIONS: (7) **ONLY** Smart Boost promo available on Sport Event level
    PRECONDITIONS: (8) Smart Boost **AND** some of promo signposting icon are available on Sport Event level
    PRECONDITIONS: (9) **ONLY** MoneyBack promo available on Sport Event level
    PRECONDITIONS: (10) MoneyBack **AND** some of promo signposting icon are available on Sport Event level
    PRECONDITIONS: (9) **ONLY** BOG promo available on Sport Event level
    PRECONDITIONS: (10) BOG **AND** some of promo signposting icon are available on Sport Event level
    PRECONDITIONS: **Link to TST2 TI** (where is configurable promotions on event/market levels):
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/ti/hierarchy/event/xxxxxxx
    PRECONDITIONS: WHERE:
    PRECONDITIONS: xxxxxxx - OpenBet event ID
    """
    keep_browser_open = True

    def test_001_navigate_to_the_next_races_tab_on_home_page(self):
        """
        DESCRIPTION: Navigate to the **Next Races** tab on Home page
        EXPECTED: 
        """
        pass

    def test_002_verify_extra_place_icon_and_label_on_the_race_event_card_1_from_preconditions(self):
        """
        DESCRIPTION: Verify 'Extra Place' **icon** **and** **label** on the Race Event Card (1) from Preconditions
        EXPECTED: * 'Extra Place' icon and label is displayed on Race Event Card
        """
        pass

    def test_003_verify_extra_place_and_some_other_promo_signposting_or_cashout_icons_on_the_race_event_card_2_from_preconditions(self):
        """
        DESCRIPTION: Verify 'Extra Place' and some other promo signposting (or CashOut) **icons** on the Race Event Card (2) from Preconditions
        EXPECTED: * 'Extra Place' icon ( **without** label) is displayed on Race Event Card
        EXPECTED: * Other promo signposting icon ( **without** label) is displayed on Race Event Card
        """
        pass

    def test_004_verify_cashout_icon_and_label_on_the_race_event_card_3_from_preconditions(self):
        """
        DESCRIPTION: Verify 'CashOut' **icon** **and** **label** on the Race Event Card (3) from Preconditions
        EXPECTED: * 'CashOut' icon and label is displayed on Race Event Card
        """
        pass

    def test_005_verify_cashout_and_some_of_promo_signposting_icon_on_the_race_event_card_4_from_preconditions(self):
        """
        DESCRIPTION: Verify 'CashOut' and some of promo signposting **icon** on the Race Event Card (4) from Preconditions
        EXPECTED: * 'CashOut' icon ( **without** label) is displayed on Race Event Card
        EXPECTED: * Other promo signposting icon ( **without** label) is displayed on Race Event Card
        """
        pass

    def test_006_repeat_steps_1_5_on_featured_tab_on_home_page_next_races_on_hr_landing_page(self):
        """
        DESCRIPTION: Repeat steps 1-5 on:
        DESCRIPTION: * Featured tab on Home page
        DESCRIPTION: * Next Races on HR Landing page
        EXPECTED: 
        """
        pass

    def test_007_navigate_to_the_sport_landing_page(self):
        """
        DESCRIPTION: Navigate to the Sport Landing page
        EXPECTED: 
        """
        pass

    def test_008_verify_byb_icon_and_label_on_the_sport_event_card_5_from_preconditions_coral_only(self):
        """
        DESCRIPTION: Verify 'BYB' **icon** **and** **label** on the Sport Event Card (5) from Preconditions (Coral only)
        EXPECTED: * 'BYB' icon and label is displayed on Sport Event Card
        """
        pass

    def test_009_verify_byb_and_some_other_promo_signposting_icons_on_the_sport_event_card_6_from_preconditions_coral_only(self):
        """
        DESCRIPTION: Verify 'BYB' and some other promo signposting **icons** on the Sport Event Card (6) from Preconditions (Coral only)
        EXPECTED: * 'BYB' icon ( **without** label) is displayed on Sport Event Card
        EXPECTED: * Other promo signposting icon ( **without** label) is displayed on Sport Event Card
        """
        pass

    def test_010_verify_smart_boost_icon_and_label_on_the_sport_event_card_7_from_preconditions(self):
        """
        DESCRIPTION: Verify 'Smart Boost' **icon** **and** **label** on the Sport Event Card (7) from Preconditions
        EXPECTED: * 'Smart Boost' icon and label is displayed on Sport Event Card
        """
        pass

    def test_011_verify_smart_boost_and_some_other_promo_signposting_icons_on_the_sport_event_card_8_from_preconditions(self):
        """
        DESCRIPTION: Verify 'Smart Boost' and some other promo signposting **icons** on the Sport Event Card (8) from Preconditions
        EXPECTED: * 'Smart Boost' icon ( **without** label) is displayed on Sport Event Card
        EXPECTED: * Other promo signposting icon ( **without** label) is displayed on Sport Event Card
        """
        pass

    def test_012_verify_moneyback_icon_and_label_on_the_sport_event_card_9_from_preconditions(self):
        """
        DESCRIPTION: Verify 'MoneyBack' **icon** **and** **label** on the Sport Event Card (9) from Preconditions
        EXPECTED: * 'MoneyBack' icon and label is displayed on Sport Event Card
        """
        pass

    def test_013_verify_moneyback_and_some_other_promo_signposting_icons_on_the_sport_event_card_10_from_preconditions(self):
        """
        DESCRIPTION: Verify 'MoneyBack' and some other promo signposting **icons** on the Sport Event Card (10) from Preconditions
        EXPECTED: * 'MoneyBack' icon ( **without** label) is displayed on Sport Event Card
        EXPECTED: * Other promo signposting icon ( **without** label) is displayed on Sport Event Card
        """
        pass

    def test_014_verify_bog_icon_and_label_on_the_sport_event_card_9_from_preconditions(self):
        """
        DESCRIPTION: Verify 'BOG' **icon** **and** **label** on the Sport Event Card (9) from Preconditions
        EXPECTED: * 'BOG' icon and label is displayed on Sport Event Card
        """
        pass

    def test_015_verify_bog_and_some_other_promo_signposting_icons_on_the_sport_event_card_10_from_preconditions(self):
        """
        DESCRIPTION: Verify 'BOG' and some other promo signposting **icons** on the Sport Event Card (10) from Preconditions
        EXPECTED: * 'BOG' icon ( **without** label) is displayed on Sport Event Card
        EXPECTED: * Other promo signposting icon ( **without** label) is displayed on Sport Event Card
        """
        pass

    def test_016_repeat_steps_7_13_on_featured_tab_on_home_page_in_play_tab_on_home_page_streaming_tab_on_home_page_coupons_tab_on_home_page_favourite_page(self):
        """
        DESCRIPTION: Repeat steps 7-13 on:
        DESCRIPTION: * Featured tab on Home page
        DESCRIPTION: * In-Play tab on Home page
        DESCRIPTION: * Streaming tab on Home page
        DESCRIPTION: * Coupons tab on Home page
        DESCRIPTION: * Favourite page
        EXPECTED: 
        """
        pass
