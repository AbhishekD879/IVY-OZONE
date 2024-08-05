
import { OUTRIGHTS_CONFIG } from '@core/constants/outrights-config.constant';

export const liveChannelsEventData = [
    {
        "id": 1935847,
        "liveServChannels": "sEVENT0001935847,",
        "liveServChildrenChannels": "SEVENT0001935847,",
        "children": [
            {
                "market": {
                    "id": "41781590",
                    "liveServChannels": "sEVMKT0041781590,",
                    "liveServChildrenChannels": "SEVMKT0041781590,",
                    "children": [
                        {
                            "outcome": {
                                "id": "157769521",
                                "liveServChannels": "sSELCN0157769521,",
                                "liveServChildrenChannels": "SSELCN0157769521,",
                            }
                        }
                    ]
                }
            }
        ]
    }
];

export const GEN_FILTER_PARAMS = {
    siteChannels: 'M',
    isNotResulted: true,
    eventSortCode: OUTRIGHTS_CONFIG.sportSortCode,
    outcomeTeamExtIds: '4dsgumo7d4zupm2ugsvm4zm4d',
    suspendAtTime: '2022-03-23T13:37:30.000Z'
};

export const REQUEST_PARAMS = {
    "typeId": "442,443,441,440,115086,434,436,438",
    "simpleFilters": "simpleFilter=event.siteChannels:contains:M&simpleFilter=event.isResulted:isFalse&simpleFilter=event.eventSortCode:intersects:TNMT,TR01,TR02,TR03,TR04,TR05,TR06,TR07,TR08,TR09,TR10,TR11,TR12,TR13,TR14,TR15,TR16,TR17,TR18,TR19,TR20&simpleFilter=outcome.teamExtIds:intersects:4dsgumo7d4zupm2ugsvm4zm4d&simpleFilter=event.suspendAtTime:greaterThan:2022-03-23T14:12:00.000Z"
};

export const EVENT_ENTITY = [
    {
        "id": 1963013,
        "name": "Premier League 2021/22",
        "eventStatusCode": "A",
        "isActive": true,
        "isDisplayed": true,
        "displayOrder": 0,
        "siteChannels": "@,B,C,D,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z,e,f,p,t,y,z,",
        "eventSortCode": "TNMT",
        "startTime": "1650539880000",
        "rawIsOffCode": "-",
        "classId": 97,
        "typeId": "442",
        "sportId": "16",
        "liveServChannels": "sEVENT0001963013,",
        "liveServChildrenChannels": "SEVENT0001963013,",
        "categoryId": "16",
        "categoryCode": "FOOTBALL",
        "categoryName": "Football",
        "categoryDisplayOrder": "10",
        "className": "Football England",
        "classDisplayOrder": 0,
        "classSortCode": "FB",
        "classFlagCodes": "UF,CN,EP,LI,ER,",
        "typeName": "Premier League",
        "typeDisplayOrder": 0,
        "typeFlagCodes": "FI,IVA,UK,QL,AVA,INT,FE,",
        "isOpenEvent": "true",
        "drilldownTagNames": "EVFLAG_FE,EVFLAG_FI,EVFLAG_AVA,",
        "isAvailable": "true",
        "cashoutAvail": "Y",
        "children": [
            {
                "market": {
                    "id": "41947302",
                    "eventId": "1963013",
                    "templateMarketId": 37243,
                    "templateMarketName": "Outright",
                    "collectionIds": "9982,9734,9951,10012,",
                    "collectionNames": "collection1012,collection0211,collection today,TRCollection,",
                    "marketMeaningMajorCode": "-",
                    "marketMeaningMinorCode": "--",
                    "name": "Outright",
                    "isLpAvailable": true,
                    "displayOrder": 4000,
                    "marketStatusCode": "A",
                    "isActive": true,
                    "isDisplayed": true,
                    "siteChannels": "C,I,M,P,Q,U,",
                    "liveServChannels": "sEVMKT0041947302,",
                    "liveServChildrenChannels": "SEVMKT0041947302,",
                    "priceTypeCodes": "LP,",
                    "isAvailable": "true",
                    "maxAccumulators": "25",
                    "minAccumulators": "1",
                    "cashoutAvail": "Y",
                    "termsWithBet": "Y",
                    "children": [
                        {
                            "outcome": {
                                "id": "158830269",
                                "marketId": "41947302",
                                "name": "Arsenal FC",
                                "outcomeMeaningMajorCode": "--",
                                "displayOrder": 0,
                                "outcomeStatusCode": "A",
                                "isActive": true,
                                "isDisplayed": true,
                                "siteChannels": "P,Q,C,U,I,M,",
                                "liveServChannels": "sSELCN0158830269,",
                                "liveServChildrenChannels": "SSELCN0158830269,",
                                "isAvailable": "true",
                                "teamExtIds": "4dsgumo7d4zupm2ugsvm4zm4d,",
                                "children": [
                                    {
                                        "price": {
                                            "id": "1",
                                            "priceType": "LP",
                                            "priceNum": 5,
                                            "priceDen": 3,
                                            "priceDec": 2.67,
                                            "isActive": true,
                                            "displayOrder": "1"
                                        }
                                    }
                                ],
                                "prices": [
                                    {
                                        "id": "1",
                                        "priceType": "LP",
                                        "priceNum": 5,
                                        "priceDen": 3,
                                        "priceDec": 2.67,
                                        "isActive": true,
                                        "displayOrder": "1"
                                    }
                                ]
                            }
                        }
                    ],
                    "outcomes": [
                        {
                            "id": "158830269",
                            "marketId": "41947302",
                            "name": "Arsenal FC",
                            "outcomeMeaningMajorCode": "--",
                            "displayOrder": 0,
                            "outcomeStatusCode": "A",
                            "isActive": true,
                            "isDisplayed": true,
                            "siteChannels": "P,Q,C,U,I,M,",
                            "liveServChannels": "sSELCN0158830269,",
                            "liveServChildrenChannels": "SSELCN0158830269,",
                            "isAvailable": "true",
                            "teamExtIds": "4dsgumo7d4zupm2ugsvm4zm4d,",
                            "prices": [
                                {
                                    "id": "1",
                                    "priceType": "LP",
                                    "priceNum": 5,
                                    "priceDen": 3,
                                    "priceDec": 2.67,
                                    "isActive": true,
                                    "displayOrder": "1"
                                }
                            ]
                        }
                    ]
                }
            }
        ],
        "responseCreationTime": "2022-03-23T14:01:34.497Z",
        "localTime": "4:48",
        "isUS": false,
        "markets": [
            {
                "id": "41947302",
                "eventId": "1963013",
                "templateMarketId": 37243,
                "templateMarketName": "Outright",
                "collectionIds": "9982,9734,9951,10012,",
                "collectionNames": "collection1012,collection0211,collection today,TRCollection,",
                "marketMeaningMajorCode": "-",
                "marketMeaningMinorCode": "--",
                "name": "Outright",
                "isLpAvailable": true,
                "displayOrder": 4000,
                "marketStatusCode": "A",
                "isActive": true,
                "isDisplayed": true,
                "siteChannels": "C,I,M,P,Q,U,",
                "liveServChannels": "sEVMKT0041947302,",
                "liveServChildrenChannels": "SEVMKT0041947302,",
                "priceTypeCodes": "LP,",
                "isAvailable": "true",
                "maxAccumulators": "25",
                "minAccumulators": "1",
                "cashoutAvail": "Y",
                "termsWithBet": "Y",
                "outcomes": [
                    {
                        "id": "158830269",
                        "marketId": "41947302",
                        "name": "Arsenal FC",
                        "outcomeMeaningMajorCode": "--",
                        "displayOrder": 0,
                        "outcomeStatusCode": "A",
                        "isActive": true,
                        "isDisplayed": true,
                        "siteChannels": "P,Q,C,U,I,M,",
                        "liveServChannels": "sSELCN0158830269,",
                        "liveServChildrenChannels": "SSELCN0158830269,",
                        "isAvailable": "true",
                        "teamExtIds": "4dsgumo7d4zupm2ugsvm4zm4d,",
                        "prices": [
                            {
                                "id": "1",
                                "priceType": "LP",
                                "priceNum": 5,
                                "priceDen": 3,
                                "priceDec": 2.67,
                                "isActive": "true",
                                "displayOrder": "1"
                            }
                        ]
                    }
                ],
                "terms": "Each Way: undefined/undefined odds - places "
            }
        ],
        "correctedDay": "sb.dayThursday",
        "correctedDayValue": "sb.dayThursday",
        "liveEventOrder": 1
    }
];

export const typeEventsSSResponse = {
    "SSResponse": {
        "xmlns": "http://schema.openbet.com/SiteServer/2.31/SSResponse.xsd",
        "children": [
            {
                "event": {
                    "id": "1963013",
                    "name": "Premier League 2021/22",
                    "eventStatusCode": "A",
                    "isActive": true,
                    "isDisplayed": true,
                    "displayOrder": "0",
                    "siteChannels": "@,B,C,D,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z,e,f,p,t,y,z,",
                    "eventSortCode": "TNMT",
                    "startTime": "2022-04-21T11:18:00Z",
                    "rawIsOffCode": "-",
                    "classId": "97",
                    "typeId": "442",
                    "sportId": "16",
                    "liveServChannels": "sEVENT0001963013,",
                    "liveServChildrenChannels": "SEVENT0001963013,",
                    "categoryId": "16",
                    "categoryCode": "FOOTBALL",
                    "categoryName": "Football",
                    "categoryDisplayOrder": "10",
                    "className": "Football England",
                    "classDisplayOrder": "0",
                    "classSortCode": "FB",
                    "classFlagCodes": "UF,CN,EP,LI,ER,",
                    "typeName": "Premier League",
                    "typeDisplayOrder": "0",
                    "typeFlagCodes": "FI,IVA,UK,QL,AVA,INT,FE,",
                    "isOpenEvent": "true",
                    "drilldownTagNames": "EVFLAG_FE,EVFLAG_FI,EVFLAG_AVA,",
                    "isAvailable": "true",
                    "cashoutAvail": "Y",
                    "children": [
                        {
                            "market": {
                                "id": "41947302",
                                "eventId": "1963013",
                                "templateMarketId": 37243,
                                "templateMarketName": "Outright",
                                "collectionIds": "9982,9734,9951,10012,",
                                "collectionNames": "collection1012,collection0211,collection today,TRCollection,",
                                "marketMeaningMajorCode": "-",
                                "marketMeaningMinorCode": "--",
                                "name": "Outright",
                                "isLpAvailable": true,
                                "displayOrder": "4000",
                                "marketStatusCode": "A",
                                "isActive": true,
                                "isDisplayed": true,
                                "siteChannels": "C,I,M,P,Q,U,",
                                "liveServChannels": "sEVMKT0041947302,",
                                "liveServChildrenChannels": "SEVMKT0041947302,",
                                "priceTypeCodes": "LP,",
                                "isAvailable": "true",
                                "maxAccumulators": "25",
                                "minAccumulators": "1",
                                "cashoutAvail": "Y",
                                "termsWithBet": "Y",
                                "children": [
                                    {
                                        "outcome": {
                                            "id": "158830269",
                                            "marketId": "41947302",
                                            "name": "Arsenal FC",
                                            "outcomeMeaningMajorCode": "--",
                                            "displayOrder": "0",
                                            "outcomeStatusCode": "A",
                                            "isActive": true,
                                            "isDisplayed": true,
                                            "siteChannels": "P,Q,C,U,I,M,",
                                            "liveServChannels": "sSELCN0158830269,",
                                            "liveServChildrenChannels": "SSELCN0158830269,",
                                            "isAvailable": "true",
                                            "teamExtIds": "4dsgumo7d4zupm2ugsvm4zm4d,",
                                            "children": [
                                                {
                                                    "price": {
                                                        "id": "1",
                                                        "priceType": "LP",
                                                        "priceNum": "5",
                                                        "priceDen": "3",
                                                        "priceDec": "2.67",
                                                        "isActive": true,
                                                        "displayOrder": "1"
                                                    }
                                                }
                                            ]
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            },
            {
                "responseFooter": {
                    "cost": "497",
                    "creationTime": "2022-03-23T14:01:34.497Z"
                }
            }
        ]
    }
};

export const STRIP_EVENT_ENTITY = [
    {
        "event": {
            "id": "1963013",
            "name": "Premier League 2021/22",
            "eventStatusCode": "A",
            "isActive": "true",
            "isDisplayed": "true",
            "displayOrder": "0",
            "siteChannels": "@,B,C,D,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z,e,f,p,t,y,z,",
            "eventSortCode": "TNMT",
            "startTime": "2022-04-21T11:18:00Z",
            "rawIsOffCode": "-",
            "classId": "97",
            "typeId": "442",
            "sportId": "16",
            "liveServChannels": "sEVENT0001963013,",
            "liveServChildrenChannels": "SEVENT0001963013,",
            "categoryId": "16",
            "categoryCode": "FOOTBALL",
            "categoryName": "Football",
            "categoryDisplayOrder": "10",
            "className": "Football England",
            "classDisplayOrder": "0",
            "classSortCode": "FB",
            "classFlagCodes": "UF,CN,EP,LI,ER,",
            "typeName": "Premier League",
            "typeDisplayOrder": "0",
            "typeFlagCodes": "FI,IVA,UK,QL,AVA,INT,FE,",
            "isOpenEvent": "true",
            "drilldownTagNames": "EVFLAG_FE,EVFLAG_FI,EVFLAG_AVA,",
            "isAvailable": "true",
            "cashoutAvail": "Y",
            "children": [
                {
                    "market": {
                        "id": "41947302",
                        "eventId": "1963013",
                        "templateMarketId": "37243",
                        "templateMarketName": "Outright",
                        "collectionIds": "9982,9734,9951,10012,",
                        "collectionNames": "collection1012,collection0211,collection today,TRCollection,",
                        "marketMeaningMajorCode": "-",
                        "marketMeaningMinorCode": "--",
                        "name": "Outright",
                        "isLpAvailable": "true",
                        "displayOrder": "4000",
                        "marketStatusCode": "A",
                        "isActive": "true",
                        "isDisplayed": "true",
                        "siteChannels": "C,I,M,P,Q,U,",
                        "liveServChannels": "sEVMKT0041947302,",
                        "liveServChildrenChannels": "SEVMKT0041947302,",
                        "priceTypeCodes": "LP,",
                        "isAvailable": "true",
                        "maxAccumulators": "25",
                        "minAccumulators": "1",
                        "cashoutAvail": "Y",
                        "termsWithBet": "Y",
                        "children": [
                            {
                                "outcome": {
                                    "id": "158830269",
                                    "marketId": "41947302",
                                    "name": "Arsenal FC",
                                    "outcomeMeaningMajorCode": "--",
                                    "displayOrder": "0",
                                    "outcomeStatusCode": "A",
                                    "isActive": "true",
                                    "isDisplayed": "true",
                                    "siteChannels": "P,Q,C,U,I,M,",
                                    "liveServChannels": "sSELCN0158830269,",
                                    "liveServChildrenChannels": "SSELCN0158830269,",
                                    "isAvailable": "true",
                                    "teamExtIds": "4dsgumo7d4zupm2ugsvm4zm4d,",
                                    "children": [
                                        {
                                            "price": {
                                                "id": "1",
                                                "priceType": "LP",
                                                "priceNum": "5",
                                                "priceDen": "3",
                                                "priceDec": "2.67",
                                                "isActive": "true",
                                                "displayOrder": "1"
                                            }
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                }
            ],
            "responseCreationTime": "2022-03-24T09:52:57.962Z"
        }
    }
];
