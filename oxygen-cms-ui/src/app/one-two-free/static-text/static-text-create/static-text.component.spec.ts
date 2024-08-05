import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { MatDialogRef } from '@angular/material/dialog';
import { CUSTOM_ELEMENTS_SCHEMA, NO_ERRORS_SCHEMA  } from '@angular/core';
import { StaticTextOtfCreateComponent } from './static-text.create.component';
import { BrandService } from '@app/client/private/services/brand.service';
import { ApiClientService } from '@app/client/private/services/http/index';


class MockMatDialogRef {
  close() {}
}

class MockBrandService {
  brand() {}
}

class MockApiClientService {}

describe('StaticTextOtfCreateComponent', () => {
  let component: StaticTextOtfCreateComponent;
  let fixture: ComponentFixture<StaticTextOtfCreateComponent>;


  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ StaticTextOtfCreateComponent ],
      providers: [{
        provide: MatDialogRef, useValue: MockMatDialogRef
      }, {
        provide: BrandService, useValue: MockBrandService
      }, {
        provide: ApiClientService, useValue: MockApiClientService
      }],
      schemas: [ NO_ERRORS_SCHEMA, CUSTOM_ELEMENTS_SCHEMA ]
    });
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(StaticTextOtfCreateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });


  it('should update page text', () => {
    const testString = '<p>it works!</p>';
    component.updateText(testString, 1);
    expect(component.newStaticTextOtf.pageText1).toContain('<p>it works!</p>');

  });
});
