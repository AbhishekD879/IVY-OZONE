import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { CUSTOM_ELEMENTS_SCHEMA, NO_ERRORS_SCHEMA  } from '@angular/core';
import { MatDialogRef, MatDialog, MatDialogModule } from '@angular/material/dialog';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { BrowserDynamicTestingModule } from '@angular/platform-browser-dynamic/testing';

import { ConfirmDialogComponent } from '../dialog/confirm-dialog/confirm-dialog.component';
import { CmsUploadDropdownComponent } from './cms-upload-dropdown.component';
import { DialogService } from './../dialog/dialog.service';
import { SvgOptionModel } from '../../client/private/models/svgOption.model';
import { NotificationDialogComponent } from '../dialog/notification-dialog/notification-dialog.component';

describe('CmsUploadDropdownComponent', () => {
  let component: CmsUploadDropdownComponent;
  let fixture: ComponentFixture<CmsUploadDropdownComponent>;

  const eventFileStub = {
    target: {
        files: [],
        value: 'blabla',
      }
  };

  const optionStub = {
    fullPath: 'string',
    name: 'string',
    svg: 'string',
    svgId: 'string',
    displayName: 'string'
  };

  const { fullPath, name, svg, svgId, displayName } = optionStub;
  const svgModelStub =  new SvgOptionModel(fullPath, name, svg, svgId, displayName);
  const svgModelStubBlank =  new SvgOptionModel('', '', '', '', '');
  const isEaqulsvgModels = (object1, object2) => {
    Object.keys(object1).forEach((item) => {
      Object.keys(object2).forEach((elem) => {
        return item !== elem;
      });
    });
    return true;
  };

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [ MatDialogModule, BrowserAnimationsModule ],
      schemas: [ NO_ERRORS_SCHEMA, CUSTOM_ELEMENTS_SCHEMA ],
      declarations: [ CmsUploadDropdownComponent, NotificationDialogComponent, ConfirmDialogComponent ],
      providers: [
          DialogService,
          { provide: MatDialogRef, useValue: <MatDialogRef<ConfirmDialogComponent>>{} },
          MatDialog,
          MatSnackBarModule,
        ]
    })
    .overrideModule(BrowserDynamicTestingModule, {
      set: {
          entryComponents: [ NotificationDialogComponent, ConfirmDialogComponent ],
      }
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CmsUploadDropdownComponent);
    component = fixture.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should set label and uploadLabel', () => {
    component.options = [];
    component.ngOnInit();
    expect(component.label).toBeDefined();
    expect(component.uploadFile).toBeDefined();
  });

  it('should set selected property', () => {
    component.options = [svgModelStub];
    component.filename = 'string';
    component.ngOnInit();
    expect(isEaqulsvgModels(component.selected, svgModelStub)).toBeTruthy();
    component.filename = 'stringstring';
    component.ngOnInit();
    expect(isEaqulsvgModels(component.selected, svgModelStubBlank)).toBeTruthy();
  });

  it('should call checkIfFileName function', () => {
    const spyOncheckIfFileName = spyOn<any>(component, 'checkIfFileName');
    component.ngDoCheck();
    expect(spyOncheckIfFileName).toHaveBeenCalled();
  });

  it('should emit onImageUpload function', () => {
    const spyOnOnImageUpload = spyOn(component.onImageUpload, 'emit');
    component.uploadFile(eventFileStub, '');
    expect(spyOnOnImageUpload).toHaveBeenCalled();
  });

  it('should call onImageUpload function', () => {
    component.uploadFile(eventFileStub, '');
    expect(eventFileStub.target.value === '').toBe(true);
  });

  it('should delete blank space', () => {
    const stringA = 'a   a';
    const stringB = 'b b';
    const stringC = 'cc';
    expect(component.removeBlankSpaces(stringA)).toBe('aa');
    expect(component.removeBlankSpaces(stringB)).toBe('bb');
    expect(component.removeBlankSpaces(stringC)).toBe('cc');
  });

  it('should emit onChange function', () => {
    const spyOnOnDataChange = spyOn(component.onDataChange, 'emit');
    component.onChange('');
    expect(spyOnOnDataChange).toHaveBeenCalled();
  });
});
