import {  RecentlyPlayedGamesModulePageComponent } from './recently-played-games-module-page.component';
import { Params } from '@angular/router';
import { Observable } from 'rxjs/Observable';
import {IRpgConfigModel} from '@app/client/private/models/rpgConfig.model';


describe('RecentlyPlayedGamesModulePageComponent', () => {
  let component: RecentlyPlayedGamesModulePageComponent;

  const routeParams: Params = {
    'id': '1',
    'moduleId': '2',
  };
  const rpgConfig: IRpgConfigModel = {
    title : 'Recently Played Games',
    seeMoreLink: 'show more',
    gamesAmount: 3,
    bundleUrl: 'http://bundle.com',
    loaderUrl: 'http://loaderUrl.com'
  };
  const moduleData = {
    rpgConfig
  } as any;
  const activatedRoute: any = {
     params: Observable.of(routeParams)
  };
  const sportsModulesService: any = {
    updateModule : jasmine.createSpy('sportsModulesService.updateModule').and.returnValue(Observable.of(moduleData))
  };
  const sportsModulesBreadcrumbsService: any = {
    getBreadcrubs: jasmine.createSpy('sportsModulesBreadcrumbsService.getBreadcrubs').and.returnValue(Observable.of({
      label : 'Test breadcrumb',
      url : 'breadcrumbs-test'
    }))
  };
  const snackBar: any = {
    open: jasmine.createSpy('snackBar.open')
  };

  beforeEach(() => {
    component = new RecentlyPlayedGamesModulePageComponent(
      activatedRoute,
      sportsModulesService,
      sportsModulesBreadcrumbsService,
      snackBar
    );

    component.actionButtons = {
      extendCollection: jasmine.createSpy('actionButtons.extendCollection')
    };
  });

  it('#constructor', () => {
    expect(component).toBeTruthy();
  });

  it('#ngOnInit', () => {
    component['loadInitialData'] = jasmine.createSpy('loadInitialData');
    component.ngOnInit();

    expect(component.routeParams).toEqual(routeParams);
    expect(component['loadInitialData']).toHaveBeenCalledWith(routeParams);
  });

  it('#loadInitialData with rpgConfig', () => {
    sportsModulesService.getSingleModuleData = jasmine.createSpy('sportsModulesService.getSingleModuleData').and.returnValue(Observable.of([
      moduleData, {}
    ]));
    component.setUpForm = jasmine.createSpy('setUpForm');
    component.loadInitialData(routeParams);

    expect(sportsModulesService.getSingleModuleData).toHaveBeenCalledWith(routeParams.moduleId, routeParams.id);
    expect(component.setUpForm).toHaveBeenCalled();
    expect(component.module).toEqual({ rpgConfig } as any);
    expect(component.module.rpgConfig).toEqual(jasmine.objectContaining({
      title : 'Recently Played Games',
      seeMoreLink: 'show more',
      gamesAmount: 3,
    }) as any);
    expect(sportsModulesBreadcrumbsService.getBreadcrubs).toHaveBeenCalledWith(routeParams, { module : component.module});
    expect(component.breadcrumbsData).toEqual({
      label : 'Test breadcrumb',
      url : 'breadcrumbs-test'
    } as any);
  });

  it('#loadInitialData without rpgConfig', () => {
    sportsModulesService.getSingleModuleData = jasmine.createSpy('sportsModulesService.getSingleModuleData').and.returnValue(Observable.of([
      {
        rpgConfig : null
      },
      {}
    ]));
    component.loadInitialData(routeParams);
    expect(component.module.rpgConfig).toEqual({} as any);
  });

  it('#isValidModule', () => {
    component.form = { valid: true } as any;
    expect(component.isValidModule()).toBeTruthy();

    component.form = { valid: false } as any;
    expect(component.isValidModule()).toBeFalsy();
  });

  it('#setupForm should create form', () => {
    component.module = moduleData;
    component.setUpForm();
    expect(component.form).toBeTruthy();
  });

  it('#actionsHandler should call #save', () => {
    component.actionsHandler('save');
    expect(sportsModulesService.updateModule).toHaveBeenCalled();
    expect(component.module).toEqual(moduleData);
    expect(component.actionButtons.extendCollection).toHaveBeenCalledWith(component.module);
    expect(snackBar.open).toHaveBeenCalledWith('Sports module saved!', 'Ok!', { duration: 3000});
  });

  it('#actionsHandler should call #revert', () => {
    component['loadInitialData'] = jasmine.createSpy('loadInitialData');
    component.actionsHandler('revert');

    expect(component.loadInitialData).toHaveBeenCalled();
  });
});
