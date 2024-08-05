import { IGtmEvent } from "@core/models/gtm.event.model";
import { ILottoNumber } from "./lotto-numbers.model";
import { ILeg } from "@app/betslip/services/models/bet.model";

export interface ILotteryMap {
  [key: string]: ILotto;
}

export interface ILotteryResultsMap {
  [key: string]: ILottoResultDraw;
}

export interface ILottoDraw {
  description: string;
  drawAtTime: string;
  drawDescriptionId: string;
  id: string;
  isActive: boolean;
  lotteryId: string;
  openAtTime: string;
  shutAtTime: string;
  sort: string;
  checked: boolean;
}

export interface ILottoPrice {
  id: string;
  lotteryId: string;
  numberCorrect: string;
  numberPicks: string;
  priceDen: number;
  priceNum: number;
}

export interface ILotto {
  country: string;
  description: string;
  draw: ILottoDraw[];
  hasOpenDraw: boolean;
  id: string;
  limits: number;
  lotteryPrice: ILottoPrice[];
  maxLines: string;
  maxNumber: string;
  maxPicks: number;
  minNumber: string;
  minPicks: string;
  name?: string;
  siteChannels: string;
  sort: string;
  resultedDraw?: ILottoResultDraw[];
  normal: ILottoType;
  boosterBall: ILottoType;
  uri: string;
  shutAtTime: string;
  sortCode?: string;
  maxPayOut?: number;
}

export interface ILottoType {
  name?: string;
  id? : string;
  sort: string;
  draw: ILottoDraw[];
  [key: string]: any; 
}

export interface ILottonMenuItem {
  imageTitle: string;
  uri: string;
  svg: string;
  svgId: string;
  inApp: boolean;
  targetUri: string;
  targetUriCopy: string;
  maxPayOut?: number;
}

export interface ILottoResultDraw extends ILotto {
  sortDate: string;
  resultedDraw: any;
  ballColor: string;
  results: string;

  page?: number;
}

export interface ILottoPlaceBetObj {
  name: string;
  selectionName: string;
  selections: string;
  draws: ILottoDraw[];
  multiplier: number;
  amount: number;
  odds: ILottoPrice;
  currency: string;
  maxPayOut?:number;
}

export interface ILottoTab {
  title: string;
  name: string;
  hidden: boolean;
  id: number;
  url: string;
}

export interface ILottoLineSummary{
  numbersData: ILottoNumber[];
  isBonusBall: boolean;
  isFavourite: boolean;
}

export interface LinesSummaryObj{
  linesNumbersData: ILottoNumber[];
}

export interface ILottoCms{
  dayCount?: number;
  globalBannerLink: string;
  globalBannerText: string;
  lottoConfig: Array<ILottoCmsPage>;
}

export interface ILottoCmsPage {
  bannerLink: string;
  bannerText: string;
  brand: string;
  id: string;
  infoMessage: string;
  label: string;
  nextLink: string;
  sortOrder: number;
  ssMappingId: string;
  enabled: boolean;
  maxPayOut?: number;
}
 export interface PreviousResults{
 result: string;
}



export interface ILottoBetDoc{
  GTMObject?: IGtmEvent;
  accaBets: ILottoAccaBets[];
  details: ILottoDetails;
  linePicks: string;
  legRef?: ILeg[];
  [key: string]: any; 
  lines: {number: number};
  isLotto?: boolean;
}

interface ILottoDetails {
currency: string;
draws: ILottoDraw[];
frequency: string;
multiplier: string;
name: string;
odds: ILottoOdds[],
isLotto?: boolean;

}
interface ILottoAccaBets {
betType: string;
betLineSummary: ILineSummary[];
betTypeRef: {id: string};
id: string;
lines: {number: number};
winingAmount: string | number;
}

interface ILottoOdds {
id: string;
lotteryId: string;
numberCorrect: string;
numberPicks: string;
priceDen: string;
priceNum: string;
}
interface ILineSummary {
betTypeRef: {id: string};
lines: {number: number};
numPicks: number
}
