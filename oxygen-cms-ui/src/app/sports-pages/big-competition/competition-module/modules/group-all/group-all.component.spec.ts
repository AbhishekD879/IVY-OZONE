import {GroupAllComponent} from './group-all.component';
import { of } from 'rxjs';
import {BigCompetitionService} from '../../../service/big-competition.service';

describe('GroupAllComponent', () => {
  let component,
    bigCompetitionApiService,
    activatedRoute,
    bigCompetitionService,
    snackBar;
  const competitionsResponse = {
    "sportId": 1,
    "sportName": "Soccer",
    "areaId": 393,
    "areaName": "International Clubs",
    "competitionId": 696,
    "competitionName": "UEFA Champions League Women",
    "allCompetitions": [
      {
        "_id": "6470c35a08697606e4274e55",
        "id": 696,
        "name": "UEFA Champions League Women",
        "uniqIdentifier": "696",
        "areaId": 393,
        "sportId": 1
      },
      {
        "_id": "6470c35c08697606e4274e5d",
        "id": 60198,
        "name": "Group B",
        "uniqIdentifier": "696",
        "areaId": 393,
        "sportId": 1
      },
      {
        "_id": "6470c35c08697606e4274e5c",
        "id": 60202,
        "name": "Group D",
        "uniqIdentifier": "696",
        "areaId": 393,
        "sportId": 1
      },
      {
        "_id": "6470c35c08697606e4274e5f",
        "id": 60200,
        "name": "Group C",
        "uniqIdentifier": "696",
        "areaId": 393,
        "sportId": 1
      },
      {
        "_id": "6470c35c08697606e4274e59",
        "id": 60196,
        "name": "Group A",
        "uniqIdentifier": "696",
        "areaId": 393,
        "sportId": 1
      },
      {
        "_id": "6470c35c08697606e4274e66",
        "id": 66229,
        "name": "Group D",
        "uniqIdentifier": "696",
        "areaId": 393,
        "sportId": 1
      },
      {
        "_id": "6470c35c08697606e4274e67",
        "id": 66223,
        "name": "Group A",
        "uniqIdentifier": "696",
        "areaId": 393,
        "sportId": 1
      },
      {
        "_id": "6470c35c08697606e4274e6c",
        "id": 66225,
        "name": "Group B",
        "uniqIdentifier": "696",
        "areaId": 393,
        "sportId": 1
      },
      {
        "_id": "6470c35c08697606e4274e71",
        "id": 66227,
        "name": "Group C",
        "uniqIdentifier": "696",
        "areaId": 393,
        "sportId": 1
      }
    ],
    "allSeasons": [
      {
        "_id": "6470c35a08697606e4274e56",
        "id": 79415,
        "name": "UEFA Champions League Women 20/21",
        "startDate": "2020-11-03T02:00:00+02:00",
        "endDate": "2021-05-17T01:59:00+02:00",
        "year": "20/21",
        "competitionIds": [
          696
        ],
        "competitionId": null,
        "areaId": 393,
        "sportId": 1,
        "uniqueId": null,
        "__v": null
      },
      {
        "_id": "6470c35c08697606e4274e60",
        "id": 85400,
        "name": "UEFA Champions League Women 21/22",
        "startDate": "2021-08-17T02:00:00+02:00",
        "endDate": "2022-05-22T01:59:00+02:00",
        "year": "21/22",
        "competitionIds": [
          696,
          60198,
          60200,
          60202,
          60196
        ],
        "competitionId": null,
        "areaId": 393,
        "sportId": 1,
        "uniqueId": null,
        "__v": null
      },
      {
        "_id": "6470c35c08697606e4274e72",
        "id": 94869,
        "name": "UEFA Champions League Women 22/23",
        "startDate": "2022-08-18T02:00:00+02:00",
        "endDate": "2023-06-04T01:59:00+02:00",
        "year": "22/23",
        "competitionIds": [
          696,
          66227,
          66225,
          66229,
          66223
        ],
        "competitionId": null,
        "areaId": 393,
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
        competitionId: 'mockId'
      })
    };
    snackBar = {};
    bigCompetitionService = new BigCompetitionService();

    component = new GroupAllComponent(
      bigCompetitionApiService,
      activatedRoute,
      bigCompetitionService,
      snackBar
    );

    component.module = {
      groupModuleData: {
        "sportId": 1,
        "areaId": 393,
        "competitionId": 60198,
        "competitionIds": null,
        "seasonId": 85400,
        "numberQualifiers": 2
      }
    };
  });

  it('should init Component', () => {
    component.ngOnInit();
    expect(component.statsCenterGroups).toBeDefined();
    expect(component.groupsNames).toBeDefined();
    expect(component.seasonsNames).toBeDefined();
    expect(component.groupsNotFound).toBeDefined();

    expect(component.currentGroupName).toEqual('Group B');
    expect(component.currentSeasonName).toEqual('UEFA Champions League Women 21/22');
  });

  it('should invoke onSelectGroupChanged on change of group', () => {
    component.ngOnInit();
    component.onSelectGroupChanged('Group A');
    
    expect(component.selectedCompetition).toBe(competitionsResponse.allCompetitions[4]);
    expect(component.module.groupModuleData.sportId).toBe(1);
    expect(component.module.groupModuleData.areaId).toBe(393);
    expect(component.module.groupModuleData.competitionId).toBe(60196);
  });

  it('should filter groups based on season', () => {
    component.ngOnInit();
    const groups = component.filterGroupsBasedOnSeasons(85400);
    const expectedGroups = [competitionsResponse.allCompetitions[4],
    competitionsResponse.allCompetitions[1],
    competitionsResponse.allCompetitions[3],
    competitionsResponse.allCompetitions[2]];

    expect(groups).toEqual(expectedGroups);
  });

  it('should invoke onSelectSeasonChanged on change of season', () => {
    component.ngOnInit();
    spyOn(component, 'onSelectGroupChanged');
    spyOn(component, 'filterGroupsBasedOnSeasons');
    component.onSelectSeasonChanged('UEFA Champions League Women 21/22');
    
    expect(component.selectedSeason).toBe(competitionsResponse.allSeasons[2]);
    expect(component.module.groupModuleData.seasonId).toBe(85400);
    expect(component.onSelectGroupChanged).toHaveBeenCalled();
    expect(component.filterGroupsBasedOnSeasons).toHaveBeenCalled();
  });
});
