import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { BrandsListComponent } from './brands-list.component';
import { SharedModule } from '../../../shared/shared.module';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { BrandsAPIService } from '../service/brands.api.service';
import { DialogService } from '../../../shared/dialog/dialog.service';

import { Observable } from 'rxjs/Observable';
import { HttpResponse } from '@angular/common/http';
import { Brand } from '../../../client/private/models';

describe('BrandsListComponent', () => {
  let component: BrandsListComponent;
  let fixture: ComponentFixture<BrandsListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [ BrowserAnimationsModule, SharedModule ],
      declarations: [ BrandsListComponent ],
      providers: [{
        provide: BrandsAPIService, useValue: <BrandsAPIService> {
          getBrandsListData: (): Observable<HttpResponse<Brand[]>> => {
            return Observable.of();
          }
        }
      }, {
        provide: DialogService, useValue: <DialogService > {
        }
      }]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(BrandsListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
