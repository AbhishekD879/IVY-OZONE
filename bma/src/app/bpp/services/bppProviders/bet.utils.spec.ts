import { BetUtils } from './bet.utils';
import { IBet } from '@app/bpp/services/bppProviders/bpp-providers.model';

describe('BetUtils', () => {
  describe('isOffer', () => {
    it('should return true if bet is an offer', () => {
      const bet = { isOffer: 'Y'} as IBet;

      expect(BetUtils.isOffer(bet)).toBe(true);
    });

    it('should return false if bet is not an offer', () => {
      const bet = { isOffer: 'N'} as IBet;

      expect(BetUtils.isOffer(bet)).toBe(false);
    });
  });
});
