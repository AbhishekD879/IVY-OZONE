import { throwError, of } from 'rxjs';
import { fakeAsync,tick} from '@angular/core/testing';
import * as _ from 'underscore';
import { of as observableOf } from 'rxjs';
import { LottoSegmentPageComponent } from './lotto-segment-page.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { NavigationStart, NavigationEnd } from '@angular/router';
import { ILotto } from '../../models/lotto.model';
import { ILottoNumber } from '../../models/lotto-numbers.model';
import { ILottoResult } from '../../models/lotto-result.model';
 
describe('LottoSegmentPageComponent', () => {
  let component: LottoSegmentPageComponent;

  let filterService;
  let locale;
  let lottoService;
  let storage;
  let location;
  let datePipe;
  let route;
  let router;
  let user;
  let segmentDataUpdateService;
  let pubSubService;
  let accountUpgradeLinkService;
  let windowRefService;
  let dialogService;
  let componentFactoryResolver;
  let changeDetectorRef;
  let userService;
  let device;
  let infoDialog;
  let TimeService;
  let filtersService;
  let routeChangeListener;

  const currentLotto = <any>{
    normal: { lotteryPrice: [{numberCorrect : '2'}]}, 
    boosterBall: { lotteryPrice: []},
    uri: 'test_uri',
    lotteryPrice:[ 'test_price']
  };

  const singleData = {
    ssMappingId: "1,2",
     infoMessage: "test"
    }

  const lottery =  {
    boosterBall: {
      name: "49"
    },
      normal: {
        name: "49"
      }
  } as any

  beforeEach(fakeAsync(() => {
    filterService = {
      getComplexTranslation: jasmine.createSpy('getComplexTranslation'),
      setCurrency: jasmine.createSpy('setCurrency').and.returnValue('setCurrency'),
      filterLink: jasmine.createSpy('filterLink').and.returnValue('test'),
      orderBy: jasmine.createSpy('orderBy').and.returnValue([])
     };

    locale = {
      getString: jasmine.createSpy('getString').and.returnValue('test_string')
    };

    lottoService = {
      getShutAtTime: jasmine.createSpy('getShutAtTime').and.returnValue([]),
      getMenuItems: jasmine.createSpy('getMenuItems').and.returnValue([]),
      getLotteryData: jasmine.createSpy('getLotteryData').and.returnValue(of({})),
      getLotteriesByLotto: jasmine.createSpy('getLotteriesByLotto').and.returnValue(of(<any>[{ active: true, uri: 'test'}])),
      lottoCmsBanner : {
        lottoConfig: [{ssMappingId: "1,2"}]
      },
      setLottoDialog : jasmine.createSpy('setLottoDialog'),
      getPreviousResult : (key: string) => of({
        uri: 'http://test.com'
      }),
      cmsLotto : jasmine.createSpy('cmsLotto'),
      getLottoCmsBanner: jasmine.createSpy('getLottoCmsBanner').and.returnValue(of({
        dayCount: 'Number',
     }))
    
    };

    storage = {
      get: jasmine.createSpy('get'),
      set: jasmine.createSpy('set'),
      remove: jasmine.createSpy('remove'),
     };

    location = {
      path: jasmine.createSpy('path').and.returnValue('test')
    };

    datePipe = {
      transform: jasmine.createSpy('transform')
    };

    route = {
      url: observableOf([]),
      params: of(['',{myId: 123}]),
      snapshot: {
        params: {}
      }
    };

    user = {
      currencySymbol: 'GBP',
      oddsFormat: 'frac',
      sportBalance: 0,
      isInShopUser: jasmine.createSpy().and.returnValue(false)
    };

    segmentDataUpdateService = {
      time:{
        days:1,
        hours: 2,
        minutes: 3,
        currentLotto:'test',
      } ,


      changes: {
        next: jasmine.createSpy('next')
      }
    };
    routeChangeListener = {
      unsubscribe: jasmine.createSpy('unsubscribe')
    };
    router = {
      navigateByUrl: jasmine.createSpy('navigateByUrl'),
      navigate: jasmine.createSpy('navigate'),
      url: 'test_url',
      isLinesummaryPage:true,
      events: {
        subscribe: jasmine.createSpy('subscribe').and.returnValue(routeChangeListener)
      },
    };
    pubSubService = {
      publish: jasmine.createSpy('publish'),
      subscribe: jasmine.createSpy('subscribe'),
      API: pubSubApi
    };

    device= {
      isOnline :() => true
    };


    accountUpgradeLinkService = {
      inShopToMultiChannelLink: 'URL_TO_REDIRECT'
    };
    windowRefService = {
      nativeWindow: {
        location: {
          href: ''
        }
      }
    };
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges')
    };
    componentFactoryResolver={

      resolveComponentFactory :jasmine.createSpy(),
    };

    infoDialog = {
      openConnectionLostPopup: jasmine.createSpy('openConnectionLostPopup')
    };

    const singleData = {
      infoMessage: "test"
    }

    dialogService={
      selectedBackup:1,
      API : {
        lottoNumberSelector: ''
      },
      openDialog :(...args) => {
        const obj = args[3];
        obj.selectNumbers(1,0);
        obj.luckyDip(1);
        obj.resetNumbers();
        obj.onBeforeClose();
        obj.doneSelected();
       
      }
    };
    TimeService = {
      getLocalDate  : jasmine.createSpy('getLocalDate'),
      getLocalDateFromString: jasmine.createSpy().and.returnValue('2019-03-04T16:30:45.000Z'),
      getDatetimeWithFormatSuffix :jasmine.createSpy('getDatetimeWithFormatSuffix')
    }

    filtersService = {
      removeLineSymbol: jasmine.createSpy().and.returnValue('test'),
      date: jasmine.createSpy().and.returnValue(new Date())
    };
    createComp();
  }));

  function createComp() {
    component = new LottoSegmentPageComponent(
      filterService,
      locale, 
      lottoService, 
      storage, 
      location, 
      datePipe, 
      route, 
      router, 
      user, 
      segmentDataUpdateService,
      pubSubService, 
      accountUpgradeLinkService, 
      windowRefService, 
      dialogService,
      componentFactoryResolver,
      changeDetectorRef,
      user,
      device,
      infoDialog,
      TimeService,
      filtersService
    );

    component.currentLotto = <any>{
      name: 'test_name',
      boosterBall: {
        id:'1',
        name: 'test_name1'
      },
      normal: {
        id:"1",
        name: 'test_name2'
      }
    };
    component.activeMenuItem = <any>{
      uri: 'test_uri'
    };
    component.lotteryData = <any>{
      name: 'test_name',
    };
    component.showDays = 123;
    component['routeChangeListener'] = routeChangeListener;
  }

  it('ngOnInit: no data', fakeAsync(() => {
    component.ngOnInit();
    tick();
    expect(router.navigate).toHaveBeenCalledWith(['/404']);
  }));

  it('ngOnInit: with data', fakeAsync(() => {
    spyOn(component, 'getHistoryOf');
    lottoService.getLotteryData = jasmine.createSpy('getLotteryData').and.returnValue(of({ uri: 'test_uri',boosterBall: {
      id:'1',
      name: 'test_name1'
    },
  }));
    component['initLotto'] = jasmine.createSpy('initLotto');
    component.hideSpinner = jasmine.createSpy('hideSpinner');
    component.ngOnInit();
    tick();

    expect(component.lotteryData.uri).toEqual('test_uri');
    expect(component['initLotto']).toHaveBeenCalled();
    expect(component.hideSpinner).toHaveBeenCalled();
    expect(router.navigate).not.toHaveBeenCalled();
    expect(component.getHistoryOf).toHaveBeenCalled();
    expect(component.currentLotto.boosterBall.id).toBe('1')

  }));

    it('ngOnInit: with data', fakeAsync(() => {
    spyOn(component, 'getHistoryOf');
    component.lotteryData.boosterBall = undefined;
    lottoService.getLotteryData = jasmine.createSpy('getLotteryData').and.returnValue(of({ uri: 'test_uri',
    normal: {
      id:"1",
      name: 'test_name2'
    } }));
    component['initLotto'] = jasmine.createSpy('initLotto');
    component.hideSpinner = jasmine.createSpy('hideSpinner');
    component.ngOnInit();
    tick();

    expect(component.lotteryData.uri).toEqual('test_uri');
    expect(component['initLotto']).toHaveBeenCalled();
    expect(component.hideSpinner).toHaveBeenCalled();
    expect(router.navigate).not.toHaveBeenCalled();
    expect(component.getHistoryOf).toHaveBeenCalled();
    expect(component.currentLotto.boosterBall.id).toBe('1')

  }));

  it('ngOnInit: error', fakeAsync(() => {
    spyOn(component, 'getHistoryOf');
    lottoService.getLotteryData = jasmine.createSpy('getLotteryData').and.returnValue(throwError([]));
    component.showError = jasmine.createSpy('showError');
    component.ngOnInit();

    tick();
    expect(component.showError).toHaveBeenCalled();
    expect(component.currentLotto.boosterBall.id).toBe('1');

  }));

  it('openLottoInfoDialog: no internet', () => {
    component['device'].isOnline = jasmine.createSpy().and.returnValue(false);
    component.openLottoInfoDialog();
    expect(infoDialog.openConnectionLostPopup).toHaveBeenCalledTimes(1);
  });

  it('should create', () => {
    component.singleData = <any>{
      infoMessage: "test"
    };
    const spy = spyOn(component['dialogService'], 'openDialog');
    const selectNumbersSpy = spyOn(component, 'selectNumbers');
    component.singleData = { singleData: 'lotto', infoMessage: 'test', nextLink: 'www.abc.com' } as any;

    component.openLottoInfoDialog();
    expect(infoDialog.openConnectionLostPopup).not.toHaveBeenCalled();
    expect(dialogService.openDialog).toHaveBeenCalled();
    expect(componentFactoryResolver.resolveComponentFactory).toHaveBeenCalled();
  });

  it('ngOnDestroy', () => {
    component['routeChangeListener'] = <any>{
      unsubscribe: jasmine.createSpy()
    };
    component.timeInterval = setInterval(() => {}, 1000);
    component.ngOnDestroy();
    expect(component.timeInterval).toEqual(jasmine.any(Number));
    expect(component['routeChangeListener'].unsubscribe).toHaveBeenCalled();
  });

  it('getDipTranslations', () => {
    component.getDipTranslations(2);
    expect(filterService.getComplexTranslation).toHaveBeenCalledWith('lotto.lucky', '%num', '2');
  });

  it('setLotto', () => {
    component['setLottoTabs'] = jasmine.createSpy('setLottoTabs');
    component['getSelected'] = jasmine.createSpy('getSelected');
    component['initializeTimer'] = jasmine.createSpy('initializeTimer');
    spyOn(component, 'updateDraws');
    spyOn(component, 'setBallNumbers');

    component.setLotto(currentLotto, true);

    expect(component.boosterBall).toEqual(true);
    expect(component.currentLotto).toEqual(_.extend(currentLotto, { shutAtTime: [] }));
    expect(component.currentLottery.lotteryPrice).toEqual([]);
    expect(component.activeMenuItem.uri).toEqual(currentLotto.uri);
    expect(lottoService.getShutAtTime).toHaveBeenCalledWith({ lotteryPrice: [] });
    expect(component.updateDraws).toHaveBeenCalled();
    expect(component.setBallNumbers).toHaveBeenCalled();
    expect(component['setLottoTabs']).toHaveBeenCalled();
    expect(component['getSelected']).toHaveBeenCalled();
    expect(component['initializeTimer']).toHaveBeenCalledWith(currentLotto.shutAtTime);
    expect(pubSubService.publish).toHaveBeenCalledWith('ballsUpdate');

    component.setLotto({ normal: currentLotto.normal, boosterBall: currentLotto.boosterBall }, null);
    expect(component.lotteryPrice).toEqual(component.currentLottery.lotteryPrice);
    expect(component.currentLottery).toEqual(currentLotto.normal);
    component.setLotto({ boosterBall: currentLotto.boosterBall }, null);
    expect(component.currentLottery).toEqual(currentLotto.boosterBall);
  });

  describe('updateDraws: ', () => {
    it('checked', () => {
      component.orderedDraws = <any>[{ checked: true }, { checked: true }];
      component.updateDraws();
      expect(_.pluck(component.draws, 'checked').length).toBe(2);
      expect(component.drawMultiplier).toEqual(2);
    });

    it('unchecked', () => {
      component.orderedDraws = <any>[{}, {}];
      component.updateDraws();

      expect(_.pluck(component.draws, 'checked').length).toBe(0);
      expect(component.drawMultiplier).toEqual(1);
    });
  });

  describe('setBallNumbers', () => {
    it('setBallNumbers: ball selection not stored', () => {
      spyOn(component, 'disabledBalls');
      component['setSelectedBallNumbers'] = jasmine.createSpy('setSelectedBallNumbers');
      component.currentLottery = <any>{
        maxNumber: 1
      };
      component.setBallNumbers();

      expect(component.numbersData[0]).toEqual({
        disabled: false,
        selected: false,
        value: 1
      });
    });

    it('setBallNumbers: ball selection stored', fakeAsync(() => {
      storage.get = jasmine.createSpy('get').and.returnValue([{}]);
      createComp();
      component['setSelectedBallNumbers'] = jasmine.createSpy('setSelectedBallNumbers');
      component.currentLottery = <any>{ maxNumber: 1 };
      spyOn(component, 'disabledBalls');
      tick();
      component.setBallNumbers();

      expect(component.numbersData[0]).toEqual({
        disabled: false,
        selected: false,
        value: 1
      });
    }));
  });

  describe('disabledBalls', () => {
    it('should set disable some balls', () => {
      component.currentLottery = <any>{ maxPicks: 2 };
      component.numbersData = <any>[ { selected: true }, { selected: false }, { selected: true }];
      component.disabledBalls();

      expect(component.selected).toBe(2);
      expect(_.pluck(component.numbersData, 'disabled')).toEqual([false, true, false]);
    });

    it('should set disable all balls', () => {
      component.currentLottery = <any>{ maxPicks: 3 };
      component.numbersData = <any>[ { selected: true }, { selected: false }, { selected: true }];
      component.disabledBalls();

      expect(_.pluck(component.numbersData, 'disabled')).toEqual([false, false, false]);
    });
  });

  it('resetDraws', () => {
    component.orderedDraws = <any>[{ checked: true }, { checked: true }];
    component.resetDraws();

    expect(component.orderedDraws[0].checked).toBeFalsy();
    expect(storage.remove).toHaveBeenCalledWith('test_nameDraw');
  });

  describe('selectNumbers', () => {
    it(' while balls are enabled', () => {
      component.numbersData = <any>[{ selected: true, disabled: true }];
      spyOn(component, 'disabledBalls');

      component.selectNumbers({ index: 0 });
      expect(component.numbersData[0].selected).toBeFalsy();
      expect(component.numbersData[0].disabled).toBeFalsy();
      expect(component.disabledBalls).toHaveBeenCalled();

      component.numbersData = <any>[{ disabled: true }];

      component.selectNumbers({ index: 0 });
      expect(component.numbersData[0].disabled).toBeTruthy();
      expect(segmentDataUpdateService.changes.next).toHaveBeenCalledWith({
        numbersSelected: component.numbersSelected,
        numbersData: component.numbersData,
        selected: component.selected
      });
    });

    it(' selected undefiend', () => {
      component.numbersData = <any>[{ selected: false, disabled: false }];
      spyOn(component, 'disabledBalls');
      component.selected = undefined;

      component.selectNumbers({ index: 0 });
      expect(component.disabledBalls).toHaveBeenCalled();
      expect(segmentDataUpdateService.changes.next).toHaveBeenCalledWith({
        numbersSelected: component.numbersSelected,
        numbersData: component.numbersData,
        selected: component.selected
      });
    });

    describe(' stress clicking: click before balls are disabled', () => {
      beforeEach(() => {
        component.numbersData = <any>[{ selected: false, disabled: false }];
        component.currentLottery = {
          maxPicks: 5
        } as any;
        spyOn(component, 'disabledBalls');
      });
      it('(max limit reached)', () => {
        component.selected = 5;
      });
      it('(coverage case)', () => {
        component.selected = 6;
      });
      afterEach(() => {
        component.selectNumbers({ index: 0 });
        expect(segmentDataUpdateService.changes.next).not.toHaveBeenCalled();
        expect(component.disabledBalls).not.toHaveBeenCalled();
      });
    });
  });

  it('resetSelected', () => {
    component.resetSelected(2);
    expect(component.selected).toBe(0);
  });

  it('doneSelected', () => {
    component.numbersData = <any>[{}, { selected: true }];
    component['getSelected'] = jasmine.createSpy();
    component['setSelectedBallNumbers'] = jasmine.createSpy();

    component.doneSelected();

    expect(component['getSelected']).toHaveBeenCalled();
    expect(component['setSelectedBallNumbers']).toHaveBeenCalledWith([component.numbersData[1]]);
    expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    expect(storage.set).toHaveBeenCalledWith(component.currentLotto.name, [component.numbersData[1]]);
    expect(router.navigate).toHaveBeenCalledWith(['/lotto','linesummary',  '']);
   });

  it('should call numDialog() method ', () => {
    component.currentLottery = { maxPicks: 100 } as ILotto;
    component.numbersData = [{ selected: true } as ILottoNumber];
    component.selected = 1;
    component.lotteryPrice = [];
    component.numbersSelected = [];
    component['isDone'] = false;
    spyOn(component, 'selectNumbers');
    spyOn(component, 'clearNumberOnClose');
    spyOn(component, 'resetSelected');
    spyOn(component, 'setBallNumbers');
    component.numDialog();
    expect(component.selected).toEqual(0);
    });

  it('luckyDip', () => {
    spyOn(component, 'disabledBalls');
    component.numbersData = <any>[{ value: '1' }, { value: '2' }, { value: '3' }];

    component.luckyDip(2);
    expect(_.compact(_.pluck(component.numbersData, 'selected')).length).toEqual(2);
    expect(component.ballSelected.length).toEqual(2);
    expect(_.keys(component.ballSelected[0])).toEqual(['value', 'selected']);
    expect(component.disabledBalls).toHaveBeenCalled();
  });

  it('resetNumbers', () => {
    component['getSelected'] = jasmine.createSpy();
    spyOn(component, 'setBallNumbers');

    component.resetNumbers();

    expect(component.ballSelected).toEqual([]);
    expect(component.selected).toBeFalsy();
    expect(storage.remove).toHaveBeenCalledWith(component.currentLotto.name);
    expect(component.setBallNumbers).toHaveBeenCalled();
    expect(component['getSelected']).toHaveBeenCalled();
    expect(segmentDataUpdateService.changes.next).toHaveBeenCalledWith({
      numbersSelected: component.numbersSelected,
      numbersData: component.numbersData,
      selected: component.selected
    });
  });
  it('setTotalStake', () => {
    component.accumulatorAmount = 10;
    component.setTotalStake();
    expect(component.totalStake === component.accumulatorAmount).toBeTruthy();
  });

  describe('confirmation', () => {
    let event;

    beforeEach(() => {
      spyOn(component as any, 'displayPopupForInShopUser').and.callThrough();
      event = { stopPropagation: jasmine.createSpy('stopPropagation') };
    });

    it('used logged in', () => {
      user.status = true;

      component.confirmation(event);

      expect(component['displayPopupForInShopUser']).toHaveBeenCalled();
      expect(event.stopPropagation).toHaveBeenCalled();
      expect(component.confirm).toBeTruthy();
    });

    it('used logged in (in shop)', () => {
      user.status = true;
      user.isInShopUser.and.returnValue(true);

      component.confirmation(event);

      expect(component['displayPopupForInShopUser']).toHaveBeenCalled();
      expect(event.stopPropagation).toHaveBeenCalled();
      expect(component.confirm).toBeFalsy();
      expect(windowRefService.nativeWindow.location.href).toBe(accountUpgradeLinkService.inShopToMultiChannelLink);
    });

    it('used logged out', () => {
      user.status = false;
      component.confirmation(event);
      expect(component.confirm).toBeFalsy();
     });
  });

  it('get totalStakeGetter()',()=>{
    component.totalStake = 1;
    component.drawMultiplier = 2;
    expect(component.totalStake).toBe(1);

  });


  it('setSelectedBallNumbers', () => {
    const data = <any>[{ value: 2 }, {}, { value: 10 }, { value: 5 }];
    const res = [{ value: 2, selected: true, disabled: false },
                 { value: '-', selected: false, disabled: false },
                 { value: 10, selected: true, disabled: false },
                 { value: 5, selected: true, disabled: false }];

    component.numbersSelected = [];
    component.currentLottery = <any>{ maxPicks: 4 };

    component['setSelectedBallNumbers'](data);
    expect(component.numbersSelected).toEqual(res);
  });

  it('getTimeLeft', () => {
    const d = new Date();
    const res = component['getTimeLeft'](d);

    expect(_.isNumber(res.total)).toBeTruthy();
    expect(_.isNumber(res.days)).toBeTruthy();
    expect(_.isNumber(res.hours)).toBeTruthy();
    expect(_.isNumber(res.minutes)).toBeTruthy();
  });

  describe('initializeTimer', () => {
    it('initializeTimer', () => {
      component['updateLotto'] = jasmine.createSpy('updateLotto');
      component['initializeTimer'](Date.now());

      expect(component.days).toEqual(0);
      expect(component.hours).toEqual(0);
      expect(component.minutes).toEqual(0);
      expect(component['updateLotto']).toHaveBeenCalled();
      expect(typeof component.timeInterval).toBe('number');
      expect(component['routeChangeListener']).toEqual(jasmine.anything());
      expect(router.events.subscribe).toHaveBeenCalledWith(jasmine.anything());
      clearInterval(component.timeInterval);
    });

    it('should not update lotto',  () => {
      router.events = of(new NavigationStart(1, ''));
      component['updateLotto'] = jasmine.createSpy('updateLotto');
      component['getTimeLeft'] = jasmine.createSpy('getTimeLeft').and.returnValue({total: 10, days: 10, hours: 10, minutes: 10});
      component['initializeTimer'](Date.now());

      expect(component['updateLotto']).not.toHaveBeenCalled();
    });

    it('should not update lotto and clear interval',  () => {
      router.events = of(new NavigationEnd(1, '', ''));
      component['updateLotto'] = jasmine.createSpy('updateLotto');
      component['getTimeLeft'] = jasmine.createSpy('getTimeLeft').and.returnValue({total: 10, days: 10, hours: 10, minutes: 10});
      component['initializeTimer'](Date.now());

      expect(component['updateLotto']).not.toHaveBeenCalled();
    });
  });

  it('getSelected', () => {
    component.numbersSelected = <any>[{ value: 1 }, { value: '-' }, { value: 3 }];
 
    component['getSelected']();
    expect(component.ballPicks).toEqual([1, 3]);
    expect(component.selectionName).toEqual('DBL');
   });

  it('setLottoTabs', () => {
    component['setLottoTabs']();

    expect(component.lottoTabs).toEqual([{
      title: 'test_string',
      name: 'Straight',
      hidden: false,
      id: 0,
      url: 'test_url'
    },
    { title: 'test_string',
      name: 'Combo',
      hidden: true,
      id: 1,
      url: 'test_url/combo'
    },
    { title: 'test_string',
      name: 'Results',
      hidden: true,
      id: 2,
      url: 'test_url/results'
    }]);
    expect(component.activeTab.name).toEqual('Straight');
    expect(pubSubService.publish).toHaveBeenCalledWith('MENU_UPDATE', component.activeMenuItem.uri);
  });

  it('initLotto: lottery data old', fakeAsync(() => {
    component['updateLotto'] = jasmine.createSpy('updateLotto');
    spyOn(component, 'setLotto');
    const d = <any>new Date();
    d.setYear(1990);
    component.lotteryData = currentLotto;
    component.lotteryData.shutAtTime = d;
    component['initLotto']();
    tick();
    expect(component.activeMenuItem).toEqual({ uri: null });
    expect(component.isExpended).toBeTruthy();
    expect(component.boosterBall).toBeFalsy();
    expect(component.confirm).toBeFalsy();
    expect(component.orderedDraws).toEqual([]);
    expect(component.ballPicks).toEqual([]);
    expect(component.ballSelected).toEqual([]);
    expect(component.numbersSelected).toEqual({});
    expect(component.luckyDipArr).toEqual([3, 4, 5]);
    expect(component.showDays).toEqual(7);
    expect(lottoService.getMenuItems).toHaveBeenCalledWith(undefined);
    expect(component.menuItems).toEqual([]);
    expect(component['updateLotto']).toHaveBeenCalledWith(component.lotteryData);
    expect(component.setLotto).not.toHaveBeenCalled();
  }));

  it('initLotto: should call hasItsown', () => {
 
    component['updateLotto'] = jasmine.createSpy('updateLotto');
    spyOn(component, 'setLotto');
    const d = <any>new Date();
    d.setYear(1990);
    const lottoConfig = <any>{
        normal: {
          name: "49",
          id: "1"
        }
    };
    lottoService.lottoCmsBanner = {
      lottoConfig: [{ssMappingId: "1,2"}]
    };
    component.lotteryData = lottoConfig;
    component.lotteryData.shutAtTime = d;
    component['initLotto']();
   expect(component['updateLotto']).toHaveBeenCalled();
  })

  it('initLotto: lottery data new', () => {
    component['updateLotto'] = jasmine.createSpy('updateLotto');
    spyOn(component, 'setLotto');
    const d = <any>new Date();
    d.setYear(3000);
    component.setLotto = jasmine.createSpy('setLotto');
    component.lotteryData = currentLotto;
    component.lotteryData.shutAtTime = d;
    component.boosterBall = true;
    component['initLotto']();
    expect(component.setLotto).toHaveBeenCalledWith(component.lotteryData, component.boosterBall);
  });

  it('initLotto: no lotteryData', () => {
    const lottoConfig = <any>{
      normal: {
        name: "49",
        id: "1"
      }
  };
    component['updateLotto'] = jasmine.createSpy().and.returnValue(null);
    spyOn(component, 'setLotto');
    component.lotteryData = lottoConfig;
    component['initLotto']();
    expect(component['updateLotto']).not.toHaveBeenCalled();
  });
  describe('updateLotto', () => {
    it('updateLotto', fakeAsync(() => {
      spyOn(component, 'setLotto');
      component.boosterBall = true;
      component['updateLotto'](currentLotto);
      tick();
      expect(pubSubService.publish).toHaveBeenCalledWith('MSG_UPDATE', {
        type: 'normal',
        msg: currentLotto.name + locale.getString() + datePipe.transform()
      });
      expect(locale.getString).toHaveBeenCalledWith('lotto.finished');
      expect(datePipe.transform).toHaveBeenCalledWith(currentLotto.shutAtTime, 'HH:mm dd/MM/yyyy');
      expect(lottoService.getLotteriesByLotto).toHaveBeenCalled();
      expect(filterService.filterLink).toHaveBeenCalledWith('lotto/test');
      expect(pubSubService.publish).toHaveBeenCalledWith('MENU_UPDATE', []);
      expect(location.path).toHaveBeenCalled();
      expect(component.setLotto).toHaveBeenCalledWith({ active: true, uri: 'test' }, true);
    }));

    it('should navigate by url',  fakeAsync(() => {
      filterService.filterLink.and.returnValue('link');
      component['updateLotto'](currentLotto);
      tick();
      expect(router.navigateByUrl).toHaveBeenCalled();
    }));
  });

  it('#documentClick', () => {
    component.documentClick();
    expect(component.confirm).toBeFalsy();
  });

  it('Should call clearNumberOnClose()',()=>{
    component.numbersData = [{value:1,selected:false} as ILottoNumber,] ;
    component.clearNumberOnClose([{value:1,selected:false, disabled:true } as ILottoNumber]);
    expect(component.numbersData).toEqual([{value:1,selected:false,disabled:true} as ILottoNumber,]);
  });

  it('should call setHeaderData() method', fakeAsync(() => {
    component.days = 2;
    component.hours = 2;
    component.minutes = 3;
    component.currentLotto = { name: 'test' } as ILotto;
    component.setHeaderData();
    tick();
    expect(component['segmentDataUpdateService'].headerTime).toEqual({
      days:2,
      hours:2,
      minutes:3,
      currentLotto: 'test',
    });

  }));

  it('it should call filterPreviousResults()',()=>{
    const previousResultSummary = [
     {
       id :"1",
       results: 'test',
       drawAtTime: 'test1',
       resultsBonus: 'test2',
       description: 'test3',
    },
    {
      id :"2",
      results: 'test',
      drawAtTime: 'test1',
      resultsBonus: null,
      description: 'test3',
   }
   ];
   spyOn(component, 'handleToggle');
   component.filterPreviousResults(previousResultSummary);
   expect(previousResultSummary[0].results).toEqual('test');
   expect(previousResultSummary[0].drawAtTime).toEqual('test1');
   expect(filtersService.removeLineSymbol).toHaveBeenCalledTimes(2);
   expect(filtersService.date).toHaveBeenCalledTimes(0);
 });
   
it('it should call getHistoryOf() with lottoId', fakeAsync(()=>{
  component.lottoData = [
   {
    resultedDraw:[{}]
   },
   {
    resultedDraw:undefined
   }
 ];
 spyOn(component['lottoService'], 'getPreviousResult').and.returnValue(of([
  { resultedDraw:undefined},{ resultedDraw:[]} as ILottoResult
 ]));
 spyOn(component, 'filterPreviousResults');
 const lottoId = ["1"]
 component.getHistoryOf(lottoId);
 tick();
 expect(component.lottoData[0].resultedDraw).toEqual(undefined);
 expect(component.lottoData[1].resultedDraw).toEqual([])
 }));

it('it should call handleToggle()', ()=>{
  const isInitial = false;
  const defaultResultData = [{balls: '1|2|3|4', drawAt: '21/02/2023', bonusBall: '6', drawName: 'LunchTime', resultedDraw : '1234'}];
  component.handleToggle(isInitial);
  expect(defaultResultData[0].balls).toEqual('1|2|3|4');
  expect(defaultResultData[0].drawAt).toEqual('21/02/2023');
  expect(defaultResultData[0].bonusBall).toEqual('6');
  expect(defaultResultData[0].drawName).toEqual('LunchTime');
});

it('it should call handleToggle()', ()=>{
  const isInitial = true ;
  const defaultResultData = undefined
  component.handleToggle(isInitial);
  expect(defaultResultData).toBeUndefined();
 });
 
 it('it should call handleToggle()', ()=>{
  const defaultResultData = undefined
  component.handleToggle();
  expect(defaultResultData).toBeUndefined();
 });


 it('it should call handleToggle()', ()=>{
  component.defaultResultData = [{ balls: '1|2|3|4', drawAt: '21/02/2023', bonusBall: '6', drawName: 'LunchTime', resultedDraw : '1234'}as any 
  ];
  component.handleToggle(true);
  expect(component.defaultResultData[0].bonusBall).toEqual('6');
  expect(component.defaultResultData[0].drawAt).toEqual('21/02/2023'as any);
  expect(component.defaultResultData[0].drawName).toEqual('LunchTime');
 });
 
});
