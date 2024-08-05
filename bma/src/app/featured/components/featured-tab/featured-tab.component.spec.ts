import { FeaturedTabComponent } from '@featured/components/featured-tab/featured-tab.component';
import { of as observableOf, throwError } from 'rxjs';

describe('FeaturedTabComponent', () => {
  let component: FeaturedTabComponent;

  let nativeBridgeService;
  let cms;
  let location;
  let router;
  let windowRef;
  let user;
  let activatedRoute;
  let changeDetectorRef, vnuser,
  pubSubService,
  device,
  sessionStorageService;
  const hubIndexInParamsMock = '1';

  beforeEach(() => {
    sessionStorageService = {
      set: jasmine.createSpy('set'),
      get: jasmine.createSpy('').and.returnValue(null),
      remove: jasmine.createSpy('remove')
    };
    device = { isMobileOnly: true};
    const pubsubReg={};
    pubSubService = {
      publish: jasmine.createSpy('publish'),
      API: {
        SESSION_LOGOUT: 'SESSION_LOGOUT',
        SUCCESSFUL_LOGIN: 'SUCCESSFUL_LOGIN'
      },
      subscribe: jasmine.createSpy('subscribe').and.callFake((a, b, cb) => { cb && cb(true); }),
      unsubscribe: jasmine.createSpy('unsubscribe')
    };
    nativeBridgeService = {
      getMobileOperatingSystem: jasmine.createSpy('getMobileOperatingSystem'),
      hasOnFeaturedTabClicked: jasmine.createSpy('hasOnFeaturedTabClicked'),
      onFeaturedTabClicked: jasmine.createSpy('onFeaturedTabClicked')
    };
    cms = {
      getRibbonModule: jasmine.createSpy('getRibbonModule').and.returnValue(observableOf({
        getRibbonModule: []
      })),
      getFirstBetDetails: jasmine.createSpy('getFirstBetDetails').and.returnValue(observableOf({
        brand:'bma',
        months:1
      }))
    };
    user={
      status:true,
      sportBalance:11,
      lastBet:'22/02/1992'
    }
    location = {
      path: jasmine.createSpy('path').and.returnValue('')
    };
    router = {
      navigate: jasmine.createSpy('navigate')
    };
    windowRef = {
      nativeWindow: {
        location: {
          href: 'https://sports.coral.co.uk/'
        }
      }
    };
    const date = new Date(); date. setDate(date. getDate() + 1);
    user = {
      username:'test',
        status:true,
        sportBalance:11,
        lastBet:date,
      getJourneyParams: jasmine.createSpy('getJourneyParams').and.returnValue({}),
      canActivateJourney: jasmine.createSpy('canActivateJourney').and.returnValue(false)
    };
    activatedRoute = {
      snapshot: {
        paramMap: {
          get: jasmine.createSpy('get').and.returnValue(null)
        }
      },
      params: observableOf({
        hubIndex: hubIndexInParamsMock
      })
    } as any;

    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges'),
      markForCheck: jasmine.createSpy('markForCheck')
    };

    component = new FeaturedTabComponent(
      nativeBridgeService,
      cms,
      location,
      router,
      windowRef,
      user,
      activatedRoute,
      changeDetectorRef
    );

  component.user.status=true;

  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('should redirect to first cms ribbon module', () => {
    
   //   spyOn(component, 'hideSpinner').and.callThrough();
    cms.getRibbonModule.and.returnValue(observableOf({
      getRibbonModule: [
        {
          directiveName: 'InPLay',
          id: 'in-play',
          url: '/some-url'
        }
      ]
    }));
    location.path.and.returnValue('/not/home/featured/page');
    user.canActivateJourney.and.returnValue(false);
    component.ngOnInit();

    expect(component.hubIndex).toEqual(hubIndexInParamsMock);
    expect(user.getJourneyParams).toHaveBeenCalledWith(jasmine.any(String));
    expect(user.canActivateJourney).toHaveBeenCalledWith({});
    expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    expect(router.navigate).toHaveBeenCalledWith(['some-url']);
  });

  it('should not redirect if featured tab page', () => {
    cms.getRibbonModule.and.returnValue(observableOf({
      getRibbonModule: [
        {
          directiveName: 'InPLay',
          id: 'in-play',
          url: '/some/url'
        }
      ]
    }));
    location.path.and.returnValue('/home/featured');
    user.canActivateJourney.and.returnValue(false);
    nativeBridgeService.hasOnFeaturedTabClicked.and.returnValue(false);
    pubSubService.subscribe.and.callFake((name, method, cb) => {
      if (method.indexOf(pubSubService.API.SESSION_LOGOUT) >= 0) {
        throwError('error');
      }
    });
    component.ngOnInit();

    expect(router.navigate).not.toHaveBeenCalled();
    expect(component.isFeaturedTabShown).toBe(true);
    expect(nativeBridgeService.onFeaturedTabClicked).not.toHaveBeenCalled();
  });

  it('should handle getRibbon error', () => {
    spyOn(component, 'showError');
    spyOn(component, 'hideSpinner');

    cms.getRibbonModule.and.returnValue(throwError('error'));
    component.ngOnInit();

    expect(component.showError).toHaveBeenCalled();
    expect(component.hideSpinner).toHaveBeenCalled();
  });

  it('should handle  error with user status false', () => {
    spyOn(component, 'showError').and.callThrough();
    spyOn(component, 'hideSpinner').and.callThrough();
    activatedRoute.snapshot.paramMap.get.and.throwError();
    component.user.status=false;
    cms.getRibbonModule.and.returnValue(throwError('no ribbon data'));
    component.ngOnInit();

    expect(component.showError).toHaveBeenCalled();
    expect(component.hideSpinner).toHaveBeenCalled();
  });

  it('should not redirect if featured-tab is first', () => {
    cms.getRibbonModule.and.returnValue(observableOf({
      getRibbonModule: [
        {
          directiveName: 'Featured',
          id: 'tab-featured',
          url: '/some/url',
          devices: 'testDevice'
        }
      ]
    }));
    location.path.and.returnValue('/not/home/featured/page');
    user.canActivateJourney.and.returnValue(false);
    nativeBridgeService.getMobileOperatingSystem.and.returnValue('testDevice');
    nativeBridgeService.hasOnFeaturedTabClicked.and.returnValue(true);

    component.ngOnInit();

    expect(component.isFeaturedTabShown).toBe(false);
    expect(router.navigate).not.toHaveBeenCalled();
  });

  it('should not redirect if user upgrade journey', () => {
    cms.getRibbonModule.and.returnValue(observableOf({
      getRibbonModule: [
        {
          directiveName: 'InPlay',
          id: 'in-play',
          url: '/some/url'
        }
      ]
    }));
    location.path.and.returnValue('/not/home/featured/page');
    user.canActivateJourney.and.returnValue(true);
    nativeBridgeService.hasOnFeaturedTabClicked.and.returnValue(true);
    component.ngOnInit();

    expect(component.isFeaturedTabShown).toBe(false);
    expect(nativeBridgeService.onFeaturedTabClicked).toHaveBeenCalledTimes(1);
    expect(router.navigate).not.toHaveBeenCalled();
  });

  it('should use OnPush strategy', () => {
    expect(FeaturedTabComponent['__annotations__'][0].changeDetection).toBe(0);
  });
});
