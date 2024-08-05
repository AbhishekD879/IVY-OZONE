import { EditMyAccaHistoryListComponent } from './edit-my-acca-history-list.component';

describe('EditMyAccaHistoryListComponent', () => {
  let component;

  beforeEach(() => {
    component = new EditMyAccaHistoryListComponent();
  });

  it('expandBet', () => {
    const bet: any = {
      eventSource: {
        accaHistory: {}
      }
    };

    component.expandBet(bet);
    expect(bet.eventSource.accaHistory.isExpanded).toBeTruthy();

    component.expandBet(bet);
    expect(bet.eventSource.accaHistory.isExpanded).toBeFalsy();
  });

  it('trackBet', () => {
    expect(
      component.trackBet(0, { eventSource: { id: '1' } } as any)
    ).toBe('1');
  });
});
