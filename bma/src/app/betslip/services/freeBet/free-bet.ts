import { el } from '@betslip/services/json-element';
import { IFreeBet } from '@betslip/services/freeBet/free-bet.model';
import { ITokenPossibleBet, IFreebetOfferCategory } from '@app/bpp/services/bppProviders/bpp-providers.model';

export class FreeBet {
  private freeBetId: string;
  private freeBetName: string;
  private freeBetValue: number;
  private freeBetExpireAt: Date;
  private freeBetType: string;
  private freeBetOfferCategories: IFreebetOfferCategory;
  private freeBetTokenDisplayText: string;
  private freeBetPossibleBets: ITokenPossibleBet[];
  private possibleBet: string;

  constructor(params: IFreeBet) {
    this.id = params.id;
    this.name = params.name;
    this.value = params.value;
    this.expireAt = params.expireAt;
    this.freeBetType = params.type;
    this.freeBetPossibleBets = params.possibleBets;
    this.freeBetTokenDisplayText = params.freeBetTokenDisplayText;
    this.freeBetOfferCategories = params.freeBetOfferCategories;
    this.setPossibleBet();
  }

  get id(): string {
    return this.freeBetId;
  }

  set id(id: string) {
    this.freeBetId = id;
  }

  set name(freeBetName: string) {
    this.freeBetName = freeBetName;
  }

  get name(): string {
    return this.freeBetName;
  }

  set value(number: number) {
    this.freeBetValue = number;
  }

  get value(): number {
    return this.freeBetValue;
  }

  set expireAt(time: Date) {
    this.freeBetExpireAt = time;
  }

  get expireAt(): Date {
    return this.freeBetExpireAt;
  }

  get cleanName(): string {
    return this.freeBetName;
  }
set cleanName(value:string){}
  get type(): string {
    return this.freeBetType;
  }
 set type(value:string){}
  doc(): IFreeBet {
    return (
      el('freebet', { id: this.id })
    );
  }

  set freebetOfferCategories(value: any) {
    this.freeBetOfferCategories = value;
  }

  get freebetOfferCategories() {
    return this.freeBetOfferCategories;
  }

  set freebetTokenDisplayText(value: string) {
    this.freeBetTokenDisplayText = value;
  }

  get freebetTokenDisplayText(): string {
    return this.freeBetTokenDisplayText;
  }

  private setPossibleBet(): void {
    const bets = this.freeBetPossibleBets;
    this.possibleBet = (bets && bets[0] && bets[0].name) ? ` (${bets[0].name})` : '';
  }
}
