import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MobileOddsBoostListComponent } from './odds-boost-list.component';

describe('MobileOddsBoostListComponent', () => {
  let component: MobileOddsBoostListComponent;
  let fixture: ComponentFixture<MobileOddsBoostListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ MobileOddsBoostListComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MobileOddsBoostListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });
});
