import { NgZone } from '@angular/core';
import { async } from '@angular/core/testing';
import { CarouselMenuComponent } from '@app/lazy-modules/carouselMenu/components/carousel-menu.component';

describe('CarouselMenuComponent', () => {
  let component: CarouselMenuComponent;
  let menuItems;
  let rendererService;
  let servingService;
  let windowRefService;
  let casinoLinkService;
  let pubSubService;
  let gtmService;
  let navigationService;
  let carouselMenuStateService;
  let domTools;
  let elementRef;
  let zone;
  let changeDetectorRef;
  let bonusSuppressionService;
  let rgyellowmenuItems;

  beforeEach(async(() => {
    rendererService = {
      renderer: {
        addClass: jasmine.createSpy(),
        removeClass: jasmine.createSpy(),
        listen: jasmine.createSpy().and.callFake((a, b, cb) => {
          cb();
        })
      }
    };
    servingService = {
      sendExternalCookies: jasmine.createSpy()
    };
    windowRefService = {
      document: {
        addEventListener: jasmine.createSpy(),
        removeEventListener: jasmine.createSpy(),
        apply: jasmine.createSpy(),
        getElementById: jasmine.createSpy('getElementById').and.returnValue({
          classList: {
            add: jasmine.createSpy().and.returnValue('icon-pressed-state'),
            remove: jasmine.createSpy().and.returnValue('icon-default-state')
          }
        }),
        documentElement: {
          scrollTop: 0
        },
        body: {
          scrollTop: 0
        }
      },
      nativeWindow: {
        open: jasmine.createSpy('open'),
        pageYOffset: 20
      }
    };
    domTools = {
      HeaderEl: {
        clientHeight: 300,
        nativeElement: { tagName: 'header' }
      },
      getElementBottomPosition: jasmine.createSpy('getElementBottomPosition').and.returnValue(120),
      getElementTopPosition: jasmine.createSpy('getElementTopPosition').and.returnValue(90),
    };
    casinoLinkService = {
      decorateCasinoLink: jasmine.createSpy('decorateCasinoLink').and.callFake(data => data)
    };
    pubSubService = {
      subscribe: jasmine.createSpy('subscribe').and.callFake((subscriberName, channel, cb) => cb()),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: {
        EVENT_COUNT: 'EVENT_COUNT',
        SESSION_LOGIN: 'SESSION_LOGIN',
        SESSION_LOGOUT: 'SESSION_LOGOUT'
      }
    };
    gtmService = {
      push: jasmine.createSpy()
    };
    navigationService = {
      isAbsoluteUri: () => true,
      redirect: jasmine.createSpy('redirect'),
      openUrl: jasmine.createSpy('openUrl')
    };

    carouselMenuStateService = {
      carouselStick$: {
        subscribe: jasmine
          .createSpy('subscribe')
          .and.returnValue(jasmine.createSpyObj('Subscription', ['unsubscribe']))
      }
    };

    rgyellowmenuItems = [
      {
        alt: 'All Sports',
        categoryId: 0,
        disabled: false,
        iconClass: '',
        id: '1',
        imageTitle: 'All Sports',
        inApp: true,
        isTopSport: true,
        showInAZ: false,
        showInHome: true,
        showInPlay: true,
        sportName: 'az-sports',
        svg: '<?xml version="1.0"?><svg><rect height="1" width="1" x="0" y="0"></rect></svg>',
        svgId: '#icon-A-ZSports',
        targetUri: '/az-sports',
        targetUriCopy: 'az-sports',
        topSport: true
      },
      {
        alt: 'All Sports',
        categoryId: 0,
        disabled: false,
        iconClass: '',
        id: '1',
        imageTitle: '5-a-side',
        inApp: true,
        isTopSport: true,
        showInAZ: false,
        showInHome: true,
        showInPlay: true,
        sportName: '5-a-side',
        svg: '<?xml version="1.0"?><svg><rect height="1" width="1" x="0" y="0"></rect></svg>',
        svgId: '#icon-A-ZSports',
        targetUri: '/5-a-side',
        targetUriCopy: '5-a-side',
        topSport: true
      }];

    menuItems = [
      {
        alt: 'All Sports',
        categoryId: 0,
        disabled: false,
        iconClass: '',
        id: '1',
        imageTitle: 'All Sports',
        inApp: true,
        isTopSport: true,
        showInAZ: false,
        showInHome: true,
        showInPlay: true,
        sportName: 'az-sports',
        svg: '<?xml version="1.0"?><svg><rect height="1" width="1" x="0" y="0"></rect></svg>',
        svgId: '#icon-A-ZSports',
        targetUri: '/az-sports',
        targetUriCopy: 'az-sports',
        topSport: true
      },
      {
        alt: '',
        categoryId: 2,
        disabled: false,
        iconClass: '',
        id: '2',
        imageTitle: 'Any title',
        inApp: true,
        isTopSport: false,
        showInAZ: true,
        showInHome: true,
        showInPlay: true,
        sportName: 'sport/name',
        svg: null,
        svgId: null,
        targetUri: '/sport/url',
        targetUriCopy: 'sport/url',
        topSport: false
      },
      {
        categoryId: 3,
        disabled: true,
        hidden: false,
        id: '3'
      },
      {
        categoryId: 4,
        disabled: false,
        hidden: true,
        id: '4'
      },
      {
        categoryId: 5,
        disabled: false,
        hidden: false,
        id: '5',
        inApp: true,
        targetUri: 'http://some/external/lnk'
      },
      {
        categoryId: 6,
        disabled: false,
        hidden: false,
        id: '6',
        inApp: false,
        targetUri: 'http://some/inner/link'
      },
      {
        categoryId: 7,
        disabled: false,
        hidden: false,
        id: '7',
        inApp: true,
        targetUri: '/some/external/link'
      },
      {
        categoryId: 8,
        disabled: false,
        hidden: false,
        id: '8',
        inApp: false,
        targetUri: '/some/external/link'
      }
    ];
    elementRef = {
      nativeElement: {
        offsetHeight: '100',
        offsetTop: '50'
      }
    };

    changeDetectorRef = {
      markForCheck: jasmine.createSpy('markForCheck'),
      detectChanges: jasmine.createSpy('detectChanges'),
    };

    zone = NgZone;

    bonusSuppressionService = {
      checkIfYellowFlagDisabled: jasmine.createSpy('checkIfYellowFlagDisabled').and.returnValue(true)
    }

    component = new CarouselMenuComponent(
      windowRefService,
      rendererService,
      servingService,
      casinoLinkService,
      pubSubService,
      gtmService,
      navigationService,
      carouselMenuStateService,
      zone,
      elementRef,
      changeDetectorRef,
      domTools,
      bonusSuppressionService
    );

    component.isSticky = true;
    component['lastScrollPosition'] = 0;
    component['forceVisibility'] = true;
  }));

  describe('#ngOnInit', () => {
    beforeEach(() => {
      component.isHidden = false;
      component.menuItems = menuItems;
      zone.runOutsideAngular = jasmine.createSpy('runOutsideAngular').and.callFake(cb => cb());
    });

    it('Not empty menu items:', () => {
      pubSubService.subscribe.and.callFake((p1, p2, cb) => cb('eventName'));
      component['filterCarouselBasedOnRgyellow'] = jasmine.createSpy('filterCarouselBasedOnRgyellow');
      component.isLiveCounter = true;
      component.ngOnInit();

      expect(casinoLinkService.decorateCasinoLink).toHaveBeenCalledWith(menuItems);
      expect(component.menuItems.length).toEqual(6);
      expect(component.isAvailable).toEqual(true);
      expect(pubSubService.subscribe).toHaveBeenCalledWith('CarouselMenu', 'EVENT_COUNT', jasmine.any(Function));
      expect(pubSubService.subscribe).toHaveBeenCalledWith('CarouselMenu', ['SESSION_LOGIN', 'SESSION_LOGOUT'], jasmine.any(Function));
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
      expect(component['eventName']).toEqual('eventName');
    });

    it('Empty menu items:', () => {
      menuItems = [{
        categoryId: 3,
        disabled: true,
        hidden: false,
        id: '1'
      }] as any;
      component['filterCarouselBasedOnRgyellow'] = jasmine.createSpy('filterCarouselBasedOnRgyellow');
      component.menuItems = menuItems;
      component.isLiveCounter = false;

      component.ngOnInit();

      expect(casinoLinkService.decorateCasinoLink).toHaveBeenCalledWith(menuItems);
      expect(component.menuItems).toEqual([]);
      expect(component.isAvailable).toEqual(false);
      expect(component['eventName']).toEqual(undefined);
      expect(pubSubService.subscribe).not.toHaveBeenCalledWith('CarouselMenu', 'EVENT_COUNT', jasmine.any(Function));
      expect(pubSubService.subscribe).toHaveBeenCalledWith('CarouselMenu', ['SESSION_LOGIN', 'SESSION_LOGOUT'], jasmine.any(Function));
    });

    afterEach(() => {
      expect(component['carouselStickSubscription']).toBeDefined();
      expect(zone.runOutsideAngular).toHaveBeenCalledWith(jasmine.any(Function));
      expect(carouselMenuStateService.carouselStick$.subscribe).toHaveBeenCalled();
    });
  });

  describe('ngOnChanges', () => {
     it('should filter menuItems', (done: DoneFn) => {
      component.menuItems = rgyellowmenuItems;
      const changes: any = {
        menuItems: true
      };
      changeDetectorRef.detectChanges= jasmine.createSpy(),
      component.ngOnChanges(changes);
      expect(component.menuItems.length).toEqual(2);
      done();
    });
    it('should not filter menuItems', () => {
      component.menuItems = rgyellowmenuItems;
      const changes: any = {
        menuItems: false
      };
      changeDetectorRef.detectChanges= jasmine.createSpy(),
      component.ngOnChanges(changes);
      expect(component.menuItems.length).toEqual(2);
    });

    it('should not filter activeMenuItem', () => {
      component.activeMenuItem = rgyellowmenuItems;
      const changes: any = {
        activeMenuItem: true
      };
      component.ngOnChanges(changes);
      expect(component.activeMenuItem).toBeTruthy();
    });
  });

  describe('@ngOnDestroy', () => {
    beforeEach(() => {
      component.menuItems = menuItems;
    });

    it('should not call scrollListener', () => {
      component.ngOnInit();
      component['scrollListener'] = null;

      component.ngOnDestroy();
    });

    it('should call scrollListener', () => {
      component.ngOnInit();
      component['scrollListener'] = jasmine.createSpy('scrollListener').and.callThrough();

      component.ngOnDestroy();

      expect(component['scrollListener']).toHaveBeenCalled();
    });

    afterEach(() => {
      expect(pubSubService.unsubscribe).toHaveBeenCalledWith('CarouselMenu');
      expect(component['forceVisibility']).toEqual(false);
      expect(component['carouselStickSubscription'].unsubscribe).toHaveBeenCalled();
    });
  });

  describe('buttonAction', () => {
    let mouseEvent;
    let item;

    beforeEach(() => {
      mouseEvent = jasmine.createSpyObj('mouseEvent', ['preventDefault']);
      item = {
        targetUri: '',
        inApp: false,
        imageTitle: 'title',
        relUri: 'https://rel'
      };
    });

    it('should call iconDefaultState', () => {
      const item = {
        targetUri: 'icon-default-state',
        imageTitle: 'icon-default-state'
      } as any
      component.iconDefaultState(mouseEvent, item, 1);
      expect(mouseEvent.preventDefault).toHaveBeenCalled();
      expect(windowRefService.document.getElementById).toHaveBeenCalledWith('icon-default-state');
    })

    it('should add buttonAction on click', () => {
      component.buttonAction(mouseEvent, item, 1);

      expect(mouseEvent.preventDefault).toHaveBeenCalled();
      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
        eventCategory: 'navigation',
        eventAction: 'main',
        eventLabel: item.imageTitle,
        position: 1
      });
      expect(servingService.sendExternalCookies).toHaveBeenCalledWith(item.relUri);
      expect(navigationService.openUrl).toHaveBeenCalledWith(item.targetUri, item.inApp, false);
    });

    it('should scroll to top on buttonAction', () => {
      component.isTopScroll = true;
      component.buttonAction(mouseEvent, item, 1);

      expect(navigationService.openUrl).toHaveBeenCalledWith(item.targetUri, item.inApp, true);
    });
  });

  describe('trackByFn', () => {
    it('should return provided index', () => {
      expect(component.trackByFn(2)).toEqual(2);
    });
  });

  describe('@ngAfterViewInit', () => {
    beforeEach(() => {
      component['setSticky'] = jasmine.createSpy('setSticky').and.callThrough();
    });

    it('should set sticky menu on scroll', () => {
      component['forceVisibility'] = false;
      component.ngAfterViewInit();

      expect(rendererService.renderer.listen).toHaveBeenCalled();
      expect(component['setSticky']).toHaveBeenCalled();
    });

    it('should not  set sticky menu on scroll', () => {
      component.ngAfterViewInit();

      expect(rendererService.renderer.listen).toHaveBeenCalled();
      expect(component['setSticky']).not.toHaveBeenCalled();
    });

    it('should not set sticky menu on scroll', () => {
      component.isSticky = false;
      component.ngAfterViewInit();

      expect(rendererService.renderer.listen).not.toHaveBeenCalled();
      expect(component['setSticky']).not.toHaveBeenCalled();
    });

    afterEach(() => {
      expect(component['lastScrollPosition']).toEqual(0);
    });
  });

  describe('@eventCount', () => {
    let event,
      result;

    beforeEach(() => {
      event = {
        liveEventCount: 1,
        upcomingEventCount: 2
      };
      component['eventName'] = '';
      component['eventNameConst'] = {
        live: '2',
        upcoming: '2'
      } as any;
    });

    it('should return event.liveEventCount', () => {
      result = component.eventCount(event);

      expect(result).toEqual(1);
    });

    it('should return event.upcomingEventCount', () => {
      event.liveEventCount = 0;
      result = component.eventCount(event);

      expect(result).toEqual(2);
    });

    it('should return 0', () => {
      event.liveEventCount = 0;
      event.upcomingEventCount = 0;
      result = component.eventCount(event);

      expect(result).toEqual(0);
    });
  });

  it('should call iconPressedState', () => {
    const item = {
      targetUri: 'icon-pressed-state',
      imageTitle: 'icon-pressed-state'
    }
    component.iconPressedState(item);
    expect(windowRefService.document.getElementById).toHaveBeenCalledWith('icon-pressed-state');
  })

  it('to call menuScrolled method', () => {
    const isScrollEnabled = false
    component.menuScrolled();
    expect(isScrollEnabled).toBeTrue;
  })

  describe('@setSticky', () => {
    beforeEach(() => {
      component['lastScrollPosition'] = 0;
      component.isHidden = false;
    });

    it('should return isHidden = true', () => {
      component['setSticky']();

      expect(component.isHidden).toEqual(true);
      expect(component['lastScrollPosition']).toEqual(20);
    });

    it('should return isHidden = false', () => {
      component.isHidden = true;
      component['lastScrollPosition'] = 40;
      windowRefService.nativeWindow.pageYOffset = 0;
      windowRefService.document.documentElement.scrollTop = 10;

      component['setSticky']();

      expect(component.isHidden).toEqual(false);
      expect(component['lastScrollPosition']).toEqual(10);
    });

    it('should return isHidden = false', () => {
      component['lastScrollPosition'] = 40;
      windowRefService.nativeWindow.pageYOffset = 0;
      elementRef.nativeElement.offsetTop = 150;
      windowRefService.document.body.scrollTop = 30;

      component['setSticky']();

      expect(component.isHidden).toEqual(false);
      expect(component['lastScrollPosition']).toEqual(30);
    });

    it('should return isHidden = true', () => {
      component['lastScrollPosition'] = 40;
      windowRefService.nativeWindow.pageYOffset = 0;
      elementRef.nativeElement.offsetTop = 150;
      windowRefService.document.body.scrollTop = 230;

      component['setSticky']();

      expect(component.isHidden).toEqual(true);
      expect(component['lastScrollPosition']).toEqual(230);
    });

    it('should return isHidden = true', () => {
      windowRefService.nativeWindow.pageYOffset = 0;
      windowRefService.document.documentElement.scrollTop = 10;
      component['lastScrollPosition'] = 5;
      component.isHidden = true;

      component['setSticky']();

      expect(component.isHidden).toEqual(true);
      expect(component['lastScrollPosition']).toEqual(10);
    });

    it('should return isHidden = false', () => {
      windowRefService.nativeWindow.pageYOffset = 0;
      component['lastScrollPosition'] = 5;
      component.isHidden = true;

      component['setSticky']();

      expect(component.isHidden).toEqual(false);
      expect(component['lastScrollPosition']).toEqual(0);
    });
  });

  describe('#filterCarouselBasedOnRgyellow, should filterout carousel links  based on rgYellow status',() =>{
    it('filterCarouselBasedOnRgyellow should filter out links with rgYellow true', () =>{
      component.menuItems = menuItems;
      component.filterCarouselBasedOnRgyellow();
      expect(component.menuItems).toEqual(menuItems);
    })
  });
});
