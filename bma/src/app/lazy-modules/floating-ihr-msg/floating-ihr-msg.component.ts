import { Component, Input, OnChanges, OnDestroy, OnInit, SimpleChanges } from "@angular/core";
import { CmsService } from '@coreModule/services/cms/cms.service';
import { ISystemConfig } from '@core/services/cms/models';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { ISportEvent } from "@core/models/sport-event.model";
import environment from '@environment/oxygenEnvConfig';
import { LocaleService } from '@core/services/locale/locale.service';
import { bma } from '@app/lazy-modules/locale/translations/en-US/bma.lang';
import { IDelta } from "@core/models/delta-object.model";
import { GtmService } from "@app/core/services/gtm/gtm.service";

@Component({
    selector: 'floating-ihr-msg',
    styleUrls: ['./floating-ihr-msg.component.scss'],
    templateUrl: './floating-ihr-msg.component.html'
})
export class FloatingIhrMsgComponent implements OnInit, OnChanges, OnDestroy {
    @Input() racingInMeeting: ISportEvent[];
    @Input() eventId: number;

    eventEntity: ISportEvent;
    showFloatingInplayMsg: boolean = false;
    closeFloatingMsg: boolean = true;
    eventStatusCode: string = 'A';
    isInplay: boolean = false;
    floatingMsgText: string = '';
    isBrandLadbrokes: boolean;
    protected BIRMarketsEnabled: string[] = [];
    private readonly tagName: string = 'FloatingIhrMsgComponent';

    constructor(private cmsService: CmsService,
        private pubSubService: PubSubService,
        private locale: LocaleService,
        private gtmService: GtmService) { }

    ngOnChanges(changes: SimpleChanges): void {
        if ((changes.eventId || changes.racingInMeeting) && this.floatingMsgText) {
            this.assignEventEntity();
            if (this.eventEntity)
                this.checkToShowFloatingMsg();
        }
    }

    ngOnInit(): void {
        this.isBrandLadbrokes = environment.brand === this.locale.getString(bma.brands.ladbrokes).toLowerCase();

        this.cmsService.getSystemConfig().subscribe((config: ISystemConfig) => {
            this.floatingMsgText = config?.HorseRacingBIR?.floatingMsgEnabled;
            this.BIRMarketsEnabled = config?.HorseRacingBIR?.marketsEnabled;
        });
        this.assignEventEntity();

        if (this.floatingMsgText) {
            this.pubSubService.subscribe(this.tagName, this.pubSubService.API.EXTRA_PLACE_RACE_OFF, (updateEventId: string) => {
                if (updateEventId && this.eventEntity && this.eventEntity.id.toString() === updateEventId.toString()) {
                    this.showFloatingInplayMsg = true;
                    this.isInplay = true;
                }
            });

            this.pubSubService.subscribe(this.tagName, this.pubSubService.API.SUSPEND_IHR_EVENT_OR_MRKT, (updateEventId: string, delta: IDelta) => {
                if (this.isInplay && updateEventId && this.eventEntity && this.eventEntity.id.toString() === updateEventId.toString()) {
                    if(delta.eventStatusCode === 'A' || delta.eventStatusCode === 'S') {
                        this.eventStatusCode = delta.eventStatusCode;
                    }
                    let isMarketSuspended = false;
                    this.eventEntity.markets.forEach(market => {
                        if (market.marketStatusCode === 'S' && this.isBirMarketEnabled(market.name))
                            isMarketSuspended = true;
                    });
                    if ((this.eventStatusCode === 'S' || this.eventEntity.eventStatusCode === 'S') 
                    || ((delta.marketStatusCode === 'S' && this.isBirMarketEnabled(delta.originalName)) || isMarketSuspended)) {
                        this.showFloatingInplayMsg = false;
                    } else if (this.eventStatusCode === 'A' && !isMarketSuspended) {
                        this.showFloatingInplayMsg = true;
                    }
                }
            });

            if (this.eventEntity)
                this.checkToShowFloatingMsg();
        }
    }

    /**
     * assigns event entity from racingInMeeting.
     * @return - void
     */
    assignEventEntity(): void {
        this.eventEntity = this.racingInMeeting.find((eventEntity: ISportEvent) => eventEntity.id.toString() === this.eventId.toString());
    }

    /**
     * checks whether to show the floating message.
     * @return - void
     */
    checkToShowFloatingMsg(): void {
        let isMarketSuspended = false;
        this.eventEntity.markets.forEach(market => {
            if (market.marketStatusCode === 'S' && this.isBirMarketEnabled(market.name))
                isMarketSuspended = true;
        });
        if (this.eventEntity.rawIsOffCode === 'Y') {
            this.isInplay = true;
            if (this.eventEntity.eventStatusCode !== 'S' && !isMarketSuspended) {
                this.showFloatingInplayMsg = true;
            }
        } else {
            this.showFloatingInplayMsg = false;
            this.isInplay = false;
        }
    }

    ngOnDestroy(): void {
        this.pubSubService.unsubscribe(this.tagName);
    }
    /**
     * closes the floatingInplayMsg
     */
    closeFloatingInplayMsg(): void {
        this.showFloatingInplayMsg = false;
        this.closeFloatingMsg = false;
        this.eventEntity && this.gtmService.push('trackEvent', {
            eventAction: "race card",
            eventCategory: "horse racing",
            eventLabel: "close - in-play betting",
            categoryID: this.eventEntity.categoryId,
            typeID: this.eventEntity.typeId,
            eventID: this.eventEntity.id,
        });
    }
    /**
     * Checks if market is enabled in CMS for BIR
     * @param {string} marketName
     * @returns {boolean}
     */
    private isBirMarketEnabled(marketName: string = ''): boolean {
        return this.BIRMarketsEnabled?.some((market: string) => marketName.toLocaleLowerCase() === market.toLocaleLowerCase());
    }
}