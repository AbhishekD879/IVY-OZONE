import { FeaturedModuleComponent } from './featured-module.component';
import { of as observableOf, of } from 'rxjs/observable/of';
import { Breadcrumb } from '@app/client/private/models/breadcrumb.model';
import { Params } from '@angular/router';
import { Location } from '@angular/common';

describe('FeaturedModuleComponent', () => {
  let component: FeaturedModuleComponent;
   let snackBar, activatedRoute, router, apiClientService, globalLoaderService, dialogService, brandService,
     errorService, segmentStoreService,
   sportsModulesBreadcrumbsService: any;
  let location: Location;

  beforeEach(() => {
    snackBar = router = dialogService = {};
    activatedRoute = {
      params: observableOf({ pageType: 'add' } as Params)
    };

    brandService = {
      brandsList: [{ brandCode: 'sb' }],
      brand: 'sb'
    };

    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };
    
    segmentStoreService = {
      setSegmentValue: jasmine.createSpy('setSegmentValue')
    };
    
    location = {
      path: jasmine.createSpy().and.returnValue('/featured-modules')
    } as any;

    sportsModulesBreadcrumbsService = {
      getBreadcrubs: jasmine.createSpy('getBreadcrubs').and.returnValue(observableOf([{label: '2'} as any]))
    };

    apiClientService = {
      eventHub: jasmine.createSpy('eventHub').and.returnValue({
        getEventHubById: jasmine.createSpy('getEventHubById').and.returnValue(observableOf({indexNumber: '3'} as any))
      } as any),
      featuredTabModules: jasmine.createSpy('featuredTabModules').and.returnValue({
        getById: jasmine.createSpy('getById').and.returnValue(of({ body: {} }))
      })
    };
    errorService = {
      emitError: jasmine.createSpy('emitError')
    };

    component = new FeaturedModuleComponent(
      snackBar,
      activatedRoute,
      router,
      apiClientService,
      globalLoaderService,
      dialogService,
      brandService,
      sportsModulesBreadcrumbsService,
      errorService,
      segmentStoreService,
      location
    );
  });

  describe('#loadInitialData', () => {
    it('pageType == add', () => {
      component.pageType = 'add';

      component['loadInitialData']();

      const resBreadcrumbs = [{
        label: `Featured Tab Modules`,
        url: `/featured-modules`
      }, {
        label: 'create',
        url: '/featured-modules/add'
      }];
      expect(component.breadcrumbsData).toEqual(resBreadcrumbs);
      expect(component.featuredTabModule).toBeTruthy();
      expect(component.featuredTabModule.publishedDevices['sb']).toEqual({desktop: true, tablet: true, mobile: true});
    });

    it('pageType == add & hubId not null', () => {
      activatedRoute.params = observableOf({ pageType: 'add', hubId: '1' } as Params);
      component.pageType = 'add';

      component['loadInitialData']();

      expect(component.breadcrumbsData).toEqual([{label: '2'} as any]);
      expect(apiClientService.eventHub).toHaveBeenCalled();
      expect(apiClientService.eventHub().getEventHubById).toHaveBeenCalledWith('1');
      expect(component.featuredTabModule).toBeTruthy();
      expect(component.featuredTabModule.publishedDevices['sb']).toEqual({desktop: true, tablet: true, mobile: true});
    });
  });

  describe('#initBreadcrumbs', () => {
    it('hubId not null & pageType == edit', () => {
      component.pageType = 'edit';
      component.featuredTabModule = {
        title: 'some'
      } as any;
      component.hubId = '1';

      component['initBreadcrumbs']({});

      const argBreadcrumbs = {
        customBreadcrumbs: [{ label: 'some' }]
      } as any;
      expect(sportsModulesBreadcrumbsService.getBreadcrubs).toHaveBeenCalledWith({}, argBreadcrumbs);
      expect(component.breadcrumbsData).toEqual([{label: '2'} as Breadcrumb]);
    });

    it('hubId not null & pageType == add', () => {
      component.pageType = 'add';
      component.hubId = '1';
      component['initBreadcrumbs']({});

      const argBreadcrumbs = {
        customBreadcrumbs: [{ label: 'create' }]
      } as any;
      expect(sportsModulesBreadcrumbsService.getBreadcrubs).toHaveBeenCalledWith({}, argBreadcrumbs);
      expect(component.breadcrumbsData).toEqual([{label: '2'} as Breadcrumb]);
    });

    it('pageType == edit', () => {
      component.pageType = 'edit';
      component.featuredTabModule = {
        id: '1',
        title: 'some'
      } as any;

      component['initBreadcrumbs']({});

      const resBreadcrumbs = [{
        label: `Featured Tab Modules`,
        url: `/featured-modules`
      }, {
        label: 'some',
        url: '/featured-modules/edit/1'
      }];
      expect(component.breadcrumbsData).toEqual(resBreadcrumbs);
    });

    it('pageType == add', () => {
      component.pageType = 'add';

      component['initBreadcrumbs']({});

      const resBreadcrumbs = [{
        label: `Featured Tab Modules`,
        url: `/featured-modules`
      }, {
        label: 'create',
        url: '/featured-modules/add'
      }];
      expect(component.breadcrumbsData).toEqual(resBreadcrumbs);
    });
  });

  describe('#form validator and emitted data handler', () => {
    it('should handle form valid and check validation to true', () => {
      component.isSegmentValid = true;
      expect(component.isValidModel()).toBeFalsy();
    });

    it('check validation to true', () => {
      component.isSegmentValid = false;
      expect(component.isValidModel()).toBeFalsy();
    });

    it('should check if segment is valid', () => {
      let flag = true;
      component.isSegmentFormValid(flag);
      expect(component.isSegmentValid).toBeTrue();
    });

    it('should check if segment is valid', () => {
      let flag = false;
      component.isSegmentFormValid(flag);
      expect(component.isSegmentValid).toBeFalse();

    });
  });

  describe('#revert', () => {
    it('should revert the data for edit Featured Tab', () => {
      activatedRoute.params = observableOf({ pageType: 'edit', id: '1' } as Params);
      component.pageType = 'edit';

      component.revertChanges();
      expect(apiClientService.featuredTabModules().getById).toHaveBeenCalled();
    });

    it('should revert the data for new Featured Tab and hubId is not null', () => {
      activatedRoute.params = observableOf({ pageType: 'add', hubId: '1' } as Params);
      component.pageType = 'add';

      component.revertChanges();
      component.hubId = '1';
      expect(component.hubId).toBe('1');
      expect(component.featuredTabModule).toBeDefined();
      expect(apiClientService.eventHub().getEventHubById).toHaveBeenCalledWith(component.hubId);
    });
    
    it('should revert the data for new Featured Tab and hubId is null', () => {
      component.revertChanges();
      expect(component.featuredTabModule).toBeDefined();
      expect(apiClientService.featuredTabModules().getById).not.toHaveBeenCalled();
      expect(apiClientService.eventHub().getEventHubById).not.toHaveBeenCalled();
    });
  });
});
