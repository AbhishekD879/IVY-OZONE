import { Injectable } from '@angular/core';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { NETWORK_CONSTANTS } from '@app/lazy-modules/networkIndicator/components/network-indicator/network-indicator.constants';
import { RendererService } from '@shared/services/renderer/renderer.service';
import environment from '@environment/oxygenEnvConfig';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';

@Injectable()
export class InitNetworkIndicatorService {
    title = 'networkIndicatorService';

    constructor(
        protected pubSubService: PubSubService,
        protected rendererService: RendererService,
        protected windowRef: WindowRefService
    ) { }

    /**
     * Init subscriptions
     * @returns void
     */
    init(): void {
        this.subscribeToNetworkIndicatorEvents();
    }

    /**
     * Subscriptions for Network Connection indicator alignment on different screens
     * @returns void
     */
    private subscribeToNetworkIndicatorEvents(): void {
        this.pubSubService.subscribe(this.title, this.pubSubService.API['show-slide-out-betslip-true'], () => {
            if (this.getNetworkIndicatorEl()) {
                this.rendererService.renderer.addClass(this.getNetworkIndicatorEl(), NETWORK_CONSTANTS.BETSLIP_SHOWN);
            }
        });

        this.pubSubService.subscribe(this.title, this.pubSubService.API['show-slide-out-betslip-false'], () => {
            if (this.getNetworkIndicatorEl()) {
                this.rendererService.renderer.removeClass(this.getNetworkIndicatorEl(), NETWORK_CONSTANTS.BETSLIP_SHOWN);
            }
        });

        this.pubSubService.subscribe(this.title, this.pubSubService.API.QUICKBET_OPENED, () => {
            if (this.getNetworkIndicatorEl()) {
                this.rendererService.renderer.addClass(this.getNetworkIndicatorEl(), NETWORK_CONSTANTS.QUICKBET_SHOWN);
            }
        });

        this.pubSubService.subscribe(this.title, this.pubSubService.API.QUICKBET_PANEL_CLOSE, () => {
            if (this.getNetworkIndicatorEl()) {
                this.rendererService.renderer.removeClass(this.getNetworkIndicatorEl(), NETWORK_CONSTANTS.QUICKBET_SHOWN);
            }
        });

        this.pubSubService.subscribe(this.title, NETWORK_CONSTANTS.NETWORK_INDICATOR_BOTTOM, (displayStatus: boolean) => {
            if (this.getNetworkIndicatorEl()) {
                if (displayStatus) {
                    this.rendererService.renderer.addClass(this.getNetworkIndicatorEl(), NETWORK_CONSTANTS.INDICATOR_BOTTOM);
                } else {
                    this.rendererService.renderer.removeClass(this.getNetworkIndicatorEl(), NETWORK_CONSTANTS.INDICATOR_BOTTOM);
                }
            }
        });
        this.pubSubService.subscribe(this.title, NETWORK_CONSTANTS.NETWORK_INDICATOR_BOTTOM_INDEX, (displayStatus: boolean) => {
            if (this.getNetworkIndicatorEl()) {
                if (displayStatus) {
                    this.rendererService.renderer.addClass(this.getNetworkIndicatorEl(), NETWORK_CONSTANTS.INDICATOR_BOTTOM_INDEX);
                } else {
                    this.rendererService.renderer.removeClass(this.getNetworkIndicatorEl(), NETWORK_CONSTANTS.INDICATOR_BOTTOM_INDEX);
                }
            }
        });
        this.pubSubService.subscribe(this.title, NETWORK_CONSTANTS.NETWORK_INDICATOR_INDEX_HIDE, (displayStatus: boolean) => {
            if (this.getNetworkIndicatorEl()) {
                if (displayStatus) {
                    this.rendererService.renderer.addClass(this.getNetworkIndicatorEl(), NETWORK_CONSTANTS.INDICATOR_INDEX_HIDE);
                } else {
                    this.rendererService.renderer.removeClass(this.getNetworkIndicatorEl(), NETWORK_CONSTANTS.INDICATOR_INDEX_HIDE);
                }
            }
        });
    }

    /**
     * Returns Network Indicator HTML element
     * @returns Element
     */
    private getNetworkIndicatorEl(): Element | null {
        const element = this.windowRef.document.querySelector(environment.brand === 'bma' ? NETWORK_CONSTANTS.NW_INDICATOR_CLASS_CORAL : NETWORK_CONSTANTS.NW_INDICATOR_CLASS_LADS);
        return element ? element : null;
    }
}
