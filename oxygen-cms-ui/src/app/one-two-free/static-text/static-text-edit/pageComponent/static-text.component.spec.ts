import {async, ComponentFixture, fakeAsync, TestBed} from '@angular/core/testing';
import { MatDialogRef } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { CUSTOM_ELEMENTS_SCHEMA, NO_ERRORS_SCHEMA  } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Observable } from 'rxjs/Observable';
import { BrandService } from '@app/client/private/services/brand.service';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { ApiClientService } from '@app/client/private/services/http';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { StaticTextOtfComponent } from './static-text-edit.component';
import { StaticTextOtfAPIService } from '../../../service/staticTextOtf.api.service';

class MockMatDialogRef {
  close() {}
}
class MockBrandService {
  brand() {}
}
class MockApiClientService {}
class MockMatSnackBar {}
class MockStaticTextOtfAPIService {}

const data = {
  body: {
    id: '5c54565cc9e77c0001c46097',
    sortOrder: null,
    brand: 'bma',
    enabled: true,
    lang: '',
    pageName: 'Current',
    title: '',
    pageText1: '<p>Some initial data</p>',
    pageText2: '',
    pageText3: null,
    pageText4: null,
    pageText5: null,
    ctaText1: '',
    ctaText2: '',
  }
};

const data2 = {
  body: {
    id: '5c54565cc9e77c0001c46097',
    sortOrder: null,
    brand: 'bma',
    enabled: true,
    pageName: 'Current',
    title: '',
    pageText1: '<p>Update static service works!</p>',
    pageText2: '',
    pageText3: null,
    pageText4: null,
    pageText5: null,
    ctaText1: '',
    ctaText2: '',
  }
};

describe('StaticTextOtfComponent', () => {
  let component: StaticTextOtfComponent;
  let fixture: ComponentFixture<StaticTextOtfComponent>;

  const dialogService: any = {
    showCustomDialog: jasmine.createSpy('showCustomDialog'),
    showConfirmDialog: jasmine.createSpy('showConfirmDialog'),
    showNotificationDialog: jasmine.createSpy('showNotificationDialog')
  };

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ StaticTextOtfComponent ],
      providers: [{
        provide: ActivatedRoute, useValue: <ActivatedRoute> {
          snapshot: {
            paramMap: {
              get: (id: string) => {
                return 'id';
              }
            }
          }
        }
      },
      { provide: Router, useValue: <Router> {} },
      { provide: GlobalLoaderService, useClass: GlobalLoaderService },
      { provide: MatSnackBar, useValue: MockMatSnackBar },
      { provide: MatDialogRef, useValue: MockMatDialogRef },
      { provide: StaticTextOtfAPIService, useValue: <MockStaticTextOtfAPIService> {
          getSingleStaticTextOtfsData: (): Observable<any> => {
            return Observable.of(data);
          },
          putStaticTextOtfsChanges: (): Observable<any> => {
            return Observable.of(data2);
          },
          deleteStaticTextOtf: (): Observable<any> => {
            return Observable.of();
          }
        }
      },
      { provide: BrandService, useValue: MockBrandService },
      { provide: ApiClientService, useValue: MockApiClientService },
      { provide: DialogService, useValue: <DialogService > {} },
      { provide: DialogService, useValue: dialogService }
      ],
      schemas: [ NO_ERRORS_SCHEMA, CUSTOM_ELEMENTS_SCHEMA ]
    });
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(StaticTextOtfComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should update page text', () => {
    const testString = '<p>it works!</p>';
    component.updateText(testString, 1);
    expect(component.staticTextOtf.pageText1).toContain('<p>it works!</p>');
  });

  it('should update static content', () => {
    component.actionButtons = jasmine.createSpyObj([
      'extendCollection'
    ]);
    const testString = '<p>Update static service works!</p>';
    component.updateText(testString, 1);
    component.saveStaticTextChanges();
    expect(dialogService.showNotificationDialog).toHaveBeenCalledWith(
      {
        title: 'Upload Completed',
        message: 'Static Text Changes are Saved.'
      }
    );
    expect(component.actionButtons.extendCollection).toHaveBeenCalled();
    expect(component.staticTextOtf.pageText1).toContain('<p>Update static service works!</p>');
  });

  it('should revert Static Text to initial', fakeAsync(() => {
    spyOn<any>(component, 'loadInitialData');
    const testString = '<p>Update static service works!</p>';
    component.updateText(testString, 1);
    component.revertStaticTextChanges();
    expect(component['loadInitialData']).toHaveBeenCalled();
  }));
});
