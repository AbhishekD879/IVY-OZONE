import { GtmTrackingService } from '@core/services/gtmTracking/gtm-tracking.service';
import environment from '@environment/oxygenEnvConfig';

describe('GtmTrackingService', () => {
  let service;
  let locationService;
  let sportTabsService;
  let storageService;
  let gamingService;
  const sectionTitle = 'sectionTitle';

  beforeEach(() => {
    environment['brand'] = 'bma';
    environment['CURRENT_PLATFORM'] = 'mobile';

    locationService = {
      path: jasmine.createSpy()
    };

    sportTabsService = {
      eventsBySections: jasmine.createSpy().and.returnValue([{sectionTitle: sectionTitle}])
    };

    storageService = {
      get: jasmine.createSpy(),
      set: jasmine.createSpy()
    };

    gamingService = {};

    service = new GtmTrackingService(locationService, sportTabsService, storageService, gamingService);
  });

  it('should create service', () => {
    expect(service).toBeTruthy();
  });

  describe('getTracking: ', () => {

    beforeEach(() => {
      service['gtmObject'] = {};
    });

    it('should get trace object', () => {
      expect(service.getTracking()).toBeTruthy();
    });
  });

  describe('restoreTracking: ', () => {

    it('should restore trace object', () => {
      service['gtmObject'] = null;
      service.restoreTracking({});

      expect(service['gtmObject']).toBeTruthy();
    });

    it('should not override service\' entity if empty trace object', () => {
      service['gtmObject'] = null;
      service.restoreTracking();

      expect(service['gtmObject']).toBeFalsy();
    });
  });

  it('should set location', () => {
    const location = 'location option';
    const sublocation = 'sublocation option';
    service.setLocation('location option', 'location');
    expect(service['location']).toEqual(location.toUpperCase());
    service.setLocation('sublocation option', 'sublocation');
    expect(service['subLocation']).toEqual(sublocation.toUpperCase());
  });

  it('should clear location', () => {
    service.clearLocation('location');
    service.clearLocation('sublocation');
    expect(service['location']).toEqual('');
    expect(service['subLocation']).toEqual('');
  });

  describe('collectiong and restoring placed bets', () => {
    let outcomeId = '333';
    let bet;
    let GTMObject;

    beforeEach(() => {
      outcomeId = '333';
      bet = {
        leg: [
          {
            sportsLeg: {
              legPart: [
                {
                  outcomeRef: {
                    id: outcomeId
                  }
                }
              ]
            }
          }
        ]
      };
      GTMObject = {
        tracking: {
          location: 'location',
          module: 'module',
          betType: undefined 
        }
      };

      storageService.get.and.returnValue([{
        outcomesIds: [outcomeId],
        GTMObject
      }]);
    });

    it('should collect placed bets origins', () => {
      service.collectPlacedBets([bet] as any);
      expect(storageService.get).toHaveBeenCalledWith('betSelections');
      expect(service['placedBetsOrigins']).toEqual({
        [outcomeId]: {
          location: GTMObject.tracking.location,
          module: GTMObject.tracking.module,
          betType: undefined 
        }
      });
    });

    it('should return placed bets origins with bet location as fanzone', () => {
      service.placedBetsOrigins = {
        "333": {
            "location": "NOW & NEXT",
            "module": "module"
        }
    }
      const result = service.getBetOrigin(outcomeId);
      expect(result).toEqual({ location: 'Fanzone', module: 'module', betType: undefined });
    });

    it('should check reuse bets', () => {
      storageService.get.and.returnValue({
        '333': {
          location: 'testlocation',
          module: 'testModule',
          betType: 'reuse'
        }
      });
      service.placedBetsOrigins = {
        "333": {
          "location": "NOW & NEXT",
          "module": "module"
        }
      }
      const result = service.getBetOrigin(outcomeId);
      expect(result).toEqual({
        location: 'testlocation',
        module: 'testModule',
        betType: 'reuse'
      });
    });

    it('should return placed bets origins', () => {
      service.collectPlacedBets([bet] as any);
      const result = service.getBetOrigin(outcomeId);
      expect(result).toEqual(GTMObject.tracking);
    });

    it('should restore bet GTM origin after reuse selection', () => {
      service.collectPlacedBets([bet] as any);
      service.restoreGtmTracking([outcomeId]);
      expect(storageService.get).toHaveBeenCalledWith('betSelections');
      expect(storageService.set).toHaveBeenCalledWith('betSelections', [{
        outcomesIds: [outcomeId],
        GTMObject
      }]);
    });
  });

  it('should detect location and module for virtual sports selection', () => {
    const module = 'VIRTUAL SPORT MODULE';
    const virtualSportEvent = {
      title: 'VIRTUAL SPORT TITLE'
    };

    const result = service.detectVirtualSportTracking(module, virtualSportEvent);

    expect(result).toEqual({
      location: virtualSportEvent.title,
      module: module
    });
  });

  it('should set location as fanzone for gtm', () => {
    service['gtmObject'] = {};
    service['gtmObject'].location = 'NOW & NEXT';

    const result = service.getTracking();

    expect(result).toEqual({
      location: 'Fanzone'
    });
  });

  describe('detectTracking', () => {
    let event;
    let market;
    const location = 'LOCATION';
    const subLocation = 'SUBLOCATION';
    const module = 'module name';

    beforeEach(() => {
      locationService.path.and.returnValue('/some/page');
      event = {
        localTime: '11:33',
        categoryName: 'Event Category',
      };
      market = {
        label: 'Market label',
        name: 'Market name',
      };
    });

    it('should set location and module by params', () => {
      service.setLocation(location, 'location');
      const result = service.detectTracking(module, '', event, market);
      expect(result).toEqual({
        location: location,
        module: module
      });
    });

    it('should set location, sublocation and module by params', () => {
      service.setLocation(location, 'location');
      service.setLocation(subLocation, 'sublocation');
      const result = service.detectTracking(module, '', event, market);
      expect(result.location).toEqual([location, subLocation].join('. '));
    });

    it('should detect module for event detail page', () => {
      const segment = 'eventMain';
      service.setLocation(location, 'location');
      const result = service.detectTracking('', segment, event, market);
      expect(result.module).toEqual('edp');
    });
     
    it('should detect module for event detail page with undefined value ', () => {
      const segment = 'eventMain';
      service.setLocation(location, 'location');
      const result = service.detectTracking(undefined, segment, event, market);
      expect(result.module).toEqual('edp');
    });

    it('should detect module for event detail page with null value ', () => {
      const segment = 'eventMain';
      service.setLocation(location, 'location');
      const result = service.detectTracking(null, segment, event, market);
      expect(result.module).toEqual('edp');
    });

    it('should detect module for matches tab', () => {
      const segment = 'sport.matches.tab';
      service.setLocation(location, 'location');
      const result = service.detectTracking('', segment, event, market);
      expect(result.module).toEqual(sectionTitle);
    });

    it('should set module empty string', () => {
      const segment = 'sport.matches.tab';
      service.setLocation(location, 'location');
      sportTabsService.eventsBySections = jasmine.createSpy().and.returnValue([{sectionTitle: ''}]);
      const result = service.detectTracking('', segment, event, market);
      expect(result.module).toEqual('');
    });

    it('should set module empty string with empty array', () => {
      const segment = 'sport.matches.tab';
      service.setLocation(location, 'location');
      sportTabsService.eventsBySections = jasmine.createSpy().and.returnValue([]);
      const result = service.detectTracking('', segment, event, market);
      expect(result.module).toEqual('');
    });

    it('should set HOME prefix for home location selections', () => {
      locationService.path.and.returnValue('/home');
      service.setLocation(location, 'location');
      service.detectTracking(module, '', event, market);
      expect(service['locationPrefix']).toEqual('HOME');
    });

    it('should set location for racing detail event page', () => {
      const segment = 'horseracing.eventMain';
      service.clearLocation('location');
      service.clearLocation('sublocation');
      const result = service.detectTracking(module, segment, event, market);
      expect(result.location).toEqual(event.localTime);
    });

    it('should set location for sport detile event page', () => {
      const segment = 'eventMain';
      service.clearLocation('location');
      service.clearLocation('sublocation');
      const result = service.detectTracking(module, segment, event, market);
      expect(result.location).toEqual(event.categoryName);
    });

    it('should set location for favourites page', () => {
      const segment = 'favourites';
      service.clearLocation('location');
      service.clearLocation('sublocation');
      const result = service.detectTracking(module, segment, event, market);
      expect(result.location).toEqual('FAVOURITES');
    });

    it('should set location from placedLocation', () => {
      const segment = 'favourites';
      service.clearLocation('location');
      service.clearLocation('sublocation');
      const result = service.detectTracking(module, segment, event, market, 'tips section');
      expect(result.location).toEqual('tips section');
    });
  });
});
