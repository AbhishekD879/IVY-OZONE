import { ChangeDetectionStrategy, ChangeDetectorRef, Component, OnDestroy, OnInit,ViewEncapsulation } from '@angular/core';
import * as _ from 'underscore';

import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { IVisibleState } from '@shared/components/loadingOverlay/loading-overlay.model';
import { ApiVanillaService } from '@lazy-modules/serviceClosure/api-vanilla.service';

@Component({
  selector: 'loading-overlay',
  templateUrl: 'loading-overlay.component.html',
  styleUrls:['loading-overlay.component.scss'],
   encapsulation: ViewEncapsulation.None,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class LoadingOverlayComponent implements OnInit, OnDestroy {
  overlayVisible: boolean = false;
  spinnerVisible: boolean = false;
  readonly NAME: string = 'LoadingOverlay';
  isOverlayPlayBreakAdjusted: boolean = false;

  constructor(
    private pubsub: PubSubService,
    private changeDetectorRef: ChangeDetectorRef,
    public apiVanillaService: ApiVanillaService
  ) {
    this.toggleVisibleState = this.toggleVisibleState.bind(this);
  }

  ngOnInit(): void {
    this.pubsub.subscribe(this.NAME, this.pubsub.API.TOGGLE_LOADING_OVERLAY, this.toggleVisibleState);
    this.apiVanillaService.playBreakSubject.subscribe((playbreakUpdatedFlag: boolean) => {
      this.isOverlayPlayBreakAdjusted = playbreakUpdatedFlag;
      this.changeDetectorRef.detectChanges();
    });
  }

  ngOnDestroy(): void {
    this.pubsub.unsubscribe(this.NAME);
  }

  /**
   * Toggles visible state of overlay and spinner.
   * @param {boolean=} options.overlay
   * @param {boolean=} options.spinner
   * @private
   */
  private toggleVisibleState(option: IVisibleState) {
    this.overlayVisible = _.isUndefined(option.overlay) ? this.overlayVisible : option.overlay;
    this.spinnerVisible = _.isUndefined(option.spinner) ? this.spinnerVisible : option.spinner;
    this.changeDetectorRef.detectChanges();
  }
}

