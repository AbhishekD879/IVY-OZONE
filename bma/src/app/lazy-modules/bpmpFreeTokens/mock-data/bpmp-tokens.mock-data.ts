export const cmsServiceBetPackData = {
    "ViewAllTokenLink": "/betbundle-market",
    "ViewAllTokenLabel": "View All Tokens"
}

export const betpackCmsServiceBetPackDetailsData = [{
    "betPackId": "37204",
    "betPackTokenList": [{
        "id": "35803",
        "tokenId": "35803",
        "tokenTitle": "Weekend 35803",
        "tokenValue": 1,
        "deepLinkUrl": "/football",
        "active": false
    },
    {
        "id": "35804",
        "tokenId": "35804",
        "tokenTitle": "football 35804",
        "tokenValue": 1,
        "deepLinkUrl": "/football",
        "active": false
    },
    {
        "id": "35805",
        "tokenId": "35805",
        "tokenTitle": "wertyu",
        "tokenValue": 1,
        "deepLinkUrl": "/football",
        "active": false
    }]
}]

export const freeBetsServiceFreeBetsData = [{
    "tokenId": "35805",
    "freebetOfferId": "37204",
    "freebetOfferCategories": {
        "freebetOfferCategory": "Bet Pack"
    },
    "freebetTokenExpiryDate": "2022-08-31 10:35:00"
},
{
    "tokenId": "35803",
    "freebetOfferId": "37204",
    "freebetOfferCategories": {
        "freebetOfferCategory": "Bet Pack"
    },
    "freebetTokenExpiryDate": "2022-08-31 10:35:00"
}]

export const cmsTokenDataEqualsUserTokenData = [{
    "betPackId": "37204",
    "betPackTokenList": [{
        "id": "35803",
        "tokenId": "35803",
        "tokenTitle": "1eekend 35803",
        "tokenValue": 1,
        "deepLinkUrl": "/football",
        "active": false
    },
    {
        "id": "35804",
        "tokenId": "35804",
        "tokenTitle": "football 35804",
        "tokenValue": 1,
        "deepLinkUrl": "/football",
        "active": false
    },
    {
        "id": "35805",
        "tokenId": "35805",
        "tokenTitle": "3ertyu",
        "tokenValue": 1,
        "deepLinkUrl": "/football",
        "active": false
    }]
}]

export const availabletokenData = [
    {
        "tokenTitle": "$1eekend 35803",
        "tokenExpiryDate": "string",
        "useNowLink": "/football"
    },
    {
        "tokenTitle": "$3ertyu",
        "tokenExpiryDate": "string",
        "useNowLink": "/football"
    }
]

export const cmsTokenDataNotEqualsTouserTokenData = [
    {
        "tokenId": "9999",
        "freebetOfferId": "37204",
        "freebetOfferCategories": {
            "freebetOfferCategory": "Bet Pack"
        },
        "freebetTokenExpiryDate": "2022-08-31 10:35:00"
    }
]

export const cmsBetPackIdNotEqualsUserOfferId = [
    {
        "tokenId": "35803",
        "freebetOfferId": "99999",
        "freebetOfferCategories": {
            "freebetOfferCategory": "Bet Pack"
        },
        "freebetTokenExpiryDate": "2022-08-31 10:35:00"
    }
]

export const NofreebetOfferCategories = [
    {
        "tokenId": "9999",
        "freebetOfferId": "37204",
        "freebetTokenExpiryDate": "2022-08-31 10:35:00"
    }
]

export const NobetPackOffer = [
    {
        "tokenId": "9999",
        "freebetOfferId": "37204",
        "freebetOfferCategories": {
            "freebetOfferCategory": "Not a Bet Pack"
        },
        "freebetTokenExpiryDate": "2022-08-31 10:35:00"
    }
]