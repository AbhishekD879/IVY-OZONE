import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { CUSTOM_ELEMENTS_SCHEMA, NO_ERRORS_SCHEMA  } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';

import { BrandService } from '../../../client/private/services/brand.service';
import { GameCreateComponent } from './game.create.component';
import { GameAPIService } from '../../service/game.api.service';

describe('GameCreateComponent', () => {
  let component: GameCreateComponent;
  let fixture: ComponentFixture<GameCreateComponent>;

  const gameAPIServiceStub = {};

  const date = {
    startDate: new Date().toDateString(),
    endDate: new Date().toDateString()
  };

  const dialogRefStub = {
    close: () => {},
  };

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      schemas: [ NO_ERRORS_SCHEMA, CUSTOM_ELEMENTS_SCHEMA ],
      declarations: [ GameCreateComponent ],
      providers: [
        { provide: MatDialogRef, useValue: dialogRefStub },
        { provide: GameAPIService, useValue: gameAPIServiceStub },
        BrandService
      ],
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(GameCreateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should set newGame', () => {
    component.ngOnInit();
    expect(component.newGame).toBeDefined();
  });

  it('should define displayFrom and displayTo', () => {
    component.handleVisibilityDateUpdate(date);
    expect(component.newGame.displayFrom).toBe(new Date(date.startDate).toISOString());
    expect(component.newGame.displayTo).toBe(new Date(date.endDate).toISOString());
   });

   it('should return false after calling isValidModel', () => {
    component.newGame.title = '';
    expect(component.isValidModel()).toBe(false);
   });

   it('should return true after calling isValidModel', () => {
    component.newGame.title = 'test';
    expect(component.isValidModel()).toBe(true);
   });

   it('should close the dilog', () => {
    const spyOnSaveGame = spyOn(component['dialogRef'], 'close');
    component.closeDialog();
    expect(spyOnSaveGame).toHaveBeenCalled();
   });

});
