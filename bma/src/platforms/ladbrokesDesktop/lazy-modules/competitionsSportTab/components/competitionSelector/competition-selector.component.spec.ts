import {
  CompetitionSelectorComponent
} from '@ladbrokesDesktop/lazy-modules/competitionsSportTab/components/competitionSelector/competition-selector.component';
import { of as observableOf } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';

describe('#CompetitionSelectorComponent', () => {
  let component: CompetitionSelectorComponent;

  let activatedRoute;
  let cmsService;
  let currentMatchesService;
  let routingHelperService;
  let router;

  const cmsCompetitionsData = { 'A-ZClassIDs': '12', InitialClassIDs: '123' };
  const ssCompetitionsData = [
    {
      class: {
        categoryCode: 'Football',
        categoryDisplayOrder: '-9998',
        categoryId: '16',
        categoryName: 'Football',
        classSortCode: 'ST',
        classStatusCode: 'A',
        displayOrder: '0',
        hasNext24HourEvent: 'true',
        hasOpenEvent: 'true',
        id: '609',
        isActive: 'true',
        name: 'Football World Club Competitions',
        originalName: 'Football World Club Competitions',
        responseCreationTime: '2019-01-30T09:44:06.550Z',
        siteChannels: 'P,Q,C,I,M,'
      },
      loading: true,
      type: {
        cashoutAvail: 'Y',
        classId: '609',
        displayOrder: -1270,
        hasNext24HourEvent: 'true',
        hasOpenEvent: 'true',
        id: '27194',
        isActive: 'true',
        name: 'ASEAN League',
        siteChannels: 'P,Q,C,I,M,',
        typeFlagCodes: 'IVA,',
        typeStatusCode: 'A'
      }
    }
  ];
  const typeEventsByClassNameData = {
    outrights: [
      {
        name: 'outright event'
      }
    ],
    data: {
      events: [{
        name: 'event'
      }],
      type: {
        id: 'id',
        name: 'name',
        classId: 'classId'
      }
    }
  };

  beforeEach(() => {
    currentMatchesService = {
      getFootballClasses: jasmine.createSpy('getFootballClasses').and.returnValue(Promise.resolve(ssCompetitionsData)),
      getTypeEventsByClassName: jasmine.createSpy('getTypeEventsByClassName').and.returnValue(Promise.resolve(typeEventsByClassNameData)),
      getTypesForClasses: jasmine.createSpy('getTypesForClasses').and.returnValue(Promise.resolve(ssCompetitionsData)),
      getOtherClasses: jasmine.createSpy('getOtherClasses').and.returnValue(Promise.resolve(ssCompetitionsData))
    };

    activatedRoute = {
      snapshot: {
        paramMap: {
          get: jasmine.createSpy('get').and.returnValue('tennis')
        }
      }
    };

    cmsService = {
      getCompetitions: jasmine.createSpy('getCompetitions').and.returnValue(observableOf(cmsCompetitionsData)),
    };

    routingHelperService = {
      formCompetitionUrl: jasmine.createSpy('formCompetitionUrl').and.returnValue('competitions/tennis')
    };

    router = {
      navigateByUrl: jasmine.createSpy('navigateByUrl')
    };

    component = new CompetitionSelectorComponent(
      activatedRoute,
      cmsService,
      currentMatchesService,
      routingHelperService,
      router
    );
  });

  it('should create component', () => {
    expect(component).toBeTruthy();
  });

  describe('#prepeareCompetionsList', () => {
    it('should create component', fakeAsync(() => {
      component['prepeareCompetionsList']([{
        class: {
          name: 'name2',
          id: '609',
          originalName: 'Tennis special'
        },
        loading: true,
        types: []
      }] as any);

      tick(200);

      expect(component.list).toEqual([{
        cashoutAvail: 'Y',
        classId: '609',
        displayOrder: -1270,
        hasNext24HourEvent: 'true',
        hasOpenEvent: 'true',
        id: '27194',
        isActive: 'true',
        name: 'ASEAN League',
        siteChannels: 'P,Q,C,I,M,',
        typeFlagCodes: 'IVA,',
        typeStatusCode: 'A', typeClassName:
        'Tennis special'
      }] as any);
    }));
  });
});
