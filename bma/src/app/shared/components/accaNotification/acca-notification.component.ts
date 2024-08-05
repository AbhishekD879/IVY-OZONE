import { Component, OnInit, OnDestroy, ChangeDetectionStrategy, ChangeDetectorRef } from '@angular/core';

import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { FracToDecService } from '@core/services/fracToDec/frac-to-dec.service';
import { UserService } from '@core/services/user/user.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { DeviceService } from '@core/services/device/device.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { NativeBridgeService } from '@core/services/nativeBridge/native-bridge.service';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';
import { IConstant } from '@core/services/models/constant.model';
import { IFirstMultipleInfo } from '@betslip/models/first-multiple-info';
import { LocaleService } from '@core/services/locale/locale.service';
import { IBetSelection } from '@betslip/services/betSelection/bet-selection.model';
import { ISystemConfig } from '@core/services/cms/models';
import { CmsService } from '@core/services/cms/cms.service';
import { FiltersService } from '@core/services/filters/filters.service';

@Component({
  changeDetection: ChangeDetectionStrategy.OnPush,
  selector: 'acca-notification',
  templateUrl: 'acca-notification.component.html',
  styleUrls: ['acca-notification.component.scss']
})

export class AccaNotificationComponent implements OnInit, OnDestroy {
  subscriberName: string = 'bma-accaBar';
  teamselectionNames = [];
  price: string;
  betType: string;
  isBetValid: boolean = false;
  homeBody: Element;
  window: IConstant;
  timelineShown: boolean = false;
  NWIndicatorShown: boolean = false;
  isLoadingAnimationActive: boolean = false; // animation as fallback for quick recalculation

  readonly minPayout: number = 1.00099;
  readonly animationDuration: number = 2000; // animation time of diagonal-shine-animation, ms
  readonly displaylimit: number = 50;
  readonly divWidthlimit: number = 6.4;

  private isRecalculationEnabled: boolean;
  private isAnimationEnabled: boolean;
  private animationStart: number;

  constructor(
    protected nativeBridgeService: NativeBridgeService,
    protected user: UserService,
    protected fracToDec: FracToDecService,
    protected domTools: DomToolsService,
    protected pubsub: PubSubService,
    protected deviceService: DeviceService,
    protected GTM: GtmService,
    protected windowRef: WindowRefService,
    protected localeService: LocaleService,
    protected cmsService: CmsService,
    protected changeDetectorRef: ChangeDetectorRef,
    protected filterService: FiltersService
  ) {
    this.window = this.windowRef.nativeWindow;
  }

  ngOnInit(): void {
    this.homeBody = this.deviceService.isWrapper ?
                          this.windowRef.document.querySelector('body') : this.windowRef.document.querySelector('html, body');

    this.pubsub.subscribe(this.subscriberName, this.pubsub.API.ACCA_NOTIFICATION_CHANGED, this.updateAccaData.bind(this));
    this.pubsub.subscribe(this.subscriberName, this.pubsub.API.TIMELINE_SHOWN, (timelineShown: boolean) => {
      this.timelineShown = timelineShown;
    });

    this.pubsub.subscribe(this.subscriberName, 'NW_INDICATOR_DISPLAY', (NWIndicatorShown: boolean) => {
      this.NWIndicatorShown = NWIndicatorShown;
      this.changeDetectorRef.markForCheck();
    });

    this.getCmsConfig();
    this.subscribeToBsUpdate();
  }

  ngOnDestroy(): void {
    this.pubsub.unsubscribe(this.subscriberName);
  }

  /**
   * Update acca bar when data when recalculated (on FE/BE),
   *  send notification to native bridge.
   *
   * @param ACCAData
   */
  updateAccaData(ACCAData: IFirstMultipleInfo): void {
    const potentialPayout: number = ACCAData && typeof ACCAData.potentialPayout !== 'string' && ACCAData.potentialPayout;
    const accaPriceDec: string = potentialPayout && this.fracToDec.roundTwoFraction(potentialPayout);
    this.isBetValid = potentialPayout > this.minPayout;
    this.betType = ACCAData && this.localeService.getString(`bs.${ACCAData.translatedType}`);
    if (this.isBetValid) {
      if (this.user.oddsFormat === 'frac') {
        this.price = this.fracToDec.getAccumulatorPrice(this.fracToDec.decToFrac(potentialPayout, true));
      } else {
        this.price = accaPriceDec;
      }

      this.nativeBridgeService.accaNotificationChanged({
        title: ACCAData.translatedType,
        price: accaPriceDec
      });
    } else {
      this.nativeBridgeService.accaNotificationChanged();
    }
    this.changeDetectorRef.markForCheck();

    if (this.isAnimationEnabled && this.animationStart) {
      const remainingAnimationTime = this.animationDuration - ((Date.now() - this.animationStart) % this.animationDuration);

      this.windowRef.nativeWindow.setTimeout(() => {
        this.isLoadingAnimationActive = false;
        this.changeDetectorRef.markForCheck();
      }, remainingAnimationTime);
    }
  }

  /**
   * Check if quick recalculation (`accaQuickRecalculation`) or alternative loading animation are enabled
   */
  getCmsConfig(): void {
    this.cmsService.getSystemConfig().subscribe((config: ISystemConfig) => {
      this.isRecalculationEnabled = !!(config.accaQuickRecalculation && config.accaQuickRecalculation.enabled);
      this.isAnimationEnabled = !!(config.accaQuickRecalculation && config.accaQuickRecalculation.allowLoadingAnimation);
    });
  }

  /**
   * Subscribe to bs selections in order to trigger refresh of acca bar info
   *  if quick recalculation is disabled but animation fallback is allowed - display shine-animation
   */
  subscribeToBsUpdate(): void {
    this.pubsub.subscribe(this.subscriberName, this.pubsub.API.BETSLIP_SELECTIONS_UPDATE, (...selections: IBetSelection[] | any) => {
      if (Array.isArray(selections) && selections.some((res:any) => res.isLotto)) {
        return;
      }
      if (this.isRecalculationEnabled) {
        this.calculateAccaData(selections);
      } else if (this.isAnimationEnabled) {
        const isAnimationStartRequired = this.isBetValid && !this.isLoadingAnimationActive;

        if (isAnimationStartRequired) {
          this.isLoadingAnimationActive = true;
          this.animationStart = Date.now();
          this.changeDetectorRef.markForCheck();
        }
      }
    });
  }

  /**
   * Focus to first multiple input, track click event
   */
  focusOnMultiple(): void {
    this.GTM.push('trackEvent', {
      eventAction: 'click ',
      eventLabel: 'odds notification banner'
    });
    const firstMultiple = this.window.document.querySelector('input#accaMultipleStake-0');

    const additionalOffsetTop = 100; // Space to show BetSlip and Multiples() headers, px
    const keyboardDisplayTime = 400; // Approximate time for keyboard to appear, ms
    const autoSrollDelay = 200;

    this.pubsub.publishSync(this.pubsub.API['show-slide-out-betslip'], true);

    this.windowRef.nativeWindow.setTimeout(() => {
      // Input focus is triggered directly from click handler
      // to open keyboard on iOS phones
      const focusEvent = new Event('focus');
      firstMultiple.dispatchEvent(focusEvent);

      this.windowRef.nativeWindow.setTimeout(() => {
        const multipleOffsetTop = this.domTools.getOffset(firstMultiple).top - additionalOffsetTop;
        this.scrollToFn(multipleOffsetTop,firstMultiple);
      }, autoSrollDelay);
    }, keyboardDisplayTime, false);
  }

  /**
   * Prepare and publish info-data of fresh selections based on FE calculations,
   *  no bpp requests involved
   *
   * @param selections
   */
  calculateAccaData(selections: IBetSelection[]): void {
    const ACCAData: IFirstMultipleInfo = {};
    const selectionsLen = selections.length;

    if (selectionsLen > 1) {
      const uniqEventIds: Set<number> = new Set();
      const selectionNames = [];
      let specialsCount = 0;
      let accaReturnDec = 1;

      selections.forEach((selection: IBetSelection) => {
        const selectionPriceDecRaw = this.fracToDec.getDecimal(selection.price.priceNum, selection.price.priceDen, 16);
        accaReturnDec *= +selectionPriceDecRaw;

        selection.isSpecial && specialsCount++;
        uniqEventIds.add(selection.eventId);
        let teamName: string;
        if (selection.outcomes[0]) {
          teamName = selection.hasOwnProperty('eventName') ? selection.eventName : selection.outcomes[0].details.info.event;
          const selectionLabelName = this.filterPlayerName(selection.outcomes[0].name, teamName);
          selectionNames.push(selectionLabelName);
          this.teamselectionNames = [...selectionNames];
        }
      });
      const allSelectionsFromDifferentEvents = uniqEventIds.size === selectionsLen;

      if (allSelectionsFromDifferentEvents && !specialsCount) {
        ACCAData.translatedType = this.getAccaTypeByCount(selectionsLen);
        ACCAData.potentialPayout = +accaReturnDec;
      }
    }

    this.pubsub.publishSync(this.pubsub.API.ACCA_NOTIFICATION_CHANGED, ACCAData);
  }
  
  /**
   * Generate type of possible accumulator based on selections count
   * (should be in sync with bs.lang)
   *
   * @param count
   */
  getAccaTypeByCount(count: number): string {
    if (count > 9) { return `AC${count}`; }
    if (count > 3) { return `ACC${count}`; }
    if (count === 3) { return `TBL`; }
    if (count === 2) { return `DBL`; }

    return ``;
  }

  filterPlayerName(selectionName: string, teamName: string): string {
    if (selectionName.toLowerCase() == 'home') {
      return this.filterService.getTeamName(teamName, 0);
    } else if (selectionName.toLowerCase() == 'away') {
      return this.filterService.getTeamName(teamName, 1);
    }
    return selectionName;
  }

  getDivWidth(selectionNames: string[]): string {
    let finalText = "";
    let elementAcca = this.window.document.querySelector('.acca-notification ');
    if (elementAcca && selectionNames) {
      elementAcca = elementAcca.offsetWidth;
      const accapadding = this.window.getComputedStyle(document.querySelector(".acca-notification ")).paddingLeft;
      const accawidth = elementAcca - parseInt(accapadding);
      const maxLimit = (accawidth / this.divWidthlimit); // 6.4 is for for each 1 character takes 6.4 px
      let init = 0;
      let sliceIndex = 0;
      if (selectionNames[0] && selectionNames[0].length > maxLimit) {
        sliceIndex++;
        const remLen = `(+${selectionNames.length - sliceIndex})`;
        return selectionNames[0].substring(0, this.displaylimit) + '...' + remLen;
      } else {
        selectionNames.forEach(item => {
          init = init + item.length + 2;// + 2 is for , and (
          if (init <= maxLimit) {
            sliceIndex++;
          }
        });
        finalText = selectionNames.slice(0, sliceIndex).join(", ");
        const remLen = `, (+${selectionNames.length - sliceIndex})`;
        return (selectionNames.length - sliceIndex) > 0 ? finalText + remLen : finalText;
      }

    }
  }
  
  /**
   * Scroll BetSlip sidebar
   * @param {Number,Element} offsetTop
   * @private
   */
  private scrollToFn(offsetTop,firstMultiple): void {
    const scrollableContent = this.window.document.querySelector('.scrollable-content');
    const parentOffsetTop = this.domTools.getOffset(this.domTools.closest(scrollableContent, '.sidebar')).top;
    const contentScrollTop = scrollableContent.scrollTop - parentOffsetTop;

    // Check if scrolling is needed
    if (offsetTop - contentScrollTop !== 0) {
      if (scrollableContent.scrollHeight > this.window.document.documentElement.clientHeight) {
        // Fix for blank space between html element and virtual keyboard on Iphone6 Safari.
        this.homeBody.scrollTop = 0;
      }
      firstMultiple.scrollIntoView()
    }
  }
}

