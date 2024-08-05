import { ActivatedRoute, Params, Router } from '@angular/router';
import { ComponentFixture, fakeAsync, TestBed, tick } from '@angular/core/testing';
import { CUSTOM_ELEMENTS_SCHEMA, NO_ERRORS_SCHEMA  } from '@angular/core';
import * as _ from 'lodash';

import {
  SportsHighlightCarouselComponent
} from '@app/sports-modules/highlight-carousels-module/highlight-carousels/highlight-carousel/highlight-carousel.component';
import { SportsModulesBreadcrumbsService } from '@app/sports-modules/sports-modules-breadcrumbs.service';
import { ApiClientService } from '@app/client/private/services/http';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { BrandService } from '@app/client/private/services/brand.service';
import { SportsModulesService } from '@app/sports-modules/sports-modules.service';
import { DateRange } from '@app/client/private/models/dateRange.model';
import { SportsHighlightCarousel } from '@app/client/private/models/sportsHighlightCarousel.model';
import { carouselMock, sportCarouselBreadcrumbs } from './highlight-carousel.component.mock';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ErrorService } from '@app/client/private/services/error.service';
import { AppConstants } from '@app/app.constants';
import {
  SportsHighlightCarouselsService
} from '@app/sports-modules/highlight-carousels-module/highlight-carousels/highlight-carousels.service';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { SegmentStoreService } from '@app/client/private/services/segment-store.service';
import { of,throwError } from 'rxjs';

describe('SportsHighlightCarouselComponent', () => {
  let component: SportsHighlightCarouselComponent,
    fixture: ComponentFixture<SportsHighlightCarouselComponent>;

  let activatedRoute: Partial<ActivatedRoute>;
  let router: Partial<Router>;
  let sportsModulesBreadcrumbsService: Partial<SportsModulesBreadcrumbsService>;
  let apiClientService;
  let globalLoaderService: Partial<GlobalLoaderService>;
  let brandService: Partial<BrandService>;
  let snackBar: Partial<MatSnackBar>;
  let errorService: Partial<ErrorService>;
  let sportsModulesService: Partial<SportsModulesService>;
  let sportsHighlightCarouselsService;
  let dialogService;
  let segmentStoreService;

  const routeParams: Params = {
    'id': '57fcfcd9b6aff9ba6c252a2c',
    'moduleId': '5bf53af4c9e77c0001a533d1',
    'carouselId': '5c055537c9e77c000168a3b7'
  };

  let carousel: SportsHighlightCarousel;

  beforeEach(fakeAsync(() => {
    carousel = _.cloneDeep(carouselMock);

    activatedRoute = {
      params: of(routeParams)
    };
    router = {
      navigate: jasmine.createSpy('navigate'),
      url: '/current-test-url'
    };
    sportsModulesBreadcrumbsService = {
      getBreadCrumbsForSportsHighlightCarousel: jasmine.createSpy('getBreadCrumbsForSportsHighlightCarousel')
        .and.returnValue(of(sportCarouselBreadcrumbs)),
      getBreadcrubs: jasmine.createSpy('getBreadcrubs')
        .and.returnValue(of(sportCarouselBreadcrumbs))
    };
    apiClientService = {
      sportsHighlightCarousel: jasmine.createSpy('sportsHighlightCarousel').and.returnValue({
        findById: jasmine.createSpy('findById').and.returnValue(of({ body: carousel })),
        delete: jasmine.createSpy('delete').and.returnValue(of({ body: '' })),
        update: jasmine.createSpy('update').and.returnValue(of({ body: carousel })),
        deleteIcon: jasmine.createSpy('deleteIcon').and.returnValue(of({ body: carousel })),
        findAllByBrandAndSport: jasmine.createSpy('findAllByBrandAndSport').and.returnValue(of({ body: carousel }))
      }),
      fanzoneService: jasmine.createSpy('fanzoneService').and.returnValue({
        getAllFanzones: jasmine.createSpy('getAllFanzones').and.returnValue(of([{ active: false, name: 'Arsenal' }]))
      })
    };
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };
    brandService = {
      brand: 'bma',
      isIMActive: jasmine.createSpy('isIMActive')
    };
    sportsModulesService = {
      getSingleModuleData: jasmine.createSpy('getSingleModuleData').and.returnValue(
        of([{ id: 4 }, {}])
      )
    };
    snackBar = {
      open: jasmine.createSpy('open')
    };
    errorService = {
      emitError: jasmine.createSpy('emitError')
    };

    sportsHighlightCarouselsService = {
      saveWithIcon: jasmine.createSpy('saveWithIcon').and.returnValue(of(carousel)),
      uploadIcon: jasmine.createSpy('uploadIcon').and.returnValue(of({ body: carousel }))
    };

    dialogService = jasmine.createSpyObj('dialogServiceSpy', ['showNotificationDialog']);
    
    segmentStoreService = {
      setSegmentValue: jasmine.createSpy('setSegmentValue'),
      validateHomeModule: jasmine.createSpy('validateHomeModule').and.returnValue(of('homepage')),
    };

    TestBed.configureTestingModule({
      declarations: [SportsHighlightCarouselComponent],
      providers: [
        { provide: ActivatedRoute, useValue: activatedRoute },
        { provide: Router, useValue: router },
        { provide: SportsModulesBreadcrumbsService, useValue: sportsModulesBreadcrumbsService },
        { provide: ApiClientService, useValue: apiClientService },
        { provide: GlobalLoaderService, useValue: globalLoaderService },
        { provide: BrandService, useValue: brandService },
        { provide: MatSnackBar, useValue: snackBar },
        { provide: ErrorService, useValue: errorService },
        { provide: SportsModulesService, useValue: sportsModulesService },
        { provide: SportsHighlightCarouselsService, useValue: sportsHighlightCarouselsService},
        {provide: DialogService,useValue: dialogService },
        {provide: SegmentStoreService,useValue: segmentStoreService},
      ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA, NO_ERRORS_SCHEMA ]
    }).compileComponents();

    fixture = TestBed.createComponent(SportsHighlightCarouselComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
    tick();
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('#ngOnInit should call #loadInitialData', fakeAsync(() => {
    component['loadInitialData'] = jasmine.createSpy('loadInitialData');
    component.ngOnInit();
    tick();
    expect(component['loadInitialData']).toHaveBeenCalled();
    expect(component.sportConfigId).toEqual(routeParams.id);
    expect(component.carouselId).toEqual(routeParams.carouselId);
    expect(component.moduleId).toEqual(routeParams.moduleId);
    expect(component.highlightCarousel.displayMarketType).toEqual('PrimaryMarket')
  }));

  it('#validationHandler should validate form before update/create', () => {
    component.form = { valid: true } as any;
    component.dateRangeError = 'error';
    expect(component.validationHandler()).toBeFalsy();

    component.dateRangeError = null;
    expect(component.validationHandler()).toBeFalsy();

    component.dateRangeError = null;
    component.form = { valid: false } as any;
    expect(component.validationHandler()).toBeFalsy();

    component.form = { valid: true } as any;
    component.isSegmentValid = true;
    component.dateRangeError = null;
    expect(component.validationHandler()).toBeTruthy();
    
    component.form = { valid: true } as any;
    component.isSegmentValid = false;
    component.dateRangeError = null;
    expect(component.validationHandler()).toBeFalsy();
  });

  it('#uploadIconHandler should trigger click on hidden element', () => {
    component['iconUploadInput'] = {
      nativeElement: {
        click: jasmine.createSpy('click')
      }
    } as any;
    component.uploadIconHandler();
    expect(component['iconUploadInput'].nativeElement.click).toHaveBeenCalledTimes(1);
  });

  it('#handleImageChange should do nothing if image is not set', () => {
    const event = {
      target: {
        files: []
      }
    } as any;
    component.handleImageChange(event);
    expect(component.imageToUpload.file).toBeFalsy();
    expect(snackBar.open).not.toHaveBeenCalled();
  });

  it('#handleImageChange should show message when file extension not supported', () => {
    const event = {
      target: {
        files: [{ fileType: 'png' }]
      }
    } as any;
    component.handleImageChange(event);
    expect(component.imageToUpload.file).toBeFalsy();
    expect(globalLoaderService.showLoader).toHaveBeenCalledTimes(1);
    expect(snackBar.open).toHaveBeenCalledWith(`Error. Unsupported file type.`, 'Ok!', {
      duration: AppConstants.HIDE_DURATION,
    });
  });

  it('#handleImageChange should save image to existing carousel', () => {
    component.actionButtons = {
      extendCollection: jasmine.createSpy('extendCollection')
    };
    component['updateEditableFields'] = jasmine.createSpy('updateEditableFields');
    const file = { name: 'fileName', type: 'image/svg+xml' } as any;
    const event = {
      target: {
        files: [file]
      }
    };

    component.highlightCarousel.id = '5c0fbf98c9e77c0001796720';
    const oldCarousel: SportsHighlightCarousel = _.cloneDeep(component.highlightCarousel);

    component.handleImageChange(event);
    expect(component.imageToUpload.file).toBeFalsy();
    expect(globalLoaderService.showLoader).toHaveBeenCalledTimes(2);
    expect(sportsHighlightCarouselsService.uploadIcon).toHaveBeenCalledWith(
      oldCarousel.id,
      file
    );
    expect(component.actionButtons.extendCollection).toHaveBeenCalledWith(carousel);
    expect(component['updateEditableFields']).toHaveBeenCalledWith(
      carousel,
      oldCarousel
    );
    expect(snackBar.open).toHaveBeenCalledWith(`Icon Uploaded.`, 'Ok!', {
      duration: AppConstants.HIDE_DURATION,
    });
    expect(globalLoaderService.hideLoader).toHaveBeenCalledTimes(2);
  });

  it('#handleImageChange should save image to existing carousel', () => {
    const file = { name: 'fileName', type: 'image/svg+xml' } as any;
    const event = {
      target: {
        files: [file]
      }
    };

    component.highlightCarousel.id = null;
    component.handleImageChange(event);
    expect(component.imageToUpload.file).toEqual(file);
  });

  it('#removeIconHandler should call #removeIconRequest', () => {
    component['removeIconRequest'] = jasmine.createSpy('removeIconRequest');
    component.highlightCarousel.id = '5c0fbf98c9e77c0001796720';
    component.removeIconHandler();
    expect(component['removeIconRequest']).toHaveBeenCalledTimes(1);
  });

  it('#removeIconHandler should clean up component.imageToUpload', () => {
    component['removeIconRequest'] = jasmine.createSpy('removeIconRequest');
    component.highlightCarousel.id = null;
    component.imageToUpload = {
      name: 'fileName',
      file: { file: 'someData' }
    } as any;
    component.removeIconHandler();
    expect(component['removeIconRequest']).toHaveBeenCalledTimes(0);
    expect(component.imageToUpload.name).toBeFalsy();
    expect(component.imageToUpload.file).toBeFalsy();
  });

  it('#toggleActiveStatus should call #validateDate', () => {
    component.validateDate = jasmine.createSpy('validateDate');
    component.highlightCarousel.disabled = true;
    component.toggleActiveStatus();
    expect(component.validateDate).toHaveBeenCalledTimes(1);
    expect(component.highlightCarousel.disabled).toBeFalsy();
  });

  it('#onDisplayOnDesktopCheck should call #validateDate', () => {
    component.validateDate = jasmine.createSpy('validateDate');
    component.highlightCarousel.displayOnDesktop = true;
    component.onDisplayOnDesktopCheck();
    expect(component.validateDate).toHaveBeenCalledTimes(1);
    expect(component.highlightCarousel.displayOnDesktop).toBeFalsy();
  });

  it('#handleDateUpdate should set display date to carousel', () => {
    component.validateDate = jasmine.createSpy('validateDate ');
    const dateRange: DateRange = {
      endDate: '2019-10-18T17:37:07+03:00',
      startDate: '2019-10-02T17:37:07+03:00'
    };

    component.handleDateUpdate(dateRange);
    expect(component.highlightCarousel.displayFrom).toEqual('2019-10-02T14:37:07.000Z');
    expect(component.highlightCarousel.displayTo).toEqual('2019-10-18T14:37:07.000Z');
    expect(component.validateDate).toHaveBeenCalledTimes(1);
  });

  describe('validateDate', () => {
    it('should return error (startDate > endDate && currentDate < endDate)', () => {
      component.highlightCarousel.displayFrom = '2099-01-01T00:00:00.000Z';
      component.highlightCarousel.displayTo = '2098-01-01T00:00:00.000Z';
      expect(component.validateDate()).toBeFalsy();
      expect(component.dateRangeError).toEqual('"Display to" date should be after "Display from" date. Please amend your schedule.');
    });

    it('should return error (currentDate > endDate)', () => {
      component.highlightCarousel.displayFrom = '2000-01-01T00:00:00.000Z';
      component.highlightCarousel.displayTo = '2000-01-01T00:00:00.000Z';
      expect(component.validateDate()).toBeFalsy();
      expect(component.dateRangeError).toEqual('"Display to" date should be in future. Please amend your schedule.');
    });

    it('should not return error', () => {
      component.highlightCarousel.displayFrom = '2099-01-01T00:00:00.000Z';
      component.highlightCarousel.displayTo = '2099-01-01T00:00:00.000Z';
      expect(component.validateDate()).toBeTruthy();
      expect(component.dateRangeError).toBeFalsy();
    });
  });

  it('#getEventsIntersection should return [1]', () => {
    carousel.events = ['1'];
    component.highlightCarousel.events = ['1'];
  });

  it('#getEventsIntersection should return []', () => {
    carousel.events = ['1'];
    component.highlightCarousel = _.cloneDeep(carousel);
    component.highlightCarousel.events = ['2'];
  });

  it('#changeEventSelection should call #setAdditionalFormFields', () => {
    component.highlightCarousel = {
      events: ['2'],
      typeId: '321'
    } as any;
    component['setAdditionalFormFields'] = jasmine.createSpy('setAdditionalFormFields');
    component.changeEventSelection(true);
    expect(component.highlightCarousel.events).toBeFalsy();
    component.changeEventSelection(false);
    expect(component.highlightCarousel.typeId).toBeFalsy();
    expect(component['setAdditionalFormFields']).toHaveBeenCalledTimes(2);
  });

  it('#actionHandler should call #remove', () => {
    component['remove'] = jasmine.createSpy('remove');
    component.actionsHandler('remove');
    expect(component['remove']).toHaveBeenCalledTimes(1);
  });

  it('#actionHandler should call #save', () => {
    component['save'] = jasmine.createSpy('save');
    component.actionsHandler('save');
    expect(component['save']).toHaveBeenCalledTimes(1);
  });

  it('#actionHandler should call #revert', () => {
    component['revert'] = jasmine.createSpy('revert');
    component.actionsHandler('revert');
    expect(component['revert']).toHaveBeenCalledTimes(1);
  });

  it('#actionHandler should do nothing', () => {
    component['remove'] = jasmine.createSpy('remove');
    component['save'] = jasmine.createSpy('save');
    component['revert'] = jasmine.createSpy('revert');
    component.actionsHandler('test');
    expect(component['remove']).not.toHaveBeenCalledTimes(1);
    expect(component['save']).not.toHaveBeenCalledTimes(1);
    expect(component['revert']).not.toHaveBeenCalledTimes(1);
  });

  it('#uploadButtonText should return button title', () => {
    component.highlightCarousel.svgFilename = {
      filename: 'file name'
    } as any;
    expect(component.uploadButtonText).toEqual('Change Icon');

    component.highlightCarousel.svgFilename = null;
    component.imageToUpload = {
      name: 'name'
    } as any;
    expect(component.uploadButtonText).toEqual('Change Icon');

    component.imageToUpload = {
      name: null
    } as any;
    expect(component.uploadButtonText).toEqual('Upload Icon');
  });

  it('#updateNotEditableFields should update editable fields', () => {
    component.highlightCarousel = _.cloneDeep(carouselMock);
    const date = (new Date()).toISOString();
    component.highlightCarousel.updatedAt = date;
    const sourceCarousel = _.cloneDeep(carouselMock);
    sourceCarousel.title = 'source title';
    sourceCarousel.limit = 4;
    component.highlightCarousel = component['updateEditableFields'](component.highlightCarousel, sourceCarousel);
    expect(component.highlightCarousel.title).toEqual('source title');
    expect(component.highlightCarousel.limit).toEqual(4);
    expect(component.highlightCarousel.updatedAt).toEqual(date);
  });

  it('#removeIconRequest should send request to remove icon', () => {
    component.actionButtons = {
      extendCollection: jasmine.createSpy('extendCollection')
    };
    component['updateEditableFields'] = jasmine.createSpy('updateEditableFields');
    component.highlightCarousel.id = '5c0e4addc9e77c00017ff132';

    component['removeIconRequest']();
    expect(globalLoaderService.showLoader).toHaveBeenCalledTimes(2);
    expect(apiClientService.sportsHighlightCarousel().deleteIcon).toHaveBeenCalledWith('5c0e4addc9e77c00017ff132');
    expect(component.actionButtons.extendCollection).toHaveBeenCalledWith(carousel);
    expect(component['updateEditableFields']).toHaveBeenCalledWith(carousel, carousel);
    expect(snackBar.open).toHaveBeenCalledWith(`Icon Removed.`, 'Ok!', {
      duration: AppConstants.HIDE_DURATION,
    });
    expect(globalLoaderService.hideLoader).toHaveBeenCalledTimes(2);
  });

  it('#removeIconRequest should handle error on remove icon', fakeAsync(() => {
    apiClientService.sportsHighlightCarousel().deleteIcon.and.returnValue(throwError({ body: 'error' }));
    component['updateEditableFields'] = jasmine.createSpy('updateEditableFields');
    component.highlightCarousel.id = '5c0e4addc9e77c00017ff132';

    component['removeIconRequest']();
    tick();
    expect(globalLoaderService.showLoader).toHaveBeenCalledTimes(2);
    expect(apiClientService.sportsHighlightCarousel().deleteIcon).toHaveBeenCalledWith('5c0e4addc9e77c00017ff132');
    expect(component['updateEditableFields']).not.toHaveBeenCalledWith(component.highlightCarousel, carousel);
    expect(snackBar.open).not.toHaveBeenCalledWith(`Icon Removed.`, 'Ok!', {
      duration: AppConstants.HIDE_DURATION,
    });
    expect(globalLoaderService.hideLoader).toHaveBeenCalledTimes(2);
  }));

  it('#remove should call remove carousel request', () => {
    component.highlightCarousel.id = '5c0e4addc9e77c00017ff132';
    component['remove']();
    expect(globalLoaderService.showLoader).toHaveBeenCalledTimes(2);
    expect(apiClientService.sportsHighlightCarousel().delete).toHaveBeenCalledWith('5c0e4addc9e77c00017ff132');
    expect(router.navigate).toHaveBeenCalledWith([
      'sports-pages/sport-categories/57fcfcd9b6aff9ba6c252a2c/sports-module/sports-highlight-carousels/5bf53af4c9e77c0001a533d1'
    ]);
    expect(globalLoaderService.hideLoader).toHaveBeenCalledTimes(2);
  });

  it('#remove should handle error on request fail', fakeAsync(() => {
    apiClientService.sportsHighlightCarousel().delete.and.returnValue(throwError({ body: 'error' }));
    component.highlightCarousel.id = '5c0e4addc9e77c00017ff132';
    component['remove']();
    tick();
    expect(globalLoaderService.showLoader).toHaveBeenCalledTimes(2);
    expect(apiClientService.sportsHighlightCarousel().delete).toHaveBeenCalledWith('5c0e4addc9e77c00017ff132');
    expect(router.navigate).not.toHaveBeenCalledWith([
      'sports-pages/sport-categories/57fcfcd9b6aff9ba6c252a2c/sports-module/sports-highlight-carousels/5bf53af4c9e77c0001a533d1'
    ]);
    expect(globalLoaderService.hideLoader).toHaveBeenCalledTimes(2);
  }));

  it('#save should call create', () => {
    component.validateDate = jasmine.createSpy('validateDate ');
    component['createRequest'] = jasmine.createSpy('createRequest');
    component.carouselId = undefined;
    component.dateRangeError = null;

    component['save']();
    expect(component['createRequest']).toHaveBeenCalledTimes(1);
    expect(component.validateDate).toHaveBeenCalledTimes(1);
  });

  it('#save should call update', () => {
    component.validateDate = jasmine.createSpy('validateDate ');
    component['updateRequest'] = jasmine.createSpy('updateRequest');
    component.highlightCarousel.id = '5c0e4addc9e77c00017ff132';
    component.dateRangeError = null;

    component['save']();
    expect(component['updateRequest']).toHaveBeenCalledTimes(1);
    expect(component.validateDate).toHaveBeenCalledTimes(1);
  });

  it('#save should do nothing', () => {
    component.validateDate = jasmine.createSpy('validateDate ');
    component['updateRequest'] = jasmine.createSpy('updateRequest');
    component['createRequest'] = jasmine.createSpy('createRequest');

    component.dateRangeError = 'error';
    component['save']();

    expect(component['updateRequest']).not.toHaveBeenCalled();
    expect(component['createRequest']).not.toHaveBeenCalled();
    expect(component.validateDate).toHaveBeenCalledTimes(1);
  });

  it('#createRequest should create carousel', () => {
    component.imageToUpload = {
      file: 'some image'
    } as any;
    component.module = { pageId: '312' } as any;
    component.isHomePage = false;

    component['getUrlToGoEdit'] = jasmine.createSpy('getUrlToGoEdit').and.returnValue('test/url');
    component['createRequest']();
    expect(globalLoaderService.showLoader).toHaveBeenCalledTimes(2);
    expect(sportsHighlightCarouselsService.saveWithIcon).toHaveBeenCalledWith(
      component.highlightCarousel,
      component.imageToUpload.file
    );
    expect(globalLoaderService.hideLoader).toHaveBeenCalledTimes(2);
    expect(component['getUrlToGoEdit']).toHaveBeenCalledWith('5c08e4dac9e77c00013099c2');
    expect(router.navigate).toHaveBeenCalledWith(['test/url']);
  });

  it('#createRequest should handle error request', fakeAsync(() => {
    sportsHighlightCarouselsService.saveWithIcon.and.returnValue(throwError('error msg'));
    component.imageToUpload = {
      file: 'some image'
    } as any;
    component.module = { pageId: '312' } as any;
    component['getUrlToGoEdit'] = jasmine.createSpy('getUrlToGoEdit').and.returnValue('test/url');
    component['createRequest']();
    tick();
    expect(globalLoaderService.showLoader).toHaveBeenCalledTimes(2);
    expect(sportsHighlightCarouselsService.saveWithIcon).toHaveBeenCalledWith(
      component.highlightCarousel,
      component.imageToUpload.file
    );
    expect(globalLoaderService.hideLoader).toHaveBeenCalledTimes(2);
    expect(component['getUrlToGoEdit']).not.toHaveBeenCalledWith('312');
    expect(router.navigate).not.toHaveBeenCalledWith(['test/url']);
    expect(errorService.emitError).toHaveBeenCalledWith('error msg');
  }));

  it('#updateRequest should update existing carousel', () => {
    component.actionButtons = {
      extendCollection: jasmine.createSpy('extendCollection')
    };
    component.imageToUpload = {
      file: 'some image'
    } as any;
    component['updateRequest']();
    expect(globalLoaderService.showLoader).toHaveBeenCalledTimes(2);
    expect(apiClientService.sportsHighlightCarousel().update).toHaveBeenCalledWith(
      component.highlightCarousel
    );
    expect(component.highlightCarousel).toEqual(carousel);
    expect(component.actionButtons.extendCollection).toHaveBeenCalledWith(carousel);
    expect(dialogService.showNotificationDialog).toHaveBeenCalledWith(
      {
        title: 'Highlight Carousel', message: 'Highlight Carousel is Saved.',
        closeCallback: jasmine.any(Function)
      }
    );
    expect(segmentStoreService.setSegmentValue).toHaveBeenCalled();
    expect(globalLoaderService.hideLoader).toHaveBeenCalledTimes(2);
  });

  it('#updateRequest should hide loader on error', fakeAsync(() => {
    apiClientService.sportsHighlightCarousel().update.and.returnValue(throwError('error'));
    component.actionButtons = {
      extendCollection: jasmine.createSpy('extendCollection')
    };
    component.imageToUpload = {
      file: 'some image'
    } as any;
    component['updateRequest']();
    tick();
    expect(globalLoaderService.showLoader).toHaveBeenCalledTimes(2);
    expect(apiClientService.sportsHighlightCarousel().update).toHaveBeenCalledWith(
      component.highlightCarousel
    );
    expect(component.actionButtons.extendCollection).not.toHaveBeenCalledWith(carousel);
    expect(globalLoaderService.hideLoader).toHaveBeenCalledTimes(2);
  }));

  it('#revert should call #loadInitialData', () => {
    component['loadInitialData'] = jasmine.createSpy('loadInitialData');
    component['revert']();
    expect(component['loadInitialData']).toHaveBeenCalledTimes(1);
  });

  it('displayMarketType returns true', () => {
      apiClientService.sportsHighlightCarousel.findById = jasmine.createSpy('findById').and.returnValue(of({ body: {displayMarketType: 'PrimaryMarket'} }));
      component.carouselId = '1212';
      const routeParamsMock = {
        id: 'highlightCarouselId'
      };
      component['loadInitialData'](routeParamsMock);
      expect(component.highlightCarousel.displayMarketType).toBeTruthy();
    })
  
    it('displayMarketType returns false', () => {
      const routeParamsMock = {
        id: 'highlightCarouselId'
      };
      apiClientService.sportsHighlightCarousel.findById = jasmine.createSpy('findById').and.returnValue(of({ body: {displayMarketType: null} }));
      component.carouselId = '1212';
      component['loadInitialData'](routeParamsMock);
      expect(component.highlightCarousel.displayMarketType).toBeTruthy();
      expect(component.highlightCarousel.displayMarketType).toBe('PrimaryMarket');
    })

  it('#loadInitialData should get carousel by ID', () => {
    const routeParamsMock = {
      id: 'highlightCarouselId'
    };
    component['setupForm'] = jasmine.createSpy('setupForm');
    component['getBreadcrumbs'] = jasmine.createSpy('getBreadcrumbs');
    component.carouselId = '5c055537c9e77c000168a3b7';

    component['loadInitialData'](routeParamsMock);
    expect(apiClientService.sportsHighlightCarousel().findById).toHaveBeenCalledWith(component.carouselId);
    expect(component['setupForm']).toHaveBeenCalledTimes(1);
    expect(component['getBreadcrumbs']).toHaveBeenCalledTimes(1);
  });

  it('#loadInitialData should get module data', () => {
    const routeParamsMock = {
      id: 'highlightCarouselId'
    };
    component['setupForm'] = jasmine.createSpy('setupForm');
    component['getBreadcrumbs'] = jasmine.createSpy('getBreadcrumbs');
    component.highlightCarousel.sportId = 1;
    component.carouselId = undefined;
    component.moduleId = '5c0e6e3bc9e77c00015e83a3';
    component.sportConfigId = '0';

    component['loadInitialData'](routeParamsMock);
    expect(sportsModulesService.getSingleModuleData).toHaveBeenCalledWith(component.moduleId, component.sportConfigId);
    expect(component['setupForm']).toHaveBeenCalledTimes(1);
    expect(component['getBreadcrumbs']).toHaveBeenCalledTimes(1);
  });

  it('#setupForm should create form', () => {
    component.highlightCarousel.events = ['1'];
    component['setAdditionalFormFields'] = jasmine.createSpy('setAdditionalFormFields');

    component['setupForm']();
    expect(component.selectByTypeId).toBeFalsy();

    component.highlightCarousel.events = null;
    component['setupForm']();
    expect(component.selectByTypeId).toBeTruthy();

    expect(component.form).toBeTruthy();
    expect(component['setAdditionalFormFields']).toHaveBeenCalledTimes(2);
  });

  it('#setAdditionalFormFields should add proper field', () => {
    component.selectByTypeId = true;
    component.highlightCarousel.typeId = 123;
    component.highlightCarousel.typeIds = ['123'];
    component.form = {
      controls: {
        'typeIds' :  {
          setValidators  : jasmine.createSpy('setValidators'),
          updateValueAndValidity : jasmine.createSpy('updateValueAndValidity')
        } ,
        'typeId' : {
          setValidators  : jasmine.createSpy('setValidators'),
          updateValueAndValidity : jasmine.createSpy('updateValueAndValidity')
        }
      },
      removeControl: jasmine.createSpy('removeControl'),
      addControl: jasmine.createSpy('addControl')
    } as any;

    component['setAdditionalFormFields']();
    expect(component.form.removeControl).toHaveBeenCalledWith('typeId');
    expect(component.form.removeControl).toHaveBeenCalledWith('events');

    expect(component.form.addControl).toHaveBeenCalledWith('typeId', jasmine.any(Object));
  });

  it('#getBreadcrumbs should get breadcrumbs from service', () => {
    const routeParamsMock = {
      id: 'highlightCarouselId'
    };
    component.highlightCarousel.title = 'titleMock';

    component['getBreadcrumbs'](routeParamsMock);

    expect(sportsModulesBreadcrumbsService.getBreadcrubs).toHaveBeenCalledWith(
      routeParamsMock,
      {
        customBreadcrumbs: [
          {
            label: component.highlightCarousel.title
          }
        ]
      });
  });

  describe('#onChangeDirectiveName', () => {
    it('set moduleRibbontab directiveName', () => {
        component.highlightCarousel = <SportsHighlightCarousel>{ displayMarketType: '' };
        component.onChangeDirectiveName('test');
        expect(component.highlightCarousel.displayMarketType).toBe('test');
    });
  });

  it('#getUrlToGoEdit should return correct url for edit page', () => {
    component.moduleId = '5beee212c9e77c0001fb69e8';
    expect(component['getUrlToGoEdit']('5c0fdb32c9e77c0001b04a58')).toEqual(
      `sports-pages/sport-categories/57fcfcd9b6aff9ba6c252a2c/sports-module/sports-highlight-carousels/5beee212c9e77c0001fb69e8
      /carousel/edit/5c0fdb32c9e77c0001b04a58`
    );
    expect(component['getUrlToGoEdit']('5c0fdb32c9e77c0001b04a58')).toEqual(
      `sports-pages/sport-categories/57fcfcd9b6aff9ba6c252a2c/sports-module/sports-highlight-carousels/5beee212c9e77c0001fb69e8
      /carousel/edit/5c0fdb32c9e77c0001b04a58`);

    component.sportConfigId = undefined;
    expect(component['getUrlToGoEdit']('5c0fdb32c9e77c0001b04a58')).toEqual(
      'sports-pages/homepage/sports-module/sports-highlight-carousels/5beee212c9e77c0001fb69e8/carousel/edit/5c0fdb32c9e77c0001b04a58'
    );
  });

  it('#getUrlToGoBack should return correct url to previous page', () => {
    component.moduleId = '5beee212c9e77c0001fb69e8';
    expect(component['getUrlToGoBack']).toEqual(
      'sports-pages/sport-categories/57fcfcd9b6aff9ba6c252a2c/sports-module/sports-highlight-carousels/5beee212c9e77c0001fb69e8'
    );
    component.sportConfigId = '55b1123c9e3897a34c02ab06';
    expect(component['getUrlToGoBack']).toEqual(
      'sports-pages/sport-categories/55b1123c9e3897a34c02ab06/sports-module/sports-highlight-carousels/5beee212c9e77c0001fb69e8'
    );

    component.sportConfigId = undefined;
    expect(component['getUrlToGoBack']).toEqual(
      'sports-pages/homepage/sports-module/sports-highlight-carousels/5beee212c9e77c0001fb69e8'
    );
  });
  describe('modifiedSegmentsHandler', () => {
    it('when segmentConfig data is not defined', () => {
      const segmentConfigData = undefined;
      component.modifiedSegmentsHandler(segmentConfigData);
      expect(component.highlightCarousel).toEqual(component.highlightCarousel);
    });
    it('when segmentConfig data is defined', () => {
      const segmentConfigData = { exclusionList: [], inclusionList: [], universalSegment: true };
      component.modifiedSegmentsHandler(segmentConfigData);
      const result = { ...component.highlightCarousel, ...segmentConfigData };
      expect(component.highlightCarousel).toEqual(result);
    });
  });
  describe('#isSegmentFormValid', () => {
    it('should set the isSegmentFormValid to true', () => {
      const isValid = true;
      component.isSegmentFormValid(isValid)
      expect(component.isSegmentValid).toBeTrue();
    });
    it('should set the isSegmentFormValid to false', () => {
      const isValid = false;
      component.isSegmentFormValid(isValid)
      expect(component.isSegmentValid).toBeFalse();
    });
    it('should set the isSegmentFormValid to false', () => {
      const isValid = null;
      component.isSegmentFormValid(isValid)
      expect(component.isSegmentValid).toBeNull();
    });
  });
  describe('#Fanzone Inlcusions', () => {
    it('#should toggle all', () => {
      component.ngOnInit();
      fixture.detectChanges();
      fixture.whenStable().then(() => {
        expect(component.allSelected).toEqual(false);
        fixture.whenStable().then(() => {
          expect(component.toggleAllSelection.length).toEqual(0);
        });
      });
    });
  });
  describe('#onselect21stTeam', () => {
    it('#onselect21stTeam', () => {
      component.fanzoneInclusions21st = false;
      component.onselect21stTeam();
      expect(component.fanzoneInclusions21st).toBeTrue();
    });
  });
  
  describe('#checkIf21stTeamSelected', () => {
    it('#checkIf21stTeamSelected', () => {
      component.fanzoneInclusions21st = true;
      component.checkIf21stTeamSelected();
      expect(component.highlightCarousel.fanzoneInclusions.length).toBe(1);
    });
    it('#checkIf21stTeamSelected if false', () => {
      component.fanzoneInclusions21st = false;
      component.checkIf21stTeamSelected();
    });
  });
});

