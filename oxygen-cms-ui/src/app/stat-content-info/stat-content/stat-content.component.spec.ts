import { StatContentComponent } from './stat-content.component';
import { of as observableOf, of } from 'rxjs/observable/of';
import { Breadcrumb } from '@app/client/private/models/breadcrumb.model';
import { Params } from '@angular/router';
import { Location } from '@angular/common';

describe('StatContentComponent', () => {
  let component: StatContentComponent;
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
      path: jasmine.createSpy().and.returnValue('/stat-content-info')
    } as any;

    sportsModulesBreadcrumbsService = {
      getBreadcrubs: jasmine.createSpy('getBreadcrubs').and.returnValue(observableOf([{label: '2'} as any]))
    };

    apiClientService = {
      eventHub: jasmine.createSpy('eventHub').and.returnValue({
        getEventHubById: jasmine.createSpy('getEventHubById').and.returnValue(observableOf({indexNumber: '3'} as any))
      } as any),
      statiContentInfo: jasmine.createSpy('statiContentInfo').and.returnValue({
        getById: jasmine.createSpy('getById').and.returnValue(of({ body: {} }))
      })
    };
    errorService = {
      emitError: jasmine.createSpy('emitError')
    };

    component = new StatContentComponent(
      activatedRoute,
      router,
      apiClientService,
      globalLoaderService,
      dialogService,
      brandService,
      sportsModulesBreadcrumbsService,
    );
  });

  describe('#loadInitialData', () => {
    it('pageType == add', () => {
      component.pageType = 'add';

      component['loadInitialData']();

      const resBreadcrumbs = [{
        label: `Statistical Content Information`,
        url: `/stat-content-info`
      }, {
        label: 'create',
        url: '/stat-content-info/add'
      }];
      expect(component.breadcrumbsData).toEqual(resBreadcrumbs);
      expect(component.statContentInfo).toBeTruthy();
    });

    it('pageType == add & hubId not null', () => {
      activatedRoute.params = observableOf({ pageType: 'add', hubId: '1' } as Params);
      component.pageType = 'add';

      component['loadInitialData']();

      expect(component.breadcrumbsData).toEqual([{label: '2'} as any]);
      expect(apiClientService.eventHub).toHaveBeenCalled();
      expect(apiClientService.eventHub().getEventHubById).toHaveBeenCalledWith('1');
      expect(component.statContentInfo).toBeTruthy();
    });
  });

  describe('#initBreadcrumbs', () => {
    it('hubId not null & pageType == edit', () => {
      component.pageType = 'edit';
      component.statContentInfo = {
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
      component.statContentInfo = {
        id: '1',
        title: 'some'
      } as any;

      component['initBreadcrumbs']({});

      const resBreadcrumbs = [{
        label: `Statistical Content Information`,
        url: `/stat-content-info`
      }, {
        label: 'some',
        url: '/stat-content-info/edit/1'
      }];
      expect(component.breadcrumbsData).toEqual(resBreadcrumbs);
    });

    it('pageType == add', () => {
      component.pageType = 'add';

      component['initBreadcrumbs']({});

      const resBreadcrumbs = [{
        label: `Statistical Content Information`,
        url: `/stat-content-info`
      }, {
        label: 'create',
        url: '/stat-content-info/add'
      }];
      expect(component.breadcrumbsData).toEqual(resBreadcrumbs);
    });
  });

});
