import { InplaySingleSportPageComponent } from './inplay-single-sport-page.component';
import { of as observableOf } from 'rxjs';
describe('LMInplaySingleSportPageComponent', () => {
  let component: InplaySingleSportPageComponent,
    inplayMainService,
    inplaySubscriptionManagerService,
    pubsubService,
    inPlayConnectionService,
    route,
    cms,
    router,
    deviceService,
    awsService,
    changeDetectorRef,
    sportsConfigService;

  beforeEach(() => {
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges')
    };
    route = {};
    router = {};
    deviceService = {};
    inPlayConnectionService = {};
    inplayMainService = {
      isNewUserFromOtherCountry: jasmine.createSpy().and.returnValue(true),
    };
    cms = {
      getMarketSwitcherFlagValue: jasmine.createSpy('getMarketSwitcherFlagValue').and.returnValue(observableOf(true))
    };
    pubsubService = {
      subscribe: jasmine.createSpy('subscribe').and.callFake((arg: string, p: string, fn: Function) => {
        if (p === 'SESSION_LOGIN') {
          fn();
        }
      }),
      unsubscribe: jasmine.createSpy('subscribe'),
      API: {
        SESSION_LOGIN: 'SESSION_LOGIN'
      }
    };
    inplaySubscriptionManagerService = {};
    awsService = {
      addAction: jasmine.createSpy()
    };
    sportsConfigService = {
      getSport: jasmine.createSpy('getSport').and.returnValue(observableOf({
        sportConfig: {
          config: {
            request: {
              categoryId: '16',

            }
          }
        }
      }))
    };

    component = new InplaySingleSportPageComponent(
      inplayMainService,
      inplaySubscriptionManagerService,
      pubsubService,
      inPlayConnectionService,
      route,
      cms,
      router,
      deviceService,
      awsService,
      changeDetectorRef,
      sportsConfigService
    );
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('should use OnPush strategy', () => {
    expect(InplaySingleSportPageComponent['__annotations__'][0].changeDetection).toBe(0);
  });

  describe('@showContent', () => {
    it('should subscribe and reloadComponent on event', () => {
      spyOn(component, 'reloadComponent');

      component['showContent']();
      expect(pubsubService.subscribe).toHaveBeenCalledWith('inplaySingleSportPage', 'SESSION_LOGIN', jasmine.any(Function));
      expect(component.reloadComponent).toHaveBeenCalled();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
      expect(component.state.loading).toBe(false);
    });

    it('should not reloadComponent on event', () => {
      spyOn(component, 'reloadComponent');
      inplayMainService.isNewUserFromOtherCountry.and.returnValue(false);

      component['showContent']();
      expect(pubsubService.subscribe).toHaveBeenCalled();
      expect(component.reloadComponent).not.toHaveBeenCalled();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
  });

});
