/**
 * This directive must be used only as attribute of <digit-keyboard-component>
 */
import { AfterViewInit, Directive, ElementRef, Input, OnDestroy, OnInit, Optional, QueryList } from '@angular/core';

import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { DigitKeyboardComponent } from '@shared/components/digitKeyboard/digit-keyboard.component';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { RendererService } from '@shared/services/renderer/renderer.service';

@Directive({
  selector: '[betslip-digit-keyboard]'
})
export class BetslipDigitKeyboardDirective implements OnInit, AfterViewInit, OnDestroy {

  // TODO: To be converted to corresponding Betslip Component@ViewChild references
  private static readonly BS_ELEMENTS = [
    '.betslip-deposit',       // BS_DEPOSIT_HEIGHT
    '.bs-buttons-wrapper',    // BS_FOOTER_BUTTONS_HEIGHT
    '.bs-total-wrapper',      // BS_FOOTER_TOTAL_HEIGHT
    '.sidebar-header-top',    // BS_TOP_HEADER_HEIGHT
    '.sidebar-header-bottom'  // BS_BOTTOM_HEADER_HEIGHT
  ];

  @Input() showQuickDeposit: boolean;

  private enterKey: ElementRef<HTMLElement>;
  private keyboardKeys: QueryList<ElementRef<HTMLElement>>;
  private quickStakeKeys: QueryList<ElementRef<HTMLElement>>;

  constructor(
    private pubSubService: PubSubService,
    private windowRefService: WindowRefService,
    private rendererService: RendererService,
    @Optional() private dkComponent: DigitKeyboardComponent // must be used only as attribute of <digit-keyboard-component>
  ) {}

  ngAfterViewInit(): void {
    if (this.dkComponent) {
      this.enterKey = this.dkComponent.enterKey;
      this.keyboardKeys = this.dkComponent.keyboardKeys;
      this.quickStakeKeys = this.dkComponent.quickStakeKeys;
    }
  }

  ngOnDestroy(): void {
    this.pubSubService.unsubscribe('betslipDigitKeyboardDirective');
  }

  ngOnInit(): void {
    if (!this.dkComponent) {
      console.warn('[betslip-digit-keyboard] directive must be used only as attribute of <digit-keyboard> component!');
      return;
    }

    this.pubSubService.subscribe('betslipDigitKeyboardDirective',
      this.pubSubService.API.DIGIT_KEYBOARD_SHOWN, this.showKeyboard.bind(this));
    this.pubSubService.subscribe('betslipDigitKeyboardDirective',
      this.pubSubService.API.DIGIT_KEYBOARD_HIDDEN, this.hideKeyboard.bind(this));
  }

  private clearInlineStyle(element: ElementRef): void {
    this.rendererService.renderer.removeAttribute(element.nativeElement, 'style');
  }

  private getBsElementsHeight(): number {
    return BetslipDigitKeyboardDirective.BS_ELEMENTS.reduce((totalHeight: number, selector: string): number => {
      const element: HTMLElement = this.windowRefService.document.querySelector(selector);
      return totalHeight + (element && element.offsetHeight || 0);
    }, 0);
  }

  private setElementHeight(height: number, element: ElementRef): void {
    this.rendererService.renderer.setStyle(element.nativeElement, 'height', `${height}px`);
    this.rendererService.renderer.setStyle(element.nativeElement, 'line-height', `${height}px`);
  }

  private hideKeyboard(): void {
    this.enterKey && this.clearInlineStyle(this.enterKey);
    this.keyboardKeys && this.keyboardKeys.forEach(this.clearInlineStyle.bind(this));
    this.quickStakeKeys && this.quickStakeKeys.forEach(this.clearInlineStyle.bind(this));
  }

  /**
   * Checks available space for keyboard, and reduce it if needed
   */
  private showKeyboard(decimalButton: boolean, quickDepositButton: boolean): void {
    const minAllowedHeight = 568, // for now agreed it's iPhone 5 window height
      kbRows = 4, // due to designs
      kbHeight = quickDepositButton ? 175 : 140, // due to designs
      bsQuickStakeHeight = quickDepositButton ? 35 : 0,
      bsElementsHeight = this.getBsElementsHeight() + bsQuickStakeHeight,
      windowHeight = this.windowRefService.nativeWindow.innerHeight,
      availableHeight = windowHeight - bsElementsHeight,
      enterHeight = availableHeight - (availableHeight / kbRows),
      keyHeight = availableHeight / kbRows;

    if (windowHeight <= minAllowedHeight && availableHeight < kbHeight) {
      this.enterKey && this.setElementHeight(enterHeight, this.enterKey);
      this.keyboardKeys && this.keyboardKeys.forEach(this.setElementHeight.bind(this, keyHeight));
      quickDepositButton && this.quickStakeKeys.forEach(this.setElementHeight.bind(this, keyHeight));
    }
  }
}
