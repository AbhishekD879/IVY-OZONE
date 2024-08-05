import { fakeAsync, tick } from '@angular/core/testing';
import { AppConstants, CSPSegmentLSConstants } from '@app/app.constants';
import { Order } from '@app/client/private/models/order.model';
import { Observable, of } from 'rxjs';
import { FeaturedModulesListComponent } from './featured-modules-list.component';
import { Location } from '@angular/common';

describe('FeaturedModulesListComponent', () => {
  let component: FeaturedModulesListComponent;
  let apiClientService;
  let globalLoaderService;
  let dialogService;
  let router;
  let activatedRoute;
  let eventHubService;
  let featuredTabModulesService;
  let snackBar;
  let segmentStoreService;
  let location: Location;
  let path = 'featured-modules';

  beforeEach(() => {
    apiClientService = {
      eventHub: () => eventHubService,
      featuredTabModules: () => featuredTabModulesService
    };
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };
    dialogService = {
      showConfirmDialog: jasmine.createSpy('showConfirmDialog').and
        .callFake(({ title, message, yesCallback }) => yesCallback())
    };
    router = {};
    activatedRoute = {
      params: of({ hubId: '1' })
    };
    eventHubService = {
      getEventHubById: jasmine.createSpy('getEventHubById').and.returnValue(of({}))
    };
    featuredTabModulesService = {
      findAllByEventHubIndex: jasmine.createSpy('findAllByEventHubIndex').and.returnValue(of({ body: [] })),
      reorder: jasmine.createSpy('reorder').and.returnValue(of({ body: [] })),
      remove: jasmine.createSpy('remove').and.returnValue(of({ body: [] })),
      findAllByBrandAndSegment : jasmine.createSpy('findAllByBrandAndSegment').and.returnValue(of({ body: [] }))
    };
    
    segmentStoreService = {
      validateSegmentValue: jasmine.createSpy('validateSegmentValue'),
      validateHomeModule: () => path.includes('featured-modules'),
      getSegmentMessage: () => Observable.of({segmentValue:'Universal', segmentModule:CSPSegmentLSConstants.FEATURED_TAB_MODULE }),
      updateSegmentMessage: jasmine.createSpy('updateSegmentMessage')
    };
    
    snackBar = {
      open: jasmine.createSpy('open')
    };
    
    location = {
      path: jasmine.createSpy().and.returnValue('/featured-modules')
    } as any;

    component = new FeaturedModulesListComponent(
      apiClientService,
      globalLoaderService,
      dialogService,
      router,
      activatedRoute,
      snackBar,
      segmentStoreService,
      location
    );
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(component.hubId).toBe('1');
    expect(eventHubService.getEventHubById).toHaveBeenCalled();
    expect(featuredTabModulesService.findAllByEventHubIndex).toHaveBeenCalled();
  });
  
  it('should success showLoader', () => {
    component.ngOnInit();
    expect(segmentStoreService.validateSegmentValue).toHaveBeenCalled();
    expect(globalLoaderService.showLoader).toHaveBeenCalled();
  });

  it('should validate segment value', fakeAsync(() => {
    segmentStoreService.validateSegmentValue = jasmine.createSpy('validateSegmentValue');
    component.ngOnInit();
    tick();

    expect(globalLoaderService.showLoader).toHaveBeenCalled();
    expect(segmentStoreService.validateSegmentValue).toHaveBeenCalled();
  }));

  it('#reorderHandler should save new order', () => {
    const newOrder: Order = { order: ['123', '456'], id: '123' };
    component.reorderHandler(newOrder);
    expect(apiClientService.featuredTabModules().reorder).toHaveBeenCalledWith(newOrder);
    expect(snackBar.open).toHaveBeenCalledWith(
      `Featured Tab order saved!`,
      'Ok!',
      {
        duration: AppConstants.HIDE_DURATION,
      }
    );
  });
  
  it('should remove data', () => {
    let featuredTabIds = ['1', '2'];
    component.removeHandlerMulty(featuredTabIds);
    expect(dialogService.showConfirmDialog).toHaveBeenCalledWith(
      {
        title: `Remove Feature Tab Modules (${featuredTabIds.length})`,
        message: `Are You Sure You Want to Remove Feature Tab Modules?`,
        yesCallback: jasmine.any(Function)
      });
    expect(featuredTabModulesService.remove).toHaveBeenCalledWith(featuredTabIds[0]);
    expect(featuredTabModulesService.remove).toHaveBeenCalledWith(featuredTabIds[1]);
    expect(component.modules.length).toBe(0);
  });

  it('should call segmentHandler method', () => {
    const segment = "Cricket";
    component.segmentHandler(segment);
    expect(component.segmentChanged).toBeTrue();
    expect(globalLoaderService.showLoader).toHaveBeenCalledTimes(1);
    expect(globalLoaderService.hideLoader).toHaveBeenCalledTimes(2);
  });
});
