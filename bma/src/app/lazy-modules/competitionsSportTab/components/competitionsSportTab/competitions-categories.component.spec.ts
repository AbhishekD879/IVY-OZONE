import { fakeAsync, flush, tick } from '@angular/core/testing';
import { of as observableOf } from 'rxjs';
import {
  CompetitionsCategoryComponent
} from '@lazy-modules/competitionsSportTab/components/competitionsSportTab/competitions-categories.component';

describe('CompetitionsCategoryComponent', () => {
  let component: CompetitionsCategoryComponent;

  let currentMatchesService;
  let routingHelperService;
  let activatedRoute;
  let pubSubService;

  const ssCompetitionsData = [
    {
      class: { id: '10', name: 'A' },
      name: 'Football Competitions A',
      originalName: 'Football World Club Competitions A',
      loading: true
    }, {
      class: { id: '11', name: 'B' },
      name: 'Football Competitions B',
      originalName: 'Football World Club Competitions B',
      loading: true
    }] as any;

  const type = [
    { type: { id: '27196', name: 'Competitions A', displayOrder: 2 } },
    {},
    { type: { id: '27195', name: 'Competitions B', displayOrder: 1 } }];

  const iconsQueryList = [
    {
      dirty: false,
      _results: []
    },
    {
      dirty: false,
      _results: []
    },
    {
      dirty: false,
      _results: []
    }
  ] as any;

  const changeDetectorRef = {
    detectChanges: jasmine.createSpy('detectChanges')
  } as any;
  iconsQueryList.reset = jasmine.createSpy('iconsQueryList reset');

  beforeEach(() => {
    currentMatchesService = {
      getClassToSubTypeForClass: jasmine.createSpy('getClassToSubTypeForClass').and.returnValue(observableOf(type))
    };
    routingHelperService = {
      formCompetitionUrl: jasmine.createSpy('formCompetitionUrl').and.returnValue('tennis/tennis/url')
    };
    activatedRoute = {
      snapshot: { paramMap: { get: jasmine.createSpy('get').and.returnValue('football') } }
    };
    pubSubService = {
      publishSync: jasmine.createSpy('publishSync'),
      API: { CHANGE_STATE_CHANGE_COMPETITIONS: 'CHANGE_STATE_CHANGE_COMPETITIONS' }
    };

    component = new CompetitionsCategoryComponent(activatedRoute, currentMatchesService, routingHelperService,
      pubSubService, changeDetectorRef);
    component.categoryId = '16';
    (component.categories as any) = ssCompetitionsData;
    spyOn(component.pageLoaded, 'emit');
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  describe('goToTypes', () => {
    it('should set loading prop to false for chosen type', fakeAsync(() => {
      component['initiallyExpanded'] = {
        0: true
      } as any;
      component.categories = [
        {
          initiallyExpanded: true,
          loading: true,
          class: {}
        },
        {
          initiallyExpanded: false,
          loading: false,
          class: {}
        }
      ] as any;
      currentMatchesService.getClassToSubTypeForClass = jasmine.createSpy().and.returnValue(observableOf({}));
      component.goToTypes(0);
      flush();
      tick();
      expect(component.categories[0].loading).toBeFalsy();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalledTimes(3);
    }));
  });

  describe('#ngOnInit', () => {
    it('should Init data if not A-Z categories list',  fakeAsync(() => {
      component.categoryId = '16';
      component.isAzCategories = false;
      component.ngOnInit();
      expect(component.isShowAz).toBe(false);
      tick();
      expect(currentMatchesService.getClassToSubTypeForClass).toHaveBeenCalledWith('10');
      expect(component.categories[0].loading).toBe(false);
      expect(component.categories[0].types).toEqual([{
        type: { id: '27195', name: 'Competitions B', displayOrder: 1 },
        name: 'Competitions B',
        link: '',
      }, {
        type: { id: '27196', name: 'Competitions A', displayOrder: 2 },
        name: 'Competitions A',
        link: '',
      }] as any);
    }));

    it('should Init data if A-Z categories are present', () => {
      component.isAzCategories = true;
      component.ngOnInit();

      expect(component.isShowAz).toBe(true);
    });

    it('should Init data for Tennis', fakeAsync(() => {
      component.categoryId = '34';
      component.ngOnInit();
      expect(component.isShowAz).toBe(false);
      expect(component.isExpanded[0]).toBe(true);
      expect(component.categories[0].loading).toBe(false);
      tick();
      expect(currentMatchesService.getClassToSubTypeForClass).toHaveBeenCalledWith('11');
      expect(component.categories[1].loading).toBe(false);
    }));
  });

  it('#closeChangeCompetition should publish pubsub event', () => {
    component.closeChangeCompetition();
    expect(pubSubService.publishSync).toHaveBeenCalledWith('CHANGE_STATE_CHANGE_COMPETITIONS', false);
  });

  it('#trackByIndex', () => {
    expect(component.trackByIndex(1)).toEqual(1);
  });

  describe('#competitionsLink', () => {
    it('should create competitions link', () => {
      const result = component.competitionsLink({
        type: {
          name: 'name'
        }
      } as any, 'tennis');
      expect(routingHelperService.formCompetitionUrl).toHaveBeenCalledWith({
        sport: 'football',
        typeName: 'name',
        className: 'tennis'
      });
      expect(result).toEqual('tennis/tennis/url');
    });
  });

  it('#isTennis for tennis', () => {
    component.categoryId = '34';
    expect(component.isTennis()).toEqual(true);
  });

  it('#isTennis for football', () => {
    component.categoryId = '16';
    expect(component.isTennis()).toEqual(false);
  });

  describe('updateLoadingState', () => {
    it('should return false if there are no categories', () => {
      component['categories'] = undefined;
      component['updateLoadingState']();
      expect(component['loading']).toBeFalsy();
      expect(component.pageLoaded.emit).toHaveBeenCalled();
    });
    it('should return true if opened sections not initialized yet', () => {
      component['initiallyExpanded'] = {
        0: true
      } as any;
      component.categories = [
        {
          initiallyExpanded: true,
          loading: true
        },
        {
          initiallyExpanded: false,
          loading: true
        }
      ] as any;
      component['updateLoadingState']();
      expect(component['loading']).toBeTruthy();
      expect(component.pageLoaded.emit).not.toHaveBeenCalled();
    });
    it('should return false if opened sections already initialized', () => {
      component['initiallyExpanded'] = {
        0: false
      } as any;
      component.categories = [
        {
          initiallyExpanded: true,
          loading: false
        },
        {
          initiallyExpanded: false,
          loading: false
        }
      ] as any;
      component['updateLoadingState']();
      expect(component['loading']).toBeFalsy();
      expect(component.pageLoaded.emit).toHaveBeenCalled();
    });
  });



  describe('extendTypes', () => {
    it('should filter and sort types', () => {
      const category: any = { class: {} };
      const types: any = [
        { type: { name: 'type2', displayOrder: 2 } },
        { type: { name: 'type1', displayOrder: 1 } },
        { type: null }
      ];
      expect(component['extendTypes'](category, types)).toEqual([
        { type: { name: 'type1', displayOrder: 1 }, name: 'type1', link: '' },
        { type: { name: 'type2', displayOrder: 2 }, name: 'type2', link: '' }
      ] as any);
    });

    it('should create competition link for type', () => {
      const category: any = { class: { originalName: 'class1' } };
      const types: any = [{ type: { name: 'type1' } }];
      component['extendTypes'](category, types);
      expect(routingHelperService.formCompetitionUrl).toHaveBeenCalledTimes(1);
    });
  });
});
