import { BetShare } from "@app/client/private/models/betShare.model";
import { FTPBETSHARING_CONFIG } from "./bet-sharing-overlay.constants";

export const BET_SHARE_MOCK_VALUES: BetShare = {
    shareCardImageFileName:'test',
    popUpDesc:"Let’s generate a picture to share. What would you like to display on this picture?"
    ,id:"6417632a33e792398f8630a6","createdBy":"5645b8a220bd9e0800afdc57",
    createdByUserName:null,updatedBy:"5645b8a220bd9e0800afdc57",
    updatedByUserName:null,createdAt:"2023-03-19T19:31:54.636Z",updatedAt:"2023-03-21T11:24:54.626Z"
    ,brand:"bma",horseRacingUrl:"https://scmedia.cms.test.env.works/$-$/9173a212658d46cdbb483225b87de755.jpeg",
    footBallUrl:"https://scmedia.itsfogo.com/$-$/5539b5e8d1cc4b6595ea27657d46ce3f.jpg",
    url5ASide:"",
    brandLogoUrl:"https://scmedia.itsfogo.com/$-$/7f10c18c8ae340a9b08219809b3ccd21.svg",
    settledBetsGenericUrl:"https://scmedia.itsfogo.com/$-$/5539b5e8d1cc4b6595ea27657d46ce3f.jpg",
    openBetsGenericUrl:"https://scmedia.itsfogo.com/$-$/5539b5e8d1cc4b6595ea27657d46ce3f.jpg",
    extensionUrl:"https://scmedia.itsfogo.com/$-$/5539b5e8d1cc4b6595ea27657d46ce3f.jpg",
    beGambleAwareLogoUrl:"https://scmedia.itsfogo.com/$-$/9ec4377d22a7465e952b051023d79fa2.jpg",
    genericSharingLink:"https://sports.ladbrokes.com/",
    lostBetsShareCardMessage:"Check my ${BetType} Bet ",lostBetControl:[{"name":"Total Returns","isSelected":true},{"name":"Stake","isSelected":true},{"name":"Odds","isSelected":true},{"name":"Selection Name","isSelected":true},{"name":"Event Name","isSelected":true},
    {"name":"Bet Placed Date","isSelected":true}],
    openBetShareCardMessage:"open bets msg",openBetShareCardSecondMessage:"Check my ${BetType} Bet",
    openBetShareCardStatus:true,openBetControl:[{"name":"Total Returns","isSelected":true},
    {"name":"Stake","isSelected":true},{"name":"Odds","isSelected":true},
    {"name":"Selection Name","isSelected":true},{"name":"Event Name","isSelected":true},
    {"name":"Bet Placed Date","isSelected":true}],wonBetShareCardMessage:"I won ${TPR} on ${BetType}",
    wonBetShareCardStatus:true,wonBetControl:[{"name":"Total Returns","isSelected":true},
    {"name":"Stake","isSelected":true},{"name":"Odds","isSelected":false},{"name":"Selection Name","isSelected":true},{"name":"Event Name","isSelected":true},{"name":"Bet Placed Date","isSelected":true}],
    cashedOutBetsShareCardMessage:"Check my ${BetType} Bet ",cashedOutBetControl:[{"name":"Total Returns","isSelected":false},{"name":"Stake","isSelected":true},{"name":"Odds","isSelected":true},{"name":"Selection Name","isSelected":true},{"name":"Event Name","isSelected":true},{"name":"Bet Placed Date","isSelected":true}],
    luckyDipBetSharingConfigs: {
        enable: false,
        header: '',
        backgroundImageUrl: '',
        wonLabel: '',
        luckyDipLabel: '',
        luckyDipAffiliateLink: '',
        potentialReturnsLabel: '',
        openBetControl : [
            { name: 'Date', isSelected: true },
            { name: 'SelectionName', isSelected: true },
            { name: 'Odds', isSelected: true },
            { name: 'Returns', isSelected: true }
        ],
        lostBetControl : [
            { name: 'Date', isSelected: true },
            { name: 'SelectionName', isSelected: true },
            { name: 'Odds', isSelected: true },
            { name: 'Returns', isSelected: true }
        ],
        wonBetControl : [
            { name: 'Date', isSelected: true },
            { name: 'SelectionName', isSelected: true },
            { name: 'Odds', isSelected: true },
            { name: 'Returns', isSelected: true }
        ]
      },ftpBetSharingConfigs:FTPBETSHARING_CONFIG
};