import { of } from 'rxjs';

import { SportBannersListComponent } from './banners.list.component';

describe('SportBannersListComponent', () => {
  let component: SportBannersListComponent;
  let router;
  let matSnackBar;
  let dialogService;
  let matDialog;
  let bannersApiService;
  let globalLoaderService;

  beforeEach(() => {
    matSnackBar = {};
    dialogService = {};
    matDialog = {};
    bannersApiService = {
      getSportCategories: jasmine.createSpy('getSportCategories').and.returnValue(of({})),
      getBannersData: jasmine.createSpy('getBannersData').and.returnValue(of({})),
    };
    router = {
      navigate: jasmine.createSpy('navigate').and.returnValue(Promise.resolve())
    };
    globalLoaderService = {};

    component = new SportBannersListComponent(
      matSnackBar,
      dialogService,
      matDialog,
      bannersApiService,
      router,
      globalLoaderService);
  });

  describe('ngOnInit', () => {
    it('should call getSportCategories', () => {
      component.ngOnInit();

      expect(bannersApiService.getSportCategories).toHaveBeenCalled();
    });
  });
});
