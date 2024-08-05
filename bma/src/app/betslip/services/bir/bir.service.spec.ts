import { of as observableOf, throwError } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';

import { BirService } from './bir.service';
import { IReadBetRequest, IReadBetResponse, IBet } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { IBirResponse } from '@betslip/services/bir/bir.model';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('BirService', () => {
  let service;
  let timeService;
  let bppService;
  let pubSubService;

  beforeEach(() => {
    timeService = {
      secondsToMiliseconds: jasmine.createSpy('secondsToMiliseconds').and.callFake(value => value * 1000)
    };
    bppService = {
      send: jasmine.createSpy('send').and.returnValue(observableOf({})),
      showErrorPopup: jasmine.createSpy('showErrorPopup')
    };
    pubSubService = {
      API: pubSubApi,
      publishSync: jasmine.createSpy('publishSync')
    };

    service = new BirService(timeService, bppService, pubSubService);
  });

  describe('reduceErrors', () => {
    it('should return empty list if no errors in response', () => {
      expect(service.reduceErrors({} as IReadBetResponse)).toEqual([]);
      expect(service.reduceErrors({ betError: null } as IReadBetResponse)).toEqual([]);
    });

    it('should return error in list if it was in response', () => {
      const response = {
        betError: {
          subErrorCode: 'INTERNAL',
          code: '500',
          price: [{
            den: 1,
            num: 2
          }],
          outcomeRef: { id: '1' }
        }
      } as IReadBetResponse;

      expect(service.reduceErrors(response)).toEqual([{
        subCode: response.betError.subErrorCode,
        code: response.betError.code,
        price: response.betError.price,
        outcomeRef: response.betError.outcomeRef
      }]);
    });
  });

  describe('getNonBirIds', () => {
    it('should return ids only for non BIR bets', () => {
      const birResponse = {
        bets: [{
          provider: 'OpenBet',
          id: 1
        }, {
          provider: 'OpenBetBir',
          id: 2
        }, {
          provider: 'OpenBetBir',
          id: 3
        }, {
          provider: 'OpenBetNonBir',
          id: 4
        }]
      } as IBirResponse;

      expect(service.getNonBirIds(birResponse)).toEqual([1, 4]);
    });
  });

  it('should build readBet request params', () => {
    const idArray = [1, 3];
    expect(service.buildReadBetRequest(idArray)).toEqual({
      betRef: [{
        id: '1',
        provider: 'OpenBetBir'
      }, {
        id: '3',
        provider: 'OpenBetBir'
      }]
    });
  });

  describe('parseResponse', () => {
    it('should parse response with error', () => {
      const nonBirIds = [1, 3];
      const readBetResponse = {
        bet: [{ id: 2 }],
        betError: {
          subErrorCode: 'INTERNAL',
          code: '500',
          price: [{
            den: 1,
            num: 2
          }],
          outcomeRef: { id: '1' }
        }
      } as IReadBetResponse;

      expect(service.parseResponse(nonBirIds, readBetResponse)).toEqual({
        errs: [{
          subCode: readBetResponse.betError.subErrorCode,
          code: readBetResponse.betError.code,
          price: readBetResponse.betError.price,
          outcomeRef: readBetResponse.betError.outcomeRef
        }],
        ids: [2, ...nonBirIds],
        bets: readBetResponse.bet
      });
    });

    it('should parse response with no errors', () => {
      const nonBirIds = [1, 3];
      const readBetResponse = {
        bet: [{ id: 2 }, { id: 4 }]
      } as IReadBetResponse;

      expect(service.parseResponse(nonBirIds, readBetResponse)).toEqual({
        errs: [],
        ids: [4, 2, ...nonBirIds],
        bets: readBetResponse.bet
      });
    });
  });

  describe('sendReadBetRequest', () => {
    it('should handle error of bppService', fakeAsync(() => {
      const error = { code: '404' };
      const request = {
        betRef: [{
          id: '1',
          provider: 'OpenBetBir'
        }]
      } as IReadBetRequest;

      bppService.send.and.returnValue(throwError(error));

      service.sendReadBetRequest(request).subscribe(() => {}, errorResponse => {
        expect(errorResponse).toEqual(error);
        expect(bppService.showErrorPopup).toHaveBeenCalledWith('betPlacementError');
      });
      tick();
    }));

    it('should handle success response of bppService', fakeAsync(() => {
      const readBetResponse = {
        bet: [{ id: 2 }, { id: 4 }]
      } as IReadBetResponse;
      const request = {
        betRef: [{
          id: '1',
          provider: 'OpenBetBir'
        }]
      } as IReadBetRequest;

      bppService.send.and.returnValue(observableOf(readBetResponse));

      service.sendReadBetRequest(request).subscribe(response => {
        expect(response).toEqual(readBetResponse);
        expect(bppService.showErrorPopup).not.toHaveBeenCalled();
      });
      tick();
    }));
  });

  it('should wait for max value of confirmationExpectedAt for all bets', fakeAsync(() => {
    const bets = [{
      documentId: '1',
      confirmationExpectedAt: '20'
    }, {
      confirmationExpectedAt: '24'
    }, {
      confirmationExpectedAt: '23'
    }] as IBet[];
    const idArray = [1, 2];

    service.wait(bets, idArray);

    expect(pubSubService.publishSync).toHaveBeenCalledWith(pubSubService.API.SET_BIR_COUNTDOWN_TIMER, 25);
  }));

  it('birBets & birBetsIds', () => {
    service['birResponse'] = {
      bets: [
        { id: 1, provider: 'OpenBetBir' },
        { id: 2 }
      ]
    };
    expect(service.birBets).toEqual([{ id: 1, provider: 'OpenBetBir' }]);
    expect(service.birBetsIds).toEqual([1]);
  });

  it('exectuteBIR', fakeAsync(() => {
    const readBetResponse = {
      bets: [{ id: 1 }]
    };
    const birResponse = {
      bets: [{ id: 1, confirmationExpectedAt: -1, provider: 'OpenBetBir' }]
    };
    spyOn(service, 'parseResponse');
    spyOn(service, 'sendReadBetRequest').and.returnValue(observableOf(readBetResponse));

    service.exectuteBIR(birResponse).subscribe();
    tick();

    expect(service['birResponse']).toBe(birResponse);
    expect(service['parseResponse']).toHaveBeenCalledWith([], readBetResponse);
  }));
});
