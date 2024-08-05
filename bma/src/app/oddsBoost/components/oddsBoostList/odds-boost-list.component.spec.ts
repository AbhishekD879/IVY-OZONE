import { of as observableOf } from 'rxjs';
import { OddsBoostListComponent } from './odds-boost-list.component';
import { SimpleChange, SimpleChanges } from '@angular/core';
import { IFreebetToken } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { discardPeriodicTasks, fakeAsync, flush, tick } from '@angular/core/testing';

describe('OddsBoostListComponent', () => {
  let component: OddsBoostListComponent;
  let freeBetsService;
  let oddsBoostService;
  let userService;
  let currencyPipe;
  let cmsService;
  let windowRef;

  beforeEach(() => {
    freeBetsService = {
      getOddsBoostsWithCategories: jasmine.createSpy('getOddsBoostsWithCategories').and.returnValue(observableOf(
        [{
          categoryId: '16',
          freebetTokenId: '10',
          freebetMaxStake: '5.00',
          freebetTokenDisplayText: 'asd|asd'
        }]
      ))
    };

    oddsBoostService = {
      sortPageTokens: jasmine.createSpy('sortPageTokens')
    };

    userService = {
      currencySymbol: '£'
    };
    currencyPipe = {
      transform: jasmine.createSpy('transform').and.returnValue('£50')
    };
    windowRef = {nativeWindow: {clearInterval:  window.setInterval,
     setInterval: window.setInterval}}
    component = new OddsBoostListComponent(freeBetsService, oddsBoostService, userService, currencyPipe, cmsService, windowRef);
  });

  it('constructor', () => {
    expect(component).toBeDefined();
  });

  it('ngOnChanges', () => {
    const changesObj: SimpleChanges = {
      oddsBoosts: new SimpleChange(undefined, [{ freebetTokenId: '126' }], false)
    };
    component.ngOnChanges(changesObj);
    expect(freeBetsService.getOddsBoostsWithCategories).toHaveBeenCalled();
    expect(currencyPipe.transform).toHaveBeenCalledTimes(1);
    expect(currencyPipe.transform).toHaveBeenCalledWith('5.00', userService.currencySymbol, 'code');
    expect(oddsBoostService.sortPageTokens).toHaveBeenCalledTimes(1);
  });

  it('ngOnChanges no tokens', () => {
    const changesObj: SimpleChanges = {
      oddsBoosts: new SimpleChange(undefined, null, false)
    };
    component.ngOnChanges(changesObj);
    expect(freeBetsService.getOddsBoostsWithCategories).not.toHaveBeenCalled();
  });

  it('ngOnChanges no category id', () => {
    freeBetsService.getOddsBoostsWithCategories.and.returnValue(observableOf([{
      freebetMaxStake: '50',
      freebetTokenId: '10',
      freebetTokenDisplayText: 'asd|asd'
    }]));

    const changesObj: SimpleChanges = {
      oddsBoosts: new SimpleChange(undefined, [{ freebetTokenId: '126' }], false)
    };
    component.ngOnChanges(changesObj);
    expect(oddsBoostService.sortPageTokens).toHaveBeenCalledWith([{
      freebetMaxStake: '£50',
      freebetOfferDesc: 'asd',
      freebetOfferName: 'asd',
      freebetTokenDisplayText: 'asd|asd',
      freebetTokenId: '10'
    }]);
  });

  it('ngOnChanges should not call "transform"', () => {

    freeBetsService.getOddsBoostsWithCategories.and.returnValue(observableOf([{
      freebetMaxStake: '£50',
      freebetTokenDisplayText: 'asd|asd',
    }]));

    const changesObj: SimpleChanges = {
      oddsBoosts: new SimpleChange(undefined, [{ freebetTokenId: '126' }], false)
    };

    component.ngOnChanges(changesObj);

    expect(currencyPipe.transform).not.toHaveBeenCalled();
  });

  it('ngOnChanges should call "transform"', () => {

    freeBetsService.getOddsBoostsWithCategories.and.returnValue(observableOf([{
      freebetMaxStake: 5,
      freebetTokenDisplayText: 'asd|asd',
    }]));

    const changesObj: SimpleChanges = {
      oddsBoosts: new SimpleChange(undefined, [{ freebetTokenId: '126' }], false)
    };

    component.ngOnChanges(changesObj);

    expect(currencyPipe.transform).toHaveBeenCalledWith('5.00', '£', 'code');
  });

  it('should get objectKeys', () => {
    expect(component.objectKeys({ a: 1, b: 2 })).toEqual(['a', 'b']);
  });

  it('should trackByOddsBoosts', () => {
    expect(component.trackByOddsBoosts(2, <IFreebetToken>{ freebetTokenId: '100001' })).toEqual('2100001');
  });

  it('should trackByCategory', () => {
    expect(component.trackByCategory(1, '32')).toEqual('1_32');
  });

  it('getOddsBoostsWithCategories, no data', () => {
    freeBetsService.getOddsBoostsWithCategories.and.returnValue(observableOf(undefined));

    const changesObj: SimpleChanges = {
      oddsBoosts: new SimpleChange(undefined, [{ freebetTokenId: '126' }], false)
    };
    component.ngOnChanges(changesObj);

    expect(oddsBoostService.sortPageTokens).not.toHaveBeenCalled();
  });


  it('should update sortedTokensData when changes are detected', () => {
    const changes = { sortedTokensData: { isFirstChange: () => false } as any };
    const previousSortedTokensData = component.sortedTokensData;
    component.ngOnChanges(changes);
    expect(component.sortedTokensData).toEqual(previousSortedTokensData);
  });

  it('should not update sortedTokensData when changes are detected but isFirstChange is true', () => {
    const changes = { sortedTokensData: { isFirstChange: () => true } as any };
    const previousSortedTokensData = component.sortedTokensData;
    component.ngOnChanges(changes);
    expect(component.sortedTokensData).toEqual(previousSortedTokensData);
  });

  it('should not update sortedTokensData when no changes are detected', () => {
    const changes = {};
    const previousSortedTokensData = component.sortedTokensData;
    component.ngOnChanges(changes);
    expect(component.sortedTokensData).toEqual(previousSortedTokensData);
  });

  it('should return the expiry date if tab is true', () => {
    const oddsboostData = { freebetTokenExpiryDate: '2023/06/27 23:59:59' };
    component.tab = true;
    const result = component.countDownTimer(oddsboostData as any);
    const expectedDate = new Date('2023/06/27 23:59:59');
    expect(result).toEqual(expectedDate);
  });

  it('should return the start date id tab is false', () => {
    const oddsboostData = { freebetTokenStartDate: '2023/06/27 00:00:01' };
    component.tab = false;
    const result = component.countDownTimer(oddsboostData as any);
    const expectedDate = new Date('2023/06/27 00:00:01');
    expect(result).toEqual(expectedDate);
  });

  it('should update the tokenExpired obj with the tokenData', () => {
    const tokenData = { freebetTokenId: '1234', tokenExpire: true };
    component.expireTokenInfo(tokenData);
    const expectedTokenExpired = { '1234': true };
    expect(component.tokenExpired).toEqual(expectedTokenExpired);
  });

  it('should update the tokenExpired obj with multiple tokenData', () => {
    const tokenData1 = { freebetTokenId: '1234', tokenExpire: true };
    const tokenData2 = { freebetTokenId: '5678', tokenExpire: false };
    component.expireTokenInfo(tokenData1);
    component.expireTokenInfo(tokenData2);
    const expectedTokenExpired = { '1234': true, '5678': false };
    expect(component.tokenExpired).toEqual(expectedTokenExpired);
  });

  it('should set nextBoost if it is not already set and tab is true', () => {
    component.tab = true;
    component.timerValue = true;
    const oddBoost = { freebetTokenExpiryDate: '2023-07-01', tokenId: '1' } as any;

    component.leastTimeTokenInfo(oddBoost);

    expect(component.nextBoost).toEqual(oddBoost);
  });

  it('should set nextBoost if it is not already set and tab is false', () => {
    component.tab = false;
    component.timerValue = true;
    const oddBoost = { freebetTokenStartDate: '2023-07-01', tokenId: '1' } as any;

    component.leastTimeTokenInfo(oddBoost);

    expect(component.nextBoost).toEqual(oddBoost);
  });

  it('should not change nextBoost if oddBoost is not earlier', () => {
    component.tab = true;
    component.timerValue = true;
    const existingBoost = { freebetTokenExpiryDate: '2023-07-02', tokenId: '1' } as any;
    const oddBoost = { freebetTokenExpiryDate: '2023-07-01', tokenId: '2' } as any;

    component.nextBoost = existingBoost;
    component.leastTimeTokenInfo(oddBoost);

    expect(component.nextBoost).toEqual(oddBoost);
  });

  it('should emit leastTimeToken if nextBoost is same as oddBoost', fakeAsync((done) => {
    component.tab = true;
    component.timerValue = true;
    const oddBoost = { freebetTokenExpiryDate: '2023-07-01', tokenId: '1' } as any;

    component.nextBoost = oddBoost;
    component.leastTimeToken.subscribe((leastTimeToken) => {
      expect(leastTimeToken).toEqual(oddBoost.freebetTokenExpiryDate);
    });

    component.leastTimeTokenInfo(oddBoost);
    tick(1000)
    flush();
    discardPeriodicTasks();
  }));

  describe('clearTimer', () => {
    it('clearTimer' , () => {
      component.timerValue = true;
      component.clearTimer();
      expect(component.timerValue).toBeTruthy();
    })
  }) 

  describe('ngOnDestroy', () => {
    it('ngOnDestroy' , () => {
      spyOn(component, 'clearTimer');
      component.ngOnDestroy();
      expect(component.clearTimer).toHaveBeenCalled();
    })
  }) 
});
