import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BlurbMessageComponent } from './blurb-message.component';

describe('BlurbMessageComponent', () => {
  let component: BlurbMessageComponent;
  let fixture: ComponentFixture<BlurbMessageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ BlurbMessageComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(BlurbMessageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
