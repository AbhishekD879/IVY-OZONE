import { ComponentFixture, fakeAsync, TestBed, tick } from '@angular/core/testing';
import { CUSTOM_ELEMENTS_SCHEMA, NO_ERRORS_SCHEMA  } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import * as _ from 'lodash';

import { ApiClientService } from '@app/client/private/services/http';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { BrandService } from '@app/client/private/services/brand.service';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { ErrorService } from '@app/client/private/services/error.service';
import {
  SportsHighlightCarouselListComponent
} from '@app/sports-modules/highlight-carousels-module/highlight-carousels/highlight-carousel-list/highlight-carousel-list.component';
import { SportsHighlightCarousel } from '@app/client/private/models/sportsHighlightCarousel.model';
import { Order } from '@app/client/private/models/order.model';
import { AppConstants, CSPSegmentLSConstants } from '@app/app.constants';
import { ActivatedRoute, Router } from '@angular/router';
import {
  SportsHighlightCarouselsService
} from '@app/sports-modules/highlight-carousels-module/highlight-carousels/highlight-carousels.service';
import { Observable, of } from 'rxjs';
import { SegmentStoreService } from '@app/client/private/services/segment-store.service';

describe('SportsHighlightCarouselListComponent', () => {
  let component: SportsHighlightCarouselListComponent,
    fixture: ComponentFixture<SportsHighlightCarouselListComponent>;

  let apiClientService;
  let dialogService: Partial<DialogService>;
  let globalLoaderService: Partial<GlobalLoaderService>;
  let errorService: Partial<ErrorService>;
  let snackBar: Partial<MatSnackBar>;
  let brandService: Partial<BrandService>;
  let HighlightCarouselListMock;
  let segmentsMock;
  let segmentStoreService;
  let router, activatedRoute;

  const carouselList: SportsHighlightCarousel[] = [
    {
      id: '5c0553a2c9e77c00011887b3'
    },
    {
      id: '5c067244c9e77c00013baf0e'
    },
    {
      id: '5c079612c9e77c0001188ae3'
    }
  ] as any;

  beforeEach(fakeAsync(() => {
    HighlightCarouselListMock = [
      {
        "id": "60f959ae3fd85f2be7bfbb06",
        "segments": ["Cricket"],
        "segmentsExcl": ["Rugby"]
      }
    ];

    segmentsMock = [
      { "id": 101, "name": "Universal" },
      { "id": 201, "name": "Cricket" }
    ];

    apiClientService = {
      sportsHighlightCarousel: jasmine.createSpy('sportsHighlightCarousel').and.returnValue({
        findAllByBrandAndSport: jasmine.createSpy('findAllByBrandAndSport').and.returnValue(of({ body: carouselList })),
        delete: jasmine.createSpy('delete').and.returnValue(of({ body: {} })),
        reorder: jasmine.createSpy('reorder').and.returnValue(of({ body: {} })),
        getHighlightCarouselBySegment : jasmine.createSpy('getHighlightCarouselBySegment').and.returnValue(of({body : HighlightCarouselListMock})),
        getSegments: jasmine.createSpy('getSegments').and.returnValue(of(segmentsMock))
      })
    };
    dialogService = {
      showConfirmDialog: jasmine.createSpy('showConfirmDialog')
        .and.returnValue(Observable.of({}))
        .and.callFake(({ title, message, yesCallback }) => {
          yesCallback();
        })
    };
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };
    errorService = {
      emitError: jasmine.createSpy('emitError')
    };
    snackBar = {
      open: jasmine.createSpy('open')
    };
    brandService = {
      brand: 'bma'
    };
    
    activatedRoute = {
      params: of({ hubId: "1"}),
      snapshot:{
      paramMap: {
        get: jasmine.createSpy('get') }}
    };

    const sportsHighlightCarouselsService = {
      getHubIndex: jasmine.createSpy('getHubIndex').and.returnValue(Observable.of(0))
    };
    
    segmentStoreService = {
      validateSegmentValue: jasmine.createSpy('validateSegmentValue'),
      validateHomeModule: jasmine.createSpy('validateHomeModule').and.returnValue(of('homepage')),
      getSegmentMessage: () => Observable.of({segmentValue:'Universal', segmentModule:CSPSegmentLSConstants.HIGHLIGHT_CAROUSEL }),
      updateSegmentMessage: jasmine.createSpy('updateSegmentMessage')
    };

    TestBed.configureTestingModule({
      declarations: [SportsHighlightCarouselListComponent],
      providers: [
        { provide: ApiClientService, useValue: apiClientService },
        { provide: DialogService, useValue: dialogService },
        { provide: GlobalLoaderService, useValue: globalLoaderService },
        { provide: ErrorService, useValue: errorService },
        { provide: MatSnackBar, useValue: snackBar },
        { provide: BrandService, useValue: brandService },
        { provide: ActivatedRoute, useValue: activatedRoute },
        { provide: SportsHighlightCarouselsService, useValue: sportsHighlightCarouselsService },
        {provide: SegmentStoreService,useValue: segmentStoreService},
        {provide:Router,useValue: router}
      ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA, NO_ERRORS_SCHEMA ]
    }).compileComponents();

    fixture = TestBed.createComponent(SportsHighlightCarouselListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
    tick();
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('#ngOnInit should get carousel list', fakeAsync(() => {
    component.ngOnInit();
    tick();
    expect(apiClientService.sportsHighlightCarousel().findAllByBrandAndSport).toHaveBeenCalledWith('bma', 0, 'eventhub');
    expect(component.highlightCarousels).toEqual(carouselList);
  }));

  it('#ngOnInit should handle request error', fakeAsync(() => {
    apiClientService.sportsHighlightCarousel().findAllByBrandAndSport.and.returnValue(Observable.throw('error'));
    component.ngOnInit();
    tick();
    expect(component.error).toEqual('error');
  }));

  it('ngOnInit when module is segmented', fakeAsync(() => {
    activatedRoute.params.subscribe((params) => {
      params['hubId'] = null;
      component.ngOnInit();
      tick();
      expect(globalLoaderService.showLoader).toHaveBeenCalled();
      expect(apiClientService.sportsHighlightCarousel().getHighlightCarouselBySegment).toHaveBeenCalled();
      expect(globalLoaderService.hideLoader).toHaveBeenCalled();
      expect(segmentStoreService.validateSegmentValue).toHaveBeenCalled();
    });
  }));

  it('removeHandler should remove carousel', () => {
    component.highlightCarousels = _.cloneDeep(carouselList);
    component.removeHandler(component.highlightCarousels[1]);

    expect(dialogService.showConfirmDialog).toHaveBeenCalledWith({
      title: 'Highlights Carousel',
      message: 'Are You Sure You Want to Remove Highlights Carousel?',
      yesCallback: jasmine.any(Function)
    });
    expect(globalLoaderService.showLoader).toHaveBeenCalled();
    expect(apiClientService.sportsHighlightCarousel().delete).toHaveBeenCalledWith(carouselList[1].id);
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
    expect(component.highlightCarousels).toEqual([carouselList[0], carouselList[2]]);
  });

  it('removeHandler should handle error on remove carousel', () => {
    component.highlightCarousels = _.cloneDeep(carouselList);
    apiClientService.sportsHighlightCarousel().delete.and.returnValue(Observable.throw({ message: 'err msg' }));
    component.removeHandler(component.highlightCarousels[1]);

    expect(dialogService.showConfirmDialog).toHaveBeenCalledWith({
      title: 'Highlights Carousel',
      message: 'Are You Sure You Want to Remove Highlights Carousel?',
      yesCallback: jasmine.any(Function)
    });
    expect(globalLoaderService.showLoader).toHaveBeenCalled();
    expect(apiClientService.sportsHighlightCarousel().delete).toHaveBeenCalledWith(component.highlightCarousels[1].id);
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
    expect(component.highlightCarousels).toEqual(carouselList);
    expect(errorService.emitError).toHaveBeenCalledWith('err msg');
  });

  it('#reorderHandler should update carousel order', fakeAsync(() => {
    const order: Order = {
      'order': ['5c067244c9e77c00013baf0e', '5c0553a2c9e77c00011887b3', '5c079612c9e77c0001188ae3'],
      'id': '5c067244c9e77c00013baf0e'
    };
    component.reorderHandler(order);
    expect(apiClientService.sportsHighlightCarousel().reorder).toHaveBeenCalledWith(order);
    expect(snackBar.open).toHaveBeenCalledWith(`Highlights Carousel order saved!`, 'Ok!', {
      duration: AppConstants.HIDE_DURATION,
    });
  }));

  describe('#segmenthandler', () => {
    it('should call segmentHandler method', () => {
      const segment = "Cricket";
      component.segmentHandler(segment);
      expect(globalLoaderService.showLoader).toHaveBeenCalled();
      expect(apiClientService.sportsHighlightCarousel().getHighlightCarouselBySegment).toHaveBeenCalled();
      expect(globalLoaderService.hideLoader).toHaveBeenCalled();
    });

    it('should get highlightcarouselList by segment', () => {
      const segment = "Cricket";
      component['segmentHandler'](segment);
      expect(globalLoaderService.showLoader).toHaveBeenCalled();
      expect(apiClientService.sportsHighlightCarousel().getHighlightCarouselBySegment).toHaveBeenCalledWith("Cricket");
      expect(apiClientService.sportsHighlightCarousel().getHighlightCarouselBySegment).toHaveBeenCalled();
      expect(globalLoaderService.hideLoader).toHaveBeenCalled();
    });
    
    it('should not get highlightcarouselList if there is no segment matching', () => {
      const segment = null;
      component['segmentHandler'](segment);
      expect(globalLoaderService.showLoader).toHaveBeenCalled();
      expect(apiClientService.sportsHighlightCarousel().getHighlightCarouselBySegment).toHaveBeenCalledWith(null);
      expect(apiClientService.sportsHighlightCarousel().getHighlightCarouselBySegment).toHaveBeenCalled();
      expect(globalLoaderService.hideLoader).toHaveBeenCalled();
    });
  });
});
