export const EVENTS_DATA = [{
    liveServChannels: '',
    eventStatusCode: 'S',
    id: '1234',
    markets: [{
        isLpAvailable: true,
        isSpAvailable: true,
        liveServChannels: '',
        eventId: '1234',
        id: '1234',
        outcomes: [{
            id: '1234',
            marketId: '1234',
            liveServChannels: '',
            outcomeMeaningMinorCode: '3',
            prices: []
        }]
    }]
}, {
    liveServChannels: '',
    id: '1234',
    markets: [{
        isLpAvailable: true,
        isSpAvailable: true,
        liveServChannels: '',
        marketStatusCode: 'S',
        id: '12345',
        eventId: '1234',
        outcomes: [{
            liveServChannels: '',
            id: '123456',
            marketId: '12345',
            outcomeMeaningMinorCode: '2',
            prices: []
        }]
    }]
}, {
    liveServChannels: '',
    id: '1234',
    markets: [{
        liveServChannels: '',
        id: '12345',
        eventId: '1234',
        isEachWayAvailable: true,
        isLpAvailable: true,
        isSpAvailable: false,
        outcomes: [{
            outcomeStatusCode: 'S',
            id: '123456',
            marketId: '12345',
            liveServChannels: '',
            prices: []
        }]
    }]
}, {
    isStarted: true,
    id: '1234',
    liveServChannels: '',
    markets: [{
        id: '12345',
        eventId: '1234',
        liveServChannels: '',
        priceTypeCodes: 'SP',
        outcomes: [{
            id: '123456',
            marketId: '12345',
            liveServChannels: '',
            prices: []
        }]
    }]
}, {
    liveServChannels: '',
    id: '1234',
    markets: [{
        liveServChannels: '',
        priceTypeCodes: 'LP',
        id: '12345',
        eventId: '1234',
        outcomes: [{
            id: '123456',
            marketId: '12345',
            liveServChannels: '',
            prices: [{ priceNum: 1, priceDen: 2 }]
        }]
    }]
},
{
    liveServChannels: '',
    id: '1234',
    markets: []
},
{
    liveServChannels: '',
    id: '1234',
    markets: [{
        liveServChannels: '',
        id: '12345',
        eventId: '1234',
        priceTypeCodes: 'LP',
        outcomes: []
    }]
},
{
    liveServChannels: '',
    eventStatusCode: 'S',
    id: '1234',
    markets: [{
        isLpAvailable: true,
        isSpAvailable: true,
        liveServChannels: '',
        id: '12345',
        eventId: '1234',
        outcomes: [{
            id: '123234',
            liveServChannels: '',
            marketId: '12345',
            outcomeMeaningMinorCode: '3',
            prices: []
        }]
    }]
}
];

export const UPDATE_CASE = {
    CASE_A: {
        type: 'MESSAGE',
        message: {
            lp_num: 1,
            lp_den: 1,
            status: 'S',
            displayed: 'Y'
        },
        channel: {
            id: '123'
        }
    },
    CASE_B: {
        type: 'MESSAGES',
        message: {
            lp_num: 1,
            lp_den: 1,
            status: 'S',
            displayed: 'Y'
        },
        channel: {
            id: '123'
        }
    },
    CASE_C: {
        type: 'MESSAGES',
        message: {
            lp_num: 1,
            lp_den: 1,
            status: 'S',
            displayed: 'Y'
        },
        channel: {
            id: '123'
        }
    },
    CASE_D: {
        type: 'MESSAGE',
        message: {
            status: 'A',
            displayed: 'Y'
        },
        channel: {
            id: 'M123'
        }
    },
    CASE_E: {
        type: 'MESSAGE',
        message: {
            lp_num: 1,
            lp_den: 1,
            displayed: 'Y'
        },
        channel: {
            id: '123'
        }
    }
};
