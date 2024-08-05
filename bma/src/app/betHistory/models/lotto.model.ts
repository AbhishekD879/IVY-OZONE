export interface ILottoModel {
  id: string;
  name: string;
  balls: IBall[];
  drawName: string;
  betDate: string | number | Date;
  betReceiptId: string;
  stake: string| number | IStakeBet;
  estReturns? : string | number;
  returns? : string | number;
  currency: string;
  status: string;
  settled: string;
  settledAt : string
  drawDate: string;
  totalReturns: string | number;
  lotteryResults?: ILotteryResult;
  isShowMore?: boolean;
  showMoreRequired?: boolean;
  outstandingSubs? : boolean;
}

export interface ILottoBet extends ILottoModel {
  betType: IBetType;
  id: string;
  lotteryDraw: ILotteryDraw;
  lotteryName: string;
  lotterySub: ILotterySub;
  numLines: string;
  numSelns: string;
  refund: IValue;
  settled: string;
  settledAt: string;
  source: string;
  subId: string;
  winnings: IValue;
}

export interface IBall {
  ballName: string;
  ballNo: string;
}

interface IBetType {
  code: string;
  name: string;
}


interface ILotteryDraw {
  drawAt: string;
  pick: IBall[];
  xgameId: string;
}

interface ILotterySub {
  date: string | number | Date;
  numSubs: string;
  outstandingSubs: string;
  stakePerBet: string;
  subId: string;
  subReceipt: string;
}

export interface IStakeBet {
  currency: string;
  stakePerLine: string;
  tokenValue: string;
  value: string;
}

interface IValue {
  value: string;
}

export interface ILotteryResult {
  drawAt?: string,
  lotteryDrawResult?: IBall[],
  status?: string;
  returned?: string;
  lotteryResults? :[] | any;
  lotteryDraws? : []
  winnings?: {
    value: string;
  }
xgameId:string;
settledAt : string;
}
