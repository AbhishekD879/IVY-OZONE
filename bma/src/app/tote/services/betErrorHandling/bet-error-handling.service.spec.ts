import { BetErrorHandlingService } from './bet-error-handling.service';
import { TOTE_CONFIG } from '../../tote.constant';

describe('BetErrorHandlingService', () => {
  let service: BetErrorHandlingService;

  let localeService;
  let filterService;
  let toteBetSlipService;

  beforeEach(() => {
    localeService = {
      getString: jasmine.createSpy()
    };

    filterService = {
      currencyPosition: jasmine.createSpy().and.returnValue('')
    };

    toteBetSlipService = {
      getCurrency: jasmine.createSpy()
    };

    service = new BetErrorHandlingService(
      localeService,
      filterService,
      toteBetSlipService
    );
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  it('checkTotalStake', () => {
    let result = service.checkTotalStake({
      maxTotalStake: '10',
      minTotalStake: '50',
      stakeIncrementFactor: '3'
    } as any, '20');
    expect(result.totalMax).toBeTruthy();
    expect(result.totalMin).toBeTruthy();
    expect(result.stakeIncrementFactor).toBeTruthy();

    result = service.checkTotalStake({
      maxTotalStake: '50',
      minTotalStake: '10',
      stakeIncrementFactor: '2'
    } as any, '30');
    expect(result.totalMax).toBeFalsy();
    expect(result.totalMin).toBeFalsy();
    expect(result.stakeIncrementFactor).toBeFalsy();
  });

  it('getTotalStakeErrorMsg', () => {
    localeService.getString.and.callFake(msg => msg);
    const result = service.getTotalStakeErrorMsg({
      maxTotalStake: '1',
      minTotalStake: '2',
      stakeIncrementFactor: '3'
    } as any, { totalMax: false, totalMin: false, stakeIncrementFactor: true } as any, '$');

    expect(localeService.getString).toHaveBeenCalledWith(
      'tt.maxTotalStake', jasmine.objectContaining({ value: jasmine.any(String) })
    );
    expect(localeService.getString).toHaveBeenCalledWith(
      'tt.minTotalStake', jasmine.objectContaining({ value: jasmine.any(String) })
    );
    expect(localeService.getString).toHaveBeenCalledWith(
      'tt.stakeIncrementFactor', jasmine.objectContaining({ value: jasmine.any(String) })
    );

    expect(result).toEqual('tt.stakeIncrementFactor');
  });

  it('isMarketsHasErrors', () => {
    let result;

    result = service.isMarketsHasErrors({
      markets: [
        {
          outcomes: [
            {
              error: { type: 'error' }
            }
          ]
        }
      ]
    });
    expect(result).toBeTruthy();

    result = service.isMarketsHasErrors({
      markets: [
        {
          outcomes: [
            {
              error: { type: 'unknown' }
            }
          ]
        }
      ]
    });
    expect(result).toBeFalsy();
  });

  it('generateServiceError', () => {
    const allErrors = {
      [TOTE_CONFIG.TOTE_GENERAL_BET_ERROR_KEY.service]: 'Some error'
    };

    const result = service.generateServiceError(allErrors);

    expect(result.serviceError.type).toBe('error');
    expect(result.serviceError.msg).toBe(allErrors[TOTE_CONFIG.TOTE_GENERAL_BET_ERROR_KEY.service]);
  });

  it('generateEventError', () => {
    const result = service.generateEventError('eventStarted');
    expect(result.type).toBe('error');
    expect(result.msg).toBe(TOTE_CONFIG.TOTE_EVENT_RELATED_ERRORS.eventStarted);
  });

  it('generateOutcomeErrorMsg', () => {
    const allErrors = {
      'STAKE_TOO_HIGH': 'Stake too high',
      'BET_GEN_ERR': 'General error'
    };

    expect(service.generateOutcomeErrorMsg('STAKE_TOO_HIGH', allErrors as any)).toBe(allErrors.STAKE_TOO_HIGH);
    expect(service.generateOutcomeErrorMsg('STAKE_TOO_LOW', allErrors as any)).toBe(allErrors.BET_GEN_ERR);
  });

  it('buildErrors', () => {
    const failedBets = [];
    const eventData = { markets: [{}] };
    const toteBetErrorsDescriptions: any = {};

    service['excludeOutcomeErrors'] = jasmine.createSpy().and.returnValue([{ serviceGenError: true }]);
    service.generateServiceError = jasmine.createSpy();
    service['extendOutcomeWithErrors'] = jasmine.createSpy();

    service.buildErrors(failedBets, eventData, toteBetErrorsDescriptions);
    expect(service['excludeOutcomeErrors']).toHaveBeenCalledWith(failedBets);
    expect(service.generateServiceError).toHaveBeenCalledWith(toteBetErrorsDescriptions);

    service['excludeOutcomeErrors'] = jasmine.createSpy().and.returnValue([]);
    service.buildErrors(failedBets, eventData, toteBetErrorsDescriptions);
    expect(service['extendOutcomeWithErrors']).toHaveBeenCalled();
  });

  it('buildPoolStakeError', () => {
    service['validationState'] = jasmine.createSpy().and.returnValue({ outcomeId: 1 });
    service['isRangeError'] = jasmine.createSpy().and.returnValue(true);
    service['errorsMessages'] = jasmine.createSpy();

    service.buildPoolStakeError({
      markets: [{
        outcomes: [{ id: 1 }, { id: 2 }]
      }]
    }, {} as any);

    expect(service['validationState']).toHaveBeenCalled();
    expect(service['isRangeError']).toHaveBeenCalled();
    expect(service['errorsMessages']).toHaveBeenCalled();
  });

  it('clearBetErrors', () => {
    const eventData = {
      markets: [
        {
          outcomes: [{
            error: { name: 'test' }
          }, {}]
        }
      ]
    };

    service.clearBetErrors(eventData);

    expect(eventData.markets[0].outcomes[0].error).toBeFalsy();
  });

  it('clearLineBetErrors', () => {
    const eventData = {
      markets: [
        {
          outcomes: [{
            id: '1',
            error: { name: 'test' }
          }, {
            id: '2',
            error: { name: 'test' }
          }, {
            id: '3'
          }]
        }
      ]
    };

    service.clearLineBetErrors(eventData, '1');

    expect(eventData.markets[0].outcomes[0].error).toBeFalsy();
  });

  it('isIncrementValid', () => {
    expect(service['isIncrementValid']('10', '3')).toBeTruthy();
    expect(service['isIncrementValid']('10', '2')).toBeFalsy();
    expect(service['isIncrementValid']('', '2')).toBeFalsy();
  });

  it('isMinValid', () => {
    expect(service['isMinValid']('2', '5')).toBeTruthy();
    expect(service['isMinValid']('6', '5')).toBeFalsy();
  });

  it('isMaxValid', () => {
    expect(service['isMaxValid']('2', '1')).toBeTruthy();
    expect(service['isMaxValid']('2', '3')).toBeFalsy();
  });

  it('isRangeError', () => {
    expect(service['isRangeError']({
      minStakePerLine: true,
      maxStakePerLine: false,
      stakeIncrementFactor: false,
      value: '1'
    } as any)).toBeTruthy();

    expect(service['isRangeError']({
      minStakePerLine: true,
      maxStakePerLine: false,
      stakeIncrementFactor: false,
      value: '0'
    } as any)).toBeFalsy();

    expect(service['isRangeError']({
      minStakePerLine: false,
      maxStakePerLine: false,
      stakeIncrementFactor: false,
      value: '2'
    } as any)).toBeFalsy();
  });

  it('validationState', () => {
    let result = service['validationState']({
      poolData: {
        minStakePerLine: '40',
        maxStakePerLine: '10',
        stakeIncrementFactor: '3'
      },
      value: '20'
    } as any);
    expect(result.minStakePerLine).toBeTruthy();
    expect(result.maxStakePerLine).toBeTruthy();
    expect(result.stakeIncrementFactor).toBeTruthy();

    result = service['validationState']({
      poolData: {
        minStakePerLine: '10',
        maxStakePerLine: '40',
        stakeIncrementFactor: '2'
      },
      value: '20'
    } as any);
    expect(result.minStakePerLine).toBeFalsy();
    expect(result.maxStakePerLine).toBeFalsy();
    expect(result.stakeIncrementFactor).toBeFalsy();
  });

  it('errorsMessages', () => {
    service['errorsMessages']('abc', {
      poolData: { currencyCode: '$' }
    } as any);
    expect(localeService.getString).toHaveBeenCalledWith('tt.abc', jasmine.any(Object));
    expect(toteBetSlipService.getCurrency).toHaveBeenCalledWith('$');
    expect(filterService.currencyPosition).toHaveBeenCalled();
  });

  it('excludeOutcomeErrors', () => {
    const failedBets = [
      {
        id: 1
      },
      {
        id: 2,
        error: {}
      },
      {
        id: 3,
        betError: [{ subErrorCode: 'e1' }],
        leg: [{
          poolLeg: {
            legPart: [{
              outcomeRef: { id: '001' }
            }]
          }
        }]
      },
      {
        id: 4,
        betError: [{ code: 'e1' }],
        leg: [{
          poolLeg: {
            legPart: [{
              outcomeRef: { id: '001' }
            }]
          }
        }]
      },
    ];

    const result = service['excludeOutcomeErrors'](failedBets);

    expect(result).toEqual(jasmine.any(Array));
    expect(result.length).toBe(3);
  });

  it('extendOutcomeWithErrors', () => {
    service.generateOutcomeErrorMsg = jasmine.createSpy();

    const outcomes: any[] = [
      { id: 1 },
      { id: 2 },
      { id: 3 }
    ];

    const failedOutcomes: any[] = [
      { id: 1 },
      { id: 2, betGenError: {} }
    ];

    service['extendOutcomeWithErrors'](outcomes, failedOutcomes, {} as any);

    expect(service.generateOutcomeErrorMsg).toHaveBeenCalledTimes(1);
    expect(outcomes[0].error).toBeDefined();
    expect(outcomes[1].error).toBeDefined();
    expect(outcomes[2].error).toBeUndefined();
  });
});
