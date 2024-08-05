import { BybHelperService } from './byb-helper.service';
import { fakeAsync, tick } from '@angular/core/testing';
import { BYBBet } from '@yourcall/models/bet/byb-bet';

describe('#BybHelperService', () => {

  let service,
      coreTools,
      localeService,
      userService,
      fracToDecService;

  beforeEach(() => {
    coreTools = {
      getOwnDeepProperty: jasmine.createSpy().and.returnValue('')
    };
    localeService = {
      getString: jasmine.createSpy()
    };
    userService = {
    };
    fracToDecService = {
      getFormattedValue: jasmine.createSpy('getFormattedValue')
    };

    service = new BybHelperService(
      coreTools,
      localeService,
      userService,
      fracToDecService
    );
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  describe('#getPlaceBetErrorMsg', () => {
    it('should return timeout error', () => {
      service.getPlaceBetErrorMsg({
        subErrorCode: 'SERVICE_ERROR'
      });
      expect(localeService.getString).toHaveBeenCalledWith('yourCall.timeoutError');
    });

    it('should return general Place Bet error', () => {
      service.getPlaceBetErrorMsg({
        subErrorCode: 'DEFAULT'
      });
      expect(localeService.getString).toHaveBeenCalledWith('yourCall.generalPlaceBetError');
    });

    it('should return event Started error', () => {
      service.getPlaceBetErrorMsg({
        subErrorCode: 'EVENT_STARTED'
      });
      expect(localeService.getString).toHaveBeenCalledWith('yourCall.eventStartedError');
    });

    it('should return stake Exceeded error', () => {
      service.getPlaceBetErrorMsg({
        subErrorCode: 'STAKE_HIGH'
      });
      expect(localeService.getString).toHaveBeenCalledWith('yourCall.stakeExceeded');
    });

    it('should return stake Value Exceeded error', () => {
      service.getPlaceBetErrorMsg({
        maxStake: 100,
        subErrorCode: 'STAKE_HIGH'
      });
      expect(localeService.getString).toHaveBeenCalledWith('yourCall.stakeValueExceeded',
        {stake: 100, currency: undefined});
    });

    it('should return price Change Warning', () => {
      service.getPlaceBetErrorMsg({
        subErrorCode: 'PRICE_CHANGED'
      });
      expect(localeService.getString).toHaveBeenCalledWith('yourCall.priceChangeWarning');
    });

    it('should return default', () => {
      const res = service.getPlaceBetErrorMsg('');
      expect(res).toEqual('');
    });
  });

  describe('#createBet', () => {
    it('should create Bet', () => {
      const betData = {
        dashboardData: {
          selections: {},
          game: {
            obTypeId: 234,
            obEventId: 456
          }
        }
      } as any;
      expect(service.createBet(betData) instanceof BYBBet).toBeTruthy();
    });
  });

  describe('#parseOddsError', () => {
    it('should parse odds error', () => {
      const error = 'erroe';
      const res = service.parseOddsError(error);

      expect(coreTools['getOwnDeepProperty']).toHaveBeenCalledWith(error, 'data.responseMessage');
      expect(res).toEqual('');
    });
  });

  describe('#createSelectionData', () => {
    it('should create Selection Data', () => {
      const result = service['createSelectionData']({
        selections: [{
          selection: {
            playerId: 1,
            statisticId: 2,
            value: 333,
            id: 1
          },
        },
          {
            selection: {
              statisticId: 2,
              value: 55,
              id: 80
            },
          }] as any,
        game: {
          obEventId: 2
        } as any
      });
      expect(result).toEqual({
        obEventId: 2,
        selectionIds: [ 80 ],
        playerSelections: [{
          statId: 2,
          playerId: 1,
          line: 333
        }]
      });
    });
  });

  describe('#buildOddsParams', () => {
    it('should build Odds Params', () => {
      const selections = [{
        playerId: 1,
        statisticId: 2,
        value: 333,
        id: 1} , {
        statisticId: 3,
        value: 555,
        id: 7}] as any;
      const result = service['buildOddsParams'](selections, {
        _obEventId: 2
      } as any);

      expect(result).toEqual({
        obEventId: 2,
        selectionIds: [7],
        playerSelections: [{
          statId: 2,
          playerId: 1,
          line: 333
        }]
      });
    });
  });

  describe('parseOddsValue', () => {
    let successHandler,
      errorHandler;

    beforeEach(() => {
      successHandler = jasmine.createSpy('successHandler');
      errorHandler = jasmine.createSpy('errorHandler');
    });

    it('should return odds in dec format',  fakeAsync(() => {
      const actualResult = service.parseOddsValue({data: {priceNum: 1, priceDen: 2}});

      actualResult.then(successHandler, errorHandler);
      tick();

      expect(successHandler).toHaveBeenCalled();
      expect(fracToDecService.getFormattedValue).toHaveBeenCalledWith(1, 2);
    }));

    it('should not return odds in dec format if priceNum is not defined',  fakeAsync(() => {
      const actualResult = service.parseOddsValue({data: {priceDen: 2}});

      actualResult.then(successHandler, errorHandler);
      tick();

      expect(errorHandler).toHaveBeenCalled();
      expect(fracToDecService.getFormattedValue).not.toHaveBeenCalled();
    }));

    it('should not return odds in dec format if priceDen is not defined',  fakeAsync(() => {
      const actualResult = service.parseOddsValue({data: {priceNum: 1}});

      actualResult.then(successHandler, errorHandler);
      tick();

      expect(errorHandler).toHaveBeenCalled();
      expect(fracToDecService.getFormattedValue).not.toHaveBeenCalled();
    }));

    it('should not return odds in dec format if response data is absent',  fakeAsync(() => {
      const actualResult = service.parseOddsValue({});

      actualResult.then(successHandler, errorHandler);
      tick();

      expect(errorHandler).toHaveBeenCalled();
      expect(fracToDecService.getFormattedValue).not.toHaveBeenCalled();
    }));
  });
});
