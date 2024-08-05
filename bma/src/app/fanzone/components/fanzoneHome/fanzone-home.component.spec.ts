import { of, throwError } from 'rxjs';
import { FanzoneAppHomeComponent } from '@app/fanzone/components/fanzoneHome/fanzone-home.component';
import { NavigationEnd } from '@angular/router';
import { FANZONEDETAILS, FANZONEDETAILS_WITH_TAB_FALSE, FANZONETEASERDATA, FANZONETEASERDATA2, FANZONETEASEREMPTYDATA, TABS, TEAMDATA, COMMUNICATION_SETTINGS, COMMUNICATION_SETTINGS_ON } from '@app/fanzone/mockdata/fanzone-home.component.mock';
import { FANZONECONFIG } from '@app/fanzone/guards/mockdata/fanzone-auth-guardservice.mock';
import { pubSubApi } from '@app/core/services/communication/pubsub/pubsub-api.constant';
import { PreferenceCentre } from '@ladbrokesMobile/fanzone/components/fanzonePreferenceCentre/mockData/fanzone-preference-center.component.mock';

describe('FanzoneAppHomeComponent', () => {
  let component: FanzoneAppHomeComponent;

  let fanzoneModuleService;
  let cmsService;
  let navigationService;
  let dynamicComponentLoader;
  let routingState;
  let changeDetectorRef;
  let wsUpdateEventService;
  let templateService;
  let commentsService;
  let router;
  let route;
  let routeChangeListener;
  let fanzoneStorageService;
  let fanzoneHelperService;
  let device;
  let dialogService;
  let gtmService;
  let fanzoneSharedService;
  let user;
  let bonusSuppression;
  let fanzoneGamesService;
  let windowRefService;
  let pubsub;
  let pubsubReg;
  let storageService;
  let componentFactoryResolver;

  const fanzoneId = 'abc123';
  const tabs = TABS;
  const activeTab = {
    id: 'now-next',
    title: 'NOW & NEXT',
    url: '/fanzone/sport-football/$teamName/now-next',
    visible: true,
    showTabOn: 'both'
  };

  const activeTabClub = {
    id: 'club',
    title: 'CLUB',
    url: '/fanzone/club',
    visible: true,
    showTabOn: 'both'
  };

  const activeTabNowNext = {
    id: 'now-next',
    title: 'NOW & NEXT',
    url: '/fanzone/now-next',
    visible: true,
    showTabOn: 'both'
  };

  const createSpyWithReturnedObservable = (spyName: string, observableOf1?: any) => {
    return jasmine.createSpy(spyName)
      .and.returnValue(of(observableOf1 ? observableOf1 : null));
  };
  const fanzoneTeaserData = FANZONETEASERDATA;

  const fanzoneTeaserData2 = FANZONETEASERDATA2;

  const teamData = TEAMDATA;

  const teamDataWithImage = [{
    'primaryColour': "#D7191F",
    'secondaryColour': "#E8E8E8",
    'teamsImage': { 'filename': 'abc' }
  }];

  const fanzoneDetails = FANZONEDETAILS;
  const fanzoneDetailsWithTabFalse = FANZONEDETAILS_WITH_TAB_FALSE;
  const tagName = 'FanzoneAppHomeComponent';

  beforeEach(() => {
    cmsService = {
      getSystemConfig: jasmine.createSpy().and.returnValue(of({
        'Sport Quick Links': { enabled: true }
      })),
      getFanzone: createSpyWithReturnedObservable('getFanzoneDetails', fanzoneDetails),
      getTeamsColors: jasmine.createSpy().and.returnValue(of(teamData)),
      getFanzonePreferences: createSpyWithReturnedObservable('getFanzonePreferences', [PreferenceCentre])
    } as any;
    navigationService = {};
    dynamicComponentLoader = {};
    routingState = {
      getPreviousUrl: jasmine.createSpy('getPreviousUrl')
    };
    pubsubReg = {};
    pubsub = {
      publish: jasmine.createSpy().and.callFake( (channel) => pubsubReg[channel] && pubsubReg[channel]() ),
      API: pubSubApi,
      subscribe: jasmine.createSpy().and.callFake((domain, channel, fn) => { pubsubReg[channel] = fn; }),
      unsubscribe: jasmine.createSpy('unsubscribe')
    };
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges'),
    };
    wsUpdateEventService = {
      subscribe: jasmine.createSpy('subscribe')
    };
    templateService = {
      setCorrectPriceType: jasmine.createSpy()
    };
    commentsService = {};
    fanzoneModuleService = {
      getFanzoneImagesFromSiteCore: createSpyWithReturnedObservable('getFanzoneImagesFromSiteCore', fanzoneTeaserData),
      createTab: jasmine.createSpy().and.returnValue({
        title: 'NOW & NEXT',
        id: 'now-next',
        url: '/fanzone/sport-football/$teamName/now-next',
        visible: true,
        showTabOn: 'both'
      }),
    };

    router = {
      events: {
        subscribe: jasmine.createSpy('subscribe').and.callFake((cb) => {
          routeChangeListener = cb;
        })
      },
      navigate: jasmine.createSpy('navigate'),
      navigateByUrl: jasmine.createSpy('navigateByUrl'),
      url: '/fanzone/sport-football/$teamName/now-next'
    } as any;

    route = {
    } as any;

    fanzoneStorageService = {
      get: jasmine.createSpy('get').and.returnValue({ teamName: 'Manchester' }),
      set: jasmine.createSpy('set')
    };
    fanzoneHelperService = {
      selectedFanzone: FANZONECONFIG,
    };
    fanzoneSharedService = {
      showNotifications: jasmine.createSpy('showNotifications'),
      pushCachedEvents: jasmine.createSpy('pushCachedEvents'),
      getFanzoneNewSignPosting: jasmine.createSpy('getFanzoneNewSignPosting').and.returnValue(of([])),
      showGamesPopup: jasmine.createSpy('showGamesPopup'),
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(of({fanzoneGamesTooltip:{Delay: 10,
        Message: 'fanzone games is newly added',
        Enable: true
      }})),
      showFanzoneGamesPopup: jasmine.createSpy('showFanzoneGamesPopup').and.returnValue(of({})),
      postEmailOptinDetails: jasmine.createSpy('postEmailOptinDetails').and.returnValue(of({})),
      getUserCommunicationSettings: jasmine.createSpy('getUserCommunicationSettings').and.returnValue(of({})),
      isIosBlackListedDevice: jasmine.createSpy('isIosBlackListedDevice').and.returnValue(of(true))
    };
    dialogService = jasmine.createSpyObj('dialogService', ['openDialog']);
    device = {
      isIos: false,
      isAndroid: false,
      isMobile: true,
      isTablet: false
    };
    gtmService = {
      push: jasmine.createSpy('push')
    };
    user = {
      checkIfYellowFlagDisabled: jasmine.createSpy('checkIfYellowFlagDisabled').and.returnValue(true),
      bonusSuppression: false
    },
    bonusSuppression = {
      checkIfYellowFlagDisabled: jasmine.createSpy('checkIfYellowFlagDisabled').and.returnValue(true)
    };
    fanzoneGamesService = {
      getNewFanzoneGamesPopupSeen: jasmine.createSpy('getNewFanzoneGamesPopupSeen').and.returnValue(false),
      showNewSignPostingIcon: jasmine.createSpy('showNewSignPostingIcon').and.returnValue(false),
      showFanzoneGamesTooltip: jasmine.createSpy('showFanzoneGamesTooltip').and.returnValue(false),
      setFanzoneGamesTooltipSeen: jasmine.createSpy('setFanzoneGamesTooltipSeen')
    };
    windowRefService = {
      nativeWindow: {
        setTimeout: jasmine.createSpy('setTimeout').and.callFake(fn => fn()),
        clearTimeout: jasmine.createSpy('clearTimeout')  
      },
      document: {
        querySelector: jasmine.createSpy('querySelector'),
        querySelectorAll: jasmine.createSpy('querySelectorAll')
      },
    };
    componentFactoryResolver = {
      resolveComponentFactory: jasmine.createSpy('resolveComponentFactory')
    };
    component = new FanzoneAppHomeComponent(cmsService, navigationService, dynamicComponentLoader,
      routingState, fanzoneModuleService, pubsub, changeDetectorRef, wsUpdateEventService,
      templateService, commentsService, router, route, fanzoneStorageService, fanzoneHelperService, fanzoneSharedService, gtmService, device, user, bonusSuppression, dialogService, componentFactoryResolver, fanzoneGamesService, windowRefService, storageService);
  });


  describe('#mainInit', () => {
    it('Should subscribe to FANZONE_DATA and update content', () => {
      pubsub.subscribe = jasmine.createSpy('subscribe')
        .and.callFake((fileName: string, method: string | string[], callback: Function) => {
          if (method === pubsub.API.FANZONE_DATA) {
            spyOn(component, <any>'init');
            callback();
            expect(component['init']).toHaveBeenCalled();
          }
        });
      component.ngOnInit();
    });

    it('Should subscribe to FANZONE_SHOW_GAMES_TAB and navigate to games tab', () => {
      pubsub.subscribe = jasmine.createSpy('subscribe')
        .and.callFake((fileName: string, method: string | string[], callback: Function) => {
          if (method === pubsub.API.FANZONE_SHOW_GAMES_TAB) {
            component.fanzoneTabs = [{
              title: 'Games',
              id: 'games',
              url: '/fanzone/sport-football/$teamName/games',
              visible: true,
              showTabOn: 'both'
            }];
            callback();
            expect(component.activeTab).toBe(component.fanzoneTabs[0]);
            expect(router.navigateByUrl).toHaveBeenCalledWith(component.fanzoneTabs[0].url);
          }
        });
      component.ngOnInit();
    });

    it('Should subscribe to FANZONE_SHOW_GAMES_TOOLTIP and navigate to games tab', () => {
      pubsub.subscribe = jasmine.createSpy('subscribe')
        .and.callFake((fileName: string, method: string | string[], callback: Function) => {
          if (method === pubsub.API.FANZONE_SHOW_GAMES_TOOLTIP) {
            spyOn(component, <any>'showFanzoneGamesTooltip');
            callback();
            expect(component['showFanzoneGamesTooltip']).toHaveBeenCalled();
          }
        });
      component.ngOnInit();
    });

    it('openFanzoneOptinEmailDialog when emails are not selected', () => {
      fanzoneSharedService.getUserCommunicationSettings = jasmine.createSpy('getUserCommunicationSettings').and.returnValue(of(COMMUNICATION_SETTINGS));
      dialogService.openDialog = jasmine.createSpy('openDialog');
      component['openFanzoneOptinEmailDialog']({description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit"
        ,id: "643f90b9c2d47d05a65ba7fb", playCTA: "Play", title: "Fanzone Games"});
      expect(dialogService.openDialog).toHaveBeenCalled();
    });

    it('openFanzoneOptinEmailDialog when emails are selected', () => {
      fanzoneSharedService.getUserCommunicationSettings = jasmine.createSpy('getUserCommunicationSettings').and.returnValue(of(COMMUNICATION_SETTINGS_ON));      
      component['openFanzoneOptinEmailDialog']({description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit"
        ,id: "643f90b9c2d47d05a65ba7fb", playCTA: "Play", title: "Fanzone Games"});
      expect(fanzoneSharedService.showFanzoneGamesPopup).toHaveBeenCalled();
      expect(fanzoneSharedService.postEmailOptinDetails).toHaveBeenCalled();
    });

    it('should set component fanzoneTabs property', () => {
      component.ngOnInit();

      expect(component.fanzoneTeam).toEqual({ teamName: 'Manchester' });
      expect(component.fanzoneTabs).toEqual(tabs);
      expect(component.fanzoneName).toEqual('Manchester');
      expect(component.fanzoneDesc).toEqual('Goodison Park, Liverpool');
      expect(component.fanzoneBannerImage).toEqual('https://scmedia.cms.test.env.works/$-$/576b7e3d75394650b21d13f3bdc17a50.jpg');
      expect(component.teamData).toEqual(teamData[0]);
    });

    it('filterIOSAppVersion', () => {
      component.fanzoneTabs.pop = jasmine.createSpy('fanzoneTabs.pop');
      component['filterIOSAppVersion']();
      expect(pubsub.publish).toHaveBeenCalledWith(pubsub.API.HIDE_FANZONE_GAMES_TAB);
      expect(component.fanzoneTabs.pop).toHaveBeenCalled();
    });

    it('should set fanzoneBannerImage when device is not mobile', () => {
      device.isMobile = false;
      component.ngOnInit();

      expect(component.fanzoneBannerImage).toEqual('');
    });

    it('should subscribe to changes on ngOnInit and update activeTab as club', () => {
      component.fanzoneTabs = [{
        "title": "CLUB",
        "visible": true,
        "id": "club",
        "url": "/fanzone/club",
        "showTabOn": "both",
      }];
      router.url = 'fanzone/club';

      router.events = of(new NavigationEnd(0, '/fanzone/club', '/fanzone/club'));
      component['getFanzoneInitData'] = jasmine.createSpy();
      component.ngOnInit();

      expect(component.activeTab).toEqual(activeTabClub);
      expect(component['getFanzoneInitData']).toHaveBeenCalled();
    });

    it('should set now & next tab as default tab if we did not find the other tabs', () => {
      component.fanzoneTabs = [{
        id: 'now-next',
        title: 'NOW & NEXT',
        url: '/fanzone/now-next',
        visible: true,
        showTabOn: 'both'
      }];
      router.url = 'fanzone/stats';

      router.events = of(new NavigationEnd(0, '/fanzone/stats', '/fanzone/stats'));
      component['getFanzoneInitData'] = jasmine.createSpy();
      component['goToDefaultPage'] = jasmine.createSpy();
      
      component.ngOnInit();

      expect(component.activeTab).toEqual(activeTabNowNext);
      expect(component['getFanzoneInitData']).toHaveBeenCalled();
      expect(component['goToDefaultPage']).toHaveBeenCalled();
    });

    it('should subscribe to changes on ngOnInit and update activeTab as now-next as default ', () => {
      component.fanzoneTabs = [{
        "title": "NOW & NEXT",
        "visible": true,
        "id": "now-next",
        "url": "/fanzone/now-next",
        "showTabOn": "both",
      },]
      router.events = of(new NavigationEnd(0, '/fanzone/now-next', '/fanzone/now-next'));
      component['getFanzoneInitData'] = jasmine.createSpy();
      spyOn(component, <any>'checkNewSignPostingIcon');
      component.ngOnInit();

      expect(component.activeTab).toEqual(activeTabNowNext);
      expect(component['getFanzoneInitData']).toHaveBeenCalled();
      expect(component['checkNewSignPostingIcon']).toHaveBeenCalled();
    });

    it('sitecore fanzone should be empty if response is not empty but no teasers data ', () => {
      fanzoneModuleService.getFanzoneImagesFromSiteCore = createSpyWithReturnedObservable('getFanzoneImagesFromSiteCore', FANZONETEASEREMPTYDATA);
      component.ngOnInit();

      expect(component.siteCoreFanzone).toEqual([]);
    });

    it('should handle if teasers call return error response', () => {
      fanzoneModuleService.getFanzoneImagesFromSiteCore = jasmine.createSpy().and.returnValue(throwError({ status: 404 }));
      component.ngOnInit();

      expect(component.fanzoneBannerImage).toEqual('');
      expect(component.state.error).toBeTrue;
    });

    it('should handle if asset managment return error response', () => {
      const err = { mess: 'error', type: 'any' };
      cmsService.getTeamsColors = jasmine.createSpy().and.returnValue(throwError({ status: 404 }));
      component.ngOnInit();

      expect(component.teamData).toBeUndefined();
      expect(component.state.error).toBeTrue;
    });

    it('should open notifications popup/ navigate to preference center', () => {
      fanzoneSharedService.showNotifications = jasmine.createSpy('fanzoneSharedService.showNotifications');
      component.showNotification();
      expect(fanzoneSharedService.showNotifications).toHaveBeenCalled();
    });

    it('should return true if teamData exist', () => {
      component.ngOnInit();
      const isTeamExist = component.checkForTeamsExist();

      expect(isTeamExist).toEqual(true);
    });

    it('#ngOnDestroy routeChangeListener', () => {
      component['routeChangeListener'] = <any>{
        unsubscribe: jasmine.createSpy('unsubscribe')
      };
      component.ngOnDestroy();
      expect(component['routeChangeListener'].unsubscribe).toHaveBeenCalled();
      expect(pubsub.unsubscribe).toHaveBeenCalledWith(tagName);
      expect(windowRefService.nativeWindow.clearTimeout).toHaveBeenCalled();
    });

    it('#goToDefaultPage', () => {
      component.fanzoneTeam = {
        teamName: 'manchester'
      }
      component.goToDefaultPage();
      expect(router.navigateByUrl).toHaveBeenCalledWith('/fanzone/sport-football/manchester/now-next');
    });
  });

  describe('showFanzoneGamesTooltip', () => {
    it('should see the fanzone games tooltip if user visited fanzone games first time', () => {
      windowRefService.nativeWindow.setTimeout = jasmine.createSpy('setTimeout');
      fanzoneGamesService.showFanzoneGamesTooltip.and.returnValue(true);
      spyOn(component, 'positionTooltip');
      component['showFanzoneGamesTooltip']();
      expect(component.positionTooltip).toHaveBeenCalled();
      expect(component.toolTipArgs.show).toBeTruthy();
      expect(windowRefService.nativeWindow.setTimeout).toHaveBeenCalledTimes(1);
    });

    it('should see the fanzone games tooltip if user visited fanzone games first time and hide automatically after sometime', () => {
      fanzoneGamesService.showFanzoneGamesTooltip.and.returnValue(true);
      spyOn(component, 'positionTooltip');
      component['showFanzoneGamesTooltip']();
      expect(component.positionTooltip).toHaveBeenCalled();
      expect(component.toolTipArgs.show).toBeFalsy();
      expect(windowRefService.nativeWindow.setTimeout).toHaveBeenCalledTimes(1);
      expect(fanzoneGamesService.setFanzoneGamesTooltipSeen).toHaveBeenCalled();
    });

    it('should not see fanzone games tooltip if user already visited fanzone games tab', () => {
      fanzoneGamesService.showFanzoneGamesTooltip.and.returnValue(false);
      spyOn(component, 'positionTooltip');
      component['showFanzoneGamesTooltip']();
      expect(component.positionTooltip).not.toHaveBeenCalled();
      expect(component.toolTipArgs.show).toBeFalsy();
    });

    it('should not see fanzone games tooltip if games tooltip config is disabled', () => {
      fanzoneSharedService.getSystemConfig.and.returnValue(of({
          fanzoneGamesTooltip:{
            Delay: 10,
            Message: 'fanzone games is newly added',
            Enable: false
          }
      }));
      component['showFanzoneGamesTooltip']();
      expect(component.toolTipArgs.show).toBeFalsy();
    });

    it('should not see fanzone games tooltip if games tooltip config is not added in CMS systemconfig', () => {
      fanzoneSharedService.getSystemConfig.and.returnValue(of({}));
      component['showFanzoneGamesTooltip']();
      expect(component.toolTipArgs).toBeUndefined();
    });
  });

  describe('checkNewSignPostingIcon', () => {
    it('should see the new signposting if user visited first time', () => {
      fanzoneGamesService.showFanzoneGamesTooltip.and.returnValue(true);
      component.fanzoneTabs = [{
        "title": "Games",
        "visible": true,
        "id": "games",
        "url": "/fanzone/games",
        "showTabOn": "both"
      }];
      fanzoneGamesService.showNewSignPostingIcon.and.returnValue(true);
      component['checkNewSignPostingIcon']();
      expect(component.fanzoneTabs[0].newSignPostingIcon).toBeTruthy();
    });
  });

  describe('getFanzoneInitData', () => {
    it('should get the fanzone new signposting data before loading the fanzone tabs in case of showGames config is true', () => {
      spyOn(component, 'getFanzoneGamesData');
      fanzoneGamesService.showNewSignPostingIcon.and.returnValue(true);
      component['openFanzoneOptinEmailDialog'] = jasmine.createSpy();
      component.getFanzoneInitData(FANZONEDETAILS);
      expect(component.getFanzoneGamesData).toHaveBeenCalled();
      expect(component['openFanzoneOptinEmailDialog']).toHaveBeenCalled();
    });

    it('should not get the fanzone new signposting data before loading the fanzone tabs in case of showGames config is false', () => {
      spyOn(component, 'getFanzoneGamesData');
      spyOn(component, 'getFanzoneTabsData');
      fanzoneGamesService.showNewSignPostingIcon.and.returnValue(true);
      FANZONEDETAILS.fanzoneConfiguration.showGames = false;
      component.getFanzoneInitData(FANZONEDETAILS);
      expect(component.getFanzoneGamesData).not.toHaveBeenCalled();
    });
  });

  describe('getFanzoneGamesData', () => {
    it('should get the fanzone new signposting data before loading the fanzone tabs in case of showGames config is true', () => {
      spyOn(component, 'getFanzoneTabsData');
      fanzoneSharedService.getFanzoneNewSignPosting.and.returnValue(of([{startDate:'', endDate:''}]));
      component.getFanzoneGamesData(FANZONEDETAILS);
      expect(component.newSignPostingData).toBeDefined();
      expect(component.getFanzoneTabsData).toHaveBeenCalled();
    });
  });

  describe('positionTooltip', () => {
    it('should place the tooltip in correct position', () => {
      component.fanzoneTabs = [{}] as any;
      windowRefService.document.querySelector.and.returnValue({style:{},clientHeight: '100', clientWidth: '150'});
      windowRefService.document.querySelectorAll.and.returnValue([{style:{},clientHeight: '100', clientWidth: '150'}]);
      component.positionTooltip();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
  });
});
