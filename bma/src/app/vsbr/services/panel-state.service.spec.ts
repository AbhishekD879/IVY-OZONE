import { PanelStateService } from './panel-state.service';

describe('PanelStateService', () => {
  let service: PanelStateService;

  beforeEach(() => {
    service = new PanelStateService();
  });

  it('changeStatePanel', () => {
    const eventId = 'EID';
    const panelId = 'PID';

    service.changeStatePanel(eventId, panelId);
    expect(service['panelsStates'][eventId][panelId]).toBeTruthy();

    service.changeStatePanel(eventId, panelId);
    expect(service['panelsStates'][eventId][panelId]).toBeFalsy();
  });

  it('getPanelsStates', () => {
    expect(service.getPanelsStates()).toBe(service['panelsStates']);
  });
});
