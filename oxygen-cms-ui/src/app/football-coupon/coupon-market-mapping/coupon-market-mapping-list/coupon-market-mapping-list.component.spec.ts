import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CouponMarketMappingListComponent } from './coupon-market-mapping-list.component';

describe('CouponMarketMappingListComponent', () => {
  let component: CouponMarketMappingListComponent;
  let fixture: ComponentFixture<CouponMarketMappingListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CouponMarketMappingListComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CouponMarketMappingListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
