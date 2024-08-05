import { ILottoPrice, ILottoDraw } from './lotto.model';

export interface ILottoResult {
  betOdds?: ILottoPrice;
  betSelections?: string;
  betStake?: number;
  betStakePerLine?: string;
  betTypeDesc?: string;
  currency?: string;
  date?: Date;
  draws?: ILottoDraw[];
  name?: string;
  id?: string;
  resultedDraw?: ILottoDraw[];
}
