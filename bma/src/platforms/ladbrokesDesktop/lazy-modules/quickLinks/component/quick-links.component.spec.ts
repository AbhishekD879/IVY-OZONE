import { LadsQuickLinksComponent } from '@ladbrokesDesktop/lazy-modules/quickLinks/component/quick-links.component';
import { IDesktopQuickLink } from '@core/services/cms/models';
import { of } from 'rxjs';

describe('LadbrokesQuickLinksComponent', () => {
  let cms, component, userService, pubSubService, bonusSuppressionService, router, flagSourceService;

  const quickLinks: IDesktopQuickLink[] = [
    {
      title: 'Football',
      target: 'sport/football'
    },
    {
      title: 'BasketBall',
      target: '/sport/basketball'
    }
  ] as IDesktopQuickLink[];

  beforeEach(() => {
    cms = {
      getDesktopQuickLinks: jasmine.createSpy('cmsQuickLinks').and.returnValue(of(quickLinks)),
      getCMSRGYconfigData: jasmine.createSpy().and.returnValue(of({}))
    };

    userService = {
      bppToken: 'abc123',
      status: true,
    };
    
    bonusSuppressionService = {
      checkIfYellowFlagDisabled: jasmine.createSpy('checkIfYellowFlagDisabled ').and.returnValue(true)
    };

    pubSubService = {
      subscribe: jasmine.createSpy('subscribe').and.callFake((arg1, arg2, callback) => callback()),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: {
        SUCCESSFUL_LOGIN: 'SUCCESSFUL_LOGIN',
        SESSION_LOGIN: 'SESSION_LOGIN',
        SESSION_LOGOUT: 'SESSION_LOGOUT'
      }
    };
    
    flagSourceService = {
      flagUpdate: {subscribe: (cb) => cb({ShowQuickLinks: true})}
    };

    router = {
      navigateByUrl: jasmine.createSpy()
    }

    component = new LadsQuickLinksComponent(cms, userService,pubSubService, bonusSuppressionService, router, flagSourceService);
  });

  describe('onInit', () => {
    it('should load and sanitize quicklinks', () => {
      component.ngOnInit();
      expect(component.quickLinks[0].target).toEqual('/sport/football');
      expect(component.quickLinks[1].target).toEqual('/sport/basketball');
    });
  });

  it('#ngOnDestroy', () => {
    component.ngOnDestroy();
    expect(pubSubService.unsubscribe).toHaveBeenCalledWith('quick-links');
  });

  it('should call navigateByUrl', () => {
    component.navigateByUrl({preventDefault: () => {}},"/url");
    expect(router.navigateByUrl).toHaveBeenCalledWith('/url');
  });
});
