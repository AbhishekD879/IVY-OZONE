import { InplayWatchLivePageComponent } from './inplay-watch-live-page.component';
import { InplayWatchLivePageComponent
    as AppInplayWatchLivePageComponent } from '@app/inPlay/components/inplayWatchLivePage/inplay-watch-live-page.component';

describe('InplayWatchLivePageComponent', () => {
  let component: InplayWatchLivePageComponent,
    pubsubService,
    inplayMainService,
    inplayConnectionService,
    cms,
    router,
    inplaySubscriptionManagerService,
    inplayStorageService,
    changeDetectorRef;


  beforeEach(() => {
    changeDetectorRef = {
      markForCheck: jasmine.createSpy('markForCheck'),
      detectChanges: jasmine.createSpy('detectChanges')
    };

    router = {};
    inplayMainService = {
      isNewUserFromOtherCountry: jasmine.createSpy().and.returnValue(true)
    };
    cms = {};
    pubsubService = {
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: {
        SESSION_LOGIN: 'SESSION_LOGIN'
      }
    };
    inplayConnectionService = {};
    inplaySubscriptionManagerService = {};
    inplayStorageService = {};

    component = new InplayWatchLivePageComponent(
      pubsubService,
      inplayMainService,
      inplayConnectionService,
      cms,
      router,
      inplaySubscriptionManagerService,
      inplayStorageService,
      changeDetectorRef
    );
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('should use OnPush strategy', () => {
    expect(InplayWatchLivePageComponent['__annotations__'][0].changeDetection).toBe(0);
  });

  it('#addEventListeners should run addEventListeners from parent and run reloadComponent', () => {
    // @ts-ignore
    spyOn(AppInplayWatchLivePageComponent.prototype, 'addEventListeners');
    spyOn<any>(component, 'reloadComponent');
    pubsubService.subscribe.and.callFake((name, api, cb) => { cb(); } );

    component['addEventListeners']();

    expect(AppInplayWatchLivePageComponent.prototype['addEventListeners']).toHaveBeenCalledTimes(1);

    expect(pubsubService.subscribe).toHaveBeenCalledWith('inplayWatchLivePage', 'SESSION_LOGIN', jasmine.any(Function) );
    expect(component['reloadComponent']).toHaveBeenCalledTimes(1);
  });

  it('#addEventListeners should run addEventListeners from parent and NOT run reloadComponent', () => {
    // @ts-ignore
    spyOn(AppInplayWatchLivePageComponent.prototype, 'addEventListeners');
    spyOn<any>(component, 'reloadComponent');
    inplayMainService['isNewUserFromOtherCountry'].and.returnValue(false);
    pubsubService.subscribe.and.callFake((name, api, cb) => { cb(); } );

    component['addEventListeners']();

    expect(AppInplayWatchLivePageComponent.prototype['addEventListeners']).toHaveBeenCalledTimes(1);

    expect(pubsubService.subscribe).toHaveBeenCalledWith('inplayWatchLivePage', 'SESSION_LOGIN', jasmine.any(Function) );
    expect(component['reloadComponent']).toHaveBeenCalledTimes(0);
  });

  it('#ngOnDestroy should run ngOnDestroy from parent', () => {
    // @ts-ignore
    spyOn(AppInplayWatchLivePageComponent.prototype, 'ngOnDestroy');

    component['ngOnDestroy']();

    expect(AppInplayWatchLivePageComponent.prototype['ngOnDestroy']).toHaveBeenCalledTimes(1);
    expect(pubsubService.unsubscribe).toHaveBeenCalledWith('inplayWatchLivePage');
  });
});
