from voltron.pages.shared.dialogs.dialog_contents.odds_boost_on_login import OddsBoostOnLogin


class OddsBoostLadbrokes(OddsBoostOnLogin):

    def close_dialog(self):
        self.thanks_link.click()
        self.wait_dialog_closed()
