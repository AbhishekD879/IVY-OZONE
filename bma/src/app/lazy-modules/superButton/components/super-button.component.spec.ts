import { of as observableOf, of } from 'rxjs';
import { SuperButtonComponent } from './super-button.component';
import { pubSubApi } from '@app/core/services/communication/pubsub/pubsub-api.constant';
import { NavigationEnd } from '@angular/router';

describe('SuperButtonComponent', () => {
  let component: SuperButtonComponent;
  let cmsService;
  let gtmService;
  let navigationService;
  let changeDetectorRef;
  let deviceService;
  let pubSubService;
  let router;
  let routingState,filtersService;
  let user;
  let locale;
  let coralSportsSegmentProviderService
  let bonusSuppressionService;


  beforeEach(() => {
    spyOn(Date, 'now').and.returnValue(1548323458917); // 2019-01-24
    cmsService = {
      getNavigationPoints: jasmine.createSpy('getNavigationPoints').and.returnValue(observableOf([{
        categoryId: [1, 2, 4],
        competitionId: ['123', '234'],
        homeTabs: ['featured', 'inplay'],
        enabled: true,
        targetUri: '/sport/football',
        title: 'Football',
        description: 'werthjk',
        validityPeriodEnd: '2019-02-24T09:48:20.917Z',
        validityPeriodStart: '2018-12-24T09:48:20.917Z',
        ctaAlignment:'center'
      }]))
    };
    pubSubService = {
      API: pubSubApi,
      unsubscribe: jasmine.createSpy('unsubscribe'),
      subscribe: jasmine.createSpy('subscribe').and.callFake((fileName: string, method: string | string[], callback: Function) => {
        callback();
      }),
    };
    gtmService = {
      push: jasmine.createSpy('push')
    };
    navigationService = {
      isInternalUri: jasmine.createSpy('isInternalUri').and.returnValue(true),
      openUrl: jasmine.createSpy('openUrl')
    };
    changeDetectorRef = {
      markForCheck: jasmine.createSpy('markForCheck')
    };
    deviceService = {
      isAndroid: false,
      isWrapper: false
    };
    router = {
      events: of(new NavigationEnd(1, '/', '/')),
    };
    routingState = {
      getCurrentUrl: jasmine.createSpy('getCurrentUrl').and.returnValue('')
    };

    bonusSuppressionService = {
      checkIfYellowFlagDisabled: jasmine.createSpy('checkIfYellowFlagDisabled').and.returnValue(true)
    } as any;

    filtersService = {
      filterLinkforRSS: jasmine.createSpy('filterLinkforRSS').and.returnValue((of('promotion/details/exclusion'))),
    };
    locale = {
      getString: jasmine.createSpy('locale.getString').and.returnValue('')
    };
    coralSportsSegmentProviderService={
      isOTFAvailable:observableOf(true)
    }
    component = new SuperButtonComponent(cmsService, gtmService, locale, navigationService, changeDetectorRef, deviceService, pubSubService,router,routingState,coralSportsSegmentProviderService, filtersService, bonusSuppressionService);
    component.type = 'sport';
    component.categoryId = 1;
    component.navPoint = {
      categoryId: [],
      competitionId: [],
      homeTabs: [""],
      enabled: false,
      targetUri: "",
      title: "",
      description: "",
      validityPeriodEnd: "",
      validityPeriodStart: "",
      shortDescription: "",
      ctaAlignment: "",
      themes: null,
      id: "",
      brand: "",
      createdBy: "",
      createdAt: '',
      updatedBy: "",
      updatedAt: "",
      updatedByUserName: "",
      createdByUserName: ""
    }
  });

  it('should create', () => {
    component.showNavPoint = jasmine.createSpy('showNavPoint');

    component.ngOnInit();
    expect(component).toBeTruthy();
    expect(cmsService.getNavigationPoints).toHaveBeenCalledTimes(4);
    expect(component['data'].length).toEqual(1);
    expect(component.showNavPoint).toHaveBeenCalled();
  });
  it('#ngOnInit havimg special char', () => {
    component.onInit = jasmine.createSpy('onInit');
    routingState.getCurrentUrl.and.returnValue('/home/featured?q=1')
    component.ngOnInit();
    expect(component.onInit).toHaveBeenCalled();
  });
  it('#ngOnInit no special char', () => {
    component.onInit = jasmine.createSpy('onInit');
    routingState.getCurrentUrl.and.returnValue('/home/featured')
    component.ngOnInit();
    expect(component.onInit).toHaveBeenCalled();
  });
  it('#ngOnInit donot have home in the route', () => {
    component.onInit = jasmine.createSpy('onInit');
    routingState.getCurrentUrl.and.returnValue('/inplay/featured')
    component.ngOnInit();
    expect(component.onInit).toHaveBeenCalled();
  });

  it('should populate the theme array with 4 items if isBrandLadbrokes is true and center alignment', () => {
    component.isBrandLadbrokes = true;
    component.themeArray = [];
    component.navPoint.ctaAlignment = 'center'
    component.onInit();

    expect(component.themeArray[0].caseVal).toEqual('theme_1');
    expect(component.themeArray[1].caseVal).toEqual('theme_2');
    expect(component.themeArray[2].caseVal).toEqual('theme_3');
    expect(component.themeArray[3].caseVal).toEqual('theme_4');

    expect(component.themeArray[0].classVal).toEqual('nav-point-theme1');
    expect(component.themeArray[1].classVal).toEqual('nav-point-theme2');
    expect(component.themeArray[2].classVal).toEqual('nav-point-theme3');
    expect(component.themeArray[3].classVal).toEqual('nav-point-theme4');

    expect(component.themeArray[0].descVal).toEqual('button btn-secondary-theme1');
    expect(component.themeArray[1].descVal).toEqual('button btn-secondary-theme2');
    expect(component.themeArray[2].descVal).toEqual('button btn-secondary-theme3');
    expect(component.themeArray[3].descVal).toEqual('button btn-secondary-theme4');

  });

  it('should populate the theme array with 6 items if isBrandLadbrokes is false and center alignment', () => {
    component.isBrandLadbrokes = false;
    component.navPoint.ctaAlignment = 'center'
    component.themeArray = [];
    component.onInit();

    expect(component.themeArray[0].caseVal).toEqual('theme_1');
    expect(component.themeArray[1].caseVal).toEqual('theme_2');
    expect(component.themeArray[2].caseVal).toEqual('theme_3');
    expect(component.themeArray[3].caseVal).toEqual('theme_4');
    expect(component.themeArray[4].caseVal).toEqual('theme_5');
    expect(component.themeArray[5].caseVal).toEqual('theme_6');

    expect(component.themeArray[0].classVal).toEqual('nav-point-coral-theme1');
    expect(component.themeArray[1].classVal).toEqual('nav-point-coral-theme2');
    expect(component.themeArray[2].classVal).toEqual('nav-point-coral-theme3');
    expect(component.themeArray[3].classVal).toEqual('nav-point-coral-theme4');
    expect(component.themeArray[4].classVal).toEqual('nav-point-coral-theme5');
    expect(component.themeArray[5].classVal).toEqual('nav-point-coral-theme6');

    expect(component.themeArray[0].descVal).toEqual('button btn-secondary-theme1');
    expect(component.themeArray[1].descVal).toEqual('button btn-secondary-theme2');
    expect(component.themeArray[2].descVal).toEqual('button btn-secondary-theme3');
    expect(component.themeArray[3].descVal).toEqual('button btn-secondary-theme4');
    expect(component.themeArray[4].descVal).toEqual('button btn-secondary-theme5');
    expect(component.themeArray[5].descVal).toEqual('button btn-secondary-theme6');

  });

  it('should populate the theme array with 6 items if isBrandLadbrokes is false and right alignment', () => {
    component.isBrandLadbrokes = false;
    component.navPoint.ctaAlignment = 'right'
    component.themeArray = [];
    component['data'] = [{
      categoryId: [1, 2, 4],
      competitionId: ['123', '234'],
      homeTabs: ['featured', 'inplay'],
      enabled: true,
      targetUri: '/sport/football',
      title: 'Football',
      description: 'werthjk',
      validityPeriodEnd: '2019-02-24T09:48:20.917Z',
      validityPeriodStart: '2018-12-24T09:48:20.917Z', ctaAlignment: 'right'
    }] as any;
    component.showNavPoint();

    expect(component.themeArray.length).toEqual(6);
    expect(component.themeArray[0].caseVal).toEqual('theme_1');
    expect(component.themeArray[1].caseVal).toEqual('theme_2');
    expect(component.themeArray[2].caseVal).toEqual('theme_3');
    expect(component.themeArray[3].caseVal).toEqual('theme_4');
    expect(component.themeArray[4].caseVal).toEqual('theme_5');
    expect(component.themeArray[5].caseVal).toEqual('theme_6');

    expect(component.themeArray[0].classVal).toEqual('row right-theme1-coral-top');
    expect(component.themeArray[1].classVal).toEqual('row right-theme2-coral-top');
    expect(component.themeArray[2].classVal).toEqual('row right-theme3-coral-top');
    expect(component.themeArray[3].classVal).toEqual('row right-theme4-coral-top');
    expect(component.themeArray[4].classVal).toEqual('row right-theme5-coral-top');
    expect(component.themeArray[5].classVal).toEqual('row right-theme6-coral-top');

    expect(component.themeArray[0].descVal).toEqual('right-theme1-coral-btn');
    expect(component.themeArray[1].descVal).toEqual('right-theme2-coral-btn');
    expect(component.themeArray[2].descVal).toEqual('right-theme3-coral-btn');
    expect(component.themeArray[3].descVal).toEqual('right-theme4-coral-btn');
    expect(component.themeArray[4].descVal).toEqual('right-theme5-coral-btn');
    expect(component.themeArray[5].descVal).toEqual('right-theme6-coral-btn');
  });

  it('should populate the theme array with 4 items if isBrandLadbrokes is true and right alignment', () => {
    component.isBrandLadbrokes = true;
    component.navPoint.ctaAlignment = 'right';
    component.themeArray = [];
    component['data'] = [{
      categoryId: [1, 2, 4],
      competitionId: ['123', '234'],
      homeTabs: ['featured', 'inplay'],
      enabled: true,
      targetUri: '/sport/football',
      title: 'Football',
      description: 'werthjk',
      validityPeriodEnd: '2019-02-24T09:48:20.917Z',
      validityPeriodStart: '2018-12-24T09:48:20.917Z', ctaAlignment: 'right'
    }] as any;
    component.showNavPoint();

    expect(component.themeArray.length).toEqual(4);
    expect(component.themeArray[0].caseVal).toEqual('theme_1');
    expect(component.themeArray[1].caseVal).toEqual('theme_2');
    expect(component.themeArray[2].caseVal).toEqual('theme_3');
    expect(component.themeArray[3].caseVal).toEqual('theme_4');

    expect(component.themeArray[0].classVal).toEqual('row right-theme1-top');
    expect(component.themeArray[1].classVal).toEqual('row right-theme2-top');
    expect(component.themeArray[2].classVal).toEqual('row right-theme3-top');
    expect(component.themeArray[3].classVal).toEqual('row right-theme4-top');

    expect(component.themeArray[0].descVal).toEqual('right-theme1-btn');
    expect(component.themeArray[1].descVal).toEqual('right-theme2-btn');
    expect(component.themeArray[2].descVal).toEqual('right-theme3-btn');
    expect(component.themeArray[3].descVal).toEqual('right-theme4-btn');

  });

  describe('onInit', () => {
    it('when CMS config is defined', () => {
      component.showNavPoint = jasmine.createSpy('showNavPoint');
      component.onInit();
      expect(cmsService.getNavigationPoints).toHaveBeenCalledTimes(1);
      expect(component['data'].length).toEqual(1);
      expect(component.showNavPoint).toHaveBeenCalled();
    });
    it('when CMS config is undefined', () => {
      cmsService.getNavigationPoints = jasmine.createSpy('getNavigationPoints').and.returnValue({ subscribe: () => {} });
      component.showNavPoint = jasmine.createSpy('showNavPoint');
      component.onInit();
      expect(component.showNavPoint).not.toHaveBeenCalled();
    });
  });

  describe('#ngOnDestroy', () => {
    it('should unsubscribe from connect and execute command', () => {
      component.ngOnDestroy();
      expect(pubSubService.unsubscribe).toHaveBeenCalledWith('super-button');
    });
  });

  describe('ngOnChanges', () => {
    it('homeTabs include homeTabUrl', () => {
      component.showNavPoint = jasmine.createSpy('showNavPoint');
      const changes = {
        homeTabUrl: {
          currentValue: 'featured'
        }
      };

      component.ngOnChanges(changes as any);
      expect(component.showNavPoint).toHaveBeenCalled();
    });

    it('homeTabs no include homeTabUrl', () => {
      component.showNavPoint = jasmine.createSpy('showNavPoint');
      const changes = {
        homeTabUrl: {
          currentValue: ''
        }
      };

      component.ngOnChanges(changes as any);
      expect(component.showNavPoint).not.toHaveBeenCalled();
    });
  });


  it('showNavPoint', () => {
    component.ngOnInit();
    expect(component.isShowNavPoint).toBeTruthy();

    component.type = 'bigCompetition';
    component.ngOnInit();
    expect(component.isShowNavPoint).toBeFalsy();

    component.type = 'homeTabs';
    component.ngOnInit();
    expect(component.isShowNavPoint).toBeFalsy();

    expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
  });

  it('setExternal Url link for android Web', () => {
    deviceService.isAndroid = true;
    component.ngOnInit();
    expect(component.isAndroidExternalUrl).toBeFalsy();
  });

  it('setExternal Url link for android wrapper for Internal link', () => {
    deviceService.isAndroid = true;
    deviceService.isWrapper = true;

    component.ngOnInit();
    expect(component.isAndroidExternalUrl).toBeFalsy();
  });

  it('setExternal Url link for android wrapper external link', () => {
    deviceService.isAndroid = true;
    deviceService.isWrapper = true;

    navigationService.isInternalUri.and.returnValue(false);

    component.ngOnInit();
    expect(component.isAndroidExternalUrl).toBeTruthy();
  });

  it('goToUrl', () => {
    component.ngOnInit();
    component.navPoint.targetUri = '/sport/football';
    component.goToUrl();

    expect(gtmService.push).toHaveBeenCalledWith(
      'Event.Tracking',{ 
        'component.CategoryEvent': 'sports banner',
        'component.LabelEvent': 'super button',
        'component.ActionEvent': 'click',
        'component.PositionEvent': '',
        'component.LocationEvent': 'sport',
        'component.EventDetails': 'Football',
        'component.URLClicked': '/sport/football'
      }
    );
    expect(filtersService.filterLinkforRSS).not.toHaveBeenCalled();
    expect(navigationService.openUrl).toHaveBeenCalledWith('/sport/football', true);
    component.type = 'bigCompetition';
    component.goToUrl();

    expect(gtmService.push).toHaveBeenCalledWith(
      'Event.Tracking',{ 
        'component.CategoryEvent': 'sports banner',
        'component.LabelEvent': 'super button',
        'component.ActionEvent': 'click',
        'component.PositionEvent': '',
        'component.LocationEvent': 'sport',
        'component.EventDetails': 'Football',
        'component.URLClicked': '/sport/football'
      }
    );
  });


  it('goToUrl call redirect if it is in-shop user', () => {
    component.ngOnInit();
    component.navPoint.targetUri = '/sport/football';
    component.goToUrl();

    expect(gtmService.push).toHaveBeenCalledWith(
      'Event.Tracking',{ 
        'component.CategoryEvent': 'sports banner',
        'component.LabelEvent': 'super button',
        'component.ActionEvent': 'click',
        'component.PositionEvent': '',
        'component.LocationEvent': 'sport',
        'component.EventDetails': 'Football',
        'component.URLClicked': '/sport/football'
      }
    );
    expect(navigationService.openUrl).toHaveBeenCalledWith('/sport/football', true);
  });
  it('goToUrl call for filterLinkForRss', () => {
  
    (filtersService['filterLinkforRSS']as any).and.returnValue(of('promotion/details/exclusion'));
    component.ngOnInit();
    component.navPoint.targetUri = 'racingsuperseries';
    component.goToUrl();
    expect(filtersService.filterLinkforRSS).toHaveBeenCalled();
    expect(component.navPoint.targetUri).toBe('promotion/details/exclusion')

  });
});
