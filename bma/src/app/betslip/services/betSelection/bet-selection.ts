import * as _ from 'underscore';
import { IBetError } from '@betslip/services/betError/bet-error.model';
import { IOutcomePrice } from '@core/models/outcome-price.model';
import { AccaBets, IBetSelection } from '@betslip/services/betSelection/bet-selection.model';
import { IOutcome, IOutcomeDetails } from '@core/models/outcome.model';
import { IGtmEvent } from '@core/models/gtm.event.model';

export class BetSelection {

  type: string;
  typeName: string;
  outcomes: IOutcome[];
  handicap: string;
  winPlace: string;
  eventIsLive: boolean;
  goToBetslip: boolean;
  GTMObject: IGtmEvent;
  isFCTC: boolean;
  details: IOutcomeDetails | any;
  linePicks: string;
  isLotto: boolean;
  eventName: string;

  private params: IBetSelection | any;
  private selectionPrice: IOutcomePrice;
  private _userStake: string;
  private _userEachWay: boolean;
  private _userFreeBet: string;
  private _errs: IBetError[];
  accaBets: AccaBets[];

  static parseSelectionPrice(params: IBetSelection): IOutcomePrice {
    const outcomePrice = _.first(params.outcomes) && _.first(params.outcomes[0].prices);
    const paramsPrice = params.price || <IOutcomePrice>{};
    const priceType = paramsPrice.priceType;
    const price = params.type === 'SCORECAST' ? paramsPrice : outcomePrice || paramsPrice;

    if (priceType) {
      // Store price type ('LP' or 'SP') of added selection ('Unnamed favourite' or racing with 'LP'/'SP')
      price.priceType = priceType;
    }

    return price;
  }

  constructor(params: IBetSelection | any) {
    const updateParams = _.omit(params, ['type', 'typeName', 'handicap', 'outcomes',
    'winPlace', 'userStake', 'userFreeBet', 'userEachWay', 'errs', 'price', 'GTMObject', 'isLotto', 'eventName']);

    this.params = params;
    this.type = params.type || 'SGL';
    this.typeName = params.typeName;
    this.handicap = <string>params.handicap;
    this.outcomes = params.outcomes;
    this.winPlace = params.winPlace;
    this.GTMObject = params.GTMObject;
    this.userStake = params.userStake || params.details?.stake;
    this.userFreeBet = params.userFreeBet || '';
    this.userEachWay = params.userEachWay || false;
    this.errs = params.errs || [];
    this.selectionPrice = BetSelection.parseSelectionPrice(params);
    this.details = params.details || params.data;
    this.linePicks = this.details?.selections || '';
    this.goToBetslip = this.goToBetslip || this.details?.goToBetslip;
    this.isLotto = params.isLotto;
    this.accaBets = params.accaBets;
    this.eventName = params.eventName;

    _.extend(this, updateParams);
  }

  get id(): string {
    return this.params.isLotto ? 
    _.union([this.type], [this.linePicks], _.pluck(this.details.draws, 'id')).join('|') : 
    _.union([this.type], _.pluck(this.outcomes, 'id')).join('|');
  }

  set id(id: string) {
    if (!id) {
      this.id = this.params.isLotto ? 
      _.union([this.type], [this.linePicks], _.pluck(this.details.draws, 'id')).join('|') : 
      _.union([this.type], _.pluck(this.outcomes, 'id')).join('|');
    }
  }

  get price(): IOutcomePrice {
    return this.selectionPrice || (this.outcomes && this.outcomes[0].prices && this.outcomes[0].prices[0]);
  }

  set price(priceParams: IOutcomePrice) {
    _.extend(this.selectionPrice, priceParams);
  }

  get userStake(): string {
    return this._userStake || '';
  }

  set userStake(amount: string) {
    this._userStake = amount;
  }

  get isRacing(): boolean {
    return this.outcomes && this.outcomes[0].details && this.outcomes[0].details.isRacing;
  }
  set isRacing(value:boolean){}
  get userEachWay(): boolean {
    return this._userEachWay;
  }

  set userEachWay(flag: boolean) {
    this._userEachWay = flag;
  }

  get userFreeBet(): string {
    return this._userFreeBet;
  }

  set userFreeBet(freeBetTokenId: string) {
    this._userFreeBet = freeBetTokenId;
  }

  get hasEachWay(): boolean {
    return _.every(this.outcomes, outcome => {
      return outcome.details && outcome.details.isEachWayAvailable;
    }, this);
  }
  set hasEachWay(value:boolean){}
  get hasBPG(): boolean {
    return _.every(this.outcomes, outcome => {
      return outcome.details && outcome.details.isGpAvailable;
    }, this);
  }
  set hasBPG(value:boolean){}
  get eachWayOn(): BetSelection {
    return this.hasEachWay
      ? new BetSelection(_.extend({}, this.params, { winPlace: 'EACH_WAY' }))
      : undefined;
  }
  set eachWayOn(value:BetSelection){}
  get errs(): IBetError[] {
    return this._errs;
  }

  set errs(errors: IBetError[]) {
    this._errs = errors;
  }

  zip(): IBetSelection {
    return <IBetSelection | any>{
      outcomesIds: _.pluck(this.outcomes, 'id'),
      userStake: this.userStake,
      userEachWay: this.userEachWay,
      userFreeBet: this.userFreeBet,
      goToBetslip: this.goToBetslip,
      handicap: this.handicap,
      id: this.id,
      price: this.price,
      type: this.type,
      typeName: this.typeName,
      isRacing: this.isRacing,
      isFCTC: this.isFCTC,
      hasBPG: this.hasBPG,
      hasEachWay: this.hasEachWay,
      eventIsLive: this.eventIsLive,
      isSuspended: this.params.outcomes && !!this.params.outcomes[0].errorMsg,
      isVirtual: this.params.isVirtual,
      eventId: this.params.eventId,
      isOutright: this.params.isOutright,
      isSpecial: this.params.isSpecial,
      isLotto: this.isLotto,
      GTMObject: this.GTMObject ? {
        tracking: this.GTMObject && this.GTMObject.tracking ? this.GTMObject.tracking : null
      } : null,
      details: this.details,
      accaBets: this.accaBets,
      eventName: this.eventName
    };
  }

  isMatch(selection: { id: string; }): boolean {
    return this.id === selection.id;
  }
}
