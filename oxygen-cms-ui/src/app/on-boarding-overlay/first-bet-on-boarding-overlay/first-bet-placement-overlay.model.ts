import { Base } from '@app/client/private/models/base.model';


export interface  button{
    title: string;
    description: string;
    leftButtonDesc: string;
    rightButtonDesc: string;
};
export interface homePage{
    title: string;
    description: string;
    button: string;
};


export interface Content {
    title: string;
    description: string;
};
export interface betSlipContent{
    boost:Content;
    defaultContent: Content;
}

export interface myBetsContent {
    cashOut:Content;
    defaultContent:Content;
    buttonDesc: string;
}

export interface buttonDescr {
    cashOut:Content;
    defaultContent:Content;
}


export interface betPlaced {
    winAlert:Content;
    defaultContent:Content;
    buttonDesc: string;
}

export interface IFirstBetPlacement extends Base {
    expiryDateEnabled: boolean;
    isEnable: boolean;
    moduleName: string;
    moduleDiscription: string;
    displayFrom: string,
    displayTo: string,
    imageUrl: string,
    heightMedium: number,
    widthMedium: number,
    fileName: string,
    button:button;
    homePage: homePage;
    pickYourBet: Content;
    addSelection: Content;
    betSlip: betSlipContent;
    placeYourBet: betSlipContent;
    myBets: myBetsContent;
    betDetails: buttonDescr;
    betPlaced: betPlaced;
    months: number;
}