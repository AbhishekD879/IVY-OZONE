import { Bet } from './bet';
import { ILiveUpdateResponseMessage } from '@betslip/services/betslipLiveUpdate/betslip-live-update.model';
import { IPayload } from '@core/models/live-serve-update.model';

export class BetLiveUpdateHistory {
  private history: {
    time: number;
    payload: ILiveUpdateResponseMessage;
  }[] = [];

  private bet: Bet;
  private prevState: {[key: string]: any} = {};

  private readonly subChannels = {
    market: 'sEVMKT',
    price: 'sPRICE'
  };

  constructor(bet: Bet) {
    this.bet = bet;
  }

  /**
   * Update live update history for betslip selection
   * (last updates at the begin of history)
   * @param {object} payload
   */
  update(payload: ILiveUpdateResponseMessage): void {
    const info = this.bet.info();

    this.prevState = {
      error: info.error,
      isSuspended: info.isSuspended,
      price: info.price
    };

    this.history.unshift({
      time: Date.now(), payload
    });
  }

  /**
   * Check if event started
   * @returns {boolean}
   */
  isStarted(): boolean {
    const info = this.bet.info();
    return (
      info.error === 'EVENT_STARTED' && info.error !== this.prevState.error
    );
  }

  /**
   * Check if bet suspended
   * @returns {boolean}
   */
  isSuspended(): boolean {
    const info = this.bet.info();
    return (
      info.isSuspended && info.isSuspended !== this.prevState.isSuspended
    );
  }

  /**
   * Check if price changed
   */
  isPriceChanged(): boolean {
    const info = this.bet.info();
    const price = info.price;
    const prevPrice = this.prevState.price;
    return (
      price.priceType === 'LP' &&
      (+price.priceNum !== +prevPrice.priceNum || +price.priceDen !== +prevPrice.priceDen)
    );
  }

  /**
   * Check if price changed and market unsuspended together.
   * Price and market changed together if time difference between these updates less than 100ms.
   * @returns {boolean}
   */
  isPriceChangedAndMarketUnsuspended(): boolean {
    const [lastUpdate] = this.history;
    const marketUpdate = lastUpdate.payload.subChannel.type === this.subChannels.market && lastUpdate;
    const priceUpdate = this.history.find(item => item.payload.subChannel.type === this.subChannels.price);
    return (
      marketUpdate && priceUpdate &&
      marketUpdate.time - priceUpdate.time < 100 &&
      (marketUpdate.payload.message as IPayload).status === 'A'
    );
  }
}
