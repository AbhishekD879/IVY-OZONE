import { YourcallValidationService } from './yourcall-validation-service';

describe('YourcallValidationService', () => {
  let service: YourcallValidationService;

  beforeEach(() => {
    service = new YourcallValidationService();
  });

  it('Tests if YourcallValidation Service Created', () => {
    expect(service).toBeTruthy();
  });

  describe('#isValidSelectionCount', () => {
    it('should Validate minimum selection amount and return false', () => {
      service.dashboard = []; // empty dashboard
      const result = service.isValidSelectionCount();
      expect(result).toEqual(false);
    });

    it('should Validate minimum selection amount and return false', () => {
      service.dashboard = [ undefined ] as any; // empty dashboard
      const result = service.isValidSelectionCount();
      expect(result).toEqual(false);
    });

    it('should Validate minimum selection amount and return true', () => {
      (service.dashboard = [{
        market: {},
        selection: {}
      }, {
        market: {},
        selection: {}
      }] as any); // just to have 2 items in dashboard

      const result = service.isValidSelectionCount();
      expect(result).toEqual(true);
    });

    it('should Validate minimum selection amount and return true for player bets', () => {
      (service.dashboard = [{
        market: { grouping: 'Player Bets' },
        selection: {}
      }] as any); // just to have 1 Player Bet item in dashboard

      const result = service.isValidSelectionCount();
      expect(result).toEqual(true);
    });
  });

  describe('#validateSelection', () => {
    it('should call validateSelection method', () => {
      service.dashboard = [{
        selection: {}
      }, {
        selection: {}
      }] as any;
      const result = service.validateSelection(service.dashboard[0].selection as any);

      expect(result).toEqual(true);
    });
  });

  describe('#validate', () => {
    it('should validate whole dashboard', () => {
      service.dashboard = [{
        selection: {
          error: 'error',
          errorMessage: 'errorMessage'
        }
      }, {
        selection: {
          error: 'error',
          errorMessage: 'errorMessage'
        }
      }] as any;

      const result = service.validate();

      expect(result).toEqual(true);

      expect(service.dashboard).toEqual([{
        selection: {}
      }, {
        selection: {}
      }] as any);
    });
  });

  describe('#validatePlayerStatistic', () => {
    it('should call validatePlayerStatistic (selection.playerId = false)', () => {
      const result = service['validatePlayerStatistic']({} as any, {} as any);

      expect(result).toEqual(true);
    });

    it('should call validatePlayerStatistic (selection.playerId = true)', () => {
      const result = service['validatePlayerStatistic']({} as any, {
        playerId: 'playerId'
      } as any);

      expect(result).toEqual(true);
    });

    it('should call validatePlayerStatistic (selection.playerId = true and equal)', () => {
      const result = service['validatePlayerStatistic']({
        playerId: 'playerId',
        statisticId: 'statisticId'
      } as any, {
        playerId: 'playerId',
        statisticId: 'statisticId'
      } as any);

      expect(result).toEqual(false);
    });

    it('should call validatePlayerStatistic (statisticId not equal)', () => {
      const result = service['validatePlayerStatistic']({
        playerId: 'playerId',
        statisticId: 'statisticId'
      } as any, {
        playerId: 'playerId',
        statisticId: 'statisticId1'
      } as any);

      expect(result).toEqual(true);
    });

    it('should call validatePlayerStatistic (playerId not equal)', () => {
      const result = service['validatePlayerStatistic']({
        playerId: 'playerId1',
        statisticId: 'statisticId'
      } as any, {
        playerId: 'playerId',
        statisticId: 'statisticId'
      } as any);

      expect(result).toEqual(true);
    });
  });

  describe('#validateGameStatistic', () => {
    it('should call validateGameStatistic (selection.type = false)', () => {
      const result = service['validateGameStatistic']({} as any, {} as any);

      expect(result).toEqual(true);
    });

    it('should call validateGameStatistic (selection.type = true)', () => {
      const result = service['validateGameStatistic']({} as any, {
        type: 20,
        statisticId: 'statisticId'
      } as any);

      expect(result).toEqual(true);
    });

    it('should call validateGameStatistic (selection.type = true tatisticId equal)', () => {
      const result = service['validateGameStatistic']({
        statisticId: 'statisticId'
      } as any, {
        type: 20,
        statisticId: 'statisticId'
      } as any);

      expect(result).toEqual(false);
    });

    it('should call validateGameStatistic (statisticId not equal)', () => {
      const result = service['validateGameStatistic']({
        statisticId: 'statisticId'
      } as any, {
        type: 20,
        statisticId: 'statisticId1'
      } as any);

      expect(result).toEqual(true);
    });
  });
});
