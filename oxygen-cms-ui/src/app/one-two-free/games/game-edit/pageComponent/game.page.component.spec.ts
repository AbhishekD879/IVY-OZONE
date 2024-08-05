import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { CUSTOM_ELEMENTS_SCHEMA, NO_ERRORS_SCHEMA  } from '@angular/core';
import { GamePageComponent } from './game.page.component';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { MatDialogRef, MatDialogModule } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ConfirmDialogComponent } from '@app/shared/dialog/confirm-dialog/confirm-dialog.component';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { GameAPIService } from '../../../service/game.api.service';
import { APP_BASE_HREF } from '@angular/common';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { ApiClientService } from '@app/client/private/services/http/';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { BrandService } from '@app/client/private/services/brand.service';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { of } from 'rxjs/observable/of';

describe('GamePageComponent', () => {
  let component: GamePageComponent;
  let fixture: ComponentFixture<GamePageComponent>;

  const game = {
    body: {
      brand: 'bma',
      createdAt: '2018-12-20T15:13:34.426Z',
      createdBy: '54905d04a49acf605d645271',
      disabled: false,
      createdByUserName: 'test.admin@coral.co.uk',
      displayFrom: '2018-12-20T15:13:27.653Z',
      displayTo: '2018-12-20T15:13:26Z',
      events: [{}],
      prizes: null,
      id: '5c1bb19ec9e77c000161d863',
      title: null,
      updatedAt: '2018-12-20T15:13:34.426Z',
      updatedBy: '54905d04a49acf605d645271',
      updatedByUserName: 'test.admin@coral.co.uk',
      sortOrder: 0,
      status: '',
      highlighted: true,
      enabled: true
    }
  };

  const date = {
    startDate: new Date().toDateString(),
    endDate: new Date().toDateString()
  };

  const events = [{
    home: {
      name: 'team1',
      displayName: 'team1',
      teamKitIcon: 'BBC'
    },
    away: {
      name: 'team2',
      displayName: 'team2',
      teamKitIcon: 'BBC'
    },
    brand: 'bma',
    gameId: '5c1bb19ec9e77c000161d863',
    tvIcon: 'BBC',
    eventId: '564734',
    startTime: '2018-12-20T15:13:34.426Z',
    sortOrder: 0
  }];

  const fakeActivatedRoute = {
    snapshot: {
      url: [
        { path: '/one-two-free/games'},
        { path: '/one-two-free/games/32738238723'},
      ]
    }
  } as ActivatedRoute;

  const gameAPIServiceStub = {
    getSingleGamesData: (_id) => of(game),
    deleteGame: (_id) => of({}),
    putGamesChanges: (_game) => of({})
  };

  const routes = [
    { path: '', component: GamePageComponent },
    { path: 'aboutus', component: GamePageComponent }
  ];

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      schemas: [ NO_ERRORS_SCHEMA, CUSTOM_ELEMENTS_SCHEMA ],
      declarations: [ GamePageComponent ],
      imports: [ MatDialogModule, RouterModule.forRoot(routes), HttpClientTestingModule, BrowserAnimationsModule ],
      providers: [
        { provide: MatDialogRef, useValue: <MatDialogRef<ConfirmDialogComponent>>{} },
        { provide: {provide: ActivatedRoute, useValue: fakeActivatedRoute} },
        { provide: {provide: Router, useClass: class { navigate = jasmine.createSpy('navigate'); }} },
        { provide: APP_BASE_HREF, useValue : '/' },
        { provide: GameAPIService, useValue: gameAPIServiceStub },
        ApiClientService,
        BrandService,
        DialogService,
        GlobalLoaderService,
        MatSnackBar
      ]
    }).compileComponents()
      .then(() => {
        fixture = TestBed.createComponent(GamePageComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
      });
  }));
  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should set id', () => {
    component.ngOnInit();
    expect(component.id).toBeDefined();
  });

  it('should set game and breadcrumbsData', () => {
    component.loadInitialData();
    expect(component.game).toBeDefined();
    expect(component.breadcrumbsData).toBeDefined();
  });

  it('should remove', () => {
    const spyOnRemoveGame = spyOn(component, 'removeGame');
    component.actionsHandler('remove');
    expect(spyOnRemoveGame).toHaveBeenCalled();
  });

  it('should save', () => {
    const spyOnSaveGame = spyOn(component, 'saveGameChanges');
    component.actionsHandler('save');
    expect(spyOnSaveGame).toHaveBeenCalled();
  });

  it('should revert', () => {
    const spyOnSaveGame = spyOn(component, 'revertGameChanges');
    component.actionsHandler('revert');
    expect(spyOnSaveGame).toHaveBeenCalled();
  });

  it('should update Ð¿ame', () => {
    const spyOnSaveGame = spyOn(component, 'updateGame');
    component.actionsHandler('game update');
    expect(spyOnSaveGame).toHaveBeenCalled();
  });

  it('should getSingleGamesData to be called', () => {
    const spyOngetSingleGamesData = spyOn(component['gameAPIService'], 'getSingleGamesData').and.returnValue(of());
    component.updateGame();
    expect(spyOngetSingleGamesData).toHaveBeenCalled();
  });

  it('should component game to equal game.body', () => {
    component.updateGame();
    expect(component.game).toEqual(game.body);
  });

  it('should be an error', () => {
    const spyOnError = spyOn(console, 'error');
    component.actionsHandler('bla');
    expect(spyOnError).toHaveBeenCalled();
  });

  it('should remove with gameId', () => {
    const spyOnRemoveGame = spyOn(component['gameAPIService'], 'deleteGame').and.returnValue(of());
    component.game.id = '5';
    component.actionsHandler('remove');
    expect(spyOnRemoveGame).toHaveBeenCalledWith('5');
  });

  it('should save with game', () => {
    const spyOnRemoveGame = spyOn(component['gameAPIService'], 'putGamesChanges').and.returnValue(of());
    component.game = game.body as any;
    component.actionsHandler('save');
    expect(spyOnRemoveGame).toHaveBeenCalledWith(game.body);
  });

  it('should call loadInitialData', () => {
    const spyOnSaveGame = spyOn(component, 'loadInitialData');
    component.revertGameChanges();
    expect(spyOnSaveGame).toHaveBeenCalled();
  });

  it('should return false after calling isValidModel', () => {
    component.game.id = '';
    expect(component.isValidModel(component.game)).toBe(false);
  });

  it('should set events', () => {
    component.onGamesEvents(events);
    expect(component.events).toBeDefined();
  });

  it('should define displayFrom and displayTo', () => {
    component.handleVisibilityDateUpdate(date);
    expect(component.game.displayFrom).toBe(new Date(date.startDate).toISOString());
    expect(component.game.displayTo).toBe(new Date(date.endDate).toISOString());
  });
});
