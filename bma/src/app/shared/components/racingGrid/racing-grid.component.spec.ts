import { RacingGridComponent } from './racing-grid.component';

describe('RacingGridComponent', () => {
  let component: RacingGridComponent;

  let horseRacingService;
  let greyhoundService;

  beforeEach(() => {
    horseRacingService = {
      _getByTabCb: null,
      getByTab: jasmine.createSpy('getByTab').and
        .returnValue({ then: cb => horseRacingService._getByTabCb = cb }),
      addFirstActiveEventProp: jasmine.createSpy('addFirstActiveEventProp')
    };
    greyhoundService = {
      _getByTabCb: null,
      getByTab: jasmine.createSpy('getByTab').and
        .returnValue({ then: cb => greyhoundService._getByTabCb = cb }),
      addFirstActiveEventProp: jasmine.createSpy('addFirstActiveEventProp')
    };
    component = new RacingGridComponent(horseRacingService, greyhoundService);
    component.raceGridRaces = {} as any;
  });

  describe('ngOnInit', () => {
    describe('if sport is not horseracing or greyhound', () => {
      beforeEach(() => {
        component.sportId = '0';
        component.ngOnInit();
      });
      it('sportName and eventsOrder properties should not be set', () => {
        expect(component.sportName).not.toBeDefined();
        expect(component.eventsOrder).not.toBeDefined();
      });
      it('should not invoke getByTab service method or update racing property', () => {
        expect(horseRacingService.getByTab).not.toHaveBeenCalled();
        expect(greyhoundService.getByTab).not.toHaveBeenCalled();
        expect(component.racing).not.toBeDefined();
      });
    });

    describe('should set sportName and eventsOrder properties', () => {
      it('for greyhound', () => {
        component.sportId = '19';
        component.ngOnInit();
        expect(component.sportName).toEqual('greyhound');
      });
      it('for horseracing', () => {
        component.sportId = '21';
        component.ngOnInit();
        expect(component.sportName).toEqual('horseracing');
      });
      afterEach(() => {
        expect(component.eventsOrder).toEqual(['startTime', 'name']);
      });
    });

    describe('should invoke getByTab service method and update racing property', () => {
      let services;

      it('for greyhound', () => {
        component.sportId = '19';
        services = [greyhoundService, horseRacingService];
      });
      it('for horseracing', () => {
        component.sportId = '21';
        services = [horseRacingService, greyhoundService];
      });

      afterEach(() => {
        component.ngOnInit();
        const result = Symbol('result');
        expect(services[1].getByTab).not.toHaveBeenCalled();
        expect(services[0].getByTab).toHaveBeenCalledWith('today', true);
        services[0]._getByTabCb(result as any);

        expect(component.racing).toEqual(result as any);
        expect(services[0].addFirstActiveEventProp).toHaveBeenCalledWith(result);
        expect(component.raceGridRaces.data).toEqual(result as any);
      });
    });

    describe('should not invoke getByTab service method and update racing property', () => {
      it('for greyhound', () => {
        component.sportId = '19';
      });
      it('for horseracing', () => {
        component.sportId = '21';
      });
      afterEach(() => {
        const data = Symbol('data');
        component.raceGridRaces.data = data as any;
        component.ngOnInit();

        expect(component.racing).toEqual(data as any);
        expect(greyhoundService.getByTab).not.toHaveBeenCalled();
        expect(horseRacingService.getByTab).not.toHaveBeenCalled();
      });
    });
  });

  describe('isRaceGridGroup', () => {
    beforeEach(() => {
      component.raceGridRaces.data = {
        classesTypeNames: { A: [0], B: [], VR: [0], ALL: [0] }
      };
    });

    it('should return true', () => {
      expect(component.isRaceGridGroup({ flag: 'A' })).toEqual(true);
    });
    it('should return false', () => {
      expect(component.isRaceGridGroup({ flag: 'B' })).toEqual(false);
      expect(component.isRaceGridGroup({ flag: 'VR' })).toEqual(false);
      expect(component.isRaceGridGroup({ flag: 'ALL' })).toEqual(false);
    });
  });

  describe('trackByGroupedRacing', () => {
    it('should return track string', () => {
      expect(component.trackByGroupedRacing(2, { data: [{ id: 'id1' }, { id: 'id2' }] }))
        .toEqual('2_id1|id2');
    });
  });
});
