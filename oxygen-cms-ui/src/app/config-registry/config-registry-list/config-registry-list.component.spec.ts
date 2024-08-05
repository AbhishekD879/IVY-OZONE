import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ConfigRegistryListComponent } from './config-registry-list.component';

describe('ConfigRegistryListComponent', () => {
  let component: ConfigRegistryListComponent;
  let fixture: ComponentFixture<ConfigRegistryListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ConfigRegistryListComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ConfigRegistryListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
