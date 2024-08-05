export interface IBetShare {
        popUpDesc: string,
        horseRacingUrl: string,
        footBallUrl: string,
        url5ASide: string,
        settledBetsGenericUrl: string,
        openBetsGenericUrl: string,
        extensionUrl: string,
        beGambleAwareLogoUrl: string,
        brandLogoUrl: string,
        genericSharingLink: string,
        lostBetsShareCardMessage: string,
        lostBetControl: UserSharePreferences[],
        openBetShareCardMessage: string,
        openBetShareCardSecondMessage: string,
        openBetShareCardStatus: boolean,
        openBetControl: UserSharePreferences[],
        wonBetShareCardMessage: string,
        wonBetShareCardStatus: boolean,
        wonBetControl: UserSharePreferences[],
        cashedOutBetsShareCardMessage : string,
          cashedOutBetControl: UserSharePreferences[],
    }

    export class UserSharePreferences{ 
      name: string;
      isSelected: boolean;  
    }