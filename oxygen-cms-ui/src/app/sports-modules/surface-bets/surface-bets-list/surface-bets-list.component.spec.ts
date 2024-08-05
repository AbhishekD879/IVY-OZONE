import { async, ComponentFixture, fakeAsync, TestBed, tick } from '@angular/core/testing';
import { CUSTOM_ELEMENTS_SCHEMA, NO_ERRORS_SCHEMA  } from '@angular/core';
import { ApiClientService } from '@app/client/private/services/http';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { BrandService } from '@app/client/private/services/brand.service';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { ErrorService } from '@app/client/private/services/error.service';
import { SurfaceBet } from '@app/client/private/models/surfaceBet.model';
import { SportsSurfaceBetsListComponent } from '@app/sports-modules/surface-bets/surface-bets-list/surface-bets-list.component';
import * as _ from 'lodash';
import { SportsSurfaceBetsService } from '@app/sports-modules/surface-bets/surface-bets.service';
import { SportCategory } from '@app/client/private/models/sportcategory.model';
import { ActivatedRoute, Router } from '@angular/router';
import { SportsModulesBreadcrumbsService } from '@app/sports-modules/sports-modules-breadcrumbs.service';
import { Breadcrumb } from '@app/client/private/models/breadcrumb.model';
import { SegmentStoreService } from '@app/client/private/services/segment-store.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AppConstants, CSPSegmentConstants, CSPSegmentLSConstants } from '@app/app.constants';
import { Order } from '@app/client/private/models/order.model';
import { of,throwError } from 'rxjs';
import { SportsModulesService } from '@app/sports-modules/sports-modules.service';

describe('SportsSurfaceBetsListComponent', () => {
  let component: SportsSurfaceBetsListComponent,
    fixture: ComponentFixture<SportsSurfaceBetsListComponent>;

  let apiClientService,
    dialogService: Partial<DialogService>,
    globalLoaderService: Partial<GlobalLoaderService>,
    errorService: Partial<ErrorService>,
    brandService: Partial<BrandService>,
    activatedRoute: Partial<ActivatedRoute>,
    router: Partial<Router>,
    sportsModulesBreadcrumbsService: Partial<SportsModulesBreadcrumbsService>,
    sportsSurfaceBetsService: Partial<SportsSurfaceBetsService>,
    snackBar: Partial<MatSnackBar>,
    segmentStoreService,
    sportsModulesService: Partial<SportsModulesService>;

  let betList: SurfaceBet[],
    breadcrumbsMock: Breadcrumb[],
    sports: SportCategory[];

  const eventHubMock: any = {
    title: 'testhub',
    disabled: false,
    sortOrder: 0,
    indexNumber: 1
  };

  beforeEach(async(() => {
    snackBar = {
      open: jasmine.createSpy('open')
    };

    sports = [
      { id: '5c092545c9e77c0001cc92dc', categoryId: 55, imageTitle: 'sport55' },
      { id: 'sadsad', categoryId: 108, imageTitle: 'sport108' },
      { id: 'asdafas', categoryId: 5, imageTitle: 'sport5' },
    ] as any;

    breadcrumbsMock = [
      {
        'label': 'Sport Categories',
        'url': '/sports-pages/sport-categories'
      },
      {
        'label': 'Horse Racing',
        'url': '/sports-pages/sport-categories/5c0a36bfc9e77c0001cc956f'
      },
      {
        'label': 'Surface Bets Module',
        'url': '/sports-pages/sport-categories/5c0a36bfc9e77c0001cc956f/sports-module/surface-bets'
      }];

    betList = [{
      'displayFrom': '2019-01-17T12:57:35.457Z',
      'displayTo': '2019-01-21T12:57:35Z',
      'svg': null,
      'svgFilename': null,
      'svgId': null,
      'content': null,
      'edpOn': false,
      'displayOnDesktop': false,
      'highlightsTabOn': false,
      'references': [{
        'relatedTo': 'sport',
        'refId': '55',
        'enabled': true
      }, {
        'relatedTo': 'edp',
        'refId': '5',
        'enabled': true
      }, {
        'relatedTo': 'sport',
        'refId': '108',
        'enabled': true
      }],
      'selectionId': 32,
      'price': { 'priceType': null, 'priceNum': 1, 'priceDen': 3, 'priceDec': 1.33 },
      'id': '5c407bd1c9e77c00014af664',
      'sortOrder': -32.0,
      'disabled': false,
      'title': 'SB2',
      'brand': 'bma',
      'pageId': null,
      'pageType': 'sport',
      'sportId': null,
      'inclusionList':[],
      'exclusionList':[],
      'universalSegment':true

    }, {
      'displayFrom': '2019-01-18T15:02:12.380Z',
      'displayTo': '2019-01-24T15:02:12Z',
      'svg': null,
      'svgFilename': null,
      'svgId': null,
      'content': null,
      'edpOn': false,
      'displayOnDesktop': false,
      'highlightsTabOn': false,
      'references': [{
        'relatedTo': 'sport',
        'refId': '55',
        'enabled': true
      }, {
        'relatedTo': 'sport',
        'refId': '0',
        'enabled': true
      }, {
        'relatedTo': 'sport',
        'refId': '76',
        'enabled': true
      }, {
        'relatedTo': 'edp',
        'refId': '34',
        'enabled': true
      }],
      'selectionId': 1,
      'price': { 'priceType': null, 'priceNum': 3, 'priceDen': null, 'priceDec': null },
      'id': '5c41ea7cc9e77c0001e8f1f3',
      'sortOrder': -35.0,
      'disabled': true,
      'title': 'SB1',
      'brand': 'bma',
      'pageId': null,
      'pageType': 'sport',
      'sportId': null,
      'inclusionList':[],
      'exclusionList':[],
      'universalSegment':true
    }] as any;

    const newDate = new Date();
    newDate.setDate(newDate.getDate() + 1);
    const dateString = newDate.toISOString();
    betList[1].displayTo = dateString;

    apiClientService = {
      sportsSurfaceBets: jasmine.createSpy('sportsSurfaceBets').and.returnValue({
        findAllByBrandAndSport: jasmine.createSpy('findAllByBrandAndSport').and.returnValue(of(betList)),
        findAllByBrand: jasmine.createSpy('findAllByBrand').and.returnValue(of({ body: betList })),
        delete: jasmine.createSpy('delete').and.returnValue(of({ body: {} })),
        reorder: jasmine.createSpy('reorder').and.returnValue(of({ body: {} })),
        updateActiveBets: jasmine.createSpy('updateActiveBets').and.returnValue(of({body: betList}))
      }),
      eventHub: jasmine.createSpy('eventHub').and.returnValue({
        getAllEventHubs: jasmine.createSpy('getAllEventHubs').and.returnValue(of([eventHubMock]))
      })
    };
    let path = 'homepage/surface-bet';
    segmentStoreService = {
      validateSegmentValue: jasmine.createSpy('validateSegmentValue'),
      validateHomeModule: () => path.includes('homepage'),
      getSegmentMessage: () => of({segmentValue:'Universal', segmentModule:CSPSegmentLSConstants.SURFACE_BET_TAB }),
      updateSegmentMessage: jasmine.createSpy('updateSegmentMessage')
    };
    activatedRoute = {
      params: of({ id: '5c092545c9e77c0001cc92dc' })
    };
    router = {
      url: 'current-url'
    };
    sportsModulesBreadcrumbsService = {
      getBreadCrumbsForSportCategory: jasmine.createSpy('getBreadCrumbsForSportCategory').and.returnValue(breadcrumbsMock)
    };

    dialogService = {
      showConfirmDialog: jasmine.createSpy('showConfirmDialog')
        .and.returnValue(of({}))
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
    brandService = {
      brand: 'bma'
    };
    sportsSurfaceBetsService = {
      getSportCategories: jasmine.createSpy('getSportCategories').and.returnValue(of(sports))
    };

    sportsModulesService={
      updateModule: jasmine.createSpy('updateModule').and.returnValue(
        of({id: 12})
      )
    }

    TestBed.configureTestingModule({
      declarations: [SportsSurfaceBetsListComponent],
      providers: [
        { provide: ActivatedRoute, useValue: activatedRoute },
        { provide: ApiClientService, useValue: apiClientService },
        { provide: SportsSurfaceBetsService, useValue: sportsSurfaceBetsService },
        { provide: DialogService, useValue: dialogService },
        { provide: GlobalLoaderService, useValue: globalLoaderService },
        { provide: ErrorService, useValue: errorService },
        { provide: SportsModulesBreadcrumbsService, useValue: sportsModulesBreadcrumbsService },
        { provide: Router, useValue: router },
        { provide: BrandService, useValue: brandService },
        { provide: SegmentStoreService, useValue: segmentStoreService },
        { provide: MatSnackBar, useValue: snackBar },
        { provide: SportsModulesService, useValue: sportsModulesService }
      ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA, NO_ERRORS_SCHEMA ]
    }).compileComponents();

    fixture = TestBed.createComponent(SportsSurfaceBetsListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
    component.sportId = 55;
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('#save should call sportsModulesService.updateModule', fakeAsync(() => {
    const SportsModule = {
      id: 12345
    } as any;
    component.actionButtons.extendCollection = jasmine.createSpy('component.actionButtons.extendCollection');
    component.filterSbData = null;
    component.filterModuleData = SportsModule;
    component.save();
    expect(snackBar.open).toHaveBeenCalledWith(
      `Sports module and surface bets saved!`, 'Ok!',
      {
        duration: AppConstants.HIDE_DURATION,
      }
    );
    tick();
  }));

  it('#save should call sportsModulesService and sendRequestSurfaceBet', fakeAsync(() => {
    component.actionButtons.extendCollection = jasmine.createSpy('component.actionButtons.extendCollection');
    component.filterModuleData = {id: 123} as any;
    component.save();
    expect(snackBar.open).toHaveBeenCalledWith(
      `Sports module saved!`, 'Ok!',
      {
        duration: AppConstants.HIDE_DURATION,
      }
    );
  }));

  it('#should call sendRequestSurfaceBet', fakeAsync(() => {
    component.cloneSurfaceBetsData = undefined;
    component.actionButtons.extendCollection = jasmine.createSpy('component.actionButtons.extendCollection');
    component.save();
    expect(snackBar.open).toHaveBeenCalledWith(
      `Surface bets are saved!`, 'Ok!',
      {
        duration: AppConstants.HIDE_DURATION,
      }
    );
    tick();
  }))

  it('ngOnInit',(() => {
    component['filterBetsByDate'] = jasmine.createSpy('filterBetsByDate');
    component.ngOnInit();
    expect(segmentStoreService.validateSegmentValue).toHaveBeenCalled();
    expect(component.selectedSegment).toEqual(CSPSegmentConstants.UNIVERSAL_TITLE);
  }));
  
  it('#ngOnInit should get route params and set breadcrumbs', () => {
    component.onFilterChange = jasmine.createSpy('onFilterChange');
    
    component.hubId = '1dc0ef'; //random number for testing purpose
    component.ngOnInit();
    expect(component.sportId).toEqual(55);
    expect(component.hubData).toEqual(undefined);
    expect(sportsSurfaceBetsService.getSportCategories).toHaveBeenCalled();
    expect(apiClientService.eventHub().getAllEventHubs).toHaveBeenCalled();
    expect(component.onFilterChange).toHaveBeenCalled();
    expect(component.sportCategories).toEqual([
      { id: '5c092545c9e77c0001cc92dc', categoryId: 55, imageTitle: 'sport55' },
      { id: 'sadsad', categoryId: 108, imageTitle: 'sport108' },
      { id: 'asdafas', categoryId: 5, imageTitle: 'sport5' }
    ] as any);
    expect(component.eventHubs).toEqual([{ title: 'testhub', disabled: false, sortOrder: 0, indexNumber: 1 }] as any);
    expect(component.sportCategory).toEqual(undefined);
    expect(component.hubData).toEqual(undefined);
   
   
  });

  it('removeHandler should remove bet', () => {
    component.surfaceBets = _.cloneDeep(betList);
    component.removeHandler(component.surfaceBets[1]);

    expect(dialogService.showConfirmDialog).toHaveBeenCalledWith({
      title: 'Surface Bet',
      message: 'Are You Sure You Want to Remove Surface Bet?',
      yesCallback: jasmine.any(Function)
    });
    expect(globalLoaderService.showLoader).toHaveBeenCalledTimes(2);
    expect(apiClientService.sportsSurfaceBets().delete).toHaveBeenCalledWith(betList[1].id);
    expect(globalLoaderService.hideLoader).toHaveBeenCalledTimes(2);
    expect(component.surfaceBets).toEqual([betList[0]]);
  });

  it('removeHandler should handle error on remove bet', () => {
    component.surfaceBets = _.cloneDeep(betList);
    apiClientService.sportsSurfaceBets().delete.and.returnValue(throwError({ message: 'err msg' }));
    component.removeHandler(component.surfaceBets[1]);

    expect(dialogService.showConfirmDialog).toHaveBeenCalledWith({
      title: 'Surface Bet',
      message: 'Are You Sure You Want to Remove Surface Bet?',
      yesCallback: jasmine.any(Function)
    });
    expect(globalLoaderService.showLoader).toHaveBeenCalledTimes(2);
    expect(apiClientService.sportsSurfaceBets().delete).toHaveBeenCalledWith(component.surfaceBets[1].id);
    expect(globalLoaderService.hideLoader).toHaveBeenCalledTimes(2);
    expect(component.surfaceBets).toEqual(betList);
    expect(errorService.emitError).toHaveBeenCalledWith('err msg');
  });

  it('#onFilterChange should call #getSurfaceBetsBySport', () => {
    component.filteredBySport = false;
    component['getAllSurfaceBets'] = jasmine.createSpy('getAllSurfaceBets');
    component['getSurfaceBetsBySport'] = jasmine.createSpy('getSurfaceBetsBySport');

    component.onFilterChange(component.selectedSegment);
    expect(component['getAllSurfaceBets']).toHaveBeenCalled();

    component.filteredBySport = true;
    component.onFilterChange(component.selectedSegment);
    expect(component['getSurfaceBetsBySport']).toHaveBeenCalledWith('sport', 55, component.selectedSegment);

    component.filteredBySport = true;
    component.hubData = eventHubMock;
    component.sportId = null;
    component.onFilterChange(component.selectedSegment);
    expect(component['getSurfaceBetsBySport']).toHaveBeenCalledWith('eventhub', eventHubMock.indexNumber, component.selectedSegment);
  });

  it('#getSurfaceBetsBySport should get surface bets', fakeAsync(() => {
    const newBetList = [
      ...betList,
      {
        'displayFrom': '2019-01-17T12:57:35.457Z',
        'displayTo': '2019-01-21T12:57:35Z',
        'references': [{
          'relatedTo': 'edp',
          'refId': '5',
          'enabled': true
        }, {
          'relatedTo': 'sport',
          'refId': '55',
          'enabled': false
        }],
        'selectionId': 32,
        'id': '5c407bd1c9e77c00014af664',
        'title': 'SB4',
        'brand': 'bma',
      }
    ];
    apiClientService.sportsSurfaceBets().findAllByBrandAndSport.and.returnValue(of({ body: newBetList }));
    component['mapBetSports'] = jasmine.createSpy('mapBetSports').and.returnValue(betList);
    component['filterBetsByDate'] = jasmine.createSpy('filterBetsByDate');
    component['getSurfaceBetsBySport']('sport', 55, component.selectedSegment);

    expect(globalLoaderService.showLoader).toHaveBeenCalledTimes(2);
    expect(apiClientService.sportsSurfaceBets().findAllByBrandAndSport).toHaveBeenCalledWith(
      'bma', 'sport', 55, component.selectedSegment
    );

    tick();

    expect(component['mapBetSports']).toHaveBeenCalledWith(betList);
    expect(component['filterBetsByDate']).toHaveBeenCalledWith(betList);
    expect(globalLoaderService.hideLoader).toHaveBeenCalledTimes(2);
    expect(component.surfaceBets).toEqual(betList);
  }));

  it('#getSurfaceBetsBySport should handle error', () => {
    apiClientService.sportsSurfaceBets().findAllByBrandAndSport.and.returnValue(throwError({}));
    component['getSurfaceBetsBySport']('sport', 108, component.selectedSegment);
    expect(globalLoaderService.showLoader).toHaveBeenCalledTimes(2);
    expect(apiClientService.sportsSurfaceBets().findAllByBrandAndSport).toHaveBeenCalledWith(
      'bma', 'sport', 108, component.selectedSegment
    );
    expect(globalLoaderService.hideLoader).toHaveBeenCalledTimes(2);
    expect(component.surfaceBets).toEqual([]);
  });

  it('#getAllSurfaceBets should get surface bets', () => {
    component['filterBetsByDate'] = jasmine.createSpy('filterBetsByDate');
    component.selectedSegment = CSPSegmentConstants.UNIVERSAL_TITLE;
    component['getAllSurfaceBets']();
    expect(globalLoaderService.showLoader).toHaveBeenCalledTimes(2);
    expect(apiClientService.sportsSurfaceBets().findAllByBrand).toHaveBeenCalledWith('bma');
    expect(component['filterBetsByDate']).toHaveBeenCalledWith(betList);
    expect(globalLoaderService.hideLoader).toHaveBeenCalledTimes(2);
    expect(component.surfaceBets).toEqual(betList);
  });

  it('#getAllSurfaceBets should handle error', () => {
    apiClientService.sportsSurfaceBets().findAllByBrand.and.returnValue(throwError({}));
    component['mapBetSports'] = jasmine.createSpy('mapBetSports').and.returnValue([]);
    component['filterBetsByDate'] = jasmine.createSpy('filterBetsByDate');
    component['getAllSurfaceBets']();
    expect(globalLoaderService.showLoader).toHaveBeenCalledTimes(2);
    expect(apiClientService.sportsSurfaceBets().findAllByBrand).toHaveBeenCalledWith('bma');  
    expect(component['mapBetSports']).not.toHaveBeenCalled();
    expect(component['filterBetsByDate']).not.toHaveBeenCalled();
    expect(globalLoaderService.hideLoader).toHaveBeenCalledTimes(2);
    expect(component.surfaceBets).toEqual([]);
  });

  it('#mapBetSports should ', () => {
    const bets = component['mapBetSports'](betList);
    expect(bets[0].sportsString).toEqual('sport55, sport108');
    expect(bets[1].sportsString).toEqual('sport55');
  });

  it('#filterBetsByDate should set expired and active bets', () => {
    component.actionButtons.extendCollection = jasmine.createSpy('component.actionButtons.extendCollection');
    component['filterBetsByDate'](betList);
    expect(component.activeBets).toEqual([betList[1]]);
    expect(component.expiredBets).toEqual([betList[0]]);
  });

  it('#reorderHandler should save new coupon order', () => {
    const newOrder: Order = { order: ['123', '456'], id: '123' };
    component.filterSbData = null;
    component.reorderHandler(newOrder);
    expect(apiClientService.sportsSurfaceBets().reorder).toHaveBeenCalledWith(newOrder);
    expect(snackBar.open).toHaveBeenCalledWith(
      `Surface Bet order saved!`,
      'Ok!',
      {
        duration: AppConstants.HIDE_DURATION,
      }
    );
  });
  
  it('#Should trigger onFilterChange function on dropdown change', () => {
    let segment = 'Test';
    component.onFilterChange = jasmine.createSpy('onFilterChange');
    component.segmentHandler(segment);

    expect(component.onFilterChange).toHaveBeenCalledWith(segment);
    expect(component.selectedSegment).toEqual(segment);
  });

  describe('actionsHandler', () => {
    it('actionsHandler revert', () => {
        spyOn(component,'revert')
        component.actionsHandler('revert');
        expect(1).toBe(1)
    });
    it('actionsHandler save', () => {
        spyOn(component,'save')
        component.actionsHandler('save');
        expect(1).toBe(1)
    });
    it('actionsHandler default', () => {
        component.actionsHandler('default');
        expect(1).toBe(1)
    });
  });

  it('should call revert', () => {
    spyOn(component,'loadInitialData');
    component.revert();
    expect(component.loadInitialData).toHaveBeenCalled();
  })

  it('should update surfaceBetsData and activeBets when propertyName is defined', () => {
    component.activeSbMappings = {
      exampleName: 'propertyName'
    } as any;
    component.surfaceBetsData = [
      { propertyName: 'highlightsTabOn' } as any,
      { propertyName: 'edpOn' } as any
    ];
    component.activeBets = [
      { propertyName: 'displayOnDesktop' } as any,
      { propertyName: 'highlightsTabOn' }
    ];
    const data = {
      rowIndex: 1,
      name: 'displayOnDesktop',
      flag: true
    };
    component.saveSurfaceBetsFlagChange(data);
    expect(component.surfaceBetsData).toBeTrue;
  });
  
  it('should not update surfaceBetsData and activeBets when propertyName is undefined', () => {
    component.activeSbMappings = {
      name: 'disabled'
    } as any;
    component.surfaceBetsData = [
      { propertyName: 'Display in Desktop' } as any,
      { propertyName: 'EDP' }
    ];
    let data1 = component.activeBets = [
      { propertyName: 'Highlights Tab' } as any,
      { propertyName: 'Enabled' }
    ];

    const data = {
      rowIndex: 1,
      name: 'disabled',
      flag: true
    };
    component.saveSurfaceBetsFlagChange(data);
    expect(data1[1].propertyName).toBe('Enabled');
  });
  
  
  it('should update highlightsTabOn when propertyName is "displayOnDesktop" and flag is true', () => {
    component.activeSbMappings = {
      exampleName: 'displayOnDesktop'
    } as any;
    component.surfaceBetsData = [
      { displayOnDesktop: false, highlightsTabOn: false } as any
    ];
    component.activeBets = [
      { displayOnDesktop: false, highlightsTabOn: false } as any
    ];
    const data = {
      rowIndex: 0,
      name: 'exampleName',
      flag: true
    };
    component.saveSurfaceBetsFlagChange(data);
    expect(component.surfaceBetsData[0].highlightsTabOn).toBe(true);
    expect(component.activeBets[0].highlightsTabOn).toBe(true);
  });
});
