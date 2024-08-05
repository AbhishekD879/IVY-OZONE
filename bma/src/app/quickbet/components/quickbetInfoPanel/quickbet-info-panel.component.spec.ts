import { fakeAsync, tick } from '@angular/core/testing';
import { QuickbetInfoPanelComponent } from '@app/quickbet/components/quickbetInfoPanel/quickbet-info-panel.component';

describe('QuickbetInfoPanelComponent', () => {
  let component,
    callbackHandler,
    quickbetNotificationService,
    pubSubService,
    fakeConfig,
    router;
  let changeDetectorRef;

  beforeEach(() => {
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges')
    };

    fakeConfig = {msg: 'fake', location: 'quick-deposit'};
    callbackHandler = jasmine.createSpy('callbackHandler');
    quickbetNotificationService = {
      config: fakeConfig
    };
    router = {
      navigateByUrl: jasmine.createSpy('navigateByUrl')
    };
    pubSubService = {
      publish: jasmine.createSpy(),
      subscribe: jasmine.createSpy(),
      API: {
        QUICKBET_INFO_PANEL: 'QUICKBET_INFO_PANEL',
      },
      unsubscribe: jasmine.createSpy()
    };
    component = new QuickbetInfoPanelComponent(
      quickbetNotificationService,
      pubSubService,
      router,
      changeDetectorRef
    );
  });

  it('should be compiled with QuickbetInfoPanelComponent', () => {
    expect(component).toBeTruthy();
  });

  describe('@$ngOnInit', () => {
    it('should init info panel config', () => {
      component.ngOnInit();

      expect(component.infoPanel).toEqual(jasmine.objectContaining(fakeConfig));
      expect(pubSubService.subscribe).toHaveBeenCalledWith(
        'QuickbetInfoPanelComponent',
        pubSubService.API.QUICKBET_INFO_PANEL,
        jasmine.any(Function));
    });

    it('should init info panel config if its quick deposit panel', () => {
      fakeConfig.location = 'selection';
      component.qdIsShown = true;
      component.ngOnInit();

      expect(component.infoPanel).toBeDefined();
      expect(pubSubService.subscribe).toHaveBeenCalledWith(
        'QuickbetInfoPanelComponent',
        pubSubService.API.QUICKBET_INFO_PANEL,
        jasmine.any(Function));
    });

    it('should update info panel config', () => {
      const newMessage = { msg: 'new' };

      pubSubService.subscribe.and.callFake((name, api, cb) => { cb(newMessage); } );
      component.infoPanel = {};
      component.ngOnInit();

      expect(component.infoPanel).toEqual(jasmine.objectContaining(newMessage));
      expect(pubSubService.subscribe).toHaveBeenCalledWith(
        'QuickbetInfoPanelComponent',
        pubSubService.API.QUICKBET_INFO_PANEL,
        jasmine.any(Function));
    });

    it('should update info panel config and filter quick deposit related', () => {
      component.qdIsShown = true;
      component.ngOnInit();

      pubSubService.subscribe.and.callFake((name, api, cb) => { cb(fakeConfig); } );

      expect(component.infoPanel).not.toBeDefined();
      expect(pubSubService.subscribe).toHaveBeenCalledWith(
        'QuickbetInfoPanelComponent',
        pubSubService.API.QUICKBET_INFO_PANEL,
        jasmine.any(Function));
    });
  });

  describe('@$ngOnDestroy', () => {
    it('should destroy component and unsubscribe', () => {
      component.ngOnDestroy();
      expect(pubSubService.unsubscribe).toHaveBeenCalledWith('QuickbetInfoPanelComponent');
    });
  });

  describe('@messageTypeClass', () => {
    it('should set css class according to infoNsg type', () => {
      component.infoPanel = {
        msg: 'Err msg',
        type: 'error'
      };
      expect(component.messageTypeClass).toEqual('error-panel');
    });

    it('should set css class according to infoNsg type', () => {
      component.infoPanel = {};
      expect(component.messageTypeClass).toEqual('');
    });

    it('should add class name for quick deposit', () => {
      component.qdIsShown = true;
      component.infoPanel = {
        msg: 'Err msg',
        type: 'error'
      };

      expect(component.messageTypeClass).toEqual('error-panel qd-info-panel');
    });
  });

  describe('@showInfoPanel', () => {
    it('should hide info msg according to location', () => {
      component.infoPanel = {
        msg: 'Err msg',
        type: 'error',
        location: 'quick-deposit'
      };
      component.qdIsShown = false;

      expect(component.showInfoPanel()).toEqual(true);
    });

    it('should show info msg according to location', () => {
      component.infoPanel = {
        msg: 'warning',
        type: 'warning',
        location: 'bet-status'
      };
      component.qdIsShown = true;

      expect(component.showInfoPanel()).toEqual(true);
    });
  });

  it('should handle click', fakeAsync(() => {
    component.notificationsPanelClickFn.subscribe(callbackHandler);
    component.onClickHandler();
    tick();

    expect(callbackHandler).toHaveBeenCalled();
  }));

  it('should handle redirect event', fakeAsync(() => {
    component.externalLinksFn.subscribe(callbackHandler);

    component.externalLinksHandler();
    tick();

    expect(callbackHandler).toHaveBeenCalled();
  }));

  it('should handle click', fakeAsync(() => {
    component.externalLinksFn.subscribe(callbackHandler);
    component.onHostClick({ target: {
      dataset: {
        routerlink: '/'
      }
    } } as any);
    tick();

    expect(callbackHandler).toHaveBeenCalled();
  }));

  it('should handle click', fakeAsync(() => {
    component.externalLinksFn.subscribe(callbackHandler);
    component.onHostClick({ target: {
      dataset: {}
    } } as any);
    tick();

    expect(callbackHandler).not.toHaveBeenCalled();
  }));

  it('should #openQuickDepositPanel', fakeAsync(() => {
    component.infoPanel = fakeConfig;
    component.notificationsPanelClickFn.subscribe(callbackHandler);
    component.openQuickDepositPanel();

    tick();

    expect(callbackHandler).toHaveBeenCalled();
  }));

  it('should not #openQuickDepositPanel', fakeAsync(() => {
    fakeConfig.location = 'fake';
    component.infoPanel = fakeConfig;
    component.notificationsPanelClickFn.subscribe(callbackHandler);
    component.openQuickDepositPanel();

    tick();

    expect(callbackHandler).not.toHaveBeenCalled();
  }));

  describe('updatePanelMessage', () => {
    it('should not skip updating message if quick deposit condititions are met and error code not cleared', () => {
      const panelMessage = { msg: 'some message', type: 'warning', location: 'bet-status' };
      const message = { msg: 'new message', type: 'warning', location: 'quick-deposit' };

      component.qdIsShown = true;
      component.infoPanel = panelMessage;
      component['updatePanelMessage'](message);

      expect(component.infoPanel).toEqual(jasmine.objectContaining(panelMessage));
    });

    it('should not skip updating message if quick deposit condititions are not met and error code is cleared', () => {
      const panelMessage = { msg: 'some message', type: 'warning', location: 'bet-status', errorCode: 'Stake is to low' };
      const message = { msg: '', type: '', location: 'quick-deposit', errorCode: '' };

      component.qdIsShown = false;
      component.infoPanel = panelMessage;
      component['updatePanelMessage'](message);

      expect(component.infoPanel).toEqual(message);
    });

    it('should not skip updating message if quick deposit location is not met and error code not cleared', () => {
      const panelMessage = { sg: 'some message', type: 'warning', location: 'bet-status', errorCode: '' };
      const message = { msg: 'new message', type: 'warning', location: 'not-quick-deposit', errorCode: '' };

      component.qdIsShown = true;
      component.infoPanel = panelMessage;
      component['updatePanelMessage'](message);

      expect(component.infoPanel).toEqual(jasmine.objectContaining(message));
    });

    it('should not skip updating message if quick deposit parameter is false', () => {
      const panelMessage = { msg: 'some message', type: 'warning', location: 'bet-status' };
      const message = { msg: 'new message', type: 'warning', location: 'quick-deposit' };

      component.qdIsShown = false;
      component.infoPanel = panelMessage;
      component['updatePanelMessage'](message);

      expect(component.infoPanel).toEqual(jasmine.objectContaining(message));
    });

    it('should not skip updating message if quick deposit parameter is false, ' +
      'locations not met and error code cleared', () => {
      const panelMessage = { msg: 'some message', type: 'warning', location: 'bet-status', errorCode: 'Stake is to low' };
      const message = { msg: '', type: '', location: 'quick-deposit', errorCode: '' };

      component.qdIsShown = false;
      component.infoPanel = panelMessage;
      component['updatePanelMessage'](message);

      expect(component.infoPanel).toEqual(jasmine.objectContaining(message));
    });

    it('should skip updating message if quick deposit parameter is true, location is "quick-deposit"' +
      'and error code is not cleared ', () => {
      const panelMessage = { msg: 'some message', type: 'warning', location: 'bet-status', errorCode: '' };
      const message = { msg: 'new message', type: 'error', location: 'quick-deposit', errorCode: '' };

      component.qdIsShown = true;
      component.infoPanel = panelMessage;
      component['updatePanelMessage'](message);

      expect(component.infoPanel).toEqual(jasmine.objectContaining(panelMessage));
    });
  });
});
