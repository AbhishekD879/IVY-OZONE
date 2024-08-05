import { of, throwError } from 'rxjs';
import * as _ from 'underscore';

import {
  featuredModuleMock,
  featuredQuickLinksMock,
  eventMock,
  featuredDataMock,
  featuredQuickLinksDataMock,
  featuredInplayModuleMock,
  featuredModuledataMock,
  footballEventMock,
  badmintonEventMock,
  surfaceBetModule,
  badmintonInplayModuleMock,
  cleanModuleMock
} from './featured-module.component.mock';

import { FeaturedModuleComponent } from './featured-module.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { IOutputModule } from '@featured/models/output-module.model';
import { PERFORMANCE_API_MARK } from '@app/lazy-modules/performanceMark/enums/performance-mark.enums';

describe('FeaturedModuleComponent', () => {
  let component: FeaturedModuleComponent;

  let locale;
  let filtersService;
  let windowRef;
  let pubsub;
  let featuredModuleService;
  let templateService;
  let commentsService;
  let wsUpdateEventService;
  let sportEventHelper;
  let cmsService;
  let promotionsService;
  let changeDetectorRef;
  let router;
  let gtmService;
  let routingHelperService;
  let awsService;
  let userService;
  let eventService;
  let virtualSharedService;
  let bonusSuppressionService;
  let ngZone;
  let deviceService;
  let storage;
  beforeEach(() => {
    locale = {
      getString: jasmine.createSpy().and.returnValue('tranlation')
    };

    bonusSuppressionService = {
      checkIfYellowFlagDisabled: jasmine.createSpy('checkIfYellowFlagDisabled').and.returnValue(false)
    };

    filtersService = {
      orderBy: jasmine.createSpy('orderBy').and.callFake((args) => args)
    };
    storage = {
      get: jasmine.createSpy('get'),
      set: jasmine.createSpy('set')
    };
    windowRef = {
      nativeWindow: {
        view: {mobile: true},
        setInterval: jasmine.createSpy('setInterval').and.callFake(cb => cb()),
        clearInterval: jasmine.createSpy(),
        setTimeout: jasmine.createSpy().and.callFake(cb => cb && cb())
      }
    };
    pubsub = {
      cbMap: {},
      publish: jasmine.createSpy('publish'),
      subscribe: jasmine.createSpy('subscribe').and.callFake((name, method, cb) => pubsub.cbMap[method] = cb),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: pubSubApi
    };
    ngZone = {
      runOutsideAngular: jasmine.createSpy().and.callFake(fn => fn())
    };
    featuredModuleService = {
      addEventListener: jasmine.createSpy(),
      reconnect: jasmine.createSpy(),
      startConnection: jasmine.createSpy(),
      onError: jasmine.createSpy(),
      clearSubscribedFeaturedTabModules: jasmine.createSpy(),
      disconnect: jasmine.createSpy(),
      cacheEvents: jasmine.createSpy(),
      addModuleToSubscribedFeaturedTabModules: jasmine.createSpy(),
      tabModuleStates: new Map(),
      emit: jasmine.createSpy(),
      addClock: jasmine.createSpy().and.callFake((args) => args),
      getSubscribedFeaturedTabModules: jasmine.createSpy().and.returnValue(['1', '2', '3']),
      removeAllListeners: jasmine.createSpy(),
      removeEventListener: jasmine.createSpy(),
      trackDataReceived: jasmine.createSpy('trackDataReceived'),
      segmentReceivedListner: jasmine.createSpy('segmentReceivedListner'),
      checkEventModuleAndReturnValue: jasmine.createSpy('checkEventModuleAndReturnValue').and.returnValue('5b759926c9e77c000163eede'),
      createSocket: jasmine.createSpy('createSocket'),
    };
    templateService = {
      setCorrectPriceType: jasmine.createSpy()
    };
    commentsService = {
      badmintonMSInitParse: jasmine.createSpy()
    };
    wsUpdateEventService = {
      subscribe: jasmine.createSpy()
    };
    sportEventHelper = {
      isSpecialEvent: jasmine.createSpy().and.returnValue(true)
    };
    cmsService = {
      getSystemConfig: jasmine.createSpy().and.returnValue(of({
        YourCallIconsAndTabs: {
          enableIcon: true
        },
        'Highlight Carousel': {
          enabled: true
        },
        'Inplay Module': {
          enabled: true
        },
        'Sport Quick Links': {enabled: true},
        'Fanzone' : {enabled: true},
        'BetPack': {
          enableBetPack: true
        },
        'UseFSCCached': {
          enabled: true
        },
        'gamingEnabled': {
          enabled: true, iosVersionBlackList: ['7.7-16']
        }
      })),
      getRibbonModule: jasmine.createSpy().and.returnValue(of({
        getRibbonModule: [{ url: 'link1' }, { url: '/' }, { url: 'link2' }]
      })),
      getCMSRGYconfigData: jasmine.createSpy().and.returnValue(of({})),
      getFSC: jasmine.createSpy().and.returnValue(of({
        directiveName: 'test',
        modules: [] as any,
        showTabOn: 'test2',
        title: 'tst',
        visible: true,
        segmented: true
      }))
    };

    router = { navigateByUrl: jasmine.createSpy() };
    gtmService = { push: jasmine.createSpy() };
    routingHelperService = {
      formSportUrl: jasmine.createSpy().and.callFake(name => of(`/${name}`)),
      getPreviousSegment: jasmine.createSpy().and.returnValue('')
    };
    promotionsService = {
      openPromotionDialog: jasmine.createSpy()
    };

    changeDetectorRef = {
      detach: jasmine.createSpy('detach'),
      detectChanges: jasmine.createSpy('detectChanges'),
      markForCheck: jasmine.createSpy('markForCheck')
    };

    awsService = {
      addAction: jasmine.createSpy()
    };
    userService = {username: 'test-user', status: false};
    eventService = {
      isUKorIRE: jasmine.createSpy('isUKorIRE').and.returnValue(true)
    };

    virtualSharedService = {
      isVirtual: jasmine.createSpy('isVirtual'),
      formVirtualTypeUrl: jasmine.createSpy('formVirtualTypeUrl')
    };
    deviceService = {
      isIos: true
    };

    component = new FeaturedModuleComponent(
      locale,
      filtersService,
      windowRef,
      pubsub,
      featuredModuleService,
      templateService,
      commentsService,
      wsUpdateEventService,
      sportEventHelper,
      cmsService,
      promotionsService,
      changeDetectorRef,
      routingHelperService,
      router,
      gtmService,
      awsService,
      userService,
      eventService,
      virtualSharedService,
      bonusSuppressionService,
      deviceService,
      storage
    );

    component['sysConfigSubscription'] = { unsubscribe: jasmine.createSpy('sysConfigSubsciption.unsubsctibe')  } as any;

    component.featuredModuleData = {
      directiveName: null,
      modules: [],
      showTabOn: null,
      title: null,
      visible: null
    };
  });

  it('needed constructor methods', () => {
    component['featureTabOnSocketUpdate'] = jasmine.createSpy();
    component['onSocketUpdate'](featuredModuleMock);

    expect(component['featureTabOnSocketUpdate']).toHaveBeenCalledWith(featuredModuleMock as any);
  });

  describe('ngOnInit', () => {
    it('should init connection during sport initialisation', () => {
      const sportIdMock = 10;
      component.sportId = sportIdMock;
      spyOn<any>(component, 'trackErrorMessage');

      component['featuredModuleService'].onError = jasmine.createSpy('onError').and.callFake((callback) => {
        callback();
        expect(component.ssDown).toBeTruthy();
        expect(component.featuredModuleData).toBeDefined();
        expect(component.showLoader).toBeFalsy();
      });
      component['pubsub'].subscribe = jasmine.createSpy('subscribe').and.callFake((namespace, message, callback) => {
        if (message === 'FEATURED_CONNECT_STATUS') {
          component['featuredModuleService'].addEventListener = jasmine.createSpy('addEventListener')
            .and.callFake((messageText, callbackFn) => {
              if (messageText === 'FEATURED_STRUCTURE_CHANGED') {
                callbackFn(Object.assign({}, featuredDataMock));
                expect(pubsub.publish).toHaveBeenCalledWith(pubsub.API.FEATURED_STRUCTURE_CHANGED, []);
              }
            });

          callback(false);
          expect(component['featuredModuleService'].addEventListener)
            .not.toHaveBeenCalled();

          callback(true);
          expect(component.showLoader).toBeFalsy();
          expect(component.isConnectSucceed).toBeTruthy();
          expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
          expect(component['featuredModuleService'].addEventListener)
            .toHaveBeenCalledWith('FEATURED_STRUCTURE_CHANGED', jasmine.any(Function));

          expect(component['trackErrorMessage']).toHaveBeenCalled();
        }
      });

      component['pubsub'].subscribe = jasmine.createSpy('subscribe').and.callFake((namespace, message, callback) => {
        callback();
        expect(component.showLoader).toBeFalsy();
        expect(component.ssDown).toBeTruthy();
        expect(component['trackErrorMessage']).toHaveBeenCalled();
      });


      component['featuredModuleService'].onError = jasmine.createSpy('onError').and.callFake((callback) => {
        callback();
        expect(component.ssDown).toBeTruthy();
        expect(component.featuredModuleData).toBeDefined();
        expect(component.showLoader).toBeFalsy();
        expect(component['trackErrorMessage']).toHaveBeenCalled();
      });
      component['pubsub'].subscribe = jasmine.createSpy('subscribe').and.callFake((namespace, message, callback) => {
        if (message[0] && message[0] === 'RELOAD_FEATURED') {
          callback();
          expect(featuredModuleService.reconnect).toHaveBeenCalled();
          expect(component.showLoader).toBeTruthy();
          expect(component.isConnectSucceed).toBeTruthy();
          expect(component.ssDown).toBeFalsy();
        }

        if (message === 'FEATURED_CONNECT_STATUS') {
          component['featuredModuleService'].addEventListener = jasmine.createSpy('addEventListener')
            .and.callFake((messageText, callbackFn) => {
              if (messageText === 'FEATURED_STRUCTURE_CHANGED') {
                callbackFn(Object.assign({}, featuredDataMock));
                expect(pubsub.publish).toHaveBeenCalledWith(pubsub.API.FEATURED_STRUCTURE_CHANGED, []);
              }
            });

          callback(false);
          expect(component['featuredModuleService'].addEventListener)
            .not.toHaveBeenCalled();

          callback(true);
          expect(component.showLoader).toBeFalsy();
          expect(component.isConnectSucceed).toBeTruthy();
          expect(component['featuredModuleService'].addEventListener)
            .toHaveBeenCalledWith('FEATURED_STRUCTURE_CHANGED', jasmine.any(Function));
        }

        if (message === 'NAMESPACE_ERROR') {
            callback();
            expect(featuredModuleService.startConnection).toHaveBeenCalledWith(sportIdMock, 'sport');
            expect(component.showLoader).toBeFalsy();
            expect(component.ssDown).toBeTruthy();
        }

        if (message[0] === pubsub.API.SESSION_LOGIN) {
          callback();
          expect(bonusSuppressionService.checkIfYellowFlagDisabled).toHaveBeenCalled();
        }
      });
      component.ngOnInit();

      expect(component.isHighlightCarouselEnabled).toBe(true);
      expect(component.isInplayModuleEnabled).toBe(true);
    });

    it('Should subscribe to APP_BUILD_VERSION and update showRpg method', () => {
      cmsService.getSystemConfig = jasmine.createSpy().and.returnValue(of({
        YourCallIconsAndTabs: {
          enableIcon: true
        },
        'Highlight Carousel': {
          enabled: true
        },
        'Inplay Module': {
          enabled: true
        },
        'Sport Quick Links': {enabled: true},
        'Fanzone' : {enabled: false},
        'GamingEnabled': {
          enabled: true, iosVersionBlackList: ['7.7-16']
        }
      }))
      component.appMenuProperties.iosVersionBlackList = ['7.7-16'] as any;
      const outputModule = { '@type': 'RecentlyPlayedGameModule' } as any;
      deviceService.isWrapper = true;
      pubsub.subscribe.and.callFake((featuredmodule, listeners, handler) => {
        if (listeners == 'APP_BUILD_VERSION') {
          handler('7.7-16');
        }
      });
      component.ngOnInit();
      expect(storage.set).toHaveBeenCalledWith('appBuildVersion', '7.7-16');
      expect(deviceService.isIos).toBeTruthy();
      expect(component['isDisplayRpg']).toBeFalsy();
      expect(component.showRpg(outputModule)).toBeFalsy();
    });
    it('Should get appbuildversion from storage', () => {
      cmsService.getSystemConfig = jasmine.createSpy().and.returnValue(of({
        YourCallIconsAndTabs: {
          enableIcon: true
        },
        'Highlight Carousel': {
          enabled: true
        },
        'Inplay Module': {
          enabled: true
        },
        'Sport Quick Links': {enabled: true},
        'Fanzone' : {enabled: false},
        'GamingEnabled': {
          enabled: true, iosVersionBlackList: ['7.7-16']
        }
      }))
      storage.get = jasmine.createSpy('storage.get').and.returnValue('7.7-16')

      component.appMenuProperties.iosVersionBlackList = ['7.7-16'] as any;
      const outputModule = { '@type': 'RecentlyPlayedGameModule' } as any;
      deviceService.isWrapper = true;

      component.ngOnInit();
      expect(storage.get).toHaveBeenCalledWith('appBuildVersion')
      expect(deviceService.isIos).toBeTruthy();
      expect(component['isDisplayRpg']).toBeFalsy();
      expect(component.showRpg(outputModule)).toBeFalsy();
    });

    const featured = {
      directiveName: 'test',
      modules: [] as any,
      showTabOn: 'test1',
      title: 'test2',
      visible: true,
      segmented: true
    } as any;
    const connectionNameSpaceId = null;
    let connectionType: 'test'



    it('should return readFSCFromCF as true', () => {
      component.readFSCFromCF = true;
      performance.mark(PERFORMANCE_API_MARK.CTI);
      component.isConnectSucceed = true;
      component['processFSCContent'](featured, connectionNameSpaceId, connectionType);
      component.ngOnInit();
      expect(component.readFSCFromCF).toBe(true);
    })

    it('should return error for readFSCFromCF', () => {
      performance.mark(PERFORMANCE_API_MARK.CTI);
      component.isConnectSucceed = true;
      component.readFSCFromCF = false;
      cmsService.getFSC = jasmine.createSpy().and.returnValue(throwError({}));
      component.ngOnInit();
      expect(component.readFSCFromCF).toBe(true);
    })

    it('should set isFanzoneConfigEnabled as false', () => {
      cmsService.getSystemConfig = jasmine.createSpy().and.returnValue(of({
        YourCallIconsAndTabs: {
          enableIcon: true
        },
        'Highlight Carousel': {
          enabled: true
        },
        'Inplay Module': {
          enabled: true
        },
        'Sport Quick Links': {enabled: true},
        'Fanzone' : {enabled: false}
      })),
      component.ngOnInit();

      expect(component.isFanzoneConfigEnabled).toBe(false);
    })

    it('should set isBetpackConfigEnabled as false', () => {
      cmsService.getSystemConfig = jasmine.createSpy().and.returnValue(of({
        YourCallIconsAndTabs: {
          enableIcon: true
        },
        'Highlight Carousel': {
          enabled: true
        },
        'Inplay Module': {
          enabled: true
        },
        'Sport Quick Links': {enabled: true},
        'Fanzone' : {enabled: false},
        'BetPack': {
          enableBetPack: false
        }
      })),
      component.ngOnInit();
      expect(component.isBetpackConfigEnabled).toBe(false);
    })

    it('should set readFSCFromCF as false', () => {
      cmsService.getSystemConfig = jasmine.createSpy().and.returnValue(of({
          YourCallIconsAndTabs: {
            enableIcon: true
          },
          'Highlight Carousel': {
            enabled: true
          },
          'Inplay Module': {
            enabled: true
          },
          'Sport Quick Links': {enabled: true},
          'Fanzone' : {enabled: true},
          'BetPack': {
            enableBetPack: true
          },
          'UseFSCCached': {
            enabled: false
          }
      })),
      component.ngOnInit();
      expect(component.readFSCFromCF).toBe(false);
    })


    it('should show betpack banner', () => {
      component.ngOnInit();
      expect(component.betpackBanner).toBe(true);
    });

    it('should not show betpack banner in case of rgy user', () => {
      userService.status = true;
      component.ngOnInit();
      expect(component.betpackBanner).toBe(false);
    });

    it(`should subscribe on SESSION_LOGIN`, () => {
      component.ngOnInit();
      expect(pubsub.subscribe).toHaveBeenCalledWith('featuredModule', [pubsub.API.SESSION_LOGIN, pubsub.API.SUCCESSFUL_LOGIN], jasmine.any(Function));
      changeDetectorRef.detectChanges.calls.reset();
      pubsub.cbMap['WS_EVENT_UPDATED']();

      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it(`should subscribe on WS_EVENT_UPDATED`, () => {
      component.ngOnInit();

      expect(pubsub.subscribe).toHaveBeenCalledWith('featuredModule', 'WS_EVENT_UPDATED', jasmine.any(Function));

      changeDetectorRef.detectChanges.calls.reset();
      pubsub.cbMap['WS_EVENT_UPDATED']();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it(`should subscribe on WS_EVENT_UPDATE`, () => {
      component.ngOnInit();

      expect(pubsub.subscribe).toHaveBeenCalledWith('featuredModuleEventHub', 'WS_EVENT_UPDATE', jasmine.any(Function));

      changeDetectorRef.detectChanges.calls.reset();
      pubsub.cbMap['WS_EVENT_UPDATE']();

      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it(' should init connection during eventhub initialisation', () => {
      const hubIndexMock = 1;
      component.hubIndex = hubIndexMock;
      component.ngOnInit();

      expect(featuredModuleService.startConnection).toHaveBeenCalledWith(hubIndexMock, 'eventhub');
    });

    it('should detectChanges', () => {
      component.ngOnInit();

      expect(component['changeDetectorRef'].markForCheck).toHaveBeenCalled();
    });

    it('trackByModuleData', () => {
      const event = { id: '1', name: 'test event', startTime: 'Friday, 13th' } as any;
      const result = component.trackByModuleData(3, event);

      expect(result).toBe('3_1_test event_Friday, 13th');
    });

    it('trackByModules', () => {
      expect(component.trackByModules(0, <any>featuredModuleMock)).toEqual(
        `0_5b759926c9e77c000163eede_HO Football_-2`
      );
    });

    it('trackByModules for QL', () => {
      expect(component.trackByModules(0, <any>featuredQuickLinksMock)).toEqual(
        `0_featuredQuickLinksModuleId`
      );
    });

    it('trackByModules for Horce Race', () => {
      expect(
        component.trackByModules(0, {
          _id: '5b759924x77c000163eede',
          '@type': 'EventsModule',
          dataSelection: {selectionType: 'RaceTypeId'}
        } as any)
      ).toEqual(
        `0_5b759924x77c000163eede`
      );
    });

    it('trackByModules for module created by market id', () => {
      expect(
        component.trackByModules(0, {
          _id: '5b759924x77c500163eede',
          '@type': 'EventsModule',
          dataSelection: {selectionType: 'Market'}
        } as any)
      ).toEqual(
        `0_5b759924x77c500163eede`
      );
    });

    it('check getEventType is special', () => {
      const result = component.getEventType(eventMock);

      expect(sportEventHelper.isSpecialEvent).toHaveBeenCalled();
      expect(result).toEqual('specials');

      sportEventHelper.isSpecialEvent.and.returnValue(false);
      const negativeResult = component.getEventType(eventMock);
      expect(negativeResult).toEqual('');
    });

    it('check badminton call for updateCommentsDataFormat', () => {
      component['updateCommentsDataFormat']([badmintonEventMock]);
      expect(commentsService.badmintonMSInitParse).toHaveBeenCalled();
    });

    it('check football call for updateCommentsDataFormat', () => {
      component['updateCommentsDataFormat']([footballEventMock]);
      expect(commentsService.badmintonMSInitParse).not.toHaveBeenCalled();
    });

    it('#updateCommentsDataFormat should skip events without categoryCode', () => {
      component['updateCommentsDataFormat']([badmintonEventMock, footballEventMock, {id: 1}]);
      expect(commentsService.badmintonMSInitParse).toHaveBeenCalledTimes(1);
    });

    it('test yourCallAction click function', () => {
      const customEvent: any = {
        stopPropagation: jasmine.createSpy()
      };

      component.yourCallAction(customEvent);

      expect(customEvent.stopPropagation).toHaveBeenCalled();
      expect(promotionsService.openPromotionDialog).toHaveBeenCalledWith('YOUR_CALL');
    });

    it('get text for label show more', () => {
      const result = component.getShowMoreText(<any>featuredModuleMock);

      expect(result).toEqual('HO Google');

      featuredModuleMock.footerLink.text = null;
      const resultWithoutFooterText = component.getShowMoreText(<any>featuredModuleMock);
      expect(resultWithoutFooterText).toEqual('tranlation 3 HO Football tranlation');

      featuredModuleMock.totalEvents = null;
      const resultWithoutEvents = component.getShowMoreText(<any>featuredModuleMock);
      expect(resultWithoutEvents).toEqual(null);
    });

    describe('seeAllRaces', () => {
      describe('should push proper GTM data', () => {
        let expectedRacingName, mockCategoryId;

        describe('and navigate to sport landing page', () => {
          it('for horseracing sport category', () => {
            mockCategoryId = '21';
            expectedRacingName = 'horseracing';
          });
          it('for greyhound sport category', () => {
            mockCategoryId = '19'; expectedRacingName = 'greyhound';
          });

          afterEach(() => {
            component.seeAllRaces({ categoryId: mockCategoryId } as IOutputModule);
            expect(routingHelperService.formSportUrl).toHaveBeenCalledWith(expectedRacingName);
            expect(router.navigateByUrl).toHaveBeenCalledWith(`/${expectedRacingName}`);
          });
        });

        afterEach(() => {
          expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
            eventCategory: 'featured module',
            eventAction: 'featured races',
            eventLabel: 'see all',
            sportName: expectedRacingName
          });
        });
      });

      it('should not navigate or push GTM data for unknown racing categoryId', () => {
        component.seeAllRaces({ categoryId: '666' } as IOutputModule);
        expect(gtmService.push).not.toHaveBeenCalled();
        expect(routingHelperService.formSportUrl).not.toHaveBeenCalled();
        expect(router.navigateByUrl).not.toHaveBeenCalled();
      });

      it('should navigate to Virtual Sport', () => {
        const module = {
          categoryId: '39',
          data: [{
            className: 'Virtual Horse Racing',
            classId: '777'
          }],
        };
        virtualSharedService.isVirtual.and.returnValue(true);
        component.seeAllRaces(module as IOutputModule);
        expect(router.navigateByUrl).toHaveBeenCalled();
        expect(virtualSharedService.formVirtualTypeUrl).toHaveBeenCalledWith('777');
      });
    });

    it('should test if subscribed/unsubscribed from updates', () => {
      const id = featuredModuledataMock.data.modules[0]._id;

      component['getDataAndSubscribe'](id);
      expect(featuredModuleService.addEventListener).toHaveBeenCalledWith(id, jasmine.any(Function));
      expect(featuredModuleService.emit).toHaveBeenCalledWith('subscribe', id);
      expect(featuredModuleService.tabModuleStates.get(id)).toBeTruthy();
    });

    it('should test if subscribed/unsubscribed from updates', () => {
      const id = featuredModuledataMock.data.modules[0]._id;

      component['unsubscribe'](id);
      expect(featuredModuleService.removeEventListener).toHaveBeenCalledWith(id, jasmine.any(Function));
      expect(featuredModuleService.emit).toHaveBeenCalledWith('unsubscribe', [id]);
      expect(featuredModuleService.tabModuleStates[id]).toBeFalsy();
    });

    it('should test if clock method called for module data', () => {
      const events = featuredModuledataMock.data.modules[0].data;
      component['addClockToModule'](<any>events);
      expect(featuredModuleService.addClock).toHaveBeenCalledWith(<any>events);
    });

    it('check isRace function call', () => {
      const result = component.isRace(<any>featuredModuleMock);

      expect(result).toEqual({
        racingGrid: false,
        racingCard: false,
        racing: false
      });
    });

    it('check getInitStateOfFeatured', () => {
      expect(component['getInitStateOfFeatured']()).toEqual({
        directiveName: null,
        modules: [],
        showTabOn: null,
        title: null,
        visible: null
      });
    });

    it('check init function call', () => {
      spyOn(component as any, 'resubscribeToManuallyExpandedModules');
      spyOn(component as any, 'addModulesEventListeners');
      spyOn(component as any, 'addEventListenersForEventsInModules');
      component.init(<any>featuredDataMock);

      const module: any = featuredModuleMock;
      expect(filtersService.orderBy).toHaveBeenCalledWith(module.data, ['displayOrder', 'startTime', 'name']);

      expect(component['resubscribeToManuallyExpandedModules']).toHaveBeenCalled();
      expect(component['addModulesEventListeners']).toHaveBeenCalled();
      expect(component['addEventListenersForEventsInModules']).toHaveBeenCalled();
      expect(featuredModuleService.cacheEvents).toHaveBeenCalled();
      expect(component.featuredModuleData).toEqual({
        directiveName: '',
        modules: [featuredModuleMock, featuredQuickLinksMock, surfaceBetModule],
        showTabOn: '',
        title: 'titel',
        visible: true
      } as any);
      expect(component.isModuleAvailable).toBe(true);
      expect(component.noEventFound).toBe(false);
    });

    it('should sort module.data', () => {
      component.init(<any>featuredQuickLinksDataMock);

      expect(filtersService.orderBy).not.toHaveBeenCalled();
    });

    it('check init function call without data', () => {
      router.url = '/home/featured';
      component.isConnectSucceed = true;
      component.init(null);
      expect(component.showLoader).toBeFalsy();
      expect(component.noEventFound).toBeTruthy();
      expect(component.isModuleAvailable).toBe(false);
    });

    it('check init function call when there are no modules', () => {
      component.init({ modules: [] } as any);

      expect(component.featuredModuleData.modules.length).toEqual(0);
    });

    it('check isRace function call', () => {
      spyOn(component as any, 'getBadge');
      spyOn(component as any, 'updateCommentsDataFormat').and.returnValue(null);

      (component['featuredModuleData'] as any) = {
        modules: []
      };
      (component['badges'] as any) = {};

      component.onModuleUpdate(<any>featuredModuleMock);

      expect(component['getBadge']).toHaveBeenCalled();
      expect(templateService.setCorrectPriceType).toHaveBeenCalled();
      expect(featuredModuleService.cacheEvents).toHaveBeenCalled();

      expect(component.badges[featuredModuleMock._id]).toBeUndefined();
    });

    it('should test if module is hidden', () => {
      expect(component.isModuleHidden(<any>{isLoaded: false})).toBeTruthy();
      expect(component.isModuleHidden(<any>{isLoaded: true, data: []})).toBeFalsy();
    });

    describe('#isOddsCardHeaderShown method', () => {
      it('should check if to show odds card header', () => {
        const module: any = featuredModuledataMock.data.modules[0];
        module.dataSelection.selectionType = 'Type';
        expect(component.isOddsCardHeaderShown(module)).toBe(true);
      });

      it('should check if not to show odds card header', () => {
        const module: any = featuredModuledataMock.data.modules[0];
        module.dataSelection.selectionType = 'RaceTypeId';
        expect(component.isOddsCardHeaderShown(module)).toBe(false);
        module.dataSelection.selectionType = 'Enhanced Multiples';
        expect(component.isOddsCardHeaderShown(module)).toBe(false);
      });
    });

    it('should test if no event found', () => {
      component.isConnectSucceed = true;
      component.featuredModuleData = <any>{};
      component.showLoader = false;
      expect(component.checkNoEventFound()).toBeTruthy();
      component.ssDown = true;
      expect(component.checkNoEventFound()).toBeFalsy();
      component.ssDown = false;
      component.featuredModuleData.modules = [<any>{}];
      expect(component.checkNoEventFound()).toBeFalsy();
      component.featuredModuleData.modules = [<any>{data: []}];
      expect(component.checkNoEventFound()).toBeFalsy();
      component.featuredModuleData.modules = [<any>{isLoaded: true, data: []}];
      expect(component.checkNoEventFound()).toBeTruthy();
    });


    it('should call add listener for each module addEventListenersForEventsInModules', () => {
      spyOn(<any>component, 'addEventListenersWithinModule');

      const featuredModuledataMockClone: any = _.clone(featuredDataMock);

      component['addEventListenersForEventsInModules'](<any>featuredModuledataMockClone);

      expect(component['addEventListenersWithinModule']).toHaveBeenCalledTimes(3);
    });

    it('should getModuleIds', () => {
      const result = component['getModuleIds'](<any>featuredDataMock.modules);

      expect(result.indexOf('5b759926c9e77c000163eede') >= 0).toBeTruthy();
      expect(result.indexOf('featuredQuickLinksModuleId') >= 0).toBeTruthy();
    });

    it('should modify Football Main Markets', () => {
      const featuredModuleMockClone: any = _.clone(featuredModuleMock);
      component['modifyMarket'] = jasmine.createSpy();
      component['modifyFootballMainMarkets'](<any>featuredModuleMockClone);
      expect(component['modifyMarket']).toHaveBeenCalled();
      expect(featuredModuleMockClone.data[1].markets[0].dispSortName).toEqual('MR');
      expect(featuredModuleMockClone.data[1].markets[0].marketMeaningMinorCode).toEqual('MR');
    });

    it('should not define HR silks type', () => {
      const featuredModuleMockClone: any = _.clone(featuredModuleMock);
      component['defineHRsilksType'](<any>featuredModuleMockClone);
      expect(eventService.isUKorIRE).not.toHaveBeenCalled();
    });

    it('should define HR silks type', () => {
      const featuredModuleMockClone: any = _.clone(featuredModuleMock);
      featuredModuleMockClone.data[1].categoryCode = 'HORSE_RACING';
      component['defineHRsilksType'](<any>featuredModuleMockClone);
      expect(eventService.isUKorIRE).toHaveBeenCalled();
      expect(featuredModuleMockClone.data[1].isUKorIRE).toBeDefined();
    });

    it('should manageSocketSubscription', () => {
      spyOn(component as any, 'getDataAndSubscribe');

      const featuredModuleMockClone: any = _.clone(featuredModuleMock);

      featuredModuleMockClone.data = [];
      component['manageSocketSubscription'](<any>featuredModuleMockClone, true);

      expect(featuredModuleMockClone.showExpanded).toBe(true);
      expect(component['getDataAndSubscribe']).toHaveBeenCalledWith(featuredModuleMockClone._id);
      expect(featuredModuleService.addModuleToSubscribedFeaturedTabModules).toHaveBeenCalledWith(featuredModuleMockClone._id);
    });

    it('should manageSocketSubscription and should not call function if data present', () => {
      spyOn(component as any, 'getDataAndSubscribe');

      const featuredModuleMockClone: any = _.clone(featuredModuleMock);
      component['manageSocketSubscription'](<any>featuredModuleMockClone, true);

      expect(featuredModuleMockClone.showExpanded).toBe(true);
      expect(component['getDataAndSubscribe']).not.toHaveBeenCalled();
      expect(featuredModuleService.addModuleToSubscribedFeaturedTabModules).not.toHaveBeenCalled();
    });

    it('should manageSocketSubscription', () => {
      spyOn(component as any, 'getDataAndSubscribe');

      const featuredModuleMockClone: any = _.clone(featuredModuleMock);

      featuredModuleMockClone.data = [];

      component['manageSocketSubscription'](<any>featuredModuleMockClone, true);

      expect(featuredModuleMockClone.showExpanded).toBe(true);
      expect(component['getDataAndSubscribe']).toHaveBeenCalledWith(featuredModuleMockClone._id);
      expect(featuredModuleService.addModuleToSubscribedFeaturedTabModules).toHaveBeenCalledWith(featuredModuleMockClone._id);
    });

    it('check getBadge function call', () => {
      const featuredModuleMockClone: any = _.clone(featuredModuleMock);

      featuredModuleMockClone.isSpecial = true;
      expect(component['getBadge'](<any>featuredModuleMockClone)).toEqual({label: 'Special', className: 'pc-badge--specials'});

      featuredModuleMockClone.isEnhanced = true;
      expect(component['getBadge'](<any>featuredModuleMockClone)).toEqual({label: 'Enhanced', className: 'pc-badge--enhanced'});
    });

    it('check addClockToEvents function call', () => {
      const featuredModuleMockClone: any = _.clone(featuredModuleMock);

      component['addClockToEvents'](<any>{
        modules: [featuredModuleMockClone]
      });

      expect(featuredModuleService.addClock).toHaveBeenCalledWith(featuredModuleMockClone.data);
    });

    it('check detect changes called on updateFeatureModuleView Call', () => {
      component['updateFeatureModuleView']();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    describe('#featureTabOnSocketUpdate', () => {
      it('other modules flow', () => {
        component['isInplayModule'] = jasmine.createSpy().and.returnValue(false);
        component['onModuleUpdate'] = jasmine.createSpy();
        component['addEventListenersWithinModule'] = jasmine.createSpy();
        component['unsubscribe'] = jasmine.createSpy();
        component['featureTabOnSocketUpdate'](featuredModuleMock as any);
        expect(component['onModuleUpdate']).toHaveBeenCalledWith(featuredModuleMock as any);
        expect(component['addEventListenersWithinModule']).toHaveBeenCalledWith(featuredModuleMock as any);
        expect(component['unsubscribe']).toHaveBeenCalledWith(featuredModuleMock._id);
        expect(featuredModuleMock.footerLink.url).toEqual('www.google.com');
      });
    });

    it('resubscribeToManuallyExpandedModules', () => {
      component['resubscribeToManuallyExpandedModules']();

      expect(featuredModuleService.emit).toHaveBeenCalledTimes(6);
      expect(featuredModuleService.addEventListener).toHaveBeenCalledTimes(3);
    });

    it('#merge should modify modules data according to expanding with empty featuredModuleData.modules', () => {
      spyOn<any>(component, 'addClockToModule');
      spyOn(_, 'some').and.returnValue(undefined);
      spyOn(_, 'find').and.returnValue(null);
      spyOn(component, 'isOutright').and.returnValues(false, true, false);

      const featuredModuleMockClone: any = {...featuredDataMock};
      featuredModuleMockClone.modules[0].showExpanded = false;
      featuredModuleMockClone.modules[1].showExpanded = true;
      component['merge'](featuredModuleMockClone.modules);

      expect(featuredModuleMockClone.modules[0].showExpanded).toBe(false);
      expect(component['addClockToModule']).toHaveBeenCalledTimes(3);
      expect(featuredModuleMockClone.modules[0].isOutright).toEqual(false);
      expect(featuredModuleMockClone.modules[1].isOutright).toEqual(true);
    });

    it('#merge should modify modules data according to expanding', () => {
      spyOn<any>(component, 'addClockToModule');
      spyOn(_, 'some').and.returnValue(true);
      spyOn(_, 'find').and.returnValue({showExpanded: true, data: {id: 1}});
      spyOn(component, 'isOutright').and.returnValues(false, true, false);

      const featuredModuleMockClone: any = {...featuredDataMock};
      featuredModuleMockClone.modules[0].showExpanded = false;
      featuredModuleMockClone.modules[1].showExpanded = true;

      component['merge'](featuredModuleMockClone.modules);
      expect(featuredModuleMockClone.modules[0].showExpanded).toBe(true);
      expect(featuredModuleMockClone.modules[0].data).toEqual({id: 1});
      expect(featuredModuleMockClone.modules[1].data).toEqual({id: 1});
      expect(component['addClockToModule']).not.toHaveBeenCalled();
    });

    it('#merge should not expand collapsed module', () => {
      spyOn(_, 'some').and.returnValue(true);
      spyOn(_, 'find').and.returnValue({showExpanded: false, data: {id: 1}});

      const featuredModuleMockClone: any = {...featuredDataMock};
      featuredModuleMockClone.modules[0].showExpanded = true;

      component['merge'](featuredModuleMockClone.modules);
      expect(featuredModuleMockClone.modules[0].showExpanded).toBe(false);
    });

    it('shoud return existing module', () => {
      const featuredModuleMockClone: any = {...featuredDataMock};

      spyOn<any>(component, 'addClockToModule');
      spyOn(_, 'some').and.returnValue(true);
      spyOn(_, 'find').and.returnValue(featuredModuleMockClone.modules[0]);
      spyOn(component, 'isOutright').and.returnValues(false, true, false);

      featuredModuleMockClone.modules[0].dataSelection.selectionType = 'RaceTypeId';
      featuredModuleMockClone.modules[0].showExpanded = false;

      component['merge'](featuredModuleMockClone.modules);

      expect(featuredModuleMockClone.modules[0].showExpanded).toBe(false);
    });

    it('should check isOutright module', () => {
      const ourightModuleMock: any = {
        dataSelection: {
          selectionType: 'Market'
        },
        data: [
          {
            categoryCode: 'GOLF',
            eventSortCode: 'TNMT',
            markets: [
              {
                templateMarketName: 'Win or Each Way'
              }
            ]
          }
        ]
      };

      const ourightModulNotByMarketIdeMock: any = {
        dataSelection: {
          selectionType: 'Event'
        },
        data: [
          {
            categoryCode: 'GOLF',
            eventSortCode: 'TNMT',
            markets: [
              {
                templateMarketName: 'Win or Each Way'
              }
            ]
          }
        ]
      };

      const ourightWithoutMarketsModuleMock: any = {
        dataSelection: {
          selectionType: 'Market'
        },
        data: [
          {
            categoryCode: 'GOLF',
            eventSortCode: 'TNMT',
            markets: []
          }
        ]
      };

      const notOurightModuleMock: any = {
        dataSelection: {
          selectionType: 'Market'
        },
        data: [
          {
            categoryCode: 'GOLF',
            eventSortCode: 'TR000'
          }
        ]
      };

      const outrightModuleMockWithoutCategory: any = {
        dataSelection: {
          selectionType: 'Market'
        },
        data: [
          {
            categoryCode: '',
            eventSortCode: 'TNMT',
            markets: [
              {
                templateMarketName: 'Win or Each Way'
              }
            ]
          }
        ]
      };

      expect(component.isOutright(ourightModuleMock)).toBeTruthy();
      expect(component.isOutright(ourightModulNotByMarketIdeMock)).toBeFalsy();
      expect(component.isOutright(notOurightModuleMock)).toBeFalsy();
      expect(component.isOutright(ourightWithoutMarketsModuleMock)).toBeFalsy();
      expect(component.isOutright(outrightModuleMockWithoutCategory)).toBeTruthy();
    });

    it('should check is Win or Each Way module', () => {
      const woEwModuleMock: any = {
        dataSelection: {
          selectionType: 'Market'
        },
        data: [
          {
            markets: [
              {
                templateMarketName: 'Win or Each Way'
              }
            ]
          }
        ]
      };

      const notWoEwModuleMock: any = {
        dataSelection: {
          selectionType: 'Market'
        },
        data: [
          {
            markets: [
              {
                templateMarketName: 'Match Betting'
              }
            ]
          }
        ]
      };

      expect(component.isWoEw(woEwModuleMock)).toBeTruthy();
      expect(component.isWoEw(notWoEwModuleMock)).toBeFalsy();
    });

    describe('#isInplayModule', () => {
      it('should be truthy', () => {
        const module: any = {
          '@type': 'InplayModule'
        };
        expect(component['isInplayModule'](module)).toBeTruthy();
      });
      it('should be falsy', () => {
        const module: any = {
          '@type': 'someOtherModule'
        };
        expect(component['isInplayModule'](module)).toBeFalsy();
      });
    });
    describe('#addEventListenersForEventsInModules', () => {
      it('should go inplay module branch', () => {
        component['addEventsLiveUpdatesListener'] = jasmine.createSpy('1');
        component['isInplayModule'] = jasmine.createSpy('2').and.returnValue(true);
        const data: any = {
          modules: [{
            '@type': 'InplayModule'
          }]
        };
        component['addEventListenersForEventsInModules'](data);
        expect(component['isInplayModule']).toHaveBeenCalled();
      });
      it('should go other modules branch', () => {
        component['addEventsLiveUpdatesListener'] = jasmine.createSpy();
        component['isInplayModule'] = jasmine.createSpy();
        const data: any = {
          modules: [{
            '@type': 'anyOtherModule'
          }]
        };
        component['addEventListenersForEventsInModules'](data);
        expect(component['isInplayModule']).toHaveBeenCalled();
      });
    });

    describe('#getEventsFromInplayModule', () => {
      it('should modify markets', () => {
        component['modifyMarket'] = jasmine.createSpy();
        component['getEventsFromInplayModule'](featuredInplayModuleMock as any);
        expect(component['modifyMarket']).toHaveBeenCalled();
      });
      it('should return all events from inplay module', () => {
        const result = component['getEventsFromInplayModule'](featuredInplayModuleMock as any);
        expect(result).toEqual(featuredInplayModuleMock.data[0].eventsByTypeName[0].events as any);
      });
      it('should return empty array', () => {
        const result = component['getEventsFromInplayModule']({} as any);
        expect(result).toEqual([]);
      });
    });

    describe('#addEventsLiveUpdatesListener', () => {
      it('should add addEventListener to events array', () => {
        component['addEventsLiveUpdatesListener']([footballEventMock, eventMock, badmintonEventMock] as any);
        expect(featuredModuleService.addEventListener).toHaveBeenCalledTimes(3);
      });

      it('should add addEventListener to events array', () => {
        component['addEventsLiveUpdatesListener']([footballEventMock, eventMock, badmintonEventMock, {}] as any);
        expect(featuredModuleService.addEventListener).toHaveBeenCalledTimes(3);
      });

      it('should call connect on update', () => {
        // eslint-disable-next-line
        featuredModuleService.addEventListener.and.callFake((string: string, cb: Function) => {
          cb(string);
        });
        component['addEventsLiveUpdatesListener']([footballEventMock, eventMock, badmintonEventMock] as any);
        expect(pubsub.publish).toHaveBeenCalledTimes(3);
      });
    });

    it('#isSimpleModule should return true', () => {
      const module = {
        '@type': 'QuickLinkModule'
      } as any;

      const result = component['isSimpleModule'](module);
      expect(result).toBeTruthy();
    });

    it('#isSimpleModule AEM should return true', () => {
      const module = {
        '@type': 'AEM_BANNERS'
      } as any;

      const result = component['isSimpleModule'](module);
      expect(result).toBeTruthy();
    });

    it('#isSimpleModule should return true', () => {
      const module = {
        '@type': 'RecentlyPlayedGameModule'
      } as any;

      const result = component['isSimpleModule'](module);
      expect(result).toBeTruthy();
    });

    it('#isSimpleModule should return false', () => {
      const module = {
        '@type': 'TestModule'
      } as any;

      const result = component['isSimpleModule'](module);
      expect(result).toBeFalsy();
    });

    it('#isSurfaceBetsModule should return true', () => {
      const module = {
        '@type': 'SurfaceBetModule'
      } as any;

      const result = component['isSurfaceBetsModule'](module);
      expect(result).toBeTruthy();
    });

    it('#isSurfaceBetsModule should return false', () => {
      const module = {
        '@type': 'Module'
      } as any;

      const result = component['isSurfaceBetsModule'](module);
      expect(result).toBeFalsy();
    });

    it('#isHighLIghtCarouselModule should return true', () => {
      const module = {
        '@type': 'HighlightCarouselModule'
      } as any;

      const result = component['isHighLIghtCarouselModule'](module);
      expect(result).toBeTruthy();
    });

    it('#isHighLIghtCarouselModule should return false', () => {
      const module = {
        '@type': 'NotAHighlightCarouselModule'
      } as any;

      const result = component['isHighLIghtCarouselModule'](module);
      expect(result).toBeFalsy();
    });


    describe('#modifyMarket', () => {
      it('should modify football event', () => {
        const event: any = _.clone(eventMock);
        event.categoryId = '16';
        event.markets[0].templateMarketName = 'To Qualify';
        component['modifyMarket'](event);
        expect(event.markets[0].dispSortName).toEqual('MR');
        expect(event.markets[0].marketMeaningMinorCode).toEqual('MR');
      });
      it('should not modify not football event ', () => {
        const event: any = _.clone(eventMock);
        event.categoryId = 'someId';
        event.markets[0].dispSortName = '123';
        event.markets[0].marketMeaningMinorCode = '312';
        component['modifyMarket'](event);
        expect(event.markets[0].dispSortName).not.toEqual('MR');
        expect(event.markets[0].marketMeaningMinorCode).not.toEqual('MR');
      });
    });

    describe('#onModuleUpdate', () => {
      it('should just return', () => {
        const result = component.onModuleUpdate({} as any);

        expect(result).toBeUndefined();
      });

      it('should add clock to the module', () => {
        const moduleMock = {
          _id: '123',
          data: [
            {
              categoryCode: 'GOLF',
              eventSortCode: 'TNMT',
              markets: [
                {
                  templateMarketName: 'Win or Each Way'
                }
              ]
            }
          ]
        };

        const moduleNotToUpdate = {
          _id: '3',
          data: [
            {
              categoryCode: 'GOLF',
              eventSortCode: 'TNMT',
              markets: [
                {
                  templateMarketName: 'Win or Each Way'
                }
              ]
            }
          ]
        };

        component.badges = {};
        component['addClockToModule'] = jasmine.createSpy().and.callFake((data) => data);
        component['updateCommentsDataFormat'] = jasmine.createSpy();
        component.featuredModuleData = {
          modules: [{...moduleMock}, {...moduleNotToUpdate}]
        } as any;
        component.onModuleUpdate(moduleMock as any);

        expect(component['addClockToModule']).toHaveBeenCalledTimes(1);
      });

      it('should call template service', () => {
        const moduleMock = {
          _id: '123',
          data: [
            {
              categoryCode: 'GOLF',
              eventSortCode: 'TNMT',
              markets: [
                {
                  templateMarketName: 'Win or Each Way'
                }
              ]
            }
          ]
        };

        component.badges = {};
        component.onModuleUpdate(moduleMock as any);

        expect(templateService.setCorrectPriceType).toHaveBeenCalled();
      });

      it('should not call template service', () => {
        const moduleMock = {
          '@type': 'RecentlyPlayedGameModule',
          _id: '123',
          data: [
            {
              categoryCode: 'GOLF',
              eventSortCode: 'TNMT',
              markets: [
                {
                  templateMarketName: 'Win or Each Way'
                }
              ]
            }
          ]
        };

        component.badges = {};
        component.onModuleUpdate(moduleMock as any);

        expect(templateService.setCorrectPriceType).not.toHaveBeenCalled();
      });
      it('should call moduleDataSort', () => {
        component['moduleDataSort'] = jasmine.createSpy();
        const moduleMock = {
          '@type': 'SurfaceBetModule',
          segmented:true,
          _id: '123',
          data: [
            {
              segmetOrder:1,
              categoryCode: 'GOLF',
              eventSortCode: 'TNMT',
              markets: [
                {
                  templateMarketName: 'Win or Each Way'
                }
              ]
            }
          ]
        };

        component.badges = {};
        component.onModuleUpdate(moduleMock as any);

        expect(component['moduleDataSort']).toHaveBeenCalled();
      });
      it('should not call moduleDataSort case 1', () => {
        spyOn(component as any, 'moduleDataSort')
        const moduleMock = {
          '@type': 'SurfaceBetModule12',
          segmented:true,
          _id: '123',
          data: [
            {
              segmetOrder:1,
              categoryCode: 'GOLF',
              eventSortCode: 'TNMT',
              markets: [
                {
                  templateMarketName: 'Win or Each Way'
                }
              ]
            }
          ]
        };

        component.badges = {};
        component.onModuleUpdate(moduleMock as any);

        expect(component['moduleDataSort']).not.toHaveBeenCalled();
      });
      it('should not call moduleDataSort case 2', () => {
        component['moduleDataSort'] = jasmine.createSpy();
        const moduleMock = {
          '@type': 'QuickLinkModule',
          _id: '123',
          data: [
            {
              segmetOrder:1,
              categoryCode: 'GOLF',
              eventSortCode: 'TNMT',
              markets: [
                {
                  templateMarketName: 'Win or Each Way'
                }
              ]
            }
          ]
        };

        component.badges = {};
        component.onModuleUpdate(moduleMock as any);

        expect(component['moduleDataSort']).toHaveBeenCalled();
      });
      it('should call moduleDataSort case 2', () => {
        component['moduleDataSort'] = jasmine.createSpy();
        const moduleMock = {
          '@type': 'QuickLinkModule',
          segmented:true,
          _id: '123',
          data: [
            {
              segmetOrder:1,
              categoryCode: 'GOLF',
              eventSortCode: 'TNMT',
              markets: [
                {
                  templateMarketName: 'Win or Each Way'
                }
              ]
            }
          ]
        };

        component.badges = {};
        component.onModuleUpdate(moduleMock as any);

        expect(component['moduleDataSort']).toHaveBeenCalled();
      });
    });

    describe('#featureTabOnSocketUpdate', () => {
      it('inplay module flow', () => {
        component['isInplayModule'] = jasmine.createSpy().and.returnValue(true);
        component['onInplayModuleUpdate'] = jasmine.createSpy();
        component['featureTabOnSocketUpdate'](featuredInplayModuleMock as any);
        expect(component['onInplayModuleUpdate']).toHaveBeenCalledWith(featuredInplayModuleMock as any);
        expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
      });
      it('other modules flow - with unsubscribe', () => {
        component['isInplayModule'] = jasmine.createSpy().and.returnValue(false);
        component['onModuleUpdate'] = jasmine.createSpy();
        component['addEventListenersWithinModule'] = jasmine.createSpy();
        component['unsubscribe'] = jasmine.createSpy();
        component['featureTabOnSocketUpdate'](featuredModuleMock as any);
        expect(component['onModuleUpdate']).toHaveBeenCalledWith(featuredModuleMock as any);
        expect(component['addEventListenersWithinModule']).toHaveBeenCalledWith(featuredModuleMock as any);
        expect(component['unsubscribe']).toHaveBeenCalledWith(featuredModuleMock._id);
        expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
      });

      it('other modules flow - without unsubscribe', () => {
        component['isInplayModule'] = jasmine.createSpy().and.returnValue(false);
        component['onModuleUpdate'] = jasmine.createSpy();
        component['addEventListenersWithinModule'] = jasmine.createSpy();
        component['unsubscribe'] = jasmine.createSpy();
        component['featureTabOnSocketUpdate'](featuredQuickLinksMock as any);
        expect(component['unsubscribe']).not.toHaveBeenCalled();
        expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
      });

      it('featured module module update without data', () => {
        component['isInplayModule'] = jasmine.createSpy().and.returnValue(false);
        component['onModuleUpdate'] = jasmine.createSpy();
        component['addEventListenersWithinModule'] = jasmine.createSpy();
        component['unsubscribe'] = jasmine.createSpy();
        component['featureTabOnSocketUpdate']();
        expect(component['onModuleUpdate']).toHaveBeenCalledWith(cleanModuleMock);
        expect(component['addEventListenersWithinModule']).toHaveBeenCalledWith(cleanModuleMock);
        expect(component['unsubscribe']).toHaveBeenCalledWith(null);
        expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
      });
    });

    describe('#onInplayModuleUpdate', () => {
      it('should call updateInPlayCounter one time', () => {
        component.featuredModuleData = {
          modules: [
            featuredQuickLinksMock,
            featuredInplayModuleMock
          ]
        } as any;
        spyOn(component as any, 'updateInPlayCounter').and.callThrough();
        const updatedModule = _.clone(featuredInplayModuleMock);
        updatedModule.totalEvents = 400;
        component['onInplayModuleUpdate'](updatedModule as any);
        expect(changeDetectorRef.markForCheck).toHaveBeenCalledTimes(1);
        expect(component['updateInPlayCounter']).toHaveBeenCalledTimes(1);
        expect(component['updateInPlayCounter']).toHaveBeenCalledWith(featuredInplayModuleMock as any, updatedModule as any);
        expect(updatedModule.totalEvents).toEqual(400);
      });
    });

    describe('trackErrorMessage', () => {
      it('should not track error if sportId not 0', () => {
        component.sportId = 555;
        component.ssDown = true;
        component.isConnectSucceed = false;
        component['trackErrorMessage']();

        expect(awsService.addAction).not.toHaveBeenCalled();
      });

      it('should not track error site serve is not down and connection established', () => {
        component.sportId = 0;
        component.ssDown = false;
        component.isConnectSucceed = true;
        component['trackErrorMessage']();

        expect(awsService.addAction).not.toHaveBeenCalled();
      });

      it('should track error if site serve is down', () => {
        component.sportId = 0;
        component.ssDown = true;
        component.isConnectSucceed = true;
        component['trackErrorMessage']();

        expect(awsService.addAction).toHaveBeenCalledWith('featured=>UI_Message=>Unavailable=>ssError');
      });

      it('should track error if connection does not established', () => {
        component.sportId = 0;
        component.ssDown = false;
        component.isConnectSucceed = false;
        component['trackErrorMessage']();

        expect(awsService.addAction).toHaveBeenCalledWith('featured=>UI_Message=>Unavailable=>wsError');
      });
    });

  });

  describe('ngOnDestroy', () => {
    let initialState;
    beforeEach(() => {
      initialState = {
        directiveName: null,
        modules: [],
        showTabOn: null,
        title: null,
        visible: null
      };
      component['detectListener'] = 2;
    });

    it('default case', () => {
      component.ngOnDestroy();
      expect(pubsub.unsubscribe).toHaveBeenCalledWith('featuredModule');
      expect(featuredModuleService.clearSubscribedFeaturedTabModules).toHaveBeenCalledTimes(1);
      expect(featuredModuleService.disconnect).toHaveBeenCalledTimes(1);
      expect(featuredModuleService.cacheEvents).toHaveBeenCalledWith(initialState);
      expect(windowRef.nativeWindow.clearInterval).toHaveBeenCalledWith(2);
      expect(component['sysConfigSubscription'].unsubscribe).toHaveBeenCalled();
    });

    it('ribbonSubscription', () => {
      component['ribbonSubscription'] = { unsubscribe: jasmine.createSpy('ribbonSubscription.unsubsctibe')  } as any;
      component.ngOnDestroy();

      expect(component['ribbonSubscription'].unsubscribe).toHaveBeenCalled();
    });
  });

  describe('ngOnChanges', () => {
    it('should call fetchSurfaceBets', () => {
      component['fetchSurfaceBets'] = jasmine.createSpy();
      component['fetchSurfaceBets']();
      expect(component['fetchSurfaceBets']).toHaveBeenCalled();
    });
  });

  describe('@updateCommentsInplayModule', () => {
    it('should call comments update on modules events', () => {
      component['updateCommentsDataFormat'] = jasmine.createSpy();
      component['init'](badmintonInplayModuleMock as any);

      const expectedEvents = badmintonInplayModuleMock.modules[0].data[0].eventsByTypeName[0].events;

      expect(component['updateCommentsDataFormat'])
        .toHaveBeenCalledWith(expectedEvents as any);
    });
  });

  describe('@updateComments', () => {
    it('updateComments for Highlight Module should update comments for module', () => {
      const DataWithHighlightCarouselModuleMock = {
        modules: [
          {
            '@type': 'HighlightCarouselModule',
            displayOrder: 0.5,
            showExpanded: true,
            publishedDevices: [],
            data: [
              {}
            ]
          }
        ]
      };

      component['updateCommentsDataFormat'] = jasmine.createSpy();
      component['init'](DataWithHighlightCarouselModuleMock as any);

      expect(component['updateCommentsDataFormat'])
        .toHaveBeenCalled();
    });
  });

  it('#childComponentLoaded', () => {
    component.childComponentLoaded();
    expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
  });

  describe('#showRpg', () => {
    beforeEach(() => {
      component.user = {
        status: true
      } as any;
    });

    it('returns true', () => {
      const outputModule = {'@type' : 'RecentlyPlayedGameModule'} as any;
      component.router = {
        url: '/'
      } as any;

      expect(component.showRpg(outputModule)).toBeTruthy();
    });

    it('returns false - not a homepage', () => {
      const outputModule = {'@type' : 'RecentlyPlayedGameModule'} as any;
      component.router = {
        url: '/test'
      } as any;

      expect(component.showRpg(outputModule)).toBeFalsy();
    });

    it('returns false - wrong outputModule', () => {
      const outputModule = {'@type' : 'TestModule'} as any;
      router.url = '/home/featured';

      expect(component.showRpg(outputModule)).toBeFalsy();
    });

    it('returns false - no user', () => {
      const outputModule = {'@type' : 'RecentlyPlayedGameModule'} as any;
      router.url = '/';
      component.user = {} as any;

      expect(component.showRpg(outputModule)).toBeFalsy();
    });
  });

  describe('showLoader', () => {

    beforeEach(() => {
      spyOn(component.isLoadedEvent, 'emit');
      spyOn(component.featuredEventsCount, 'emit');
    });

    it('should trigger change detection and timeout for emitter', () => {
      component.showLoader = true;

      expect(component['windowRef'].nativeWindow.setTimeout).toHaveBeenCalled();
    });

    it('should show loader and emit false', () => {
      component.ssDown = false;
      component.isConnectSucceed = true;
      component.showLoader = true;

      expect(component['isLoaderShown']).toBe(true);
      expect(component.isLoadedEvent.emit).toHaveBeenCalledWith(false);
      expect(component.featuredEventsCount.emit).not.toHaveBeenCalled();
    });

    it('should hide loader and emit true', () => {
      spyOn<any>(component, 'getFeaturedEventsCount').and.returnValue(0);
      component.sportId = 10;
      component.featuredModuleData.modules = [{} as any];
      component.ssDown = true;
      component.isConnectSucceed = false;
      component.showLoader = true;

      expect(component['isLoaderShown']).toBe(false);
      expect(component.isLoadedEvent.emit).toHaveBeenCalledWith(true);
      expect(component['getFeaturedEventsCount']).toHaveBeenCalledWith([{} as any]);
      expect(component.featuredEventsCount.emit).toHaveBeenCalledWith(0);
    });

    it('should hide loader and emit true 2', () => {
      component.ssDown = false;
      component.isConnectSucceed = true;
      component.showLoader = false;

      expect(component['isLoaderShown']).toBe(false);
      expect(component.isLoadedEvent.emit).toHaveBeenCalledWith(true);
    });

    it('should use getter with private value', () => {
      component['isLoaderShown'] = true;
      expect(component.showLoader).toBe(true);

      component['isLoaderShown'] = false;
      expect(component.showLoader).toBe(false);
    });
    it('should be falsy is shouldDisplayLoader is false', () => {
      component['shouldDisplayLoader'] = false;
      component['isLoaderShown'] = true;
      expect(component.showLoader).toBe(false);

      component['isLoaderShown'] = false;
      expect(component.showLoader).toBe(false);
    });
  });

  describe('getFeaturedEventsCount', () => {

    it('filters should have one filter and totalEvents is not exist', () => {
      const modules = [{data: [{} as any]}] as any;
      spyOn<any>(component, 'isSurfaceBetsModule');
      spyOn<any>(component, 'isInplayModule');
      spyOn<any>(component, 'isHighLIghtCarouselModule').and.returnValue(false);

      expect(component['getFeaturedEventsCount'](modules)).toEqual(0);
      expect(component['isSurfaceBetsModule']).toHaveBeenCalled();
      expect(component['isInplayModule']).not.toHaveBeenCalled();
      expect(component['isHighLIghtCarouselModule']).not.toHaveBeenCalled();
    });

    it('filters should have 3 filters and totalEvents is not exist', () => {
      const modules = [{data: [{} as any], '@type': 'SurfaceBetModule'}] as any;
      component.isInplayModuleEnabled = true;
      component.isHighlightCarouselEnabled = true;
      spyOn<any>(component, 'isSurfaceBetsModule');
      spyOn<any>(component, 'isInplayModule');
      spyOn<any>(component, 'isHighLIghtCarouselModule').and.returnValue(true);

      expect(component['getFeaturedEventsCount'](modules)).toEqual(1);
      expect(component['isSurfaceBetsModule']).toHaveBeenCalled();
      expect(component['isInplayModule']).toHaveBeenCalled();
      expect(component['isHighLIghtCarouselModule']).toHaveBeenCalled();
    });

    it('filters should have one filter and totalEvents is exist', () => {
      const modules = [{totalEvents: 2, '@type': 'SurfaceBetModule'}] as any;
      spyOn<any>(component, 'isSurfaceBetsModule').and.returnValue(true);

      expect(component['getFeaturedEventsCount'](modules)).toEqual(2);
      expect(component['isSurfaceBetsModule']).toHaveBeenCalled();
    });
  });

  it('@reloadComponent should reload component', () => {
     component.reloadComponent();
     expect(featuredModuleService.reconnect).toHaveBeenCalled();
     expect(component.ssDown).toBe(false);
     expect(component.isConnectSucceed).toBe(true);
     expect(component.showLoader).toBe(true);
     expect(component['changeDetectorRef'].markForCheck).toHaveBeenCalled();
  });

  it('should use OnPush strategy', () => {
    expect(FeaturedModuleComponent['__annotations__'][0].changeDetection).toBe(0);
  });

  describe('oddsCardHeaderInitialized', () => {
    it('set initialized module to true', () => {
      component.oddsCardHeaderInitialized('123456');
      expect(component.initializedModulesMap['123456']).toBeTruthy();
    });
    it('set initialized module to true', () => {
      component.oddsCardHeaderInitialized('');
      expect(component.initializedModulesMap).toEqual({});
    });
  });
  it('isFeaturedUrl', () => {
    expect(component['isFeaturedUrl']('/')).toBeTruthy();
    expect(component['isFeaturedUrl']('/home/featured')).toBeTruthy();
    expect(component['isFeaturedUrl']('abc')).toBeFalsy();
  });

  describe('handleErrorOnFirstLoad', () => {
    it('homepage', () => {
      router.url = '/';
      component.handleErrorOnFirstLoad();
      expect(router.navigateByUrl).toHaveBeenCalledWith('link2');
    });

    it('not homepage', () => {
      component['trackErrorMessage'] = jasmine.createSpy();
      router.url = 'test';
      component.handleErrorOnFirstLoad();
      expect(component.ssDown).toBeTruthy();
      expect(component.showLoader).toBeFalsy();
      expect(component['changeDetectorRef'].markForCheck).toHaveBeenCalled();
      expect(component['trackErrorMessage']).toHaveBeenCalled();
    });
  });
  describe('#showLeaderboardWidget', () => {
    it('should return false, if none satisfies', ()=> {
      spyOn(component as any, 'isFeaturedUrl').and.returnValue(false);
      const response = component.showLeaderboardWidget('sport/football/live');
      expect(response).toBe(false);
    });
    it('should return false, if 2nd condition is (true/false)', ()=> {
      component.leaderBoardConfig = null;
      spyOn(component as any, 'isFeaturedUrl').and.returnValue(false);
      const response = component.showLeaderboardWidget('/sport/football/matches');
      expect(response).toBe(false);
    });
    it('should return true, if 2nd condition is (true/true)', ()=> {
      component.leaderBoardConfig = { homePage: true, footballPage: true } as any;
      spyOn(component as any, 'isFeaturedUrl').and.returnValue(false);
      const response = component.showLeaderboardWidget('/sport/football/matches');
      expect(response).toBe(true);
    });
    it('should return false, if 1st condition is (true/false)', () => {
      component.leaderBoardConfig = null;
      spyOn(component as any, 'isFeaturedUrl').and.returnValue(true);
      const response = component.showLeaderboardWidget('/');
      expect(response).toBe(false);
    });
    it('should return true, if 1st condition is (true/true)', ()=> {
      component.leaderBoardConfig = { homePage: true, footballPage: true } as any;
      spyOn(component as any, 'isFeaturedUrl').and.returnValue(true);
      const response = component.showLeaderboardWidget('/');
      expect(response).toBe(true);
    });
  });
  describe('#sortAndFormFeaturedData',()=>{
    it('sortAndFormFeaturedData With SurfaceBetModule and QuickLinkModule',()=>{
       const feature = {segmented:true,
        modules:[{'segmentOrder':2,'@type':'SurfaceBetModule','data':[{'segmentOrder':1},{'segmentOrder':2}]} as any,
        {'segmentOrder':1,'@type':'QuickLinkModule','data':[{'segmentOrder':2},{'segmentOrder':1}]} as any]
       } as any;
      component['sortAndFormFeaturedData'](feature);
      expect(feature.modules[0].segmentOrder).toEqual(1);
      expect(feature.modules[1].data[0].segmentOrder).toEqual(1);
    });
    it('sortAndFormFeaturedData With SurfaceBetModule, QuickLinkModule and InplayModule',()=>{
      const feature = {segmented:true,
       modules:[{'segmentOrder':2,'@type':'SurfaceBetModule','data':[{'segmentOrder':1},{'segmentOrder':2}]} as any,
       {'segmentOrder':1,'@type':'QuickLinkModule','data':[{'segmentOrder':2},{'segmentOrder':1}]} as any,
       {'segmentOrder':3,'@type':'InplayModule','data':[{'segmentOrder':2.1},{'segmentOrder':2.5},{'segmentOrder':1.5}]} as any]
      } as any;
     component['sortAndFormFeaturedData'](feature);
     expect(feature.modules[2].segmentOrder).toEqual(3);
     expect(feature.modules[2].data[0].segmentOrder).toEqual(1.5);
   });
    it('sortAndFormFeaturedData WithOut SurfaceBetModule and QuickLinkModule',()=>{
      const feature = {segmented:true,
       modules:[{'segmentOrder':2,'@type':'SurfaceBetModule12','data':[{'segmentOrder':1},{'segmentOrder':2}]} as any,
       {'segmentOrder':1,'@type':'QuickLinkModule12','data':[{'segmentOrder':2},{'segmentOrder':1}]} as any]
      } as any;
      component['sortAndFormFeaturedData'](feature);
     expect(feature.modules[0].segmentOrder).toEqual(1);
   });
    it('sortAndFormFeaturedData WithOut SurfaceBetModule and QuickLinkModule and  without segmented property', () => {
      const feature = {
        modules: [{ 'segmentOrder': 2, '@type': 'SurfaceBetModule12', 'data': [{ 'segmentOrder': 1 }, { 'segmentOrder': 2 }] } as any,
        { 'segmentOrder': 2, '@type': 'QuickLinkModule12', 'data': [{ 'segmentOrder': 2 }, { 'segmentOrder': 1 }] } as any]
      } as any;
      component['sortAndFormFeaturedData'](feature);
      expect(feature.modules[0].segmentOrder).toEqual(2);
    });
    it('sortAndFormFeaturedData WithOut SurfaceBetModule and QuickLinkModule and  with segmented property false', () => {
      const feature = {segmented:false,
        modules: [{ 'segmentOrder': 2, '@type': 'SurfaceBetModule12', 'data': [{ 'segmentOrder': 1 }, { 'segmentOrder': 2 }] } as any,
        { 'segmentOrder': 2, '@type': 'QuickLinkModule12', 'data': [{ 'segmentOrder': 2 }, { 'segmentOrder': 1 }] } as any]
      } as any;
      component['sortAndFormFeaturedData'](feature);
      expect(feature.modules[0].segmentOrder).toEqual(2);
    });
    it('sortAndFormFeaturedData WithOut SurfaceBetModule and QuickLinkModule and with segmented property null', () => {
      const feature = {segmented:null,
        modules: [{ 'segmentOrder': 2, '@type': 'SurfaceBetModule12', 'data': [{ 'segmentOrder': 1 }, { 'segmentOrder': 2 }] } as any,
        { 'segmentOrder': 2, '@type': 'QuickLinkModule12', 'data': [{ 'segmentOrder': 2 }, { 'segmentOrder': 1 }] } as any]
      } as any;
      component['sortAndFormFeaturedData'](feature);
      expect(feature.modules[0].segmentOrder).toEqual(2);
    });
    it('sortAndFormFeaturedData WithOut SurfaceBetModule and QuickLinkModule and with segmented property null', () => {
      const feature = {segmented:'',
        modules: [{ 'segmentOrder': 2, '@type': 'SurfaceBetModule12', 'data': [{ 'segmentOrder': 1 }, { 'segmentOrder': 2 }] } as any,
        { 'segmentOrder': 2, '@type': 'QuickLinkModule12', 'data': [{ 'segmentOrder': 2 }, { 'segmentOrder': 1 }] } as any]
      } as any;
      component['sortAndFormFeaturedData'](feature);
      expect(feature.modules[0].segmentOrder).toEqual(2);
    });
  });

  describe('#checkIfTheUserIsSegmented', () => {
    it('checkIfTheUserIsSegmented segmentReceivedListner called', () => {
      userService.username = 'test';
     component.checkIfTheUserIsSegmented();
     expect(featuredModuleService.segmentReceivedListner).toHaveBeenCalled();
    });
    it('checkIfTheUserIsSegmented segmentReceivedListner did not get called case 1', () => {
      userService.username = '';
     component.checkIfTheUserIsSegmented();
     expect(featuredModuleService.segmentReceivedListner).not.toHaveBeenCalled();
    });
    it('checkIfTheUserIsSegmented segmentReceivedListner did not get called case 2', () => {
      userService.username = '';
     component.checkIfTheUserIsSegmented();
     expect(featuredModuleService.segmentReceivedListner).not.toHaveBeenCalled();
    });
  });
  
  
  describe('#showFreeRideBanner', () => {
    it('isFeaturedUrl called', () => {
      spyOn(component,'isFeaturedUrl');

     component.showFreeRideBanner('url');

     expect(component.isFeaturedUrl).toHaveBeenCalled();
    });
  });

  it('call fetchSurfaceBets', () => {
   component.surfaceBetIds = ['1'];
   component.highlightCarouselIds = ['2'];
   component.featuredModuleData.modules = [
    {
      '@type': "SurfaceBetModule",
      'cashoutAvail': true,
      'data': [
        {
          '@type': "SurfaceBetModuleData",
          'objId': '1'
        },
        {
          '@type': "SurfaceBetModuleData",
          'objId': '2'
        }
      ]
    },
    {
      '@type': "HighlightCarouselModule",
      'cashoutAvail': true,
      '_id': '2'
    },
    {
      '@type': "HighlightCarouselModule",
      'cashoutAvail': true,
      '_id': '3'
    }
   ] as any;
   component.showOnlyBigCompetitionData = true;
   component['fetchSurfaceBets']();
   expect(component.featuredModuleData.modules[0].data.length).toEqual(1);
  });
});