import environment from '@environment/oxygenEnvConfig';
import { RoutingHelperService } from './routing-helper.service';
import { of } from 'rxjs';

describe('RoutingHelperService', () => {
  let service: RoutingHelperService;
  let sportsConfigHelperService;
  let routingState;

  beforeEach(() => {
    sportsConfigHelperService = {
      getSportPathByName: jasmine.createSpy('getSportPathByName').and.returnValue(of())
    };
    routingState = {
      getPreviousSegment: jasmine.createSpy().and.returnValue('test')
    };
    service = new RoutingHelperService(sportsConfigHelperService, routingState);
  });

  it('constructor', () => {
    expect(service['racingCategories']).toEqual(environment.CATEGORIES_DATA.racing);
    expect(service['racingIds']).toEqual([ 21, 19, 39, 39, 39, 39 ]);
  });

  it('encodeUrlPart', () => {
    expect(service.encodeUrlPart('ASaA')).toEqual('asaa');
    expect(service.encodeUrlPart('ASa-A-')).toEqual('asa-a');
    expect(service.encodeUrlPart('ASa+A+')).toEqual('asa-a');
  });

  describe('formEdpUrl', () => {
    it('sport', () => {
      expect(service.formEdpUrl(<any>{
        categoryId: 16,
        name: 'liverpool vs newcastle',
        categoryName: 'Football',
        className: 'England',
        typeName: 'Premier League',
        id: '2345671'
      })).toEqual('event/football/england/premier-league/liverpool-vs-newcastle/2345671');
    });
    it('isRacing', () => {
      expect(service.formEdpUrl(<any>{
        categoryId: 21,
        name: 'Hamilton 20:20',
        categoryName: 'Racing',
        className: 'England',
        typeName: 'Hamilton',
        id: '2345671'
      })).toEqual('/racing/england/hamilton/hamilton-20-20/2345671');
    });
  });

  describe('#formSportUrl', () => {
    it('should return /football', () => {
      service.formSportUrl('football').subscribe((data) => {
        expect(data).toEqual('/football');
      });
    });

    it('should return sportPath with location', () => {
      sportsConfigHelperService.getSportPathByName = jasmine.createSpy('getSportPathByName').and.returnValue(of('path'));

      service.formSportUrl('football', 'eu').subscribe((data) => {
        expect(data).toEqual('/path/eu');
      });
    });

    it('should return only sportPath', () => {
      sportsConfigHelperService.getSportPathByName = jasmine.createSpy('getSportPathByName').and.returnValue(of('path'));

      service.formSportUrl('football').subscribe((data) => {
        expect(data).toEqual('/path');
      });
    });


  });

  it('formCompetitionUrl', () => {
    expect(service.formCompetitionUrl(<any>{
      sport: 'football',
      className: 'England',
      typeName: 'Premier league'
    })).toEqual('/competitions/football/england/premier-league');
  });

  it('formResultedEdpUrl + origin', () => {
    expect(service.formResultedEdpUrl(<any>{
      categoryId: 16,
      name: 'liverpool vs newcastle',
      categoryName: 'Football',
      className: 'England',
      typeName: 'Premier League',
      id: '2345671'
    }, '?origin=next-races')).toEqual('event/football/england/premier-league/liverpool-vs-newcastle/2345671?origin=next-races');
  });

  it('formResultedEdpUrl', () => {
    expect(service.formResultedEdpUrl(<any>{
      categoryId: 16,
      name: 'liverpool vs newcastle',
      categoryName: 'Football',
      className: 'England',
      typeName: 'Premier League',
      id: '2345671'
    })).toEqual('event/football/england/premier-league/liverpool-vs-newcastle/2345671');
  });

  it('formResultedEdpUrl: isResulted', () => {
    expect(service.formResultedEdpUrl(<any>{
      categoryId: 16,
      name: 'liverpool vs newcastle',
      categoryName: 'Football',
      className: 'England',
      typeName: 'Premier League',
      id: '2345671',
      isResulted: true
    })).toEqual('event/football/england/premier-league/liverpool-vs-newcastle/2345671');
  });

  it('#formInplayUrl', () => {
    const res = service.formInplayUrl('someSport');
    expect(res).toEqual('/in-play/someSport');
  });

  it('formSportCompetitionsUrl', () => {
    const res = service.formSportCompetitionsUrl('sport/someSport');
    expect(res).toEqual('/sport/someSport/competitions');
  });

  describe('getLastUriSegment', () => {
    it('should parse Uri with trailing slash', () => {
      const result = service.getLastUriSegment('/test/');
      expect(result).toEqual('test');
    });

    it('should parse Uri without trailing slash', () => {
      const result = service.getLastUriSegment('/test');
      expect(result).toEqual('test');
    });

    it('should return empty string', () => {
      const result = service.getLastUriSegment('');
      expect(result).toEqual('');
    });
  });

  it('getPreviousSegment', () => {
    expect(service.getPreviousSegment()).toEqual('test');
  });

  describe('#formFiveASideUrl', () => {
    it('should form 5-a-side Url', () => {
    const result = service.formFiveASideUrl( 'Football', 'England', 'Premier League', 'liverpool vs newcastle', '2345671');
        expect(result).toEqual('/football/england/premier-league/liverpool-vs-newcastle/2345671');
    });
  });
});
