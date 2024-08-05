import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { GamificationDetailsComponent } from './gamification-details.component';

describe('GamificationDetailsComponent', () => {
  let component: GamificationDetailsComponent;
  let fixture: ComponentFixture<GamificationDetailsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [GamificationDetailsComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(GamificationDetailsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
