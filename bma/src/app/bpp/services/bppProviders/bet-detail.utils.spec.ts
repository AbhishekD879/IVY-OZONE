import { BetDetailUtils } from '@app/bpp/services/bppProviders/bet-detail.utils';

describe('BetDetailUtils', () => {

  describe('isCanceled', () => {

    it('should return true if stake.status is "X"', () => {
      const stake = { status: 'X' };
      expect(BetDetailUtils.isCanceled(stake as any)).toBe(true);
    });

    it('should return true if stake.status is "P"', () => {
      const stake = { status: 'P' };
      expect(BetDetailUtils.isCanceled(stake as any)).toBe(true);
    });

    it('should return false if stake.status is neither "X", neither "P"', () => {
      const stake = { status: 'A' };
      expect(BetDetailUtils.isCanceled(stake as any)).toBe(false);
    });

    it('should return true if stake.status is "A", but async is "T" (topup)', () => {
      const stake = { status: 'A', asyncAcceptStatus: 'T' };
      expect(BetDetailUtils.isCanceled(stake as any)).toBe(true);
    });

    it('should return true if stake.status is "P", and async is "T" (topup)', () => {
      const stake = { status: 'P', asyncAcceptStatus: 'T' };
      expect(BetDetailUtils.isCanceled(stake as any)).toBe(true);
    });
  });
});
