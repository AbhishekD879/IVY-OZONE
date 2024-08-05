from voltron.pages.shared.contents.football import Football


class RugbyLeague(Football):
    _url_pattern = r'^https?:\/\/.+\/rugby-league(\/)?(live|matches|competitions|specials|coupons|outrights)?(\/)?(today|tomorrow|future)?'
