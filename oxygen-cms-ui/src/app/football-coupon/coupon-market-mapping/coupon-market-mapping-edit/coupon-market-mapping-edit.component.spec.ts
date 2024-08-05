import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CouponMarketMappingEditComponent } from './coupon-market-mapping-edit.component';

describe('CouponMarketMappingEditComponent', () => {
  let component: CouponMarketMappingEditComponent;
  let fixture: ComponentFixture<CouponMarketMappingEditComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CouponMarketMappingEditComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CouponMarketMappingEditComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
