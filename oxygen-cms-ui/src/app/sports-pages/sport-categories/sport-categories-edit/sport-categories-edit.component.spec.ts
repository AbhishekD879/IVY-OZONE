import { of as observableOf } from 'rxjs/observable/of';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/observable/throw';
import { SportCategoriesEditComponent } from './sport-categories-edit.component';
import { SportCategory } from '@app/client/private/models';
import { SportsModule } from '@app/client/private/models/homepage.model';
import { SportTab } from '@app/client/private/models/sporttab.model';
import { throwError } from 'rxjs';
import { CUSTOM_ELEMENTS_SCHEMA, NO_ERRORS_SCHEMA } from '@angular/core';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router, ActivatedRoute } from '@angular/router';
import { ApiClientService } from '@app/client/private/services/http';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { SportsModulesService } from '@app/sports-modules/sports-modules.service';
import { BrandService } from '@app/client/private/services/brand.service';
import { MatDialogModule } from '@angular/material/dialog';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { BrowserDynamicTestingModule } from '@angular/platform-browser-dynamic/testing';
import { ConfirmDialogComponent } from '@app/shared/dialog/confirm-dialog/confirm-dialog.component';
import { NotificationDialogComponent } from '@app/shared/dialog/notification-dialog/notification-dialog.component';

describe('SportCategoriesEditComponent', () => {
  let component: SportCategoriesEditComponent;
  let globalLoaderService, apiClientService, dialogService, sportsModulesService, brandService, sportCategoryService;
  let router, activatedRoute;
  let snackBar;
  let fixture: ComponentFixture<SportCategoriesEditComponent>;

  const modules: SportsModule[] = [
    {
      id: '5',
      brand: 'bma',
      identifier: ' ',
      moduleType: ' ',
      title: ' ',
      href: ' ',
      enabled: true,
      disabled: false,
      sportId: 1,    // deprecated
      pageType: ' ', // "sport" or "eventhub"
      pageId: ' ',   // sport id or eventhubIndex
      sortOrder: 1,
      publishedDevices: []
    }
  ] as any;
  const sportCategorymockData: SportCategory =
  {
    "alt": "",
    "brand": "bma",
    "categoryId": 1234,
    "messageLabel" : "Non runner message",
    "collectionType": "",
    "createdAt": "2021-10-13T13:09:06.228Z",
    "createdBy": "5645b8a220bd9e0800afdc57",
    "createdByUserName": null,
    "disabled": false,
    "dispSortNames": "",
    "filename": { "filename": "", "originalfilename": "", "path": "", "size": 0, "filetype": "" },
    "heightLarge": 0,
    "heightLargeIcon": 0,
    "heightMedium": 0,
    "heightMediumIcon": 0,
    "heightSmall": 0,
    "heightSmallIcon": 0,
    "icon": { "filename": "", "originalfilename": "", "path": "", "size": 0, "filetype": "" },
    "id": "6166da7270fc3a656dd04e0a",
    "imageTitle": "FZ",
    "inApp": true,
    "inplayEnabled": false,
    "isTopSport": false,
    "key": "",
    "lang": "",
    "link": "",
    "multiTemplateSport": false,
    "oddsCardHeaderType": null,
    "outrightSport": true,
    "path": "",
    "primaryMarkets": "",
    "scoreBoardUri": "",
    "showInAZ": false,
    "showInHome": false,
    "showInMenu": false,
    "showInPlay": false,
    "showScoreboard": false,
    "sortOrder": 0,
    "spriteClass": "",
    "ssCategoryCode": "1234",
    "svg": "",
    "svgFilename": { "filename": "", "originalfilename": "", "path": "", "size": 0, "filetype": "" },
    "svgId": "",
    "targetUri": "sport/ee",
    "tier": "TIER_2",
    "typeIds": null,
    "updatedAt": "2021-12-22T00:00:12.862Z",
    "updatedBy": "5645b8a220bd9e0800afdc57",
    "updatedByUserName": null,
    "uriLarge": "",
    "uriMedium": "",
    "uriMediumIcon": "",
    "uriSmall": "",
    "uriSmallIcon": "",
    "widthLarge": 0,
    "widthLargeIcon": 0,
    "widthMedium": 0,
    "widthMediumIcon": 0,
    "widthSmall": 0,
    "widthSmallIcon": 0,
    "highlightCarouselEnabled": false,
    "quickLinkEnabled": false,
    "inplaySportModule": { enabled: false, inplayCount: 10 },
    isRealSport() { return true; }
  } as any;

  const sportsTabMockData: SportTab[] = [{

    brand: 'bma',
    sportId: 1,
    name: 'Cricket',
    displayName: 'Cricket',
    enabled: true,
    href:'test',
    checkEvents: true,
    id: '111', createdBy: '', createdAt: '', updatedBy: '', updatedAt: '11', updatedByUserName: '', createdByUserName: ''
  }]

  beforeEach(async(() => {
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };
    sportCategoryService = {
      findOne: jasmine.createSpy('findOne').and.returnValue(observableOf({ body: sportCategorymockData })),
      update: jasmine.createSpy('update').and.returnValue(observableOf({ body: sportCategorymockData })),
      delete: jasmine.createSpy('delete').and.returnValue(observableOf({})),
      uploadImage: jasmine.createSpy('uploadImage').and.returnValue(observableOf({ body: sportCategorymockData })),
      removeImage: jasmine.createSpy('removeImage').and.returnValue(observableOf({ body: sportCategorymockData })),
      uploadIcon: jasmine.createSpy('uploadIcon').and.returnValue(observableOf({ body: sportCategorymockData })),
      removeIcon: jasmine.createSpy('removeIcon').and.returnValue(observableOf({ body: sportCategorymockData })),
      uploadSvg: jasmine.createSpy('uploadSvg').and.returnValue(observableOf({ body: sportCategorymockData })),
      removeSvg: jasmine.createSpy('removeSvg').and.returnValue(observableOf({ body: sportCategorymockData })),
    };

    apiClientService = {
      sportCategory: () => sportCategoryService,

      sportTabService: jasmine.createSpy('sportTabService').and.returnValue({
        findAllByBrandAndSportId: jasmine.createSpy('findAllByBrandAndSportId').and.returnValue(observableOf({ body: sportsTabMockData }))

      })
    };
    dialogService = {
      showNotificationDialog: jasmine.createSpy('showNotificationDialog')
    };
    sportsModulesService = {
      getModulesData: jasmine.createSpy('getModulesData').and.returnValue(observableOf(modules)),
      updateModulesOrder: jasmine.createSpy('updateModulesOrder')
    };
    router = jasmine.createSpyObj('routerSpy', ['navigate']);

    activatedRoute = {
      params: observableOf({ id: 1 }),
      queryParams: observableOf({ expanded: true })
    };

    snackBar = {
      open: jasmine.createSpy('open').and.callThrough()
    };
    brandService = {
      isIMActive: jasmine.createSpy('isIMActive').and.returnValue(false)
    };


    TestBed.configureTestingModule({
      declarations: [SportCategoriesEditComponent, NotificationDialogComponent, ConfirmDialogComponent],
      imports: [
        MatDialogModule,
        BrowserAnimationsModule
      ],
      providers: [
        { provide: ApiClientService, useValue: apiClientService },
        { provide: DialogService, useValue: dialogService },
        { provide: GlobalLoaderService, useValue: globalLoaderService },
        { provide: Router, useValue: router },
        { provide: SportsModulesService, useValue: sportsModulesService },
        { provide: MatSnackBar, useValue: snackBar },
        { provide: BrandService, useValue: brandService },
        { provide: ActivatedRoute, useValue: activatedRoute }
      ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA, NO_ERRORS_SCHEMA ],

    })
    .overrideModule(BrowserDynamicTestingModule, {
      set: {
          entryComponents: [NotificationDialogComponent, ConfirmDialogComponent],
      }
  }).compileComponents();

    fixture = TestBed.createComponent(SportCategoriesEditComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();

    component.form = <any>{
      value: {
        categoryId: 90,
        disabled: false
      }
    };
    component.sportCategory = sportCategorymockData;

  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('ngoninit', () => {
    component.sportCategory = sportCategorymockData;
    component.form = {
      value: {},
      valueChanges: {
        subscribe: jasmine.createSpy().and.callFake(cb => cb({
          svgId: 1, categoryId: 90,
          disabled: false
        })),
        unsubscribe: jasmine.createSpy()
      }
    } as any;
    component.ngOnInit();
    expect(component['expandGeneralSettings']).toBeTruthy();
    expect(component).toBeTruthy();
  });

  it('ngoninit sportCategory empty', () => {
    component.sportCategory = sportCategorymockData;
    component.sportTabData = [];
    component.sportCategory.categoryId=null;
    component.form = {
      value: {},
      valueChanges: {
        subscribe: jasmine.createSpy().and.callFake(cb => cb({
          svgId: 1, categoryId: 90,
          disabled: false
        })),
        unsubscribe: jasmine.createSpy()
      }
    } as any;
    component.ngOnInit();
    expect(component['expandGeneralSettings']).toBeTruthy();
    expect(component).toBeTruthy();
    expect(component.sportTabData).toEqual([]);
    expect(component.sportCategory.categoryId).toEqual(null);
  });

  it('loadInitData error scenario', () => {
    component.form = {
      value: {
        subscribe: jasmine.createSpy().and.callFake(cb => cb({
          svgId: 1, categoryId: 90,
          disabled: false
        }))
      },
      valueChanges: {
        subscribe: jasmine.createSpy().and.callFake(cb => cb({
          svgId: 1, categoryId: 90,
          disabled: false
        })),
        unsubscribe: jasmine.createSpy()
      }
    } as any;

    sportCategoryService.findOne.and.returnValue(throwError({ error: '401', message: ''}));
    component.loadInitData();
    expect(component['expandGeneralSettings']).toBeTruthy();
    expect(component).toBeTruthy();
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
  });

  it('should uploadImageHandler', () => {
    const event = '';
    sportCategoryService['uploadImage'] = { bind: jasmine.createSpy('bind').and.returnValue(()=>observableOf({ body: sportCategorymockData }))}
    component.uploadImageHandler(event);
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
    expect(sportCategoryService['uploadImage'].bind).toHaveBeenCalled();
  });


  it('should removeImageHandler', () => {
    sportCategoryService['removeImage'] = { bind: jasmine.createSpy().and.returnValue(()=>observableOf({ body: sportCategorymockData }))}
    component.removeImageHandler();
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
    expect(sportCategoryService['removeImage'].bind).toHaveBeenCalled();
  });


  it('should check uploadIconHandler', () => {
    sportCategoryService['uploadIcon'] = { bind: jasmine.createSpy().and.returnValue(()=>observableOf({ body: sportCategorymockData }))}
    const event = '';
    component.uploadIconHandler(event);
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
    expect(sportCategoryService['uploadIcon'].bind).toHaveBeenCalled();
  });


  it('should check removeIconHandler', () => {
    sportCategoryService['removeIcon'] = { bind: jasmine.createSpy().and.returnValue(()=>observableOf({ body: sportCategorymockData }))}
    component.removeIconHandler();
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
    expect(sportCategoryService['removeIcon'].bind).toHaveBeenCalled();
  });
  it('should check uploadSvgHandler', () => {
    const event = '';
    sportCategoryService['uploadSvg'] = { bind: jasmine.createSpy().and.returnValue(()=>observableOf({ body: sportCategorymockData }))}
    component.uploadSvgHandler(event);
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
    expect(sportCategoryService['uploadSvg'].bind).toHaveBeenCalled();
  });

  it('should check removeSvgHandler', () => {
    sportCategoryService['removeSvg'] = { bind: jasmine.createSpy().and.returnValue(()=>observableOf({ body: sportCategorymockData }))}
    component.removeSvgHandler();
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
    expect(sportCategoryService['removeSvg'].bind).toHaveBeenCalled();
  });

  it('should save data', () => {
    component.actionButtons = {
      extendCollection: jasmine.createSpy('extendCollection')
    } as any;
    component.actionsHandler({ event: 'save' });
    component.actionsHandler('save');
    expect(sportCategoryService.update).toHaveBeenCalled();
    expect(component.actionButtons.extendCollection).toHaveBeenCalled();
    expect(component.initialFormState).toEqual({...component.form.value});
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
  });

  it('should return error message', () => {
    sportCategoryService.update.and.returnValue(throwError({ error: '401' }));

    component.actionsHandler({ event: 'save' })

    expect(component.sportCategory).toEqual(component.sportCategory);
    expect(dialogService.showNotificationDialog).not.toHaveBeenCalled();
  });

  it('should revert data', () => {

    const event = 'revert';
    component.actionsHandler(event);
    expect(component['sportCategoryService'].findOne).toHaveBeenCalled();
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
  });

  it('should return delete error message', () => {
    apiClientService.sportCategory().delete.and.returnValue(Observable.throw({
      error: {
        message: 'error'
      }
    }));
    const event = 'remove';
    component.actionsHandler(event);
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
    expect(component.sportCategory).toEqual(component.sportCategory);
    expect(dialogService.showNotificationDialog).not.toHaveBeenCalled();
  });
  it('should delete data', () => {
    const event = 'remove';
    component.actionsHandler(event);
    expect(component['sportCategoryService'].delete).toHaveBeenCalledWith(component.sportCategory.id);
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
    component['actionsHandler']('');
  });

});
