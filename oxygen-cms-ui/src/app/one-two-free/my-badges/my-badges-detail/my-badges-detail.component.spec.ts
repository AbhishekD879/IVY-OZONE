import { HttpClientTestingModule } from '@angular/common/http/testing';
import { CUSTOM_ELEMENTS_SCHEMA, NO_ERRORS_SCHEMA } from '@angular/core';
import { async, ComponentFixture, fakeAsync, TestBed } from '@angular/core/testing';
import { FormsModule } from '@angular/forms';
import { MatDialogModule } from '@angular/material/dialog';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { BrandService } from '@root/app/client/private/services/brand.service';
import { ApiClientService } from '@root/app/client/private/services/http';
import { DialogService } from '@root/app/shared/dialog/dialog.service';
import { GlobalLoaderService } from '@root/app/shared/globalLoader/loader.service';
import { of } from 'rxjs';
import { mybadgesMock } from '../../constants/otf.model';
import { MybadgesApiService } from '../../service/mybadges.api.service';

import { MyBadgesDetailComponent } from './my-badges-detail.component';

describe('MyBadgesDetailComponent', () => {
  let component: MyBadgesDetailComponent;
  let fixture: ComponentFixture<MyBadgesDetailComponent>;
  let myBadgeService, dialogService;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      schemas: [CUSTOM_ELEMENTS_SCHEMA, NO_ERRORS_SCHEMA],
      declarations: [MyBadgesDetailComponent],
      imports: [FormsModule, HttpClientTestingModule, BrowserAnimationsModule, MatDialogModule],
      providers: [MybadgesApiService, GlobalLoaderService, DialogService, ApiClientService, BrandService]
    })
      .compileComponents();

    myBadgeService = {
      getMyBadgesData: jasmine.createSpy('getMyBadgesData').and.returnValue(mybadgesMock),
      createMyBadges: jasmine.createSpy('createMyBadges').and.returnValue(mybadgesMock),
      updateMyBadges: jasmine.createSpy('updateMyBadges').and.returnValue(mybadgesMock)
    };
    dialogService = { showNotificationDialog: jasmine.createSpy('showNotificationDialog') };
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MyBadgesDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('ngOnInit', () => {
    spyOn(component, 'loadMybadgeData');
    component.ngOnInit();
    expect(component.loadMybadgeData).toHaveBeenCalled();
  });

  describe('loadMybadgeData', () => {
    it('Load MyBadges Data', () => {
      myBadgeService.getMyBadgesData.and.returnValue(of({ body: mybadgesMock }));

      component.loadMybadgeData();

      expect(myBadgeService.getMyBadgesData()).toBeDefined();
      expect(Object.keys(component.myBadges).length).toBeGreaterThan(0);
    });

    it('Do Not Load My Badges Data', fakeAsync(() => {
      component.loadMybadgeData();

      expect(myBadgeService.getMyBadgesData()).toEqual(mybadgesMock);
      expect(Object.keys(component.myBadges).length).toBe(0);
    }));
  });

  describe('createEditbadges', () => {
    it('Create Badges Flow', () => {
      myBadgeService.createMyBadges.and.returnValue(of({ body: mybadgesMock }));
      component.myBadges.id = '';

      component.createEditbadges();

      expect(myBadgeService.createMyBadges()).toBeDefined();
      expect(Object.keys(component.myBadges).length).toBeGreaterThan(0);
      expect(dialogService.showNotificationDialog).toHaveBeenCalled();

    });

    it('Update Badges Flow', fakeAsync(() => {
      myBadgeService.updateMyBadges.and.returnValue(of({ body: {} }));

      component.loadMybadgeData();

      expect(myBadgeService.updateMyBadges()).toBeDefined();
      expect(dialogService.showNotificationDialog).toHaveBeenCalled();
    }));
  });

  describe('isValidModel', () => {
    it('Check Model for Badge details', () => {
      component.myBadges = mybadgesMock;

      component.isValidModel(component.myBadges);

      expect(component.isValidModel(component.myBadges)).toBeTrue();
    });
  });

  describe('isLoadBadges', () => {
    it('Checkif mybadges has data', () => {
      component.myBadges = mybadgesMock;

      component.isLoadBadges();

      expect(component.isLoadBadges()).toBeTrue();
    });
  });
});
