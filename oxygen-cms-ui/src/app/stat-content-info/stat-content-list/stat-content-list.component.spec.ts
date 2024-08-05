import { fakeAsync, tick } from '@angular/core/testing';
import { CSPSegmentLSConstants } from '@app/app.constants';

import { Observable, of } from 'rxjs';
import { StatContentListComponent } from './stat-content-list.component';
import { Location } from '@angular/common';

describe('StatContentListComponent', () => {
  let component: StatContentListComponent;
  let apiClientService;
  let globalLoaderService;
  let dialogService;
  let router;
  let activatedRoute;
  let eventHubService;
  let statContentInfoService;
  let snackBar;
  let segmentStoreService;
  let location: Location;
  let path = 'stat-content-info';

  beforeEach(() => {
    apiClientService = {
      eventHub: () => eventHubService,
      statContentInfo: () => statContentInfoService
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
    statContentInfoService = {
      findAllByEventHubIndex: jasmine.createSpy('findAllByEventHubIndex').and.returnValue(of({ body: [] })),
      reorder: jasmine.createSpy('reorder').and.returnValue(of({ body: [] })),
      remove: jasmine.createSpy('remove').and.returnValue(of({ body: [] })),
      findAllByBrandAndSegment : jasmine.createSpy('findAllByBrandAndSegment').and.returnValue(of({ body: [] }))
    };
    
    segmentStoreService = {
      validateSegmentValue: jasmine.createSpy('validateSegmentValue'),
      validateHomeModule: () => path.includes('stat-content-info'),
      getSegmentMessage: () => Observable.of({segmentValue:'Universal', segmentModule:CSPSegmentLSConstants.FEATURED_TAB_MODULE }),
      updateSegmentMessage: jasmine.createSpy('updateSegmentMessage')
    };
    
    snackBar = {
      open: jasmine.createSpy('open')
    };
    
    location = {
      path: jasmine.createSpy().and.returnValue('/stat-content-info')
    } as any;

    component = new StatContentListComponent(
      apiClientService,
      dialogService,
      router,
      apiClientService,
    );
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(eventHubService.getEventHubById).toHaveBeenCalled();
    expect(statContentInfoService.findAllByEventHubIndex).toHaveBeenCalled();
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


  
  it('should remove data', () => {
    let staticalContentIds = ['1', '2'];
    component.removeHandlerMulty(staticalContentIds);
    expect(dialogService.showConfirmDialog).toHaveBeenCalledWith(
      {
        title: `Remove Statistical Content Information (${staticalContentIds.length})`,
        message: `Are You Sure You Want to Remove Statistical Content Information?`,
        yesCallback: jasmine.any(Function)
      });
    expect(statContentInfoService.remove).toHaveBeenCalledWith(staticalContentIds[0]);
    expect(statContentInfoService.remove).toHaveBeenCalledWith(staticalContentIds[1]);
  });

});
