import * as _ from 'underscore';
import { delay } from 'rxjs/operators';
import {
  AfterViewInit, Directive, ElementRef, EventEmitter, HostBinding, HostListener,
  Input, OnChanges, OnDestroy, OnInit, Output, SimpleChanges
} from '@angular/core';

import { DeviceService } from '@core/services/device/device.service';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { Subject } from 'rxjs';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { CoreToolsService } from '@app/core/services/coreTools/core-tools.service';
import { RendererService } from '@shared/services/renderer/renderer.service';
import { ILazyComponentOutput } from '../lazy-component/lazy-component.model';
import { IFreebetsPopupDetails } from '@core/services/cms/models/system-config';
import { IFreebetToken } from '@app/bpp/services/bppProviders/bpp-providers.model';
import environment from '@environment/oxygenEnvConfig';
import { LocaleService } from '@core/services/locale/locale.service';
import { bma } from '@app/lazy-modules/locale/translations/en-US/bma.lang';
import { BetslipService } from '@app/betslip/services/betslip/betslip.service';

@Directive({
  // eslint-disable-next-line
  selector: '[digit-keyboard-input]',
})
export class DigitKeyboardInputDirective implements AfterViewInit, OnChanges, OnDestroy, OnInit {
  @HostBinding('attr.type') hostType: string | null = null;
  @HostBinding('attr.readonly') hostReadonly: string | null = null;
  @HostBinding('attr.tabindex') hostTabindex: string | null = null;

  @Input() componentId?: string;
  @Input() disabled?: boolean;
  @Input() eventAction: string;
  @Input() eventLocation?: string;
  @Input() maxLength?: number;
  @Input() ngModel: string;
  @Input() numbersOnly?: boolean;
  @Input() showDecimalPoint: boolean;
  @Input() showQuickDepositButtons?: boolean;
  @Input() quickStakeItems?: number[];
  @Input() showOnDesktop?: boolean;
  @Input() freebetsList?: IFreebetToken[];
  @Input() selectedFreeBet?: IFreebetToken;
  @Input() freebetsConfig?: IFreebetsPopupDetails;
  @Input() isBoostEnabled?: boolean;
  @Input() isSelectionBoosted?: boolean;
  @Input() canBoostSelection?: boolean;
  @Input() betPackList: IFreebetToken[];
  @Input() fanzoneList: IFreebetToken[];
  @Input() isTotePool: boolean;

  @Output() readonly isInit: EventEmitter<boolean> = new EventEmitter();
  @Output() readonly ngModelChange: EventEmitter<string> = new EventEmitter();
  @Output() freeBetSelected: EventEmitter<ILazyComponentOutput> = new EventEmitter();

  private viewReady$ = new Subject();
  private bsSelectionsElement: HTMLElement;
  private bsTotalElement: HTMLElement;
  private keyboardElement: HTMLElement;
  private qsElement: HTMLElement;
  private mainElement: HTMLElement;
  private mainElementTouchSubscription: Function;
  private element: HTMLElement;

  private currentValue: string;
  private currentValueLength: number;
  private depositPlaceholder: string;

  private isEdited: boolean = false;
  private newValue: string;
  private dkActiveInputClass = 'dk-active-input';
  private freeBetUuidAttr = 'data-uuid';
  private qdCvvId: string = 'QDCVV2';
  private qdAmount: string = 'QDAmount';
  private shouldInit: boolean;
  private stakeClickHandlerInProgressFlag: boolean;

  private uuid = `DigitKeyboardInputDirective-${this.coreToolsService.uuid()}`;
  private quikStateUuid = `DigitKeyboardInputDirective-${this.coreToolsService.uuid()}`;
  private freebetUuid = `DigitKeyboardInputDirective-${this.coreToolsService.uuid()}`;

  private isMobileOnly: boolean;
  isBrandLadbrokes: boolean;

  constructor(
    private pubSubService: PubSubService,
    private deviceService: DeviceService,
    private gtmService: GtmService,
    private domToolsService: DomToolsService,
    private rendererService: RendererService,
    private elementRef: ElementRef<HTMLInputElement>,
    private windowRefService: WindowRefService,
    private coreToolsService: CoreToolsService,
    private locale:LocaleService,
    private betslipService:BetslipService
  ) {
    this.isMobileOnly = this.deviceService.isMobileOnly && !this.deviceService.isTabletOrigin;
    this.autoScrollToStakeField = this.autoScrollToStakeField.bind(this);
    this.onCloseHandler = this.onCloseHandler.bind(this);
    this.onKeyBoardPressHandler = this.onKeyBoardPressHandler.bind(this);
    this.setFreeBetSelectedValue = this.setFreeBetSelectedValue.bind(this);
    this.element = this.elementRef.nativeElement;
    this.isBrandLadbrokes = environment.brand === this.locale.getString(bma.brands.ladbrokes).toLowerCase();
  }

  @HostListener('click', ['$event'])
  @HostListener('focus', ['$event'])
  onClickHandler($event: MouseEvent): void {
    if (!this.shouldInit) { return; }
    this.stakeClickHandlerInProgressFlag = true;
    this.windowRefService.nativeWindow.setTimeout(() => { this.stakeClickHandlerInProgressFlag = false; }, 1000);
    $event.stopPropagation();
    $event.preventDefault();

    // close native navigation panel (prev, next, done) opened on focus
    this.isMobileOnly && (<HTMLElement>$event.target).blur();

    this.isEdited = false;

    this.pubSubService.publish(this.pubSubService.API.BETSLIP_BALANCE_DROPDOWN_HIDE);

    if ($event.isTrusted) {
      this.pubSubService.publish(this.pubSubService.API.BS_HIDE_FREEBET_TOOLTIP);
    }

    this.subscribeOnMainElementTouchEvent();
    this.clearActiveElement();
    this.setActiveElement();
    this.resetPlaceholder();
    this.subscribeToEvent();
    this.validateValue();
  }

  ngOnChanges(changesObj: SimpleChanges): void {
    if (!this.shouldInit) { return; }
    changesObj.disabled && this.whenViewReady(this.disableKeyboard)(changesObj.disabled.currentValue);
  }

  /**
   * Check device, set proper attributes, subscribe to events
   */
  ngOnInit(): void {
    this.shouldInit = this.showOnDesktop ? true : this.isMobileOnly;

    if (!this.shouldInit) {
      // Desktop, tablet, etc.
      this.hostType = 'tel';
      return;
    }
    // Mobile phones
    this.hostType = 'text';
    this.hostReadonly = 'readonly';
    this.hostTabindex = '-1';

    this.pubSubService.subscribe(this.quikStateUuid, this.pubSubService.API.QB_QUICKSTAKE_PRESSED, () => {
      this.isEdited = false;
      this.validateValue();
    });

    // set a flag that directive is initialized (so other directives able to check this)
    this.rendererService.renderer.setAttribute(this.element, 'data-has-keyboard', 'true');
  }

  ngAfterViewInit(): void {
    if (!this.shouldInit) {
      this.isInit.emit(false);
      return;
    }

    this.bindElements();
    this.viewReady$.complete();
    this.isInit.emit(true);
  }

  ngOnDestroy(): void {
    if (!this.shouldInit) { return; }
    this.unsubscribeFromMainElementTouchEvent();
    this.hideKeyboard();
    this.renderValue('');
    this.isInit.emit(false);
    this.pubSubService.unsubscribe(this.quikStateUuid);
    this.pubSubService.unsubscribe(this.freebetUuid);
  }

  private bindElements(): void {
    this.mainElement = this.windowRefService.document.getElementById(this.componentId);
    this.keyboardElement = this.mainElement.querySelector('#dk-keyboard');
    this.qsElement = this.mainElement.querySelector('.quickbet-quick-stake');
    this.bsSelectionsElement = this.windowRefService.document.getElementById('bs-selections-wrapper');
    this.bsTotalElement = this.windowRefService.document.getElementById('bs-total-wrapper');
  }

  private subscribeOnMainElementTouchEvent(): void {
    this.unsubscribeFromMainElementTouchEvent();
    this.mainElementTouchSubscription = this.rendererService.renderer.listen(this.mainElement, 'click', this.onCloseHandler);
  }

  private unsubscribeFromMainElementTouchEvent(): void {
    (typeof this.mainElementTouchSubscription === 'function') && this.mainElementTouchSubscription();
  }

  /**
   * Auto scroll to stake field if it's necessary
   */
  private autoScrollToStakeField(): void {
    const bsTotalWrapper = this.windowRefService.document.querySelector('.in-bs-footer');
    const totalWrapperHeight = bsTotalWrapper ? this.domToolsService.getHeight(bsTotalWrapper) : 0;
    const elementOffset = this.domToolsService.getOffset(this.elementRef.nativeElement);
    const keyboardOffset = this.domToolsService.getOffset(this.keyboardElement);
    const totalHeight = this.domToolsService.getHeight(this.bsTotalElement) + this.domToolsService.getHeight(this.elementRef.nativeElement);
    const bsSelectionsScrollTop = this.domToolsService.getScrollTop(this.bsSelectionsElement);
    const bsStakeClosestElement = this.domToolsService.closest(this.elementRef.nativeElement, '.bs-stake');
    const bsStakeClosestHeight = this.domToolsService.getHeight(bsStakeClosestElement);

    if (keyboardOffset && elementOffset.top > (keyboardOffset.top - totalHeight)) {
      const calculatedTop = bsSelectionsScrollTop + (elementOffset.top - keyboardOffset.top) + bsStakeClosestHeight + totalWrapperHeight;
      this.bsSelectionsElement && this.rendererService.renderer.setProperty(this.bsSelectionsElement, 'scrollTop', calculatedTop);
    }
  }

  /**
   * @params {object} event
   */
  private onCloseHandler(event: MouseEvent): void {
    if (this.stakeClickHandlerInProgressFlag) {
      const element = this.windowRefService.document.querySelector('.quickbet-content .stake-input');
      if (element) {
        this.rendererService.renderer.addClass(element, 'dk-active-input');
      }
      return;
    }
    event.stopPropagation();
    const target = <HTMLElement>(event.target || event.srcElement);
    const isValidTarget = target !== this.elementRef.nativeElement
      && !this.domToolsService.isChild(target, this.keyboardElement)
      && !this.domToolsService.isChild(target, this.qsElement);
    if (isValidTarget) {
      this.unsubscribeFromMainElementTouchEvent();
      this.restorePlaceholder();
      this.hideKeyboard();
      this.validateValue();
      this.renderValue(this.ngModel);
    }
  }

  /**
   * @params {string} value
   */
  private onKeyBoardPressHandler(value: string): void {
    // active input elements CVV/Amount || stake
    const activeInputElement: boolean = this.elementRef.nativeElement.parentElement.classList.contains(this.dkActiveInputClass)
      || this.elementRef.nativeElement.classList.contains(this.dkActiveInputClass);
    if (!activeInputElement) { return; }

    this.currentValue = (this.ngModel || '').toString();
    this.currentValueLength = this.currentValue.length;
    const outcomeId=this.elementRef.nativeElement.classList[0];
    if (value.substring(0, 2) === 'qb') {      
      if(!this.betslipService.betKeyboardData.includes(outcomeId)){
        this.betslipService.betKeyboardData = outcomeId;
      }
      this.handleQDButton(value);
      return;
    }

    switch (value) {
      case 'enter': {
        this.handleEnter(value);
        break;
      }
      case 'delete': {
        this.handleDelete(value);
        break;
      }
      case '.': {
        this.handleDot(value);
        break;
      }
      default: {
        this.handleNumber(value);
        this.betslipService.filterKyeBoardData=outcomeId;
      }
    }
  }

  /**
   * Handle 'Enter' pressed
   * @param {string} value
   */
  private handleEnter(value: string): void {
    this.restorePlaceholder();
    this.hideKeyboard();
    this.allInputsValueToFixed();
    this.validateValue();

    this.pubSubService.publish(this.pubSubService.API.DIGIT_KEYBOARD_DEC_DOT_PRESSED, [this.newValue, value]);
  }

  /**
   * Handle 'Delete' pressed
   * @param value
   */
  private handleDelete(value: string): void {
    this.isEdited = true;
    if (this.currentValue.charAt(this.currentValueLength - 2) === '.') {
      this.newValue = this.currentValue.substring(0, this.currentValueLength - 2);
    } else {
      this.newValue = this.currentValue.substring(0, this.currentValueLength - 1);
    }

    this.ngModelChange.emit(this.newValue);
    this.pubSubService.publishSync(this.pubSubService.API.DIGIT_KEYBOARD_DEC_DOT_PRESSED, [this.newValue, value]);
  }

  /**
   * Handle decimal point pressed
   * @param value
   */
  private handleDot(value: string): void {
    if (!this.isEdited || !this.currentValue) {
      this.isEdited = true;
      this.currentValue = '0.';
      this.newValue = '0.';
    }

    if (this.currentValue.indexOf('.') === -1) {
      this.newValue = `${this.currentValue}.`;
    }
    this.ngModelChange.emit(this.newValue);

    this.pubSubService.publish(this.pubSubService.API.DIGIT_KEYBOARD_DEC_DOT_PRESSED, [this.newValue, value]);
  }

  /**
   * Handle quick deposit button
   * @param value
   */
  private handleQDButton(value: string): void {
    const amount = value.substring(3, value.length);
    const pushEvent: any = {
      eventCategory: this.eventAction,
      eventDetails: amount,
      eventAction: 'click',
      eventLabel:'keypad predefined stake',
      locationEvent:'betslip stake',
      positionEvent:this.isBrandLadbrokes?'top':'bottom',
    };
    if (this.eventAction === 'quick deposit') {
      pushEvent.location = this.eventLocation;
    }
    this.gtmService.push('trackEvent', pushEvent);
    this.isEdited = false;

    this.newValue = (parseFloat(this.currentValue || '0') + parseFloat(amount)).toFixed(2);
    const dec = this.newValue.split('.');
    if (dec.length > 1) {
      dec[1] = dec[1].substring(0, 2);
      this.newValue = Number(dec.join(".")).toFixed(2);
    }
    this.ngModelChange.emit(this.newValue);
  }

  /**
   * Handle number pressed
   * @param value
   */
  private handleNumber(value: string): void {
    if (!this.isEdited) {
      this.isEdited = true;
      this.currentValue = '';
      this.currentValueLength = 0;
    }

    if (this.maxLength && this.currentValueLength === this.maxLength) {
      return;
    }

    this.newValue = `${this.currentValue}${value}`;

    const pattern = this.eventLocation === 'quick deposit' ? '^\\d{0,7}(\\.\\d{0,2}){0,1}$' : '^\\d{0,12}(\\.\\d{0,2}){0,1}$';

    if (!this.newValue.match(pattern)) {
      this.newValue = this.currentValue;
    }

    this.ngModelChange.emit(this.newValue);
    this.pubSubService.publish(this.pubSubService.API.DIGIT_KEYBOARD_DEC_DOT_PRESSED, [this.newValue, value]);
  }

  /**
   * Render input value to proper format
   * @params {string} value
   */
  private renderValue(value: string): void {
    this.rendererService.renderer.setAttribute(this.elementRef.nativeElement, 'value', value && value.length && Number(value) !== 0
      ? (this.numbersOnly ? Number(value).toString() : Number(value).toFixed(2)) : '');
  }

  /**
   * Sets class to the selected item
   */
  private setActiveElement(): void {
    const activeInputElements = this.windowRefService.document
      .querySelectorAll<HTMLElement>(`.custom-input-container.${this.dkActiveInputClass}`);

    _.each(activeInputElements, (element: HTMLElement) => this.rendererService.renderer.removeClass(element, this.dkActiveInputClass));

    const activeInputElement = this.elementRef.nativeElement.id === this.qdCvvId || this.elementRef.nativeElement.id === this.qdAmount
      ? this.domToolsService.closest(this.elementRef.nativeElement, '.custom-input-container')
      : this.elementRef.nativeElement;

    this.rendererService.renderer.addClass(activeInputElement, this.dkActiveInputClass);
    this.rendererService.renderer.setAttribute(activeInputElement, this.freeBetUuidAttr, this.freebetUuid);
  }

  /**
   * Clears active class, restores placeholders
   */
  private clearActiveElement(): void {
    const inputElements = this.mainElement ?
      this.mainElement.querySelectorAll<HTMLInputElement>('input[type=text], .custom-input-container') : [];

    _.each(inputElements, (inputElement: HTMLInputElement) => {
      this.rendererService.renderer.removeClass(inputElement, this.dkActiveInputClass);

      //removes the previous subscriber to avoid adding freebet selection to the previous stake
      if (inputElement.attributes[this.freeBetUuidAttr]) {
        this.pubSubService.unsubscribe(inputElement.attributes[this.freeBetUuidAttr].value);
        this.rendererService.renderer.removeAttribute(inputElement, this.freeBetUuidAttr);
      }
      // CVV field should be without placeholder
      if (inputElement.id !== this.qdCvvId && inputElement.id !== this.qdAmount && !this.isTotePool) {
        this.rendererService.renderer.setAttribute(inputElement, 'placeholder', 'Stake');
      } else if (inputElement.id === this.qdAmount && this.depositPlaceholder) {
        this.rendererService.renderer.setAttribute(inputElement, 'placeholder', this.depositPlaceholder);
      }
    });

    this.allInputsValueToFixed();
  }

  /**
   * Find and format all inputs value
   */
  private allInputsValueToFixed(): void {
    const inputElements = this.bsSelectionsElement ?
      this.bsSelectionsElement.querySelectorAll<HTMLInputElement>('input[type=text], .custom-input-container') : [];

    _.each(inputElements, (inputElement: HTMLInputElement) => {
      inputElement.value && this.rendererService.renderer.setAttribute(inputElement, 'value', Number(inputElement.value).toFixed(2));
    });
  }

  /**
   * Validate and set value to proper format
   */
  private validateValue(): void {
    const inputValue = this.ngModel;
    if (inputValue && (this.elementRef.nativeElement.id !== this.qdCvvId)) {
      this.ngModelChange.emit(Number(inputValue).toFixed(2));
    }
    if (Number(inputValue)) {
      this.renderValue(inputValue);
    }
  }

  /**
   * Removes input placeholder on click
   */
  private resetPlaceholder(): void {
    const activePlaceholder = 'Stake';

    // CVV field should be without placeholder and deposit amount placeholder should not be changed
    if (this.elementRef.nativeElement.id !== this.qdCvvId && this.elementRef.nativeElement.id !== this.qdAmount && !this.isTotePool) {
      this.rendererService.renderer.setAttribute(this.elementRef.nativeElement, 'placeholder', activePlaceholder);
    }
  }

  /**
   * Restores placeholder on blur
   */
  private restorePlaceholder(): void {
    if (this.elementRef.nativeElement.id !== this.qdCvvId &&
      this.elementRef.nativeElement.id !== this.qdAmount) {
      this.rendererService.renderer.setAttribute(this.elementRef.nativeElement, 'placeholder', '0.00');
    } else if (this.elementRef.nativeElement.id === this.qdAmount && this.depositPlaceholder) {
      this.rendererService.renderer.setAttribute(this.elementRef.nativeElement, 'placeholder', this.depositPlaceholder);
    }
  }

  /**
   * Subscribe to element events
   */
  private subscribeToEvent(): void {
    const isAsync = !(this.deviceService.isIos && this.deviceService.isWrapper);

    this.pubSubService.publish(this.pubSubService.API.FREEBETS_BY_SELECTION, [this.freebetsList,
      this.selectedFreeBet, this.freebetsConfig, this.isBoostEnabled, this.isSelectionBoosted, this.canBoostSelection,this.betPackList,this.fanzoneList]);
    this.pubSubService.publish(this.pubSubService.API.DIGIT_KEYBOARD_SHOWN, [this.showDecimalPoint,
      this.showQuickDepositButtons,this.quickStakeItems, this.componentId, this.isTotePool], isAsync);
    this.pubSubService.subscribe(this.uuid, this.pubSubService.API.DIGIT_KEYBOARD_KEY_PRESSED,
      this.onKeyBoardPressHandler);
    this.pubSubService.subscribe(this.freebetUuid, this.pubSubService.API.FREEBET_SELECTED_EVENT,
      this.setFreeBetSelectedValue);
    // TODO: Attempt to avoid using setTimeout: formerly used $animate.removeClass(...).then(...)
    setTimeout(this.autoScrollToStakeField, 100);
  }

  /**
   * Sets selected FB and emits action
   * @param event {ILazyComponentOutput}
   */
  private setFreeBetSelectedValue(event: ILazyComponentOutput){
    this.selectedFreeBet = event.value;
    this.freeBetSelected.emit(event);
  }

  private disableKeyboard(disabled) {
    if (disabled) {
      this.unsubscribeFromMainElementTouchEvent();
      this.hideKeyboard();
    }
  }

  /**
   * Hide keyboard
   */
  private hideKeyboard(): void {
    this.pubSubService.publish(this.pubSubService.API.DIGIT_KEYBOARD_HIDDEN, this.componentId);
    this.pubSubService.unsubscribe(this.uuid);
    this.clearActiveElement();
  }

  /**
   * Returns wrapping function which executes the provided method on Subject completion,
   * which happens after the ngAfterViewInit hook.
   * The context is preserved. Arguments of wrapper are passed to the callback.
   */
  private whenViewReady(cb: Function): Function {
    return (...params): void => {
      this.viewReady$.asObservable().pipe(delay(0)).subscribe(null, null, cb.bind(this, ...params));
    };
  }
}
