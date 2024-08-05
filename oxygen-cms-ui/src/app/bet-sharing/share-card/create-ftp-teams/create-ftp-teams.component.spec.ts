import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateFtpTeamsComponent } from './create-ftp-teams.component';

describe('CreateFtpTeamplayersComponent', () => {
  let component: CreateFtpTeamsComponent;
  let fixture: ComponentFixture<CreateFtpTeamsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CreateFtpTeamsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CreateFtpTeamsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
