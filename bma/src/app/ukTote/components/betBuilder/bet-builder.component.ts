import * as _ from 'underscore';
import { Component, ElementRef, Input, OnDestroy, OnInit } from '@angular/core';

import { LocaleService } from '@core/services/locale/locale.service';
import { DeviceService } from '@core/services/device/device.service';
import { CommandService } from '@core/services/communication/command/command.service';
import { UkToteBetBuilderService } from '../../services/ukTotebetBuilder/uk-tote-bet-builder.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { StakeValidatorService } from '../../services/stakeValidator/stake-validator.service';
import { UK_TOTE_CONFIG } from '../../constants/uk-tote-config.contant';
import { GtmService } from '@core/services/gtm/gtm.service';
import { TimeService } from '@core/services/time/time.service';
import { UkToteService } from '@uktote/services/ukTote/uk-tote.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { UkToteLiveUpdatesService } from '@core/services/ukTote/uktote-live-update.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { StraightExactaBet } from '../../models/straightEcxactaBet/straight-exacta-bet';
import { StraightTrifectaBet } from '../../models/straightTrifectaBet/straight-trifecta-bet';
import { CombinationBet } from '../../models/combinationBet/combination-bet';
import { IRacingEvent } from '@core/models/racing-event.model';
import { IUkTotePoolBet } from '@uktote/models/tote-pool.model';
import { IOutcome } from '@core/models/outcome.model';
import { IStakeRestrictions, IToteBetDetails } from '@betslip/services/toteBetslip/tote-betslip.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { IPoolBet } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';
import { CurrencyCalculator } from '@core/services/currencyCalculatorService/currency-calculator.class';
import { UserService } from '@core/services/user/user.service';
import { CurrencyCalculatorService } from '@core/services/currencyCalculatorService/currency-calculator.service';
import { RendererService } from '@shared/services/renderer/renderer.service';
import { TotePotBet } from '@uktote/models/totePotBet/tote-pot-bet';
import { Subscription } from 'rxjs';
import { CmsService } from '@app/core/services/cms/cms.service';

@Component({
  selector: 'bet-builder',
  templateUrl: 'bet-builder.component.html'
})
export class BetBuilderComponent implements OnInit, OnDestroy {
  @Input() eventEntity: IRacingEvent;
  @Input() channelIds: string[];
  @Input() currentPool: IUkTotePoolBet;
  @Input() msg: { warning: string };
  sticky: boolean = false;
  quickStakeVisible: boolean = true;
  @Input() betslipType: string;
  private readonly globalStake = 'global_stakes';

  totalStakeInUserCurrency: string;
  stakeChanged: boolean;
  errorField: string;
  isBetReadyForBetslip: boolean;
  previousStakePerLine: string;
  messageClosed: boolean;
  expanded: boolean;
  stakePerLine: string | any;
  betName: string;
  previousBetName: string;
  stakeRestrictions: IStakeRestrictions;
  visible: boolean;
  relocateAfterJob: number;
  scrollListener: Function;
  resiseListener: Function;
  currencyCalculator: CurrencyCalculator;
  userCurrencyCode: string;
  poolCurrencyCode: string;
  userCurrencySymbol: string;
  isMultipleLegsBet: boolean;
  totalStakeWithCurrency: string;
  private isMultipleLegsBetSubscription: Subscription;

  private scrollHandler = this.relocate.bind(this);
  private resizeHandler = this.relocateAfter.bind(this);

  private BETBUILDER_MIN_HEIGHT: number = 50;
  private TABLET_BOTTOM_MENU_HEIGHT: number = 52;
  private readonly title = 'BetBuilderController';
  readonly stakePattern: string = '^(\\d{0,12}((\\.|,)\\d{0,2})?)?$';
  quickStakeItems;
  keyboardToggle: boolean;

  constructor(
    private commandService: CommandService,
    private deviceService: DeviceService,
    private ukToteBetBuilderService: UkToteBetBuilderService,
    private pubsubService: PubSubService,
    private stakeValidatorService: StakeValidatorService,
    private localeService: LocaleService,
    private filtersService: FiltersService,
    private gtmService: GtmService,
    private timeService: TimeService,
    private ukToteService: UkToteService,
    private windowRefService: WindowRefService,
    private elementRef: ElementRef,
    private ukToteLiveUpdatesService: UkToteLiveUpdatesService,
    private rendererService: RendererService,
    private domToolsService: DomToolsService,
    private userService: UserService,
    private currencyCalculatorService: CurrencyCalculatorService,
    private cms: CmsService
  ) {
    // Get currency exchange calculator instance
    this.currencyCalculatorService.getCurrencyCalculator()
      .subscribe(calculator => {
        this.currencyCalculator = calculator;
      });
    this.userCurrencyCode = userService.currency;
    this.userCurrencySymbol = this.userService.currencySymbol;
    this.totalStakeWithCurrency = this.getTotalStakeWithCurrency();
    this.addListeners();
  }

  /**
   *
   * @returns {TotePotBet} - member of TotePotBet class
   */
  get betModel(): TotePotBet {
    return this.ukToteBetBuilderService.betModel;
  }
  set betModel(value:TotePotBet){}

  get alertMsg(): string {
    return (this.msg && this.msg.warning) || this.getErrorTranslate();
  }
  set alertMsg(value:string){}

  get showAlert(): boolean {
    return !!(this.msg && this.msg.warning) || (this.betModel && this.errorField && !this.messageClosed);
  }
  set showAlert(value:boolean){}

  ngOnInit(): void {
    this.cms.getQuickStakes(this.betslipType).subscribe((predefinedStakes: string[]) => {
      this.quickStakeItems = predefinedStakes;
      this.formatTotepoolStakes(this.quickStakeItems);
    });

    this.pubsubService.subscribe(this.title, this.pubsubService.API.BETBUILDER_UPDATED, this.init.bind(this));
    this.pubsubService.subscribe(this.title, this.pubsubService.API.RELOAD_COMPONENTS, () => {
      this.setVisibility(false, true);
    });
    this.pubsubService.subscribe(this.title, this.pubsubService.API.RELOCATE_BET_BUILDER, () => {
      this.relocateAfter();
    });
    this.pubsubService.subscribe(this.title, this.pubsubService.API.CLEAR_BET_BUILDER, () => {
      this.ukToteBetBuilderService.clear();
      this.resetState();
      this.updateSwitchersState();
      this.setVisibility(false, true);
    });
    if (!this.deviceService.isMobileOrigin || this.deviceService.isTablet) {
      this.scrollListener = this.rendererService.renderer.listen(this.windowRefService.nativeWindow, 'scroll',
        () => this.scrollHandler());
      this.resiseListener = this.rendererService.renderer.listen(this.windowRefService.nativeWindow, 'resize',
        () => this.resizeHandler());
    }
    this.isMultipleLegsBetSubscription = this.ukToteBetBuilderService.isMultipleLegsBet$
      .subscribe((isMultiple: boolean) => this.isMultipleLegsBet = isMultiple);
    this.relocateAfter();
    this.init(true);
  }
  
  /**
   * @param  {string[]} quickStakeItems
   */
  formatTotepoolStakes(quickStakeItems: string[]) {
    this.quickStakeItems = quickStakeItems.map((stake: string) => {
      const dec = stake.split('.');
      if (dec.length > 1) {
        dec[1] = dec[1].substring(0, 2);
        stake = dec.join(".");
      }
      return stake;
    });
  }

  ngOnDestroy(): void {
    this.resetState();
    this.setFooterVisibility(true);
    this.scrollListener && this.scrollListener();
    this.resiseListener && this.resiseListener();
    this.pubsubService.unsubscribe(this.title);
    this.isMultipleLegsBetSubscription.unsubscribe();
  }

  /**
   * Reset bet builder state
   */
  resetState(): void {
    this.expanded = false;
    this.stakePerLine = undefined;
    this.messageClosed = false;
    this.errorField = undefined;
  }

  /**
   * Set visibility for betbuilder and footer menu
   */
  init(betTypeChanged: boolean): void {
    this.betName = this.ukToteBetBuilderService.betName;
    this.poolCurrencyCode = this.currentPool && this.currentPool.currencyCode;
    if (betTypeChanged) {
      this.resetState();
    }
    if (this.ukToteBetBuilderService.checkIfShouldShow()) {
      this.setVisibility(true);
      if (this.betName && this.betName !== this.previousBetName) {
        this.previousBetName = this.betName;
        this.gtmService.push('trackEvent', {
          eventCategory: this.getToteType(),
          eventAction: 'bet selection',
          eventLabel: this.betName
        });
      }
    } else {
      this.setVisibility(false, true);
    }
    this.setStake();
    this.isBetReadyForBetslip = this.checkIfBetReadyForBetSlip();
  }

  /**
   * Recalculate betbuilder position and dimensions
   */
  relocate(): void {
    if (this.deviceService.isMobileOrigin && !this.deviceService.isTablet) {
      return;
    }
    const container = this.elementRef.nativeElement,
      betbuilder = container.querySelector('section');

    if (!betbuilder) {
      return;
    }
    const windowHeight = this.windowRefService.nativeWindow.innerHeight || 0,
      windowYOffset = this.windowRefService.nativeWindow.pageYOffset || 0,
      betbuilderHeight = this.domToolsService.getHeight(betbuilder) || this.BETBUILDER_MIN_HEIGHT,
      betbuilderOffset = this.domToolsService.getOffset(container).top || 0,
      betbuilderBottom = (this.deviceService.isTablet && !this.deviceService.isDesktop) ? this.TABLET_BOTTOM_MENU_HEIGHT : 0;
    this.sticky = this.deviceService.isMobile || betbuilderOffset + betbuilderHeight + betbuilderBottom > windowHeight + windowYOffset;
    if (this.sticky) {
      this.domToolsService.css(betbuilder, {
        position: 'fixed',
        left: this.domToolsService.getOffset(container).left,
        bottom: betbuilderBottom,
        width: this.domToolsService.getWidth(container)
      });
    } else {
      this.domToolsService.css(betbuilder, {
        position: 'relative',
        left: 'auto',
        bottom: 'auto',
        width: '100%'
      });
    }
  }

  /**
   * Generate bet details object for one event bet type: Exacta, Trifecta etc
   * @returns Object
   */
  generateToteBetDetails(): IToteBetDetails {
    const isStrightExactaOrTrifecta = _.contains([2, 3], Object.keys(this.ukToteBetBuilderService.items).length);

    return {
      betName: this.ukToteBetBuilderService.betName,
      poolName: this.getPoolName(),
      eventTitle: this.ukToteService.getRaceTitle(this.eventEntity),
      correctedDay: this.timeService.getCorrectDay(this.eventEntity.startTime),
      orderedOutcomes: this.getOrderedOutcomes(),
      stakeRestrictions: this.stakeRestrictions,
      showOrderPosition: isStrightExactaOrTrifecta
    };
  }

  /**
   * Forms bet object and adds it to betslip
   */
  addToBetslip(): void {
    const bet = this.getBetObject();

    this.stakeRestrictions = {
      maxStakePerLine: this.currentPool.maxStakePerLine,
      maxTotalStake: this.currentPool.maxTotalStake,
      minStakePerLine: this.currentPool.minStakePerLine,
      minTotalStake: this.currentPool.minTotalStake,
      stakeIncrementFactor: this.currentPool.stakeIncrementFactor
    };
    const selectedOutcomes = this.isMultipleLegsBet ? this.betModel.selectedOutcomes : this.getOrderedOutcomes(),
      toteEvents = this.isMultipleLegsBet ? this.betModel.events : [ this.eventEntity ];

    const addToBetSlipObject = {
      isTote: true,
      toteBetDetails: this.isMultipleLegsBet ? this.betModel.generateToteBetDetails(this.stakeRestrictions) : this.generateToteBetDetails(),
      poolBet: bet,
      events: this.isMultipleLegsBet ? this.betModel.events : [ this.eventEntity ],
      outcomes: selectedOutcomes,
      channelIds: this.getChannelIds(toteEvents, selectedOutcomes),
      poolCurrencyCode: this.currentPool && this.currentPool.currencyCode
    };
    this.pubsubService.publish(this.pubsubService.API.ADD_TO_BETSLIP_BY_SELECTION, addToBetSlipObject);
  }

  /**
   * Order outcomes to show them in betslip
   * @returns {array} array of ordered outcomes
   */
  getOrderedOutcomes(): IOutcome[] {
    let orderedOutcomes = [];

    if (Object.keys(this.ukToteBetBuilderService.items).length === 2) {
      orderedOutcomes.push(this.ukToteBetBuilderService.items['1st'], this.ukToteBetBuilderService.items['2nd']);
    }
    if (Object.keys(this.ukToteBetBuilderService.items).length === 3) {
      orderedOutcomes.push(this.ukToteBetBuilderService.items['1st'],
        this.ukToteBetBuilderService.items['2nd'], this.ukToteBetBuilderService.items['3rd']);
    }
    if (this.ukToteBetBuilderService.items['any']) {
      orderedOutcomes = this.ukToteBetBuilderService.items['any'];
    }

    return orderedOutcomes;
  }

  getPoolName(): string {
    return UK_TOTE_CONFIG.poolTypesMap[this.ukToteBetBuilderService.poolType].name;
  }

  getBetObject(): IPoolBet {
    if (this.isMultipleLegsBet) {
      return this.betModel.getBetObject(Number(this.stakePerLine));
    }

    let betNameClass;

    switch (this.betName) {
      case this.localeService.getString('uktote.strightExactaBet'): {
        betNameClass = StraightExactaBet;
        break;
      }
      case this.localeService.getString('uktote.strightTrifectaBet'): {
        betNameClass = StraightTrifectaBet;
        break;
      }
      default: {
        betNameClass = CombinationBet;
      }
    }

    return new betNameClass(this.ukToteBetBuilderService.items, this.ukToteBetBuilderService.poolType,
      this.ukToteBetBuilderService.poolId).betObject;
  }

  /**
   * Clear selections in betbuilder
   */
  clearSelections(): void {
    this.ukToteBetBuilderService.clear();
    this.setVisibility(false, true);
    this.gtmService.push('trackEvent', {
      eventCategory: this.getToteType(),
      eventAction: 'dashboard',
      eventLabel: 'clear selection'
    });
  }

  /**
   * Toggle selections overview widget
   */
  toggleSummary(): void {
    this.expanded = !this.expanded;
    if(this.expanded){
      this.pubsubService.publish(this.pubsubService.API.DIGIT_KEYBOARD_HIDDEN, 'uk-tote-event');
    }
  }

  /**
   * Get stake error translate
   * @returns {string} - error locale
   */
  getErrorTranslate(): string {
    const value = +this.betModel.pool[this.errorField],
      formattedValue = this.filtersService.numberWithCurrency(value, '£');
    return this.localeService.getString(`uktote.${this.errorField}`, { value: formattedValue });
  }

  /**
   * Provide validation and calculations for entered stake
   */
  setStake(): void {
    this.stakePerLine = this.stakePerLine?.replace(",",".");
    if (!this.betModel) {
      return;
    }
    const validationOptions = {
      stake: Number(this.stakePerLine),
      totalStake: this.ukToteBetBuilderService.getTotalStake(Number(this.stakePerLine)),
      pool: this.betModel.pool
    };
    this.totalStakeInUserCurrency = this.getTotalStakeInUserCurrency(validationOptions.totalStake);
    this.totalStakeWithCurrency = this.getTotalStakeWithCurrency();
    this.stakeChanged = this.previousStakePerLine !== this.stakePerLine;
    this.errorField = this.validateStake(validationOptions);
    this.isBetReadyForBetslip = this.checkIfBetReadyForBetSlip();
    this.previousStakePerLine = this.stakePerLine;
    this.messageClosed = false;
  }

  /**
   * Close warning message
   */
  closeMessage(): void {
    this.messageClosed = true;
    this.msg = null;
  }

  /**
   * Checks if multiple selections are present in betbuilder
   */
  get isManySelections(): string {
    const anySelections = this.ukToteBetBuilderService.items['any'];
    return anySelections && anySelections.length > 1 ?
      this.localeService.getString('uktote.clearSelections') :
      this.localeService.getString('uktote.clearSelection');
  }
  set isManySelections(value:string){}

  get stakeInputClasses() {
    return {
      dark: !!this.stakePerLine
    };
  }
  set stakeInputClasses(value:any){}

  getTotalStakeInUserCurrency(totalStakeInPoolCurrency: number): string {
    let totalStakeInUserCurrency;
    if (this.poolCurrencyCode && this.userCurrencyCode
      &&  this.poolCurrencyCode === this.userCurrencyCode) {
      totalStakeInUserCurrency = totalStakeInPoolCurrency;
    } else {
      totalStakeInUserCurrency = totalStakeInPoolCurrency && this.currencyCalculator
        ? this.currencyCalculator.currencyExchange(this.poolCurrencyCode, this.userCurrencyCode,
          totalStakeInPoolCurrency) : null;
    }
    return totalStakeInUserCurrency && (+totalStakeInUserCurrency).toFixed(2);
  }

  /**
   * Check if bet is ready to be add to Betslip
   * @returns {Boolean}
   * @private
   */
  private checkIfBetReadyForBetSlip(): boolean {
    let isBetReadyForBetslip;
    if (this.isMultipleLegsBet) {
      isBetReadyForBetslip = !!this.stakePerLine && this.betModel.checkIfAllLegsFilled() && !this.errorField;
    } else {
      isBetReadyForBetslip = !!this.betName;
    }
    return isBetReadyForBetslip;
  }

  private relocateAfter(delay: number = 100): void {
    this.windowRefService.nativeWindow.clearTimeout(this.relocateAfterJob);
    this.relocateAfterJob = this.windowRefService.nativeWindow.setTimeout(() => {
      this.relocate();
    }, delay);
  }

  /**
   * Update state of leg switchers
   * @private
   */
  private updateSwitchersState(): void {
    if (!this.isMultipleLegsBet) {
      return;
    }
    _.forEach(this.betModel.legs, leg => {
      this.pubsubService.publish(this.pubsubService.API.UK_TOTE_LEG_UPDATED, leg);
    });
  }

  /**
   * Get channel ids of events, markets and only selected outcomes
   * @param events {Array} - array of events
   * @param selectedOutcomes {Array} - array of selected outcomes
   * @returns {Object} - object with channel ids for outcomes, events and markets
   * @private
   */
  private getChannelIds(events: ISportEvent[], selectedOutcomes: IOutcome[]): Array<string> {
    const allIdsForEvents = this.ukToteService.getAllIdsForEvents(events);

    allIdsForEvents.outcome = _.compact(_.map(selectedOutcomes, (outcome: IOutcome) => outcome.linkedOutcomeId));

    return this.ukToteLiveUpdatesService.getAllChannels(allIdsForEvents);
  }

  /**
   * Footer visibility
   */
  private setFooterVisibility(visible: boolean): void {
    this.commandService.execute(this.commandService.API.SHOW_HIDE_FOOTER_MENU, [visible || this.deviceService.isTablet], []);
  }

  /**
   * Visibility for betbuilder component
   * @param {boolean} visible
   * @param {boolean} footerVisible
   */
  private setVisibility(visible: boolean, footerVisible: boolean = false): void {
    this.visible = visible;
    if(!visible){this.pubsubService.publish(this.pubsubService.API.DIGIT_KEYBOARD_HIDDEN, 'uk-tote-event');}
    this.setFooterVisibility(footerVisible);
  }

  /**
   * Get stake error name if stake is invalid
   * @returns String - error name
   * @private
   */
  private getValidationError(validationState): string {
    let error;
    for (const key in validationState) {
      if (validationState[key]) {
        error = key;
        break;
      }
    }
    return error;
  }

  /**
   * Validate entered stake
   * @param {Object} options - object with contains stake, totalStake and pool properties
   * @private
   */
  private validateStake(options): string {
    let errorField,
      validationState;
    if (this.stakePerLine) {
      validationState = this.stakeValidatorService.getValidationState(options);
      errorField = this.getValidationError(validationState);
    }
    return errorField;
  }

  /**
   * Add login/logout listeners to update currency
   */
  private addListeners(): void {
    this.pubsubService.subscribe(this.title,
      [this.pubsubService.API.SUCCESSFUL_LOGIN, this.pubsubService.API.SESSION_LOGOUT], () => {
        this.userCurrencyCode = this.userService.currency;
        this.userCurrencySymbol = this.userService.currencySymbol;
        this.totalStakeWithCurrency = this.getTotalStakeWithCurrency();
      });
  }

  private getToteType(): string {
    return UK_TOTE_CONFIG.intTotePoolTypes.indexOf(this.currentPool.type) > -1 ? 'international tote' : 'uk tote';
  }

  private getTotalStakeWithCurrency(): string {
    return this.filtersService.numberWithCurrency(+this.totalStakeInUserCurrency, this.userCurrencySymbol);
  }

  onKeyboardToggle(status: boolean) {
    this.expanded = (this.expanded) ? status: this.expanded
  }
}
