import { Component, Input, OnInit, OnDestroy } from '@angular/core';
import { IBetTermsChange, IClaimedOffer } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { IBetPromotion } from '@app/betHistory/models/bet-promotion.model';
import { CmsService } from '@core/services/cms/cms.service';
import { BET_PROMO_CONFIG as bet_promos } from '@betHistoryModule/constants/bet-promotions.constant';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { CashoutBet } from '@app/betHistory/betModels/cashoutBet/cashout-bet.class';
import { RegularBet } from '@app/betHistory/betModels/regularBet/regular-bet.class';
import { PlacedBet } from '@app/betHistory/betModels/placedBet/placed-bet.class';
import { LocaleService } from '@core/services/locale/locale.service';
import { BetInfoDialogService } from '@betslip/services/betInfoDialog/bet-info-dialog.service';
import { LUCKY_TYPES } from '@betslip/constants/bet-slip.constant';
import { GtmService } from '@core/services/gtm/gtm.service';
import { bma } from '@app/lazy-modules/locale/translations/en-US/bma.lang';
import environment from '@environment/oxygenEnvConfig';

@Component({
  selector: 'bet-promotions',
  templateUrl: './bet-promotions.component.html',
  styleUrls: ['./bet-promotions.component.scss']
})
export class BetPromotionComponent implements OnInit, OnDestroy {
  @Input() betEventSource: CashoutBet | RegularBet | PlacedBet | any;

  promoIcons: IBetPromotion[];
  ctrlName: string;
  luckyBet: any;
  luckyTypes = ['L15', 'L31', 'L63'];
  luckyBetStatus: any;
  allWinnerStatus: any;
  fullBetType: string;
  isBrandLadbrokes: boolean;
  luckyCheck: boolean;
  isShownInfo: boolean;
  constructor(
    private cmsService: CmsService,
    private pubSubService: PubSubService,
    private locale: LocaleService,
    protected betInfoDialogService: BetInfoDialogService,
    protected gtmService: GtmService) { }

  ngOnInit(): void {
    this.isBrandLadbrokes = environment.brand === this.locale.getString(bma.brands.ladbrokes).toLowerCase();
    this.fullBetType = this.getBetType();
    this.ctrlName = 'BetPromotionComponent';
    this.updatePromos();

    this.pubSubService.subscribe(`${this.ctrlName}_${this.betEventSource.betId}`, this.pubSubService.API.BET_EVENTENTITY_UPDATED,
    () => this.updatePromos());

    this.checkLuckyBonus();
  }

  ngOnDestroy(): void {
    this.pubSubService.unsubscribe(`${this.ctrlName}_${this.betEventSource.betId}`);
  }
  /**
   * Check lucky bonus available for lucky types(15/31/63)
   *  @param betEventSource
   */
  private checkLuckyBonus(){
    if(this.luckyTypes.includes(this.betEventSource.betType) && this.betEventSource && this.betEventSource.availableBonuses && this.isBonusApplicable(this.betEventSource.availableBonuses.availableBonus)){
      this.betEventSource.availableBonuses.availableBonus.map(element => {
        if((this.betEventSource.betType == LUCKY_TYPES.L15.TYPE && element.num_win == LUCKY_TYPES.L15.ALL_WIN) ||
          (this.betEventSource.betType == LUCKY_TYPES.L31.TYPE && element.num_win == LUCKY_TYPES.L31.ALL_WIN) ||
          (this.betEventSource.betType == LUCKY_TYPES.L63.TYPE && element.num_win == LUCKY_TYPES.L63.ALL_WIN)){
            element['isShown'] = false;
          }else{
            element['isShown'] = true;
          }
      });
      this.luckyBet = this.filterOnlyAvailable(this.betEventSource.availableBonuses.availableBonus).sort((a,b)=>{return b.num_win-a.num_win});
    }else if(this.luckyTypes.includes(this.betEventSource.betType) && this.betEventSource && this.betEventSource.altSettle  && this.isBonusApplicable(this.betEventSource.altSettle.rule)){
      this.luckyBet = (this.betEventSource.altSettle.rule) ? this.filterOnlyAvailable(this.betEventSource.altSettle.rule).sort((a,b)=>{return b.num_win-a.num_win}): [];
    }
    
    this.luckyCheck = this.luckyTypes.includes(this.betEventSource.betType);
    const luckytext = this.cmsService.systemConfiguration['LuckyBonus'];
    this.isShownInfo = luckytext && luckytext['SettledBetPopUpHeader'] && luckytext['SettledBetPopUpHeader'].trim().length > 0 && luckytext['SettledBetPopUpMessage'] && luckytext['SettledBetPopUpMessage'].trim().length > 0;
  }
  isBonusApplicable(bonuses): boolean{
    return !bonuses.every(item => Number(item.multiplier) == 1);
  }
  filterOnlyAvailable(bonus){
    return bonus.filter(item => Number(item.multiplier) !== 1);
  }
  /**
   * Check for lucky types(15/31/63)
   *  @param betEventSource
   */
  private getBetType(){
    const bet = this.betEventSource;
    return bet.bybType
      ? bet.bybType
      : this.locale.getString(`bethistory.betTypes.${bet.betType}`);
  }

  private updatePromos(): void {
    this.promoIcons = [];
    let betBoosted: IBetPromotion;
    let twoUpMarket: IBetPromotion;

    // Boosted icon
    if (this.betEventSource.betTermsChange && this.isBetBoosted()) {
      betBoosted = { ...bet_promos.find((item: IBetPromotion) => item.name === 'boosted')};
      this.promoIcons.push(betBoosted);
    }

    if(this.betEventSource.betType === 'SGL' && this.is2UpMarket()) {
      twoUpMarket = {...bet_promos.find((item: IBetPromotion) => item.name == 'two-up-market')};
      this.promoIcons.push(twoUpMarket);
    }

    // Money Back icon
    this.cmsService.getToggleStatus('PromoSignposting')
      .subscribe((toggleStatus: boolean) => {
        if (toggleStatus && this.betEventSource.betType === 'SGL' && this.isMoneyBack()) {
          this.promoIcons.push(bet_promos.find((item: IBetPromotion) => item.name === 'money-back'));
        }

        if (this.promoIcons.length <= 1 && this.isAccaInsurance()) {
          this.promoIcons.push(bet_promos.find((item: IBetPromotion) => item.name === 'acca-insurance'));
        }

        // Shortened boosted label text, show two only icons
        if (this.promoIcons.length >= 2 && (betBoosted || twoUpMarket)) {
          if(betBoosted) {
            betBoosted.label = 'bs.boostedMsg2';
          } 
          if(twoUpMarket){
            twoUpMarket.label = 'bs.twoUpMsg';
          }
          this.promoIcons = this.promoIcons.slice(0, 2);
        }
      });
  }

  private isBetBoosted(): boolean {
    const terms = this.betEventSource.betTermsChange;
    return terms && terms.some((term: IBetTermsChange) => term.reasonCode === 'ODDS_BOOST');
  }

  private isMoneyBack(): boolean {
    const leg = this.betEventSource.leg;
    const marketLevel = leg[0] && leg[0].eventEntity && leg[0].eventEntity.markets && leg[0].eventEntity.markets[0]
    && leg[0].eventEntity.markets[0].drilldownTagNames && leg[0].eventEntity.markets[0].drilldownTagNames.search('MKTFLAG_MB') !== -1;
    return  marketLevel;
  }

  private is2UpMarket() {
    const twoUpMarketName: string = this.locale.getString('bma.twoUpMarketName');
    const leg = this.betEventSource.leg;
    if(leg[0] && leg[0].eventEntity && leg[0].eventEntity.categoryId === '16') {
      return leg[0].part && leg[0].part.length && leg[0].part[0].eventMarketDesc == twoUpMarketName;
    }
    return false;
  }
  /**
   * check if bet is ACC5 or more type
   * betEventSource.betType expl: SGL, TBL, ACC4, ACC5,...
   * @returns {boolean}
   */
  private isAccaInsurance(): boolean {
    const accaNumber = this.betEventSource.betType && this.betEventSource.betType.replace( /^\D+/g, '');
    return +accaNumber >= 5 && this.betEventSource.claimedOffers && this.betEventSource.claimedOffers.claimedOffer &&
      this.betEventSource.claimedOffers.claimedOffer
      .some((claimedOffer: IClaimedOffer) => claimedOffer.offerCategory === 'Acca Insurance' && claimedOffer.status === 'qualified');
  }

  openSelectionMultiplesDialog(betType, label): void {
    const luckytype=this.betEventSource.altSettle.rule;
    this.sendGtmDataonMoreinFoicon(label);
    this.betInfoDialogService.multiple(betType, 1, luckytype, true, 'settled bets', label);
  }
  /**
   * Add GA tracking for lucky bonus available for lucky types(15/31/63)
   *  @param label
   */
  sendGtmDataonMoreinFoicon(label){
    const gtmData={
      event: 'Event.Tracking',
     'component.CategoryEvent': 'betslip',
     'component.LabelEvent': 'lucky bonus',
     'component.ActionEvent': 'click',
     'component.PositionEvent': label,
     'component.LocationEvent': 'settled bets',
     'component.EventDetails': ' more info link',
     'component.URLClicked':  'not applicable',
    }
    this.gtmService.push(gtmData.event, gtmData);
  }

  /**
   * Get the bet selections updates and change the labels for lucky bonuses
   *  @param betEventSource
   */
  betTypeStatus(){
    const luckyBet = this.betEventSource;
    const event = luckyBet.leg[0].eventEntity || luckyBet.leg[0].backupEventEntity;
    let status = '';
    if (event) {
      const sport = event.categoryId;
      if(this.luckyTypes.includes(luckyBet.betType) && luckyBet.leg.length >= 4 && (sport === '21' || sport === '19') && luckyBet.availableBonuses){
        this.luckyBetStatus = luckyBet.leg.filter(item => {return item.status === 'won'});
        this.allWinnerStatus = luckyBet.leg.filter(item => {return item.status === 'lost'});
        const luckyBetLen = (this.luckyBetStatus.length).toString();
        // Get if bet lose/suspended
        if(this.allWinnerStatus.length && this.onlyAllWinnerBonusApplicable(luckyBet)){
          this.pubSubService.publish('LUCKY_BONUS', luckyBet.receipt);
        }
        if(luckyBet.settled === 'N' && (luckyBet.betType == LUCKY_TYPES.L15.TYPE && luckyBetLen === LUCKY_TYPES.L15.ALL_WIN) ||
        (luckyBet.betType == LUCKY_TYPES.L31.TYPE && luckyBetLen == LUCKY_TYPES.L31.ALL_WIN) ||
        (luckyBet.betType == LUCKY_TYPES.L63.TYPE && luckyBetLen == LUCKY_TYPES.L63.ALL_WIN)){
          status = 'AllWinner';
        }
        return (status === 'AllWinner' ? status : luckyBetLen);
      }
    }
    if(luckyBet.altSettle){
      return this.winnerType(luckyBet);
    }
  }

  private winnerType(bet): string{
    if(bet.settled === 'Y' && this.getWinner(bet)){
      return 'AllWinner';
    }else{
      return bet.altSettle.rule[0].num_win;
    }
  }

  /**
   * Check lucky bonus available for settled bets page
   *  return boolean
   */
  private getWinner(lucky): boolean{
    if(lucky.settled === 'Y' && lucky.altSettle){
      return (lucky.betType == LUCKY_TYPES.L15.TYPE && lucky.altSettle.rule[0].num_win == LUCKY_TYPES.L15.ALL_WIN) ||
      (lucky.betType == LUCKY_TYPES.L31.TYPE && lucky.altSettle.rule[0].num_win == LUCKY_TYPES.L31.ALL_WIN) ||
      (lucky.betType == LUCKY_TYPES.L63.TYPE && lucky.altSettle.rule[0].num_win == LUCKY_TYPES.L63.ALL_WIN)
    }
  }

  onlyAllWinnerBonusApplicable(luckydata): boolean{
    const type = (luckydata.betType || luckydata.betTypeRef.id);
    return luckydata.availableBonuses.availableBonus.filter(list=>{
      if(type == LUCKY_TYPES.L15.TYPE){
        return (list.num_win === LUCKY_TYPES.L15.ALL_WIN && Number(list.multiplier) !== 1);
      }else if(type == LUCKY_TYPES.L31.TYPE){
        return (list.num_win === LUCKY_TYPES.L31.ALL_WIN && Number(list.multiplier) !== 1);
      }else{
        return (list.num_win === LUCKY_TYPES.L63.ALL_WIN && Number(list.multiplier) !== 1);
      }
    }).length !== 0;
  }

  addWinnerLabel(winnerCount, isAllWinner){
    if(isAllWinner){
      return Number(winnerCount) > 1 ? (winnerCount+' WINNERS') : (winnerCount+' WINNER');
    }
  }
}
