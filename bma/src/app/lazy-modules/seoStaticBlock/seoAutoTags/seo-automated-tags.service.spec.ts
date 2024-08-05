import { of as observableOf, Subject } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { SeoAutomatedTagsService } from '@lazy-modules/seoStaticBlock/seoAutoTags/seo-automated-tags.service';
import { autoSeoConstants } from '@lazy-modules/seoStaticBlock/seoAutoTags/seo-automated-tags.constant';
import environment from '@environment/oxygenEnvConfig';

describe('SeoAutomatedTagsService', () => {
  let service: SeoAutomatedTagsService;
  let windowRef;
  let cms;
  let pubsub;
  let router;
  let routeSubject;
  let domElement;
  let timeService;

  beforeEach(() => {
    routeSubject = new Subject();
    domElement = {
      setAttribute: jasmine.createSpy('setAttribute'),
      appendChild: jasmine.createSpy('appendChild'),
      removeChild: jasmine.createSpy('removeChild')
    };
    windowRef = {
      nativeWindow: {
        location: {
          pathname: '/',
          origin: 'https://'
        },
        document: {
          querySelector: jasmine.createSpy('querySelector').and.returnValue(domElement),
          createElement: jasmine.createSpy('createElement').and.returnValue({ type: 'type', text: '' }),
          getElementById: jasmine.createSpy('getElementById')
        }
      }
    };
    cms = {
      getSeoPagesPaths: jasmine.createSpy('getSeoPagesPaths').and.returnValue(observableOf({
        '/': 'askjdhsakjd',
        'test': 'bcd'
      })),
      getAutoSeoPages: jasmine.createSpy('getAutoSeoPages').and.returnValue(observableOf({
        '/event': { metaTitle: 'bet on <event>|<competition>', metaDescription: 'bet on <event>' },
        '/outrights': { metaTile: 'outright title|<sport>', metaDescription: 'outright description|<sport>' }
      })),
      getSeoPage: jasmine.createSpy('getSeoPage').and.returnValue(observableOf({
        '/': 'askjdhsakjd',
        'test': 'bcd'
      }))
    };
    pubsub = {
      publish: jasmine.createSpy('publish'),
      subscribe: jasmine.createSpy('subscribe'),
      API: pubSubApi
    };
    router = {
      events: routeSubject,
      url:'/event/teamA-v-teamB'
    };
    service = new SeoAutomatedTagsService(windowRef, cms, pubsub, router);    
  });
  function createService() {
    service = new SeoAutomatedTagsService(windowRef, cms, pubsub, router);
  }
  describe('constructor', () => {
    it('should subscribe to data from cms and call loadAutoseopages method', fakeAsync(() => {
      const autoSeoData = { isOutright: false, typeName: 'World Cup', categoryName: 'football', name: 'teamA v teamB' };
      const autoseopagesdata = {
        '/event': { metaTitle: 'bet on <event>|<competition>', metaDescription: 'bet on <event>' },
      };
      pubsub.subscribe.and.callFake((autoAutomatedtags, listeners, handler) => { if (listeners == 'AUTO_SEOTAGS_DATA_UPDATED'){
        handler(autoseopagesdata);
      }else if(listeners == 'AUTOSEO_DATA_UPDATED'){
          handler(autoSeoData);
        }
       });
      createService();
      tick();
      spyOn(service as any,'getSeoPagesPaths').and.callFake(()=>{service['isAutoSEO']=true;});
      spyOn(service as any,'loadAutoSeoPage').and.callThrough();
      spyOn(service as any,'removeSchema');
      spyOn(service as any,'schemaForMultipleEvents');
      service['getSeoPagesPaths']();
      service['loadAutoSeoPage'](autoseopagesdata);
      expect(service['getSeoPagesPaths']).toHaveBeenCalled();
      expect(pubsub.subscribe).toHaveBeenCalledWith(autoSeoConstants.subscriberName, 'AUTO_SEOTAGS_DATA_UPDATED', jasmine.any(Function));
      expect(service['loadAutoSeoPage']).toHaveBeenCalledWith(autoseopagesdata);
      expect(service['isAutoSEO']).toBeTrue();
    }));
    it('should subscribe to data from cms and not call loadAutoseopages method if autoseopagesdata is empty ', fakeAsync(() => {
      const autoSeoData = { isOutright: false, typeName: 'World Cup', categoryName: 'football', name: 'teamA v teamB' };
      const autoseopagesdata = undefined;
      pubsub.subscribe.and.callFake((autoAutomatedtags, listeners, handler) => { if (listeners == 'AUTO_SEOTAGS_DATA_UPDATED'){
        handler(autoseopagesdata);
      }else if(listeners === 'AUTOSEO_DATA_UPDATED'){
          handler(autoSeoData);
        }
       });
      createService();
      tick();
      spyOn(service as any,'getSeoPagesPaths').and.callFake(()=>{service['isAutoSEO']=true;});
      service['getSeoPagesPaths']();
      spyOn(service as any,'loadAutoSeoPage').and.callThrough();
      expect(pubsub.subscribe).toHaveBeenCalledWith(autoSeoConstants.subscriberName, 'AUTO_SEOTAGS_DATA_UPDATED', jasmine.any(Function));
      expect(service['loadAutoSeoPage']).not.toHaveBeenCalledWith(autoseopagesdata);
      expect(service['isAutoSEO']).toBeTrue();
    }));
  });
  describe('loadAutoSeoPage', () => {
    it('should define splitedUrl and activeUrl', () => {
      const splitedUrl = jasmine.createSpy('splitedUrl');
      const activeUrl =  jasmine.createSpy('activeUrl');
      const autoseopagesdata = {
        '/event': { metaTitle: 'bet on <event>|<competition>', metaDescription: 'bet on <event>' }
      };
      const currentAutoSeo_Page = { metaTitle: 'bet on <event>|<competition>', metaDescription: 'bet on <event>' };
      service['loadAutoSeoPage'](autoseopagesdata);
      expect(splitedUrl).toBeDefined();
      expect(activeUrl).toBeDefined();
      expect(currentAutoSeo_Page).toEqual(autoseopagesdata['/event']);
    });
    it('should assign autoseopage tile and description if currentAutoseopage is defined', () => {
      const autoSeoData = { isOutright: false, typeName: 'World Cup', categoryName: 'football', name: 'teamA v teamB' };
      const autoseopagesdata = {
        '/event': { metaTitle: 'bet on <event>|<competition>', metaDescription: 'bet on <event>' }
      };
      const resultedautoseopagesdata = {
        metaTitle: 'bet on teamA - teamB|World Cup', metaDescription: 'bet on teamA - teamB'
      };
      const currentAutoSeo_Page = { metaTitle: 'bet on <event>|<competition>', metaDescription: 'bet on <event>' };
      spyOn(service as any, 'replaceAutoSeoPage').and.callThrough();
      service['isAutoSEO'] = true;
      pubsub.subscribe.and.callFake((autoAutomatedtags, listeners, handler) =>  { if(listeners === 'AUTOSEO_DATA_UPDATED'){
        handler(autoSeoData);
      }});
      service['loadAutoSeoPage'](autoseopagesdata);
      expect(pubsub.subscribe).toHaveBeenCalledWith(autoSeoConstants.subscriberName, 'AUTOSEO_DATA_UPDATED', jasmine.any(Function));
      expect(currentAutoSeo_Page).toEqual(autoseopagesdata['/event']);
      expect(service['autoseo_Page']['title']).toEqual(resultedautoseopagesdata.metaTitle);
      expect(service['autoseo_Page']['description']).toEqual(resultedautoseopagesdata.metaDescription);
      expect(service['replaceAutoSeoPage']).toHaveBeenCalledWith(service['autoseo_Page'], autoSeoData);
    });
    it('should assign default tile and description if currentAutoseopage is undefined', () => {
      router.url = '/coupons/teamA-v-TeamB';
      const autoseopagesdata = {
        '/event': { metaTitle: 'bet on <event>|<competition>', metaDescription: 'bet on <event>' },
        '/outrights': { metaTile: 'outright title', metaDescription: 'outright description' }
      };
      spyOn(service as any, 'doUpdate').and.callThrough();
      service['isAutoSEO'] = true;
      service['loadAutoSeoPage'](autoseopagesdata);
      expect(service['isAutoSEO']).toBeFalse();
      expect(service['doUpdate']).toHaveBeenCalled();
    });
    it('should not overide the title if isAutoseo is false and assign default or manual title and description', () => {
      const autoSeoData = { isOutright: false, typeName: 'World Cup', categoryName: 'football', name: 'teamA v teamB' };
      const autoseopagesdata = {
        '/event': { metaTitle: 'bet on <event>|<competition>', metaDescription: 'bet on <event>' },
        '/outrights': { metaTile: 'outright title', metaDescription: 'outright description' }
      };
      const currentAutoSeo_Page = { metaTitle: 'bet on <event>|<competition>', metaDescription: 'bet on <event>' };
      spyOn(service as any, 'replaceAutoSeoPage').and.callThrough();
      service['isAutoSEO'] = false;
      pubsub.subscribe.and.callFake((autoAutomatedtags, listeners, handler) => {if(listeners === 'AUTOSEO_DATA_UPDATED'){
        handler(autoSeoData);
      }});
      service['loadAutoSeoPage'](autoseopagesdata);
      expect(pubsub.subscribe).toHaveBeenCalledWith(autoSeoConstants.subscriberName, 'AUTOSEO_DATA_UPDATED', jasmine.any(Function));
      expect(service['autoseo_Page']['title']).not.toEqual(currentAutoSeo_Page.metaTitle);
      expect(service['autoseo_Page']['description']).not.toEqual(currentAutoSeo_Page.metaDescription);
      expect(service['replaceAutoSeoPage']).not.toHaveBeenCalledWith(service['autoseo_Page'], autoSeoData);
    });
    it('should assign outright template if isOutright is true and defined in autoseopages object', fakeAsync(() => {
      const autoSeoData = { isOutright: true, typeName: 'World Cup', categoryName: 'football', name: 'teamA v teamB' };
      const autoseopagesdata = {
        '/event': { metaTitle: 'bet on <event>|<competition>', metaDescription: 'bet on <event>' },
        '/outrights': { metaTitle: 'outright title <event>', metaDescription: 'outright description <event>' }
      };
      const resultedautoseopagesdata = {
          metaTitle: 'outright title teamA - teamB', metaDescription: 'outright description teamA - teamB' };
      spyOn(service as any, 'replaceAutoSeoPage').and.callThrough();
      service['isAutoSEO'] = true;
      pubsub.subscribe.and.callFake((autoAutomatedtags, listeners, handler) => {if(listeners === 'AUTOSEO_DATA_UPDATED'){
        handler(autoSeoData);
      }});
      service['loadAutoSeoPage'](autoseopagesdata);
      tick();
      expect(pubsub.subscribe).toHaveBeenCalledWith(autoSeoConstants.subscriberName, 'AUTOSEO_DATA_UPDATED', jasmine.any(Function));
      expect(service['autoseo_Page']['title']).toEqual(resultedautoseopagesdata.metaTitle);
      expect(service['autoseo_Page']['description']).toEqual(resultedautoseopagesdata.metaDescription);
      expect(service['replaceAutoSeoPage']).toHaveBeenCalledWith(service['autoseo_Page'], autoSeoData);
    }));
    it('should not assign outright template if isOutright is true and undefined in autoseopages object', fakeAsync(() => {
      const autoseopagesdata = {
        '/event': { metaTitle: 'bet on <event>|<competition>', metaDescription: 'bet on <event>' }
      };
      service['isAutoSEO'] = true;
      service['loadAutoSeoPage'](autoseopagesdata);
      tick();
      expect(pubsub.subscribe).toHaveBeenCalledWith(autoSeoConstants.subscriberName, 'AUTOSEO_DATA_UPDATED', jasmine.any(Function));
      expect(service['autoseo_Page']['title']).toBeUndefined();
      expect(service['autoseo_Page']['description']).toBeUndefined();
    }));
    it('should not assign outright template if isOutright is false and undefined in autoseopages object', () => {
      const autoseopagesdata = {
        '/event': { metaTitle: 'bet on <event>|<competition>', metaDescription: 'bet on <event>' },
      };
      service['isAutoSEO'] = true;
      service['loadAutoSeoPage'](autoseopagesdata);
      expect(pubsub.subscribe).toHaveBeenCalledWith(autoSeoConstants.subscriberName, 'AUTOSEO_DATA_UPDATED', jasmine.any(Function));
      expect(service['autoseo_Page']['title']).toBeUndefined();
      expect(service['autoseo_Page']['description']).toBeUndefined();
    });
  });
  describe('formatFirstLetter', () => {
    it('should return string with first letter as captial', () => {
      const autoseoplaceholder = 'football';
      expect(service['formatFirstLetter'](autoseoplaceholder)).toEqual('Football')
    });
    it('should not return string with first letter as captial', () => {
      const autoseoplaceholder = '';
      expect(service['formatFirstLetter'](autoseoplaceholder)).not.toEqual('Football')
    });
  });
  describe('replaceAutoSeoPage', () => {
    it('should replace all the placeholders as required and call doUpdate', () => {
      const autoSeoData = { isOutright: true, typeName: 'World Cup', categoryName: 'football', name: 'teamA v teamB' };
      service['autoseo_Page'] = { title: 'bet on <event>|<competition> <sport>|<brand>', description: 'bet on <event>|<competition> <sport>|<brand>' };
      environment.brand = 'bma';
      spyOn(service as any, 'doUpdate');
      service['replaceAutoSeoPage'](service['autoseo_Page'],autoSeoData);
      expect(service['autoseo_Page']['title']).toEqual('bet on teamA - teamB|World Cup Football|Coral');
      expect(service['autoseo_Page']['description']).toEqual('bet on teamA - teamB|World Cup Football|Coral');
      expect(service['doUpdate']).toHaveBeenCalledWith(service['autoseo_Page']);
    });
    it('should replace all the placeholders as required and call doUpdate with brand as ladbrokes', () => {
      const autoSeoData = { isOutright: true, typeName: 'World Cup', categoryName: 'football', name: 'teamA v teamB' };
      service['autoseo_Page'] = { title: 'bet on <event>|<competition> <sport>|<brand>', description: 'bet on <event>|<competition> <sport>|<brand>' };
      environment.brand = 'ladbrokes';
      spyOn(service as any, 'doUpdate');
      service['replaceAutoSeoPage'](service['autoseo_Page'],autoSeoData);
      expect(service['autoseo_Page']['title']).toEqual('bet on teamA - teamB|World Cup Football|Ladbrokes');
      expect(service['autoseo_Page']['description']).toEqual('bet on teamA - teamB|World Cup Football|Ladbrokes');
      expect(service['doUpdate']).toHaveBeenCalledWith(service['autoseo_Page']);
    }); 
  });
  describe('schemaForMultipleEvents', () => {
    it('should assign schema object and remove and append if script.id is not null', () => {
      Date.prototype.getTimezoneOffset = jasmine.createSpy('getTimezoneOffset').and.callFake(() => {
        return -330;
      });
      const events = [{
        id: 24458910,
        name: "Catterick",
        categoryId: "21",
        categoryName: "Horse Racing",
        typeName: "Catterick",
        startTime: "2023-05-03T17:00:00Z",
        localTime:"17:00",
        originalName: "16:15 Catterick",
        url: 'horse-racing/horse-racing-live/kempton/16-15-Catterick/24458910/'
      }];
      const url = '/horse-racing/featured';
      const dummyPreviousTag = document.createElement('script')
      dummyPreviousTag.id = url;
      document.getElementById = jasmine.createSpy('html element').and.returnValue(dummyPreviousTag);
      pubsub.subscribe.and.callFake((a, b, cb) => {
        if(b=='SCHEMA_DATA_UPDATED'){
          document.querySelector('head').append(dummyPreviousTag);
          cb(events,url);
        }
      });
      createService();
      service['schemaForMultipleEvents']();
      expect(service['eventsSchema']).toEqual(
        [{ '@context': 'https://schema.org', '@type': 'SportsEvent', name: '16:15 Catterick', description: 'Horse Racing', startDate: '2023-05-03T17:00:00+05:30', location: { '@type': 'city', name: 'Catterick' }, url: 'https:///horse-racing/horse-racing-live/kempton/16-15-Catterick/24458910/' }]);
    });
    it('should assign schema object and appendchild if script.id is null', () => {
      Date.prototype.getTimezoneOffset = jasmine.createSpy('getTimezoneOffset').and.callFake(() => {
        return -330;
      });
      const events = [{
        id: 24458910,
        name: "Catterick",
        categoryId: "21",
        categoryName: "Horse Racing",
        typeName: "Catterick",
        startTime: "2023-05-03T17:00:00Z",
        localTime:"17:00",
        originalName: "16:15 Catterick",
        url: 'horse-racing/horse-racing-live/kempton/16-15-Catterick/24458910/'
      }];
      const url = '/horse-racing/featured';
      document.getElementById = jasmine.createSpy('html element').and.returnValue(null);
      pubsub.subscribe.and.callFake((autoAutomatedtags, listeners, handler) => {
        if (listeners === 'SCHEMA_DATA_UPDATED') {
          handler(events, url);
        }
      });
      createService();
      service['schemaForMultipleEvents']();
      expect(service['eventsSchema']).toEqual(
        [{ '@context': 'https://schema.org', '@type': 'SportsEvent', name: '16:15 Catterick', description: 'Horse Racing', startDate: '2023-05-03T17:00:00+05:30', location: { '@type': 'city', name: 'Catterick' }, url: 'https:///horse-racing/horse-racing-live/kempton/16-15-Catterick/24458910/' }]);
    });
    it('should assign schema object and appendchild if script.id is null', () => {
      Date.prototype.getTimezoneOffset = jasmine.createSpy('getTimezoneOffset').and.callFake(() => {
        return -330;
      });
      const events = [{
        id: 24458910,
        name: "Catterick",
        categoryId: "21",
        categoryName: "Horse Racing",
        typeName: "Catterick",
        startTime: "2023-05-03T17:00:00Z",
        localTime:"17:00",
        originalName: "16:15 Catterick",
        url: 'horse-racing/horse-racing-live/kempton/16-15-Catterick/24458910/'
      }];
      const url = '/horse-racing/featured';
      document.getElementById = jasmine.createSpy('html element').and.returnValue(null);
      pubsub.subscribe.and.callFake((autoAutomatedtags, listeners, handler) => {
        if (listeners === 'SCHEMA_DATA_UPDATED') {
          handler(events, url);
        }
      });
      createService();
      service['schemaForMultipleEvents']();
      expect(service['eventsSchema']).toEqual(
        [{ '@context': 'https://schema.org', '@type': 'SportsEvent', name: '16:15 Catterick', description: 'Horse Racing', startDate: '2023-05-03T17:00:00+05:30', location: { '@type': 'city', name: 'Catterick' }, url: 'https:///horse-racing/horse-racing-live/kempton/16-15-Catterick/24458910/' }]);
    });
    it('should assign undefined/null if events is undefined/null', () => {
      Date.prototype.getTimezoneOffset = jasmine.createSpy('getTimezoneOffset').and.callFake(() => {
        return -330;
      });
      const events = undefined;
      const url = '/horse-racing/featured';
      pubsub.subscribe.and.callFake((autoAutomatedtags, listeners, handler) => {
        if (listeners == 'SCHEMA_DATA_UPDATED') {
          handler(events, url);
        }
      });
      createService();
      service['schemaForMultipleEvents']();
      expect(service['eventsSchema']).toBeUndefined();
    });
    it('should assign undefined/null if events is undefined/null events[0] is null', () => {
      Date.prototype.getTimezoneOffset = jasmine.createSpy('getTimezoneOffset').and.callFake(() => {
        return -330;
      });
      const events = [null];
      const url = '/horse-racing/featured';
      pubsub.subscribe.and.callFake((autoAutomatedtags, listeners, handler) => {
        if (listeners == 'SCHEMA_DATA_UPDATED') {
          handler(events, url);
        }
      });
      createService();
      service['schemaForMultipleEvents']();
      expect(service['eventsSchema']).toEqual([]);
    });
    it('should assign name if it is other than HR and GH', () => {
      Date.prototype.getTimezoneOffset = jasmine.createSpy('getTimezoneOffset').and.callFake(() => {
        return -330;
      });
      const events = [{
        id: 24458910,
        name: "teamA vs teamB",
        categoryId: "18",
        categoryName: "Horse Racing",
        typeName: "Catterick",
        startTime: "2023-05-03T17:00:00Z",
        originalName: "16:15 Catterick",
        url: 'horse-racing/horse-racing-live/kempton/16-15-Catterick/24458910/'
      }];
      document.getElementById = jasmine.createSpy('html element').and.returnValue(null);
      const url = '/horse-racing/featured';
      pubsub.subscribe.and.callFake((autoAutomatedtags, listeners, handler) => {
        if (listeners == 'SCHEMA_DATA_UPDATED') {
          handler(events, url);
        }
      });
      createService();
      service['schemaForMultipleEvents']();
      expect(service['eventsSchema']).toEqual(
        [{ '@context': 'https://schema.org', '@type': 'SportsEvent', name: 'teamA vs teamB', description: 'Horse Racing', startDate: '2023-05-03T17:00:00+05:30', location: { '@type': 'city', name: 'Catterick' }, url: 'https:///horse-racing/horse-racing-live/kempton/16-15-Catterick/24458910/',competitor:[{ '@type': 'SportsTeam', name: 'teamA' },{ '@type': 'SportsTeam', name: 'teamB' }] }]); 
    });
    it('should assign competitior if it is other than HR and GH', () => {
      Date.prototype.getTimezoneOffset = jasmine.createSpy('getTimezoneOffset').and.callFake(() => {
        return -330;
      });
      const events = [{
        id: "2563519",
        name: "IND vs NZ",
        startTime: "2023-02-15T05:54:00Z",
        sportId: "16",
        categoryId: "16",
        categoryCode: "FOOTBALL",
        categoryName: "Football",
        typeName: "Premier League",
        url: "/event/football/english/premier-league/indvsnz/2563519/"
      }];
      document.getElementById = jasmine.createSpy('html element').and.returnValue(null);
      const url = '/horse-racing/featured';
      pubsub.subscribe.and.callFake((autoAutomatedtags, listeners, handler) => {
        if (listeners == 'SCHEMA_DATA_UPDATED') {
          handler(events, url);
        }
      });
      createService();
      service['schemaForMultipleEvents']();
      expect(service['eventsSchema']).toEqual([{
        '@context': 'https://schema.org', '@type': 'SportsEvent', name: 'IND vs NZ', description: 'Football', startDate: '2023-02-15T05:54:00+05:30', location: {
          '@type': 'city', name: 'Premier League'
        }, url: 'https:////event/football/english/premier-league/indvsnz/2563519/', competitor: [{
          '@type': 'SportsTeam', name: 'IND'
        }, { '@type': 'SportsTeam', name: 'NZ' }]
      }]
      );
    });
  });

  describe('removeSchema', () => {
    it('should call head.removechild', () => {
      const url = '/horse-racing/featured';
      const dummyPreviousTag = document.createElement('script');
      dummyPreviousTag.id = url;
      document.getElementById = jasmine.createSpy('html element').and.returnValue(dummyPreviousTag);
      pubsub.subscribe.and.callFake((a, b, cb) => {
        if(b=='SCHEMA_DATA_REMOVED'){
          document.querySelector('head').append(dummyPreviousTag);
          cb(url);
        }
      });
      createService();
      service['removeSchema']();
      expect(windowRef.nativeWindow.document.querySelector).toHaveBeenCalled();
    });
    it('should call not call head.removechild', () => {
      const url = '/horse-racing/featured';
      document.getElementById = jasmine.createSpy('html element').and.returnValue(null);
      pubsub.subscribe.and.callFake((a, b, cb) => {
        if(b=='SCHEMA_DATA_REMOVED'){
          cb(url);
        }
      });
      createService();
      service['removeSchema']();
      expect(windowRef.nativeWindow.document.querySelector).toHaveBeenCalled();
    });
  });
  describe('getseoSchemastartTime', () => {
    it('should return Europe time Zone convereted time with +5:30 appeneded if isRacing is true', () => {
      Date.prototype.getTimezoneOffset = jasmine.createSpy('getTimezoneOffset').and.callFake(() => {
        return -330;
      });
      createService();
      const startTime = service['getseoSchemastartTime']('2023-05-03T17:00:00Z', true, '18:00');
      expect(startTime).toEqual('2023-05-03T18:00:00+05:30');
    });
    it('should return empty string if starttime is undefined', () => {
      Date.prototype.getTimezoneOffset = jasmine.createSpy('getTimezoneOffset').and.callFake(() => {
        return -330;
      });
      createService();
      const startTime = service['getseoSchemastartTime'](undefined, true, '18:00');
      expect(startTime).toEqual('');
    });
    it('should return UTC time Zone convereted time with +5:30 appeneded if isRacing is true', () => {
      Date.prototype.getTimezoneOffset = jasmine.createSpy('getTimezoneOffset').and.callFake(() => {
        return -330;
      });
      createService();
      const startTime = service['getseoSchemastartTime']('2023-05-03T17:00:00Z', false, '18:00');
      expect(startTime).toEqual('2023-05-03T17:00:00+05:30');
    });
  });
  describe('getTimeZoneOffSet', () => {
    it('should return empty if timezoneoffset is null/undefined', () => {
      const timeZoneOffSet = null;
      createService();
      const timezoneStandard = service['getTimeZoneOffSet'](timeZoneOffSet);
      expect(timezoneStandard).toEqual('');
    });
    it('should return empty if timezoneoffset is null/undefined', () => {
      const timeZoneOffSet = undefined;
      createService();
      const timezoneStandard = service['getTimeZoneOffSet'](timeZoneOffSet);
      expect(timezoneStandard).toEqual('');
    });
    it('should return Z if timezoneoffset is 0', () => {
      const timeZoneOffSet = 0;
      createService();
      const timezoneStandard = service['getTimeZoneOffSet'](timeZoneOffSet);
      expect(timezoneStandard).toEqual('Z');
    });
    it('should return +05:30 if timezoneoffset is -330', () => {
      const timeZoneOffSet = -330;
      createService();
      const timezoneStandard = service['getTimeZoneOffSet'](timeZoneOffSet);
      expect(timezoneStandard).toEqual('+05:30');
    });
    it('should return -07:30 if timezoneoffset is 100', () => {
      const timeZoneOffSet = 330;
      createService();
      const timezoneStandard = service['getTimeZoneOffSet'](timeZoneOffSet);
      expect(timezoneStandard).toEqual('-05:30');
    });
  });
  describe('#paddingValue', () => {
    it('should padd 0 to theoffsetvalue', () => {
      const timeZoneOffSet = 5;
      createService();
      const timezoneStandard = service['paddingValue'](timeZoneOffSet);
      expect(timezoneStandard).toEqual('05');
    });
  });
});
