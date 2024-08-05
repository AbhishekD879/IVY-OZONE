
export interface IBetError {
  code?: string;
  subCode?: string;
  desc?: string;
  outcomeId?: string;
  legDocId?: string;
  live?: any;
  // [ key: string ]: any;
}

export interface IBetErrorDoc {
  code: string;
  subErrorCode: string;
  errorDesc: string;
  outcomeRef?: { id: string; };
  legRef: { documentId: string; };
}
