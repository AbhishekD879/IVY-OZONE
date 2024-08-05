import {
  ForcastTricastRaceCardComponent
} from '@lazy-modules/forecastTricast/components/forecastTricastRaceCard/forecast-tricast-race-card.component';

describe('ForcastTricastRaceCardComponent', () => {
  let component: ForcastTricastRaceCardComponent;
  let filterService;

  beforeEach(() => {
    filterService = {
      removeLineSymbol: jasmine.createSpy().and.returnValue('Name without line')
    };

    createComponent();

    component.outcomeEntity = {
      id: 'outcomeEntityId',
      isFavourite: false
    } as any;
    component.marketEntity = {
      id: 'marketEntityId'
    } as any;
    component.eventEntity = {
      id: 'eventEntityId'
    } as any;
  });

  function createComponent() {
    component = new ForcastTricastRaceCardComponent(
      filterService,
    );
  }
  it('constructor', () => {
    expect(component).toBeTruthy();
  });


  describe('ngOnInit', () => {
    it('card should be available', () => {
      component.ngOnInit();

      expect(component.isOutcomeCardAvailable).toEqual(true);
    });

    it('card should not be available', () => {
      component.marketEntity = undefined;
      component.ngOnInit();

      expect(component.isOutcomeCardAvailable).toEqual(false);
    });

    it('should display runner number', () => {
      component.ngOnInit();

      expect(component.runnerNumberDisplay).toEqual(true);
    });

    it('should not display runner number when it is unnamed favourite', () => {
      component.outcomeEntity.isFavourite = true;
      component.ngOnInit();

      expect(component.runnerNumberDisplay).toEqual(false);
    });
  });

  it('nameWithoutLineSymbol', () => {
    const actualResult = component['nameWithoutLineSymbol']('Name with line');

    expect(actualResult).toEqual('Name without line');
  });

  it('isNumberNeeded', () => {
    const outcome = {
      runnerNumber: '1'
    } as any;
    const actualResult = component['isNumberNeeded'](outcome);

    expect(actualResult).toEqual(true);
  });
});
