from voltron.pages.shared.components.preferences_overlay import PreferencesOverlay


class PreferencesOverlayLadbrokes(PreferencesOverlay):
    # TODO https://jira.egalacoral.com/browse/VOL-1746
    _save_preferences_button = 'xpath=.//button[contains(text(), "SAVE MY PREFERENCES")]'
