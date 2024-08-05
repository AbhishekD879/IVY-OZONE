import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { NextEventCarouselListComponent } from './next-event-carousel-list.component';

describe('NextEventCarouselListComponent', () => {
  let component: NextEventCarouselListComponent;
  let fixture: ComponentFixture<NextEventCarouselListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ NextEventCarouselListComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(NextEventCarouselListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
