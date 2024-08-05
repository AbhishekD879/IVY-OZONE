import { Component, Input, OnChanges, OnDestroy } from '@angular/core';
import { NETWORK_CONSTANTS } from './network-indicator.constants';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { GtmService } from 'app/core/services/gtm/gtm.service';
import { NIConfig } from './network-indicator.model';
import { DialogService } from '@core/services/dialogService/dialog.service';
import { ConnectionInterruptionDialogComponent } from '@app/shared/components/connection-interruption-dialog/connection-interruption-dialog.component';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import environment from '@environment/oxygenEnvConfig';
import { NETWORK_CONSTANTS_CORE } from './network-indicator-core.constants';

@Component({
  selector: 'network-indicator',
  templateUrl: './network-indicator.component.html',
  styleUrls: ['./network-indicator.component.scss']
})
export class NetworkIndicatorComponent implements OnChanges, OnDestroy {
  @Input() config: NIConfig;
  indicatorConfig: NIConfig = new NIConfig();
  display: boolean;
  isSlowEverCalled = false;
  private previousState: string = NETWORK_CONSTANTS.GA_TAGS.ONLINE;
  private isCoral = environment.brand === 'bma';
  private subscriber = 'NetworkIndicatorComponent';
  private timeout: number;

  constructor(private windowRef: WindowRefService,
    private dialogService: DialogService,
    private gtmService: GtmService,
    private pubSubService: PubSubService
  ) { }

  ngOnChanges(): void {
    this.styleIndicatorOnType(this.config);
  }

  ngOnDestroy(): void {
    this.pubSubService.unsubscribe(this.subscriber);
  }

  /**
   * Changes the indicator styles based on input network config
   * @param  {NIConfig} config
   */
  styleIndicatorOnType(config: NIConfig): void {
    if (config) {
      if (config.networkSpeed === NETWORK_CONSTANTS_CORE.SLOW) {
        this.windowRef.nativeWindow.clearTimeout(this.timeout);
        this.setIndicatorProperties(true, true, NETWORK_CONSTANTS_CORE.COLORS[environment.brand].SLOW_COLOR, NETWORK_CONSTANTS_CORE.ICONS[environment.brand].SLOW_ICON, NETWORK_CONSTANTS.GA_TAGS.CONNECTION_INTERRUPTED);
        this.pushToGTMService(NETWORK_CONSTANTS.GA_TAGS.CONTENT_VIEW, NETWORK_CONSTANTS.GA_TAGS.LOAD, NETWORK_CONSTANTS.GA_TAGS.BOTTOM, NETWORK_CONSTANTS.GA_TAGS.NA, NETWORK_CONSTANTS.GA_TAGS.CONNECTION_INTERRUPTED);
        this.pushPreviousStateGTM(this.previousState, NETWORK_CONSTANTS.GA_TAGS.CONNECTION_INTERRUPTED);
        this.pubSubService.publish(NETWORK_CONSTANTS_CORE.NW_INDICATOR_DISPLAY, true);
      } else if (config.networkSpeed === NETWORK_CONSTANTS_CORE.ONLINE && this.isSlowEverCalled) {
        this.setIndicatorProperties(false, true, NETWORK_CONSTANTS_CORE.COLORS[environment.brand].ONLINE_COLOR, NETWORK_CONSTANTS_CORE.ICONS[environment.brand].ONLINE_ICON, NETWORK_CONSTANTS.GA_TAGS.ONLINE);
        this.timeout = this.windowRef.nativeWindow.setTimeout(() => {
          this.display = false;
          this.pubSubService.publish(NETWORK_CONSTANTS_CORE.NW_INDICATOR_DISPLAY, false);
        }, config.timeout ? config.timeout : 5000);
        this.pushToGTMService(NETWORK_CONSTANTS.GA_TAGS.CONTENT_VIEW, NETWORK_CONSTANTS.GA_TAGS.LOAD, NETWORK_CONSTANTS.GA_TAGS.BOTTOM, NETWORK_CONSTANTS.GA_TAGS.NA, NETWORK_CONSTANTS.GA_TAGS.ONLINE);
        this.pushPreviousStateGTM(this.previousState, NETWORK_CONSTANTS.GA_TAGS.ONLINE);
        this.pubSubService.publish(NETWORK_CONSTANTS_CORE.NW_INDICATOR_DISPLAY, true);
      } else if (config.networkSpeed === NETWORK_CONSTANTS.OFFLINE) {
        this.windowRef.nativeWindow.clearTimeout(this.timeout);
        this.setIndicatorProperties(true, true, NETWORK_CONSTANTS_CORE.COLORS[environment.brand].OFFLINE_COLOR, NETWORK_CONSTANTS_CORE.ICONS[environment.brand].OFFLINE_ICON, NETWORK_CONSTANTS.GA_TAGS.OFFLINE);
        this.pushToGTMService(NETWORK_CONSTANTS.GA_TAGS.CONTENT_VIEW, NETWORK_CONSTANTS.GA_TAGS.LOAD, NETWORK_CONSTANTS.GA_TAGS.BOTTOM, NETWORK_CONSTANTS.GA_TAGS.NA, NETWORK_CONSTANTS.GA_TAGS.OFFLINE);
        this.pushPreviousStateGTM(this.previousState, NETWORK_CONSTANTS.GA_TAGS.OFFLINE);
        this.pubSubService.publish(NETWORK_CONSTANTS_CORE.NW_INDICATOR_DISPLAY, true);
      }
    }
  }

  /**
   * To close the network indicator
   */
  onClose(): void {
    this.pushToGTMService(NETWORK_CONSTANTS.GA_TAGS.EVENT_TRACKING, NETWORK_CONSTANTS.GA_TAGS.CLOSE, NETWORK_CONSTANTS.GA_TAGS.BOTTOM, NETWORK_CONSTANTS.GA_TAGS.NA, this.previousState);
    this.display = false;
    this.pubSubService.publish(NETWORK_CONSTANTS_CORE.NW_INDICATOR_DISPLAY, false);
  }

  /**
   * To trigger popup on info icon click
   */
  onInfoIconClick(): void {
    this.pushToGTMService(NETWORK_CONSTANTS.GA_TAGS.CONTENT_VIEW, NETWORK_CONSTANTS.GA_TAGS.LOAD, NETWORK_CONSTANTS.GA_TAGS.NA, NETWORK_CONSTANTS.GA_TAGS.INTERRUPTED_POPUP, NETWORK_CONSTANTS.GA_TAGS.INTERRUPTED_POPUP);
    this.pushToGTMService(NETWORK_CONSTANTS.GA_TAGS.EVENT_TRACKING, NETWORK_CONSTANTS.GA_TAGS.CLICK, NETWORK_CONSTANTS.GA_TAGS.NA, NETWORK_CONSTANTS.GA_TAGS.INTERRUPTED_POPUP, NETWORK_CONSTANTS.GA_TAGS.INFO_ICON);
    this.dialogService.openDialog(this.dialogService.ids.connectionInterrupted, ConnectionInterruptionDialogComponent, true, { header: this.config.displayText, message: this.config.infoMsg });
  }

  /**
   * Adds GA tracking for previous and current network state
   * @param  {string} previousState
   * @param  {string} currentState
   * @returns void
   */
  private pushPreviousStateGTM(previousState: string, currentState: string): void {
    if (previousState !== currentState) {
      this.pushToGTMService(NETWORK_CONSTANTS.GA_TAGS.CONTENT_VIEW, NETWORK_CONSTANTS.GA_TAGS.LOAD, NETWORK_CONSTANTS.GA_TAGS.BOTTOM, NETWORK_CONSTANTS.GA_TAGS.NA, `${previousState} to ${currentState}`);
    }
  }

  /**
   * Pushes GA tracking tags to datalayer
   * @param  {string} event
   * @param  {string} actionEvent
   * @param  {string} positionEvent
   * @param  {string} locationEvent
   * @param  {string} eventDetails
   * @returns void
   */
  private pushToGTMService(event: string, actionEvent: string, positionEvent: string, locationEvent: string, eventDetails: string): void {
    this.gtmService.push(event, [{
      ...NETWORK_CONSTANTS.GA_STATIC_FIELDS,
      'component.ActionEvent': actionEvent,
      'component.PositionEvent': positionEvent,
      'component.LocationEvent': locationEvent,
      'component.EventDetails': eventDetails
    }]);
  }

  /**
   * Set common Indicator Properties
   * @param  {boolean} isSlowEverCalled
   * @param  {boolean} display
   * @param  {string} indicatorColor
   * @returns string
   */
  private setIndicatorProperties(isSlowEverCalled: boolean, display: boolean, indicatorColor: string, displayIcon: string, previousState: string): void {
    this.isSlowEverCalled = isSlowEverCalled;
    this.display = display;
    this.indicatorConfig.indicatorColor = indicatorColor;
    this.indicatorConfig.displayIcon = displayIcon;
    this.previousState = previousState;
  }
}
