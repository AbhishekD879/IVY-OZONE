import { PriceOddsButtonService } from '@shared/components/priceOddsButton/price-odds-button.service';

describe('PriceOddsButtonService', () => {
  let service: PriceOddsButtonService;

  const outcome = {
    name: 'Outcome',
    prices: [{
      priceType: 'LP'
    }]
  } as any;

  beforeEach(() => {
    service = new PriceOddsButtonService();
  });

  describe('@isRacingOutcome', () => {

    it('should check if it is Racing Outcome = false', () => {
      const result = service.isRacingOutcome(outcome, 'LP');
      expect(result).toBe(false);
    });

    it('should check if it is Racing Outcome (price - SP) = true', () => {
      const result = service.isRacingOutcome(outcome, 'SP');
      expect(result).toBe(true);
    });

    it('should check if it is Racing Outcome (correctPriceType - SP) = true', () => {
      const outcomeTest = {
        name: 'Outcome',
        correctPriceType: 'SP'
      } as any;
      const result = service.isRacingOutcome(outcomeTest, 'LP');
      expect(result).toBe(true);
    });

    it('should check if it is Racing Outcome (no prices !outcome.prices[0]) = true', () => {
      const outcomeTest = {
        name: 'Outcome'
      } as any;
      const result = service.isRacingOutcome(outcomeTest, 'LP, SP');
      expect(result).toBe(true);
    });

    it('should check if it is Racing Outcome (Unnamed Favourite) = true', () => {
      const outcomeTest = {
        name: 'Unnamed Favourite',
        prices: [{
          priceType: 'LP'
        }]
      } as any;
      const result = service.isRacingOutcome(outcomeTest, 'LP');
      expect(result).toBe(true);
    });

    it('should check if it is Racing Outcome (isFavourite) = true', () => {
      const outcomeTest = {
        name: 'Outcome',
        isFavourite: true,
        prices: [{
          priceType: 'LP'
        }]
      } as any;
      const result = service.isRacingOutcome(outcomeTest, 'LP');
      expect(result).toBe(true);
    });
  });
});
