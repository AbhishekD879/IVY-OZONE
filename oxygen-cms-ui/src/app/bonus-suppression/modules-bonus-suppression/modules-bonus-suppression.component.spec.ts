import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ModulesBonusSuppressionComponent } from './modules-bonus-suppression.component';

describe('ModulesBonusSuppressionComponent', () => {
  let component: ModulesBonusSuppressionComponent;
  let fixture: ComponentFixture<ModulesBonusSuppressionComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ModulesBonusSuppressionComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ModulesBonusSuppressionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
