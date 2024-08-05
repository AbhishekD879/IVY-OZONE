import { TestBed, getTestBed } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { MatDialog } from '@angular/material/dialog';
import { GameAPIService } from './game.api.service';
import { TeamKitAPIService } from './../teamKit.api.service';
import { GlobalLoaderService } from '../../shared/globalLoader/loader.service';
import { ApiClientService } from '../../client/private/services/http/';
import { BrandService } from '../../client/private/services/brand.service';
import { of } from 'rxjs/observable/of';

describe('GameApiService', () => {
  let injector: TestBed;
  let service: GameAPIService;

  const mockedGames = [{
    brand: 'bma',
    createdAt: '2018-11-06T11:47:26.950Z',
    createdBy: '54905d04a49acf605d645271',
    createdByUserName: null,
    displayFrom: '2018-11-06T08:46:59Z',
    displayTo: '2018-11-07T13:46:59Z',
    enabled: false,
    events: null,
    prizes: null,
    id: '5be17f4ec9e77c0001642c17',
    status: 'Past',
    title: null,
    updatedAt: '2018-11-06T11:47:26.950Z',
    updatedBy: '54905d04a49acf605d645271',
    updatedByUserName: null
  }];

  const mockedGame = {
    brand: 'bma',
    createdAt: '2018-11-06T11:47:26.950Z',
    createdBy: '54905d04a49acf605d645271',
    createdByUserName: null,
    displayFrom: '2018-11-06T08:46:59Z',
    displayTo: '2018-11-07T13:46:59Z',
    enabled: false,
    events: null,
    prizes: null,
    id: '5be17f4ec9e77c0001642c17',
    status: 'Past',
    title: null,
    updatedAt: '2018-11-06T11:47:26.950Z',
    updatedBy: '54905d04a49acf605d645271',
    updatedByUserName: null,
    sortOrder: 0,
    highlighted: true,
    seasonId: '1'
  };

  const mockedEvent = {
    awayTeamName: 'Team23',
    eventId: '8830146',
    homeTeamName: 'Team12',
    startTime: '2018-12-25T19:20:00Z'
  };

  const apiServiceStub = {
    gamesService: () => ({
      getGames: () => of(mockedGames),
      deleteGame: (id) => of(id),
      postNewGame: () => of(mockedGame),
      getSingleGame: (id) => of(mockedGame),
      putGameChanges: (id, game) => of(mockedGame)
    }),
    eventsService: () => ({
      getEvent: (id) => of(mockedEvent)
    })
  };

  const kitServiceStub = {

  };

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [ HttpClientTestingModule ],
      providers: [
        GameAPIService,
        GlobalLoaderService,
        { provide: ApiClientService, useValue: apiServiceStub },
        { provide: TeamKitAPIService, useValue: kitServiceStub },
        BrandService,
        MatDialog
      ]
    });
    injector = getTestBed();
    service = injector.get(GameAPIService);
  });

  it('should return games and call showLoader', () => {
    const spyOnLoader = spyOn(service['globalLoaderService'], 'showLoader');
    service.getGamesData().subscribe(games => {
      expect(spyOnLoader).toHaveBeenCalled();
      expect(games).toEqual(mockedGames);
    });
  });

  it('should call wrappedObservable and responce to be equal 1', () => {
    const spyOnWrappedObservable = spyOn(service, 'wrappedObservable').and.callThrough();
    service.deleteGame('1').subscribe(data => {
      expect(data).toBe('1');
      expect(spyOnWrappedObservable).toHaveBeenCalled();
    });
  });

  it('should call wrappedObservable and showloader', () => {
    const spyOnLoader = spyOn(service['globalLoaderService'], 'showLoader');
    service.postNewGame(mockedGame).subscribe(game => {
      expect(spyOnLoader).toHaveBeenCalled();
      expect(game).toEqual(mockedGame);
    });
  });

  it('should call wrappedObservable and responce to be equal mockedGame', () => {
    const spyOnWrappedObservable = spyOn(service, 'wrappedObservable').and.callThrough();
    const spyOnLoader = spyOn(service['globalLoaderService'], 'showLoader');
    service.putGamesChanges(mockedGame).subscribe(game => {
      expect(game).toEqual(mockedGame);
      expect(spyOnWrappedObservable).toHaveBeenCalled();
      expect(spyOnLoader).toHaveBeenCalled();
    });
  });
  it('should call wrappedObservable and responce to be equal mockedEvent', () => {
    const spyOnWrappedObservable = spyOn(service, 'wrappedObservable').and.callThrough();
    service.getEventById(mockedEvent.eventId).subscribe(event => {
      expect(event).toEqual(mockedEvent);
      expect(spyOnWrappedObservable).toHaveBeenCalled();
    });
  });

  it('should call wrappedObservable and responce to be equal mockedGame', () => {
    const spyOnWrappedObservable = spyOn(service, 'wrappedObservable').and.callThrough();
    service.getSingleGamesData(mockedGame.id).subscribe(game => {
      expect(game).toEqual(mockedGame);
      expect(spyOnWrappedObservable).toHaveBeenCalled();
    });
  });

});
