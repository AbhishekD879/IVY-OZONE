import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { CUSTOM_ELEMENTS_SCHEMA, NO_ERRORS_SCHEMA  } from '@angular/core';
import { SvgListComponent } from './svg-list.component';

describe('SvgListComponent', () => {
  let component: SvgListComponent;
  let fixture: ComponentFixture<SvgListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      schemas: [ NO_ERRORS_SCHEMA, CUSTOM_ELEMENTS_SCHEMA ],
      declarations: [ SvgListComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SvgListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should reinit default elem', () => {
    const defaultElem = component['elem'].nativeElement;
    component.reinitSvgElement('test');
    expect(component['elem'].nativeElement === defaultElem).toBeTruthy();
  });
});
