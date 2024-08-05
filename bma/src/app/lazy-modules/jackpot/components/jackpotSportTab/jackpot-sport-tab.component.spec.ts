import { throwError, of as observableOf } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';

import { JackpotSportTabComponent } from './jackpot-sport-tab.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('JackpotSportTabComponent', () => {
  let component: JackpotSportTabComponent;
  let jackpotSportTabService;
  let localeService;
  let timeService;
  let pubsub;
  let betPlacementErrorTrackingService;
  let windowRefService;
  let sbFiltersService;
  let filtersService;
  let jackpotReceiptService;
  let domToolsService;
  let dialogService;
  let router;
  let userService;
  let accountUpgradeLinkService;

  beforeEach(() => {
    localeService = {
      getString: jasmine.createSpy('getString').and.callFake((str, eventsArray) => str + eventsArray.length)
    };
    jackpotSportTabService = {
      getStake: () => { },
      sortJackpotData: () => events,
      placeJackpotBet: jasmine.createSpy().and.returnValue({ subscribe: () => { } }),
      isSelected: jasmine.createSpy().and.returnValue(true),
      addStake: jasmine.createSpy(),
      addBet: jasmine.createSpy(),
      removeAllBets: jasmine.createSpy(),
      removeStake: jasmine.createSpy(),
      betsArray: jasmine.createSpy(),
      makeLuckyDip: jasmine.createSpy()
    };
    timeService = {
      formatByPattern: jasmine.createSpy('formatByPattern').and.returnValue('EEEE, d-MMM-yy. h:mm a')
    };
    pubsub = {
      subscribe: jasmine.createSpy('subscribe')
        .and.callFake((a: string, b: string[] | string, fn: Function) => fn()),
      publish: jasmine.createSpy(),
      unsubscribe: jasmine.createSpy(),
      API: pubSubApi
    };
    betPlacementErrorTrackingService = {
      sendJackpot: jasmine.createSpy()
    };
    windowRefService = {
      nativeWindow: {
        innerHeight: 100,
        location: {
          href: ''
        }
      },
      document: {
        body: {
          scrollTop: 50
        },
        documentElement: {
          scrollTop: 50
        }
      }
    };
    sbFiltersService = {
      outcomeMinorCodeName: jasmine.createSpy('outcomeMinorCodeName')
    };
    filtersService = {
      setCurrency: jasmine.createSpy('setCurrency').and.returnValue('10e')
    };
    jackpotReceiptService = {
      setReceiptData: jasmine.createSpy('setReceiptData')
    };
    domToolsService = {
      getOffset: jasmine.createSpy('getOffset').and.returnValue({ top: 150 })
    };
    dialogService = {
      openDialog: jasmine.createSpy('openDialog'),
      API: {
        howToPlay: 'howToPlay',
        luckyDip: 'luckyDip'
      }
    };
    router = {
      navigate: jasmine.createSpy('navigate')
    };
    userService = {
      isInShopUser: () => false
    };
    accountUpgradeLinkService = {
      inShopToMultiChannelLink: () => false
    };

    const events = [{
      name: 'Burnley vs Rochester',
      startTime: 1552748400000,
      markets: [
        {
          outcomes: [{
            name: '3'
          }]
        }
      ]
    }];

    component = new JackpotSportTabComponent(betPlacementErrorTrackingService, jackpotReceiptService, sbFiltersService,
      filtersService, domToolsService, dialogService, jackpotSportTabService, localeService, windowRefService,
      timeService, router, pubsub, userService, accountUpgradeLinkService);

    component.sport = {
      jackpot: jasmine.createSpy('jackpot').and.returnValue(Promise.resolve(events))
    };

  });

  it('should unsync from pubSubService in onDestroy', () => {
    component.ngOnDestroy();

    expect(pubsub.unsubscribe).toHaveBeenCalledWith('JackpotSportTabComponent');
  });

  it('@ngInit should load init data', fakeAsync(() => {
    expect(component.isLoaded).toBe(false);
    expect(component.isResponseError).toBe(false);
    component.ngOnInit();
    tick();
    expect(component.initialData).toBeTruthy();
  }));

  it('should return error', fakeAsync(() => {
    component['sport'].jackpot = jasmine.createSpy().and.returnValue(Promise.reject());
    component['initialData[0]'] = { pool: null };
    component.ngOnInit();
    tick();
    expect(component.isLoaded).toBeTruthy();
    expect(component.isResponseError).toBeTruthy();
    expect(component.initialData).toEqual([]);
  }));

  it('should add number of jackpot events to header', fakeAsync(() => {
    component.ngOnInit();
    tick();
    expect(component['localeService'].getString).toHaveBeenCalledWith('fb.headerMessage', [1]);
    expect(component.headerMessage).toEqual('fb.headerMessage1');
  }));

  it('should call countSelections', fakeAsync(() => {
    spyOn(component as any, 'loadJackpotData').and.callThrough();
    spyOn(component as any, 'countSelections').and.callThrough();
    spyOn(jackpotSportTabService, 'sortJackpotData').and.returnValue(null);
    component['placeJackpotBets'] = jasmine.createSpy();
    component.ngOnInit();
    tick();

    expect(component['countSelections']).toHaveBeenCalled();
  }));

  describe('@placeJackpotBets', () => {

    it('should redirect in-shop user to upgrade page', () => {
      component.initialData[0] = { pool: true } as any;
      component['removeAllBets'] = jasmine.createSpy('removeAllBets');
      component['jackpotSportTabService'].placeJackpotBet = jasmine.createSpy().and.returnValue(observableOf({bet: [{}]}));

      Object.defineProperty(component['accountUpgradeLinkService'], 'inShopToMultiChannelLink', { get: () => 'http://ffs.com' });
      component['userService'].isInShopUser = () => true;

      component.placeJackpotBets();

      expect(component['windowRef'].nativeWindow.location.href).toEqual('http://ffs.com');

      expect(component['jackpotSportTabService'].placeJackpotBet).not.toHaveBeenCalled();
      expect(component.removeAllBets).not.toHaveBeenCalled();
    });

    it('should call removeAllBets', () => {
      component.initialData[0] = { pool: true } as any;
      component['removeAllBets'] = jasmine.createSpy('removeAllBets');
      component['jackpotSportTabService'].placeJackpotBet = jasmine.createSpy().and.returnValue(observableOf({bet: [{}]}));
      component.placeJackpotBets();
      expect(component['jackpotSportTabService'].placeJackpotBet).toHaveBeenCalled();
      expect(component.removeAllBets).toHaveBeenCalled();
    });

    it('placebet error should SHOW_LOCATION_RESTRICTED_BETS_DIALOG', () => {
      component['jackpotSportTabService'].placeJackpotBet = jasmine.createSpy().and.returnValue(throwError({
        code: 'status.CountryBanned'
      }));
      spyOn(component as any, 'scrollToError').and.callThrough();
      component.initialData[0] = { pool: true } as any;
      component.placeJackpotBets();
      expect(component.betRejectedError).toBeTruthy();
      expect(component['scrollToError']).toHaveBeenCalled();
      expect(pubsub.publish).toHaveBeenCalledWith(pubSubApi.SHOW_LOCATION_RESTRICTED_BETS_DIALOG);
    });

    it('placebet error should OPEN_LOGIN_DIALOG', () => {
      component['jackpotSportTabService'].placeJackpotBet = jasmine.createSpy().and.returnValue(throwError({
        code: 'NOT_LOGGEDIN'
      }));
      // @ts-ignore
      component.initialData[0] = { pool: true };
      component.placeJackpotBets();
      expect(pubsub.publish).toHaveBeenCalledWith(pubsub.API.OPEN_LOGIN_DIALOG, {
        placeBet: 'jackpot',
        moduleName: 'footballjackpot'
      });
    });

    it('placebet error INSUFFICIENT_FUNDS', () => {
      component['jackpotSportTabService'].placeJackpotBet = jasmine.createSpy().and.returnValue(throwError({
        code: 'INSUFFICIENT_FUNDS'
      }));
      component.initialData[0] = <any>{ pool: true };
      component.placeJackpotBets();
      expect(component['insuficientFoundsError']).toEqual(true);
    });

    it('placebet error BET_REJECTED', () => {
      component['jackpotSportTabService'].placeJackpotBet = jasmine.createSpy().and.returnValue(throwError({
        code: 'BET_REJECTED'
      }));
      component.initialData[0] = <any>{ pool: true };
      component.placeJackpotBets();
      expect(component['betRejectedError']).toEqual(true);
    });

    it('placebet error CUSTOM', () => {
      component['jackpotSportTabService'].placeJackpotBet = jasmine.createSpy().and.returnValue(throwError({
        code: 'CUSTOM'
      }));
      component.initialData[0] = <any>{ pool: true };
      component.placeJackpotBets();
      expect(component['internalError']).toEqual(true);
    });
  });

  it('subscribe to events', () => {
    component['isLoginAndPlaceBets'] = true;
    component.placeJackpotBets = jasmine.createSpy('placeJackpotBets');
    component['subscribe']();
    expect(pubsub.subscribe).toHaveBeenCalledWith('JackpotSportTabComponent', pubSubApi.LOGIN_POPUPS_END, jasmine.any(Function));
    expect(component['isLoginAndPlaceBets']).toBeFalsy();
    expect(component.placeJackpotBets).toHaveBeenCalled();
  });

  it('openHowToPlayDialog', () => {
    component.openHowToPlayDialog();

    expect(dialogService.openDialog).toHaveBeenCalledWith(
      dialogService.API.howToPlay,
      jasmine.any(Function),
      false,
      {
        dialogClass: 'new-dialog dialog-no-overlay jackpot-dialog'
      }
    );
  });

  it('addStake', () => {
    component.addStake(1);
    expect(jackpotSportTabService.addStake).toHaveBeenCalledWith(1);
  });

  it('addBet', () => {
    const event = <any>{};
    component.stakePerLineOptions = [1, 2];
    component.addBet('1', event);
    expect(jackpotSportTabService.addBet).toHaveBeenCalledWith('1', event);
  });

  describe('@removeAllBets', () => {
    it('removeAllBets', () => {
      component.stakePerLineOptions = [1, 2];
      component.initialData = <any>[{}];
      component.removeAllBets();
      expect(jackpotSportTabService.removeStake).toHaveBeenCalled();
      expect(jackpotSportTabService.removeAllBets).toHaveBeenCalled();
    });

    it('removeAllBets (confirmPromise)', () => {
      component.stakePerLineOptions = [1, 2];
      component.initialData = <any>[{}];
      component['confirmPromise'] = setTimeout(() => {});
      component.removeAllBets();
      expect(component['confirmPromise']).toEqual(jasmine.any(Number));
    });
  });

  describe('@confirmClear', () => {
    it('setCurrency', () => {
      component.setCurrency(1, true);
      expect(filtersService.setCurrency).toHaveBeenCalledWith('1.00', '£');
    });

    it('setCurrency', () => {
      component.setCurrency(1);
      expect(filtersService.setCurrency).toHaveBeenCalledWith(1, '£');
    });
  });

  it('setButtonText', () => {
    localeService.getString.and.returnValue('111');
    expect(component.setButtonText('text')).toEqual('111');
  });

  describe('@confirmClear', () => {
    it('confirmClear', () => {
      component.confirmClear();
      expect(component.confirm).toEqual(true);
    });

    it('confirmClear (confirmPromise)', fakeAsync(() => {
      component['confirmPromise'] = setTimeout(() => {});
      component.confirmClear();
      tick(5000);
      expect(component.confirm).toEqual(false);
    }));
  });


  describe('@makeLuckyDipClicked', () => {
    it('makeLuckyDipClicked', () => {
      const data = <any>[{
        unavailable: true
      }];
      jackpotSportTabService.betsArray = [];
      component.initialData = data;
      component.stakePerLineOptions = [1, 2];
      component.makeLuckyDipClicked();
      expect(jackpotSportTabService.makeLuckyDip).toHaveBeenCalledWith(data);
    });

    it('makeLuckyDipClicked (betsArray)', () => {
      const data = <any>[{}];
      jackpotSportTabService.betsArray = [{}];
      component.initialData = data;
      component.makeLuckyDipClicked();
      expect(dialogService.openDialog).toHaveBeenCalled();
    });
  });

  describe('@updateStakePerLineSelection', () => {
    it('updateStakePerLineSelection (0.5)', () => {
      component.totalLines = 2;
      component.stakePerLineOptions = [1, 2];
      component['updateStakePerLineSelection']();
      expect(component.stakePerLineOptions[0]).toEqual(0.5);
    });

    it('updateStakePerLineSelection (0.25)', () => {
      component.totalLines = 4;
      component.stakePerLineOptions = [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1];
      component['updateStakePerLineSelection']();
      expect(component.stakePerLineOptions[0]).toEqual(0.25);
    });

    it('updateStakePerLineSelection (shiftOption)', () => {
      component.stakePerLine = {
        value: 1
      };
      component.totalLines = 2;
      component.stakePerLineOptions = [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 1];
      component['updateStakePerLineSelection']();
      expect(jackpotSportTabService.addStake).toHaveBeenCalled();
    });

    it('updateStakePerLineSelection (shiftOption)', () => {
      component.stakePerLine = {
        value: 1
      };
      component.totalLines = 1;
      component.stakePerLineOptions = [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1];
      component['updateStakePerLineSelection']();
      expect(jackpotSportTabService.addStake).toHaveBeenCalled();
    });
  });

  it('openLuckyDipDialog', () => {
    component['openLuckyDipDialog']();

    expect(dialogService.openDialog).toHaveBeenCalledWith(
      dialogService.API.luckyDip,
      jasmine.any(Function),
      false,
      {
        makeLuckyDip: jasmine.any(Function),
        closeByEsc: false,
        closeByDocument: false
      }
    );
  });

  describe('@scrollToError', () => {
    it('scrollToError', () => {
      component.errorElm = <any>{
        nativeElement: {}
      };
      domToolsService.getOffset.and.returnValue({
        top: 1
      });
      component['scrollToError']();
      expect(domToolsService.getOffset).toHaveBeenCalledWith(component.errorElm.nativeElement);
    });

    it('scrollToError', () => {
      component['scrollToError']();
      expect(domToolsService.getOffset).not.toHaveBeenCalled();
    });
  });
});
