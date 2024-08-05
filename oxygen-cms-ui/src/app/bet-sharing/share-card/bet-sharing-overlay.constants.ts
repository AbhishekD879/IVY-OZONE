import { BetShare } from "@root/app/client/private/models/betShare.model";

export const UserPreferncesArray: { name: string, isSelected: boolean }[] =
    [
        { name: 'Total Returns', isSelected: true },
        { name: 'Stake', isSelected: true },
        { name: 'Odds', isSelected: true },
        { name: 'Selection Name', isSelected: true },
        { name: 'Event Name', isSelected: true },
        { name: 'Bet Placed Date', isSelected: true }
    ];
    export const FTPBETSHARING_CONFIG = {
        enable: true,
        header: '',
        subHeader: '',
        playLabel: '',
        backgroundImageUrl:'',
        affiliateLink:'',
        teamDetails: []
    } 

    export const LuckyDipUserPreferncesArray: { name: string, isSelected: boolean }[] = [
      { name: 'Date', isSelected: true },
      { name: 'SelectionName', isSelected: true },
      { name: 'Odds', isSelected: true },
      { name: 'Returns', isSelected: true }
  ];

    export const LUCKYDIP_BETSHARINGCONFIG = {
        enable: false,
        header: '',
        backgroundImageUrl: '',
        wonLabel: '',
        luckyDipLabel: '',
        potentialReturnsLabel: '',
        luckyDipAffiliateLink: '',
        openBetControl : LuckyDipUserPreferncesArray,
        lostBetControl : LuckyDipUserPreferncesArray,
        wonBetControl : LuckyDipUserPreferncesArray
    }
    

export const BET_SHARECARD_VALUES: BetShare = {
    id: '',
    updatedBy: '',
    updatedAt: '',
    createdBy: '',
    createdAt: '',
    updatedByUserName: '',
    createdByUserName: '',
    brand: '',
    genericSharingLink: '',
    popUpDesc: '',
    openBetShareCardStatus: true,
    openBetShareCardMessage: '',
    openBetShareCardSecondMessage: '',
    shareCardImageFileName: '',
    wonBetShareCardStatus: true,
    wonBetShareCardMessage: '',
    lostBetsShareCardMessage: '',
    cashedOutBetsShareCardMessage: '',
    horseRacingUrl: '',
    footBallUrl: '',
    url5ASide: '',
    settledBetsGenericUrl: '',
    openBetsGenericUrl: '',
    extensionUrl: '',
    beGambleAwareLogoUrl: '',
    brandLogoUrl: '',
    openBetControl: UserPreferncesArray,
    wonBetControl: UserPreferncesArray,
    lostBetControl: UserPreferncesArray,
    cashedOutBetControl: UserPreferncesArray,
    luckyDipBetSharingConfigs :LUCKYDIP_BETSHARINGCONFIG,
    ftpBetSharingConfigs: FTPBETSHARING_CONFIG,
}

export const FTP_BETSHARING_TEAMS_TABLE = [
        {
          name: 'Name',
          property: 'teamName',
          type: 'text'
        },
        {
          name: 'URL',
          property: 'teamLogoUrl',
          link: {
            hrefProperty: 'id'
          },
          type: 'link'
        }
      ];
