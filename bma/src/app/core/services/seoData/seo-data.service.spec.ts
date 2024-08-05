import { of as observableOf, Subject } from 'rxjs';
import { NavigationEnd, NavigationStart } from '@angular/router';
import { fakeAsync, tick } from '@angular/core/testing';

import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { SeoDataService } from './seo-data.service';

describe('SeoDataService', () => {
  let service: SeoDataService;
  let windowRef;
  let cms;
  let pubsub;
  let router;
  let routeSubject;
  let domElement;

  beforeEach(() => {
    routeSubject = new Subject();
    domElement = {
      setAttribute: jasmine.createSpy('setAttribute'),
      appendChild: jasmine.createSpy('appendChild')
    };
    windowRef = {
      nativeWindow: {
        location: {
          pathname: '/',
          origin: 'https://'
        },
        document: {
          querySelector: jasmine.createSpy('querySelector').and.returnValue(domElement),
          createElement: jasmine.createSpy('createElement').and.returnValue({ type: 'type', text: '' })
        }
      }
    };
    cms = {
      getSeoPagesPaths: jasmine.createSpy('getSeoPagesPaths').and.returnValue(observableOf({
        '/': 'askjdhsakjd',
        'test': 'bcd'
      })),
      getSeoPage: jasmine.createSpy('getSeoPage').and.returnValue(observableOf({
        '/': 'askjdhsakjd',
        'test': 'bcd'
      })),
      getAutoSeoPages: jasmine.createSpy('getAutoSeoPages').and.returnValue(observableOf({
        '/event': { metaTitle: 'bet on <event>|<competition>', metaDescription: 'bet on <event>' },
        '/outrights': { metaTile: 'outright title|<sport>', metaDescription: 'outright description|<sport>' }
      }))
    };
    pubsub = {
      publish: jasmine.createSpy('publish'),
      API: pubSubApi
    };
    router = {
      events: routeSubject
    };
  });

  function createService() {
    service = new SeoDataService(windowRef, cms, pubsub, router);
  }

  it('should have default title and description', () => {
    createService();

    expect(service.defaultPage).toEqual(jasmine.objectContaining({
      title: 'Online Sports Betting and Latest Odds - Coral',
      description: 'Betting has never been better with pre-event and in-play markets available from all over the world.' +
        ' Get the latest betting odds at Coral. Don\'t Bet Silly, Bet Savvy!'
    }));
  });

  it('should getSeoPagesPaths', fakeAsync(() => {
    createService();

    expect(cms.getSeoPagesPaths).toHaveBeenCalledTimes(1);
    expect(cms.getSeoPage).toHaveBeenCalledWith('askjdhsakjd');

    windowRef.nativeWindow.location.pathname = 'test';
    routeSubject.next(new NavigationEnd(0, 'test', 'test'));
    tick(150);

    expect(cms.getSeoPage).toHaveBeenCalledWith('bcd');
    expect(cms.getSeoPage).toHaveBeenCalledTimes(2);
  }));

  it('getPage', () => {
    createService();

    service['executed'] = false;
    expect(service.getPage()).toBeDefined();
    service['executed'] = true;
    expect(service.getPage()).toBeDefined();
  });


  it('eventPageSeo', () => {
    createService();
    spyOn(service, 'competitors');
    service['checkForHorse'] = jasmine.createSpy().and.returnValue(false);
    const event = {
      categoryId: '1',
      name: 'home v away',
      teamHome: 'home',
      teamAway: 'away',
      categoryName: 'football',
      liveStreamAvailable: 'false',
      startTime: new Date().getTime(),
      typeName: 'football'
    } as any;
    service.eventPageSeo(event, 'edpUrl');
    expect(windowRef.nativeWindow.document.querySelector).toHaveBeenCalled();
  });

  it('eventPageSeo for horse racing', () => {
    createService();
    spyOn(service, 'competitors');
    service['checkForHorse'] = jasmine.createSpy().and.returnValue(true);
    const event = {
      categoryId: '21',
      name: 'home',
      teamHome: 'home',
      teamAway: 'away',
      categoryName: 'horse racing',
      liveStreamAvailable: 'false',
      startTime: new Date().getTime(),
      typeName: 'horse racing',
      markets: [{
        outcomes: [{
          name: 'greyhound racing'
        }]
      }]
    } as any;
    service.eventPageSeo(event, 'edpUrl');
    expect(windowRef.nativeWindow.document.querySelector).toHaveBeenCalled();
  });

  it('eventPageSeo for GH', () => {
    createService();
    spyOn(service, 'competitors');
    service['checkForHorse'] = jasmine.createSpy().and.returnValue(true);
    const event = {
      categoryId: '19',
      name: 'home',
      teamHome: 'home',
      teamAway: 'away',
      categoryName: 'grey hound racing',
      liveStreamAvailable: 'false',
      startTime: new Date().getTime(),
      typeName: 'horse racing',
      markets: [{
        outcomes: [{
          name: 'greyhound racing'
        }]
      }]
    } as any;
    service.eventPageSeo(event, 'edpUrl');
    expect(windowRef.nativeWindow.document.querySelector).toHaveBeenCalled();
  });

  describe('competitors', () => {
    it('competitors for sports having team A vs team B', () => {
      createService();
      service['checkForSport'] = jasmine.createSpy().and.returnValue(true);
      const event = {
        categoryId: '1',
        name: 'home v away',
        teamHome: 'home',
        teamAway: 'away',
        categoryName: 'football',
        liveStreamAvailable: 'false',
        startTime: new Date().getTime(),
        typeName: 'football',
        markets: [{
          outcomes: [{
            name: 'home'
          }]
        }]
      } as any;
      service['eventSchema'] = {
        'broadcastOfEvent': {
          'competitor': []
        }
      };
      service.competitors(event);
    });

    it('competitors for other sports when team away, home not present for sports having team A vs team B', () => {
      createService();
      service['checkForSport'] = jasmine.createSpy().and.returnValue(true);
      const event = {
        categoryId: '1',
        name: 'home v away',
        categoryName: 'football',
        liveStreamAvailable: 'false',
        startTime: new Date().getTime(),
        typeName: 'football',
        markets: [{
          outcomes: [{
            name: 'home'
          }]
        }]
      } as any;
      service['eventSchema'] = {
        'broadcastOfEvent': {
          'competitor': []
        }
      };
      service.competitors(event);

    });

    it('competitors for horseracing for sports not having team A vs team B & no minorcode', () => {
      createService();
      service['checkForSport'] = jasmine.createSpy().and.returnValue(false);
      service['checkForHorse'] = jasmine.createSpy().and.returnValue(true);
      const event = {
        categoryId: '19',
        name: 'home',
        teamHome: 'home',
        teamAway: 'away',
        categoryName: 'horse racing',
        liveStreamAvailable: 'false',
        startTime: new Date().getTime(),
        typeName: 'horse racing',
        markets: [{
          outcomes: [{
            name: 'greyhound racing'
          }]
        }]
      } as any;
      service['eventSchema'] = {
        'broadcastOfEvent': {
          'competitor': []
        }
      };
      service.competitors(event);
    });

    it('competitors for horseracing for sports not having team A vs team B & with minorcode', () => {
      createService();
      service['checkForSport'] = jasmine.createSpy().and.returnValue(false);
      service['checkForHorse'] = jasmine.createSpy().and.returnValue(true);
      const event = {
        categoryId: '21',
        name: 'home',
        teamHome: 'home',
        teamAway: 'away',
        categoryName: 'horse racing',
        liveStreamAvailable: 'false',
        startTime: new Date().getTime(),
        typeName: 'horse racing',
        markets: [{
          outcomes: [{
            outcomeMeaningMinorCode: 1,
            name: 'greyhound racing'
          },
          {
            name: 'greyhound racing'
          }]
        }]
      } as any;
      service['eventSchema'] = {
        'broadcastOfEvent': {
          'competitor': []
        }
      };
      service.competitors(event);
      event.markets = [{}]
      service.competitors(event);
      event.markets = [{name: 'test'}];
      service.competitors(event);
      event.markets = [];
      service.competitors(event);
    });

    it('competitors other than HR/GH without minorcode', () => {
      createService();
      service['checkForSport'] = jasmine.createSpy().and.returnValue(false);
      service['checkForHorse'] = jasmine.createSpy().and.returnValue(false);
      const event = {
        categoryId: '18',
        name: 'home',
        categoryName: 'golf',
        liveStreamAvailable: 'false',
        startTime: new Date().getTime(),
        typeName: 'golf',
        markets: [{
          outcomes: [{
            name: 'home'
          }]
        }]
      } as any;
      service['eventSchema'] = {
        'broadcastOfEvent': {
          'competitor': []
        }
      };
      service.competitors(event);
    });

    it('competitors other than HR/GH without minorcode for empty array validation', () => {
      createService();
      service['checkForSport'] = jasmine.createSpy().and.returnValue(false);
      service['checkForHorse'] = jasmine.createSpy().and.returnValue(false);
      const event = {
        categoryId: '18',
        name: 'home',
        categoryName: 'golf',
        liveStreamAvailable: 'false',
        startTime: new Date().getTime(),
        typeName: 'golf',
        markets: [{ }]
      } as any;
      service['eventSchema'] = {
        'broadcastOfEvent': {
          'competitor': []
        }
      };
      service.competitors(event);
    });
  });

  describe('checkForSport', () => {
    it('checkForSport if event has id', () => {
      createService();
      const event = {
        categoryId: '1',
        name: 'home v away',
        teamHome: 'home',
        teamAway: 'away',
        categoryName: 'football',
        liveStreamAvailable: 'false',
        startTime: new Date().getTime(),
        typeName: 'football',
        markets: [{
          outcomes: [{
            name: 'home'
          }]
        }]
      } as any;
      service['checkForSport'](event);
    });
    it('checkForSport if event does not have id', () => {
      createService();
      const event = {
        categoryId: '19',
        name: 'home',
        teamHome: 'home',
        teamAway: 'away',
        categoryName: 'horse racing',
        liveStreamAvailable: 'false',
        startTime: new Date().getTime(),
        typeName: 'horse racing',
        markets: [{
          outcomes: [{
            name: 'greyhound racing'
          }]
        }]
      } as any;
      service['checkForSport'](event);
    });
  });

  describe('checkForHorse', () => {
    it('checkForSport if event does not have id', () => {
      createService();
      const event = {
        categoryId: '1',
        name: 'home v away',
        teamHome: 'home',
        teamAway: 'away',
        categoryName: 'football',
        liveStreamAvailable: 'false',
        startTime: new Date().getTime(),
        typeName: 'football',
        markets: [{
          outcomes: [{
            name: 'home'
          }]
        }]
      } as any;
      service['checkForHorse'](event);
    });
    it('checkForHorse if event have id', () => {
      createService();
      const event = {
        categoryId: '21',
        name: 'home',
        teamHome: 'home',
        teamAway: 'away',
        categoryName: 'horse racing',
        liveStreamAvailable: 'false',
        startTime: new Date().getTime(),
        typeName: 'horse racing',
        markets: [{
          outcomes: [{
            outcomeMeaningMinorCode: 1,
            name: 'greyhound racing'
          },
          {
            name: 'greyhound racing'
          }]
        }]
      } as any;
      service['checkForHorse'](event);
    });
  });

  describe('organisationPageSeo', () => {
    const event = [{
        href: 'https://www.facebook.com/coral'
      },
      {
        href: 'https://www.facebook.com/coral'
      },
      {
        href: 'https://www.facebook.com/coral'
      }] as any;
    beforeEach(() => {
      windowRef = {
        nativeWindow: {
          location: {
            pathname: '/',
            origin: 'https://'
          },
          gcData: {
            brand:'coral'
          },
          document: {
            querySelector: jasmine.createSpy('querySelector').and.returnValue(domElement)
          }
        },
        document: {
          querySelectorAll: jasmine.createSpy('querySelectorAll').and.returnValue(event),
          createElement: jasmine.createSpy('createElement').and.returnValue({ type: 'type', text: '' })
        }
      };
    });
    it('#organisationPageSeo when brand is coral', () => {
      createService();
      windowRef.nativeWindow.gcData.brand = 'Coral';
      service.organisationPageSeo();
      expect(windowRef.nativeWindow.document.querySelector).toHaveBeenCalled();
    });
    it('#organisationPageSeo when brand is lads', () => {
      createService();
      windowRef.nativeWindow.gcData.brand = 'ladbrokes';
      service.organisationPageSeo();
      expect(windowRef.nativeWindow.document.querySelector).toHaveBeenCalled();
    });
  });

  it('doUpdate', () => {
    createService();

    service['doUpdate'](<any>{
      description: 'abc'
    });
    expect(windowRef.nativeWindow.document.querySelector).toHaveBeenCalledWith('meta[name=description]');
    expect(domElement.setAttribute).toHaveBeenCalledWith('content', 'abc');
    expect(pubsub.publish).toHaveBeenCalledWith(pubSubApi.SEO_DATA_UPDATED, [{
      description: 'abc'
    }]);
  });

  describe('constructor with getSeoPagesPaths', () => {
    it('should subscribe only once to router events', fakeAsync(() => {
      spyOn(router.events, 'subscribe').and.callThrough();

      createService();
      service['getSeoPagesPaths']();
      tick();

      expect(cms.getSeoPagesPaths).toHaveBeenCalledTimes(2);
      expect(router.events.subscribe).toHaveBeenCalledTimes(1);
    }));

    it('should handle only NavigationEnd router event', fakeAsync(() => {
      createService();

      windowRef.nativeWindow.location.pathname = 'test';
      routeSubject.next(new NavigationStart(0, 'test', ));
      tick(150);

      expect(cms.getSeoPage).toHaveBeenCalledTimes(1);
    }));
  });
  describe('#handlePaths', () => {
    it('should subscribe to getseopage and call doUpdate', fakeAsync(() => {
      const paths = { 1: '/sports/matchs', 2: '/inplay' };
      const page = { title: 'test update', description: 'test' };
      createService();
      spyOn(service as any, 'doUpdate').and.callThrough();
      service['handlePaths'](paths);
      tick();
      expect(service['isAutoSEO']).toBeFalse();
      expect(cms.getSeoPage).toHaveBeenCalledWith('askjdhsakjd');
    }));
    it('should subscribe to getAutoseopages and publish the data object', () => {
      const paths = { 1: '/sports/matchs', 2: '/inplay' };
      createService();
      service['handlePaths'](paths);
      expect(cms.getAutoSeoPages).toHaveBeenCalled();
      expect(pubsub.publish).toHaveBeenCalledWith('AUTO_SEOTAGS_DATA_UPDATED', [jasmine.any(Object)]);
    });
  });
});
