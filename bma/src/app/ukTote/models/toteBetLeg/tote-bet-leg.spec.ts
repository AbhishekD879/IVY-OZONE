import { ToteBetLeg } from '@uktote/models/toteBetLeg/tote-bet-leg';

describe('ToteBetLeg', () => {
  let toteBetLeg;
  let index;
  let marketId;
  let eventEntity;
  let ukToteService;

  beforeEach(() => {
    index = 5;
    marketId = 'marketId';
    eventEntity = {
      eventStatusCode: 'S',
      markets: [
        {
          linkedMarketId: 'linkedMarketId',
          outcomes: [
            { id: '8793' },
            { id: '2134' }
            ]
        }
      ]
    };
    ukToteService = {};
    toteBetLeg = new ToteBetLeg(index, marketId, eventEntity, ukToteService);
  });

  it('constructor no event', () => {
    toteBetLeg = new ToteBetLeg(index, marketId, null, ukToteService);
    expect(toteBetLeg.index).toBe(index);
    expect(toteBetLeg.name).toBe(`Leg ${index + 1}`);
    expect(toteBetLeg.linkedMarketId).toBeUndefined();
  });

  it('constructor with event', () => {
    toteBetLeg = new ToteBetLeg(index, marketId, eventEntity, ukToteService);
    expect(toteBetLeg.index).toBe(index);
    expect(toteBetLeg.name).toBe(`Leg ${index + 1}`);
    expect(toteBetLeg.linkedMarketId).toBe(toteBetLeg.event.markets[0].linkedMarketId);
  });

  it('get event', () => {
    const event = toteBetLeg.event;
    expect(event).toBe(eventEntity);
  });

  it('get selectionsCount', () => {
    const selectionsCount = toteBetLeg.selectionsCount;
    expect(selectionsCount).toBe(0);
  });

  it('get selectedOutcomes', () => {
    const sortedOutcomes = [];
    toteBetLeg.selectedOutcomesIds = ['2313', '9083', '1289'];
    toteBetLeg.outcomesMap = {
      '2313': {},
      '9083': {},
      '1289': {}
    };
    ukToteService.sortOutcomes = jasmine.createSpy().and.returnValue(sortedOutcomes);
    const result = toteBetLeg.selectedOutcomes;
    expect(ukToteService.sortOutcomes).toHaveBeenCalledWith([{}, {}, {}]);
    expect(result).toBe(sortedOutcomes);
  });

  describe('updateSuspendedStatus', () => {
    it('isEventSuspended', () => {
      toteBetLeg.isEventSuspended = jasmine.createSpy().and.returnValue(true);
      toteBetLeg.isMarketSuspended = jasmine.createSpy().and.returnValue(false);
      toteBetLeg.isEventResulted = jasmine.createSpy().and.returnValue(false);
      toteBetLeg.clear = jasmine.createSpy();
      toteBetLeg.updateSuspendedStatus();
      expect(toteBetLeg.isEventSuspended).toHaveBeenCalled();
      expect(toteBetLeg.isMarketSuspended).not.toHaveBeenCalled();
      expect(toteBetLeg.isEventResulted).not.toHaveBeenCalled();
      expect(toteBetLeg.clear).toHaveBeenCalled();
    });

    it('isMarketSuspended', () => {
      toteBetLeg.isEventSuspended = jasmine.createSpy().and.returnValue(false);
      toteBetLeg.isMarketSuspended = jasmine.createSpy().and.returnValue(true);
      toteBetLeg.isEventResulted = jasmine.createSpy().and.returnValue(false);
      toteBetLeg.clear = jasmine.createSpy();
      toteBetLeg.updateSuspendedStatus();
      expect(toteBetLeg.isEventSuspended).toHaveBeenCalled();
      expect(toteBetLeg.isMarketSuspended).toHaveBeenCalled();
      expect(toteBetLeg.isEventResulted).not.toHaveBeenCalled();
      expect(toteBetLeg.clear).toHaveBeenCalled();
    });

    it('isEventResulted', () => {
      toteBetLeg.isEventSuspended = jasmine.createSpy().and.returnValue(false);
      toteBetLeg.isMarketSuspended = jasmine.createSpy().and.returnValue(false);
      toteBetLeg.isEventResulted = jasmine.createSpy().and.returnValue(true);
      toteBetLeg.clear = jasmine.createSpy();
      toteBetLeg.updateSuspendedStatus();
      expect(toteBetLeg.isEventSuspended).toHaveBeenCalled();
      expect(toteBetLeg.isMarketSuspended).toHaveBeenCalled();
      expect(toteBetLeg.isEventResulted).toHaveBeenCalled();
      expect(toteBetLeg.clear).toHaveBeenCalled();
    });

    it('isSuspended false', () => {
      toteBetLeg.isEventSuspended = jasmine.createSpy().and.returnValue(false);
      toteBetLeg.isMarketSuspended = jasmine.createSpy().and.returnValue(false);
      toteBetLeg.isEventResulted = jasmine.createSpy().and.returnValue(false);
      toteBetLeg.filterSelectedOutcomes = jasmine.createSpy();
      toteBetLeg.updateSuspendedStatus();
      expect(toteBetLeg.isEventSuspended).toHaveBeenCalled();
      expect(toteBetLeg.isMarketSuspended).toHaveBeenCalled();
      expect(toteBetLeg.isEventResulted).toHaveBeenCalled();
      expect(toteBetLeg.filterSelectedOutcomes).toHaveBeenCalled();
    });
  });

  it('updateFilledStatus', () => {
    toteBetLeg.updateFilledStatus();
    expect(toteBetLeg.filled).toBeFalsy();
  });

  it('selectOutcome', () => {
    const outcomeId = '3245';
    toteBetLeg.updateFilledStatus = jasmine.createSpy();
    toteBetLeg.selectedOutcomesIds = [];
    toteBetLeg.selectOutcome(outcomeId);
    expect(toteBetLeg.selectedOutcomesIds).toEqual([outcomeId]);
    expect(toteBetLeg.updateFilledStatus).toHaveBeenCalled();
  });

  it('deselectOutcome', () => {
    const outcomeId = '3245';
    toteBetLeg.updateFilledStatus = jasmine.createSpy();
    toteBetLeg.selectedOutcomesIds = ['3245'];
    toteBetLeg.deselectOutcome(outcomeId);
    expect(toteBetLeg.selectedOutcomesIds).toEqual([]);
    expect(toteBetLeg.updateFilledStatus).toHaveBeenCalled();
  });

  it('isOutcomeSelected', () => {
    const outcomeId = '3245';
    toteBetLeg.selectedOutcomesIds = ['5422', '3245', '9087'];
    const result = toteBetLeg.isOutcomeSelected(outcomeId);
    expect(result).toBeTruthy();
  });

  it('clear', () => {
    toteBetLeg.updateFilledStatus = jasmine.createSpy();
    toteBetLeg.selectedOutcomesIds = ['5422', '3245', '9087'];
    toteBetLeg.clear();
    expect(toteBetLeg.selectedOutcomesIds).toEqual([]);
    expect(toteBetLeg.updateFilledStatus).toHaveBeenCalled();
  });


  describe('generateOutcomesMap', () => {
    it('no event', () => {
      toteBetLeg.eventEntity = null;
      const result = toteBetLeg['generateOutcomesMap']();
      expect(result).toEqual({});
    });

    it('event is set', () => {
      const result = toteBetLeg['generateOutcomesMap']();
      expect(result).toEqual({
        '2134': { id: '2134' },
        '8793': { id: '8793' }
      });
    });
  });

  describe('isEventSuspended', () => {
    it('no event', () => {
      toteBetLeg.eventEntity = null;
      const result = toteBetLeg['isEventSuspended']();
      expect(result).toBeFalsy();
    });

    it('event is set', () => {
      const result = toteBetLeg['isEventSuspended']();
      expect(result).toBeTruthy();
    });
  });

  describe('isMarketSuspended', () => {
    it('no event', () => {
      toteBetLeg.eventEntity = null;
      const result = toteBetLeg['isMarketSuspended']();
      expect(result).toBeFalsy();
    });

    it('no markets', () => {
      toteBetLeg.eventEntity = { markets: null };
      const result = toteBetLeg['isMarketSuspended']();
      expect(result).toBeFalsy();
    });

    it('market is set', () => {
      toteBetLeg.eventEntity = { markets: [{ marketStatusCode: 'S' }]};
      const result = toteBetLeg['isMarketSuspended']();
      expect(result).toBeTruthy();
    });
  });

  describe('isEventResulted', () => {
    it('no event', () => {
      toteBetLeg.eventEntity = null;
      const result = toteBetLeg['isEventResulted']();
      expect(result).toBeFalsy();
    });

    it('event is set', () => {
      toteBetLeg.eventEntity = { isResulted: true };
      const result = toteBetLeg['isEventResulted']();
      expect(result).toBeTruthy();
    });
  });

  it('isOutcomeSuspended', () => {
    const outcome = { outcomeStatusCode: 'S' };
    const result = toteBetLeg['isOutcomeSuspended'](outcome);
    expect(result).toBeTruthy();
  });

  it('filterSelectedOutcomes', () => {
    toteBetLeg.selectedOutcomesIds = ['2134', '8793'];
    toteBetLeg.outcomesMap = {
      '2134': { id: '2134' },
      '8793': { id: '8793' }
    };
    toteBetLeg.isOutcomeSuspended = jasmine.createSpy().and.callFake((outcome) => outcome.id === '2134');
    toteBetLeg.deselectOutcome = jasmine.createSpy();
    toteBetLeg.updateFilledStatus = jasmine.createSpy();
    toteBetLeg['filterSelectedOutcomes']();
    expect(toteBetLeg.isOutcomeSuspended).toHaveBeenCalledTimes(2);
    expect(toteBetLeg.deselectOutcome).toHaveBeenCalledWith('2134');
    expect(toteBetLeg.updateFilledStatus).toHaveBeenCalled();
  });
});
