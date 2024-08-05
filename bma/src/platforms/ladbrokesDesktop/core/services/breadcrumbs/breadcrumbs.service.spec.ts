import { BreadcrumbsService } from '@ladbrokesDesktop/core/services/breadcrumbs/breadcrumbs.service';

describe('LDBreadcrumbsService', () => {
  let service: BreadcrumbsService;

  let locale;
  let location;

  beforeEach(() => {
    locale = {
      getString: jasmine.createSpy('getString')
    };
    location = {};

    service = new BreadcrumbsService(locale, location);
    service['config'] = {
      sportName: '',
      tabs: [],
      isEDPPage: true,
      competitionName: '',
      isOlympicsPage: false,
      isCompetitionPage: false,
      eventName: '',
      className: '',
      display: '',
      isFootballPage: false,
      isHorseRacingPage: false,
      isGreyhoundPage: false,
      isBuildYourRaceCardPage: false,
    } as any;
  });

  describe('#buildEDPBreadcrumb', () => {
    it('should build breadcrumb path for Greyhounds EDP', () => {
      service['config'].isGreyhoundPage = true;
      service['config'].eventName = 'Shepp dogs 25 oct';
      const pathArray = ['greyhound-racing', 'greyhounds-specials', 'watch-your-trap', 'shepp-dogs-25-oct', '8719238'];
      const result = service['buildEDPBreadcrumb'](pathArray);
      expect(result).toEqual(['greyhound-racing', 'event', 'Shepp dogs 25 oct']);
    });

    it('should build breadcrumb path for Greyhounds', () => {
      service['config'].isGreyhoundPage = true;
      service['config'].eventName = 'Shepp dogs 25 oct';
      service['breadcrumbsTitles'] = { 'greyhound-racing': 'greyhound racing', 'shepp-dogs-25-oct': 'Shepp dogs 25 oct' };
      const pathArray = ['greyhound-racing', 'shepp-dogs-25-oct'];
      const result = service['initializeBreadcrumbsList'](pathArray);
      expect(result).toEqual([
        { name: 'Home', targetUri: '/' },
        { name: 'greyhound racing', targetUri: '/greyhound-racing/next-races' },
        { name: 'Shepp dogs 25 oct', targetUri: '/greyhound-racing/shepp-dogs-25-oct' }
      ]);
    });

    it('should strip url params from breadcrumb name', () => {
      service['config'].sportName = 'football';
      service['config'].isCompetitionPage = false;
      service['breadcrumbsTitles'] = { 'football': 'Football', 'coupons?utm=test&something=123': 'coupons?utm=test&something=123'};
      const pathArray = ['football', 'coupons?utm=test&something=123'];
      const result = service['initializeBreadcrumbsList'](pathArray);
      expect(result).toEqual([
        {name: 'Home', targetUri: '/'},
        { name: 'Football', targetUri: '/sport/football' },
        { name: 'coupons', targetUri: '/sport/football/coupons?utm=test&something=123' }
      ]);
    });

    it('should build breadcrumb path for Football EDP', () => {
      service['config'].isFootballPage = true;
      service['config'].sportName = 'football';
      service['config'].eventName = 'Chelsea v Liverpool';
      const pathArray = ['event', 'football', 'england-championship', 'chelsea-v-liverpool', '8717353', 'main-markets'];
      const result = service['buildEDPBreadcrumb'](pathArray);
      expect(result).toEqual(['football', 'event', 'Chelsea v Liverpool']);
    });
    it('should build breadcrumb path for Olympics Archery EDP', () => {
      service['config'].isOlympicsPage = true;
      service['config'].sportName = 'archery';
      service['config'].eventName = 'foo v bar';
      const pathArray = ['olympics', 'archery', 'archery-all-archery', 'men-s-olympics', 'foo-v-bar', '8720690'];
      const result = service['buildEDPBreadcrumb'](pathArray);
      expect(result).toEqual(['olympics', 'archery', 'event', 'foo v bar']);
    });

    it('should call function getItemTitle with correct params order', () => {
      const pathArray = ['horseracing', 'test-event-name-with-dash-symbols'];
      service['getItemTitle'] = jasmine.createSpy('getItemTitle');
      (service as any).getPathTitles(pathArray, 'test-event-name-with-dash-symbols', 'horseracing');
      expect(service['getItemTitle'])
        .toHaveBeenCalledWith('test-event-name-with-dash-symbols', 'horseracing', 'test-event-name-with-dash-symbols');
    });

    it('should correctly form item title fo events with dash symbols in name', () => {
      (service  as any)
        .getItemTitle('test-event-name-with-dash-symbols', 'horseracing', 'test-event-name-with-dash-symbols');
      expect((service as any).breadcrumbsTitles).toEqual({ 'test-event-name-with-dash-symbols': 'test-event-name-with-dash-symbols' });
    });

    it('should get correct greyhounds path with getPathArray', () => {
      const pathMock = 'greyhound-racing/today';
      const builtPathMock = ['today', 'event'];

      spyOn(service as any, 'sliceArrayToFoundElement').and.callThrough();
      service['location'].path = jasmine.createSpy('path').and.returnValue(pathMock);

      service['config'].isGreyhoundPage = true;
      service['config'].sportName = 'football';

      const result = service['getPathArray']();

      expect(service['sliceArrayToFoundElement']).toHaveBeenCalledWith(builtPathMock, service['greyhoungUrlItemsRestrictors']);
      expect(result).toEqual(['today']);
    });

    it('should get correct sports path with getPathArray', () => {
      const pathMock = 'sport/football/matches/today';
      const builtPathMock = ['football', 'event'];

      spyOn(service as any, 'sliceArrayToFoundElement').and.callThrough();
      service['location'].path = jasmine.createSpy('path').and.returnValue(pathMock);

      service['config'].isGreyhoundPage = false;
      service['config'].sportName = 'football';

      const result = service['getPathArray']();

      expect(service['sliceArrayToFoundElement']).toHaveBeenCalledWith(builtPathMock, service['urlItemsRestrictors']);
      expect(result).toEqual(['football']);
    });
    it('should get correct sports path with getPathArray', () => {
      const pathMock = 'sport/football';

      spyOn(service as any, 'sliceArrayToFoundElement').and.callThrough();
      service['location'].path = jasmine.createSpy('path').and.returnValue(pathMock);

      service['config'].isGreyhoundPage = false;
      service['config'].sportName = 'football';

      const result = service['getPathArray']('matches');
      expect(result).toEqual(['football', 'matches']);
    });
  });

  describe('#initializeBreadcrumbsList', () => {
    it('should split breadcrumb element name', () => {
      service['breadcrumbsTitles'] = { 'football': 'Football', 'coupons?utm=test&something=123': 'coupons?utm=test&something=123'};
      const breadcrumbArr = ['football', 'coupons?utm=test&something=123'];
      const res =  service['initializeBreadcrumbsList'](breadcrumbArr);

      expect(res).toEqual([
        {name: 'Home', targetUri: '/'},
        {targetUri: '/sport/football', name: 'Football'},
        {targetUri: '/sport/football/coupons?utm=test&something=123', name: 'coupons'}
      ]);
    });
    it('should set breadcrumb elements with defaultTab as matches', () => {
      service['breadcrumbsTitles'] = { 'football': 'Football', 'matches': 'Matches'};
      const breadcrumbArr = ['football', 'matches'];
      const res =  service['initializeBreadcrumbsList'](breadcrumbArr, 'matches');

      expect(res).toEqual([
        {name: 'Home', targetUri: '/'},
        {targetUri: '/sport/football/matches', name: 'Football'},
        {targetUri: '/sport/football/matches', name: 'Matches'}
      ]);
    });
    it('should set breadcrumb elements with sport as football and defaultTab as matches', () => {
      service['config'].sportName = 'football';
      service['breadcrumbsTitles'] = { 'football': 'Football', 'matches': 'Matches'};
      const breadcrumbArr = ['football', 'matches'];
      const res =  service['initializeBreadcrumbsList'](breadcrumbArr, 'matches');

      expect(res).toEqual([
        {name: 'Home', targetUri: '/'},
        {targetUri: '/sport/football/matches', name: 'Football'},
        {targetUri: '/sport/football/matches', name: 'Matches'}
      ]);
    });
    it('should set breadcrumb elements with sport as horseracing and defaultTab as featured', () => {
      service['config'].sportName = 'horseracing';
      service['config'].isHorseRacingPage = true;
      service['breadcrumbsTitles'] = { 'horseracing': 'Horse racing', 'featured': 'featured'};
      const breadcrumbArr = ['horseracing', 'featured'];
      const res =  service['initializeBreadcrumbsList'](breadcrumbArr, 'matches');

      expect(res).toEqual([
        {name: 'Home', targetUri: '/'},
        {targetUri: '/horse-racing/featured', name: 'Horse racing'},
        {targetUri: '/horseracing/featured', name: 'featured'}
      ]);
    });
    it('should set breadcrumb elements with sport as olympics and defaultTab as matches', () => {
      service['config'].sportName = 'olympics';
      service['config'].isOlympicsPage = true;
      service['breadcrumbsTitles'] = { 'olympics': 'Olympics', 'matches': 'Matches'};
      const breadcrumbArr = ['olympics', 'matches'];
      const res =  service['initializeBreadcrumbsList'](breadcrumbArr, 'matches');

      expect(res).toEqual([
        {name: 'Home', targetUri: '/'},
        {targetUri: '/olympics/matches', name: 'Olympics'},
        {targetUri: '/olympics/matches', name: 'Matches'}
      ]);
    });
  });

  describe('#getLocalizedString', () => {
    it('return breadcrumbItemName thwn module is default', () => {
      const result = service['getLocalizedString']('default', 'breadcrumbItemName');

      expect(result).toEqual('breadcrumbItemName');
    });

    it('return breadcrumbItemName when module is default and replace it', () => {
      const result = service['getLocalizedString']('default', 'bredcr- \n qw');

      expect(result).toEqual('bredcr   qw');
    });

    it('return breadcrumbItemName itemTranslation === \'KEY_NOT_FOUND\'', () => {
      locale.getString.and.returnValue('KEY_NOT_FOUND');

      const result = service['getLocalizedString']('not_default', 'bredcr- \n qw');

      expect(result).toEqual('bredcr   qw');
    });

    it('return breadcrumbItemName itemTranslation === \'KEY_FOUND\'', () => {
      locale.getString.and.returnValue('KEY_FOUND');

      const result = service['getLocalizedString']('not_default', 'bredcr- \n qw');

      expect(result).toEqual('KEY_FOUND');
    });
  });
  describe('#getBreadcrumbsList', () => {
    it('horseracing breadcrumbs', () => {
      const config = {
        sportName: 'horseracing',
        display: null
      } as any;
      service['getPathArray'] = jasmine.createSpy().and.returnValue([]);
      service['initializeBreadcrumbsList'] = jasmine.createSpy();
      service.getBreadcrumbsList(config);
      expect(service['initializeBreadcrumbsList']).toHaveBeenCalledWith([], undefined);
    });
    it('greyhound breadcrumbs', () => {
      const config = {
        sportName: 'greyhound',
        display: null
      } as any;
      service['getPathArray'] = jasmine.createSpy().and.returnValue([]);
      service['initializeBreadcrumbsList'] = jasmine.createSpy();
      service.getBreadcrumbsList(config, 'races');
      expect(service['getPathArray']).toHaveBeenCalled();
      expect(service['initializeBreadcrumbsList']).toHaveBeenCalledWith(['races'], 'races');
    });
    it('football breadcrumbs', () => {
      const config = {
        sportName: 'football',
        display: null
      } as any;
      service['getPathArray'] = jasmine.createSpy().and.returnValue([]);
      service['initializeBreadcrumbsList'] = jasmine.createSpy();
      service.getBreadcrumbsList(config, 'matches');
      expect(service['getPathArray']).toHaveBeenCalled();
      expect(service['initializeBreadcrumbsList']).toHaveBeenCalledWith(['matches'], 'matches');
    });
  });
});
