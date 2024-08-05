import { of } from 'rxjs';

import { TemplateEditComponent } from './template-edit.component';

describe('TemplateEditComponent', () => {
  let component: TemplateEditComponent;
  let router;
  let activatedRoute;
  let templateApiService;
  let dialogService;
  let globalLoaderService;
  let imageLoaderService;
  let snackBar;
  let brandService;

  beforeEach(() => {
    router = {};
    activatedRoute = {
      params: of({})
    };
    templateApiService = {
      getTemplate: jasmine.createSpy('getTemplate').and.returnValue(of({ body: {} }))
    };
    dialogService = {};
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };
    imageLoaderService = {
      getDataForBrandAndSprite: jasmine.createSpy('getDataForBrandAndSprite').and.returnValue(of({}))
    };
    snackBar = {};
    brandService = { brand: 'bma' };

    component = new TemplateEditComponent(
      router, activatedRoute, templateApiService, dialogService, globalLoaderService,
      imageLoaderService, snackBar, brandService
    );
  });

  describe('ngOnInit', () => {
    it('ngOnInit', () => {
      component.ngOnInit();
      expect(component.isBrandLads).toBeFalsy();
      expect(component.showLeftSideLineTextName).toEqual('Show Left Side Blue Line');
      expect(globalLoaderService.showLoader).toHaveBeenCalled();
      expect(templateApiService.getTemplate).toHaveBeenCalled();
    });
  });

  describe('ngOnInit should be the brand ladbrokes', () => {
    beforeEach(() => {
      brandService = { brand: 'ladbrokes' };

      component = new TemplateEditComponent(
        router, activatedRoute, templateApiService, dialogService, globalLoaderService,
        imageLoaderService, snackBar, brandService
      );
    });

    it('ngOnInit ladbrokes brand', () => {
      component.ngOnInit();
      expect(component.isBrandLads).toBeTruthy();
      expect(component.showLeftSideLineTextName).toEqual('Show Left Side Red Line');
      expect(globalLoaderService.showLoader).toHaveBeenCalled();
      expect(templateApiService.getTemplate).toHaveBeenCalled();
    });
  });
});
