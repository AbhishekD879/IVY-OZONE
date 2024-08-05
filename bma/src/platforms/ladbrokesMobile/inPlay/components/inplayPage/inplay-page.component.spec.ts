import { InplayPageComponent as AppInplayPageComponent } from '@app/inPlay/components/inplayPage/inplay-page.component';
import { InplayPageComponent } from './inplay-page.component';

describe('InplayPageComponent', () => {
  let component: InplayPageComponent,
      inPlayConnectionService,
      inplayMainService,
      inplayStorageService,
      router,
      route,
      routingState,
      changeDetector,
      pubsubService;

  beforeEach(() => {
    router = {};
    route = {};
    routingState = {};
    inPlayConnectionService = {};
    inplayMainService = {
      isNewUserFromOtherCountry: jasmine.createSpy().and.returnValue(true),
    };
    inplayStorageService = {
      outdateRibbonCache: jasmine.createSpy('outdateRibbonCache')
    };
    pubsubService = {
      API: {
        SESSION_LOGIN: 'SESSION_LOGIN'
      },
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe')
    };
    changeDetector = {
      detectChanges: jasmine.createSpy('detectChanges')
    };

    component = new InplayPageComponent(
      inPlayConnectionService,
      inplayMainService,
      inplayStorageService,
      router,
      route,
      routingState,
      pubsubService,
      changeDetector
    );
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('should use OnPush strategy', () => {
    expect(InplayPageComponent['__annotations__'][0].changeDetection).toBe(0);
  });

  it('#addEventListeners should run addEventListeners from parent and run reloadPage', () => {
    // @ts-ignore
    spyOn(AppInplayPageComponent.prototype, 'addEventListeners');
    spyOn<any>(component, 'reloadComponent');
    pubsubService.subscribe.and.callFake((name, api, cb) => { cb(); } );

    component['addEventListeners']();

    expect(AppInplayPageComponent.prototype['addEventListeners']).toHaveBeenCalledTimes(1);

    expect(pubsubService.subscribe).toHaveBeenCalledWith('inplayPage', 'SESSION_LOGIN', jasmine.any(Function) );
    expect(component['reloadComponent']).toHaveBeenCalledTimes(1);
    expect(changeDetector.detectChanges).toHaveBeenCalled();
  });

  it('#addEventListeners should run addEventListeners from parent and NOT run reloadPage', () => {
    // @ts-ignore
    spyOn(AppInplayPageComponent.prototype, 'addEventListeners');
    spyOn<any>(component, 'reloadComponent');
    inplayMainService['isNewUserFromOtherCountry'].and.returnValue(false);
    pubsubService.subscribe.and.callFake((name, api, cb) => { cb(); } );

    component['addEventListeners']();

    expect(AppInplayPageComponent.prototype['addEventListeners']).toHaveBeenCalledTimes(1);

    expect(pubsubService.subscribe).toHaveBeenCalledWith('inplayPage', 'SESSION_LOGIN', jasmine.any(Function) );
    expect(component['reloadComponent']).toHaveBeenCalledTimes(0);
    expect(changeDetector.detectChanges).not.toHaveBeenCalled();
  });
});
