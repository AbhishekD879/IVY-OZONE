import { BetErrorService } from './bet-error.service';
import { IBetErrorDoc } from '@betslip/services/betError/bet-error.model';
import { BetError } from '@betslip/services/betError/bet-error';

describe('BetErrorService', () => {
  let betErrorService;
  const betErrorDoc = {
    code: '500',
    subErrorCode: 'SERVER_INTERNAL',
    errorDesc: 'Message',
    outcomeRef: { id: '1' },
    legRef: { documentId: '2' }
  };

  beforeEach(() => {
    betErrorService = new BetErrorService();
  });

  it('should create instance of BetError', () => {
    const result = betErrorService.parse(betErrorDoc as IBetErrorDoc);

    expect(result).toEqual(jasmine.any(BetError));
  });

  it('should parse multiple bet errors', () => {
    const params = [betErrorDoc, {
      code: '500',
      subErrorCode: 'SERVER_INTERNAL',
      errorDesc: 'Message'
    } as IBetErrorDoc];
    const result = betErrorService.parseErrors(params);

    expect(result.length).toEqual(2);
    expect(result[0]).toEqual(jasmine.any(BetError));
    expect(result[1]).toEqual(jasmine.any(BetError));
  });
});
