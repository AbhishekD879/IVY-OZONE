import { ComponentFixture, fakeAsync, TestBed, tick } from '@angular/core/testing';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { CUSTOM_ELEMENTS_SCHEMA, NO_ERRORS_SCHEMA  } from '@angular/core';
import { EventHubCreateComponent } from '@app/sports-pages/event-hub/components/event-hub-create/event-hub-create.component';
import { BrandService } from '@app/client/private/services/brand.service';

describe('EventHubCreateComponent', () => {
  let component: EventHubCreateComponent;
  let fixture: ComponentFixture<EventHubCreateComponent>;

  const brandService: any = {
    brand: 'bma'
  };

  const dialogRef: any = {
    close: jasmine.createSpy('close')
  };

  const dialogDataMock = {
    data: {
      index: 0
    }
  };

  beforeEach(fakeAsync(() => {
    TestBed.configureTestingModule({
      declarations: [
        EventHubCreateComponent
      ],
      providers: [
        { provide: MAT_DIALOG_DATA, useValue: dialogDataMock },
        { provide: BrandService, useValue: brandService },
        { provide: MatDialogRef, useValue: dialogRef }
      ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA, NO_ERRORS_SCHEMA ]
    }).compileComponents();

    fixture = TestBed.createComponent(EventHubCreateComponent);
    component = fixture.componentInstance;

    fixture.detectChanges();
    tick();
  }));

  it('should create component', () => {
    expect(component).toBeTruthy();
  });

  it('#ngOnInit should create initial Hub Object', fakeAsync(() => {
    component.ngOnInit();
    tick();
    expect(component.newEventHub).toBeDefined();
    expect(component.newEventHub.brand).toEqual('bma');
    expect(component.newEventHub.indexNumber).toEqual(0);
    expect(component.newEventHub.disabled).toEqual(false);
  }));
});

