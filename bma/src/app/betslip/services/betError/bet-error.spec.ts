import { BetError } from './bet-error';
import { IBetErrorDoc } from '@betslip/services/betError/bet-error.model';

describe('BetError', () => {
  it('should create instance of BetError with passed params', () => {
    const params = {
      code: '500',
      subErrorCode: 'SERVER_INTERNAL',
      errorDesc: 'Message'
    };

    expect(new BetError(params as IBetErrorDoc)).toEqual(jasmine.objectContaining({
      code: params.code,
      subCode: params.subErrorCode,
      desc: params.errorDesc,
      outcomeId: undefined,
      legDocId: undefined
    }));
  });

  it('should create instance of BetError with passed legDocId and outcomeId', () => {
    const params = {
      code: '500',
      subErrorCode: 'SERVER_INTERNAL',
      errorDesc: 'Message',
      outcomeRef: { id: '1' },
      legRef: { documentId: '2' }
    };

    expect(new BetError(params as IBetErrorDoc)).toEqual(jasmine.objectContaining({
      outcomeId: params.outcomeRef.id,
      legDocId: params.legRef.documentId
    }));
  });
});
