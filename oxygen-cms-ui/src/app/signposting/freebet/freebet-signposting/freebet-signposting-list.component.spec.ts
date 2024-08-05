import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { FreebetSignpostingListComponent } from './freebet-signposting-list.component';

fdescribe('FreebetSignpostingListComponent', () => {
  let component: FreebetSignpostingListComponent;
  let fixture: ComponentFixture<FreebetSignpostingListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ FreebetSignpostingListComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FreebetSignpostingListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});