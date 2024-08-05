import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CouponMarketMappingCreateComponent } from './coupon-market-mapping-create.component';

describe('CouponMarketMappingCreateComponent', () => {
  let component: CouponMarketMappingCreateComponent;
  let fixture: ComponentFixture<CouponMarketMappingCreateComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CouponMarketMappingCreateComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CouponMarketMappingCreateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
