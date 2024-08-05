import { of as observableOf } from 'rxjs/observable/of';
import { InplayModuleComponent } from '@app/sports-modules/inplay-module/module-page/inplay-module.component';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AppConstants } from '@app/app.constants';
import { SportsModule } from '@app/client/private/models/homepage.model';
import { Observable, of, throwError } from 'rxjs';
import { CONTESTS } from '@root/app/five-a-side-showdown/components/contest-manager/contests.mock';
import { HomeInplayModule } from '@root/app/client/private/models/inplaySportModule.model';
import { Order } from '@app/client/private/models/order.model';
import { Params } from '@angular/router';
import { ISegmentMsg } from '@root/app/client/private/models/segment.model';


const inplaySportMock: HomeInplayModule = {
  id: '123',
  eventCount: 1,
  categoryId: '123',
  tier: 'UNITED',
  sportName: 'Cricket',
  brand: 'bma',
  updatedBy: null,
  updatedAt: null,
  createdBy: null,
  createdAt: null,
  updatedByUserName: null,
  createdByUserName: null,
  inclusionList: [],
  exclusionList: [],
  universalSegment: true
};

const segmentMsgMock: ISegmentMsg = {
  segmentModule: 'inplay-sport',
  segmentValue: 'Cricket'
};

describe('InplayModuleComponent', () => {
  let component,
    activatedRoute,
    sportsModulesService,
    sportsModulesBreadcrumbsService,
    snackBar: MatSnackBar,
    dialogService,
    brandService,
    globalLoaderService,
    segmentStoreService,
    errorService;

  beforeEach(() => {
    activatedRoute = {
      params: Observable.of({
        linkId: '57fcfcd9b6aff9ba6c252a2c',
        moduleId: '5beee1bbc9e77c0001fb69e3'
      })
    };

    sportsModulesService = {
      deleteSportById: jasmine.createSpy('deleteSportById').and.returnValue(observableOf({})),
      getSingleModuleData: jasmine.createSpy('getSingleModuleData').and.returnValue(observableOf({})),
      inplaySportsReorder: jasmine.createSpy('inplaySportsReorder').and.returnValue(observableOf({})),
      getInplaySportsBySegment: jasmine.createSpy('getInplaySportsBySegment').and.returnValue(observableOf(inplaySportMock)),
      updateModule: jasmine.createSpy('updateModule').and.returnValue(observableOf({ id: 'new_module_id' }))
    } as any;

    sportsModulesBreadcrumbsService = {
      getBreadcrubs: jasmine.createSpy('getBreadcrubs')
          .and.returnValue(Observable.of([{
              label: 'test label',
              url: 'test/url/inplay'
          }]))
    };

    snackBar = {
      open: jasmine.createSpy('open')
    } as any;

    errorService = {
      emitError: jasmine.createSpy('emitError')
    };

    dialogService = {
      showConfirmDialog: jasmine.createSpy()
        .and.returnValue(Observable.of({}))
        .and.callFake(({ title, message, yesCallback }) => {
          yesCallback();
        }),
      showCustomDialog: jasmine.createSpy('showCustomDialog').and
        .callFake((AddContestComponent, { width, title, yesOption, noOption, yesCallback }) =>
          yesCallback(CONTESTS[0]))
    };

    brandService = {
      brand: 'bma'
    };

    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };

    let path = 'homepage/sports-module/inplay';

    segmentStoreService = {
      validateSegmentValue: jasmine.createSpy('validateSegmentValue'),
      validateHomeModule: () => path.includes('homepage'),
      getSegmentMessage: jasmine.createSpy('getSegmentMessage').and.returnValue(of(segmentMsgMock)),
      updateSegmentMessage: jasmine.createSpy('updateSegmentMessage')
    };


    component = new InplayModuleComponent(activatedRoute, sportsModulesService, sportsModulesBreadcrumbsService, snackBar, dialogService,
      brandService, globalLoaderService, segmentStoreService, errorService);
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('on onInit', () => {
    activatedRoute.params = of({
      linkId: '57fcfcd9b6aff9ba6c252a2c',
      moduleId: '5beee1bbc9e77c0001fb69e3'
    } as Params);
    
    activatedRoute.params.subscribe((params) => {
      component.ngOnInit();
      expect(component.routeParams).toEqual({
        linkId: '57fcfcd9b6aff9ba6c252a2c',
        moduleId: '5beee1bbc9e77c0001fb69e3'
      });

      expect(component['loadInitialData']).toHaveBeenCalled();
      expect(segmentStoreService.validateSegmentValue).toHaveBeenCalled();
      expect(segmentStoreService.getSegmentMessage).toHaveBeenCalled();
      expect(component.selectedSegment).toEqual('Universal');
      expect(sportsModulesService.getInplaySportsBySegment).toHaveBeenCalledWith('Universal', 'bma');
      expect(component.inplaySportsList).toEqual(inplaySportMock);
    });
  })

  it('#actionsHandler should save module', () => {
    component.actionButtons = {
      extendCollection: jasmine.createSpy('extendCollection')
    };
    component.module = {
      id: 'module_id'
    };
    component.actionsHandler('save');
    expect(sportsModulesService.updateModule).toHaveBeenCalledWith({ id: 'module_id' } as SportsModule);
    expect(component.module).toEqual({ id: 'new_module_id' });
    expect(component.actionButtons.extendCollection).toHaveBeenCalledWith({ id: 'new_module_id' });
    expect(snackBar.open).toHaveBeenCalledWith(
      `Sports module saved!`, 'Ok!', {
      duration: AppConstants.HIDE_DURATION,
    }
    );
  });

  it('validate if page is homepage module', () => {
    component.module = { sportId: 0} as any;
    expect(component.isHomePageModule()).toBeTruthy();

    component.module = { sportId: 1} as any;
    expect(component.isHomePageModule()).toBeFalsy();
  })

  it('#createSportConfigRow ', () => {
    component.createSportConfigRow();
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
    expect(segmentStoreService.updateSegmentMessage).toHaveBeenCalled();

  });

  it('#reorderHandler ', () => {
    const orderMck: Order = {
      order: ['1', '11'],
      id: '213',
      segmentName: 'INPLAY'
    }
    component.reorderHandler(orderMck);
    expect(sportsModulesService
      .inplaySportsReorder).toHaveBeenCalled();
    expect(snackBar.open).toHaveBeenCalled();
  });

  it('#removeHandler ', () => {

    component.removeHandler(inplaySportMock);
    expect(sportsModulesService.deleteSportById).toHaveBeenCalled();
  });

  it('#removeHandler with error scenrio', () => {
    sportsModulesService.deleteSportById =
      jasmine.createSpy().and.returnValue(throwError({ error: '401' }));


    component.removeHandler(inplaySportMock);
    expect(errorService.emitError).toHaveBeenCalled();
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
  });

  it('#validate segmentHandler', () => {
    const segment = 'Universal';
    component.segmentHandler(segment);
    expect(component.segmentChanged).toBeTrue();
    expect(segmentStoreService.updateSegmentMessage).toHaveBeenCalledWith({segmentModule: 'inplay-sports-module', segmentValue: segment});
    expect(globalLoaderService.showLoader).toHaveBeenCalled();

    expect(sportsModulesService.getInplaySportsBySegment).toHaveBeenCalledWith('Universal', 'bma');
    expect(component.inplaySportsList).toEqual(inplaySportMock);
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
  })

  it('#validate error segmentHandler', () => {
    sportsModulesService.getInplaySportsBySegment.and.returnValue(Observable.throwError({ message: 'err msg' }));
    const segment = 'Uni';
    component.selectedSegment = 'Uni';
    component.segmentHandler(segment);
    expect(component.segmentChanged).toBeTrue();
    expect(segmentStoreService.updateSegmentMessage).toHaveBeenCalledWith({segmentModule: 'inplay-sports-module', segmentValue: segment});
    expect(globalLoaderService.showLoader).toHaveBeenCalled();

    expect(sportsModulesService.getInplaySportsBySegment).toHaveBeenCalledWith('Uni', 'bma');
    expect(component.inplaySportsList).not.toEqual(inplaySportMock);
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
  })
});
