import {
  Component, ElementRef, EventEmitter, Input, OnChanges, OnDestroy,
  OnInit, Output, QueryList, ViewChild, ViewChildren, ChangeDetectorRef
} from '@angular/core';
import * as _ from 'underscore';

import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { CoreToolsService } from '@app/core/services/coreTools/core-tools.service';
import { IFreebetToken } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { ILazyComponentOutput } from '@shared/components/lazy-component/lazy-component.model';
import { IFreebetsPopupDetails } from '@core/services/cms/models/system-config';
import environment from '@environment/oxygenEnvConfig';
import { LocaleService } from '@core/services/locale/locale.service';
import { bma } from '@app/lazy-modules/locale/translations/en-US/bma.lang';
import { StorageService } from '@core/services/storage/storage.service';
import { ToteBetslipService } from '@app/betslip/services/toteBetslip/tote-betslip.service';
import { ItoteFreeBets } from '@betslip/services/toteBetslip/tote-betslip.model';

interface ILabelledValue {
  label: string;
  value: string;
}

@Component({
  selector: 'digit-keyboard',
  templateUrl: 'digit-keyboard.component.html',
  styleUrls: ['digit-keyboard.component.scss']
})
export class DigitKeyboardComponent implements OnInit, OnChanges, OnDestroy {
  @ViewChild('dkKeyEnter', {static: false}) enterKey: ElementRef<HTMLElement>;
  @ViewChildren('dkKey') keyboardKeys: QueryList<ElementRef<HTMLElement>>;
  @ViewChildren('qsKey') quickStakeKeys: QueryList<ElementRef<HTMLElement>>;

  @Input() currency?: string;
  @Input() componentId: string;
  @Input() hideKeyboardFlag?: boolean;
  @Input() isBetslip: boolean;
  @Input() freeBetImageName:string;
  @Input() selectedToteFreeBetValue?: any;
  @Input() areToteBetsInBetslip?: boolean;
  @Input() toteFreeBetSelected?: boolean;

  @Output() readonly isNotBackspace: EventEmitter<boolean> = new EventEmitter();
  @Output() readonly keyboardShown: EventEmitter<void> = new EventEmitter();
  @Output() readonly keyboardHidden: EventEmitter<void> = new EventEmitter();

  isDecimalButtonEnabled: boolean = true;
  isDecimalPointPressed: boolean = false;
  isTotePool: boolean;
  isKeyboardShown: boolean = false;
  isQuickDepositButtonsShown: boolean = false;
  quickDepositButtons: ILabelledValue[] = [];
  availableFreeBets: IFreebetToken[];
  availableBetPacks: IFreebetToken[];
  availableFanzone: IFreebetToken[];
  selected: IFreebetToken;
  freebetsConfig: IFreebetsPopupDetails;
  isBoostEnabled: boolean;
  isSelectionBoosted: boolean;
  canBoostSelection: boolean;
  isBrandLadbrokes: boolean;
  availableToteFreeBets:  ItoteFreeBets[];
  availableToteBetPacks:  ItoteFreeBets[];
  triggeredFromToteBets: boolean = false;
  selectedToteFreeBetObj: any;

  readonly tagName: string = 'digitKeyboard';

  private uuid = `DigitKeyboardComponent-${this.coreToolsService.uuid()}`;
  private freeBetUuid = `DigitKeyboardComponent-${this.coreToolsService.uuid()}`;
  quickStakeItemsList: ILabelledValue[] = [];

  constructor(
    private pubSubService: PubSubService,
    private coreToolsService: CoreToolsService,
    private changeDetectorRef: ChangeDetectorRef,
    private locale: LocaleService,
    private storageService: StorageService,
    private toteBetslipService: ToteBetslipService
  ) {
    this.isBrandLadbrokes = environment.brand === this.locale.getString(bma.brands.ladbrokes).toLowerCase();
  }

  ngOnInit(): void {
    this.availableToteFreeBets = this.storageService.get('toteFreeBets');
    this.availableToteBetPacks = this.storageService.get('toteBetPacks');
    const toteBet = this.storageService.get('toteBet');
    if((this.availableToteFreeBets && this.availableToteFreeBets.length > 0) || (this.availableToteBetPacks && this.availableToteBetPacks.length > 0)) {
      this.checkIfToteFreebetAdded(toteBet, this.availableToteFreeBets, this.availableToteBetPacks);
    }
    this.setLabels();
    this.pubSubService.subscribe(this.uuid,
      this.pubSubService.API.DIGIT_KEYBOARD_DEC_DOT_PRESSED, this.updateDecimalPointState.bind(this));
    this.pubSubService.subscribe(this.uuid,
      this.pubSubService.API.DIGIT_KEYBOARD_SHOWN, this.showKeyboard.bind(this));
      this.pubSubService.subscribe(this.uuid,
        this.pubSubService.API.MAIN_BETSLIP_STAKES, this.showKeyboard.bind(this));
    this.pubSubService.subscribe(this.uuid,
      this.pubSubService.API.DIGIT_KEYBOARD_HIDDEN, this.hideKeyboard.bind(this));
    this.hideKeyboardFlag = typeof this.hideKeyboardFlag === 'boolean' ? this.hideKeyboardFlag : true;
    this.pubSubService.subscribe(this.freeBetUuid, this.pubSubService.API.FREEBETS_BY_SELECTION,
      this.setFreeBetList.bind(this));
    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.ODDS_BOOST_UNSET_FREEBETS, () => {
      this.selected = null;
    });
  }

  checkIfToteFreebetAdded(toteBet, toteFreeBets, toteBetPacks) : void {
    if(toteBet !== null && toteBet && toteBet.poolBet) {
      const freebetTokenId = toteBet.poolBet.freebetTokenId;
      if(freebetTokenId) {
        this.reAssignSelectedToteFreeBetObj(freebetTokenId, toteFreeBets, toteBetPacks);
      }
    }
  }

  reAssignSelectedToteFreeBetObj(freebetTokenId, toteFreeBets, toteBetPacks) : void {
    const filteredToteBet = toteFreeBets && toteFreeBets.filter(list => list.freebetTokenId === freebetTokenId);
    const filteredToteBetPack = toteBetPacks && toteBetPacks.filter(list => list.freebetTokenId === freebetTokenId);
      if(filteredToteBet.length > 0) {
        this.selectedToteFreeBetObj = filteredToteBet;
      } else if(filteredToteBetPack.length > 0) {
        this.selectedToteFreeBetObj = filteredToteBetPack;
      }
  }

  ngOnChanges(): void {
    this.setLabels();
  }

  ngOnDestroy(): void {
    this.pubSubService.unsubscribe(this.uuid);
    this.pubSubService.unsubscribe(this.freeBetUuid);
    this.pubSubService.unsubscribe(this.tagName);
  }

  /**
   * Handles key press
   * @param {MouseEvent} $event
   */
  onButtonClickHandler($event: MouseEvent,stakeType?:string): void {
    const value = (<HTMLElement>$event.target).dataset.value;
    if (value === '.') {
      if (!this.isDecimalButtonEnabled) { return; }
      this.isDecimalPointPressed = true;
    }
    if(stakeType && stakeType ==='qb'){
      this.pubSubService.publishSync(this.pubSubService.API.QB_QUICKSTAKE_PRESSED_DIGIT_KEYBOARD, value);      
    }
      this.pubSubService.publishSync(this.pubSubService.API.DIGIT_KEYBOARD_KEY_PRESSED, value);
    
    $event.stopPropagation();
    this.clickTransition(value);
  }  

  clickTransition(value: string) {
    const element = document.getElementsByClassName(`dk-key-${value}`) as any;
    [].forEach.call(element, (el) => {
      el["style"].backgroundColor = this.isBrandLadbrokes ? value.includes('qb') ? "#AAAAAA" : "#D5D5D5": value.includes('qb') ? "#084D8D" : "rgba(18,132,224,0.11)";
    })
    this.changeDetectorRef.detectChanges();
    setTimeout(() => {
      const removeClass = document.getElementsByClassName(`dk-key-${value}`);
      [].forEach.call(removeClass, (el) => {
        el["style"].backgroundColor = value.includes('qb') ? "#252835" : "#FFFFFF";
      })
    }, 250)
  }

  /**
   * @param {IFreebetToken[]} freebetsList
   * @param {IFreebetToken} selectedFreeBet
   * @param {IFreebetsPopupDetails} freebetsConfig
   * @param {boolean} isBoostEnabled
   * @param {boolean} isSelectionBoosted
   * @param {boolean} canBoostSelection
   * @param {IFreebetToken[]} betPackList
   */
  setFreeBetList(freebetsList: IFreebetToken[], selectedFreeBet: IFreebetToken, freebetsConfig: IFreebetsPopupDetails,
    isBoostEnabled: boolean, isSelectionBoosted: boolean, canBoostSelection: boolean, betPackList: IFreebetToken[], fanzoneList: IFreebetToken[]): void {
    this.availableFreeBets = freebetsList;
    this.selected = selectedFreeBet;
    if(this.triggeredFromToteBets) { 
      this.selectedToteFreeBetObj = selectedFreeBet;
    }
    this.freebetsConfig = freebetsConfig;
    this.isBoostEnabled = isBoostEnabled;
    this.isSelectionBoosted = isSelectionBoosted;
    this.canBoostSelection = canBoostSelection;
    this.availableBetPacks = betPackList;
    this.availableFanzone = fanzoneList;

  }
/**
 * Publish event on freebet change
 * @param {ILazyComponentOutput} event
 */
  onFreebetChange(event: ILazyComponentOutput): void {
    this.selected = event.value;
    this.pubSubService.publishSync(this.pubSubService.API.FREEBET_SELECTED_EVENT, event);
  }

  onToteFreebetChange(event: any): void {
    this.selectedToteFreeBetObj = event.value;
    this.triggeredFromToteBets = true;
    this.pubSubService.publishSync(this.pubSubService.API.FREEBET_SELECTED_EVENT, event);
  }

  private getLabelData(values: number[] | string[]): ILabelledValue[] {
    return _.map(values, (value: number | string): ILabelledValue => ({ label: this.getLabelWithCurrency(value), value: `qb-${value}` }));
  }

  private getLabelWithCurrency(value: number | string): string {
    return `+${this.currency}${value}`;
  }

  private hideKeyboard(componentId: string): void {
    if (this.isKeyboardShown && (this.componentId === componentId)) {
      this.isDecimalButtonEnabled = true;
      this.isDecimalPointPressed = false;
      this.isKeyboardShown = false;
      this.keyboardHidden.emit();
    }
  }

  private setLabels(): void {
    this.quickDepositButtons = this.getLabelData(this.currency === 'Kr' ? [50, 100, 500, 1000] : [5, 10, 50, 100]);
  }

  private showKeyboard(decimalButton: boolean, quickDepositButton: boolean, quickStakeItems: number[] | string[], componentId: string, isTotePool?: boolean): void {
    if (this.componentId === componentId) {
      this.isTotePool = isTotePool;
      this.isDecimalButtonEnabled = decimalButton;
      this.isDecimalPointPressed = false;
      this.isKeyboardShown = true;
      this.isQuickDepositButtonsShown = quickDepositButton;
      this.quickStakeItemsList = this.getLabelData(quickStakeItems);
      this.keyboardShown.emit();
      this.changeDetectorRef.detectChanges();
    }
  }

  /**
   * Identify if 'dot' button should be disabled
   * @params {array} params
   */
  private updateDecimalPointState(newValue: string, value: string): void {
    if (!newValue && !value) {
      return;
    }
    this.isDecimalPointPressed = (newValue && newValue.indexOf('.') !== -1) || (value === '.');
  }

  private setToteFreebetConfig(): any {
    return this.toteBetslipService.getFreeBetsConfig() ;
  }
}
