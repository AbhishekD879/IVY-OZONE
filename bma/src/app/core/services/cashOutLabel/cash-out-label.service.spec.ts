import { CashOutLabelService } from './cash-out-label.service';
describe('CashOutLabelService', () => {
  let service: CashOutLabelService;
  let event;

  beforeEach(() => {
    service = new CashOutLabelService();

    event = {
      cashoutAvail: 'Y,YES,'
    };
  });

  describe('checkCondition', () => {
    it('no cashoutAvail on event level', () => {
      expect(service.checkCondition({} as any, [])).toBeFalsy();
    });

    it('checkForValid', () => {
      expect(service.checkCondition(event, [{ cashoutAvail: 'Y' }])).toBeTruthy();
    });

    it('checkForValid', () => {
      expect(service.checkCondition(event, [{ cashoutAvail: 'YES' }])).toBeTruthy();
    });
  });
});
