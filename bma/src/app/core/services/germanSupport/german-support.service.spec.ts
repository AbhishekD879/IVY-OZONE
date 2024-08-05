import { GermanSupportService } from './german-support.service';
import { Observable, of as observableOf } from 'rxjs';
import { NavigationEnd, NavigationStart } from '@angular/router';

describe('GermanSupportService', () => {
  let service: GermanSupportService;
  let router;
  let localeService;
  let infoDialogService;
  let userService;
  let storageService;
  let menuItems;

  beforeEach(() => {
    menuItems = [{
      directiveName: 'NextRaces',
      sportName: 'racing'
    },
    {
      directiveName: 'NextRaces',
      sportName: 'sport'
    }];

    router = {
      url: '/horse-racing/featured',
      navigate: jasmine.createSpy('navigate'),
      events: jasmine.createSpy('events').and.returnValue(observableOf())
    };

    storageService = jasmine.createSpyObj('storageService', ['get']);
    userService = {
      countryCode: 'DE'
    };
    localeService = jasmine.createSpyObj('localeService', ['getString']);
    infoDialogService = jasmine.createSpyObj('infoDialogService', ['openInfoDialog']);

    service = new GermanSupportService(
      userService,
      storageService,
      router,
      localeService,
      infoDialogService
    );
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  it('#restrictedSportsCategoriesIds should contain racing categories IDs', () => {
    expect(service.restrictedSportsCategoriesIds).toEqual(['19', '21', '161']);
  });

  it('#isGermanUser from userService should be true', () => {
    // default user is 'DE'
    expect(service.isGermanUser()).toBeTruthy();
  });

  it('#isGermanUser from userService should be false', () => {
    userService.countryCode = 'GB';
    expect(service.isGermanUser()).toBeFalsy();
  });

  it('#isGermanUser from storageService should be false', () => {
    userService.countryCode = 'GB';
    storageService.get.and.returnValue('GB');
    expect(service.isGermanUser()).toBeFalsy();
  });

  it('#isGermanUser from storageService should be true', () => {
    userService.countryCode = 'GB';
    storageService.get.and.returnValue('DE');
    expect(service.isGermanUser()).toBeTruthy();
  });

  it('#filterNextRaces', () => {
    const result = service.filterNextRaces(menuItems);
    expect(result).toEqual([]);
  });

  it('#filterRestrictedSports', () => {
    const result = service.filterRestrictedSports(menuItems);
    expect(result).toEqual([{ directiveName: 'NextRaces', sportName: 'sport' }]);
  });

  it('#filterRestrictedSports without sportName prop', () => {
    const result = service.filterRestrictedSports([{isActive: false}]);
    expect(result).toEqual([]);
  });

  it('#toggleItemsList for user except German with filterNextRaces', () => {
    userService.countryCode = 'GB';
    const result = service.toggleItemsList(menuItems, 'filterNextRaces');
    expect(result).toEqual(menuItems);
  });

  it('#toggleItemsList for user except German with filterRestrictedSports', () => {
    userService.countryCode = 'GB';
    const result = service.toggleItemsList(menuItems, 'filterRestrictedSports');
    expect(result).toEqual(menuItems);
  });

  it('#toggleItemsList for German user with filterNextRaces', () => {
    storageService.get.and.returnValue('DE');
    const result = service.toggleItemsList(menuItems, 'filterNextRaces');
    expect(result).toEqual([]);
  });

  it('#toggleItemsList for German user with filterRestrictedSports', () => {
    storageService.get.and.returnValue('DE');
    const result = service.toggleItemsList(menuItems, 'filterRestrictedSports');
    expect(result).toEqual([{ directiveName: 'NextRaces', sportName: 'sport' }]);
  });

  it('#should not redirectToMainPage', () => {
    userService.countryCode = 'GB';
    service.redirectToMainPage();
    expect(router.navigate).not.toHaveBeenCalled();
  });

  it('#showDialog', () => {
    const message = 'message';
    service['showDialog'](message);
    expect(infoDialogService.openInfoDialog).toHaveBeenCalled();
  });

  it('#isRestrictedSport should return true', () => {
    storageService.get.and.returnValue('DE');
    const result = service['isRestrictedSport'](menuItems[0]);
    expect(result).toBeTruthy();
  });

  it('#isRestrictedSport should return false', () => {
    storageService.get.and.returnValue('GB');
    const result = service['isRestrictedSport'](menuItems);
    expect(result).toBeFalsy();
  });

  it('filterEnhancedCategories', () => {
    const categopries: any[] = [{ id: '1' }, { id: '19' }];
    expect(service.filterEnhancedCategories(categopries).length).toBe(1);
  });

  it('filterEnhancedOutcomes', () => {
    const events: any[] = [
      { categoryId: '21' },
      { categoryId: '1' }
    ];
    expect(service.filterEnhancedOutcomes(events).length).toBe(1);
  });

  describe('@redirectToMainPageOnLogin', () => {
    let updateObserver;
    beforeEach(() => {
      // @ts-ignore
      service['router'].events = Observable.create(o => updateObserver = o);
    });

    it('shoudl redirect to main page', () => {
      service['redirectToMainPageOnLogin']();
      updateObserver.next(new NavigationEnd(0, '/horse-racing/featured', '/horse-racing/featured'));
      expect(router.navigate).toHaveBeenCalledTimes(1);
    });

    it('shoudl NOT redirect to main page when instance of router is not NavigationEnd', () => {
      service['redirectToMainPageOnLogin']();
      updateObserver.next(new NavigationStart(0, '/horse-racing/featured', 'imperative'));
      expect(router.navigate).not.toHaveBeenCalled();
    });

    it('shoudl NOT redirect to main page when firs event is NOT as route as was on redirection start', () => {
      service['redirectToMainPageOnLogin']();
      updateObserver.next(new NavigationEnd(0, '/', '/'));
      updateObserver.next(new NavigationEnd(0, '/horse-racing/featured', '/horse-racing/featured'));
      expect(router.navigate).not.toHaveBeenCalled();
    });

    it('shoudl NOT redirect to main page when route url is not the same as route that was on redirection start', () => {
      service['redirectToMainPageOnLogin']();
      updateObserver.next(new NavigationEnd(0, '/', '/horse-racing/featured'));
      expect(router.navigate).not.toHaveBeenCalled();
    });

    it('shoudl NOT redirect to main page when route urlAfterRedirects is not the same as route that was on redirection start', () => {
      service['redirectToMainPageOnLogin']();
      updateObserver.next(new NavigationEnd(0, '/horse-racing/featured', '/'));
      expect(router.navigate).not.toHaveBeenCalled();
    });

  });
});
