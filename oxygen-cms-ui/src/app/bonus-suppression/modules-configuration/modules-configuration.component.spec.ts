import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ModulesConfigurationComponent } from './modules-configuration.component';

describe('ModulesConfigurationComponent', () => {
  let component: ModulesConfigurationComponent;
  let fixture: ComponentFixture<ModulesConfigurationComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ModulesConfigurationComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ModulesConfigurationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
