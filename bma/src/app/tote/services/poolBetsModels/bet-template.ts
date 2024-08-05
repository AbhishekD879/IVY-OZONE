export const BET_TEMPLATE = {
  betslip: {
    documentId: '1',
    stake: {
      amount: 0,
      currencyRef: {
        id: ''
      }
    },
    clientUserAgent: '',
    isAccountBet: 'Y',
    slipPlacement: {
      IPAddress: '91.232.241.59',
      channelRef: {
        id: ''
      }
    },
    betRef: [{
      documentId: '1'
    }]
  },
  leg: [{
    documentId: '1',
    poolLeg: {
      poolRef: {
        id: ''
      },
      legPart: []
    }
  }],
  bet: [{
    documentId: '1',
    betslipRef: {
      documentId: '1'
    },
    betTypeRef: {
      id: ''
    },
    stake: {
      stakePerLine: 0,
      amount: 0,
      currencyRef: {
        id: ''
      }
    },
    lines: {
      number: '1'
    },
    legRef: [{
      documentId: '1',
      ordering: '1'
    }]
  }]
};
