import { throwError, of } from 'rxjs';
import { FreebetsComponent } from './freebets.component';
import { fakeAsync, tick } from '@angular/core/testing';
import { IFreebetToken } from '@app/bpp/services/bppProviders/bpp-providers.model';

describe('FreebetsComponent', () => {
  let component: FreebetsComponent;
  let userService;
  let filtersService;
  let freeBetsService;
  let router;
  let localeService;
  let cmsService;
  let storageService;

  beforeEach(() => {
    userService = {
      status: false
    };
    filtersService = {
      setCurrency: jasmine.createSpy()
    };
    freeBetsService = {
      getFreeBets: jasmine.createSpy().and.returnValue(of(null)),
      getFreeBetWithBetNowLink: jasmine.createSpy('getFreeBetWithBetNowLink'),
      groupByName: jasmine.createSpy('groupByName').and.returnValue(of(null)),
      isFanzone: jasmine.createSpy('isFanzone')

    };
    router = {
      navigate: jasmine.createSpy(),
      navigateByUrl: jasmine.createSpy('navigateByUrl')
    };
    localeService = {
      getString: jasmine.createSpy()
    };
    cmsService = {
      getFreebetsHelperText: jasmine.createSpy().and.returnValue(of(null))
    };
    storageService = {
      set: jasmine.createSpy('set'),
      get: jasmine.createSpy('get')
    };
    component = new FreebetsComponent(userService, filtersService, freeBetsService, router, localeService, cmsService, storageService);
  });

  it('constructor', () => {
    expect(component).toBeTruthy();
  });

  describe('#ngOnInit', () => {
    it('ngOnInit', () => {
      component.hideSpinner = jasmine.createSpy();
      component['addCurrencySymbol'] = jasmine.createSpy();
      component['getTotalFreeBetsBalance'] = jasmine.createSpy();
      component['getTotalBalance'] = jasmine.createSpy();
      component['extendFreebetsData'] = jasmine.createSpy();
      component.totalFreeBetsAmount = '10';

      component.ngOnInit();

      expect(component.hideSpinner).toHaveBeenCalled();
      expect(component['addCurrencySymbol']).toHaveBeenCalledWith(userService.sportBalance);
      expect(component['getTotalFreeBetsBalance']).toHaveBeenCalled();
      expect(component['addCurrencySymbol']).toHaveBeenCalledWith(component.totalFreeBetsAmount);
      expect(component['getTotalBalance']).toHaveBeenCalled();
      expect(component['extendFreebetsData']).toHaveBeenCalled();
    });

    it('ngOnInit (get freebets fail)', fakeAsync(() => {
      component.hideSpinner = jasmine.createSpy();
      freeBetsService.getFreeBets.and.returnValue(throwError(null));

      component.ngOnInit();
      tick();

      expect(component.hideSpinner).toHaveBeenCalled();
      expect(router.navigate).toHaveBeenCalledWith(['/']);
    }));

    it('ngOnInit (get freebets fail) no user status', fakeAsync(() => {
      component.hideSpinner = jasmine.createSpy();
      userService.status = true;
      freeBetsService.getFreeBets.and.returnValue(throwError(null));

      component.ngOnInit();
      tick();

      expect(component.state.error).toBeTruthy();
      expect(component.hideSpinner).toHaveBeenCalled();
      expect(router.navigate).not.toHaveBeenCalled();
    }));

    it('should return helper text', fakeAsync(() => {
      component.hideSpinner = jasmine.createSpy();
      cmsService.getFreebetsHelperText.and.returnValue(of(12345));

      component.ngOnInit();
      tick();

      expect(component.hideSpinner).toHaveBeenCalled();
      expect(component.freebetsHelperText).toEqual(12345 as any);
    }));

    it('test filter the value if token is FRRIDE', fakeAsync(() => {
      const mockData: IFreebetToken[] = [{
        tokenId: '2200000778',
        freebetTokenId: '2200000778',
        freebetOfferId: '28985',
        freebetOfferName: 'CRM-Offer-1',
        freebetOfferDesc: 'LASPRETLASPONONFRBNN',
        freebetTokenDisplayText: '',
        freebetTokenValue: '5.00',
        freebetAmountRedeemed: '0.00',
        freebetTokenRedemptionDate: '2022-03-29 06:47:43',
        freebetRedeemedAgainst: '2022-03-29 06:47:43',
        freebetTokenExpiryDate: '2022-03-29 06:47:43',
        freebetMinPriceNum: '',
        freebetMinPriceDen: '',
        freebetTokenAwardedDate: '2022-03-29 06:47:43',
        freebetTokenStartDate: '2022-03-29 06:47:43',
        freebetTokenType: 'BETBOOST',
        freebetTokenRestrictedSet: {
          level: '',
          id: ''
        },
        freebetGameName: '',
        freebetTokenStatus: '',
        currency: '',
        tokenPossibleBet: {
          name: '',
          betLevel: '',
          betType: '',
          betId: '',
          channels: ''
        },
        tokenPossibleBets: [{
          name: '',
          betLevel: '',
          betType: '',
          betId: '',
          channels: ''
        }],
        freebetOfferType: '',
        tokenPossibleBetTags: {
          'tagName': 'FRRIDE'
        }
      }];
      component.hideSpinner = jasmine.createSpy();
      userService.status = true;
      freeBetsService.getFreeBets.and.returnValue(of(mockData));

      component.ngOnInit();
      tick();


      expect(component.state.error).toBeFalsy();
      expect(component.hideSpinner).toHaveBeenCalled();
      expect(router.navigate).not.toHaveBeenCalled();
    }));
    it('test filter the value if token is not FRRIDE', fakeAsync(() => {
      const mockData: IFreebetToken[] = [{
        tokenId: '2200000778',
        freebetTokenId: '2200000778',
        freebetOfferId: '28985',
        freebetOfferName: 'CRM-Offer-1',
        freebetOfferDesc: 'LASPRETLASPONONFRBNN',
        freebetTokenDisplayText: '',
        freebetTokenValue: '5.00',
        freebetAmountRedeemed: '0.00',
        freebetTokenRedemptionDate: '2022-03-29 06:47:43',
        freebetRedeemedAgainst: '2022-03-29 06:47:43',
        freebetTokenExpiryDate: '2022-03-29 06:47:43',
        freebetMinPriceNum: '',
        freebetMinPriceDen: '',
        freebetTokenAwardedDate: '2022-03-29 06:47:43',
        freebetTokenStartDate: '2022-03-29 06:47:43',
        freebetTokenType: 'BETBOOST',
        freebetTokenRestrictedSet: {
          level: '',
          id: ''
        },
        freebetGameName: '',
        freebetTokenStatus: '',
        currency: '',
        tokenPossibleBet: {
          name: '',
          betLevel: '',
          betType: '',
          betId: '',
          channels: ''
        },
        tokenPossibleBets: [{
          name: '',
          betLevel: '',
          betType: '',
          betId: '',
          channels: ''
        }],
        freebetOfferType: '',
      }];
      component.hideSpinner = jasmine.createSpy();
      userService.status = true;
      freeBetsService.getFreeBets.and.returnValue(of(mockData));

      component.ngOnInit();
      tick();

      expect(component.state.error).toBeFalsy();
      expect(component.hideSpinner).toHaveBeenCalled();
      expect(router.navigate).not.toHaveBeenCalled();
    }));
  });

  it('indexNumber', () => {
    expect(component.indexNumber(0)).toBe(0);
    expect(component.indexNumber(1)).toBe(1);
  });

  it('#trackByTokenId', () => {
    const result = component.trackByTokenId(1, { freebetTokenId: '1' } as any);
    expect(result).toBe(1);
  });

  it('getTotalBalance', () => {
    component['userService'] = { sportBalance: '5' } as any;
    component.totalFreeBetsAmount = '5';
    component['addCurrencySymbol'] = jasmine.createSpy();

    component['getTotalBalance']();
    expect(component['addCurrencySymbol']).toHaveBeenCalledWith(10);
  });

  it('addCurrencySymbol', () => {
    component['userService'] = { currencySymbol: '$' } as any;
    component['addCurrencySymbol'](1);
    expect(filtersService.setCurrency).toHaveBeenCalledWith(1, component['userService'].currencySymbol);
  });

  it('extendFreebetsData', () => {
    component['addCurrencySymbol'] = jasmine.createSpy();
    component.freebets = [{
      freebetTokenId: 'id',
      freebetTokenValue: 'value'
    }] as any[];

    component['extendFreebetsData']();

    expect(component['addCurrencySymbol']).toHaveBeenCalledWith(
      component.freebets[0].freebetTokenValue
    );
    expect(component.freebets[0].redirectUrl).toBe('/freebets/id');
  });

  describe('getTotalFreeBetsBalance', () => {
    it('should handle freebets stored in component', () => {
      component.freebets = [
        { freebetTokenValue: '4' },
        { freebetTokenValue: '3.2567' }
      ] as any[];
      expect(component['getTotalFreeBetsBalance']()).toBe('7.26');
    });

    it('should handle case when no freebets stored in component', () => {
      component.freebets = undefined;
      expect(component['getTotalFreeBetsBalance']()).toBe('0.00');
    });
  });
  describe('getLabelText', () => {
    it('label text for fanzonebet ', () => {
      freeBetsService.isFanzone.and.returnValue(true);
      localeService.getString.and.returnValue('Fanzone Freebet');
      expect(component['getLabelText']('Fanzone')).toBe('Fanzone Freebet');
    });

    it('label text for freebet', () => {
      freeBetsService.isFanzone.and.returnValue(false);
      localeService.getString.and.returnValue('Free Bet');
      expect(component['getLabelText']('Free Bet')).toBe('Free Bet');
    });
  });

  describe('#navigateToEvent', () => {
    it('should successfully navigate', () => {
      const freeBet = { betNowLink: 'someLink' } as any;
      freeBetsService.getFreeBetWithBetNowLink.and.returnValue(of(freeBet));
      component.navigateToEvent(freeBet);
      expect(router.navigateByUrl).toHaveBeenCalledWith('someLink');
      expect(freeBet.pending).toBeFalsy();
    });

    it('shouldn`t successfully navigate', () => {
      const freeBet = { betNowLink: '' } as any;
      freeBetsService.getFreeBetWithBetNowLink.and.returnValue(throwError({}));
      component.navigateToEvent(freeBet);
      expect(router.navigateByUrl).not.toHaveBeenCalled();
      expect(freeBet.pending).toBeFalsy();
    });
  });

  it('#stopOuterAction', () => {
    const event = {
      stopPropagation: jasmine.createSpy('stopPropagation')
    } as any;
    component.stopOuterAction(event);
    expect(event.stopPropagation).toHaveBeenCalledTimes(1);
  });

  describe('#group freebets by sportsname', () => {
    it('shouldn freeBetsService.groupByName returns undefined', fakeAsync(() => {
      component.freebets = [];
      freeBetsService.groupByName.and.returnValue(of(undefined));
      component['groupByName']();
      tick();
      expect(component.freebetsGroup).toEqual(undefined);
    }));

    it('shouldn`t call freeBetsService.groupByName', fakeAsync(() => {
      component.freebets = [];
      component.ngOnInit();
      tick();
      expect(freeBetsService.groupByName).not.toHaveBeenCalled();
    }));

    it('should group freebets by Sportname', fakeAsync(() => {
      const fb = {
        'freebetOfferName': 'HR_Freebet',
        'freebetOfferDesc': 'LASPRETLASPONONFRBNN',
        'freebetTokenValue': '1.00',
        'tokenPossibleBet': {
          'name': 'Horse_Racing',
          'betLevel': 'CATEGORY',
          'betType': '',
          'betId': '21',
          'channels': ''
        }
      };
      const name = 'Horse Racing';
      const groupedFreebets = { [name]: [fb] };
      freeBetsService.groupByName.and.returnValue(of(groupedFreebets));
      component.ngOnInit();
      component.freebets = [fb] as any[];
      component['groupByName']();
        expect(component.freebetsGroup as any).toEqual(jasmine.objectContaining(groupedFreebets));
        expect(Object.keys(component.freebetsGroup)).toEqual([name]);
      tick();
    }));
  });
  it('should call availableTotefreebets', () => {
    storageService.get.and.returnValue(undefined);
    component["availableTotefreebets"](undefined);
    expect(component.freebets.length).toEqual(0);
  });
  it('should call availableTotefreebets with usedToteFreebets', () => {
    storageService.get.and.returnValue(['1']);
    component["availableTotefreebets"]([{freebetTokenId: '2'}]);
    expect(component.freebets.length).toEqual(1);
  });
});
