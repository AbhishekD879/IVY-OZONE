import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { AddEditBonusSuppressionModulesComponent } from './add-edit-bonus-suppression-modules.component';

describe('AddEditBonusSuppressionModulesComponent', () => {
  let component: AddEditBonusSuppressionModulesComponent;
  let fixture: ComponentFixture<AddEditBonusSuppressionModulesComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AddEditBonusSuppressionModulesComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AddEditBonusSuppressionModulesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
