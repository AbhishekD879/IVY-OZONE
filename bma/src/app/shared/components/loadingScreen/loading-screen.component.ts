import {
  Component,
  OnChanges,
  OnInit,
  Input,
  SimpleChanges,
  ChangeDetectionStrategy,
  ChangeDetectorRef
} from '@angular/core';

import { DeviceService } from '@core/services/device/device.service';
import { CmsService } from '@core/services/cms/cms.service';
import { WindowRefService } from '@app/core/services/windowRef/window-ref.service';

import { ISystemConfig } from '@core/services/cms/models';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
@Component({
  selector: 'loading-screen',
  templateUrl: 'loading-screen.component.html',
  styleUrls: ['fade-out-animation.scss', 'loading-screen.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})

export class LoadingScreenComponent implements OnInit, OnChanges {
  isTablet: boolean;
  numberOfElements;
  numberOfPricesOrLines: number;
  numberOfSurfaceBets: number;
  numberOfGenericElements: number;
  skeletonFeatureEnabled: boolean;
  blocks = Array;
  hide: boolean = false;
  initialized: boolean = false;
  isHome = false;
  @Input() templateType: string = 'GENERIC';
  @Input() isUsedFromWidget: boolean = false;
  @Input() displayed: boolean = false;
  @Input() skeletonOnlyDisplayed: boolean = false;
  @Input() longRenderView: boolean = false;
  @Input() skeletonOnly: boolean = false;
  @Input() onlySpinner: boolean = false;
  @Input() isFullPage: boolean = false;

  private skeletonTimer: number;
  private readonly ANIMATION_TIME: number = 800; // animation delay 600 + 200 animation duration
  private readonly LONG_ANIMATION_TIME: number = 1000; // animation delay 800 + 200 animation duration

  constructor(
    private device: DeviceService,
    private cmsService: CmsService,
    private windowRefService: WindowRefService,
    private changeDetectorRef: ChangeDetectorRef,
    private pubsub: PubSubService,
    protected routingState: RoutingState
  ) { }

  ngOnInit(): void {
    this.isTablet = this.device.isTablet;
    this.numberOfElements = 11;
    this.numberOfSurfaceBets = 2;
    this.numberOfPricesOrLines = 3;
    this.numberOfGenericElements = this.isTablet ? 6 : 3;
    this.cmsService.getSystemConfig().subscribe((config: ISystemConfig) => {
      this.skeletonFeatureEnabled = config.FeatureToggle && config.FeatureToggle.skeletonLoadingScreen;
      this.initialized = true;
    });
    this.isHome = this.routingState.getCurrentUrl() === '/';
  }

  /**
   * Remove skeleton from DOM after animation finished
   * @param changes
   */
  ngOnChanges(changes: SimpleChanges): void {
    if ((this.initialized && !this.skeletonFeatureEnabled) || this.onlySpinner || (!changes.displayed && !changes.skeletonOnlyDisplayed)) {
      return;
    }
    const displayedValue = (changes.displayed && changes.displayed.currentValue) || this.displayed,
      skeletonOnlyDisplayedValue = (changes.skeletonOnlyDisplayed && changes.skeletonOnlyDisplayed.currentValue)
        || this.skeletonOnlyDisplayed,
      displaySkeleton = displayedValue || skeletonOnlyDisplayedValue;
    if (!displaySkeleton) {
      this.skeletonTimer = this.windowRefService.nativeWindow.setTimeout(() => {
        this.hide = true;
        this.changeDetectorRef.markForCheck();
      }, this.longRenderView ? this.LONG_ANIMATION_TIME : this.ANIMATION_TIME);
      this.publishPerformanceMark();
    } else {
      this.windowRefService.nativeWindow.clearTimeout(this.skeletonTimer);
      this.hide = false;
    }
  }
  publishPerformanceMark(): void {
    if (this.routingState.getCurrentSegment() !== 'home') {
      this.pubsub.publish(this.pubsub.API.PERFORMANCE_MARK);
    }
  }
}

