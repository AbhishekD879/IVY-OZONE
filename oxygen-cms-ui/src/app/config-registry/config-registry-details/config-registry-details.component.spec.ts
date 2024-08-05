import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ConfigRegistryDetailsComponent } from './config-registry-details.component';

describe('ConfigRegistryDetailsComponent', () => {
  let component: ConfigRegistryDetailsComponent;
  let fixture: ComponentFixture<ConfigRegistryDetailsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ConfigRegistryDetailsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ConfigRegistryDetailsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
