import { HttpClientTestingModule } from '@angular/common/http/testing';
import { CUSTOM_ELEMENTS_SCHEMA, NO_ERRORS_SCHEMA } from '@angular/core';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatDialogModule } from '@angular/material/dialog';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { Router, RouterModule } from '@angular/router';
import { BrandService } from '@root/app/client/private/services/brand.service';
import { ApiClientService } from '@root/app/client/private/services/http';
import { DialogService } from '@root/app/shared/dialog/dialog.service';
import { GlobalLoaderService } from '@root/app/shared/globalLoader/loader.service';
import { SharedModule } from '@root/app/shared/shared.module';
import { seasonMockData } from '@root/app/one-two-free/constants/otf.model';

import { SeasonViewComponent } from './season-view.component';

describe('SeasonViewComponent', () => {
  let component: SeasonViewComponent;
  let fixture: ComponentFixture<SeasonViewComponent>;
  let seasonApiService;
  let router: Partial<Router>;
  let dialogService: Partial<DialogService>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      schemas: [CUSTOM_ELEMENTS_SCHEMA, NO_ERRORS_SCHEMA],
      declarations: [SeasonViewComponent],
      imports: [FormsModule, ReactiveFormsModule, RouterModule, HttpClientTestingModule,
        MatDialogModule, BrowserAnimationsModule, SharedModule],
      providers: [{ provide: Router, useClass: class { navigateByUrl = jasmine.createSpy('navigateByUrl') } },
        GlobalLoaderService, DialogService, ApiClientService, BrandService]
    })
      .compileComponents();
    seasonApiService = {
      getAllSeasons: jasmine.createSpy('getAllSeasons').and.returnValue(seasonMockData[0]),
      deleteSeason: jasmine.createSpy('createMyBadges').and.returnValue(true)
    };

    router = {
      navigateByUrl: jasmine.createSpy('navigateByUrl')
    };
    dialogService = {
      showNotificationDialog: jasmine.createSpy('showNotificationDialog'),
      showConfirmDialog: jasmine.createSpy('showConfirmDialog').and
        .callFake(({ title, message, yesCallback }) => {
          yesCallback();
        })
    };
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SeasonViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
  it('ngOnInit', () => {
    component.ngOnInit();
    expect(seasonApiService.getAllSeasons).toHaveBeenCalled();
  });

  it('Create new Season should navigate to new page', () => {
    component.navigateToCreateSeason();
    expect(router.navigateByUrl).toHaveBeenCalledWith('/one-two-free/otf-seasons/create');
  });

  it('removeSeason should show dialog', () => {
    spyOn<any>(component, 'removeSeason');
    component.seasonData = seasonMockData;
    component.removeSeason(component.seasonData[0]);
    expect(dialogService.showNotificationDialog).toHaveBeenCalledWith({
      title: 'Remove Season',
      message: 'Active Season Cannot be Deleted.'
    });

  });

  it('#removeSeason should remove Campaign', () => {
    component.seasonData = seasonMockData;
    component.seasonData[0].isActive = false;
    component.removeSeason(component.seasonData[0]);
    expect(seasonApiService.deleteSeason).toHaveBeenCalledWith(component.seasonData[0].id);
  });
});
