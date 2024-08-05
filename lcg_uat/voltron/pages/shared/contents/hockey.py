from voltron.pages.shared.contents.football import Football


class Hockey(Football):
    _url_pattern = r'^https?:\/\/.+\/hockey(\/)?(live|matches|competitions|specials|coupons|outrights)?(\/)?(today|tomorrow|future)?'
