import {GroupIndividualComponent} from './group-individual.component';
import { of } from 'rxjs';
import {BigCompetitionService} from '../../../service/big-competition.service';

describe('GroupIndividualComponent', () => {
  let component,
    bigCompetitionApiService,
    activatedRoute,
    bigCompetitionService;
  const competitionsResponse = {
    "sportId": 1,
    "sportName": "Soccer",
    "areaId": 1,
    "areaName": "England",
    "competitionId": 17,
    "competitionName": "Premier League",
    "allCompetitions": [
      {
        "_id": "647124cc08697606e4290889",
        "id": 17,
        "name": "Premier League",
        "uniqIdentifier": "17",
        "areaId": 1,
        "sportId": 1
      },
      {
        "_id": "647124cf08697606e429088d",
        "id": 51387,
        "name": "Premier League",
        "uniqIdentifier": "17",
        "areaId": 1,
        "sportId": 1
      },
      {
        "_id": "647124d108697606e4290891",
        "id": 56620,
        "name": "Premier League",
        "uniqIdentifier": "17",
        "areaId": 1,
        "sportId": 1
      },
      {
        "_id": "647124d408697606e4290895",
        "id": 65927,
        "name": "Premier League",
        "uniqIdentifier": "17",
        "areaId": 1,
        "sportId": 1
      }
    ],
    "allSeasons": [
      {
        "_id": "647124cf08697606e429088e",
        "id": 77179,
        "name": "Premier League 20/21",
        "startDate": "2020-09-12T02:00:00+02:00",
        "endDate": "2021-05-24T01:59:00+02:00",
        "year": "20/21",
        "competitionIds": [
          17,
          51387
        ],
        "competitionId": null,
        "areaId": 1,
        "sportId": 1,
        "uniqueId": null,
        "__v": null
      },
      {
        "_id": "647124d108697606e4290892",
        "id": 83706,
        "name": "Premier League 21/22",
        "startDate": "2021-08-13T02:00:00+02:00",
        "endDate": "2022-05-22T01:59:00+02:00",
        "year": "21/22",
        "competitionIds": [
          17,
          56620
        ],
        "competitionId": null,
        "areaId": 1,
        "sportId": 1,
        "uniqueId": null,
        "__v": null
      },
      {
        "_id": "647124d408697606e4290898",
        "id": 93741,
        "name": "Premier League 22/23",
        "startDate": "2022-08-05T02:00:00+02:00",
        "endDate": "2023-05-28T01:59:00+02:00",
        "year": "22/23",
        "competitionIds": [
          17,
          65927
        ],
        "competitionId": null,
        "areaId": 1,
        "sportId": 1,
        "uniqueId": null,
        "__v": null
      }
    ]
  };

  beforeEach(() => {
    bigCompetitionApiService = {
      getCompetitionGroups: jasmine.createSpy('getCompetitionGroups').and.returnValue(of({
        body: competitionsResponse
      }))
    };
    activatedRoute = {
      params: of({
        id: 'mockId'
      })
    };
    bigCompetitionService = new BigCompetitionService();

    component = new GroupIndividualComponent(
      bigCompetitionApiService,
      activatedRoute,
      bigCompetitionService
    );

    component.module = {
      groupModuleData: {
        "sportId": 1,
        "areaId": 1,
        "competitionId": 17,
        "competitionIds": null,
        "seasonId": 93741,
        "numberQualifiers": 10
      }
    };
  });

  it('should init Component', () => {
    component.ngOnInit();
    expect(component.statsCenterGroups).toBeDefined();
    expect(component.groupsNames).toBeDefined();
    expect(component.seasonsNames).toBeDefined();
    expect(component.groupsNotFound).toBeDefined();

    expect(component.currentGroupName).toEqual('Premier League');
    expect(component.currentSeasonName).toEqual('Premier League 22/23');
  });

  it('should invoke onSelectGroupChanged on change of group', () => {
    component.ngOnInit();
    component.onSelectGroupChanged('Premier League');
    
    expect(component.module.groupModuleData.sportId).toBe(1);
    expect(component.module.groupModuleData.areaId).toBe(1);
    expect(component.module.groupModuleData.competitionId).toBe(65927);
  });

  it('should filter groups based on season', () => {
    component.ngOnInit();
    const groups = component.filterGroupsBasedOnSeasons(83706);
    const expectedGroups = [competitionsResponse.allCompetitions[2]];

    expect(groups).toEqual(expectedGroups);
  });

  it('should invoke onSelectSeasonChanged on change of season', () => {
    component.ngOnInit();
    spyOn(component, 'onSelectGroupChanged');
    spyOn(component, 'filterGroupsBasedOnSeasons');
    component.onSelectSeasonChanged('Premier League 21/22');
    
    expect(component.selectedSeason).toEqual(competitionsResponse.allSeasons[1]);
    expect(component.module.groupModuleData.seasonId).toBe(83706);
    expect(component.onSelectGroupChanged).toHaveBeenCalled();
    expect(component.filterGroupsBasedOnSeasons).toHaveBeenCalled();
  });
});
