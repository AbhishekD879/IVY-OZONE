import { fakeAsync, tick } from '@angular/core/testing';
import { DesktopFavouritesMatchesComponent } from './favourites-matches.component';
import { of as observableOf } from 'rxjs';

describe('DesktopFavouritesMatchesComponent', () => {
  let component: DesktopFavouritesMatchesComponent;
  let favouritesService;
  let userService;
  let pubSubService;
  let favouritesMatchesService;
  let filtersService;

  beforeEach(() => {
    favouritesService = {
      getFavoritesText: jasmine.createSpy('getFavoritesText').and.returnValue(observableOf({})),
    };
    userService = {};
    pubSubService = {};
    favouritesMatchesService = {};
    filtersService = {
      orderBy: jasmine.createSpy('filtersService.orderBy')
    };

    component = new DesktopFavouritesMatchesComponent(
      favouritesService,
      userService,
      pubSubService,
      favouritesMatchesService,
      filtersService
    );
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('should init',  fakeAsync(() => {
    component.getFavourites = jasmine.createSpy('getFavourites').and.returnValue([{}, {}]);

    component.init().subscribe();
    tick();

    expect(component.getFavourites).toHaveBeenCalled();
    expect(component.filteredMatches).toEqual([{}, {}] as any);
  }));

  it('should orderMatches',  () => {
    component.getFavourites = jasmine.createSpy('getFavourites').and.returnValue([{}, {}]);
    component.orderMatches();

    expect(component.filteredMatches).toEqual([{}, {}] as any);
  });

  describe('getFavourites', () => {
    it('should return all favourites', () => {
      component.matches = [
        {startTime: '4.01.2020'},
        {startTime: '2.01.2020'},
        {startTime: '1.01.2020'},
        {startTime: '3.01.2020'}
        ];
      component.isShowAll = true;
      const actualResult = component.getFavourites();

      expect(actualResult).toEqual([
        {startTime: '1.01.2020'},
        {startTime: '2.01.2020'},
        {startTime: '3.01.2020'},
        {startTime: '4.01.2020'}] as any);
    });

    it('should return first favourite', () => {
      component.matches = [
        {startTime: '4.01.2020'},
        {startTime: '2.01.2020'},
        {startTime: '1.01.2020'},
        {startTime: '3.01.2020'}
        ];
      component.isShowAll = false;
      const actualResult = component.getFavourites();

      expect(actualResult).toEqual([
        {startTime: '1.01.2020'},
        {startTime: '2.01.2020'},
        {startTime: '3.01.2020'}] as any);
    });
  });

  it('should toggleShowAllButton', () => {
    component.getFavourites = jasmine.createSpy('getFavourites').and.returnValue([{}, {}]);
    component.isShowAll = true;

    component.toggleShowAllButton();

    expect(component.isShowAll).toBeFalsy();
    expect(component.filteredMatches).toEqual([{}, {}] as any);
    expect(component.getFavourites).toHaveBeenCalled();
  });

  describe('isShowAllButtonShown', () => {
    it('should be true if user is logged in',  () => {
      component.isFavourite = jasmine.createSpy('isFavourite').and.returnValue(true);
      component.isUserLoggedIn = true;
      component.matches = [{}, {}, {}, {}];

      const actualResult = component.isShowAllButtonShown;

      expect(actualResult).toBeTruthy();
    });

    it('should be true if user is not logged in',  () => {
      component.isFavourite = jasmine.createSpy('isFavourite').and.returnValue(false);
      component.isUserLoggedIn = false;
      component.matches = [{}, {}];

      const actualResult = component.isShowAllButtonShown;

      expect(actualResult).toBeFalsy();
    });
  });

  describe('isNoMatchesTextShown', () => {
    it('should be true if user is logged in',  () => {
      component.isFavourite = jasmine.createSpy('isFavourite').and.returnValue(false);
      component.isUserLoggedIn = true;
      component.state.loading = false;

      const actualResult = component.isNoMatchesTextShown;

      expect(actualResult).toBeTruthy();
    });

    it('should be true if user is not logged in',  () => {
      component.isFavourite = jasmine.createSpy('isFavourite').and.returnValue(true);
      component.isUserLoggedIn = false;
      component.state.loading = true;

      const actualResult = component.isNoMatchesTextShown;

      expect(actualResult).toBeFalsy();
    });
  });

});
