import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { NextEventCarouselFormComponent } from './next-event-carousel-form.component';

describe('NextEventCarouselFormComponent', () => {
  let component: NextEventCarouselFormComponent;
  let fixture: ComponentFixture<NextEventCarouselFormComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ NextEventCarouselFormComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(NextEventCarouselFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
