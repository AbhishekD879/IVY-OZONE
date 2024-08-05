import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ViewPotTableComponent } from './view-pot-table.component';

describe('ViewPotTableComponent', () => {
  let component: ViewPotTableComponent;
  let fixture: ComponentFixture<ViewPotTableComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ViewPotTableComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ViewPotTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
