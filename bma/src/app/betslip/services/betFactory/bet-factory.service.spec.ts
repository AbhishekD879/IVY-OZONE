import { BetFactoryService } from './bet-factory.service';
import { IBetError } from '@betslip/services/betError/bet-error.model';
import { ILegList } from '@betslip/services/models/bet.model';
import { IBetDoc } from '@betslip/services/bet/bet.model';

describe('BetFactoryService', () => {
  let service;
  let betService;

  beforeEach(() => {
    betService = jasmine.createSpyObj('betService', ['parse', 'construct']);

    service = new BetFactoryService(betService);
  });

  it('should return errors present in leg', () => {
    const errs = [{
      outcomeId: '1',
      legDocId: '11'
    }, {
      outcomeId: '2',
      legDocId: '22'
    }, {
      outcomeId: '3',
      legDocId: '11'
    }, {
      outcomeId: '1',
      legDocId: '44'
    }];
    const leg = {
      docId: '11',
      parts: [{
        outcome: {
          id: '1'
        }
      }]
    };
    const result = BetFactoryService['getErrsByLeg'](errs as IBetError[], leg);

    expect(result.length).toEqual(3);
    expect(result[0]).toEqual(errs[0]);
    expect(result[1]).toEqual(errs[3]);
    expect(result[2]).toEqual(errs[2]);
  });

  it('should parse bets', () => {
    const betDocs = [{ id: '1' }, { id: '2' }];
    const legs = [{ id: '11' }, { id: '22' }];

    service.parseBets(betDocs, legs);

    expect(betService.parse.calls.count()).toEqual(betDocs.length);
    expect(betService.parse).toHaveBeenCalledWith(betDocs[1], legs);
  });

  describe('constructTempBets', () => {
    it('should construct empty list', () => {
      const legs = [] as ILegList;
      const errors = [] as IBetError[];
      const result = service.constructTempBets(legs, errors);

      expect(result).toEqual([]);
    });

    it('should reject EACH_WAY legs', () => {
      const legs = [{
        winPlace: 'WIN',
        docId: '1',
        parts: [{
          outcome: {
            id: '1'
          }
        }]
      }, {
        winPlace: 'EACH_WAY'
      }] as ILegList;
      const errors = [{
        outcomeId: '3',
        legDocId: '2'
      }, {
        outcomeId: '5',
        legDocId: '1'
      }] as IBetError[];
      const result = service.constructTempBets(legs, errors);

      expect(result.length).toEqual(1);
      expect(betService.construct.calls.count()).toEqual(1);
      expect(betService.construct).toHaveBeenCalledWith({
        isMocked: true,
        type: 'SGL',
        betOffer: {},
        allLegs: legs,
        legIds: [legs[0].docId],
        errs: [errors[1]],
        lines: 1,
        docId: legs[0].docId
      });
    });
  });

  describe('constructBets', () => {
    it('should parse bets', () => {
      const betDocs = [{ id: '1' }, { id: '2' }] as IBetDoc[];
      const legs = [{
        winPlace: 'WIN',
        docId: '1'
      }, {
        winPlace: 'EACH_WAY'
      }] as ILegList;
      const errors = [{
        outcomeId: '3',
        legDocId: '2'
      }, {
        outcomeId: '5',
        legDocId: '1'
      }] as IBetError[];
      const result = service.constructBets(betDocs, legs, errors);

      expect(result.length).toEqual(betDocs.length);
      expect(betService.parse.calls.count()).toEqual(betDocs.length);
    });

    it('should construct temp bets', () => {
      const betDocs = [] as IBetDoc[];
      const legs = [{
        winPlace: 'WIN',
        docId: '1',
        parts: [{
          outcome: {
            id: '111'
          }
        }]
      }, {
        combi: 'FORECAST', selection: { places: '2' },
        parts: [{ outcome: {} }]
      }, {
        combi: 'FORECAST', selection: { places: '*' },
        parts: [{ outcome: {} }]
      }, {
        combi: 'TRICAST', selection: { places: '3' },
        parts: [{ outcome: {} }]
      }, {
        combi: 'TRICAST', selection: { places: '*' },
        parts: [{ outcome: {} }]
      }, {
        winPlace: 'EACH_WAY'
      }] as ILegList;
      const errors = [{
        outcomeId: '3',
        legDocId: '2'
      }, {
        outcomeId: '5',
        legDocId: '1'
      }] as IBetError[];
      const result = service.constructBets(betDocs, legs, errors);

      expect(result.length).toEqual(5);
      expect(betService.construct.calls.count()).toEqual(5);
    });
  });
});
