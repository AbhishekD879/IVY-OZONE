import { of as observableOf } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';
import * as _ from 'underscore';

import { WBetslipComponent } from './w-betslip.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('WBetslipComponent', () => {
  let component: WBetslipComponent;

  let pubSubService;
  let localeService;
  let deviceService;
  let betslipTabsService;
  let subscribeEvents;
  let userService;
  let windowRef;

  beforeEach(() => {
    subscribeEvents = {
      'LOAD_CASHOUT_BETS': null,
      'LOAD_UNSETTLED_BETS': null,
      'LOAD_BET_HISTORY': null,
      'EMA_UNSAVED_IN_WIDGET': null
    };
    pubSubService = {
      API: pubSubApi,
      publish: jasmine.createSpy('publish'),
      subscribe: jasmine.createSpy('publish').and.callFake((subscriber, method, cb) => {
        if (typeof method === 'string' && ['LOAD_CASHOUT_BETS', 'LOAD_UNSETTLED_BETS', 'LOAD_BET_HISTORY', 'UPDATE_SETTLED_BETS_HEIGHT',
          'EMA_UNSAVED_IN_WIDGET', 'UPDATE_ITEM_HEIGHT'].includes(method)) {
          subscribeEvents[method] = cb;
        }
      }),
      unsubscribe: jasmine.createSpy('unsubscribe')
    };
    localeService = {
      getString: jasmine.createSpy('getString').and.returnValue('betslip')
    };
    deviceService = {
      isMobileOrigin: true,
      isMobile: true,
      isDesktop: false
    };
    betslipTabsService = {
      createTab: jasmine.createSpy('betslipTabsService'),
      getTabsList: jasmine.createSpy('getTabsList')
    };
    userService = {
      status: false
    };

    windowRef = {
      document: {
          querySelector: { get: jasmine.createSpy() },
          querySelectorAll: { get: jasmine.createSpy() }
      }
    }

    component = new WBetslipComponent(
      pubSubService,
      localeService,
      deviceService,
      betslipTabsService,
      windowRef,
      userService
    );

    component['betHistoryPageRef'] = {
      destroy: jasmine.createSpy('destroy')
    } as any;
    component['cashOutPageRef'] = {
      destroy: jasmine.createSpy('destroy')
    } as any;
    component['openBetsRef'] = {
      destroy: jasmine.createSpy('destroy')
    } as any;
    component['inShopBetsPageRef'] = {
      destroy: jasmine.createSpy('destroy')
    } as any;

    component['betslipContainerView'] = {
      parentInjector: null
    } as any;

    component.sessionStateDefined = false;
    component.isBetCountMatch = false;
    component.activeTab = { id: 0, name: '', title: '', url: '' };
  });

  it('constructor', () => {
    expect(component.mobile).toBeTruthy();
    expect(_.keys(component['tabsMap'])).toEqual(['cashout', 'openbets', 'bethistory']);
    expect(localeService.getString).toHaveBeenCalledTimes(3);
  });

  it('ngOnInit', fakeAsync(() => {
    component['openBetslip'] = jasmine.createSpy();
    component['selectMyBetsTab'] = jasmine.createSpy();
    component.title = 'title';
    betslipTabsService.createTab = jasmine.createSpy().and.callFake((tabName, id) => {
      return {
        title: tabName,
        name: tabName,
        url: '',
        id
      };
    });
    betslipTabsService.getTabsList.and.returnValue(observableOf([{ id: 0, name: 'Cashout' }, { id: 2, name: 'Open Bets' }]));
    pubSubService.subscribe = jasmine.createSpy('publish').and.callFake((subscriber, method, cb) => cb());
    windowRef.document.querySelector = jasmine.createSpy().and.returnValue({});
    windowRef.document.querySelectorAll = jasmine.createSpy().and.returnValue([{clientHeight: 10}]);
    component.ngOnInit();
    component.displayBets();

    tick(100);
    expect(betslipTabsService.getTabsList).toHaveBeenCalled();
    expect(component.betslipTabs.length).toEqual(2);
    expect(component.errorMsg).toEqual('betslip');
    expect(pubSubService.subscribe).toHaveBeenCalledTimes(8);
    expect(pubSubService.subscribe).toHaveBeenCalledWith(
      component.title,
      jasmine.arrayContaining([pubSubService.API.SESSION_LOGOUT, pubSubService.API.HOME_BETSLIP]),
      jasmine.any(Function)
    );
    expect(pubSubService.subscribe).toHaveBeenCalledWith(component.title, 'LOAD_CASHOUT_BETS', jasmine.any(Function));
    expect(pubSubService.subscribe).toHaveBeenCalledWith(component.title, 'LOAD_UNSETTLED_BETS', jasmine.any(Function));
    expect(pubSubService.subscribe).toHaveBeenCalledWith(component.title, 'LOAD_BET_HISTORY', jasmine.any(Function));
    expect(pubSubService.subscribe).toHaveBeenCalledWith(component.title, 'EMA_UNSAVED_IN_WIDGET', jasmine.any(Function));
    expect(pubSubService.subscribe).toHaveBeenCalledWith(component.title, 'UPDATE_SETTLED_BETS_HEIGHT', jasmine.any(Function));
    expect(component['openBetslip']).toHaveBeenCalledTimes(2);
    expect(betslipTabsService.createTab).toHaveBeenCalledWith('cashout', 1);
    expect(betslipTabsService.createTab).toHaveBeenCalledWith('openbets', 2);
    expect(betslipTabsService.createTab).toHaveBeenCalledWith('betHistory', 3);
    expect(component['selectMyBetsTab']).toHaveBeenCalledWith(jasmine.objectContaining({
      title: 'cashout',
      name: 'cashout',
      url: '',
      id: 1
    }));
    expect(component['selectMyBetsTab']).toHaveBeenCalledWith(jasmine.objectContaining({
      title: 'openbets',
      name: 'openbets',
      url: '',
      id: 2
    }));
    expect(component['selectMyBetsTab']).toHaveBeenCalledWith(jasmine.objectContaining({
      title: 'betHistory',
      name: 'betHistory',
      url: '',
      id: 3
    }));
  }));

  it('ngOnInit: should not show error when user is logged in', fakeAsync(() => {
    userService.status = true;
    betslipTabsService.getTabsList.and.returnValue(observableOf([{ id: 0, name: 'Cashout' }, { id: 2, name: 'Open Bets' }]));
    component.ngOnInit();

    tick(100);
    expect(betslipTabsService.getTabsList).toHaveBeenCalled();
    expect(component.errorMsg).toEqual('');
  }));

  it('ngOnInit: should call updateBetSlipHeight ', () => {
    userService.status = true;
    betslipTabsService.getTabsList.and.returnValue(observableOf([{ id: 0, name: 'Cashout' }, { id: 2, name: 'Open Bets' }]));
    deviceService.isDesktop = true;
    component.isHeightUpdated = true;
    const betTypesNodeElement = {clientHeight: 10, scrollTop: 0};
    const myBetNodeElement = [betTypesNodeElement];
    windowRef.document.querySelectorAll = jasmine.createSpy().and.returnValue(myBetNodeElement);
    windowRef.document.querySelector = jasmine.createSpy().and.returnValue(betTypesNodeElement);
    component['handleHeightUpdate'] = jasmine.createSpy().and.callThrough();
    component.ngOnInit();
    component.displayBets();
    expect(component['handleHeightUpdate']).toHaveBeenCalled();
    expect(component['bsHeight']).toEqual('100%');
  });

  describe('ngAfterViewChecked', () => {

    it('should not call updateBetSlipHeight', () => {
      component.isHeightUpdated = false;
      component['handleHeightUpdate'] = jasmine.createSpy().and.callThrough();
      component.displayBets();
      expect(component['handleHeightUpdate']).not.toHaveBeenCalled();
    });

    it('should call updateBetSlipHeight from ngAfterViewChecked', ()=> {
      const betTypesNodeElement = {clientHeight: 10, scrollTop: 0};
      const myBetNodeElement = [betTypesNodeElement];
      deviceService.isDesktop = true;
      windowRef.document.querySelectorAll = jasmine.createSpy().and.returnValue(myBetNodeElement);
      windowRef.document.querySelector = jasmine.createSpy().and.returnValue(betTypesNodeElement);
      component.isHeightUpdated = true;
      component['handleHeightUpdate'] = jasmine.createSpy().and.callThrough();
      component.displayBets();
      expect(component['handleHeightUpdate']).toHaveBeenCalled();
    });

    it('should call updateBetSlipHeight with betcount <= 4', ()=> {
      component.betCount = 4;
      const betTypesNodeElement = {clientHeight:10, scrollTop: 0} as Element;
      deviceService.isDesktop = true;
      windowRef.document.querySelectorAll = jasmine.createSpy().and.returnValue(betTypesNodeElement);
      windowRef.document.querySelector = jasmine.createSpy().and.returnValue(betTypesNodeElement);
      component.isHeightUpdated = true;
      component.displayBets();
      component['handleHeightUpdate'](betTypesNodeElement, betTypesNodeElement);
      expect(component['bsHeight']).toEqual('100%');
    });

    it('should call updateBetSlipHeight and display scroll bar when betcount > 4', ()=> {
      component.betCount = 25;
      const betTypesNodeElement = {clientHeight:10, scrollTop: 0} as Element;
      const myBetNodeElement = [{clientHeight:100},{clientHeight:100},{clientHeight:100},{clientHeight:100},{clientHeight:100}] as Element[];
      deviceService.isDesktop = true;
      windowRef.document.querySelectorAll = jasmine.createSpy().and.returnValue(myBetNodeElement);
      windowRef.document.querySelector = jasmine.createSpy().and.returnValue(betTypesNodeElement);
      component.isHeightUpdated = true;
      component.displayBets();
      component['handleHeightUpdate'](myBetNodeElement[0], betTypesNodeElement, false);
      expect(component['bsHeight']).not.toEqual('100%');
    });

    it('should call updateBetSlipHeight and display scroll bar when betcount > 4', ()=> {
      component.betCount = 5;
      const betTypesNodeElement = {clientHeight:10, scrollTop: 0} as Element;
      const myBetNodeElement = [{clientHeight:100},{clientHeight:100},{clientHeight:100},{clientHeight:100},{clientHeight:100}] as Element[];
      deviceService.isDesktop = true;
      windowRef.document.querySelectorAll = jasmine.createSpy().and.returnValue(myBetNodeElement);
      windowRef.document.querySelector = jasmine.createSpy().and.returnValue(betTypesNodeElement);
      component.isHeightUpdated = true;
      component.displayBets();
      component['handleHeightUpdate'](myBetNodeElement[0], betTypesNodeElement, false);
      component.isHeightUpdated = false;
      expect(component['bsHeight']).not.toEqual('100%');
    });

    it('should call updateBetSlipHeight and display scroll bar when betcount > 4 and length of bet is null', ()=> {
      component.betCount = 5;
      const betTypesNodeElement = null;
      const myBetNodeElement = [{clientHeight:100},{clientHeight:100},{clientHeight:100},{clientHeight:100},{clientHeight:100}] as Element[];
      deviceService.isDesktop = true;
      windowRef.document.querySelectorAll = jasmine.createSpy('Element').and.returnValue(myBetNodeElement);
      windowRef.document.querySelector = jasmine.createSpy('Element').and.returnValue(betTypesNodeElement);
      component.isHeightUpdated = true;
      component.displayBets();
      component['handleHeightUpdate'](myBetNodeElement[0], betTypesNodeElement, false);
      component.isHeightUpdated = false;
      expect(component['bsHeight']).not.toEqual('100%');
    });

    it('should call updateBetSlipHeight and display scroll bar when betcount > 4 and length of bet is undefined', ()=> {
      component.betCount = 5;
      const betTypesNodeElement = undefined;
      const myBetNodeElement = [{clientHeight:100},{clientHeight:100},{clientHeight:100},{clientHeight:100},{clientHeight:100}] as Element[];
      deviceService.isDesktop = true;
      windowRef.document.querySelectorAll = jasmine.createSpy().and.returnValue(myBetNodeElement);
      windowRef.document.querySelector = jasmine.createSpy().and.returnValue(betTypesNodeElement);
      component.isHeightUpdated = true;
      component.displayBets();
      component['handleHeightUpdate'](myBetNodeElement[0], betTypesNodeElement, false);
      component.isHeightUpdated = false;
      expect(component['bsHeight']).not.toEqual('100%');
    });

    it('should call updateBetSlipHeight and display scroll bar when betcount > 4 and length of parent conatiner is zero', fakeAsync(()=> {
      component.betCount = 5;
      const betTypesNodeElement = {clientHeight: 10, scrollTop: 0} as Element;
      const myBetNodeElement = [{}] as any;
      deviceService.isDesktop = true;
      component.isBetCountMatch = false
      windowRef.document.querySelectorAll = jasmine.createSpy().and.returnValue(myBetNodeElement);
      windowRef.document.querySelector = jasmine.createSpy().and.returnValue(betTypesNodeElement);
      component.displayBets();
      component['handleHeightUpdate']({scrollHeight: 10} as Element, betTypesNodeElement, false);
      expect(component['bsHeight']).not.toEqual('100%');
    }));

  });


  describe('handleTabClick', () => {
    it('handleTabClick', () => {
      component['selectBetSlipTab'] = jasmine.createSpy();
      component.handleTabClick({ id: 0, tab: 'test' });
      expect(component['selectBetSlipTab']).toHaveBeenCalledWith(0 as any, 'test' as any);
    });

    it('handleTabClick (unseved acca in bs widget)', () => {
      component['editMyAccaUnsavedInWidget'] = true;
      component.handleTabClick({ id: 0, tab: 'test' });
      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.EMA_OPEN_CANCEL_DIALOG);
    });
  });

  describe('setActiveView', () => {
    it('setActiveView betslip', () => {
      component['publishTabName'] = jasmine.createSpy();
      component.setActiveView('betslip');
      expect(component.activeView).toEqual('betslip');
      expect(component['publishTabName']).toHaveBeenCalledWith('betslip');
    });

    it('setActiveView mybets', () => {
      component.betslipTabs = [{ id: 0, name: 'Cashout', title:"Cashout", url: "" }, { id: 2, name: 'Open Bets', title:"Open Bets", url: ""  }]
      component['publishTabName'] = jasmine.createSpy();
      component['editMyAccaUnsavedInWidget'] = true;
      component.setActiveView('mybets');
      expect(component.activeView).not.toEqual('mybets');
      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.EMA_OPEN_CANCEL_DIALOG);
      expect(component['publishTabName']).toHaveBeenCalledWith('mybets');
    });
  });

  it('LOAD_CASHOUT_BETS', () => {
    component.tabsMap = {cashout: 'cashout'};
    betslipTabsService.getTabsList.and.returnValue(observableOf([{ id: 0, name: 'Cashout' }, { id: 2, name: 'Open Bets' }]));
    component['selectMyBetsTab'] = jasmine.createSpy().and.callFake(() => {});

    component.ngOnInit();
    subscribeEvents['LOAD_CASHOUT_BETS']();
    expect(component['selectMyBetsTab']).toHaveBeenCalled();
    expect(betslipTabsService.createTab).toHaveBeenCalledWith('cashout', 1);
  });

  it('LOAD_UNSETTLED_BETS', () => {
    component['selectMyBetsTab'] = jasmine.createSpy().and.callFake(() => {});
    betslipTabsService.getTabsList.and.returnValue(observableOf([{ id: 0, name: 'Cashout' }, { id: 2, name: 'Open Bets' }]));

    component.ngOnInit();
    subscribeEvents['LOAD_UNSETTLED_BETS']();
    expect(component['selectMyBetsTab']).toHaveBeenCalled();
    expect(betslipTabsService.createTab).toHaveBeenCalledWith('openbets', 2);
  });

  it('LOAD_BET_HISTORY', () => {
    component.tabsMap = {bethistory: 'bethistory'};
    component['selectMyBetsTab'] = jasmine.createSpy().and.callFake(() => {});
    betslipTabsService.getTabsList.and.returnValue(observableOf([{ id: 0, name: 'Cashout' }, { id: 2, name: 'Open Bets' }]));

    component.ngOnInit();
    subscribeEvents['LOAD_BET_HISTORY']();
    expect(component['selectMyBetsTab']).toHaveBeenCalled();
    expect(betslipTabsService.createTab).toHaveBeenCalledWith('betHistory', 3);
  });

  it('EMA_UNSAVED_IN_WIDGET', () => {
    betslipTabsService.getTabsList.and.returnValue(observableOf([{ id: 0, name: 'Cashout' }, { id: 2, name: 'Open Bets' }]));
    component.ngOnInit();
    subscribeEvents['EMA_UNSAVED_IN_WIDGET'](true);
    expect(component['editMyAccaUnsavedInWidget']).toEqual(true);
  });

  it('UPDATE_SETTLED_BETS_HEIGHT', () => {
    betslipTabsService.getTabsList.and.returnValue(observableOf([{ id: 0, name: 'Cashout' }, { id: 2, name: 'Open Bets' }]));
    deviceService.isDesktop = true;
    component.isHeightUpdated = true;
    windowRef.document.querySelector = jasmine.createSpy().and.returnValue({});
    windowRef.document.querySelectorAll = jasmine.createSpy().and.returnValue([{clientHeight: 10}]);
    component.ngOnInit();
    subscribeEvents['UPDATE_SETTLED_BETS_HEIGHT'](2);
    expect(component['betCount']).toEqual(2);
  });

  it('UPDATE_ITEM_HEIGHT', () => {
    component.isDefaultHeight = false;
    betslipTabsService.getTabsList.and.returnValue(observableOf([{ id: 0, name: 'Cashout' }, { id: 2, name: 'Open Bets' }]));
    component.ngOnInit();
    subscribeEvents['UPDATE_ITEM_HEIGHT'](true);
    expect(component['isDefaultHeight']).toEqual(true);
  });

  describe('widget actions', () => {
    describe('select widget tabs', () => {
      let mockData;

      beforeEach(() => {
        mockData = { id: 0, name: 'betslip' } as any;
        component['updateActiveTab'] = jasmine.createSpy();
      });

      it('@selectBetSlipTab', () => {
        component['publishTabName'] = jasmine.createSpy();
        component.betslipTabs = [{ id: 0, name: 'Cashout', title:"Cashout", url: "" }, { id: 2, name: 'Open Bets', title:"Open Bets", url: ""  }];
        component.activeTab = {id: 0} as any;
        component.activeView = 'betslip';
        component['selectBetSlipTab']('betslip', mockData);
        expect(component['updateActiveTab']).toHaveBeenCalledWith(mockData);
        expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.BETSLIP_LABEL, 'betslip');
        expect(component['publishTabName']).toHaveBeenCalledWith('betslip');
      });

      it('@selectMyBetsTab', () => {
        component['setActiveView'] = jasmine.createSpy();

        component['selectMyBetsTab'](mockData);
        expect(component['updateActiveTab']).toHaveBeenCalledWith(mockData);
        expect(component['setActiveView']).toHaveBeenCalledWith(component.MAIN_VIEWS.MY_BETS);
      });
    });

    it('@updateActiveTab', () => {
      const mockData = { id: 2, name: 'myBets' } as any;
      component.activeTab = {} as any;

      component['updateActiveTab'](mockData);
      expect(component.activeTab).toEqual(mockData);
      expect(component.errorMsg).toEqual('betslip');
    });

    it('@updateActiveTab: should not show error when user is logged in', () => {
      userService.status = true;
      const mockData = { id: 2, name: 'myBets' } as any;
      component.activeTab = {} as any;

      component['updateActiveTab'](mockData);
      expect(component.activeTab).toEqual(mockData);
      expect(component.errorMsg).toEqual('');
    });

    it('@openBetslip', () => {
      component['setActiveView'] = jasmine.createSpy();

      component['openBetslip']();
      expect(component['setActiveView']).toHaveBeenCalledWith(component.MAIN_VIEWS.BETSLIP);
    });
  });

  describe('@showError', () => {
    beforeEach(() => {
      localeService.getString = jasmine.createSpy('getString').and.callFake((token: string, args: { page: string }) => {
        if (token.indexOf('cashout') > -1 && token.indexOf('betslipTabs') > -1) {
          return 'cash out';
        } else if (args && args.page && args.page.indexOf('cashout')) {
          return args && args.page;
        } else {
          return 'betslip';
        }
      });
    });

    it('should show error message when user is logged out', () => {
      const activeTabName = 'Open Bets';
      component['showError'](activeTabName);

      expect(component.errorMsg).toEqual('betslip');
      expect(localeService.getString).toHaveBeenCalledWith('app.betslipTabs.openbets');
      expect(localeService.getString).toHaveBeenCalledWith('app.loginToSeePageMessage', { page: 'betslip' });
    });

    it('should show error message for cash out tab', () => {
      const activeTabName = 'Cash Out';
      component['showError'](activeTabName);

      expect(component.errorMsg).toEqual('cash out bets');
      expect(localeService.getString).toHaveBeenCalledWith('app.betslipTabs.cashout');
      expect(localeService.getString).toHaveBeenCalledWith('app.loginToSeePageMessage', { page: 'cash out bets' });
    });
  });

  describe('publishTabName', ()=> {
    it('if tabe name is betslip', () => {
      component.betslipTabs = [{ id: 0, name: 'Cashout', title:"Cashout", url: "" }, { id: 2, name: 'Open Bets', title:"Open Bets", url: ""  }];
      component.activeTab = {id: 0} as any;
      component.activeView = 'betslip';
      component['publishTabName']('betslip');
      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.REUSE_LOCATION, 'betslip');
    });
    it('if tab name is mybets', () => {
      component.betslipTabs = [{ id: 0, name: 'Cashout', title:"Cashout", url: "" }, { id: 2, name: 'Open Bets', title:"Open Bets", url: ""  }];
      component.activeTab = {id: 0} as any;
      component.activeView = 'my bets';
      component['publishTabName']('my bets');
      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.REUSE_LOCATION, 'my bets- cashout');
    });
  })

});
