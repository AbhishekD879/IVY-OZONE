import { of } from 'rxjs';
import { DesktopHomeComponent } from './home.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { FANZONECONFIG, SITECORE_PROMOTION, TEAM_COLORS } from '@ladbrokesDesktop/bma/components/home/mockdata/home.component.mock';

describe('#DesktopHomeComponent', () => {
  let component: DesktopHomeComponent;
  let cms, dynamicComponentLoader, germanSupportService, pubSubService,userService,vanillaApiService,fanzoneHelperService,gtmService,changeDetectorRef, freeRideHelperService, bonusSuppressionService;
  const futureTimeStamp = ((new Date()).getTime() + 10000000000);
  const futureIsoTime = (new Date(futureTimeStamp)).toISOString();

  const sitecorePromotion = SITECORE_PROMOTION;
  const fanzoneConfig =FANZONECONFIG
  const statsDataMock = {
   
    getRibbonModule: [
      {
        directiveName: 'Featured',
        id: 'tab-featured',
        showTabOn: 'both',
        title: 'Featured',
        url: '/home/featured',
        visible: true
      },
      {
        directiveName: 'EventHub',
        id: 'tab-eventhub-4',
        showTabOn: 'both',
        displayFrom: '2019-02-18T13:12:01Z',
        displayTo: '2019-02-18T15:12:01Z',
        title: 'hub 4',
        url: '/home/eventhub/4',
        visible: true
      },
      {
        directiveName: 'EventHub',
        id: 'tab-eventhub-5',
        showTabOn: 'both',
        displayFrom: '2019-02-18T13:12:01Z',
        displayTo: futureIsoTime,
        title: 'hub 5',
        url: '/home/eventhub/5',
        visible: true
      }
    ] as any,
    getMMOutcomesByEventType: { },
    getSystemConfig: {
      moduleOrder: [
        ['yourCall', 80],
        ['featured', 60],
        ['nextRace', 40],
        ['inPlay', 22]
      ],
      DesktopHomePageOrder:{ nextRace: 40, featured: 60, inPlay: 22, yourCall: 80 },
      Fanzone: {
        enabled: true
      }
    } as any
  };
  const teamColors = TEAM_COLORS;

  beforeEach(() => {
    cms = {
      getRibbonModule: jasmine.createSpy('cms.getRibbonModule').and.returnValue(of(statsDataMock)),
      getToggleStatus: jasmine.createSpy('getToggleStatus').and.returnValue(of(true)),
      getFanzone: jasmine.createSpy('getFanzone').and.returnValue(of(fanzoneConfig)),
      getTeamsColors: jasmine.createSpy('getTeamsColors').and.returnValue(of(teamColors)),
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(of(
        statsDataMock.getSystemConfig
      ))
    } as any;
    dynamicComponentLoader = {};
    germanSupportService = {
      isGermanUser: jasmine.createSpy().and.returnValue(false)
    };
    userService = {

    }
    pubSubService = {
      API: pubSubApi,
      subscribe: jasmine.createSpy().and.callFake((p1, p2, cb) => {
        cb({data: [1]});
      }),
      unsubscribe: jasmine.createSpy('unsubscribe'),
    };
    userService = {
      username: 'abc'
    };
    vanillaApiService = {
      get: jasmine.createSpy('get').and.returnValue(of(sitecorePromotion))
    };
    fanzoneHelperService = {
      selectedFanzone: fanzoneConfig
    }
    gtmService = {
      push: jasmine.createSpy('push')
    };
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges'),
    };
    bonusSuppressionService = {

    };

    component = new DesktopHomeComponent(
      changeDetectorRef,
      cms,
      dynamicComponentLoader,
      germanSupportService,
      pubSubService,
      freeRideHelperService,
      userService,
      bonusSuppressionService
    );
  });

  describe('#ngOnInit', () => {
    it('ngOnInit', () => {
      spyOn(component, 'hideSpinner');
      cms.getRibbonModule.and.returnValue(of(statsDataMock));
      component.ngOnInit();
      expect(germanSupportService.isGermanUser).toHaveBeenCalledTimes(2);
      expect(component.isFanzoneEnabled).toBe(true);
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
      expect(pubSubService.subscribe).toHaveBeenCalledWith('HomeComponent',
      [
        pubSubService.API.SUCCESSFUL_LOGIN, pubSubService.API.SESSION_LOGIN,
        pubSubService.API.SESSION_LOGOUT],
        jasmine.any(Function));
    });
    it('should call getSystemConfig and set moduleorder', () => {
      cms.getRibbonModule.and.returnValue(of(statsDataMock));
      component.ngOnInit();
      expect(component.moduleOrder).toEqual(statsDataMock.getSystemConfig.moduleOrder);
    });
    it('should call getSystemConfig and empty DesktopHomePageOrder', () => {
      cms.getRibbonModule.and.returnValue(of(statsDataMock));
      const sysConfig = {
        moduleOrder: [
          ['yourCall', 80],
          ['featured', 60],
          ['nextRace', 40],
          ['inPlay', 22]
        ]
      };
      cms.getSystemConfig.and.returnValue(of(sysConfig));
      component.ngOnInit();
      expect(component.moduleOrder).not.toEqual(statsDataMock.getSystemConfig.moduleOrder);
    });
    it('should call getSystemConfig and empty config', () => {
      cms.getRibbonModule.and.returnValue(of(statsDataMock));
      cms.getSystemConfig.and.returnValue(of());
      component.ngOnInit();
      expect(component.moduleOrder).not.toEqual(statsDataMock.getSystemConfig.moduleOrder);
    });
  });
  
  it('ngOnDestroy', () => {
    component.ngOnDestroy();
    expect(pubSubService.unsubscribe).toHaveBeenCalledWith('HomeComponent');
  });
});

