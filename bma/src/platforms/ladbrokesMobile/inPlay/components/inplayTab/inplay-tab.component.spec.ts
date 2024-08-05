import { InplayTabComponent as AppInplayTabComponent } from '@app/inPlay/components/inplayTab/inplay-tab.component';
import { InplayTabComponent } from './inplay-tab.component';
import { of } from 'rxjs';

describe('InplayTabComponent', () => {
  let component: InplayTabComponent,
    inPlayConnectionService,
    inplayMainService,
    cmsService,
    inplayStorageService,
    inplaySubscriptionManagerService,
    pubsubService,
    changeDetectorRef,
    awsService,
    activatedRoute;

  beforeEach(() => {
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges')
    };
    inPlayConnectionService = {};
    inplayMainService = {
      isNewUserFromOtherCountry: jasmine.createSpy().and.returnValue(true),
    };
    cmsService = {};
    pubsubService = {
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('subscribe'),
      API: {
        SESSION_LOGIN: 'SESSION_LOGIN'
      }
    };
    inplayStorageService = {};
    inplaySubscriptionManagerService = {};
    awsService = {
      addAction: jasmine.createSpy()
    };
    activatedRoute = {
      snapshot: {
          paramMap: {
              get: jasmine.createSpy('paramMap.get').and.returnValue('golf')
          }
      },
      params: of({
          sport: 'golf',
          id: '18'
      })
  };
    component = new InplayTabComponent(
      inPlayConnectionService,
      inplayMainService,
      cmsService,
      inplayStorageService,
      inplaySubscriptionManagerService,
      pubsubService,
      changeDetectorRef,
      awsService,
      activatedRoute
    );
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('should use OnPush strategy', () => {
    expect(InplayTabComponent['__annotations__'][0].changeDetection).toBe(0);
  });

  it('#addEventListeners should run addEventListeners from parent and run reloadPage', () => {
    // @ts-ignore
    spyOn(AppInplayTabComponent.prototype, 'addEventListeners');
    spyOn<any>(component, 'reloadComponent');
    pubsubService.subscribe.and.callFake((name, api, cb) => { cb(); } );

    component['addEventListeners']();

    expect(AppInplayTabComponent.prototype['addEventListeners']).toHaveBeenCalledTimes(1);

    expect(pubsubService.subscribe).toHaveBeenCalledWith('inplay', 'SESSION_LOGIN', jasmine.any(Function) );
    expect(component['reloadComponent']).toHaveBeenCalledTimes(1);
    expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
  });

  it('#addEventListeners should run addEventListeners from parent and NOT run reloadPage', () => {
    // @ts-ignore
    spyOn(AppInplayTabComponent.prototype, 'addEventListeners');
    spyOn<any>(component, 'reloadComponent');
    inplayMainService['isNewUserFromOtherCountry'].and.returnValue(false);
    pubsubService.subscribe.and.callFake((name, api, cb) => { cb(); } );

    component['addEventListeners']();

    expect(AppInplayTabComponent.prototype['addEventListeners']).toHaveBeenCalledTimes(1);

    expect(pubsubService.subscribe).toHaveBeenCalledWith('inplay', 'SESSION_LOGIN', jasmine.any(Function) );
    expect(component['reloadComponent']).toHaveBeenCalledTimes(0);
    expect(changeDetectorRef.detectChanges).not.toHaveBeenCalled();
  });

  it('#ngOnDestroy should run ngOnDestroy from parent', () => {
    // @ts-ignore
    spyOn(AppInplayTabComponent.prototype, 'ngOnDestroy');

    component['ngOnDestroy']();

    expect(AppInplayTabComponent.prototype['ngOnDestroy']).toHaveBeenCalledTimes(1);
    expect(pubsubService.unsubscribe).toHaveBeenCalledWith('inplay');
  });
});
