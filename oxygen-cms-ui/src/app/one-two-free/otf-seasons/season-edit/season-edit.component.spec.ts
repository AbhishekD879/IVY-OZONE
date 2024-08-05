import { HttpClientTestingModule } from '@angular/common/http/testing';
import { CUSTOM_ELEMENTS_SCHEMA, NO_ERRORS_SCHEMA } from '@angular/core';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatDialogModule } from '@angular/material/dialog';
import { ActivatedRoute, Router } from '@angular/router';
import { BrandService } from '@root/app/client/private/services/brand.service';
import { ApiClientService } from '@root/app/client/private/services/http';
import { ImageManagerService } from '@root/app/image-manager/services/image-manager.service';
import { DialogService } from '@root/app/shared/dialog/dialog.service';
import { GlobalLoaderService } from '@root/app/shared/globalLoader/loader.service';
import { MockTeams, seasonMockData } from '@root/app/one-two-free/constants/otf.model';

import { SeasonEditComponent } from './season-edit.component';

describe('SeasonEditComponent', () => {
  let component: SeasonEditComponent;
  let fixture: ComponentFixture<SeasonEditComponent>;
  let seasonApiService, fakeactivatedRoute;
  let router: Partial<Router>;
  let dialogService: Partial<DialogService>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      schemas: [CUSTOM_ELEMENTS_SCHEMA, NO_ERRORS_SCHEMA],
      declarations: [SeasonEditComponent],
      providers: [{ provide: ActivatedRoute, useValue: fakeactivatedRoute },
        GlobalLoaderService, DialogService, ApiClientService, BrandService,
      { provide: ImageManagerService, useValue: {} }, { provide: Router, useValue: router }],
      imports: [FormsModule, ReactiveFormsModule, HttpClientTestingModule, MatDialogModule]
    })
      .compileComponents();
    seasonApiService = {
      getAllSeasons: jasmine.createSpy('getAllSeasons').and.returnValue(seasonMockData),
      deleteSeason: jasmine.createSpy('createMyBadges').and.returnValue(true),
      getAllTeams: jasmine.createSpy('createMyBadges').and.returnValue(MockTeams),
      getSingleSeasonData: jasmine.createSpy('getAllSeasons').and.returnValue(seasonMockData[0])
    };
    dialogService = {
      showNotificationDialog: jasmine.createSpy('showNotificationDialog'),
      showConfirmDialog: jasmine.createSpy('showConfirmDialog').and
        .callFake(({ title, message, yesCallback }) => {
          yesCallback();
        })
    };
    router = {
      navigateByUrl: jasmine.createSpy('navigateByUrl')
    };

    fakeactivatedRoute = {
      snapshot: {
        params: {
          id: 'dkjgqewydgediuye'
        }
      }
    };
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SeasonEditComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
  it('ngOnInit Edit flow', () => {
    spyOn(component, 'loadInitialData');

    component.ngOnInit();

    expect(component.isCreate).toBeFalse();
    expect(component['initForm']).toHaveBeenCalled();
    expect(component['loadTeams']).toHaveBeenCalled();
    expect(component['loadInitialData']).toHaveBeenCalled();

  });
  it('ngOnInit Create flow', () => {
    spyOn(component, 'loadInitialData');

    component.ngOnInit();

    expect(component.isCreate).toBeTrue();
    expect(component['initForm']).toHaveBeenCalled();
    expect(component['loadTeams']).toHaveBeenCalled();
    expect(component['loadInitialData']).not.toHaveBeenCalled();

  });
  describe('initForm', () => {
    it('initialize the form', () => {

      component['initForm']();

      expect(component.seasonForm.get('id')).toBeTruthy();
      expect(component.seasonForm.get('seasonName')).toBeTruthy();
      expect(component.seasonForm.get('seasonInfo')).toBeTruthy();
      expect(component.seasonForm.get('displayFrom')).toBeTruthy();
      expect(component.seasonForm.get('displayTo')).toBeTruthy();
      expect(component.seasonForm.get('teams')).toBeTruthy();
      expect(component.seasonForm.get('badgeTypes')).toBeTruthy();
      expect(component.seasonForm.get('createdBy')).toBeTruthy();
      expect(component.seasonForm.get('createdByUserName')).toBeTruthy();
      expect(component.seasonForm.get('updatedByUserName')).toBeTruthy();
      expect(component.seasonForm.get('createdAt')).toBeTruthy();
      expect(component.seasonForm.get('updatedAt')).toBeTruthy();
      expect(component.seasonForm.get('brand')).toBeTruthy();
    });

  });

  describe('loadTeams', () => {
    it('should load teams', () => {
      component['loadTeams']();
      expect(seasonApiService.getAllTeams()).toHaveBeenCalled();
      /* expect(component.teams).toEqual(MockTeams); */
    });
  });

  describe('loadInitData', () => {
    it('get call', () => {

      component['loadInitData']('dkjgqewydgediuye');

      expect(seasonApiService.getSingleSeasonData).toHaveBeenCalled();

    });
  });

  describe('handleDisplayDateUpdate', () => {

    it('handleDisplayDate should Update season date', () => {
      const startdate = seasonMockData[0].displayFrom;
      const enddate = seasonMockData[0].displayTo;

      component.handleDisplayDateUpdate({
        startDate: startdate,
        endDate: enddate
      });

      expect(component.seasonForm.value.displayFrom).toEqual(startdate);
      expect(component.seasonForm.value.displayTo).toEqual(enddate);
    });
  });

  describe('setValueToForm', () => {
    it('setValueToForm ', () => {
      let data = {
        body: seasonMockData[0]
      }
      component['setValueToForm'](data);

      expect(component.seasonForm.get('id').value).toEqual(seasonMockData[0].id);
    });

  });
  describe('createEditSeason', () => {
    it('createEditSeason Create', () => {

      component['createEditSeason']('create');

      expect(seasonApiService.createSeason).toHaveBeenCalled();
    });

    it('createEditSeason Update', () => {
      component['createEditSeason']('update');

      expect(seasonApiService.updateSeason).toHaveBeenCalled();
    });
  });

  describe('actionHandler', () => {
    it('#actionHandler should call correct method', () => {
      spyOn(component, 'removeSeason');

      component.actionsHandler('remove');

      expect(component.removeSeason).toHaveBeenCalled();

      spyOn(component, 'createEditSeason');

      component.actionsHandler('save');

      expect(component.createEditSeason).toHaveBeenCalled();

      spyOn(component, 'loadInitialData');

      component.actionsHandler('revert');

      expect(component.loadInitialData).toHaveBeenCalled();
    });

    it('#actionHandler should do nothing if wrong event', () => {
      spyOn(component, 'removeSeason');
      spyOn(component, 'createEditSeason');
      spyOn(component, 'loadInitialData');

      component.actionsHandler('test-event');

      expect(component.removeSeason).not.toHaveBeenCalled();
      expect(component.createEditSeason).not.toHaveBeenCalled();
      expect(component.loadInitialData).not.toHaveBeenCalled();
    });

    it('#removeCampaign should remove Campaign', () => {
      component.removeSeason(seasonMockData[0]);

      expect(seasonApiService.deleteSeason).toHaveBeenCalledWith(seasonMockData[0].id);
      expect(dialogService.showNotificationDialog).toHaveBeenCalledWith({
        title: 'Remove Completed',
        message: 'Season is Removed.',
        closeCallback: jasmine.any(Function)
      });
      expect(router.navigateByUrl).toHaveBeenCalledWith('/one-two-free/otf-seasons');
    });
  });
});
