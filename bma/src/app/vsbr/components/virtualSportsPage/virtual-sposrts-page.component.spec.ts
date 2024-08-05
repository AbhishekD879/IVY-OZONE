import { of, of as observableOf, Subject, Subscription, throwError } from 'rxjs';
import { NavigationEnd } from '@angular/router';
import { fakeAsync, discardPeriodicTasks, tick } from '@angular/core/testing';
import { VirtualSportsPageComponent } from '@app/vsbr/components/virtualSportsPage/virtual-sports-page.component';
import { IVirtualCategoryStructure, IVirtualChildCategory } from '@app/vsbr/models/virtual-sports-structure.model';
import { ISportEventEntity } from '@core/models/sport-event-entity.model';
import { SPRITE_PATH } from '@bma/constants/image-manager.constant';

describe('VirtualSportsPageComponent', () => {
  let component: VirtualSportsPageComponent;
  let virtualMenuDataService;
  let virtualSportsService;
  let pubsub;
  let filterService;
  let router;
  let route;
  let localStorageMapperService;
  let navigationService;
  let asyncScriptLoaderService;
  let cmsService, changeDetectorRef, virtualHubService;
  const iconsSubject = new Subject();
  const fakeSubscription: Subscription = new Subscription();

  const child = {
    id: '5e85e070c9e77c0001805f6b',
    title: 'Inspired Cycling',
    classId: '287',
    streamUrl: 'streamUrl',
    numberOfEvents: 4,
    alias: 'inspired-cycling-test',
    startTimeUnix: 1586360520000,
    timeLeft: -1897,
    events: [{} as ISportEventEntity],
    ventAliases: {},
    showRunnerImages: false,
    showRunnerNumber: false,
    targetUri: ''
  } as IVirtualChildCategory;
  const childs = new Map<string | number, IVirtualChildCategory>();
  childs.set(child.classId, child);

  const mock = [
    {
      id: '5e85df97c9e77c0001d62999',
      title: 'Motorsports',
      svgId: '#icon-motor-bikes',
      svg: 'svgIcon',
      tracks: [],
      ctaButtonUrl: '/motorsports',
      ctaButtonText: 'THIS CONFIG!!!!',
      alias: 'motorsports',
      targetUri: '/virtual-sports/motorsports/СТЕПЛЕР',
      childs: childs
    } as IVirtualCategoryStructure
  ] as IVirtualCategoryStructure[];

  beforeEach(() => {

    pubsub = {
      subscribe: jasmine.createSpy().and.callFake((p1, p2, cb) => {
        cb({
          eventName: 'category-update-288',
          classId: 287,
          actionType: 'category-update'
        });
      }),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: {
        RELOAD_COMPONENTS: 'RELOAD_COMPONENTS'
      }
    };

    filterService = {
      date: jasmine.createSpy()
    };

    router = {
      navigate: jasmine.createSpy().and.returnValue(fakeSubscription),
      events: of(new NavigationEnd(1, '/', '/')),
    };

    navigationService = {
      openUrl: jasmine.createSpy()
    };

    const urlSubject = new Subject();

    route = {
      url: urlSubject,
      navigateByUrl: jasmine.createSpy(),
      snapshot: {
        params: [],
        children: []
      },
      children: [
        {
          url: urlSubject,
          navigateByUrl: jasmine.createSpy(),
          snapshot: {
            params: [
              {
                category: 'horse',
                alias: 'horse',
                eventId: null
              }
            ]
          },
          data: {
            allowAnonymous: true,
            product: 'host',
            segment: 'virtual-sports.class'
          },
          children: []
        }
      ]
    };

    localStorageMapperService = {
      init: jasmine.createSpy()
    };

    virtualSportsService = {
      addLiveServeUpdateEventListener: jasmine.createSpy('addLiveServeUpdateEventListener'),
      removeLiveServeUpdateEventListener: jasmine.createSpy('removeLiveServeUpdateEventListener'),
      time: {
        subscribe: jasmine.createSpy('subscribe').and.callFake((callback) => callback()),
      },
      eventsData: jasmine.createSpy().and.returnValue(observableOf(mock)),
      subscribeForUpdates: jasmine.createSpy(),
      updateCategoryClasses: jasmine.createSpy(),
      unsubscribeFromUpdates: jasmine.createSpy(),
      setIsReloaded: jasmine.createSpy('setIsReloaded'),
      isReloaded: jasmine.createSpy('isReloaded').and.returnValue(false)
    };

    virtualMenuDataService = {
      getParentIndex: jasmine.createSpy('getParentIndex').and.returnValue(1),
      getChildIndex: jasmine.createSpy('getParentIndex').and.returnValue(0),
      setActiveParentIndex: jasmine.createSpy('getParentIndex').and.returnValue(1),
      destroy: () => { },
      hasParentAndChild: () => { }
    };

    asyncScriptLoaderService = {
      getSvgSprite: jasmine.createSpy('getSvgSprite').and.returnValue(iconsSubject)
    };

    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(of({VirtualHubHomePage: {
        enabled: true,otherSports: false,topSports: false, featureZone: false,headerBanner: false, nextEvents: false
      }}))
    }

    changeDetectorRef = {
      detectChanges:  jasmine.createSpy('detectChanges').and.callThrough()
    }

    virtualHubService = {
      triggerGTATracking:  jasmine.createSpy('triggerGTATracking').and.returnValue(true)
    }

    component = new VirtualSportsPageComponent(pubsub, filterService, localStorageMapperService, virtualSportsService,
      router, route, virtualMenuDataService, navigationService, asyncScriptLoaderService,cmsService, changeDetectorRef, virtualHubService);
  });

  it('should call updateCategoryClasses for ngOnInit if parentCategory.childs is not empty', fakeAsync(() => {
    component.ngOnInit();

    tick(1000);

    expect(virtualSportsService.updateCategoryClasses).toHaveBeenCalledWith(child.events, child);

    discardPeriodicTasks();
  }));

  it('should create VirtualSportsPageComponent instance', () => {
    expect(component).toBeTruthy();
  });

  it('should call @ngOnInit', fakeAsync(() => {
    component.ngOnInit();

    tick(1000);

    expect(virtualSportsService.eventsData).toHaveBeenCalled();
    expect(virtualSportsService.subscribeForUpdates).toHaveBeenCalled();
    expect(pubsub.subscribe).toHaveBeenCalledWith('virtualSport', 'INSOMNIA', jasmine.any(Function));
    expect(pubsub.subscribe).toHaveBeenCalledWith('VirtualSportsCtrl', 'RELOAD_COMPONENTS', jasmine.any(Function));
    expect(virtualSportsService.setIsReloaded).toHaveBeenCalledWith(true);
    discardPeriodicTasks();
  }));

  it('should call @reload', () => {
    component['timerSubscription'] = {
      unsubscribe: jasmine.createSpy()
    } as any;
    virtualSportsService.isReloaded = jasmine.createSpy('isReloaded').and.returnValue(true);
    component.ngOnInit = jasmine.createSpy('ngOnInit').and.callThrough();
    component['reload']();
    expect(virtualSportsService.setIsReloaded).toHaveBeenCalledWith(false);
  });

  it('should call @ngOnDestroy', () => {
    component['routeChangeSuccessHandler'] = {
      unsubscribe: jasmine.createSpy()
    } as any;
    component['virtualSportsEventsSubscription'] = {
      unsubscribe: jasmine.createSpy()
    } as any;
    component['timerSubscription'] = {
      unsubscribe: jasmine.createSpy()
    } as any;
    component['eventsDataSub'] = {
      unsubscribe: jasmine.createSpy()
    } as any;
    component.showSpinner = jasmine.createSpy();
    component.ngOnDestroy();

    expect(component['timerSubscription'].unsubscribe).toHaveBeenCalled();
    expect(virtualSportsService.removeLiveServeUpdateEventListener).toHaveBeenCalled();
    expect(pubsub.unsubscribe).toHaveBeenCalledWith('VirtualSportsCtrl');
    expect(virtualSportsService.unsubscribeFromUpdates).toHaveBeenCalled();
    expect(component['routeChangeSuccessHandler'].unsubscribe).toHaveBeenCalled();
  });

  it('should call @cateTopSportMenu', () => {
    component['createTopSportMenu'](mock);
    expect(component.parentMenuItems.length).toEqual(1);
  });

  describe('@updateActiveTab', () => {
    it('should call updateActiveTab with no data', () => {
      route.children = null;
      component.ngOnInit();
      expect(component.activeParent).not.toBeDefined();
    });

    it('should call updateActiveTab() when hasParentAndChild=true', () => {
      virtualMenuDataService.hasParentAndChild = jasmine.createSpy('hasParentAndChild').and.returnValue(true);
      component.ngOnInit();
      expect(component.activeParent).toBeDefined();
    });

    it('should call updateActiveTab() to check activeParent, activeChild', () => {
      virtualMenuDataService.hasParentAndChild = jasmine.createSpy('hasParentAndChild').and.returnValue(true);
      virtualMenuDataService.getParentIndex = jasmine.createSpy('getParentIndex').and.returnValue(-1);
      virtualMenuDataService.getChildIndex = jasmine.createSpy('getChildIndex').and.returnValue(-1);
      component['setActiveMenuElement'] = jasmine.createSpy('setActiveMenuElement');
      component['checkAndRedirect'] = jasmine.createSpy();
      component.ngOnInit();
      component['updateActiveTab']();

      expect(component['setActiveMenuElement']).toHaveBeenCalled();
      expect(component['checkAndRedirect']).toHaveBeenCalled();
      expect(component.activeParent).toBe(0);
      expect(component.activeChild).toBe(0);
    });

    it('should set parentOrChildHasChanged variable to true', () => {
      route.children = [{
        snapshot: { params: { alias: 'vr', category: 'Motorsports' } }
      }];
      virtualMenuDataService.hasParentAndChild = jasmine.createSpy('hasParentAndChild').and.returnValue(true);
      virtualMenuDataService.getParentIndex = jasmine.createSpy('getParentIndex').and.returnValue(-1);
      virtualMenuDataService.getChildIndex = jasmine.createSpy('getChildIndex').and.returnValue(-1);
      component['setActiveMenuElement'] = jasmine.createSpy('setActiveMenuElement');
      component['checkAndRedirect'] = jasmine.createSpy();
      component.ngOnInit();
      component['updateActiveTab']();

      expect(component['setActiveMenuElement']).toHaveBeenCalled();
      expect(component['checkAndRedirect']).toHaveBeenCalled();
      expect(component.activeParent).toBe(0);
      expect(component.activeChild).toBe(0);
    });

    it('should check and redirect params.eventId', () => {
      component['setActiveMenuElement'] = jasmine.createSpy('setActiveMenuElement');
      spyOn(component as any, 'checkAndRedirect');
      route.children = [{
        snapshot: { params: { alias: 'vr', eventId: '1' } }
      }];
      virtualMenuDataService.hasParentAndChild = jasmine.createSpy().and.returnValue(true);
      component['updateActiveTab']();

      expect(component['setActiveMenuElement']).toHaveBeenCalled();
      expect(component['checkAndRedirect']).not.toHaveBeenCalled();
    });
  });

  describe('Test error section for virtualSportsService.eventsData()', () => {
    it('should call error', () => {
      virtualSportsService.eventsData.and.returnValue(throwError('error'));
      component.ngOnInit();

      expect(component.parentMenuItems).not.toBeDefined();
    });

    it('should check when error=noCategories', () => {
      virtualSportsService.eventsData.and.returnValue(throwError('noCategories'));
      component.ngOnInit();

      expect(component.parentMenuItems).toEqual([]);
    });

    it('shoul call showError() when no categories', () => {
      const mockError = [];
      component.showError = jasmine.createSpy('showError');
      virtualSportsService.eventsData.and.returnValue(observableOf(mockError));
      component.ngOnInit();

      expect(component.showError).toHaveBeenCalled();
    });
  });

  it('should check data.actionType', () => {
    pubsub.subscribe = jasmine.createSpy().and.callFake((p1, p2, cb) => {
      cb({
        eventName: null,
        classId: null,
        actionType: null
      });
    });
    component.ngOnInit();

    expect(component.parentMenuItems.length).toEqual(0);
  });

  it('shoud call addListeners() and add live serve event listener', () => {
    router.events = observableOf(null);
    component.ngOnInit();
    component['addListeners']();

    expect(virtualSportsService.addLiveServeUpdateEventListener).toHaveBeenCalled();
  });

  describe('Test parentCategory and childCategory', () => {
    let parentCategory: IVirtualCategoryStructure;
    const childItem = {
      id: '5e85e070c9e77c0001805f6b',
      title: 'Inspired Cycling',
      classId: '287',
      streamUrl: 'zz',
      numberOfEvents: 4,
      alias: 'inspired-cycling',
      startTimeUnix: undefined,
      timeLeft: undefined,
      events: [{
        'event': 'event'
      }]
    };
    const parentCategories = [];

    beforeEach(() => {
      parentCategory = {
        id: '5e85df97c9e77c0001d62999',
        title: 'Motorsports',
        tracks: [],
        svgId: '#icon-motor-bikes',
        svg: '',
        ctaButtonUrl: 'DO NOT TOUCH',
        ctaButtonText: 'THIS CONFIG!!!!',
        alias: 'motorsports',
        targetUri: '/virtual-sports/motorsports'
      } as any;
      parentCategories.push(parentCategory);
    });

    it('should check if parentCategory.childs is empty for ngOnInit and createTopSportMenu()', () => {
      parentCategories[0].childs = new Map();
      virtualSportsService.eventsData.and.returnValue(observableOf(parentCategories));
      component.ngOnInit();
      component['createTopSportMenu'](parentCategories);

      expect(virtualMenuDataService.menu).toBeDefined();
      expect(virtualSportsService.updateCategoryClasses).not.toHaveBeenCalled();
    });

    it('should call timerHandler() if parentCategory.childs is empty ', () => {
      component.categories = parentCategories;
      component['getLabel'] = jasmine.createSpy();
      component['timerHandler']();

      expect(component['getLabel']).not.toHaveBeenCalled();
    });

    describe('Test timeLeft', () => {

      it('should check child timeLeft for updateCategoryClasses', () => {
        const localChildTest = new Map();
        localChildTest.set(childItem.classId, childItem);
        parentCategories[0].childs = localChildTest;
        virtualSportsService.eventsData.and.returnValue(observableOf(parentCategories));
        component.ngOnInit();

        expect(virtualSportsService.updateCategoryClasses).not.toHaveBeenCalled();
      });

      it('should call timerHandler() if childCategory.timeLeft is undefined ', () => {
        const localChildTest = new Map();
        localChildTest.set(childItem.classId, childItem);
        component['getLabel'] = jasmine.createSpy();
        component.categories = [{ ...parentCategory, childs: localChildTest }];
        component['timerHandler']();

        expect(component['getLabel']).not.toHaveBeenCalled();
      });

      it('should call getLabel() when timeLeft is 0', () => {
        component['getLabel'](0);

        expect(virtualMenuDataService.menu).not.toBeDefined();
        expect(filterService.date).toHaveBeenCalled();
      });
    });
  });

  describe('@setActiveMenuElement', () => {
    let parentMock: any;

    beforeEach(() => {
      parentMock = [
        {
          name: 'Motorsports',
          inApp: true,
          svgId: '#icon-motor-bikes',
          svg: 'svgIcon',
          targetUri: '/virtual-sports/motorsports',
          targetUriSegment: 'motorsports',
          priority: 0,
          displayOrder: 0,
          childMenuItems: [
            {
              name: 'Inspired Cycling',
              inApp: true,
              svgId: '',
              targetUri: '/virtual-sports/motorsports/inspired-cycling-test',
              targetUriSegment: 'inspired-cycling-test',
              priority: 0,
              numberOfEvents: 4,
              displayOrder: 1,
              alias: 'inspired-cycling-test',
              streamUrl: 'streamUrl',
              label: {
                className: 'vс-live',
                text: 'Live'
              }
            }
          ],
          alias: 'motorsports'
        }
      ];
    });

    it('it should set active parent and child categories if input data are valid', () => {
      virtualMenuDataService.menu = parentMock;
      component['setActiveMenuElement'](0, 0);

      expect(parentMock[0].isActive).toBeTruthy();
      expect(parentMock[0].childMenuItems[0].isActive).toBeTruthy();
    });

    it('it should set only active parent if child categories is empty', () => {
      parentMock[0].childMenuItems = [];
      virtualMenuDataService.menu = parentMock;
      component['setActiveMenuElement'](0, 0);

      expect(parentMock[0].isActive).toBeTruthy();
      expect(parentMock[0].childMenuItems.length).toBeFalsy();
    });

    it('it shouldn\'t set active parent and child categories if menu is empty', () => {
      virtualMenuDataService.menu = [];
      component['setActiveMenuElement'](0, 0);

      expect(parentMock[0].isActive).toBeUndefined();
      expect(parentMock[0].childMenuItems[0].isActive).toBeUndefined();
    });

    it('it should set to first parent and first child active status if active parent and child inputs are less then 0', () => {
      virtualMenuDataService.menu = parentMock;
      component['setActiveMenuElement'](-1, -1);

      expect(parentMock[0].isActive).toBeTruthy();
      expect(parentMock[0].childMenuItems[0].isActive).toBeTruthy();
    });
  });

  describe('@checkAndRedirect', () => {
    let parentMock: any;

    beforeEach(() => {
      parentMock = [
        {
          name: 'Motorsports',
          inApp: true,
          svgId: '#icon-motor-bikes',
          svg: 'svgIcon',
          targetUri: '/virtual-sports/motorsports',
          targetUriSegment: 'motorsports',
          priority: 0,
          displayOrder: 0,
          childMenuItems: [
            {
              name: 'Inspired Cycling',
              isActive: true,
              inApp: true,
              svgId: '',
              targetUri: '/virtual-sports/motorsports/inspired-cycling-test',
              targetUriSegment: 'inspired-cycling-test',
              priority: 0,
              numberOfEvents: 4,
              displayOrder: 1,
              alias: 'inspired-cycling-test',
              streamUrl: 'streamUrl',
              label: {
                className: 'vс-live',
                text: 'Live'
              }
            }
          ],
          isActive: true,
          alias: 'motorsports'
        }
      ];
    });
    it('should redirect to parent if it was changed', () => {
      component.parentMenuItems = parentMock;
      virtualMenuDataService.menu = parentMock;

      router.url = '/virtual-sports';
      component['activeParent'] = 0;
      component['activeChild'] = 0;
      component.isVirtualHomeDisabled = true;
      component['checkAndRedirect'](true);

      expect(navigationService.openUrl).toHaveBeenCalledWith('/virtual-sports/sports/motorsports', true, true);
    });

    it('should redirect to parent if it was changed', () => {
      component.parentMenuItems = parentMock;
      virtualMenuDataService.menu = parentMock;

      router.url = '/virtual-sports';
      component['activeParent'] = 0;
      component['activeChild'] = 0;
      component.isVirtualHomeDisabled = false;
      component['checkAndRedirect'](true);

      expect(navigationService.openUrl).toHaveBeenCalledWith('/virtual-sports/sports/motorsports/inspired-cycling-test', true, true);
    });

    it('should redirect to child if parent didnt changed', () => {
      router.url = '/virtual-sports';
      component['activeParent'] = 0;
      component['activeChild'] = 0;
      component.ngOnInit();

      component['checkAndRedirect'](false);

      expect(navigationService.openUrl).not.toHaveBeenCalledWith('/virtual-sports/motorsports', true, true);
    });

    it('should check if !path.includes(parentSegment)', () => {
      router.url = '/virtual-sports/motorsports/';
      component.isVirtualHomeDisabled = true;
      component.ngOnInit();
      component['checkAndRedirect'](false);

      expect(navigationService.openUrl).toHaveBeenCalledWith('/virtual-sports/sports/undefined/undefined', false, true);
    });

    it('should check if !path.includes(childSegment)', () => {
      virtualMenuDataService.menu = parentMock;
      component.parentMenuItems = parentMock;

      router.url = '/virtual-sports/motorsports/';
      component['activeParent'] = 0;
      component['activeChild'] = 0;
      component.isVirtualHomeDisabled = true;
      component['checkAndRedirect'](false);

      expect(navigationService.openUrl).toHaveBeenCalledWith('/virtual-sports/sports/motorsports/inspired-cycling-test', true, true);
    });

    it('should check if !path.includes(childSegment)', () => {
      virtualMenuDataService.menu = parentMock;
      component.parentMenuItems = parentMock;
      console.log('parentMock', parentMock)
      parentMock[0].childMenuItems[0].alias = 'motorsports';
      child.alias = 'motorsports'
      router.url = '/virtual-sports/motorsports/motorsports';
      component['activeParent'] = 0;
      component['activeChild'] = 0;
      component.isVirtualHomeDisabled = true;
      component['checkAndRedirect'](false);
      parentMock[0].childMenuItems[0].alias = 'inspired-cycling-test';

    });

  });

  it('should set virtual icons', fakeAsync(() => {
    expect(component.virtualIcons).toBeUndefined();
    expect(asyncScriptLoaderService.getSvgSprite).toHaveBeenCalledWith(SPRITE_PATH.virtual);
    iconsSubject.next('icons');
    tick();

    expect(component.virtualIcons).toEqual('icons');
  }));

  describe('virtualHomepageCheck', () => {
    it('virtualHomepageCheck', fakeAsync(() => {
      component['virtualHomepageCheck']();
      tick();
      expect(component.isVirtualHomeDisabled).toBeTruthy();
    }))
  })

  
  describe('isTwice', () => {
    it('isTwice', () => {
      const retVal = component['isTwice']('virtual-sports/national-chase/national-chase', 'national-chase');
      expect(retVal).toBeTruthy();
    })

    it('isTwice falsy case', () => {
      const retVal = component['isTwice']('virtual-sports/national-chase', 'national-chase');
      expect(retVal).toBeFalsy();
    })
  })
});
