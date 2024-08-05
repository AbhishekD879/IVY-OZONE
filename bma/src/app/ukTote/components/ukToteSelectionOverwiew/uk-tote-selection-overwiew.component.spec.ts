import { UkToteSelectionOverwiewComponent } from '@uktote/components/ukToteSelectionOverwiew/uk-tote-selection-overwiew.component';
import { IOutcome } from '@core/models/outcome.model';

describe('UkToteSelectionOverwiewComponent', () => {
  let component;
  let pubSubService;

  beforeEach(() => {
    pubSubService =  {
      API: {
        UK_TOTE_LEG_UPDATED: 'UK_TOTE_LEG_UPDATED'
      },
      publish: jasmine.createSpy()
    };
    component = new UkToteSelectionOverwiewComponent(pubSubService);
  });

  it('trackBySelectedOutcome', () => {
    const index = 5;
    const outcome = { id: '8' } as IOutcome;
    const result = component.trackBySelectedOutcome(index, outcome);
    expect(result).toBe('8');
  });

  it('getSelectionName for favourite record', () => {
    const outcome = {
      id: '8',
      runnerNumber: 1,
      isFavourite: true,
      name: '2 N/R'
    };
    const result = component.getSelectionName(outcome);
    expect(result).toBe('2 N/R');
  });

  it('getSelectionName for non favourite record', () => {
    const outcome = {
      id: '8',
      runnerNumber: 1,
      isFavourite: false,
      name: '2 N/R'
    };
    const result = component.getSelectionName(outcome);
    expect(result).toBe('1. 2 N/R');
  });

  it('deselectOutcome', () => {
    component.poolBet = {
      getOutcomeLinkedLeg: jasmine.createSpy().and.returnValue({
        deselectOutcome: jasmine.createSpy(),
      }),
    };
    const outcome = { id: '8' } as IOutcome;
    const linkedLeg = component.poolBet.getOutcomeLinkedLeg(outcome);
    component.deselectOutcome(outcome);
    expect(component.pubsub.publish).toHaveBeenCalledWith(
      component.pubsub.API.UK_TOTE_LEG_UPDATED,
      linkedLeg
    );
  });
});
