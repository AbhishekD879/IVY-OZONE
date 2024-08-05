import { UkToteBetBuilderService } from './uk-tote-bet-builder.service';
import { TotePotBet } from '@uktote/models/totePotBet/tote-pot-bet';
import { ToteBetLeg } from '@uktote/models/toteBetLeg/tote-bet-leg';
import { IUkTotePoolBet } from '@uktote/models/tote-pool.model';
import { Subject } from 'rxjs';

describe('UkToteBetBuilderService', () => {
  let service: UkToteBetBuilderService;
  let pubSubService;
  let betRecognitionService;
  let ukToteService;

  beforeEach(() => {
    pubSubService = {
      publishSync: jasmine.createSpy(),
      API: {
        CLEAR_BETBUILDER: 'CLEAR_BETBUILDER',
        BETBUILDER_UPDATED: 'BETBUILDER_UPDATED'
      }
    };

    betRecognitionService = {
      recognizeBet: jasmine.createSpy()
    };

    ukToteService = {
      isMultipleLegsToteBet: jasmine.createSpy().and.returnValue(false)
    };

    service = new UkToteBetBuilderService(
      pubSubService,
      betRecognitionService,
      ukToteService
    );
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  it('get isMultipleLegsBet$', () => {
    const isMultipleLegsBetSubject$ = new Subject<boolean>();
    service['isMultipleLegsBetSubject'] = isMultipleLegsBetSubject$;
    expect(service.isMultipleLegsBet$).toEqual(isMultipleLegsBetSubject$.asObservable());
  });

  it('get items', () => {
    service['ukToteItems'] = [];
    expect(service.items).toBe(service['ukToteItems']);
  });

  it('get betName', () => {
    service['ukToteBetName'] = 'abc';
    expect(service.betName).toBe(service['ukToteBetName']);
  });

  it('get poolId', () => {
    service['ukTotePoolId'] = 1;
    expect(service.poolId).toBe(service['ukTotePoolId']);
  });


  it('checkIfBetSuspended ret false', () => {
    service.betModel = new TotePotBet({isActive: true} as IUkTotePoolBet, [], null, null);
    service.betModel.legs = [{isSuspended: true}, {isSuspended: false}] as ToteBetLeg[];
    expect(service.betModel.checkIfBetSuspended()).toBe(false);
  });

  it('checkIfBetSuspended ret true', () => {
    service.betModel = new TotePotBet({isActive: false} as IUkTotePoolBet, [], null, null);
    service.betModel.legs = [{isSuspended: true}, {isSuspended: true}] as ToteBetLeg[];
    expect(service.betModel.checkIfBetSuspended()).toBe(true);
  });

  it('clear', () => {
    service['isMultipleLegsBet'] = true;
    service.betModel = new TotePotBet({isActive: true} as IUkTotePoolBet, [], null, null);
    const leg = new ToteBetLeg(null, null, null, null);
    service.betModel.clear = jasmine.createSpy();
    leg.isSuspended = false;
    service.betModel.legs = [] as ToteBetLeg[];
    expect(service.betModel.checkIfBetSuspended()).toBe(true);
    service.clear('1');
    expect(service.betModel.clear).toHaveBeenCalled();
    expect(pubSubService.publishSync).toHaveBeenCalledWith('CLEAR_BETBUILDER', '1');
    expect(pubSubService.publishSync).toHaveBeenCalledWith('BETBUILDER_UPDATED');
    service['isMultipleLegsBet'] = false;
    service.betModel = { clear: jasmine.createSpy() } as any;
    service.clear('1');
    expect(service.betModel.clear).not.toHaveBeenCalled();
    expect(pubSubService.publishSync).toHaveBeenCalledWith('CLEAR_BETBUILDER', '1');
    expect(pubSubService.publishSync).toHaveBeenCalledWith('BETBUILDER_UPDATED');
  });
  it('add (case 1)', () => {
    service['ukToteService'] = {
      isMultipleLegsToteBet: jasmine.createSpy().and.returnValue(true)
    } as any;

    const options: any = { betModel: {} };
    service.add(options);

    expect(service['ukToteService'].isMultipleLegsToteBet).toHaveBeenCalled();
    expect(service['betModel']).toBe(options.betModel);
    expect(pubSubService.publishSync).toHaveBeenCalledWith('BETBUILDER_UPDATED');
  });

  it('add (case 2)', () => {
    service['ukToteService'] = {
      isMultipleLegsToteBet: jasmine.createSpy().and.returnValue(false)
    } as any;

    service.add({} as any);

    expect(service['ukToteService'].isMultipleLegsToteBet).toHaveBeenCalled();
    expect(service['betModel']).toBeUndefined();
    expect(service['poolType']).toBeUndefined();
    expect(service['ukTotePoolId']).toBeUndefined();
    expect(betRecognitionService.recognizeBet).toHaveBeenCalled();
    expect(pubSubService.publishSync).toHaveBeenCalledWith('BETBUILDER_UPDATED');
  });

  it('add (case 2), pool was set', () => {
    service['ukToteService'] = {
      isMultipleLegsToteBet: jasmine.createSpy().and.returnValue(false)
    } as any;

    service.add({
      currentPool: { poolType: 'type', id: 8768 }
    } as any);

    expect(service['ukToteService'].isMultipleLegsToteBet).toHaveBeenCalled();
    expect(service['betModel']).toBeUndefined();
    expect(service['poolType']).toBe('type');
    expect(service['ukTotePoolId']).toBe(8768);
    expect(betRecognitionService.recognizeBet).toHaveBeenCalled();
    expect(pubSubService.publishSync).toHaveBeenCalledWith('BETBUILDER_UPDATED');
  });

  it('checkIfShouldShow', () => {
    service['isMultipleLegsBet'] = true;
    service.betModel = { checkIfSomeLegFilled: () => true } as any;
    expect(service.checkIfShouldShow()).toBeTruthy();

    service['isMultipleLegsBet'] = true;
    service.betModel = { checkIfSomeLegFilled: () => false } as any;
    expect(service.checkIfShouldShow()).toBeFalsy();

    service['isMultipleLegsBet'] = false;
    service['ukToteItems'] = [{}] as any;
    expect(service.checkIfShouldShow()).toBeTruthy();

    service['isMultipleLegsBet'] = false;
    service['ukToteItems'] = [] as any;
    expect(service.checkIfShouldShow()).toBeFalsy();
  });

  it('getTotalStake', () => {
    service.betModel = { numberOfLines: 2 } as any;
    expect(service.getTotalStake(2)).toBe(4);
    expect(service.getTotalStake(0)).toBe(0);
  });

  describe('handleMultipleLegsBetChange', () => {
    it('should call next method', () => {
      service['isMultipleLegsBetSubject'] = {
        next: jasmine.createSpy('next'),
        observers: [{}]
      } as any;
      service['isMultipleLegsBet'] = true;
      service['handleMultipleLegsBetChange']();
      expect(service['isMultipleLegsBetSubject']['next']).toHaveBeenCalledWith(service['isMultipleLegsBet']);
    });

    it('should not call next method', () => {
      service['isMultipleLegsBetSubject'] = {
        next: jasmine.createSpy('next'),
        observers: []
      } as any;
      service['handleMultipleLegsBetChange']();
      expect(service['isMultipleLegsBetSubject']['next']).not.toHaveBeenCalled();
    });
  });
});
