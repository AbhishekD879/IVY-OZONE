import { YourCallBet } from '@yourcall/models/bet/your-call-bet';
import { CHANNEL } from '@shared/constants/channel.constant';

export class BYBBet extends YourCallBet {
  constructor(data) {
    super(data);
  }

  /**
   * Builds object for request
   * @param data
   * @return {object}
   */
  normalize(data: BYBBet): any {
    const result: any = {};

    if (data.freebet) {
      result.freebet = {
        id: data.freebet.freebetTokenId,
        stake: data.freebet.freebetTokenValue
      };
    }

    result.stake = data.stake;
    result.currency = data.currencyName;
    result.token = data.token;
    result.price = data.betOddsFract;
    result.channel = data.channel || CHANNEL.byb;

    return result;
  }

  /**
   * Used in quickbet-panel for preparing bet to request
   * @return {object}
   */
  formatBet() {
    return this.normalize(this);
  }

  /**
   * Calculate Estimated Returns for single selection of BYB
   * @return {string}
   */
  getPotentialPayout(): string {
    const stake = Number(this.stake);
    if (stake || (stake === 0 && !this.freebetValue)) {
      return (Number(super.getPotentialPayout()) - Number(this.freebetValue || 0)).toFixed(2);
    }
    const betOdds = Number.parseFloat(this.betOdds);
    return (betOdds * (this.freebetValue || 1) - (this.freebetValue || 0)).toFixed(2);
  }
}
