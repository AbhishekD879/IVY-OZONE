import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ManageBonusSuppressionModulesComponent } from './manage-bonus-suppression-modules.component';

describe('ManageBonusSuppressionModulesComponent', () => {
  let component: ManageBonusSuppressionModulesComponent;
  let fixture: ComponentFixture<ManageBonusSuppressionModulesComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ManageBonusSuppressionModulesComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ManageBonusSuppressionModulesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
