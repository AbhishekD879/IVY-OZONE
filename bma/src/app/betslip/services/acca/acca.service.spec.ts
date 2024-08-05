import { throwError, of as observableOf,  Observable } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';

import { AccaService } from './acca.service';
import { Bet } from '@betslip/services/bet/bet';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('AccaService', () => {
  let service;
  let bppService;
  let userService;
  let infoDialogService,
    localeService,
    router,
    pubSubService,
    awsService;
  const freebetTrigger = {
    freebetTriggerBetType: 'ACC4',
    freebetTriggerId: '11'
  };
  const offerData = {
    response: {
      respFreebetGetOffers: {
        freebetOffer: [{
          freebetTrigger: [freebetTrigger]
        }]
      }
    }
  };
  let betObj;

  beforeEach(() => {
    bppService = {
      send: jasmine.createSpy('send').and.returnValue(observableOf([]))
    };
    userService = {
      currency: 'EUR'
    };
    infoDialogService = {
      openInfoDialog: jasmine.createSpy('openInfoDialog'),
      closePopUp: jasmine.createSpy('closePopUp')
    };
    localeService = {
      getString: jasmine.createSpy('getString').and.returnValue('some string')
    };
    router = {
      navigateByUrl: jasmine.createSpy('navigateByUrl').and.returnValue(Promise.resolve('success'))
    };
    pubSubService = {
      API: pubSubApi,
      publish: jasmine.createSpy('publish')
    };
    awsService = {
      addAction: jasmine.createSpy('addAction')
    };

    betObj = {
      betOffer: {
        offerType: 'eligible',
        offer: {
          freebetTriggerMaxBonus: '25'
        }
      }
    } as Bet;

    service = new AccaService(bppService, userService, infoDialogService, localeService, router, pubSubService, awsService);
  });

  describe('getFreeBetTriggers', () => {
    it('should return empty array if passed data has no needed info', () => {
      expect(service['getFreeBetTriggers']()).toEqual([]);
      expect(service['getFreeBetTriggers']({ response: null })).toEqual([]);
      expect(service['getFreeBetTriggers']({ response: { respFreebetGetOffers: null } })).toEqual([]);
      expect(service['getFreeBetTriggers']({
        response: {
          respFreebetGetOffers: {
            freebetOffer: []
          }
        }
      })).toEqual([]);
    });

    it('should return freebetTrigger value from first freebetOffer', () => {
      expect(service['getFreeBetTriggers'](offerData)).toEqual([freebetTrigger]);
    });
  });

  describe('getBetOffer', () => {
    it('should return bppService method call result', () => {
      const offerId = '1';
      const result = service['getBetOffer'](offerId);

      expect(bppService.send).toHaveBeenCalledWith('freeBetOffer', { freebetOfferId: offerId });
      expect(result).toEqual(jasmine.any(Observable));
    });
  });

  describe('getCount', function () {
    it('should return number 3 if passed value is equal "TBL"', () => {
      expect(service['getCount']('TBL')).toEqual(3);
    });

    it('should return parsed number if passed value is "ACC"', () => {
      expect(service['getCount']('ACC4')).toEqual(4);
      expect(service['getCount']('ACC10')).toEqual(10);
    });

    it('should return parsed number if passed value is not "TBL" or "ACC"', () => {
      expect(service['getCount']('AC12')).toEqual(12);
      expect(service['getCount']('AC14')).toEqual(14);
    });
  });

  describe('additionalLegs', () => {
    it('should return difference between trigger bet types', () => {
      expect(service['additionalLegs']('TBL', 'TBL')).toEqual(0);
      expect(service['additionalLegs']('ACC2', 'TBL')).toEqual(1);
      expect(service['additionalLegs']('AC10', 'AC12')).toEqual(2);
    });
  });

  describe('getFreeBetOffer', () => {
    it('should return passed data if there are less then 3 legs', fakeAsync(() => {
      const data = { legs: [1, 2] };

      service.getFreeBetOffer(data)
        .subscribe(result => {
          expect(result).toEqual(data);
        });
      tick();
    }));

    it('should return passed data if user\'s currency is not EUR or GBP', fakeAsync(() => {
      const data = { legs: [1, 2, 3] };
      userService.currency = 'UAH';

      service.getFreeBetOffer(data)
        .subscribe(result => {
          expect(result).toEqual(data);
        });
      tick();
    }));

    it('should return passed data if no betOffers passed', fakeAsync(() => {
      const data = { legs: [1, 2, 3], betOffers: [] };

      service.getFreeBetOffer(data)
        .subscribe(result => {
          expect(result).toEqual(data);
        });
      tick();
    }));

    it('should handle error when retrieving bet offers', fakeAsync(() => {
      const data = { legs: [1, 2, 3], betOffers: [{ id: '1' }] };

      bppService.send.and.returnValue(throwError('error'));
      spyOn(service, 'getFreeBetTriggers');

      service.getFreeBetOffer(data)
        .subscribe(() => {}, () => {
          expect(service['getFreeBetTriggers']).not.toHaveBeenCalled();
        });
      tick();
    }));

    it('should not change bet object if no bet offers returned from bppService', fakeAsync(() => {
      const bet = { type: '111', betOffer: {} };
      const data = {
        legs: [1, 2, 3],
        betOffers: [{
          id: '1',
          trigger: { id: '11' },
          betTypeRef: { id: '111' }
        }],
        bets: [bet]
      };
      bppService.send.and.returnValue(observableOf({}));

      service.getFreeBetOffer(data)
        .subscribe(() => {
          expect(bet.betOffer).toEqual({});
        });
      tick();
    }));

    it('should not change bet object if no bets could be mapped to returned bet offers', fakeAsync(() => {
      const bet = { type: 'ACC4', betOffer: {} };
      const data = {
        legs: [1, 2, 3],
        betOffers: [{
          id: '1',
          trigger: { id: '11' },
          betTypeRef: { id: 'ACC4' }
        }],
        bets: [bet]
      };

      bppService.send.and.returnValue(observableOf(offerData));
      freebetTrigger.freebetTriggerId = '2';

      service.getFreeBetOffer(data)
        .subscribe(() => {
          expect(bet.betOffer).toEqual({});
        });
      tick();
    }));

    it('should add betOffer data to bet if it could be mapped to returned bet offers', fakeAsync(() => {
      const bet = {
        type: 'TBL',
        betOffer: {
          offer: null,
          isAccaValid: false,
          additionalLegsCount: 0,
          offerType: ''
        }
      };
      const data = {
        legs: [1, 2, 3],
        betOffers: [{
          id: '1',
          trigger: { id: '11' },
          betTypeRef: { id: 'TBL' },
          offerType: 'eligible'
        }],
        bets: [bet]
      };

      freebetTrigger.freebetTriggerId = data.betOffers[0].trigger.id;
      bppService.send.and.returnValue(observableOf(offerData));

      service.getFreeBetOffer(data)
        .subscribe(() => {
          expect(bet.betOffer.offer).toEqual(freebetTrigger);
          expect(bet.betOffer.isAccaValid).toEqual(true);
          expect(bet.betOffer.additionalLegsCount).toEqual(1);
          expect(bet.betOffer.offerType).toEqual('eligible');
        });
      tick();
    }));
  });

  it('accaInsuransePopup: should open acca insurance information popup', fakeAsync(() => {
    infoDialogService.openInfoDialog.and.callFake((p1, p2, p3, p4, p5, btns) => {
      btns[0].handler();
      btns[1].handler();
    });

    service.accaInsurancePopup('Static block');
    tick();

    expect(infoDialogService.openInfoDialog).toHaveBeenCalledWith(
      jasmine.any(String),
      'Static block',
      'bs-selection-info-dialog acca-insurance-dialog', undefined, undefined,
      jasmine.any(Array)
    );

    expect(localeService.getString).toHaveBeenCalledTimes(3);
    expect(router.navigateByUrl).toHaveBeenCalledWith('/promotions/all');
    expect(pubSubService.publish).toHaveBeenCalledWith('show-slide-out-betslip', false);
    expect(awsService.addAction).toHaveBeenCalledWith('AccaInsurance=>MoreClickRedirectSuccess', jasmine.any(Object));
    expect(infoDialogService.closePopUp).toHaveBeenCalledTimes(2);
  }));

  it('accaInsuransePopup: should open acca insurance information popup with failed redirection', fakeAsync(() => {
    router.navigateByUrl.and.returnValue(Promise.reject('fail'));
    infoDialogService.openInfoDialog.and.callFake((p1, p2, p3, p4, p5, btns) => {
      btns[0].handler();
      btns[1].handler();
    });

    service.accaInsurancePopup('Static block');
    tick();

    expect(infoDialogService.openInfoDialog).toHaveBeenCalledWith(
      jasmine.any(String),
      'Static block',
      'bs-selection-info-dialog acca-insurance-dialog', undefined, undefined,
      jasmine.any(Array)
    );
    expect(awsService.addAction).toHaveBeenCalledTimes(2);

    expect(awsService.addAction).toHaveBeenCalledWith('AccaInsurance=>MoreClickRedirectFailed', jasmine.any(Object));
    expect(infoDialogService.closePopUp).toHaveBeenCalledTimes(2);
    expect(localeService.getString).toHaveBeenCalledTimes(3);
    expect(router.navigateByUrl).toHaveBeenCalledWith('/promotions/all');
    expect(pubSubService.publish).toHaveBeenCalledWith('show-slide-out-betslip', false);
  }));

  it('should check if bet offer is available', () => {
    expect(service.isBetOffer(betObj)).toBeTruthy();
  });

  it('should check if bet offer is available(negative case)', () => {
    betObj.betOffer = undefined;
    expect(service.isBetOffer(betObj)).toBeFalsy();
  });

  it('should check if bet offer is available(negative case - bet not found)', () => {
    betObj = undefined;

    expect(service.isBetOffer(betObj)).toBeFalsy();
  });

  it('should check if acca insurance is enabled in cms and offer is eligible for user', () => {
    expect(service.isAccaInsuranceEligible(betObj)).toBeTruthy();
  });

  it('should check if acca insurance is enabled in cms and offer is eligible for user(negative case)', () => {
    betObj.betOffer.offerType = 'suggested';

    expect(service.isAccaInsuranceEligible(betObj)).toBeFalsy();
  });

  it('should check if acca insurance is enabled in cms and offer is suggested for user', () => {
    betObj.betOffer.offerType = 'suggested';

    expect(service.isAccaInsuranceSuggested(betObj)).toBeTruthy();
  });

  it('should check if acca insurance is enabled in cms and offer is suggested for user(negative case)', () => {
    betObj.betOffer.offerType = 'eligible';

    expect(service.isAccaInsuranceSuggested(betObj)).toBeFalsy();
  });

  it('should get acca insurance offer max bonus for static block dynamic parameter', () => {
    expect(service.getAccaOfferMaxBonus(betObj)).toEqual('25');
  });

  it('should get acca insurance offer max bonus for static block dynamic parameter(negative case)', () => {
    betObj.betOffer.offer = undefined;

    expect(service.getAccaOfferMaxBonus(betObj)).toBeFalsy();
  });
});
