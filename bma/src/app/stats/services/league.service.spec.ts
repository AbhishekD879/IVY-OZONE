import { LeagueService } from '@app/stats/services/league.service';
import { of as observableOf, throwError } from 'rxjs';
import { map } from 'rxjs/operators';
import {
  IStatsAreas,
  IStatsAreasAndCompetitions,
  IStatsCompetitions,
  IStatsRequestParams,
  IStatsResults,
  IStatsSeasons
} from '@app/stats/models';

describe('LeagueService', () => {
  let leagueService: LeagueService;
  let commandService, statsPointsProvider;

  beforeEach(() => {
    statsPointsProvider = {
      leagueTableCompetitionSeason: jasmine.createSpy().and.returnValue(observableOf({
        sportId: 'sportId_32',
        areaId: 'areaId_32',
        competitionId: 'competitionId_32',
      })),
      leagueTableAreas: jasmine.createSpy().and.returnValue(observableOf([
        { id: '5', name: 'area5' },
        { id: '3', name: 'area3' },
        { id: '4', name: 'area4' }
      ])),
      leagueTableResults: jasmine.createSpy().and.returnValue(observableOf([
        { id: '991', areaId: 'a991' },
        { id: '992', areaId: 'a992' },
      ])),
      leagueTableSeasons: jasmine.createSpy().and.returnValue(observableOf([
        { id: '31' },
        { id: '17' },
        { id: '923' },
      ])),
      leagueTableCompetitions: jasmine.createSpy().and.returnValue(observableOf([]))
    } as any;
    commandService = {
      register: jasmine.createSpy().and.callFake((command, commandFunction) => {
        commandFunction('some_params');
      }),
      API: {
        GET_COMPETITION_AND_SEASON: 'get/competitions-and-seasons',
        GET_SEASONS: 'get/seasons',
        GET_RESULT_TABLES: 'get/result-tables',
        GET_LEAGUE_TABLE: 'get/league-table',
      }
    } as any;
    leagueService = new LeagueService(statsPointsProvider, commandService);
  });

  it('Tests if LeagueService Service Created', () => {
    expect(leagueService).toBeTruthy();
    expect(leagueService['ids']).toEqual({
      sportId: '1',
      areaId: '',
      competitionId: '',
      seasonId: '',
      rows: []
    });
  });

  it('#registerCommand should ', () => {
    leagueService.registerCommand();
    expect(commandService.register).toHaveBeenCalledWith('get/competitions-and-seasons', jasmine.any(Function));
    expect(commandService.register).toHaveBeenCalledWith('get/seasons', jasmine.any(Function));
    expect(commandService.register).toHaveBeenCalledWith('get/result-tables', jasmine.any(Function));
    expect(commandService.register).toHaveBeenCalledWith('get/league-table', jasmine.any(Function));

    expect(statsPointsProvider.leagueTableCompetitionSeason).toHaveBeenCalledTimes(2);
    expect(statsPointsProvider.leagueTableSeasons).toHaveBeenCalledTimes(2);
    expect(statsPointsProvider.leagueTableResults).toHaveBeenCalledWith('some_params');
  });

  describe('#getAreas', () => {
    it('should get area and sort them', () => {
      leagueService['ids'] = { sportId: '333' } as any;

      const expectedAreas: IStatsAreas[] = [
        { id: '3', name: 'area3' },
        { id: '4', name: 'area4' },
        { id: '5', name: 'area5' }
      ] as any;

      leagueService.getAreas().subscribe((response: IStatsAreas[]) => {
        expect(statsPointsProvider.leagueTableAreas).toHaveBeenCalledWith({ sportId: '333' });
        expect(response).toEqual(expectedAreas);
        expect(leagueService['areas']).toEqual(expectedAreas);
      });
    });

    it('should return saved areas', () => {
      const expectedAreas: IStatsAreas[] = [
        { id: '3', name: 'area3' },
        { id: '4', name: 'area4' },
        { id: '5', name: 'area5' }
      ] as any;

      leagueService['areas'] = expectedAreas;

      leagueService.getAreas().subscribe((response: IStatsAreas[]) => {
        expect(statsPointsProvider.leagueTableAreas).not.toHaveBeenCalled();
        expect(response).toEqual(expectedAreas);
        expect(leagueService['areas']).toEqual(expectedAreas);
      });
    });

    it('should call error handler', () => {
      leagueService['areas'] = undefined;
      statsPointsProvider.leagueTableAreas.and.returnValue(throwError('some error'));
      leagueService.getAreas().subscribe(() => {
      }, error => {
        expect(error).toEqual([]);
      });
    });
  });

  describe('#getResultsTables', () => {
    it('should get league results', () => {
      const tableResults: IStatsResults[] = [
        { id: '991', areaId: 'a991' },
        { id: '992', areaId: 'a992' },
      ] as any;

      const params: IStatsRequestParams = {
        sportId: 'sportID',
        areaId: 'areaid',
        competitionId: 'competitionId'
      };

      leagueService.getResultsTables(params).subscribe((response: IStatsResults[]) => {
        expect(statsPointsProvider.leagueTableResults).toHaveBeenCalledWith(params);
        expect(response).toEqual(tableResults);
      });
    });

    it('should handle error', () => {
      statsPointsProvider.leagueTableResults.and.returnValue(throwError('error'));
      leagueService.getResultsTables({}).subscribe(() => {
      }, error => {
        expect(error).toEqual([]);
      });
    });
  });

  describe('#getCompetitionAndSeason', () => {
    it('should get competition and season and return current season', () => {
      const params: IStatsRequestParams = {
        sportId: 'sportId_32',
        areaId: 'areaId_32',
        competitionId: 'competitionId_32'
      };

      leagueService.getCompetitionAndSeason(params).subscribe((response: IStatsSeasons) => {
        expect(statsPointsProvider.leagueTableCompetitionSeason).toHaveBeenCalledWith(params);
        expect(statsPointsProvider.leagueTableSeasons).toHaveBeenCalledWith(params);
        expect(response).toEqual({ id: '31' } as any);
      });
    });

    it('should return undefined (no sportId)', () => {
      statsPointsProvider.leagueTableCompetitionSeason.and.returnValue(observableOf({
        areaId: 'areaId',
        competitionId: 'competitionId',
      }));
      leagueService.getCompetitionAndSeason({}).subscribe((response: IStatsSeasons) => {
        expect(response).toEqual(undefined);
      });
    });
    it('should return undefined (no areaId)', () => {
      statsPointsProvider.leagueTableCompetitionSeason.and.returnValue(observableOf({
        sportId: 'sportId',
        competitionId: 'competitionId',
      }));
      leagueService.getCompetitionAndSeason({}).subscribe((response: IStatsSeasons) => {
        expect(response).toEqual(undefined);
      });
    });
    it('should return undefined (no competitionId)', () => {
      statsPointsProvider.leagueTableCompetitionSeason.and.returnValue(observableOf({
        sportId: 'sportId',
        areaId: 'areaId',
      }));
      leagueService.getCompetitionAndSeason({}).subscribe((response: IStatsSeasons) => {
        expect(response).toEqual(undefined);
      });
    });

    it('should return empty object on error', () => {
      statsPointsProvider.leagueTableCompetitionSeason.and.returnValue(throwError('some error'));

      leagueService.getCompetitionAndSeason({}).subscribe((response: IStatsSeasons) => {
        expect(response).toEqual({} as any);
      });
    });
  });

  describe('#getAreaAndCompetitions', () => {
    it('should get areas and competitions', () => {
      const competitions: IStatsCompetitions[] = [
        { id: '963', name: 'name_963' },
        { id: '961', name: 'name_961' },
        { id: '962', name: 'name_962' },
        { id: '900', name: 'name_903' },
        { id: '900', name: 'name_901' },
        { id: '900', name: 'name_902' },
        { id: '800', name: 'name_800' },
        { id: '800', name: 'name_800' },
      ] as any;

      const expectedCompetitions: IStatsCompetitions[] = [
        { id: '800', name: 'name_800' },
        { id: '800', name: 'name_800' },
        { id: '900', name: 'name_901' },
        { id: '900', name: 'name_902' },
        { id: '900', name: 'name_903' },
        { id: '961', name: 'name_961' },
        { id: '962', name: 'name_962' },
        { id: '963', name: 'name_963' },
      ] as any;

      statsPointsProvider.leagueTableCompetitions.and.returnValue(observableOf(competitions));

      leagueService['areas'] = [
        { id: '323', name: 'name323', sportId: 'sport_id323' },
        { id: '390', name: 'name390', sportId: 'sport_id390' }
      ];

      leagueService.getAreaAndCompetitions('area_id1').subscribe((response: { value: IStatsAreasAndCompetitions }) => {
        expect(leagueService['ids'].areaId).toEqual('area_id1');
        expect(statsPointsProvider.leagueTableCompetitions).toHaveBeenCalledWith({ sportId: '1', areaId: 'area_id1' });
        expect(leagueService['competitions']).toEqual(expectedCompetitions);
      });
    });

    it('should find and return area name', async() => {
      leagueService['areas'] = [
        { id: '323', name: 'area_name323', sportId: 'sport_id323' },
        { id: '390', name: 'area_name390', sportId: 'sport_id390' }
      ];

      statsPointsProvider.leagueTableCompetitions.and.returnValue(observableOf([]));

      leagueService.getAreaAndCompetitions('323').pipe(map((response) => {
        // eslint-disable-next-line
        console.log(response);
        expect(response.value).toEqual({ area: 'area_name323', competitions: [] });
      }));
    });

    it('should get empty competitions', () => {
      statsPointsProvider.leagueTableCompetitions.and.returnValue(throwError('error'));
      leagueService.getAreaAndCompetitions('area_id2').subscribe((response) => {
        expect(leagueService['competitions']).toEqual([]);
      });
    });

    it('should handle error', () => {
      statsPointsProvider.leagueTableAreas.and.returnValue(throwError('#getAreaAndCompetitions error'));

      leagueService.getAreaAndCompetitions('area_id2').subscribe((response) => {
        expect(leagueService['ids'].areaId).toEqual('area_id2');
        expect(response).toEqual({ value: { area: '', competitions: [] } });
      });
    });
  });

  describe('#getStandings', () => {
    it('should return empty array if no competitions', () => {
      leagueService['competitions'] = [];
      leagueService.getStandings('competitionId', 'seasonId').subscribe((results: IStatsResults[]) => {
        expect(results).toEqual([]);
      });
    });

    it('should return empty array if no seasons', () => {
      leagueService['competitions'] = [{} as any];
      leagueService.getStandings('competitionId', 'seasonId').subscribe((results: IStatsResults[]) => {
        expect(results).toEqual([]);
      });
    });

    it('should return stats result', () => {
      statsPointsProvider.leagueTableResults.and.returnValue(observableOf([{ id: 'some_id' }]));
      leagueService['seasons'] = [{ id: 'seasonId' }] as any;
      leagueService['competitions'] = [{ id: 'competitionId' } as any];

      leagueService.getStandings('competitionId', 'seasonId').subscribe((results: IStatsResults[]) => {
        expect(statsPointsProvider.leagueTableResults).toHaveBeenCalledWith({
          sportId: '1',
          areaId: '',
          competitionId: 'competitionId',
          seasonId: 'seasonId',
          rows: []
        } as any);
        expect(results).toEqual([{ id: 'some_id' }] as any);
      });
    });

    it('should handle error', () => {
      statsPointsProvider.leagueTableResults.and.returnValue(observableOf([]));
      leagueService['seasons'] = [{ id: 'seasonId' }] as any;
      leagueService['competitions'] = [{ id: 'competitionId' } as any];
      leagueService.getStandings('competitionId', 'seasonId').subscribe((results: IStatsResults[]) => {
        expect(results).toEqual([]);
      });
    });
  });

  describe('#getSeasons', () => {
    it('should get league table seasons', () => {
      statsPointsProvider.leagueTableSeasons.and.returnValue(observableOf([
        { id: 1, startDate: '2015-08-07T00:00:00 03:00' },
        { id: 1, startDate: '2015-08-07T00:00:00 01:00' },
        { id: 1, startDate: '2015-08-07T00:00:00 02:00' },
      ]));
      const params: IStatsRequestParams = {
        sportId: 'sportId',
        areaId: 'areaId',
        competitionId: 'competitionId',
        typeId: 'typeId'
      };

      const expectedResult: IStatsSeasons[] = [
        { id: 1, startDate: '2015-08-07T00:00:00 01:00' },
        { id: 1, startDate: '2015-08-07T00:00:00 02:00' },
        { id: 1, startDate: '2015-08-07T00:00:00 03:00' }
      ] as any;

      leagueService.getSeasons(params).subscribe((result: IStatsSeasons[]) => {
        expect(result).toEqual(expectedResult);
        expect(leagueService['seasons']).toEqual(expectedResult);
      });
    });

    it('should return empty list on error', () => {
      statsPointsProvider.leagueTableSeasons.and.returnValue(throwError('error'));
      leagueService.getSeasons({}).subscribe((result: IStatsSeasons[]) => {
        expect(result).toEqual([]);
        expect(leagueService['seasons']).toEqual([]);
      });
    });
  });

});
