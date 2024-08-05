import { IBetErrorDoc } from '@betslip/services/betError/bet-error.model';

export class BetError {

  code: string;
  subCode: string;
  desc: string;
  outcomeId: string;
  legDocId: string;

  constructor(params: IBetErrorDoc) {
    this.code = params.code;
    this.subCode = params.subErrorCode;
    this.desc = params.errorDesc;
    this.outcomeId = params.outcomeRef && params.outcomeRef.id;
    this.legDocId = params.legRef && params.legRef.documentId;
  }
}


