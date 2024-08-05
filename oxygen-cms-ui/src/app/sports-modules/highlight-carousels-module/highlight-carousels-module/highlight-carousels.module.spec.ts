import { ComponentFixture, fakeAsync, TestBed, tick } from '@angular/core/testing';
import { CUSTOM_ELEMENTS_SCHEMA, NO_ERRORS_SCHEMA  } from '@angular/core';
import { ActivatedRoute, Params, Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import {
  HighlightCarouselsModuleComponent
} from '@app/sports-modules/highlight-carousels-module/highlight-carousels-module/highlight-carousels-module.component';
import { SportsModulesService } from '@app/sports-modules/sports-modules.service';
import { SportsModulesBreadcrumbsService } from '@app/sports-modules/sports-modules-breadcrumbs.service';
import { Observable } from 'rxjs/Observable';
import { SportsModule } from '@app/client/private/models/homepage.model';
import { SportCategory } from '@app/client/private/models/sportcategory.model';
import { AppConstants } from '@app/app.constants';

describe('SportsHighlightCarouselsModuleComponent', () => {
  let component: HighlightCarouselsModuleComponent,
    fixture: ComponentFixture<HighlightCarouselsModuleComponent>;

  let activatedRoute: Partial<ActivatedRoute>;
  let sportsModulesService: Partial<SportsModulesService>;
  let sportsModulesBreadcrumbsService: Partial<SportsModulesBreadcrumbsService>;
  let router: Partial<Router>;
  let maSnackBar: Partial<MatSnackBar>;

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
      params: Observable.of(routeParams)
    };
    sportsModulesService = {
      getSingleModuleData: jasmine.createSpy('getSingleModuleData').and.returnValue(
        Observable.of(moduleData)
      ),
      updateModule: jasmine.createSpy('updateModule').and.returnValue(
        Observable.of(moduleData[0])
      )
    };
    sportsModulesBreadcrumbsService = {
      getBreadCrumbsForSportCategory: jasmine.createSpy('getBreadCrumbsForSportCategory').and.returnValue(
        []
      ),
      getBreadcrubs: jasmine.createSpy('getBreadcrubs').and.returnValue(
        Observable.of([])
      )
    };
    router = {
      url: '/url'
    };
    maSnackBar = {
      open: jasmine.createSpy('open')
    };

    TestBed.configureTestingModule({
      declarations: [
        HighlightCarouselsModuleComponent
      ],
      providers: [
        { provide: ActivatedRoute, useValue: activatedRoute },
        { provide: SportsModulesService, useValue: sportsModulesService },
        { provide: SportsModulesBreadcrumbsService, useValue: sportsModulesBreadcrumbsService },
        { provide: Router, useValue: router },
        { provide: MatSnackBar, useValue: maSnackBar }
      ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA, NO_ERRORS_SCHEMA ]
    }).compileComponents();

    fixture = TestBed.createComponent(HighlightCarouselsModuleComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
    tick();
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
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
    expect(component.module).toEqual(moduleData[0]);
    expect(sportsModulesBreadcrumbsService.getBreadcrubs).toHaveBeenCalledWith(
      routeParams,
      {
        module: component.module
      }
    );
  }));

  it('#save should call sportsModulesService.updateModule', fakeAsync(() => {
    component.actionButtons = {
      extendCollection: jasmine.createSpy('extendCollection')
    };
    component.module = moduleData[0];
    component.save();
    expect(sportsModulesService.updateModule).toHaveBeenCalledWith(moduleData[0]);
    expect(component.actionButtons.extendCollection).toHaveBeenCalledWith(moduleData[0]);
    expect(maSnackBar.open).toHaveBeenCalledWith(
      `Sports module saved!`, 'Ok!', {
        duration: AppConstants.HIDE_DURATION,
      }
    );
    tick();
  }));

  it('#actionsHandler call save', () => {
    component.save = jasmine.createSpy('save');
    component.actionsHandler('save');
    expect(component.save).toHaveBeenCalled();
  });

  it('#actionsHandler call revert', () => {
    component.loadInitialData = jasmine.createSpy('loadInitialData');
    component.actionsHandler('revert');
    expect(component.loadInitialData).toHaveBeenCalled();
  });

  it('#actionsHandler do nothing', () => {
    component.save = jasmine.createSpy('save');
    component.loadInitialData = jasmine.createSpy('loadInitialData');
    component.actionsHandler('test');
    expect(component.save).not.toHaveBeenCalled();
    expect(component.loadInitialData).not.toHaveBeenCalled();
  });
});
