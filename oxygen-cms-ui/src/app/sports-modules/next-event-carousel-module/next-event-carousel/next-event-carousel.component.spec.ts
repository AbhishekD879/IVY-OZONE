import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { NextEventCarouselComponent } from './next-event-carousel.component';

describe('NextEventCarouselComponent', () => {
  let component: NextEventCarouselComponent;
  let fixture: ComponentFixture<NextEventCarouselComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ NextEventCarouselComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(NextEventCarouselComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
