import { ComponentFixture, fakeAsync, TestBed, tick } from '@angular/core/testing';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Observable } from 'rxjs/Observable';
import { EventHubService } from '@app/sports-pages/event-hub/services/event-hub.service';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { ErrorService } from '@app/client/private/services/error.service';
import { CUSTOM_ELEMENTS_SCHEMA, NO_ERRORS_SCHEMA  } from '@angular/core';
import { EventHubListPageComponent } from '@app/sports-pages/event-hub/components/event-hub-list-page/event-hub-list.page.component';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { EventHubCreateComponent } from '@app/sports-pages/event-hub/components/event-hub-create/event-hub-create.component';

describe('EventHubListPageComponent', () => {
  let component: EventHubListPageComponent;
  let fixture: ComponentFixture<EventHubListPageComponent>;

  const singleHub = {
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

  const hubDataMock = [singleHub];
  const maxHubsDataMock = [singleHub, singleHub, singleHub, singleHub, singleHub, singleHub, singleHub];

  const router: Partial<Router> = {
    url: '/url',
    navigate: jasmine.createSpy('navigate')
  };
  const maSnackBar: Partial<MatSnackBar> = {
    open: jasmine.createSpy('open')
  };
  const eventHubService: any = {
    getHubList: jasmine.createSpy('getHubList').and.returnValue(Observable.of(hubDataMock))
  };
  const dialogService: any = {
    showCustomDialog: jasmine.createSpy('showCustomDialog'),
    showConfirmDialog: jasmine.createSpy('showConfirmDialog')
  };
  const globalLoaderService: any = {
    showLoader: jasmine.createSpy('showLoader'),
    hideLoader: jasmine.createSpy('hideLoader')
  };
  const errorService: any = {};

  beforeEach(fakeAsync(() => {
    TestBed.configureTestingModule({
      declarations: [
        EventHubListPageComponent
      ],
      providers: [
        { provide: EventHubService, useValue: eventHubService },
        { provide: DialogService, useValue: dialogService },
        { provide: GlobalLoaderService, useValue: globalLoaderService },
        { provide: ErrorService, useValue: errorService },
        { provide: MatSnackBar, useValue: maSnackBar },
        { provide: Router, useValue: router }
      ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA, NO_ERRORS_SCHEMA ]
    }).compileComponents();

    fixture = TestBed.createComponent(EventHubListPageComponent);
    component = fixture.componentInstance;

    fixture.detectChanges();
    tick();
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('#ngOnInit should get route params and call #loadInitialData', fakeAsync(() => {
    component.ngOnInit();
    tick();
    expect(eventHubService.getHubList).toHaveBeenCalledWith();
    expect(component.hubs).toEqual(hubDataMock);
  }));

  it('should check isMaxHubAmount', fakeAsync(() => {
    component.hubs = hubDataMock;
    expect(component.isMaxHubAmount()).toBeFalsy();

    component.hubs = maxHubsDataMock;
    expect(component.isMaxHubAmount()).toBeTruthy();
  }));

  it('should show create dialog', () => {
    component.createHub();
    expect(dialogService.showCustomDialog)
      .toHaveBeenCalledWith(EventHubCreateComponent, jasmine.any(Object));
  });

  it('should show confirmation when deleting item', () => {
    component.removeHandler(hubDataMock[0]);
    expect(dialogService.showConfirmDialog)
      .toHaveBeenCalled();
  });
});

