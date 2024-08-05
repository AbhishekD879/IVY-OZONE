from .base_market import BaseMarketEntity


class DrawNoBetMarket(BaseMarketEntity):

    def __init__(self, **kwargs):
        super(DrawNoBetMarket, self).__init__(**kwargs)
        self.market_display_sort_code = 'DN'

    def _generate_params(self):
        return ((f'name_{self.market_template_id}_{self.market_display_sort_code}', self.market_name),
                ('ev_oc_grp_id', self.market_template_id),
                ('ev_oc_grp_id_sort', f'{self.market_template_id}_{self.market_display_sort_code}'),
                (f'name_{self.market_template_id}_{self.market_display_sort_code}_disporder', self.market_disporder))
