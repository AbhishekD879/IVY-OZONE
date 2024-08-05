import { BetStatusIndicatorComponent } from './bet-status-indicator.component';

describe('BetStatusIndicatorComponent', () => {
  let component;

  beforeEach(() => {
    component = new BetStatusIndicatorComponent();
  });

  it('should return icon status', () => {
    component.status = 'Won';
    expect(component.iconStatusName).toEqual('#bet-status-won');

    component.status = 'Lose';
    expect(component.iconStatusName).toEqual('#bet-status-lose');

    component.status = 'Winning';
    expect(component.iconStatusName).toEqual('#bet-status-arrow-up');

    component.status = 'Losing';
    expect(component.iconStatusName).toEqual('#bet-status-arrow-down');

    component.status = '';
    expect(component.iconStatusName).toEqual('');
  });
});
