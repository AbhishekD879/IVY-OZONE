import { SportCategoriesListComponent } from './sport-categories-list.component';
import {  Observable, of, throwError } from 'rxjs';
import { CONTESTS } from '@app/five-a-side-showdown/components/contest-manager/contests.mock';
import { SportCategory } from '@app/client/private/models';
import { CUSTOM_ELEMENTS_SCHEMA, NO_ERRORS_SCHEMA } from '@angular/core';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { ApiClientService } from '@app/client/private/services/http';
import { SegmentStoreService } from '@app/client/private/services/segment-store.service';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import * as _ from 'lodash';


describe('SportCategoriesListComponent', () => {
 let component: SportCategoriesListComponent;
  let apiClientService,sportCategoryService, dialogService, globalLoaderService, snackBar, segmentStoreService, router;
  let fixture: ComponentFixture<SportCategoriesListComponent>;
  let segments,sportCategorymockData: SportCategory[];


  beforeEach(async(() => {

     segments = [{ "name": "Universal" }, { "name": "CSP_LA_GA_AL_AS_NL_A3_RE_AL_CA_EM_20210920_ALL" }, { "name": "CSP_LA_SP_AS_AS_CR_A1_RE_AL_MA_PS_20210920_ACC" }, { "name": "CSP_Lads" }, { "name": "CSP_LADS_SPORTS_FOOTBALL_20210923_ALL" }, { "name": "CSP_LADS_SPORTS_HR_20210923_ALL" }, { "name": "CSP_LB_TST_1" }, { "name": "CSP_LD_Lewtest" }, { "name": "CSP_LD_Segment-1" }, { "name": "cspseg" }, { "name": "Hyd_Test_Madhu_LD_369" }, { "name": "Lads_CSP_FooterMenu_1" }, { "name": "Lads_CSP_SuperButton_1" }, { "name": "testcsp" }, { "name": "testSegment" }, { "name": "testSegment2" }];
     sportCategorymockData = [{
      "alt": "",
      "brand": "bma",
      "categoryId": 1234,
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
      "inplaySportModule": null,
      isRealSport() { return false; }
    }] as any;
    router = {

      navigate: jasmine.createSpy('navigate'),
      url: '/sports-pages/sport-categories/6166da7270fc3a656dd04e0a'
    };
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };
    
    sportCategoryService = {
      update: jasmine.createSpy('update').and.returnValue(Observable.of({ body: sportCategorymockData })),
      getSportCategory: jasmine.createSpy('getSportCategory').and.returnValue(of(sportCategorymockData)),
      findAllByBrand: jasmine.createSpy('findAllByBrand').and.returnValue(of({ body: sportCategorymockData })),
      delete: jasmine.createSpy('delete').and.returnValue(Observable.of({})),
      save: jasmine.createSpy('save').and.returnValue(of({ body: sportCategorymockData[0] })),
      reorder: jasmine.createSpy('reorder').and.returnValue(of({ body: sportCategorymockData })) };

    apiClientService = {
      sportCategory: () => sportCategoryService,
      sportCategoryService: jasmine.createSpy('sportCategoryService').and.returnValue({ getSportCategory: jasmine.createSpy('getSportCategory').and.returnValue(of(sportCategorymockData)) }),
      segmentMethods: jasmine.createSpy('segmentMethods').and.returnValue({ getSegments: jasmine.createSpy('getSegments').and.returnValue(of(segments)) }),

    };
    dialogService = {
      showConfirmDialog: jasmine.createSpy('showConfirmDialog').and
        .callFake(({ title, message, yesCallback }) => yesCallback()),
      showCustomDialog: jasmine.createSpy('showCustomDialog').and
        .callFake((AddContestComponent, { width, title, yesOption, noOption, yesCallback }) =>
          yesCallback(CONTESTS[0]))
    };
    snackBar = {
      open: jasmine.createSpy('open').and.callThrough()
    };
    segmentStoreService={
      updateSegmentMessage: jasmine.createSpy('updateSegmentMessage')
    }

    TestBed.configureTestingModule({
      declarations: [SportCategoriesListComponent],
      providers: [
        { provide: ApiClientService, useValue: apiClientService },
        { provide: DialogService, useValue: dialogService },
        { provide: GlobalLoaderService, useValue: globalLoaderService },
        { provide: Router, useValue: router },
        { provide: SegmentStoreService, useValue: segmentStoreService },
        { provide: MatSnackBar, useValue: snackBar },
      ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA, NO_ERRORS_SCHEMA ]
    }).compileComponents();

    fixture = TestBed.createComponent(SportCategoriesListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
    component.sportsCategoryFlag = true;
    component.sportCategories = sportCategorymockData;
    
    component.dataTableColumns = [
      {
        'name': 'Name',
        'property': 'imageTitle',
        'link': {
          hrefProperty: 'id'
        },
        'type': 'link'
      },
      {
        'name': 'Tier',
        'property': 'tier'
      }
    ];

  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('ngOnInit error scenario', () => {
    apiClientService.sportCategory().findAllByBrand.and.returnValue(throwError({ error: '401' }));
    component.ngOnInit();
    expect(globalLoaderService.showLoader).toHaveBeenCalled();
  });

  it('create SportCategory', () => {
    apiClientService.sportCategory().save.and.returnValue(of({ body: sportCategorymockData[0] }))
    component.createSportCategory();
      expect(dialogService.showCustomDialog).toHaveBeenCalled();
  });

  it('create SportCategory error scenario', () => {
    apiClientService.sportCategory().save.and.returnValue(throwError({ error: '401' ,message:''}));
    component.createSportCategory();
    expect(dialogService.showCustomDialog).toHaveBeenCalled();
  });

  it('reorder Handler SportCategory', () => {
    apiClientService.sportCategory().reorder.and.returnValue(of({ }));
    const newOrder = { order: ["test"], "id": "test" };
    component.reorderHandler(newOrder);
    expect(apiClientService
      .sportCategory()
      .reorder).toHaveBeenCalled();
      expect(snackBar.open).toHaveBeenCalled();
  });

  it('remove Handler SportCategory', () => {
    apiClientService.sportCategory().delete.and.returnValue(of({ }));
    component.removeHandler(sportCategorymockData[0]);
    expect(apiClientService.sportCategory()
      .delete).toHaveBeenCalled();
  });

  it('Segment Handler SportCategory', () => {
    component['onFilterChange'] = jasmine.createSpy('onFilterChange');
    apiClientService.sportCategory().findAllByBrand.and.returnValue(of({ body: sportCategorymockData }));
    component.segmentHandler('UNIVERSAL');
    expect(segmentStoreService.updateSegmentMessage).toHaveBeenCalled();
  });

  
  it('saveSportsRibbonFlagChange', () => {
    component.sportCategories = sportCategorymockData;
    component.saveSportsRibbonFlagChange({sportsRibbonFlag:false,rowIndex:0});
    expect(sportCategoryService
      .update).toHaveBeenCalled();
  });

  it('sports category and show on', () => {
    apiClientService.sportCategory().findAllByBrand.and.returnValue(of({ body: sportCategorymockData }));
    apiClientService.sportCategoryService().getSportCategory.and.returnValue(of({ body: sportCategorymockData }));
    component.sportsCategoryFlag = true;
    component.onFilterChange('Universal');
    component.sportsCategoryFlag = false;
    component.onFilterChange('Universal');
    expect(globalLoaderService.showLoader).toHaveBeenCalled();
    expect(apiClientService.sportCategoryService().getSportCategory).toHaveBeenCalled();
  });

  it('sports category and show on error scenario', () => {
    component.sportCategories = sportCategorymockData;
    apiClientService.sportCategoryService().getSportCategory.and.returnValue(throwError({ error: '401' }));
    component.sportsCategoryFlag = true;
    component.onFilterChange('Universal');
    component.sportsCategoryFlag = false;
    component.onFilterChange('Universal');
    expect(globalLoaderService.showLoader).toHaveBeenCalled();
    expect(apiClientService.sportCategoryService().getSportCategory).toHaveBeenCalled();
  });

});
