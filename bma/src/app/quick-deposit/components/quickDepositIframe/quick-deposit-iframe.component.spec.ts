import { QuickDepositIframeComponent } from './quick-deposit-iframe.component';
import { SafeResourceUrl } from '@angular/platform-browser';
import { SimpleChanges } from '@angular/core';
import { fakeAsync, tick } from '@angular/core/testing';
import { of, throwError } from 'rxjs';
import { IEvent, IEventData } from './quick-deposit-event.model';

describe('QuickDepositIframeComponent', () => {
  let component: QuickDepositIframeComponent;

  let quickDepositIframeService;
  let vanillaAuthService;
  let domToolsService;
  let windowRefService;
  let deviceService;
  const url = 'url' as SafeResourceUrl;

  beforeEach(() => {

    const HTMLElements = {
      '.quick-deposit__header': {
        clientHeight: 55
      }
    };

    quickDepositIframeService = {
      getUrl: jasmine.createSpy().and.returnValue(url),
      isEnabled: jasmine.createSpy().and.returnValue(of(true)),
      redirectToDepositPage: jasmine.createSpy()
    };
    vanillaAuthService = {
      refreshBalance: jasmine.createSpy().and.returnValue(Promise.resolve())
    };
    domToolsService = {
      getHeight: jasmine.createSpy().and.callFake((el) => {
        return el.clientHeight;
      }),
      getWidth: jasmine.createSpy('getHeight'),
      HeaderEl: {
        clientHeight: 60
      }
    };
    windowRefService = {
      document: {
        querySelector: jasmine.createSpy().and.callFake((id: string) => {
          return HTMLElements[id];
        }),
        body: {
          clientHeight: 500
        }
      }
    };
    deviceService = {
      isPortraitOrientation: true,
    };

    component = new QuickDepositIframeComponent(
      quickDepositIframeService,
      vanillaAuthService,
      domToolsService,
      windowRefService,
      deviceService
    );
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('#ngOnInit should load quick-deposit iframe if it`s enabled', () => {
    component.stake = 5;
    component.estimatedReturn = 70;
    component['redirectToDepositPage'] = jasmine.createSpy();
    component.ngOnInit();
    expect(component.isQuickDepositEnabled).toBeTruthy();
    expect(component.url).toBe(url);
    expect(quickDepositIframeService.getUrl).toHaveBeenCalledWith(component.stake, component.estimatedReturn);
    expect(component['redirectToDepositPage']).not.toHaveBeenCalled();
  });

  it('#ngOnInit should not load quick-deposit when it is not enabled', () => {
    quickDepositIframeService.isEnabled = jasmine.createSpy().and.returnValue(of(false));
    component['redirectToDepositPage'] = jasmine.createSpy();
    component.ngOnInit();
    expect(component.isQuickDepositEnabled).toBeFalsy();
    expect(component['redirectToDepositPage']).toHaveBeenCalled();
    expect(quickDepositIframeService.getUrl).not.toHaveBeenCalled();
  });

  it('#ngOnInit should not load quick-deposit when isEnabled returns false', () => {
    quickDepositIframeService.isEnabled = jasmine.createSpy().and.returnValue(throwError({}));
    component['redirectToDepositPage'] = jasmine.createSpy();
    component.ngOnInit();
    expect(component.isQuickDepositEnabled).toBeFalsy();
    expect(component['redirectToDepositPage']).toHaveBeenCalled();
    expect(quickDepositIframeService.getUrl).not.toHaveBeenCalled();
  });

  it('#ngOnDestroy', () => {
    (component['isEnabledSubscription'] as any) = {
      unsubscribe: jasmine.createSpy()
    };
    component.ngOnDestroy();
    expect(component['isEnabledSubscription'].unsubscribe).toHaveBeenCalled();
  });

  it('should multiply original stake by 100', () => {
    component.stake = 10;
    expect(component.stake).toBe(1000);
  });

  describe('ngOnChanges', () => {
    let changes = {
      stake: {
        currentValue: 5,
        previousValue: 10,
      },
      priceChangeBannerMsg: {} as any,
      placeSuspendedErr: {
        currentValue: {msg: ''},
        previousValue: {msg: ''},
      }
    } as any;

    it('#ngOnChanges should not call any methods when no properties were changed', () => {
      changes = {} as SimpleChanges;
      component['handleStakeChange'] = jasmine.createSpy();
      component['handlePriceChange'] = jasmine.createSpy();
      component['handleSuspendedChange'] = jasmine.createSpy();
      component.ngOnChanges(changes);
      expect(component['handleStakeChange']).not.toHaveBeenCalled();
      expect(component['handlePriceChange']).not.toHaveBeenCalled();
      expect(component['handleSuspendedChange']).not.toHaveBeenCalled();
    });

    it('#ngOnChanges should not call handleStakeChange when stake was set for the first time', () => {
      changes = {
        stake: {
          firstChange: false,
          currentValue: 20,
          previousValue: undefined,
          isFirstChange: () => false
        },
        placeSuspendedErr: {
          firstChange: false,
          currentValue: undefined,
          previousValue: undefined,
          isFirstChange: () => false
        }
      } as SimpleChanges;
      component['handleStakeChange'] = jasmine.createSpy();
      component.ngOnChanges(changes);
      expect(component['handleStakeChange']).not.toHaveBeenCalled();
    });

    it('#ngOnChanges should call handleStakeChange when stake was changed', () => {
      changes = {
        stake: {
          firstChange: false,
          currentValue: 5,
          previousValue: 10,
          isFirstChange: () => false
        },
        placeSuspendedErr: {
          firstChange: false,
          currentValue: undefined,
          previousValue: undefined,
          isFirstChange: () => false
        }
      } as SimpleChanges;
      component['handleStakeChange'] = jasmine.createSpy();
      component.ngOnChanges(changes);
      expect(component['handleStakeChange']).toHaveBeenCalled();
    });

    it('#ngOnChanges should not call handlePriceChange when estimatedReturnAfterPriceChange is undefined', () => {
      changes = {
        estimatedReturnAfterPriceChange: {
          firstChange: false,
          currentValue: undefined,
          previousValue: 10,
          isFirstChange: () => false
        }
      } as SimpleChanges;
      component['handlePriceChange'] = jasmine.createSpy();
      component.ngOnChanges(changes);
      expect(component['handlePriceChange']).not.toHaveBeenCalled();
    });

    it('#ngOnChanges should call handlePriceChange when estimatedReturnAfterPriceChange was changed', () => {
      changes = {
        estimatedReturnAfterPriceChange: {
          firstChange: false,
          currentValue: 12,
          previousValue: 10,
          isFirstChange: () => false
        }
      } as SimpleChanges;
      component.estimatedReturnAfterPriceChange = 12;
      component['handlePriceChange'] = jasmine.createSpy();
      component.ngOnChanges(changes);
      expect(component['handlePriceChange']).toHaveBeenCalledWith(component.estimatedReturnAfterPriceChange);
    });

    it('#ngOnChanges should not call handleSuspendedChange when placeSuspendedErr is undefined', () => {
      changes = {
        placeSuspendedErr: {
          firstChange: false,
          currentValue: undefined,
          previousValue: undefined,
          isFirstChange: () => false
        }
      } as SimpleChanges;
      component['handleSuspendedChange'] = jasmine.createSpy();
      component.ngOnChanges(changes);
      expect(component['handleSuspendedChange']).not.toHaveBeenCalled();
    });

    it('#ngOnChanges should not call handleSuspendedChange if msg was not changed', () => {
      changes = {
        placeSuspendedErr: {
          firstChange: false,
          currentValue: {
            multipleWithDisableSingle: undefined,
            disableBet: false,
            msg: '',
          },
          previousValue: {
            multipleWithDisableSingle: false,
            disableBet: true,
            msg: '',
          },
          isFirstChange: () => false
        }
      } as SimpleChanges;
      component['handleSuspendedChange'] = jasmine.createSpy();
      component.ngOnChanges(changes);
      expect(component['handleSuspendedChange']).not.toHaveBeenCalled();
    });

    it('#ngOnChanges should call handleSuspendedChange when placeSuspendedErr was changed', () => {
      changes = {
        placeSuspendedErr: {
          firstChange: false,
          currentValue: {
            multipleWithDisableSingle: undefined,
            disableBet: false,
            msg: '',
          },
          previousValue: {
            multipleWithDisableSingle: false,
            disableBet: true,
            msg: 'placeSuspendedErr',
          },
          isFirstChange: () => false
        }
      } as SimpleChanges;
      component['handleSuspendedChange'] = jasmine.createSpy();
      component.ngOnChanges(changes);
      expect(component['handleSuspendedChange']).toHaveBeenCalled();
    });
  });

  it('should emit closeWindow event', fakeAsync(() => {
    component.closeWindow.emit = jasmine.createSpy();
    component.closeIFrameQD();
    tick();

    expect(component['vanillaAuthService'].refreshBalance).toHaveBeenCalled();
    expect(component.showContent).toBeFalsy();
    expect(component.closeWindow.emit).toHaveBeenCalledWith(null);
  }));

  it('handleStakeChange should not emit event', () => {
    const event = {
      eventName: 'StakeChange',
      eventData: {
        stake: 5,
        estimatedReturn: 7
      }
    };
    component['getEventObj'] = jasmine.createSpy().and.returnValue(event);
    component['sendPostMessageToIFrame'] = jasmine.createSpy();
    component.quickDepositStakeChange.emit = jasmine.createSpy();
    component['handleStakeChange']();
    expect(component['getEventObj']).toHaveBeenCalledWith('StakeChange');
    expect(component['sendPostMessageToIFrame']).toHaveBeenCalledWith(event);
    expect(component.quickDepositStakeChange.emit).not.toHaveBeenCalled();
  });

  it('handleStakeChange should emit event', () => {
    const event = {
      eventName: 'StakeChange',
      eventData: {
        stake: 5,
        estimatedReturn: 7
      }
    };
    component['getEventObj'] = jasmine.createSpy().and.returnValue(event);
    component['sendPostMessageToIFrame'] = jasmine.createSpy();
    component.quickDepositStakeChange.emit = jasmine.createSpy();
    component.quickDepositStakeChange.observers = [
      {
        closed: false,
        complete: () => {},
        error: () => {},
        next: () => {}
      }
    ] as any;
    component['handleStakeChange']();
    expect(component['getEventObj']).toHaveBeenCalledWith('StakeChange');
    expect(component['sendPostMessageToIFrame']).toHaveBeenCalledWith(event);
    expect(component.quickDepositStakeChange.emit).toHaveBeenCalledWith(null);
  });

  it('handlePriceChange', () => {
    const estimatedReturnAfterPriceChange = 12;
    const event = {
      eventName: 'PriceChange',
      eventData: {
        stake: 5,
        estimatedReturn: 7
      }
    };
    component['getEventObj'] = jasmine.createSpy().and.returnValue(event);
    component['sendPostMessageToIFrame'] = jasmine.createSpy();
    component['handlePriceChange'](estimatedReturnAfterPriceChange);
    expect(component['getEventObj']).toHaveBeenCalledWith('PriceChange', estimatedReturnAfterPriceChange);
    expect(component['sendPostMessageToIFrame']).toHaveBeenCalledWith(event);
  });

  it('handleSuspendedChange is suspended', () => {
    const event = {
      eventName: 'EventSuspended'
    };
    component['getEventObj'] = jasmine.createSpy().and.returnValue(event);
    component['sendPostMessageToIFrame'] = jasmine.createSpy();
    component['handleSuspendedChange'](true);
    expect(component['getEventObj']).toHaveBeenCalledWith('EventSuspended', 0, false);
    expect(component['sendPostMessageToIFrame']).toHaveBeenCalledWith(event);
  });

  it('handleSuspendedChange is unsuspended', () => {
    const event = {
      eventName: 'EventUnSuspended'
    };
    component['getEventObj'] = jasmine.createSpy().and.returnValue(event);
    component['sendPostMessageToIFrame'] = jasmine.createSpy();
    component['handleSuspendedChange'](false);
    expect(component['getEventObj']).toHaveBeenCalledWith('EventUnSuspended', 0, false);
    expect(component['sendPostMessageToIFrame']).toHaveBeenCalledWith(event);
  });

  it('getEventObj should return event obj with data', () => {
    component.stake = 7;
    component.estimatedReturn = 12;
    const eventName = 'StakeChange';
    const event = component['getEventObj'](eventName);
    const eventData = {
      stake: component.stake,
      estimatedReturn: component.estimatedReturn * 100
    } as IEventData;
    expect(event).toEqual(jasmine.objectContaining({ eventName, eventData } as IEvent));
  });

  it('getEventObj should return event obj with passed estimatedReturn in data', () => {
    component.stake = 7;
    component.estimatedReturn = 12;
    const eventName = 'PriceChange';
    const estimatedReturnAfterPriceChange = 16;
    const event = component['getEventObj'](eventName, estimatedReturnAfterPriceChange);
    const eventData = {
      stake: component.stake,
      estimatedReturn: estimatedReturnAfterPriceChange * 100
    } as IEventData;
    expect(event).toEqual(jasmine.objectContaining({ eventName, eventData } as IEvent));
  });

  it('getEventObj should return event obj without data', () => {
    const eventName = 'EventSuspended';
    const event = component['getEventObj'](eventName, 0, false);
    expect(event).toEqual(jasmine.objectContaining({ eventName } as IEvent));
  });


  it('should send post message event to iframe', () => {
    const event = {
      eventName: 'StakeChange',
      eventData: {
        stake: 7,
        estimatedReturn: 12
      }
    } as IEvent;
    component.iframe = {
      nativeElement: {
        contentWindow: {
          postMessage: jasmine.createSpy()
        }
      }
    };
    component.showContent = true;
    component['sendPostMessageToIFrame'](event);
    expect(component.iframe.nativeElement.contentWindow.postMessage)
      .toHaveBeenCalledWith('{"eventName":"StakeChange","eventData":{"stake":7,"estimatedReturn":12}}', '*');
  });

  it('should not send post message event to iframe', () => {
    const event = {
      eventName: 'StakeChange',
      eventData: {
        stake: 7,
        estimatedReturn: 12
      }
    } as IEvent;
    component.iframe = {
      nativeElement: {
        contentWindow: {
          postMessage: jasmine.createSpy()
        }
      }
    };
    component.showContent = false;
    component['sendPostMessageToIFrame'](event);
    expect(component.iframe.nativeElement.contentWindow.postMessage).not.toHaveBeenCalled();
    expect(component['eventsToSend']).toEqual(jasmine.arrayContaining([event]));
  });

  it('should call handleMessage method when receives post message', () => {
    const event = {} as MessageEvent;
    component['handleMessage'] = jasmine.createSpy();
    component.onMessage(event);
    expect(component['handleMessage']).toHaveBeenCalledWith(event);
  });

  it('should call openIFrame method', () => {
    const event = { data: 'action%3Dopen'} as MessageEvent;
    component['openIFrame'] = jasmine.createSpy();
    component['handleMessage'](event);
    expect(component['openIFrame']).toHaveBeenCalled();
  });

  it('should call resizeIFrame method', () => {
    const event = { data: 'action%3Dresize%26width%3D320%26height%3D370' } as MessageEvent;
    component['resizeIFrame'] = jasmine.createSpy();
    component['handleMessage'](event);
    expect(component['resizeIFrame']).toHaveBeenCalledWith(event);
  });

  it('should call closeIFrame method', () => {
    const event = { data: 'action%3Dclose'} as MessageEvent;
    component['closeIFrame'] = jasmine.createSpy();
    component['handleMessage'](event);
    expect(component['closeIFrame']).toHaveBeenCalled();
  });

  it('should redirect to deposit page', () => {
    component['redirectToDepositPage']();
    expect(quickDepositIframeService.redirectToDepositPage).toHaveBeenCalled();
  });

  it('should define action correctly', () => {
    const event = { data: 'action%3Dopen'} as MessageEvent;
    const action = component['getEventAction'](event);
    expect(action).toBe('open');
  });

  it('should show iframe and emit event when there are observers', () => {
    component.openIframeEmit.emit = jasmine.createSpy();
    component.openIframeEmit.observers = [
      {
        closed: false,
        complete: () => {},
        error: () => {},
        next: () => {}
      }
    ] as any;
    component['sendPendingPostMessages'] = jasmine.createSpy();
    component['openIFrame']();
    expect(component.showContent).toBeTruthy();
    expect(component['sendPendingPostMessages']).toHaveBeenCalled();
    expect(component.openIframeEmit.emit).toHaveBeenCalled();
  });

  it('should show iframe and should not emit event when there are no observers', () => {
    component.openIframeEmit.emit = jasmine.createSpy();
    component.openIframeEmit.observers = [];
    component['sendPendingPostMessages'] = jasmine.createSpy();
    component['openIFrame']();
    expect(component.showContent).toBeTruthy();
    expect(component['sendPendingPostMessages']).toHaveBeenCalled();
    expect(component.openIframeEmit.emit).not.toHaveBeenCalled();
  });

  it('should close iframe',  fakeAsync(() => {
    component.closeIframeEmit.emit = jasmine.createSpy();
    component['closeIFrame']();
    expect(component['vanillaAuthService'].refreshBalance).toHaveBeenCalled();

    tick();

    expect(component.showContent).toBeFalsy();
    expect(component.closeIframeEmit.emit).toHaveBeenCalled();
  }));

  it('should not handle balance update action', () => {
    const event = { data: 'action%3DupdateBalance'} as MessageEvent;
    component['openIFrame'] = jasmine.createSpy();
    component['resizeIFrame'] = jasmine.createSpy();
    component['closeIFrameQD'] = jasmine.createSpy();
    component['handleMessage'](event);
    expect(component['openIFrame']).not.toHaveBeenCalled();
    expect(component['resizeIFrame']).not.toHaveBeenCalled();
    expect(component['closeIFrameQD']).not.toHaveBeenCalled();
  });

  it('should set correct iframe height and max-height', () => {
    const event = { data: 'action%3Dresize%26width%3D320%26height%3D370' } as MessageEvent;
    component['resizeIFrame'](event);
    expect(component.frameHeight).toBe(370);
    expect(component.frameMaxHeight).toBe(385);
  });

  it('should send events when iframe is already opened', () => {
    const event1 = {} as IEvent;
    const event2 = {} as IEvent;
    component['eventsToSend'] = [event1, event2];
    component['sendPostMessageToIFrame'] = jasmine.createSpy();
    component['sendPendingPostMessages']();
    expect(component['sendPostMessageToIFrame']).toHaveBeenCalledWith(event1);
    expect(component['sendPostMessageToIFrame']).toHaveBeenCalledWith(event2);
    expect(component['eventsToSend'].length).toBe(0);
  });

  it('should not send events when iframe is already opened but no events are pending', () => {
    component['eventsToSend'] = [];
    component['sendPostMessageToIFrame'] = jasmine.createSpy();
    component['sendPendingPostMessages']();
    expect(component['sendPostMessageToIFrame']).not.toHaveBeenCalled();
  });

  describe('getBodyPortraitHeight', () => {
    it('portrait orientation', () => {
      deviceService.isPortraitOrientation = true;
      component['getBodyPortraitHeight']();
      expect(domToolsService.getHeight).toHaveBeenCalled();
    });

    it('landscape orientation', () => {
      deviceService.isPortraitOrientation = false;
      component['getBodyPortraitHeight']();
      expect(domToolsService.getWidth).toHaveBeenCalled();
    });
  });
});
