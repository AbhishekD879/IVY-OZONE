import { TimelineComponent } from '@lazy-modules/timeline/components/timeline/timeline.component';
import { of as observableOf, of } from 'rxjs';
import { NavigationEnd } from '@angular/router';
import { TIMELINE_EVENTS } from '@lazy-modules/timeline/constants/timeline.constant';
import { fakeAsync, tick } from '@angular/core/testing';
import environment from '@environment/oxygenEnvConfig';

describe('TimelineComponent', () => {
  let component;
  let cms;
  let router;
  let timelineService;
  let changeDetectorRef;
  let pubSubService;
  let userService;
  let asyncScriptLoaderService;
  let windowRefService;
  let rendererService;
  let locale;

  beforeEach(() => {
    timelineService = {
      connect: jasmine.createSpy('connect').and.returnValue(of({})),
      addListener: jasmine.createSpy('addListener'),
      removeListener: jasmine.createSpy('removeListener'),
      disconnect: jasmine.createSpy('disconnect'),
      emit: jasmine.createSpy('emit'),
      createSocket: jasmine.createSpy('connect').and.returnValue(of({state$: observableOf('connect')})),
      gtm: jasmine.createSpy('gtm')
    };

    pubSubService = {
      publish: jasmine.createSpy('publish'),
      API: {
        TIMELINE_SHOWN: 'TIMELINE_SHOWN',
        BYB_SHOWN: 'BYB_SHOWN',
        TIMELINE_SETTINGS_CHANGE: 'TIMELINE_SETTINGS_CHANGE',
        LOGIN_POPUPS_END: 'LOGIN_POPUPS_END',
        SESSION_LOGOUT: 'SESSION_LOGOUT',
        SUCCESSFUL_LOGIN: 'SUCCESSFUL_LOGIN',
        RELOAD_COMPONENTS: 'RELOAD_COMPONENTS'
      },
      subscribe: jasmine.createSpy('subscribe').and.callFake((a, b, cb) => { cb && cb(true); }),
      unsubscribe: jasmine.createSpy('unsubscribe')
    };

    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges'),
      markForCheck: jasmine.createSpy('markForCheck'),
      detach: jasmine.createSpy('detach'),
    };

    cms = {
      getTimelineSetting: jasmine.createSpy('getTimelineSetting').and.returnValue(of({})),
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(of({}))
    };

    router = {
      events: {
        subscribe: jasmine.createSpy('subscribe'),
        url: '/'
      }
    };

    userService = {
      timeline: true,
      status: true
    };

    asyncScriptLoaderService = {
      getSvgSprite: jasmine.createSpy('getSvgSprite').and.returnValue(of({}))
    };

    windowRefService = {
      nativeWindow: {
        setTimeout: jasmine.createSpy().and.callFake((fn: Function) => fn())
      },
      document: {
        body: {}
      }
    };

    rendererService = {
      renderer: {
        addClass: jasmine.createSpy('add'),
        removeClass: jasmine.createSpy('remove')
      }
    };

    locale = {
      getString: jasmine.createSpy().and.returnValue('Ladbrokes')
    };

    component = new TimelineComponent(
      timelineService,
      cms,
      router,
      changeDetectorRef,
      asyncScriptLoaderService,
      pubSubService,
      windowRefService,
      rendererService,
      userService,
      locale
    );
  });

  it('should init component', () => {
    environment.brand = 'bma';
    component['handleTimeline'] = jasmine.createSpy();
    component['subscribeToRouteEvents'] = jasmine.createSpy();
    component.openTimeline = jasmine.createSpy('openTimeline');
    component.closeTimeline = jasmine.createSpy('closeTimeline');
    component.ngOnInit();

    expect(pubSubService.subscribe).toHaveBeenCalledWith('timeline', 'BYB_SHOWN', jasmine.any(Function));
    expect(pubSubService.subscribe).toHaveBeenCalledWith('timeline', 'LOGIN_POPUPS_END', jasmine.any(Function));
    expect(component.bybShown).toBeTruthy();
    expect(component.isBrandLadbrokes).toBeFalsy();
    expect(component.gtmModuleBrandName).toBe('coral pulse');
    expect(component.cms.getTimelineSetting).toHaveBeenCalled();
    expect(component.availableRoutes.length).toBe(1);
    expect(component.handleTimeline).toHaveBeenCalled();
    expect(component.tutorialReady).toBeTruthy();
    expect(component.openTimeline).toHaveBeenCalled();
    expect(component.closeTimeline).not.toHaveBeenCalled();
    expect(pubSubService.subscribe).toHaveBeenCalledWith('timeline', [
      pubSubService.API.TIMELINE_SETTINGS_CHANGE,
      pubSubService.API.SESSION_LOGOUT,
      pubSubService.API.SUCCESSFUL_LOGIN
    ], jasmine.any(Function));
  });

  it('should not call opentimeline if socket is opened', () => {
    environment.brand = 'ladbrokes';
    pubSubService.subscribe.and.returnValue(null);
    router.events = observableOf(new NavigationEnd(0, '', ''));
    spyOn(component, 'handleTimeline');
    component.timelineService.socket = {
      isConnected: jasmine.createSpy('isConnected').and.returnValue(true)
    };
    component.openTimeline = jasmine.createSpy('openTimeline');
    component.closeTimeline = jasmine.createSpy('closeTimeline');
    component.cms.getTimelineSetting = jasmine.createSpy('getTimelineSetting').and.returnValue(of({pageUrls: 'test'}));
    component.ngOnInit();
    expect(component.isBrandLadbrokes).toBeTruthy();
    expect(component.gtmModuleBrandName).toBe('ladbrokes lounge');
    expect(component.cms.getTimelineSetting).toHaveBeenCalled();
    expect(component.availableRoutes.length).toBe(1);
    expect(component.openTimeline).not.toHaveBeenCalled();
    expect(component.closeTimeline).not.toHaveBeenCalled();
    expect(component.tutorialReady).toBeTruthy();
  });

  it('should not set tutorialReady as true if user is not logged in', () => {
    component.router.url = 'test';
    pubSubService.subscribe.and.returnValue(null);
    router.events = observableOf(new NavigationEnd(0, '', ''));
    spyOn(component, 'handleTimeline');
    userService.status = false;
    component.openTimeline = jasmine.createSpy('openTimeline');
    component.closeTimeline = jasmine.createSpy('closeTimeline');
    component.cms.getTimelineSetting = jasmine.createSpy('getTimelineSetting').and.returnValue(of({pageUrls: 'test,test2'}));
    component.ngOnInit();
    expect(component.cms.getTimelineSetting).toHaveBeenCalled();
    expect(component.availableRoutes.length).toBe(2);
    expect(component.openTimeline).not.toHaveBeenCalled();
    expect(component.handleTimeline).toHaveBeenCalled();
    expect(component.closeTimeline).toHaveBeenCalled();
    expect(component.tutorialReady).toBeFalsy();
  });

  describe('CMS systemconfig ', () => {
    beforeEach(() => {
      component.router.url = 'test';
      pubSubService.subscribe.and.returnValue(null);
      router.events = observableOf(new NavigationEnd(0, '', ''));
    });
    it('should not send totalpost value for no config data', () => {
      component.ngOnInit();
      expect(component.totalPoststoDisplay).toBeUndefined();
    });
    it('should have totalpost value for valid CMS call', () => {
      component.cms.getSystemConfig.and.returnValue(observableOf({ Timeline: { totalPostsCount: 4 } }));
      component.ngOnInit();
      expect(component.totalPoststoDisplay).toBe(4);
    });
    it('should not have totalpost value for no timeline property', () => {
      component.cms.getSystemConfig.and.returnValue(observableOf({ test: {} }));
      component.ngOnInit();
      expect(component.totalPoststoDisplay).toBeUndefined();
    });
    it('should not have totalpost value for no totalPostsCount property', () => {
      component.cms.getSystemConfig.and.returnValue(observableOf({ Timeline: { test: 4 } }));
      component.ngOnInit();
      expect(component.totalPoststoDisplay).toBeUndefined();
    });
  });

  describe('handleTimeline', () => {
    beforeEach(() => {
      component.timelineSettings = {
        enabled: true,
        pageUrls: '/,/horses',
        liveCampaignDisplayTo: Date.now() * 2
      };
      component.gtmModuleBrandName = 'event category';
      component.availableRoutes = ['/', '/horses'];
      component.isUrlAvailable = jasmine.createSpy('isUrlAvailable').and.returnValue(true);
      component.openTimeline = jasmine.createSpy('openTimeline');
      component.closeTimeline = jasmine.createSpy('closeTimeline');
    });

    it('should open timeline if url is available, timeline is enabled, socket not opened', () => {
      component.tutorialReady = true;
      component.handleTimeline();

      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.TIMELINE_SHOWN, true);
      expect(timelineService.gtm).toHaveBeenCalled();
      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.SHOW_TIMELINE_TUTORIAL);
      expect(component.openTimeline).toHaveBeenCalled();
      expect(component.changeDetectorRef.detectChanges).toHaveBeenCalled();
      expect(component.isUrlAvailable).toHaveBeenCalledWith(component.availableRoutes, component.router.url);
    });

    it('shouldnt open trigger tutorial', () => {
      component.tutorialReady = false;
      component.handleTimeline();

      expect(timelineService.gtm).toHaveBeenCalled();
      expect(pubSubService.publish).not.toHaveBeenCalledWith(pubSubService.API.SHOW_TIMELINE_TUTORIAL);
    });

    it('shouldn\'t open timeline if url is available, timeline is enabled, socket opened', () => {
      component.timelineService.socket = {
        isConnected: jasmine.createSpy('isConnected').and.returnValue(true)
      };
      component.openTimeline = jasmine.createSpy('openTimeline');

      component.handleTimeline();

      expect(timelineService.gtm).toHaveBeenCalled();
      expect(component.openTimeline).not.toHaveBeenCalled();
      expect(component.changeDetectorRef.detectChanges).toHaveBeenCalled();
      expect(component.isUrlAvailable).toHaveBeenCalledWith(component.availableRoutes, component.router.url);
    });

    it('should close timeline if end date passed', () => {
      component.timelineSettings.liveCampaignDisplayTo = 1;
      component.handleTimeline();

      expect(component.closeTimeline).not.toHaveBeenCalled();
      expect(component.changeDetectorRef.detectChanges).toHaveBeenCalled();
      expect(component.isUrlAvailable).toHaveBeenCalledWith(component.availableRoutes, component.router.url);
    });

    it('should close timeline if isUrlAvailable returns false', () => {
      component.isUrlAvailable = jasmine.createSpy('isUrlAvailable').and.returnValue(false);

      component.handleTimeline();

      expect(component.changeDetectorRef.detectChanges).toHaveBeenCalled();
      expect(component.isUrlAvailable).toHaveBeenCalledWith(component.availableRoutes, component.router.url);
    });

    it('should hide timeline if user disabled timeline in betting settings', () => {
      component.isUrlAvailable = jasmine.createSpy('isUrlAvailable').and.returnValue(true);
      userService.timeline = false;

      component.handleTimeline();
      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.TIMELINE_SHOWN, false);
    });

    it('should hide timeline if user is logged out', () => {
      component.isUrlAvailable = jasmine.createSpy('isUrlAvailable').and.returnValue(true);
      userService.timeline = true;
      userService.status = false;

      component.handleTimeline();
      expect(component.closeTimeline).toHaveBeenCalled();
      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.TIMELINE_SHOWN, false);
    });

    it('should check if url is available if timeline is enabled', () => {
      component.timelineSettings = {
        enabled: true,
        pageUrls: null
      };
      component.availableRoutes = [''];
      component.handleTimeline();

      expect(component.changeDetectorRef.detectChanges).toHaveBeenCalled();
      expect(component.isUrlAvailable).toHaveBeenCalledWith(component.availableRoutes, component.router.url);
    });

    it('shouldn\'t check if url is available if timeline is not enabled', () => {
      component.timelineSettings = {
        enabled: false,
        pageUrls: ''
      };

      component.handleTimeline();

      expect(component.isUrlAvailable).not.toHaveBeenCalled();
      expect(component.changeDetectorRef.detectChanges).not.toHaveBeenCalled();
    });
  });

  describe('onStateChange', () => {
    it('should change state of timeline - close', () => {
      component.timelineSettings = {
        liveCampaignName: '123'
      };
      component.gtmModuleBrandName = 'event category';
      component.onStateChange(false);

      expect(timelineService.gtm).toHaveBeenCalledWith('close', { eventLabel: '123'}, 'event category');
      expect(component.timelineOpened).toBeFalsy();
      expect(component.isNewPostIconDisplayed).toBeFalsy();
    });

    it('should change state of timeline - open', () => {
      spyOn(component, 'toggleBodyScroll');
      component.timelineSettings = {
        liveCampaignName: '123'
      };
      component.gtmModuleBrandName = 'event category';
      component.isNewPostIconDisplayed = true;
      component.onStateChange(true);

      expect(timelineService.gtm).toHaveBeenCalledWith('open', { eventLabel: '123'}, 'event category');
      expect(component['toggleBodyScroll']).toHaveBeenCalledWith(true);
      expect(component.isNewPostIconDisplayed).toBeFalsy();
      expect(component.timelineOpened).toBeTruthy();
    });
  });

  it('onTimelineReload should close and open timeline panel', () => {
    component.closeTimeline = jasmine.createSpy('closeTimeline');
    component.openTimeline = jasmine.createSpy('openTimeline');
    component.changeDetectorRef.detectChanges = jasmine.createSpy('detectChanges');

    component.onTimelineReload(true);

    expect(component.closeTimeline).toHaveBeenCalled();
    expect(component.openTimeline).toHaveBeenCalled();
    expect(component.changeDetectorRef.detectChanges).toHaveBeenCalled();
  });

  it('onTimelineReload shouldn\'t close and open timeline panel', () => {
    component.closeTimeline = jasmine.createSpy('closeTimeline');
    component.openTimeline = jasmine.createSpy('openTimeline');
    component.changeDetectorRef.detectChanges = jasmine.createSpy('detectChanges');

    component.onTimelineReload(false);

    expect(component.closeTimeline).not.toHaveBeenCalled();
    expect(component.openTimeline).not.toHaveBeenCalled();
    expect(component.changeDetectorRef.detectChanges).not.toHaveBeenCalled();
  });

  describe('openTimeline', () => {
    beforeEach(() => {
      pubSubService.subscribe = jasmine.createSpy('subscribe');
    });

    it('should open timeline', () => {
      component.openTimeline();
      expect(component.timelineService.createSocket).toHaveBeenCalled();
      expect(component.timelineService.connect).toHaveBeenCalled();
      expect(component.showSkeleton).toEqual(false);
      expect(component.isReconectedFailedMsg).toEqual(false);

      component.timelineService.connect().subscribe();

      expect(component.timelineService.addListener).toHaveBeenCalled();
      expect(component.timelineService.addListener).toHaveBeenCalledWith('POST', jasmine.any(Function));
      expect(component.timelineService.addListener).toHaveBeenCalledWith('POST_PAGE', jasmine.any(Function));
      expect(component.timelineService.addListener).toHaveBeenCalledWith('POST_CHANGED', jasmine.any(Function));
      expect(component.timelineService.addListener).toHaveBeenCalledWith('POST_REMOVED', jasmine.any(Function));
      expect(component.timelineService.addListener).toHaveBeenCalledWith('CAMPAIGN_CLOSED', jasmine.any(Function));
      expect(component['pubSubService'].subscribe)
        .toHaveBeenCalledWith(component['title'], pubSubService.API.RELOAD_COMPONENTS, jasmine.any(Function));
    });

    it('should subscribe to reload components event', () => {
      pubSubService.subscribe = jasmine.createSpy('subscribe').and.callFake((tag, api, callback) => callback());
      component['subscribeToTimelineUpdates'] = jasmine.createSpy('subscribeToTimelineUpdates');

      component.openTimeline();

      expect(component['subscribeToTimelineUpdates']).toHaveBeenCalledTimes(2);
      expect(component['pubSubService'].subscribe)
        .toHaveBeenCalledWith(component['title'], pubSubService.API.RELOAD_COMPONENTS, jasmine.any(Function));
    });

    it('POST_PAGE, not all posts loaded', fakeAsync(() => {
      const lastPost = {id: '2', data: {}};
      const postsPage = {
        page: [
          {id: '1', data: {}},
          {id: '2', data: {}},
          lastPost
        ],
        count: 10
      };

      component.timelineService.addListener.and.callFake((action, cb) => {
        action === TIMELINE_EVENTS.POST_PAGE && cb(postsPage);
      });

      component.openTimeline();
      tick(300);

      expect(component.lastPost).toEqual(lastPost);
      expect(component.showSkeleton).toEqual(false);
      expect(component.allPostsLoaded).toBeFalsy();
      expect(component.changeDetectorRef.detectChanges).toHaveBeenCalled();
    }));

    it('POST_PAGE, all posts loaded', fakeAsync(() => {
      const lastPost = {id: '2', data: {}};
      const postsPage = {
        page: [
          {id: '1', data: {}},
          {id: '2', data: {}},
          lastPost
        ],
        count: 3
      };
      component.validateTotalPostsDisplay = jasmine.createSpy('validateTotalPostsDisplay');
      component.timelineService.addListener.and.callFake((action, cb) => {
        action === TIMELINE_EVENTS.POST_PAGE && cb(postsPage);
      });

      component.openTimeline();
      tick(300);

      expect(component.lastPost).toEqual(lastPost);
      expect(component.showSkeleton).toEqual(false);
      expect(component.allPostsLoaded).toBeTruthy();
      expect(component.validateTotalPostsDisplay).toHaveBeenCalled();
      expect(component.changeDetectorRef.detectChanges).toHaveBeenCalled();
    }));

    it('POST_PAGE, all posts were loaded previously', fakeAsync(() => {
      const postsPage = {
        page: [],
        count: 3
      };

      component.allPostsLoaded = true;
      component.timelineService.addListener.and.callFake((action, cb) => {
        action === TIMELINE_EVENTS.POST_PAGE && cb(postsPage);
      });

      component.openTimeline();
      tick(300);

      expect(component.showSkeleton).toEqual(false);
      expect(component.allPostsLoaded).toBeTruthy();
      expect(component.changeDetectorRef.detectChanges).toHaveBeenCalled();
    }));

    it('POST_PAGE should handle case if there are no posts', fakeAsync(() => {
      const postsPage = {
        page: null
      };

      component.timelineService.addListener.and.callFake((action, cb) => {
        action === TIMELINE_EVENTS.POST_PAGE && cb(postsPage);
      });

      component.openTimeline();
      tick(300);

      expect(component.lastPost).not.toBeDefined();
      expect(component.changeDetectorRef.detectChanges).toHaveBeenCalled();
    }));

    describe('#subscribeToTimelineUpdates', () => {
      it('POST_PAGE, all posts loaded with resetPosts = true', fakeAsync(() => {
        const lastPost = {id: '2', data: {}};
        const postsPage = {
          page: [
            {id: '1', data: {}},
            {id: '2', data: {}},
            lastPost
          ],
          count: 10
        };

        component.timelineService.addListener.and.callFake((action, cb) => {
          action === TIMELINE_EVENTS.POST_PAGE && cb(postsPage);
        });

        component['subscribeToTimelineUpdates'](true);
        tick(300);
        expect(component.lastPost).toEqual(lastPost);
        expect(component.showSkeleton).toEqual(false);
        expect(component.allPostsLoaded).toBeFalsy();
        expect(component.changeDetectorRef.detectChanges).toHaveBeenCalled();
        expect(component.posts).toEqual([
          {id: '1', data: {}},
          {id: '2', data: {}},
          {id: '2', data: {}}
        ]);
      }));
    });

    describe('@POST', () => {
      let post;
      beforeEach(() => {
        post = {id: 'id'};
        component.isNewPostIconDisplayed = false;
        component.timelineService.addListener.and.callFake((action, cb) => {
          action === TIMELINE_EVENTS.POST && cb(post);
        });
      });

      it('should modify isNewPostIconDisplayed property', () => {
        component.timelineOpened = false;

        component.openTimeline();

        expect(component.changeDetectorRef.detectChanges).toHaveBeenCalled();
        expect(component.isNewPostIconDisplayed).toBeTruthy();
      });

      it('should not modify posts', () => {
        component.posts = [{id: 'id', data: {}}];
        component.timelineOpened = false;
        component.validateTotalPostsDisplay = jasmine.createSpy('validateTotalPostsDisplay');
        component.openTimeline();

        expect(component.changeDetectorRef.detectChanges).toHaveBeenCalled();
        expect(component.isNewPostIconDisplayed).toBeTruthy();
        expect(component.validateTotalPostsDisplay).toHaveBeenCalled();
        expect(component.posts).toEqual([{id: 'id', data: {}}]);
        expect(component.lastPost).toEqual({id: 'id', data: {}});
      });

      it('shouldn\'t modify isNewPostIconDisplayed property', () => {
        component.timelineOpened = true;

        component.openTimeline();

        expect(component.changeDetectorRef.detectChanges).toHaveBeenCalled();
        expect(component.isNewPostIconDisplayed).toBeFalsy();
      });
    });

    it('POST, when posts are empty', () => {
      component.posts = [];
      component.timelineService.addListener.and.callFake((action, cb) => {
        action === TIMELINE_EVENTS.POST && cb([]);
      });
      component.openTimeline();
      expect(component.changeDetectorRef.detectChanges).toHaveBeenCalled();
      expect(component.posts.length).toBe(1);
      expect(component.lastPost.length).toBe(0);
    });

    it('POST_CHANGED, post in data property', () => {
      const post = { id: '2' };

      component.posts = [
        { id: '1' },
        { id: '2' },
        { id: '3' }
      ];
      const postToUpdate = component.posts[1];

      component.timelineService.addListener.and.callFake((action, cb) => {
        action === TIMELINE_EVENTS.POST_CHANGED && cb([post]);
      });
      component.handlePriceChange = jasmine.createSpy('handlePriceChange');

      component.openTimeline();

      expect(component.handlePriceChange).toHaveBeenCalledWith(post, postToUpdate);
      expect(component.posts[1]).toBe(post);
      expect(component.changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('POST_CHANGED, post in array', () => {
      const post = { id: '2' };
      const actionMessage = [post];

      component.posts = [
        { id: '1' },
        { id: '2' },
        { id: '3' }
      ];
      const postToUpdate = component.posts[1];

      component.timelineService.addListener.and.callFake((action, cb) => {
        action === TIMELINE_EVENTS.POST_CHANGED && cb(actionMessage);
      });
      component.handlePriceChange = jasmine.createSpy('handlePriceChange');

      component.openTimeline();

      expect(component.handlePriceChange).toHaveBeenCalledWith(post, postToUpdate);
      expect(component.posts[1]).toBe(post);
      expect(component.changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('POST_CHANGED, post in array', () => {
      const post = { id: '2' };
      const actionMessage = [post];

      component.posts = [
        { id: '1' },
        { id: '2' },
        { id: '3' }
      ];
      const postToUpdate = component.posts[1];

      component.timelineService.addListener.and.callFake((action, cb) => {
        action === TIMELINE_EVENTS.POST_CHANGED && cb(actionMessage);
      });
      component.handlePriceChange = jasmine.createSpy('handlePriceChange');

      component.openTimeline();

      expect(component.handlePriceChange).toHaveBeenCalledWith(post, postToUpdate);
      expect(component.posts[1]).toBe(post);
      expect(component.changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('POST_REMOVED', () => {
      const post = { id: '2' };
      const actionMessage = {
        affectedMessageId: '2',
        data: post
      };

      component.posts = [
        { id: '1' },
        { id: '2' },
        { id: '3' }
      ];

      component.timelineService.addListener.and.callFake((action, cb) => {
        action === TIMELINE_EVENTS.POST_REMOVED && cb(actionMessage);
      });

      component.openTimeline();

      expect(component.posts).toEqual([{ id: '1' }, { id: '3' }]);
      expect(component.changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('CAMPAIGN_CLOSED', () => {
      component.timelineService.addListener.and.callFake((action, cb) => {
        action === TIMELINE_EVENTS.CAMPAIGN_CLOSED && cb();
      });

      component.openTimeline();

      expect(component.posts).toEqual([]);
      expect(component.changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
  });

  describe('TIMELINECONFIG', () => {
    it('when timelineSettings is false', () => {
      component.timelineService.addListener.and.callFake((action, cb) => {
        action === TIMELINE_EVENTS.TIMELINE_CONFIG && cb({ enabled: false });
      });
      component['subscribeToTimelineUpdates']();
      expect(component.isTimelineAvailable).toBeFalsy();
      expect(component.changeDetectorRef.markForCheck).toHaveBeenCalled();
    });

    it('when timelineSettings is true and timelineconfig is true', () => {
      component.handleTimeline = jasmine.createSpy();
      component.timelineService.addListener.and.callFake((action, cb) => {
        action === TIMELINE_EVENTS.TIMELINE_CONFIG && cb({ enabled: true });
      });
      component.timelineSettings = { pageUrls: '/,/horses' };
      component['subscribeToTimelineUpdates']();
      expect(component.handleTimeline).toHaveBeenCalled();
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
    });

    it('when timelineSettings is true and isUrlAvailable is false', () => {
      component.timelineService.addListener.and.callFake((action, cb) => {
        action === TIMELINE_EVENTS.TIMELINE_CONFIG && cb({ enabled: false });
      });
      component.timelineSettings = { pageUrls: '/,/horses' };
      component['subscribeToTimelineUpdates']();
      expect(component.isTimelineAvailable).toBeFalsy();
      expect(component.changeDetectorRef.markForCheck).toHaveBeenCalled();
    });
  });

  describe('validateTotalPostsDisplay', () => {
    it('when post count is less or equal to totalpost allowed', () => {
      component.totalPoststoDisplay = 2;
      component.posts = [{ id: '1' }];
      component.validateTotalPostsDisplay();
      expect(component.posts).toEqual([{ id: '1' }]);
    });
    it('when post count is more than totalpost allowed', () => {
      component.totalPoststoDisplay = 1;
      component.posts = [{ id: '1' }, { id: '2' }];
      component.validateTotalPostsDisplay();
      expect(component.posts).toEqual([{ id: '1' }]);
    });
  });

  describe('@handlePriceChange', () => {
    beforeEach(() => {
      component['getClassForPriceUpdate'] = jasmine.createSpy('getClassForPriceUpdate');
      component['updateButtonClass'] = jasmine.createSpy('updateButtonClass');
    });

    it('no selection event in post', () => {
      const post = {};
      const updatedPost = {};
      component['handlePriceChange'](post, updatedPost);
      expect(component['getClassForPriceUpdate']).not.toHaveBeenCalled();
      expect(component['updateButtonClass']).not.toHaveBeenCalled();
    });

    it('post to update is undefined', () => {
      const post = {
        id: '2',
        selectionEvent: { obEvent: { markets: [{ outcomes: [{ prices: [{ priceNum: 3, priceDen: 5 }] }] }] } }
      };
      const updatedPost = undefined;
      component['getClassForPriceUpdate'] = jasmine.createSpy('getClassForPriceUpdate').and.returnValue(undefined);
      component['handlePriceChange'](post, updatedPost);
      expect(component['getClassForPriceUpdate']).toHaveBeenCalled();
      expect(component['updateButtonClass']).toHaveBeenCalled();
    });
    it('post to update has selectionEvent is undefined', () => {
      const post = {
        id: '2',
        selectionEvent: { obEvent: { markets: [{ outcomes: [{ prices: [{ priceNum: 3, priceDen: 5 }] }] }] } }
      };
      const updatedPost = { selectionEvent: undefined };
      component['getClassForPriceUpdate'] = jasmine.createSpy('getClassForPriceUpdate').and.returnValue(undefined);
      component['handlePriceChange'](post, updatedPost);
      expect(component['getClassForPriceUpdate']).toHaveBeenCalled();
      expect(component['updateButtonClass']).toHaveBeenCalled();
    });

    it('post has selection event', () => {
      const post = {
        id: '2',
        selectionEvent: {
          obEvent: {
            markets: [
              {
                outcomes: [
                  {
                    prices: [
                      {
                        priceNum: 3,
                        priceDen: 5
                      }
                    ]
                  }
                ]
              }
            ]
          }
        }
      };
      const updatedPost = {
        id: '2',
        selectionEvent: {
          obEvent: {
            markets: [
              {
                outcomes: [
                  {
                    prices: [
                      {
                        priceNum: 2,
                        priceDen: 7
                      }
                    ]
                  }
                ]
              }
            ]
          }
        }
      };
      const buttonClass = 'button-class';
      component['getClassForPriceUpdate'] = jasmine
        .createSpy('getClassForPriceUpdate').and.returnValue(buttonClass);
      component['handlePriceChange'](post, updatedPost);
      expect(component['getClassForPriceUpdate']).toHaveBeenCalledWith(
        post.selectionEvent.obEvent.markets[0].outcomes[0].prices[0],
        updatedPost.selectionEvent.obEvent.markets[0].outcomes[0].prices[0]
      );
      expect(component['updateButtonClass']).toHaveBeenCalledWith(post.id, buttonClass);
    });
  });

  describe('@getClassForPriceUpdate', () => {
    it('price was increased', () => {
      const currentPrices = {
        priceNum: 3,
        priceDen: 5
      };
      const updatedPrices = {
        priceNum: 1,
        priceDen: 7
      };
      expect(component['getClassForPriceUpdate'](currentPrices, updatedPrices)).toBe('bet-up');
    });

    it('price was decreased', () => {
      const currentPrices = {
        priceNum: 5,
        priceDen: 7
      };
      const updatedPrices = {
        priceNum: 98,
        priceDen: 99
      };
      expect(component['getClassForPriceUpdate'](currentPrices, updatedPrices)).toBe('bet-down');
    });

    it('price was not updated', () => {
      const currentPrices = {
        priceNum: 2,
        priceDen: 9
      };
      const updatedPrices = {
        priceNum: 2,
        priceDen: 9
      };
      expect(component['getClassForPriceUpdate'](currentPrices, updatedPrices)).toBe('');
    });

    it('no currentPrice', () => {
      const currentPrices = null;
      const updatedPrices = {
        priceNum: 2,
        priceDen: 9
      };
      expect(component['getClassForPriceUpdate'](currentPrices, updatedPrices)).toBe('');
    });

    it('no updatedPrice', () => {
      const currentPrices = {
        priceNum: 2,
        priceDen: 9
      };
      const updatedPrices = null;
      expect(component['getClassForPriceUpdate'](currentPrices, updatedPrices)).toBe('');
    });
  });

  describe('@updateButtonClass', () => {
    it('no button class', () => {
      component['updateButtonClass']('2', '');
      expect(component['priceButtonClasses']).toEqual({});
    });

    it('button class was passed', fakeAsync(() => {
      component['updateButtonClass']('2', 'bet-up');
      expect(component['priceButtonClasses']).toEqual({'2': 'bet-up'});

      tick(component['removePriceUpdateClassTime']);

      expect(component['priceButtonClasses']).toEqual({'2': ''});
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
    }));
  });

  describe('@closeTimeline', () => {
    let localTimelineService;
    beforeEach(() => {
      localTimelineService = {
        removeListener: jasmine.createSpy('removeListener'),
        disconnect: jasmine.createSpy('disconnect')
      };

      component.timelineService = localTimelineService;

      component.routeChangeSub = { unsubscribe: jasmine.createSpy('unsubscribe') };
    });

    afterEach(() => {
      component.timelineService = timelineService;
    });

    it('should close timeline', () => {
      component.timelineServiceSub = { unsubscribe: jasmine.createSpy('unsubscribe') };
      component.createSocketSub = { unsubscribe: jasmine.createSpy('unsubscribe') };
      component.closeTimeline();

      expect(component.timelineService.disconnect).toHaveBeenCalled();
      expect(component.timelineService.removeListener).toHaveBeenCalledWith(TIMELINE_EVENTS.CAMPAIGN_CLOSED);
      expect(component.timelineService.removeListener).toHaveBeenCalledWith(TIMELINE_EVENTS.POST_CHANGED);
      expect(component.timelineService.removeListener).toHaveBeenCalledWith(TIMELINE_EVENTS.POST_REMOVED);
      expect(component.timelineService.removeListener).toHaveBeenCalledWith(TIMELINE_EVENTS.POST_PAGE);
      expect(component.timelineService.removeListener).toHaveBeenCalledWith(TIMELINE_EVENTS.POST);
      expect(component.timelineService.removeListener).toHaveBeenCalledWith(TIMELINE_EVENTS.TIMELINE_CONFIG);
      expect(component.timelineService.removeListener).toHaveBeenCalledTimes(6);
      expect(component['timelineServiceSub'].unsubscribe).toHaveBeenCalled();
      expect(component['createSocketSub'].unsubscribe).toHaveBeenCalled();
      expect(component.posts).toEqual([]);
    });

    it('shouldn\'t disconnect and remove listeners if timelineService is empty', () => {
      component.timelineService = null;
      component.closeTimeline();

      expect(timelineService.removeListener).not.toHaveBeenCalled();
      expect(component.changeDetectorRef.detectChanges).toHaveBeenCalled();
      expect(component.posts).toEqual([]);
    });
  });

  it('should load more posts if loadMore() is called', () => {
    component.totalPoststoDisplay = 3;
    component.posts.length = 2;
    component.lastPost = {
      id: 'id',
      createdDate: 'createdDate'
    };

    component.loadMore();

    expect(component.timelineService.emit).toHaveBeenCalledWith(TIMELINE_EVENTS.LOAD_POST_PAGE, {
      from: {
        id: component.lastPost.id,
        timestamp: component.lastPost.createdDate
      }
    });
    expect(component.showSkeleton).toBeTruthy();
    expect(component.changeDetectorRef.detectChanges).toHaveBeenCalled();
  });
  it('should not load more posts if totalposts count is reached', () => {
    component.totalPoststoDisplay = 3;
    component.posts.length = 4;
    component.loadMore();
    expect(component.timelineService.emit).not.toHaveBeenCalled();
    expect(component.showSkeleton).toBeFalsy();
    expect(component.changeDetectorRef.detectChanges).not.toHaveBeenCalled();
  });

  describe('onTimelineReload', () => {
    it('state: true', () => {
      component.closeTimeline = jasmine.createSpy('closeTimeline');
      component.openTimeline = jasmine.createSpy('openTimeline');
      component.onTimelineReload(true);
      expect(component.closeTimeline).toHaveBeenCalled();
      expect(component.openTimeline).toHaveBeenCalled();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('state: false', () => {
      component.onTimelineReload();
      expect(changeDetectorRef.detectChanges).not.toHaveBeenCalled();
    });
  });

  describe('isUrlAvailable', () => {
    it('should return true if timeline is available for route', () => {
      const routes = ['/', '/horse-racing/*', '/home/live-stream'];
      const url = '/horse-racing/';
      const result = component.isUrlAvailable(routes, url);

      expect(result).toBeTruthy();
    });

    it('should return false if timeline is not available for route url', () => {
      const routes = ['/', '/horse-racing/*', '/home/live-stream'];
      const url = '/home/live-stream/horse-racing/';
      const result = component['isUrlAvailable'](routes, url);

      expect(result).toBeFalsy();
    });

    it('should check if current url is in availables pool', () => {
      const routes = ['/', '/horse-racing/*', '/home/live-stream'];
      const url1 = '/';
      const url2 = '/horse-racing/features';
      const url3 = '/home/live-stream';


      const url4 = '/home/live-stream/';
      const url5 = '/home/horse-racing/';
      const url6 = 'horse-racing';

      expect(component['isUrlAvailable'](routes, url1)).toBeTruthy();
      expect(component['isUrlAvailable'](routes, url2)).toBeTruthy();
      expect(component['isUrlAvailable'](routes, url3)).toBeTruthy();

      expect(component['isUrlAvailable'](routes, url4)).toBeFalsy();
      expect(component['isUrlAvailable'](routes, url5)).toBeFalsy();
      expect(component['isUrlAvailable'](routes, url6)).toBeFalsy();
    });
  });

  describe('toggleBodyScroll', () => {
    it('should add class', () => {
      component['toggleBodyScroll'](true);
      expect(rendererService.renderer.addClass).toHaveBeenCalledWith({}, 'timeline-opened');
    });

    it('should remove class', () => {
      component['toggleBodyScroll'](false);
      expect(rendererService.renderer.removeClass).toHaveBeenCalledWith({}, 'timeline-opened');
    });
  });

  it('should call ngOnDestroy()', () => {
    component.routeChangeSub = { unsubscribe: jasmine.createSpy('unsubscribe') };
    component.timelineSettingSub = { unsubscribe: jasmine.createSpy('unsubscribe') };
    component.timelineServiceSub = { unsubscribe: jasmine.createSpy('unsubscribe') };
    component.timelinePostsCountSub = { unsubscribe: jasmine.createSpy('unsubscribe') };
    component.createSocketSub = { unsubscribe: jasmine.createSpy('unsubscribe') };

    component.closeTimeline = jasmine.createSpy('closeTimeline');
    component.ngOnDestroy();

    expect(component.closeTimeline).toHaveBeenCalled();
    expect(component['routeChangeSub'].unsubscribe).toHaveBeenCalled();
    expect(component['timelineSettingSub'].unsubscribe).toHaveBeenCalled();
    expect(component['timelineServiceSub'].unsubscribe).toHaveBeenCalled();
    expect(component['timelinePostsCountSub'].unsubscribe).toHaveBeenCalled();
    expect(component['createSocketSub'].unsubscribe).toHaveBeenCalled();
    expect(pubSubService.unsubscribe).toHaveBeenCalledWith(component['title']);
  });

  describe('displayBtn', () => {
    function displayBtn() {
      return component.tutorialReady && !component.timelineOpened && !component.bybShown;
    }

    it('should return false if tutorialReady: false', () => {
      component.tutorialReady = false;
      expect(displayBtn()).toBeFalsy();
    });

    it('should return false if timelineOpened: true', () => {
      component.tutorialReady = true;
      component.timelineOpened = true;
      expect(displayBtn()).toBeFalsy();
    });

    it('should return false if bybShown: true', () => {
      component.tutorialReady = true;
      component.timelineOpened = false;
      component.bybShown = true;
      expect(displayBtn()).toBeFalsy();
    });

    it('should return true if all conditions correct', () => {
      component.tutorialReady = true;
      component.timelineOpened = false;
      component.bybShown = false;
      expect(displayBtn()).toBeTruthy();
    });
  });

  describe('subscribeToRouteEvents', () => {
    beforeEach(() => {
      component.availableRoutes = ['/', '/horses'];
      component.router.url = '/sport';
      component.openTimeline = jasmine.createSpy('openTimeline');
    });
    it('handleTimeline is called when isUrlConfigured is true', fakeAsync(() => {
      component.timelineSettings = {
        liveCampaignId: '123'
      };
      component.router.url = '/';
      router.events = observableOf(new NavigationEnd(0, '', ''));
      spyOn(component, 'handleTimeline');
      component['subscribeToRouteEvents']();

      tick();

      expect(component.handleTimeline).toHaveBeenCalled();
    }));

    it('isUrlConfigured false, hide bubble, socket undefined', fakeAsync(() => {
      router.events = observableOf(new NavigationEnd(0, '', ''));
      component['subscribeToRouteEvents']();
      expect(component.openTimeline).toHaveBeenCalled();
      expect(component.isTimelineAvailable).toBeFalsy();
    }));

    it('isUrlConfigured false, hide bubble, socket connected', fakeAsync(() => {
      router.events = observableOf(new NavigationEnd(0, '', ''));
      component.timelineService.socket = {
        isConnected: jasmine.createSpy('isConnected').and.returnValue(true)
      };
      component['subscribeToRouteEvents']();
      expect(component.openTimeline).not.toHaveBeenCalled();
      expect(component.isTimelineAvailable).toBeFalsy();
    }));

    it('isUrlConfigured false, hide bubble, socket not connected', fakeAsync(() => {
      router.events = observableOf(new NavigationEnd(0, '', ''));
      component.timelineService.socket = {
        isConnected: jasmine.createSpy('isConnected').and.returnValue(false)
      };
      component['subscribeToRouteEvents']();
      expect(component.openTimeline).toHaveBeenCalled();
      expect(component.isTimelineAvailable).toBeFalsy();
    }));
  });

  describe('should openTimeline and test webSocket.state$', () => {
    it ('should show skeleton when webSocket.state$ = reconnect', ()=> {
      component.timelineService.createSocket = jasmine.createSpy('createSocket').and.returnValue(of(
        {state$: observableOf('reconnect')}));

      component.openTimeline();
      expect(component.timelineService.createSocket).toHaveBeenCalled();

      expect(component.showSkeleton).toEqual(true);
      expect(component.isReconectedFailedMsg).toEqual(false);
    });

    it ('should show skeleton when webSocket.state$ = reconnect_attempt', ()=> {
      component.timelineService.createSocket = jasmine.createSpy('createSocket').and.returnValue(of(
        {state$: observableOf('reconnect_attempt')}));

      component.openTimeline();

      expect(component.showSkeleton).toEqual(true);
      expect(component.isReconectedFailedMsg).toEqual(false);
    });

    it ('should hide skeleton and show ReconectedFailedMsg when webSocket.state$ = reconnect_failed ', ()=> {
      component.timelineService.createSocket = jasmine.createSpy('createSocket').and.returnValue(of(
        {state$: observableOf('reconnect_failed')}));

      component.openTimeline();

      expect(component.showSkeleton).toEqual(false);
      expect(component.isReconectedFailedMsg).toEqual(true);
    });

    it ('should hide skeleton and ReconectedFailedMsg when webSocket.state$ = disconnect ', ()=> {
      component.timelineService.createSocket = jasmine.createSpy('createSocket').and.returnValue(of(
        {state$: observableOf('disconnect')}));

      component.openTimeline();

      expect(component.showSkeleton).toEqual(false);
      expect(component.isReconectedFailedMsg).toEqual(false);
    });
  });
});
