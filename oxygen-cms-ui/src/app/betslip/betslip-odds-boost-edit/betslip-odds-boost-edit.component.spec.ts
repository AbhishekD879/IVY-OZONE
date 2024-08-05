import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { BetslipOddsBoostEditComponent } from './betslip-odds-boost-edit.component';

describe('BetslipOddsBoostEditComponent', () => {
  let component: BetslipOddsBoostEditComponent;
  let fixture: ComponentFixture<BetslipOddsBoostEditComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ BetslipOddsBoostEditComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(BetslipOddsBoostEditComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
