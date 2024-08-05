export interface IbetslipsAcca  {
  brand?: string,
  id?:string,
  enabled? : boolean,
  accInsMsgEnabled :boolean,
  svgId : string,
  bsAddToQualifyMsg:string,
  bsQualifiedMsg: string,
  bsqInfoIcon : boolean,
  avlblInscCountIndi: string,
  obAccaCount : number,
  betslipSp :IbetslipSp,
  accabarSp: IaccabarSp,
  betreceiptSp:  IbetreceiptSp,
  mybetsSp:ImybetsSp,
  profitIndi: string,
  profitIndiUrl:string,
  popUpDetails: IpopUpDetails,
}

export interface IbetslipSp   {
  bsSp: string,
  enabled: boolean,
  progressBar: boolean,
  infoIcon: boolean,
}
export interface IaccabarSp  {
  absp: string,
  enabled: boolean,
  progressBar: boolean
}
export interface IbetreceiptSp  {
  brsp: string,
  enabled: boolean
}
export interface ImybetsSp  {
  mbsp: string,
  enabled: boolean
}
export interface IpopUpDetails {
  popUpTitle:string,
  popUpMessage: string,
  priCtaLabel: string,
  priCtaUrl: string,
  secCtaLabel: string,
  secCtaUrl: string,
};
export interface IbetSlipAccaTable  {
  href :string,
  enable : boolean,
  tabName : string
}

export  interface IoddsBoost {
  brand?: string,
  id?:string
  svgId: string,
  oddsBoostMsgEnabled: boolean,
  bsHeader: string,
  bsDesc: string,
  infoIcon: boolean,
  brsp: string,
  brspEnabled: boolean,
  brDispBoostedPrice: boolean,
  mbsp: string,
  mbspEnabled: boolean
  mbDispBoostedPrice: boolean,
  profitIndicator: string,
  popUpDetails: {
    popUpTitle: string,
    popUpMessage: string,
    priCtaLabel: string,
    priCtaUrl: string,
    secCtaLabel: string,
    secCtaUrl: string,
  },
};
