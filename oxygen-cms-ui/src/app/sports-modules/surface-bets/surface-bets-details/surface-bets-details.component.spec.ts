import { async, ComponentFixture, fakeAsync, TestBed, tick } from '@angular/core/testing';
import { ActivatedRoute, Params, Router } from '@angular/router';
import { CUSTOM_ELEMENTS_SCHEMA, NO_ERRORS_SCHEMA  } from '@angular/core';
import { SportsSurfaceBetsDetailsComponent } from '@app/sports-modules/surface-bets/surface-bets-details/surface-bets-details.component';
import { ApiClientService } from '@app/client/private/services/http';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { BrandService } from '@app/client/private/services/brand.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { SportsModulesBreadcrumbsService } from '@app/sports-modules/sports-modules-breadcrumbs.service';
import { FracToDecService } from '@app/shared/services/fracToDec/frac-to-dec.service';
import { SportsSurfaceBetsService } from '@app/sports-modules/surface-bets/surface-bets.service';
import { Observable, of, throwError } from 'rxjs';
import { SurfaceBet } from '@app/client/private/models/surfaceBet.model';
import { DateRange } from '@app/client/private/models/dateRange.model';
import { AppConstants, CSPSegmentLSConstants } from '@app/app.constants';
import * as _ from 'lodash';
import { Price } from '@app/client/private/models/price.model';
import { SportCategory } from '@app/client/private/models/sportcategory.model';
import { FormGroup } from '@angular/forms';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { SegmentStoreService } from '@app/client/private/services/segment-store.service';
import { SortByPipe as sortBy} from '@app/client/private/pipes/sortBy.pipe';
import { SharedModule } from '@app/shared/shared.module';

let surfaceBetMock: SurfaceBet;
let routeParams: Params;
let mockSurfaceBet;

const sportsMock = [
  { id: 32 },
  { id: 8 }
] as any;

describe('SportsSurfaceBetsComponent', () => {
  let component: SportsSurfaceBetsDetailsComponent,
    fixture: ComponentFixture<SportsSurfaceBetsDetailsComponent>;

    let activatedRoute: { params: Observable<Params>; },
    router: Partial<Router>,
    apiClientService,
    segmentStoreService,
    sportsSurfaceBetsService,
    globalLoaderService: Partial<GlobalLoaderService>,
    brandService: Partial<BrandService>,
    snackBar: Partial<MatSnackBar>,
    sportsModulesBreadcrumbsService: Partial<SportsModulesBreadcrumbsService>,
    fracToDecService: Partial<FracToDecService>,
    dialogService: Partial<DialogService>,
    sortByPipe;

  const eventHubMock: any = {
    title: 'testhub',
    disabled: false,
    sortOrder: 0,
    indexNumber: 0
  };


  beforeEach(async(() => {
    routeParams = {
      'id': '57fcfcd9b6aff9ba6c252a2c',
      'moduleId': '5bf53af4c9e77c0001a533d1',
      'betId': '5c0e4addc9e77c00017ff132'
    };

    surfaceBetMock = {
      'displayFrom': '2019-01-14T16:01:44.656Z',
      'displayTo': '2019-01-15T16:01:44.656Z',
      'svg': '',
      'svgFilename': {
        'filename': '70d09581-d93e-42ed-a964-c723ed003349.svg',
        'originalname': '410.svg',
        'path': '/images/uploads/surfaceBet',
        'size': 313,
        'filetype': 'image/svg+xml'
      },
      'svgId': '#b49f740f-1e52-3e59-956d-4623336cb0a3',
      'content': null,
      'edpOn': false,
      'displayOnDesktop': false,
      'highlightsTabOn': false,
      'fanzoneInclusions': [],
      'references': [{'id':undefined,
        'relatedTo': 'sport',
        'refId': '108',
        'enabled': true,
      }, {
        'id':undefined,
        'relatedTo': 'sport',
        'refId': '55',
        'enabled': true,
      }, {'id':undefined,
        'relatedTo': 'edp',
        'refId': '6',
        'enabled': true,
      }],
      'selectionId': 54,
      'price': { 'priceType': 'LP', 'priceNum': 3, 'priceDen': 5, 'priceDec': 1.6 },
      'id': '5c0e4addc9e77c00017ff132',
      'createdBy': '5a30ee8aa36a75b109be3789',
      'createdByUserName': 'test.admin@coral.co.uk',
      'updatedBy': '5a30ee8aa36a75b109be3789',
      'updatedByUserName': 'test.admin@coral.co.uk',
      'createdAt': '2019-01-14T16:02:33.863Z',
      'updatedAt': '2019-01-16T15:43:32.040Z',
      'sortOrder': -26.0,
      'disabled': false,
      'title': 'test1 img1',
      'brand': 'bma',
      'pageId': null,
      'pageType': 'sport',
      'sportId': null,
      'exclusionList': [],
      'inclusionList': [],
      'universalSegment': true,
      categoryIDs: [108, 55],
      eventIDs: ['6']
    } as any;

     mockSurfaceBet = [
      {
          "id": "64d352f09ba03738133f1fe4",
          "createdBy": "5645b8a220bd9e0800afdc57",
          "createdByUserName": null,
          "updatedBy": "5645b8a220bd9e0800afdc57",
          "updatedByUserName": null,
          "createdAt": "2023-08-09T08:48:48.012Z",
          "updatedAt": "2023-08-09T08:48:48.012Z",
          "brand": "bma",
          "title": "Surface Bet Module"
      }
  ]
    activatedRoute = {
      params: of(routeParams)
    };
    router = {
      navigate: jasmine.createSpy('navigate'),
      url: '/current-test-url'
    };
    sportsModulesBreadcrumbsService = {
      getBreadcrubs: jasmine.createSpy('getBreadcrubs')
        .and.returnValue(of([{
          label: 'test label',
          url: 'test/url/surface-bet'
        }]))
    };
    apiClientService = {
      sportsSurfaceBets: jasmine.createSpy('sportsSurfaceBets').and.returnValue({
        findAllByBrand: jasmine.createSpy('findAllByBrand').and.returnValue(of({ body: [surfaceBetMock] })),
        findById: jasmine.createSpy('findById').and.returnValue(of({ body: surfaceBetMock })),
        delete: jasmine.createSpy('delete').and.returnValue(of({ body: '' })),
        update: jasmine.createSpy('update').and.returnValue(of({ body: surfaceBetMock })),
        deleteIcon: jasmine.createSpy('deleteIcon').and.returnValue(of({ body: surfaceBetMock })),
        getSurfaceBetTitle: jasmine.createSpy('getSurfaceBetTitle').and.returnValue(of({ body: mockSurfaceBet })),
        deleteSurfaceBetTitle : jasmine.createSpy('deleteSurfaceBetTitle'),
      }),
      eventHub: jasmine.createSpy('sportsSurfaceBets').and.returnValue({
        getAllEventHubs: jasmine.createSpy('findAllByBrandAndSport').and.returnValue(of([eventHubMock]))
      }),
      fanzoneService: jasmine.createSpy('fanzoneService').and.returnValue({
        getAllFanzones: jasmine.createSpy('getAllFanzones').and.returnValue(of([{ active: false, name: 'Arsenal' }]))
      })
    };

    let path = 'homepage/surface-bet';
    segmentStoreService = {
      validateSegmentValue: jasmine.createSpy('validateSegmentValue'),
      validateHomeModule: () => path.includes('homepage'),
      getSegmentMessage: () => of({segmentValue:'Universal', segmentModule:CSPSegmentLSConstants.SURFACE_BET_TAB }),
      updateSegmentMessage: jasmine.createSpy('updateSegmentMessage'),
      setSegmentValue:jasmine.createSpy('setSegmentValue')
    };
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };
    brandService = {
      brand: 'bma',
      isIMActive: jasmine.createSpy('isImActive').and.returnValue(true)
    };
    snackBar = {
      open: jasmine.createSpy('open')
    };
    sportsSurfaceBetsService = {
      getSportCategories: jasmine.createSpy('getSportCategories').and.returnValue(of(sportsMock)),
      saveWithIcon: jasmine.createSpy('saveWithIcon').and.returnValue(of(surfaceBetMock)),
      uploadIcon: jasmine.createSpy('uploadIcon').and.returnValue(of({ body: surfaceBetMock }))
    };
    dialogService = jasmine.createSpyObj('dialogServiceSpy', ['showNotificationDialog', 'showConfirmDialog']);
    fracToDecService = {
      fracToDec: jasmine.createSpy('fracToDec').and.returnValue(1.6)
    };
    sortByPipe = {
      transform: jasmine.createSpy('transform')
    };

    TestBed.configureTestingModule({
      imports: [SharedModule ],
      declarations: [SportsSurfaceBetsDetailsComponent,sortBy],
      providers: [
        { provide: ActivatedRoute, useValue: activatedRoute },
        { provide: Router, useValue: router },
        { provide: ApiClientService, useValue: apiClientService },
        { provide: GlobalLoaderService, useValue: globalLoaderService },
        { provide: BrandService, useValue: brandService },
        { provide: MatSnackBar, useValue: snackBar },
        { provide: SportsModulesBreadcrumbsService, useValue: sportsModulesBreadcrumbsService },
        { provide: FracToDecService, useValue: fracToDecService },
        { provide: SportsSurfaceBetsService, useValue: sportsSurfaceBetsService },
        { provide: DialogService, useValue: dialogService},
        { provide: SegmentStoreService, useValue: segmentStoreService},
        { provide: sortBy, useValue: sortByPipe }
      ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA, NO_ERRORS_SCHEMA ]
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SportsSurfaceBetsDetailsComponent);
    component = fixture.componentInstance;
    component.surfaceBet = _.clone(surfaceBetMock);
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('#ngOnInit should get route params and call loadInitialData', () => {
    component['loadInitialData'] = jasmine.createSpy('loadInitialData');
    component.ngOnInit();
    expect(component.surfaceBetId).toEqual('5c0e4addc9e77c00017ff132');
    expect(component.pageTitle).toEqual('Surface Bet:');
    expect(component.sportConfigId).toEqual('57fcfcd9b6aff9ba6c252a2c');

    routeParams.betId = null;
    component.ngOnInit();
    expect(component.pageTitle).toEqual('New Surface Bet');
  });

  it('#validationHandler should return form validity', () => {
    component.form = {
      valid: true
    } as any;
    component.isSegmentValid = true;
    expect(component.validationHandler()).toBe(true);
  });

  it('#handleDateUpdate should set surfaceBetDate', () => {
    let dateRange: DateRange = {
      endDate: '2019-10-18T17:37:07+03:00',
      startDate: '2019-10-02T17:37:07+03:00'
    };

    component.handleDateUpdate(dateRange);
    expect(component.surfaceBet.displayFrom).toEqual('2019-10-02T14:37:07.000Z');
    expect(component.surfaceBet.displayTo).toEqual('2019-10-18T14:37:07.000Z');

    dateRange = {
      endDate: 'test1',
      startDate: 'test2'
    };

    component.handleDateUpdate(dateRange);
    expect(component.surfaceBet.displayFrom).toEqual('2019-10-02T14:37:07.000Z');
    expect(component.surfaceBet.displayTo).toEqual('2019-10-18T14:37:07.000Z');
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

  it('#save should call create', () => {
    component['createRequest'] = jasmine.createSpy('createRequest');
    component['setReferences'] = jasmine.createSpy('setReferences');
    component.surfaceBet.id = undefined;

    component['save']();
    expect(component['createRequest']).toHaveBeenCalledTimes(1);
    expect(component['setReferences']).toHaveBeenCalledTimes(1);
  });

  it('#save should call update', () => {
    component['updateRequest'] = jasmine.createSpy('updateRequest');
    component['setReferences'] = jasmine.createSpy('setReferences');
    component.surfaceBetId = '5c0e4addc9e77c00017ff132';
      component['save']();
    expect(component['setReferences']).toHaveBeenCalledTimes(1);
    expect(component['updateRequest']).toHaveBeenCalledTimes(1);
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
        files: [{ type: 'png' }]
      }
    } as any;
    component.form = {
      valid: true,
    } as any;
    component['setupForm']();
    expect(component.form).toEqual(jasmine.any(FormGroup));
    component.handleImageChange(event);
    expect(component.imageToUpload.file).toBeFalsy();
    expect(globalLoaderService.showLoader).toHaveBeenCalledTimes(1);
    expect(snackBar.open).toHaveBeenCalledWith(`Error. Unsupported file type.`, 'Ok!', {
      duration: AppConstants.HIDE_DURATION,
    });
  });

  it('#handleImageChange should save image to existing surface bet', () => {
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

    component.surfaceBet.id = '5c0e4addc9e77c00017ff132';
    const oldBet: SurfaceBet = _.cloneDeep(component.surfaceBet);

    component.handleImageChange(event);
    expect(component.imageToUpload.file).toBeFalsy();
    expect(globalLoaderService.showLoader).toHaveBeenCalledTimes(2);
    expect(sportsSurfaceBetsService.uploadIcon).toHaveBeenCalledWith(
      oldBet.id,
      file
    );
    expect(component.actionButtons.extendCollection).toHaveBeenCalledWith(surfaceBetMock);
    expect(component['updateEditableFields']).toHaveBeenCalledWith(
      surfaceBetMock,
      oldBet
    );
    expect(snackBar.open).toHaveBeenCalledWith(`Icon Uploaded.`, 'Ok!', {
      duration: AppConstants.HIDE_DURATION,
    });
    expect(globalLoaderService.hideLoader).toHaveBeenCalledTimes(2);
  });

  it('#handleImageChange should handle error', () => {
    sportsSurfaceBetsService.uploadIcon.and.returnValue(throwError('error'));
    component['updateEditableFields'] = jasmine.createSpy('updateEditableFields');
    const file = { name: 'fileName', type: 'image/svg+xml' } as any;
    const event = {
      target: {
        files: [file]
      }
    };

    component.handleImageChange(event);
    expect(globalLoaderService.showLoader).toHaveBeenCalled();
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
  });

  it('#handleImageChange should save image to existing surface bet', () => {
    const file = { name: 'fileName', type: 'image/svg+xml' } as any;
    const event = {
      target: {
        files: [file]
      }
    };

    component.surfaceBet.id = null;
    component.handleImageChange(event);
    expect(component.imageToUpload.file).toEqual(file);
  });

  it('#removeIconHandler should call #removeIconRequest', () => {
    component['removeIconRequest'] = jasmine.createSpy('removeIconRequest');
    component.surfaceBetId = '5c0e4addc9e77c00017ff132';
    component.removeIconHandler();
    expect(component['removeIconRequest']).toHaveBeenCalledTimes(1);
  });

  it('#removeIconHandler should clean up component.imageToUpload', () => {
    component['removeIconRequest'] = jasmine.createSpy('removeIconRequest');
    component.surfaceBetId = null;
    component.imageToUpload = {
      name: 'fileName',
      file: { file: 'someData' }
    } as any;
    component['iconUploadInput'] = {
      nativeElement: {
        value: 'file',
        click: jasmine.createSpy('click')
      }
    } as any;

    component.removeIconHandler();
    expect(component['removeIconRequest']).toHaveBeenCalledTimes(0);
    expect(component.imageToUpload.name).toBeFalsy();
    expect(component.imageToUpload.file).toBeFalsy();
    component.uploadIconHandler();
    expect(component['iconUploadInput'].nativeElement.click).toHaveBeenCalledTimes(1);
  });

  it('#uploadButtonText should return button title', () => {
    component.surfaceBet.svgFilename = {
      filename: 'file name'
    } as any;
    expect(component.uploadButtonText).toEqual('Change Icon');

    component.surfaceBet.svgFilename = null;
    component.imageToUpload = {
      name: 'name'
    } as any;
    expect(component.uploadButtonText).toEqual('Change Icon');

    component.imageToUpload = {
      name: null
    } as any;
    expect(component.uploadButtonText).toEqual('Upload Icon');
  });

  it('#trackSportById should return sport id', () => {
    const sport = {
      id: 'test_id'
    } as SportCategory;
    expect(component.trackSportById(sport)).toBe('test_id');
  });

  it('#setPrice should set decimal price value', () => {
    const price: Price = {
      'priceType': 'LP',
      'priceNum': 3,
      'priceDen': 5,
      'priceDec': undefined
    };

    component.setPrice(price);
    expect(fracToDecService.fracToDec).toHaveBeenCalledWith(3, 5);
    expect(price.priceDec).toBe(1.6);
  });

  it('#setPrice should set price dec to null', () => {
    const price: Price = {
      'priceType': 'LP',
      'priceNum': undefined,
      'priceDen': 5,
      'priceDec': 54
    };

    component.setPrice(price);
    expect(fracToDecService.fracToDec).not.toHaveBeenCalled();
    expect(price.priceDec).toBe(null);
  });

  it('#validateSelection should set error', () => {
    fixture.detectChanges();
    component.validateSelection();
    expect(component.error).toEqual(null);
    component.surfaceBet = _.clone(surfaceBetMock);
    component.surfaceBet.id = _.uniqueId();
    const futureDate = new Date();
    futureDate.setDate(futureDate.getDate() + 1);
    const stringDate = futureDate.toISOString();

    component.allSurfaceBets[0].displayTo = stringDate;
    component.allSurfaceBets[0].selectionId = '8';
    component.allSurfaceBets[0].title = 'Surface Bet 1';
    component.surfaceBet = surfaceBetMock;
    expect(component.error).toEqual('This selection ID is already used in: Surface Bet 1');
    expect(component.error).toEqual(null);
  });

  it('#validateSelection should error to null', () => {
    component.surfaceBet.disabled = true;
    component.validateSelection();
    expect(component.error).toEqual(null);
  });

  it('#setReferences should set surfaceBet.references', () => {
    const references = [
      { id:undefined, refId: '42', relatedTo: 'edp', enabled: true },
      { id:undefined, refId: '75', relatedTo: 'edp', enabled: true },
      { id:undefined,  refId: '2', relatedTo: 'edp', enabled: true },
      { id:undefined, refId: '64', relatedTo: 'sport', enabled: true },
      { id:undefined, refId: '234', relatedTo: 'sport', enabled: true },
      { id:undefined, refId: '6', relatedTo: 'sport', enabled: true },
      { id:undefined, refId: '34', relatedTo: 'sport', enabled: true }
    ];
    component.surfaceBet.eventIDs = ['42', '75', '2'];
    component.surfaceBet.categoryIDs = [64, 234, 6, 34];
    component['setReferences']();
    expect(component.surfaceBet.references).toBeDefined();

    const refsWithHomepage = [
      ...references,
      { id:undefined, refId: '0', relatedTo: 'sport', enabled: true }
    ];
    component.surfaceBet.highlightsTabOn = true;
    component['setReferences']();
    expect(component.surfaceBet.references).toEqual(refsWithHomepage);
  });

  it('#removeIconRequest should send request to remove icon', () => {
    component.actionButtons = {
      extendCollection: jasmine.createSpy('extendCollection')
    };
    component['updateEditableFields'] = jasmine.createSpy('updateEditableFields');
    component.surfaceBet.id = '5c0e4addc9e77c00017ff132';
    component['setupForm']();
        expect(component.form).toEqual(jasmine.any(FormGroup));

    component['removeIconRequest']();
    expect(globalLoaderService.showLoader).toHaveBeenCalledTimes(2);
    expect(apiClientService.sportsSurfaceBets().deleteIcon).toHaveBeenCalledWith('5c0e4addc9e77c00017ff132');
    expect(component['updateEditableFields']).toHaveBeenCalledWith(surfaceBetMock, surfaceBetMock);
    expect(snackBar.open).toHaveBeenCalledWith(`Icon Removed.`, 'Ok!', {
      duration: AppConstants.HIDE_DURATION,
    });
    expect(globalLoaderService.hideLoader).toHaveBeenCalledTimes(2);
  });

  it('#removeIconRequest should handle error on remove icon', fakeAsync(() => {
    apiClientService.sportsSurfaceBets().deleteIcon.and.returnValue(throwError({ body: 'error' }));
    component['updateEditableFields'] = jasmine.createSpy('updateEditableFields');
    component.surfaceBet.id = '5c0e4addc9e77c00017ff132';
    component['removeIconRequest']();
    tick();
    expect(globalLoaderService.showLoader).toHaveBeenCalledTimes(2);
    expect(apiClientService.sportsSurfaceBets().deleteIcon).toHaveBeenCalledWith('5c0e4addc9e77c00017ff132');
    expect(component['updateEditableFields']).not.toHaveBeenCalledWith(component.surfaceBet, surfaceBetMock);
    expect(snackBar.open).not.toHaveBeenCalledWith(`Icon Removed.`, 'Ok!', {
      duration: AppConstants.HIDE_DURATION,
    });
    expect(globalLoaderService.hideLoader).toHaveBeenCalledTimes(2);
  }));

  it('#remove should call remove bet request and navigate to sport modules', () => {
    component.surfaceBet.id = '5c0e4addc9e77c00017ff132';
    component['remove']();
    expect(globalLoaderService.showLoader).toHaveBeenCalledTimes(2);
    expect(apiClientService.sportsSurfaceBets().delete).toHaveBeenCalledWith('5c0e4addc9e77c00017ff132');
    expect(router.navigate).toHaveBeenCalledWith([
      'sports-pages/sport-categories/57fcfcd9b6aff9ba6c252a2c/sports-module/surface-bets/5bf53af4c9e77c0001a533d1'
    ]);
    expect(globalLoaderService.hideLoader).toHaveBeenCalledTimes(2);
  });

  it('#remove should call remove bet request and navigate to home page', () => {
    component.surfaceBet.id = '5c0e4addc9e77c00017ff132';
    component.sportConfigId = undefined;
    component['remove']();
    expect(globalLoaderService.showLoader).toHaveBeenCalledTimes(2);
    expect(apiClientService.sportsSurfaceBets().delete).toHaveBeenCalledWith('5c0e4addc9e77c00017ff132');
    expect(router.navigate).toHaveBeenCalledWith([
      'sports-pages/homepage/sports-module/surface-bets/5bf53af4c9e77c0001a533d1'
    ]);
    expect(globalLoaderService.hideLoader).toHaveBeenCalledTimes(2);
  });

  it('#remove should handle error on request fail', fakeAsync(() => {
    apiClientService.sportsSurfaceBets().delete.and.returnValue(throwError({ body: 'error' }));
    component.surfaceBet.id = '5c0e4addc9e77c00017ff132';
    component['remove']();
    tick();
    expect(globalLoaderService.showLoader).toHaveBeenCalledTimes(2);
    expect(apiClientService.sportsSurfaceBets().delete).toHaveBeenCalledWith('5c0e4addc9e77c00017ff132');
    expect(router.navigate).not.toHaveBeenCalledWith([
      ''
    ]);
    expect(globalLoaderService.hideLoader).toHaveBeenCalledTimes(2);
  }));

  it('#createRequest should create surface bet', () => {
    component.imageToUpload = {
      file: 'some image'
    } as any;
    component.isHomePage = false;
    component['getUrlToGoEdit'] = jasmine.createSpy('getUrlToGoEdit').and.returnValue('test/url');
    component['createRequest']();
    expect(globalLoaderService.showLoader).toHaveBeenCalledTimes(2);
    expect(sportsSurfaceBetsService.saveWithIcon).toHaveBeenCalledWith(
      component.surfaceBet,
      component.imageToUpload.file
    );
    // expect(segmentStoreService.setSegmentValue).toHaveBeenCalled();
    // expect(globalLoaderService.hideLoader).toHaveBeenCalledTimes(2);
    expect(component['getUrlToGoEdit']).toHaveBeenCalledWith('5c0e4addc9e77c00017ff132');
    expect(router.navigate).toHaveBeenCalledWith(['test/url']);
  });

  it('#createRequest should handle error request', fakeAsync(() => {
    sportsSurfaceBetsService.saveWithIcon.and.returnValue(throwError('error msg'));
    component.imageToUpload = {
      file: 'some image'
    } as any;
    component['getUrlToGoEdit'] = jasmine.createSpy('getUrlToGoEdit').and.returnValue('test/url');
    component['createRequest']();
    tick();
    expect(globalLoaderService.showLoader).toHaveBeenCalledTimes(2);
    expect(sportsSurfaceBetsService.saveWithIcon).toHaveBeenCalledWith(
      component.surfaceBet,
      component.imageToUpload.file
    );
    expect(globalLoaderService.hideLoader).toHaveBeenCalledTimes(2);
    expect(component['getUrlToGoEdit']).not.toHaveBeenCalledWith('test/url');
    expect(router.navigate).not.toHaveBeenCalledWith(['test/url']);
  }));

  it('#updateRequest should update existing bet', () => {
    component.actionButtons = {
      extendCollection: jasmine.createSpy('extendCollection')
    };
    component.imageToUpload = {
      file: 'some image'
    } as any;
    component['updateRequest']();
    expect(globalLoaderService.showLoader).toHaveBeenCalledTimes(2);
    expect(apiClientService.sportsSurfaceBets().update).toHaveBeenCalledWith(
      component.surfaceBet
    );
    expect(component.surfaceBet).toEqual(surfaceBetMock);
    expect(component.actionButtons.extendCollection).toHaveBeenCalledWith(surfaceBetMock);
    expect(dialogService.showNotificationDialog).toHaveBeenCalledWith(
      {
        title: 'Surface Bet', message: 'Surface Bet is Updated.',
        closeCallback: jasmine.any(Function)
      }
    );
   
    expect(globalLoaderService.hideLoader).toHaveBeenCalledTimes(2);
  });

  it('#updateRequest should hide loader on error', fakeAsync(() => {
    apiClientService.sportsSurfaceBets().update.and.returnValue(throwError('error'));
    component.actionButtons = {
      extendCollection: jasmine.createSpy('extendCollection')
    };
    component.imageToUpload = {
      file: 'some image'
    } as any;
    component['updateRequest']();
    tick();
    expect(globalLoaderService.showLoader).toHaveBeenCalledTimes(2);
    expect(apiClientService.sportsSurfaceBets().update).toHaveBeenCalledWith(
      component.surfaceBet
    );
    expect(component.actionButtons.extendCollection).not.toHaveBeenCalledWith(surfaceBetMock);
    expect(globalLoaderService.hideLoader).toHaveBeenCalledTimes(2);
  }));

  it('#revert should call #loadInitialData', () => {
    component['loadInitialData'] = jasmine.createSpy('loadInitialData');
    component['revert']();
    expect(component['loadInitialData']).toHaveBeenCalledTimes(1);
  });

  it('#loadInitialData should get surface bet and sports', () => {
    component['setEventAndCategoryIds'] = jasmine.createSpy('setEventAndCategoryIds');
    component['validateSelection'] = jasmine.createSpy('validateSelection');
    component['setupForm'] = jasmine.createSpy('setupForm');
    component['getBreadcrumbs'] = jasmine.createSpy('getBreadcrumbs');
    // component.surfaceBetId = '5c0e4addc9e77c00017ff132';
    component['loadInitialData']();
    component['setupForm']();
    // expect(component.form).toEqual(jasmine.any(FormGroup));
    component['setupForm'] = jasmine.createSpy('setupForm');
     expect(globalLoaderService.showLoader).toHaveBeenCalledTimes(2)
    expect(globalLoaderService.showLoader).toHaveBeenCalledTimes(2);
    expect(sportsSurfaceBetsService.getSportCategories).toHaveBeenCalledTimes(2);
    expect(apiClientService.sportsSurfaceBets().findAllByBrand).toHaveBeenCalledWith('bma');
    expect(component.surfaceBet).toEqual(surfaceBetMock);
    expect(component['validateSelection']).toHaveBeenCalledTimes(0);
    expect(component['setupForm']).toHaveBeenCalledTimes(0);
    expect(component['getBreadcrumbs']).toHaveBeenCalledTimes(0);
    expect(globalLoaderService.hideLoader).toHaveBeenCalledTimes(2);
    component.surfaceBetId = null;
    component.surfaceBet.brand = 'bma';
    component['loadInitialData']();
    expect(component.surfaceBet.brand).toEqual(brandService.brand);
  });

  it('#loadInitialData should hide loader on error', () => {
    component['setEventAndCategoryIds'] = jasmine.createSpy('setEventAndCategoryIds');
    apiClientService.sportsSurfaceBets().findAllByBrand.and.returnValue(throwError({}));
    component['loadInitialData']();
    expect(globalLoaderService.showLoader).toHaveBeenCalledTimes(2);
    expect(component['setEventAndCategoryIds']).not.toHaveBeenCalled();
    expect(globalLoaderService.hideLoader).toHaveBeenCalledTimes(2);
  });

  it('#setEventAndCategoryIds should set categories and events', () => {
    component['setEventAndCategoryIds'](component.surfaceBet);
    expect(component.surfaceBet.categoryIDs).toEqual([108, 55]);
    expect(component.surfaceBet.eventIDs).toEqual(['6']);
  });

  it('#setupForm ', () => {
    component['setupForm']();
    expect(component.form).toEqual(jasmine.any(FormGroup));
  });

  it('#updateEditableFields should update some fields in bet', () => {
    const newBet = _.clone(surfaceBetMock);
    newBet.title = 'testTitle1';
    component['updateEditableFields'](component.surfaceBet, newBet);
    expect(component.surfaceBet.title).toEqual('testTitle1');
  });

  it('#getBreadcrumbs should get breadcrumbs from service', () => {
    const params = { moduleId: 'somemoduleid' };
    component['getBreadcrumbs'](params);
    expect(sportsModulesBreadcrumbsService.getBreadcrubs).toHaveBeenCalledWith(params, {
      customBreadcrumbs: [
        {
          label: 'test1 img1'
        }
      ]
    });
    expect(component.breadcrumbsData).toEqual([
      {
        label: 'test label',
        url: 'test/url/surface-bet'
      }
    ]);
  });

  it('#getUrlToGoEdit should return correct url for edit page', () => {
    expect(component['getUrlToGoEdit']('5c0fdb32c9e77c0001b04a58')).toEqual(
      `sports-pages/sport-categories/57fcfcd9b6aff9ba6c252a2c/sports-module/surface-bets/`
      + `5bf53af4c9e77c0001a533d1/bet/edit/5c0fdb32c9e77c0001b04a58`
    );
    expect(component['getUrlToGoEdit']('5c0fdb32c9e77c0001b04a58')).toEqual(
      `sports-pages/sport-categories/57fcfcd9b6aff9ba6c252a2c/sports-module/surface-bets/`
      + `5bf53af4c9e77c0001a533d1/bet/edit/5c0fdb32c9e77c0001b04a58`
    );
    
    component.sportConfigId = undefined;
    component.hubId = '5c0fdb32c9e77c0001b04a58';
    expect(component['getUrlToGoEdit']('5c0fdb32c9e77c0001b04a58')).toEqual(
      'sports-pages/event-hub/5c0fdb32c9e77c0001b04a58/sports-module/surface-bets/5bf53af4c9e77c0001a533d1/bet/edit/5c0fdb32c9e77c0001b04a58'
       );

    component.sportConfigId = undefined;
    component.hubId = undefined;
    expect(component['getUrlToGoEdit']('5c0fdb32c9e77c0001b04a58')).toEqual(
      'sports-pages/homepage/sports-module/surface-bets/5bf53af4c9e77c0001a533d1/bet/edit/5c0fdb32c9e77c0001b04a58'
    );
  });

  it('#getUrlToGoBack should return correct url to previous page', () => {
    expect(component['getUrlToGoBack']).toEqual(
      'sports-pages/sport-categories/57fcfcd9b6aff9ba6c252a2c/sports-module/surface-bets/5bf53af4c9e77c0001a533d1'
    );
    component.sportConfigId = '55b1123c9e3897a34c02ab06';
    expect(component['getUrlToGoBack']).toEqual(
      `sports-pages/sport-categories/55b1123c9e3897a34c02ab06/sports-module/surface-bets/5bf53af4c9e77c0001a533d1`
    );

    component.sportConfigId = undefined;
    component.hubId = '5c0fdb32c9e77c0001b04a58';
    expect(component['getUrlToGoBack']).toEqual(
      'sports-pages/event-hub/5c0fdb32c9e77c0001b04a58/sports-module/surface-bets/5bf53af4c9e77c0001a533d1'
    );


    component.sportConfigId = undefined;
    component.hubId = undefined;
    expect(component['getUrlToGoBack']).toEqual(
      'sports-pages/homepage/sports-module/surface-bets/5bf53af4c9e77c0001a533d1'
    );
  });

  it('#toggleActiveStatus should toggle disabled status and call #validateSelection', () => {
    component.surfaceBet.disabled = true;
    component.validateSelection = jasmine.createSpy('validateSelection');
    component.toggleActiveStatus();
    expect(component.surfaceBet.disabled).toEqual(false);
    expect(component.validateSelection).toHaveBeenCalledTimes(1);
  });
  
  it('should handle form valid and check validation to true', () => {
    component.form = {
      valid: true
    } as any;
    expect(component.form).toBeDefined();
    component.isSegmentValid = true;
    expect(component.validationHandler()).toBeTruthy();
  });

  it('check validation to true', () => {
    component.form = {
      valid: true
    } as any;
    component.isSegmentValid = false;
    expect(component.validationHandler()).toBeFalsy();
  });

  it('should check if segment is true', () => {
    let flag = true;
     expect(component.isSegmentFormValid).toBeDefined();
    component.isSegmentFormValid(flag);
    expect(component.isSegmentValid).toBe(true);
  })

  it('should check if segment is false', () => {
    let flag = false;
    component.isSegmentFormValid(flag);
    expect(component.isSegmentValid).toBe(false);
  });

  it('# Highlights checkbox should be checked automatically when displayOnDesktop is checked', () => {
    component.surfaceBet.displayOnDesktop = true;
    component.surfaceBet.highlightsTabOn = false;
    component.onDisplayOnDesktopCheck();
    expect(component.surfaceBet.highlightsTabOn).toBeTrue();
  });

  it('# Highlights checkbox should not be checked automatically when displayOnDesktop is not checked', () => {
    component.surfaceBet.displayOnDesktop = false;
    component.surfaceBet.highlightsTabOn = false;
    component.onDisplayOnDesktopCheck();
    expect(component.surfaceBet.highlightsTabOn).toBeFalse();
  });

  it('#should update the surfacebet properties with segment values', () => {
    let obj = {exclusionList:[], inclusionList:['Cricket'], universalSegment:false};
    const surfaceBet = {...component.surfaceBet, ...obj};
    expect(component.modifiedSegmentsHandler).toBeDefined();
    component.modifiedSegmentsHandler(surfaceBet);
    expect(component.surfaceBet).toEqual(surfaceBet);
  });

  it('#should toggle all', async(() => {
    component.ngOnInit();
    fixture.detectChanges();
    fixture.whenStable().then(() => {
      expect(component.allSelected).toEqual(false);
      fixture.whenStable().then(() => {
        expect(component.toggleAllSelection.length).toEqual(0);
      });
    });
  }));
  

  it('#getSurfaceBetTitle should send request to get surfaceBetTitle', fakeAsync(() => {
    component.actionButtons = {
      extendCollection: jasmine.createSpy('extendCollection')
    };
    const mockSurfaceBet = [
      {
          "id": "64d352f09ba03738133f1fe4",
          "createdBy": "5645b8a220bd9e0800afdc57",
          "createdByUserName": null,
          "updatedBy": "5645b8a220bd9e0800afdc57",
          "updatedByUserName": null,
          "createdAt": "2023-08-09T08:48:48.012Z",
          "updatedAt": "2023-08-09T08:48:48.012Z",
          "brand": "bma",
          "title": "Surface Bet Module"
      }
  ]
    apiClientService.sportsSurfaceBets().getSurfaceBetTitle.and.returnValue(of({body :mockSurfaceBet}));
    component['updateEditableFields'] = jasmine.createSpy('updateEditableFields');
    component.surfaceBet.id = '5c0e4addc9e77c00017ff132';
    component['setupForm']();
        expect(component.form).toEqual(jasmine.any(FormGroup));

    component['getSurfaceBetTitle']();
    tick();
    expect(globalLoaderService.showLoader).toHaveBeenCalled();
    expect(apiClientService.sportsSurfaceBets().getSurfaceBetTitle).toHaveBeenCalled();
  }));

  it('#getSurfaceBetTitle should handle error on getting Title', fakeAsync(() => {
    apiClientService.sportsSurfaceBets().getSurfaceBetTitle.and.returnValue(throwError({ body: 'error' }));
    component['updateEditableFields'] = jasmine.createSpy('updateEditableFields');
    component.surfaceBet.id = '5c0e4addc9e77c00017ff132';
    component['getSurfaceBetTitle']();
    tick();
    expect(globalLoaderService.showLoader).toHaveBeenCalled();
    expect(apiClientService.sportsSurfaceBets().getSurfaceBetTitle).toHaveBeenCalled();
  }));

  it('#deleteTitle should call confirmDialog',fakeAsync(() => {
    const event = {
      preventDefault : jasmine.createSpy(),
      stopPropagation : jasmine.createSpy()
    }
    component.deleteTitle(event as any,'64d352f09ba03738133f1fe4');
    tick();
    expect(dialogService.showConfirmDialog).toHaveBeenCalledWith(
      {
        title: 'Do you want to delete the surface bet title?',
        yesCallback: jasmine.any(Function)
      }
    ); 
  }));

  it('#sendRemoveRequest should call getSurfaceBetTitle',fakeAsync(() => {
    component['getSurfaceBetTitle'] = jasmine.createSpy('getSurfaceBetTitle');
        const mockSurfaceBet = [
      {
          "id": "64d352f09ba03738133f1fe4",
          "createdBy": "5645b8a220bd9e0800afdc57",
          "createdByUserName": null,
          "updatedBy": "5645b8a220bd9e0800afdc57",
          "updatedByUserName": null,
          "createdAt": "2023-08-09T08:48:48.012Z",
          "updatedAt": "2023-08-09T08:48:48.012Z",
          "brand": "bma",
          "title": "Surface Bet Module"
      }
  ]
    apiClientService.sportsSurfaceBets().deleteSurfaceBetTitle.and.returnValue(of({body :mockSurfaceBet}));
    component.sendRemoveRequest('64d352f09ba03738133f1fe4');
    tick();

    expect(globalLoaderService.showLoader).toHaveBeenCalled();
    expect(component.getSurfaceBetTitle).toHaveBeenCalled();
    
  }));
   it('#sendRemoveRequest should call hideLoader in case of error thrown',fakeAsync(() => {

    apiClientService.sportsSurfaceBets().deleteSurfaceBetTitle.and.returnValue(throwError('error'));
    component.sendRemoveRequest('64d352f09ba03738133f1fe4');
    tick();

    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
    
  }));

  it('#filterDropDown if value matches',() => {
  component.surfaceBetTitle  = [{
    title : 'test'
  }
  ] as any;
    apiClientService.sportsSurfaceBets().deleteSurfaceBetTitle.and.returnValue(throwError('error'));
    component['filterDropDown']('test');

    expect(component['filterDropDown']).toBeDefined();
    
  });
  it('#filterDropDown if value dont matches',() => {
    component.surfaceBetTitle  = [{
      title : 'abc'
    }
    ] as any;
      apiClientService.sportsSurfaceBets().deleteSurfaceBetTitle.and.returnValue(throwError('error'));
      component['filterDropDown']('test');
  
      expect(component['filterDropDown']).toBeDefined();
});

it('#updateSurfaceBetTitle',() => {
  component.surfaceBetTitle  = [{
    title : 'abc'
  }
  ] as any;
  component.form= {
    get : (title) =>{ return {
        valueChanges : {
            subscribe: jasmine.createSpy().and.callFake(cb => cb(component['filterDropDown(abc)'])),
            pipe : jasmine.createSpy()
        },
    }
}
} as any;
  
    apiClientService.sportsSurfaceBets().deleteSurfaceBetTitle.and.returnValue(throwError('error'));
    component['updateSurfaceBetTitle']();

    expect(component.filteredSurfaceBetTitle).toBeUndefined();
});
it('#toggleDropDown ',() => {
  component.getSurfaceBetTitle = jasmine.createSpy('getSurfaceBetTitle')
    apiClientService.sportsSurfaceBets().deleteSurfaceBetTitle.and.returnValue(throwError('error'));
    component.toggleDropDown();

    expect(component.isDropDownVisible ).toBeFalse();
});

it('#handleOpen ',() => {
    component.handleOpen();

    expect(component.isDropDownVisible ).toBeFalse();
});

it('#handleClosed ',() => {
  component.handleClosed();

  expect(component.isDropDownVisible ).toBeTrue();
});
});
