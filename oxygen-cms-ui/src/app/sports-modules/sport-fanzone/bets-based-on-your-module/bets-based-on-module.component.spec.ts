import {fakeAsync, tick,} from '@angular/core/testing';
import { BetsbasedonmoduleComponent } from './bets-based-on-module.component';
import { of } from 'rxjs';
import { AppConstants } from '@root/app/app.constants';
import { Params } from '@angular/router';
import { SportsModule } from '@root/app/client/private/models/homepage.model';
import { SportCategory } from '@root/app/client/private/models';
 

describe('LottoResultCardComponent', () => {
  let component: BetsbasedonmoduleComponent,
      activatedRoute,
      sportsModulesService,
      sportsModulesBreadcrumbsService,
      snackBar 
          
  const routeParams: Params = {
    id: '57fcfcd9b6aff9ba6c252a2c',
    moduleId: '5beee1bbc9e77c0001fb69e3'
  };

  const moduleData: [SportsModule, SportCategory] = [
    { id: '5beee1bbc9e77c0001fb69e3' },
    {
      categoryId: 16,
      id: '57fcfcd9b6aff9ba6c252a2c'
    }
  ] as any;
  beforeEach(fakeAsync(() => { 
    activatedRoute = {
      params:of(routeParams)
    };
    sportsModulesService = {
      getSingleModuleData: jasmine.createSpy('getSingleModuleData').and.returnValue(
        of(moduleData)
      ),
      updateModule: jasmine.createSpy('updateModule').and.returnValue(
         of(moduleData[0])
      )
    };
    sportsModulesBreadcrumbsService = {
      getBreadCrumbsForSportCategory: jasmine.createSpy('getBreadCrumbsForSportCategory').and.returnValue(
        []
      ),
      getBreadcrubs: jasmine.createSpy('getBreadcrubs').and.returnValue(
        of([])
      )
    };
    
    snackBar = {
      open: jasmine.createSpy('open')
    };
    createComp();
  }));

  function createComp() {
    component = new BetsbasedonmoduleComponent(
     activatedRoute,
     sportsModulesService,
     sportsModulesBreadcrumbsService,
     snackBar
    )}

  it('should create', () => {
    expect(component).toBeDefined();
  });


  it('#ngOnInit should get route params and call #loadInitialData', fakeAsync(() => {
    component.loadInitialData = jasmine.createSpy('loadInitialData');
    component.ngOnInit();
    expect(component.loadInitialData).toHaveBeenCalledWith(routeParams);
    tick();
  }));

  it('#loadInitialData should get module info', fakeAsync(() => {
    component.loadInitialData(routeParams);
    expect(sportsModulesService.getSingleModuleData).toHaveBeenCalledWith(routeParams['moduleId'], routeParams['id']);

    tick();
    expect(component.moduleData).toEqual(moduleData[0]);
    expect(sportsModulesBreadcrumbsService.getBreadcrubs).toHaveBeenCalledWith(
      routeParams,
      {
        module: component.moduleData
      }
    );
  }));

  it('#save should call sportsModulesService.updateModule', fakeAsync(() => {
    component.actionButtons = {
      extendCollection: jasmine.createSpy('extendCollection')
    };
    component.moduleData = moduleData[0];
    component.saveChanges();
    expect(sportsModulesService.updateModule).toHaveBeenCalledWith(moduleData[0]);
    expect(component.actionButtons.extendCollection).toHaveBeenCalledWith(moduleData[0]);
    expect(snackBar.open).toHaveBeenCalledWith(
      `Sports module saved!`, 'Ok!', {
        duration: AppConstants.HIDE_DURATION,
      }
    );
    tick();
  }));

  it('#actionsHandler call save', () => {
    component.saveChanges = jasmine.createSpy('save');
    component.actionsHandler('save');
    expect(component.saveChanges).toHaveBeenCalled();
  });

  it('#actionsHandler call revert', () => {
    component.loadInitialData = jasmine.createSpy('loadInitialData');
    component.actionsHandler('revert');
    expect(component.loadInitialData).toHaveBeenCalled();
  });

  it('#actionsHandler do nothing', () => {
    component.saveChanges = jasmine.createSpy('save');
    component.loadInitialData = jasmine.createSpy('loadInitialData');
    component.actionsHandler('test');
    expect(component.saveChanges).not.toHaveBeenCalled();
    expect(component.loadInitialData).not.toHaveBeenCalled();
  });
 
});
