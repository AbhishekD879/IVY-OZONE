import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { GamificationListComponent } from './gamification-list.component';

describe('GamificationListComponent', () => {
  let component: GamificationListComponent;
  let fixture: ComponentFixture<GamificationListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [GamificationListComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(GamificationListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
