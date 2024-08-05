import { of as observableOf } from 'rxjs';

import { RaceOutcomeDetailsService } from './race-outcome-details.service';
import environment from '@environment/oxygenEnvConfig';

describe('RaceOutcomeDetailsService', () => {
  let service: RaceOutcomeDetailsService;
  let cmsService;

  beforeEach(() => {
    cmsService = {
      getSystemConfig: jasmine.createSpy().and.returnValue(observableOf({aggregationMS:{enabled:true}}))
    };

    service = new RaceOutcomeDetailsService(
      cmsService
    );
  });

  it('constructor', () => {
    expect(service).toBeDefined();
  });

  describe('getSilkStyle', () => {
    it(`should define isSilkSmall`, () => {
      spyOn(service as any, 'getSilkStyles');
      service['isSilkSmall'] = false;
      service.getSilkStyle({} as any, {} as any, '', true);

      expect(service['isSilkSmall']).toBeTruthy();
    });

    it('should sort silks', () => {
      spyOn(service as any, 'getSilkStyles');
      const outcomes = [{
        racingFormOutcome: {
          silkName: 'image2.gif'
        }
      }, {
        racingFormOutcome: {
          silkName: 'image1.png'
        },
      },
      {
        racingFormOutcome: {
          silkName: 'image3.png'
        }
      }
    ] as any;
      service.getSilkStyle(outcomes, outcomes, '0', true);

      expect(service['getSilkStyles']).toHaveBeenCalledWith(['image1', 'image2', 'image3'], outcomes, '0', false);
    });
  });

  it('getSilkStyle with raceData as object', () => {
    service['getSilkStyles'] = jasmine.createSpy();

    const raceData: any = { outcomes: [] };
    const outcome: any = {};
    service.getSilkStyle(raceData, outcome);

    expect(service['getSilkStyles']).toHaveBeenCalledWith(
      jasmine.any(Array), jasmine.any(Object), undefined, false
    );
  });

  it('getSilkStyle with raceData as array', () => {
    service['getSilkStyles'] = jasmine.createSpy();

    const raceData: any = [];
    const outcome: any = {};
    service.getSilkStyle(raceData, outcome);

    expect(service['getSilkStyles']).toHaveBeenCalledWith(
      jasmine.any(Array), jasmine.any(Object), undefined, false
    );
  });

  it('getSilkStyle - should get style if silk is available and isAggregationMSEnabled=true', () => {
    const outcome: any = { racingFormOutcome: { silkName: 'wrwffszxv.gif' } };
    const ids: any = ['23533665', '23432423'];
    const silkStyles = {
      'background-image': `url(${environment.IMAGES_RACE_ENDPOINT}/23533665,23432423)`,
      'background-position': '-10px 29px',
      'background-size': ''
    };
    service['isAggregationMSEnabled'] = true;
    expect(service['getSilkStyles'](ids, outcome)).toEqual(silkStyles);
  });

  it('getSilkStyle - should get style if silk is not available and isAggregationMSEnabled=true', () => {
    const outcome: any = { racingFormOutcome: {silkName: '23533665'} };
    const ids: any = ['23533665', '23432423'];
    const silkStyles = {
      'background-image': 'url(https://aggregation.coral.co.uk/silks/racingpost/23533665,23432423)',//`url(${environment.IMAGES_RACE_ENDPOINT}/racing_post/23533665,23432423)`,
      'background-position': '-10px 0px',
      'background-size': ''
    };
    service['isAggregationMSEnabled'] = true;
    expect(service['getSilkStyles'](ids, outcome)).toEqual(silkStyles);
  });

  it('getSilkStyle - should get style if silk is not available and isAggregationMSEnabled=true with streambet', () => {
    const outcome: any = { racingFormOutcome: {silkName: '23533665'} };
    const ids: any = ['23533665', '23432423'];
    const silkStyles = {
      'background-image': 'url(https://aggregation.coral.co.uk/silks/racingpost/23533665,23432423)',//`url(${environment.IMAGES_RACE_ENDPOINT}/racing_post/23533665,23432423)`,
      'background-position': '0 0px',
      'width': '45px'
    };
    service['isAggregationMSEnabled'] = true;
    expect(service['getSilkStyles'](ids, outcome,'0', true)).toEqual(silkStyles);
  });

  it('getSilkStyle - should get style if silk is not available and isAggregationMSEnabled=false', () => {
    const outcome: any = { racingFormOutcome: { silkName: 'wrwffszxv.gif' } };
    const ids: any = ['23533665', '23432423'];
    const silkStyles = {
      'background-image': `url(${environment.IMAGES_ENDPOINT}/racing_post/wrwffszxv.gif)`
    };
    service['isAggregationMSEnabled'] = false;
    expect(service['getSilkStyles'](ids, outcome)).toEqual(silkStyles);
  });

  describe('isGenericSilk', () => {
    const event: any = {};
    beforeEach(() => {
      service.isSilkAvailable = jasmine.createSpy().and.returnValue(true);
      service.isValidSilkName = jasmine.createSpy();
    });

    it('should return true when generic silk is needed', () => {
      const outcome: any = { racingFormOutcome: {} };
      const expectedResult = service.isGenericSilk(event, outcome);

      expect(service.isSilkAvailable).toHaveBeenCalledWith(event);
      expect(service.isValidSilkName).toHaveBeenCalledWith(outcome.racingFormOutcome);
      expect(expectedResult).toEqual(true);
    });

    it('should return false when generic silk is not needed', () => {
      const outcome: any = { racingFormOutcome: { silkName: 'silkName' } };
      const expectedResult = service.isGenericSilk(event, outcome);

      expect(expectedResult).toEqual(false);
    });
  });

  it('isGenericSilk (grayhounds category)', () => {
    service.isSilkAvailable = jasmine.createSpy().and.returnValue(true);
    service['isValidNumber'] = jasmine.createSpy();

    const event: any = { categoryCode: service['TYPE_GREYHOUNDS'] };
    const outcome: any = {};
    service.isGenericSilk(event, outcome);

    expect(service.isSilkAvailable).toHaveBeenCalledWith(event);
    expect(service['isValidNumber']).toHaveBeenCalledWith(outcome.runnerNumber);
  });

  it('isGreyhoundSilk', () => {
    service['isValidNumber'] = jasmine.createSpy();

    const event: any = {};
    const outcome: any = {};
    service.isGreyhoundSilk(event, outcome);

    expect(service['isValidNumber']).not.toHaveBeenCalledWith(outcome.runnerNumber);
  });

  it('isGreyhoundSilk (greyhounds category)', () => {
    service['isValidNumber'] = jasmine.createSpy();

    const event: any = { categoryCode: service['TYPE_GREYHOUNDS'] };
    const outcome: any = {};
    service.isGreyhoundSilk(event, outcome);

    expect(service['isValidNumber']).toHaveBeenCalledWith(outcome.runnerNumber);
  });

  it('isSilkAvailable', () => {
    let event: any;

    service.isGreyhoundSilk = jasmine.createSpy().and.returnValue(true);
    event = {
      markets: [{
        outcomes: [{}]
      }]
    };
    expect(service.isSilkAvailable(event)).toBeTruthy();
    expect(service.isGreyhoundSilk).toHaveBeenCalledWith(event, event.markets[0].outcomes[0]);

    service.isGreyhoundSilk = jasmine.createSpy().and.returnValue(false);
    event = {
      markets: [{
        outcomes: [{
          racingFormOutcome: { silkName: 'SN' }
        }]
      }]
    };
    expect(service.isSilkAvailable(event)).toBeTruthy();
    expect(service.isGreyhoundSilk).toHaveBeenCalledWith(event, event.markets[0].outcomes[0]);

    service.isGreyhoundSilk = jasmine.createSpy().and.returnValue(false);
    event = {
      markets: [{
        outcomes: [{
        }]
      }]
    };   
    expect(service.isSilkAvailable(event)).toBeFalsy();
  });

  describe('isNumberNeeded', () => {
    let event;
    let outcome;

    it('should be false if no runner number and no racingFormOutcome', () => {
      service['isValidNumber'] = jasmine.createSpy().and.returnValue(false);
      event = { categoryCode: '' };
      outcome = { runnerNumber: undefined };
      expect(service.isNumberNeeded(event, outcome)).toBeFalsy();
    });

    it('should be false if valid runner number', () => {
      service['isValidNumber'] = jasmine.createSpy().and.returnValue(true);
      event = { categoryCode: '' };
      outcome = { runnerNumber: 123 };
      expect(service.isNumberNeeded(event, outcome)).toBeTruthy();
    });

    it('should be false for greyhounds', () => {
      service['isValidNumber'] = jasmine.createSpy().and.returnValue(true);
      event = { categoryCode: service['TYPE_GREYHOUNDS'] };
      outcome = { runnerNumber: 123 };
      expect(service.isNumberNeeded(event, outcome)).toBeFalsy();
    });

    it('should be false for virtual greyhounds', () => {
      service['isValidNumber'] = jasmine.createSpy().and.returnValue(true);
      event = { categoryCode: '', className: 'Virtual Greyhounds' };
      outcome = { runnerNumber: 123 };
      expect(service.isNumberNeeded(event, outcome)).toBeTruthy();
    });

    it('should be if false no runner number and no racing form draw', () => {
      service['isValidNumber'] = jasmine.createSpy().and.returnValue(false);
      event = { categoryCode: '', className: '' };
      outcome = { runnerNumber: 123, racingFormOutcome: {} };
      expect(service.isNumberNeeded(event, outcome)).toBeFalsy();
    });

    it('should be false if no runner number and racing form draw is NOT a number', () => {
      service['isValidNumber'] = jasmine.createSpy().and.returnValues(false, false);
      event = { categoryCode: '', className: '' };
      outcome = { runnerNumber: 123, racingFormOutcome: {} };
      expect(service.isNumberNeeded(event, outcome)).toBeFalsy();
    });

    it('should be true if no runner number and racing form draw is VALID a number', () => {
      service['isValidNumber'] = jasmine.createSpy().and.returnValues(false, true);
      event = { categoryCode: '', className: '' };
      outcome = { runnerNumber: 123, racingFormOutcome: { draw: 4 } };
      expect(service.isNumberNeeded(event, outcome)).toBeTruthy();
    });
  });

  it('getsilkNamesForEvents', () => {
    const events: any[] = [
      { categoryId: '' },
      {
        categoryId: service['HORSE_RACING_CATEGORY_ID'],
        markets: [{
          outcomes: [{
            racingFormOutcome: {
              silkName: 'SN'
            }
          }]
        }]
      }
    ];
    expect(service.getsilkNamesForEvents(events)).toEqual(['SN']);
  });

  describe('getSilkStyleForPage', () => {
    const outcomeId = 'OID';
    const event: any = {};
    const allSilkNames: any[] = ['testimg1','testimg2'];

    beforeEach(() => {
      service['getOutcomeData'] = jasmine.createSpy().and.returnValue({ outcome: {} });
      service['getSilkStyles'] = jasmine.createSpy();
    });

    it('getSilkStyleForPage', () => {
      service.getSilkStyleForPage(outcomeId, event, allSilkNames);

      expect(service['getOutcomeData']).toHaveBeenCalledWith(outcomeId, event);
      expect(service['getSilkStyles']).toHaveBeenCalledWith(
        jasmine.any(Array), jasmine.any(Object)
      );
    });

    it(`should define isSilkSmall `, () => {
      service['isSilkSmall'] = false;

      service.getSilkStyleForPage(outcomeId, event, allSilkNames, true);

      expect(service['isSilkSmall']).toBeTruthy();
    });
  });
  it('isSilkAvailableForOutcome', () => {
    service['getOutcomeData'] = jasmine.createSpy().and.returnValue({
      outcome: {
        racingFormOutcome: {
          silkName: 'SN'
        }
      }
    });
    service.isValidSilkName = jasmine.createSpy();

    const outcomeId = 'OID';
    const event: any = {};
    service.isSilkAvailableForOutcome(outcomeId, event);

    expect(service['getOutcomeData']).toHaveBeenCalledWith(outcomeId, event);
    expect(service.isValidSilkName).toHaveBeenCalled();

    service['getOutcomeData'] = jasmine.createSpy().and.returnValue({
      outcome: {
      }
    });
    service.isValidSilkName = jasmine.createSpy();
    service.isSilkAvailableForOutcome(outcomeId, event);
    const outcome={} as any
    expect(service['getOutcomeData']).toHaveBeenCalledWith(outcomeId, event);
    expect(service.isValidSilkName(outcome)).toBeFalsy();

  });

  it('isUnnamedFavourite', () => {
    service['getOutcomeData'] = jasmine.createSpy().and.returnValue({
      outcome: {
        name: 'Unnamed Favourite'
      }
    });

    const outcomeId = 'OID';
    const event: any = {};
    expect(service.isUnnamedFavourite(outcomeId, event)).toBeTruthy();
    expect(service['getOutcomeData']).toHaveBeenCalledWith(outcomeId, event);
  });

  it('isValidSilkName', () => {
    [
      { name: '1.gif', expect: true },
      { name: '2.jpg', expect: true },
      { name: '3.jpeg', expect: true },
      { name: '4.PNG', expect: true },
      { name: '5.js', expect: false },
      { name: '6.py', expect: false }
    ].forEach(item => {
      expect(
        service.isValidSilkName({ silkName: item.name })
      ).toBe(item.expect);
    });
  });

  describe('getOutcomeData', () => {
    it('should return formatted data', () => {
      const outcomeId = 'OID';
      const event: any = {
        markets: [{
          outcomes: [{
            id: 'OID'
          }]
        }]
      };

      const result = service['getOutcomeData'](outcomeId, event);
      expect(result.market).toBe(event.markets[0]);
      expect(result.outcome).toBe(event.markets[0].outcomes[0]);
    });

    it('should return undefined', () => {
      const result = service['getOutcomeData']({} as any, undefined);
      expect(result).toEqual(undefined);
    });
  });

  describe('getSilkStyles', () => {
    const racingIds = ['1', '2'];
    const outcome: any = {
      racingFormOutcome: { silkName: 'SN' }
    };
    beforeEach(() => {
      spyOn(service as any, 'getRacingPostImagePostion');
    });

    it('aggregation MS enabled', () => {
      service['isAggregationMSEnabled'] = true;

      expect(service['getSilkStyles'](racingIds, outcome)).toEqual({
        'background-image': jasmine.any(String),
        'background-position': jasmine.any(String),
        'background-size': jasmine.any(String),
      } as any);
      expect(service['getRacingPostImagePostion']).toHaveBeenCalledWith(racingIds, outcome.racingFormOutcome.silkName);
    });

    it('aggregation MS disalbed', () => {
      service['isAggregationMSEnabled'] = false;
      expect(service['getSilkStyles']([], outcome)).toEqual({
        'background-image': jasmine.any(String)
      } as any);
    });

    it(`should return bg position for Small img`, () => {
      service['isSilkSmall'] = true;
      service['isAggregationMSEnabled'] = true;
      (service['getRacingPostImagePostion'] as jasmine.Spy).and.returnValue(99);

      expect(service['getSilkStyles'](racingIds, outcome)['background-position'])
        .toEqual(`${service['SILK_POSITION_SMALL']} 99px`);
    });

    it(`should return bg position for Regular img`, () => {
      service['isSilkSmall'] = false;
      service['isAggregationMSEnabled'] = true;
      (service['getRacingPostImagePostion'] as jasmine.Spy).and.returnValue(99);

      expect(service['getSilkStyles'](racingIds, outcome)['background-position'])
        .toEqual(`${service['SILK_POSITION']} 99px`);
    });
  });

  describe('getRacingPostImagePostion', () => {
    it('for regular img', () => {
      service['isSilkSmall'] = false;
      expect(
        service['getRacingPostImagePostion'](['1', '2'], '2.gif')
      ).toBe(-service['SILK_IMAGE_HEIGHT']);
    });

    it('for small img', () => {
      service['isSilkSmall'] = true;
      expect(
        service['getRacingPostImagePostion'](['1', '2'], '2.gif')
      ).toBe(-service['SILK_IMAGE_SMALL_HEIGHT']);
    });

  });

  it('isValidNumber', () => {
    expect(
      service['isValidNumber'](1)
    ).toBeTruthy();
    expect(
      service['isValidNumber'](-1)
    ).toBeFalsy();
    expect(
      service['isValidNumber'](null)
    ).toBeFalsy();
    expect(
      service['isValidNumber'](undefined)
    ).toBeFalsy();
    expect(
      service['isValidNumber']('test')
    ).toBeFalsy();
  });

  it('formatJockeyWeight should form jockey / allowance string', () => {
    const racingFormOutcome = {
      jockey: 'Jockey',
      allowance: 3
    } as any;
    expect(service.formatJockeyWeight(racingFormOutcome)).toBe('Jockey (3)');

    racingFormOutcome.allowance = undefined;
    expect(service.formatJockeyWeight(racingFormOutcome)).toBe('Jockey');

    racingFormOutcome.allowance = 0;
    expect(service.formatJockeyWeight(racingFormOutcome)).toBe('Jockey');
  });

  it('isJockeyAndTrainer should return true', () => {
      const racingFormOutcome = 
         {
          jockey: 'test',
          trainer: 'test'
        } as any;

      expect(service.isJockeyAndTrainer(racingFormOutcome)).toBe(true);
    });

    it('isJockeyAndTrainer should return false', () => {
      const racingFormOutcome = {
      } as any;
      expect(service.isJockeyAndTrainer(racingFormOutcome)).toBe(false);
    });

    it('getOutcomeClass should return smaller case names', () => {
      const outcome: any = {
        name: 'SN'
      };
      expect(service.getOutcomeClass(outcome)).toBe('sn');
    });

    it('isGroupSilkNeeded should return true /false', () => {
      const outcome = {
        name: 'Odd',
      } as any;
      expect(service.isGroupSilkNeeded(outcome)).toBeTruthy();
      outcome.name = undefined;
      expect(service.isGroupSilkNeeded(outcome)).toBeFalsy();
      outcome.name = 'Even';
      expect(service.isGroupSilkNeeded(outcome)).toBeTruthy();
      outcome.name = 'Inside';
      expect(service.isGroupSilkNeeded(outcome)).toBeTruthy();
      outcome.name = 'Outside';
      expect(service.isGroupSilkNeeded(outcome)).toBeTruthy();
    });
});
