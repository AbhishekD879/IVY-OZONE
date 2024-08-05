import {
  CardViewComponent
} from '@app/bigCompetitions/components/outrightCard/outright-card.component';
import { IMarket } from '@core/models/market.model';
import { IOutcome } from '@core/models/outcome.model';

describe('CardViewComponent', () => {

  let component: CardViewComponent;

  const market = {
    outcomes: [{}, {}, {}]
  } as IMarket;

  beforeEach(() => {
    component = new CardViewComponent();
    component.market = market;
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('#ngOnInit', () => {
    component.maxDisplay = 2;
    component.ngOnInit();
    expect(component.limit).toBe(2);
    expect(component.hideShowNext).toBeTruthy();
  });

  it('should set correct properties', () => {
    component.limit = 2;
    component.maxDisplay = 3;
    component.showNext();
    expect(component.limit).toBe(5);
    expect(component.hideShowNext).toBeFalsy();
  });

  it('should return correct result', () => {
    const item = { id: '13' } as IOutcome;
    const index = 7;
    expect(component.trackByFn(index, item)).toBe('713');
  });

  it('should return correct result and set properties', () => {
    const participants = {
      HOME: {
        name: 'HOME TEAM',
        abbreviation: ''
      },
      AWAY: null
    };
    component.limit = 2;
    const result = component.getOutcomeName(participants);
    expect(component.hideShowNext).toBeTruthy();
    expect(result).toBe('HOME TEAM');
  });

  it('should return correct result and set properties', () => {
    const participants = {
      HOME: {
        name: 'HOME TEAM',
        abbreviation: ''
      },
      AWAY: {
        name: 'AWAY TEAM',
        abbreviation: ''
      }
    };
    component.limit = 5;
    const result = component.getOutcomeName(participants);
    expect(component.hideShowNext).toBeFalsy();
    expect(result).toBe('HOME TEAM vs AWAY TEAM');
  });
});
