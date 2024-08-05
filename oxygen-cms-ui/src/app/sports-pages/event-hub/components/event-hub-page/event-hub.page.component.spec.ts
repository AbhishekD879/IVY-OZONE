import { EventHubPageComponent } from '@app/sports-pages/event-hub/components/event-hub-page/event-hub.page.component';
import { ComponentFixture, fakeAsync, TestBed, tick } from '@angular/core/testing';
import { ActivatedRoute, Params, Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Observable } from 'rxjs/Observable';
import { EventHubService } from '@app/sports-pages/event-hub/services/event-hub.service';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { ErrorService } from '@app/client/private/services/error.service';
import { CUSTOM_ELEMENTS_SCHEMA, NO_ERRORS_SCHEMA  } from '@angular/core';

describe('EventHubPageComponent', () => {
  let component: EventHubPageComponent;
  let fixture: ComponentFixture<EventHubPageComponent>;

  const hubDataMock = {
    createdAt: null,
    createdBy: null,
    updatedBy: null,
    updatedAt: null,
    updatedByUserName: null,
    createdByUserName: null,

    brand: 'bma',
    disabled: false,
    indexNumber: 1,
    title: 'hub1 mock',
    id: 'sdafjksadhf'
  };

  const routeParams: Params = {
    hubId: hubDataMock.id
  };

  const activatedRoute: Partial<ActivatedRoute> = {
    params: Observable.of(routeParams)
  };
  const router: Partial<Router> = {
    url: '/url',
    navigate: jasmine.createSpy('navigate')
  };
  const maSnackBar: Partial<MatSnackBar> = {
    open: jasmine.createSpy('open')
  };
  const eventHubService: any = {
    getHubData: jasmine.createSpy('getHubData').and.returnValue(Observable.of(hubDataMock)),
    removeHub: jasmine.createSpy('removeHub').and.returnValue(Observable.of(hubDataMock)),
    updateHubData: jasmine.createSpy('updateHubData').and.returnValue(Observable.of(hubDataMock))
  };
  const globalLoaderService: any = {
    showLoader: jasmine.createSpy('showLoader'),
    hideLoader: jasmine.createSpy('hideLoader')
  };
  const errorService: any = {};

  beforeEach(fakeAsync(() => {
    TestBed.configureTestingModule({
      declarations: [
        EventHubPageComponent
      ],
      providers: [
        { provide: ActivatedRoute, useValue: activatedRoute },
        { provide: EventHubService, useValue: eventHubService },
        { provide: GlobalLoaderService, useValue: globalLoaderService },
        { provide: ErrorService, useValue: errorService },
        { provide: MatSnackBar, useValue: maSnackBar },
        { provide: Router, useValue: router }
      ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA, NO_ERRORS_SCHEMA ]
    }).compileComponents();

    fixture = TestBed.createComponent(EventHubPageComponent);
    component = fixture.componentInstance;

    fixture.detectChanges();
    tick();
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('#ngOnInit should get route params and call #loadInitialData', fakeAsync(() => {
    component.loadInitData = jasmine.createSpy('loadInitialData');
    component.ngOnInit();
    tick();
    expect(component.loadInitData).toHaveBeenCalledWith(routeParams.hubId);
  }));

  it('#loadInitialData should get module info', fakeAsync(() => {
    component.loadInitData(hubDataMock.id);
    expect(eventHubService.getHubData).toHaveBeenCalledWith(hubDataMock.id);

    expect(component.hubIndex).toEqual(hubDataMock.indexNumber);
    expect(component.hubData).toEqual(hubDataMock);
    expect(component.breadcrumbsData).toBeDefined();
  }));

  it('should validate hub title', () => {
    component.hubData = hubDataMock;
    component.hubData.title = '';

    expect(component.validationHandler()).toBeFalsy();

    component.hubData.title = 'test';
    expect(component.validationHandler()).toBeTruthy();
  });

  it(' should handle action buttons clicks', () => {
    component.loadInitData = jasmine.createSpy('loadInitialData');
    component.actionButtons = {
      extendCollection: function() {}
    };

    component.hubData = hubDataMock;

    component.actionsHandler('remove');
    expect(globalLoaderService.showLoader).toHaveBeenCalledWith();
    expect(eventHubService.removeHub).toHaveBeenCalledWith(hubDataMock);

    component.actionsHandler('save');
    expect(globalLoaderService.showLoader).toHaveBeenCalledWith();
    expect(eventHubService.updateHubData).toHaveBeenCalledWith(hubDataMock);

    component.actionsHandler('revert');
    expect(component.loadInitData).toHaveBeenCalledWith(hubDataMock.id);
  });
});

