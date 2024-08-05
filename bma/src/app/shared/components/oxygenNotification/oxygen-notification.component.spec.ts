import { async } from '@angular/core/testing';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { OxygenNotificationComponent } from '@shared/components/oxygenNotification/oxygen-notification.component';

describe('OxygenNotificationComponent', () => {
  let component: OxygenNotificationComponent;
  let pubSubService;
  let componentFactoryResolver;
  let hideCb;
  let showCb;
  let cmp;
  let domTools;
  let changeDetectorRef;

  beforeEach(async(() => {
    cmp = {};
    pubSubService = {
      API: pubSubApi,
      subscribe: jasmine.createSpy('subscribe').and.callFake((file, method, cb) => {
        if (method === 'NOTIFICATION_HIDE') {
          hideCb = cb;
        } else if (method === 'NOTIFICATION_SHOW') {
          showCb = cb;
        }
      }),
      unsubscribe: jasmine.createSpy('unsubscribe')
    };
    componentFactoryResolver = {
      resolveComponentFactory: jasmine.createSpy('resolveComponentFactory').and.returnValue({
        create: jasmine.createSpy('create').and.returnValue({})
      })
    };
    domTools = {
      HeaderEl: { clientHeight: 40 }
    };
    changeDetectorRef = {
      markForCheck: jasmine.createSpy('markForCheck')
    };
  }));

  beforeEach(() => {
    component = new OxygenNotificationComponent(
      pubSubService,
      componentFactoryResolver,
      domTools,
      changeDetectorRef
    );

    component.componentHolder = <any> {
      createComponent: jasmine.createSpy('createComponent')
    };
  });

  it('should subscribe on events', () => {
    expect(component).toBeDefined();
    expect(pubSubService.subscribe).toHaveBeenCalledWith(
      'notificationComponent',
      pubSubService.API.NOTIFICATION_SHOW,
      jasmine.any(Function)
    );
    expect(pubSubService.subscribe).toHaveBeenCalledWith(
      'notificationComponent',
      pubSubService.API.NOTIFICATION_HIDE,
      jasmine.any(Function)
    );
  });

  it('should show', () => {
    showCb(cmp);
    expect(componentFactoryResolver.resolveComponentFactory).toHaveBeenCalledWith(cmp);
  });

  it('should hide', () => {
    hideCb();
    expect(component['componentRef']).not.toBeDefined();

    component['componentRef'] = <any>{
      destroy: jasmine.createSpy('destroy')
    };
    hideCb();
    expect(component['componentRef'].destroy).toHaveBeenCalled();
    expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
  });

  it('should setNotificationOffset', () => {
    showCb(cmp);

    expect(component.offsetTop).toEqual(34);
    expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
  });

  it('ngOnDestroy should unsubscribe form notificationComponent', () => {
    component.ngOnDestroy();

    expect(pubSubService.unsubscribe).toHaveBeenCalledWith('notificationComponent');
  });
});
