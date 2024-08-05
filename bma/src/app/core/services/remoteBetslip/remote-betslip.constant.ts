export interface IRemoteBetslipRequestConfig {
  [ key: string ]: string;
}

export interface IRemoteBetslipProviderConfig {
  [ key: string ]: IRemoteBetslipRequestConfig;
}

export interface IRemoteBetslipBet {
  currency: string;
  price: string;
  stake: string;
  token: string;
  winType: string;
  clientUserAgent: string;
}

export const enum BETSLIP {
  QUICKBET = 'QUICK_BET'
}

export const remoteBetslipConstant = {
  general: {
    sessionInit: '30000',
    sessionClear: '30003',
    error: 'ERROR'
  },
  sgl: {
    add: {
      request: '30001',
      success: '31001',
      error: '31002'
    },
    remove: {
      request: '30002',
      success: '30003'
    },
    placeBet: {
      request: '30011',
      success: ['30012'],
      overask: '30031',
      error: '31012',
      bir: '30013',
    },
  luckyDipPlaceBet:{
    request: '30022',
      success: ['30012'],
      overask: '30031',
      error: '31012'
  }
  },
  ds: {
    add: {
      request: '40001',
      success: '41001',
      error: '41002',
      change: '41003'
    },
    remove: {
      request: '30002',
      success: '30003'
    },
    placeBet: {
      request: '40011',
      success: '41101',
      error: '41102'
    }
  },
  byb: {
    add: {
      request: '50001',
      success: '51001',
      error: '51002',
      change: '' // TODO: check
    },
    remove: {
      request: '30002',
      success: '30003'
    },
    placeBet: {
      request: '50011',
      success: '51101',
      error: '51102'
    }
  }
};
