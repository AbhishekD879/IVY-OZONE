import { StatsPointsProvider } from '@app/stats/services/stats-points.provider';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { of as observableOf } from 'rxjs';
import {
  IStatsAreas,
  IStatsBRCompetitionSeason,
  IStatsCompetitions, IStatsPlayer,
  IStatsRequestParams,
  IStatsResults, IStatsSeasonMatch,
  IStatsSeasons
} from '@app/stats/models';

describe('StatsPointsProvider', () => {
  let service, http;

  beforeEach(() => {
    http = {
      get: jasmine.createSpy().and.returnValue(observableOf({ body: 'response' })),
      post: jasmine.createSpy().and.returnValue(observableOf({ body: 'response' }))
    };
    service = new StatsPointsProvider(http as HttpClient);
  });

  it('should create', () => {
    expect(service).toBeTruthy();
  });

  it('#leagueTableAreas', () => {
    service.leagueTableAreas({ sportId: 'sportId' } as IStatsRequestParams).subscribe((data: HttpResponse<IStatsAreas[]>) => {
      expect(data).toEqual('response' as any);
    });
    expect(http.get).toHaveBeenCalledWith(`${service.STATS_CENTRE_ENDPOINT}/areas/sportId`, {
      observe: 'response',
      params: {}
    });
  });

  it('#leagueTableCompetitions', () => {
    service.leagueTableCompetitions({ sportId: 'sportId', areaId: 'areaId' } as IStatsRequestParams)
      .subscribe((data: HttpResponse<IStatsCompetitions[]>) => {
        expect(data).toEqual('response' as any);
      });
    expect(http.get).toHaveBeenCalledWith(`${service.STATS_CENTRE_ENDPOINT}/competitions/sportId/areaId`, {
      observe: 'response',
      params: {}
    });
  });

  it('#leagueTableSeasons', () => {
    service.leagueTableSeasons({ sportId: 'sportId', areaId: 'areaId', competitionId: 'competitionId' } as IStatsRequestParams)
      .subscribe((data: HttpResponse<IStatsSeasons[]>) => {
        expect(data).toEqual('response' as any);
      });
    expect(http.get).toHaveBeenCalledWith(`${service.STATS_CENTRE_ENDPOINT}/seasons/sportId/areaId/competitionId`, {
      observe: 'response',
      params: {}
    });
  });

  it('#leagueTableResults', () => {
    service.leagueTableResults({
      sportId: 'sportId', areaId: 'areaId', competitionId: 'competitionId', seasonId: 'seasonId'
    } as IStatsRequestParams)
      .subscribe((data: HttpResponse<IStatsResults[]>) => {
        expect(data).toEqual('response' as any);
      });
    expect(http.get).toHaveBeenCalledWith(`${service.STATS_CENTRE_ENDPOINT}/resultstables/sportId/areaId/competitionId/seasonId`, {
      observe: 'response',
      params: {}
    });
  });

  it('#leagueTableCompetitionSeason', () => {
    const leagueTableCompetitionSeasonResponse = {body:{allCompetitions:[{"_id":"646a6699a3ab5a70afc55095","id":"7_Group_A","name":"UEFA Champions League, Group A","uniqIdentifier":"7","areaId":"393","sportId":"1"},{"_id":"646a6699a3ab5a70afc55097","id":"7_Group_C","name":"UEFA Champions League, Group C","uniqIdentifier":"7","areaId":"393","sportId":"1"},{"_id":"646a6697a3ab5a70afc55087","id":"7","name":"UEFA Champions League","uniqIdentifier":"7","areaId":"393","sportId":"1"}]}};
    http.get.and.returnValue(observableOf(leagueTableCompetitionSeasonResponse));
    service.leagueTableCompetitionSeason({ sportId: 'sportId', classId: 'classId', typeId: 'typeId' } as IStatsRequestParams)
      .subscribe((data: HttpResponse<IStatsBRCompetitionSeason[]>) => {
        expect(data).toEqual(leagueTableCompetitionSeasonResponse.body as any);
      });
    expect(http.get).toHaveBeenCalledWith(`${service.STATS_CENTRE_ENDPOINT}/brcompetitionseason/sportId/classId/typeId`, {
      observe: 'response',
      params: {}
    });
  });

  it('#seasonMatches', () => {
    service.seasonMatches(
      'seasonId', 2, 5
    ).subscribe((data: HttpResponse<IStatsSeasonMatch[]>) => {
      expect(data).toEqual('response' as any);
    });
    expect(http.get).toHaveBeenCalledWith(`${service.STATS_CENTRE_ENDPOINT}/season/seasonId/matches/?skip=2&limit=5`, {
      observe: 'response',
      params: {}
    });
  });

  it('#matchesByDate', () => {
    service.matchesByDate(
      { startdate: 'startDate', enddate: 'endDate' }
    ).subscribe((data: HttpResponse<IStatsSeasonMatch[]>) => {
      expect(data).toEqual('response' as any);
    });
    expect(http.get).toHaveBeenCalledWith(`${service.STATS_CENTRE_ENDPOINT}/matches/bydate?startdate=startDate&enddate=endDate`, {
      observe: 'response',
      params: {}
    });
  });

  it('#statsCentrePlayers', () => {
    service.statsCentrePlayers(
      ['3', '1']
    ).subscribe((data: HttpResponse<IStatsPlayer[]>) => {
      expect(data).toEqual({ body: 'response' } as any);
    });
    expect(http.post).toHaveBeenCalledWith(`${service.STATS_CENTRE_ENDPOINT}/player`, ['3', '1']);
  });

});
