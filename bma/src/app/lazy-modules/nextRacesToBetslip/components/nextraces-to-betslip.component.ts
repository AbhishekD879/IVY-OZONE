import { Component, ChangeDetectionStrategy, ChangeDetectorRef, OnInit, OnDestroy, EventEmitter, Output, Input, OnChanges, SimpleChanges } from '@angular/core';
import { ISportEvent } from '@app/core/models/sport-event.model';
import { Subscription } from 'rxjs';
import { RoutingHelperService } from '@app/core/services/routingHelper/routing-helper.service';
import { Router } from '@angular/router';
import { GtmService } from '@app/core/services/gtm/gtm.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { IBetDetail } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { IQuickbetSelectionModel } from '@app/core/models/quickbet-selection.model';
import { BetslipService } from '@app/betslip/services/betslip/betslip.service';
import environment from '@environment/oxygenEnvConfig';
import { INextRacesToBetslip } from '@app/core/services/cms/models/system-config';
import { LocaleService } from '@app/core/services/locale/locale.service';
import { NextRacesHomeService } from '@lazy-modules/lazyNextRacesTab/components/nextRacesHome/next-races-home.service';
import { STRATEGY_TYPES } from '@app/core/constants/strategy-types.constant';

@Component({
    selector: 'nextraces-to-betslip',
    templateUrl: 'nextraces-to-betslip.component.html',
    styleUrls: ['./nextraces-to-betslip.component.scss',
        '../../../racing/assets/styles/next-races.scss',
        '../../../../app/shared/components/raceCard/next-races-carousel.scss',
        '../../../shared/components/raceCard/race-card.component.scss'
    ],
    changeDetection: ChangeDetectionStrategy.OnPush,
})
export class NextRacesToBetslipComponent implements OnInit, OnDestroy, OnChanges {
    @Input() mainBetReceipts: IBetDetail[] = [];
    @Input() quickBetReceipt: IQuickbetSelectionModel;
    @Input() multiReceipts: IBetDetail[];
    @Input() racingPostData: ISportEvent[];
    @Output() readonly closeFn: EventEmitter<boolean> = new EventEmitter();

    nextRaceData: ISportEvent[] = [];
    upCellSubscription: Subscription;
    raceOrigin: string = '?origin=next-races';
    betData = [];
    changeStrategy = STRATEGY_TYPES.ON_PUSH;
    private isBetPlacedOnHR: boolean = false;
    private readonly BET_PLACED_ON_HR = environment.HORSE_RACING_CATEGORY_ID;
    constructor(
        private changeDetectorRef: ChangeDetectorRef,
        private routingHelperService: RoutingHelperService,
        private router: Router,
        private gtmService: GtmService,
        private pubSubService: PubSubService,
        private betSlipService: BetslipService,
        private locale: LocaleService,
        private nextRacesHomeService: NextRacesHomeService,
    ) { }

    ngOnInit(): void {
        this.pubSubService.subscribe('isTipPresent', this.pubSubService.API.IS_TIP_PRESENT, (nextRaces: INextRacesToBetslip) => {
            if (!nextRaces.isTipPresent) {
                this.getNextRaces(nextRaces.raceData);
            }
        });
        this.betData = this.betSlipService.betData;
    }

    ngOnChanges(changes: SimpleChanges): void {
        if(this.racingPostData && changes?.isNextRacesData?.currentValue) {
            this.getNextRaces(this.racingPostData);
        }
    }

    formEdpUrl(eventEntity: ISportEvent): string {
        return `${this.routingHelperService.formEdpUrl(eventEntity)}${this.raceOrigin}`;
    }

    trackByEvents(index: number, event: ISportEvent): string {
        return `${index}_${event.id}_${event.name}_${event.categoryId}`;
    }

    trackEvent(entity: ISportEvent): void {
        const link = this.formEdpUrl(entity);

        this.gtmService.push('trackEvent', {
            eventCategory: 'bet receipt',
            eventAction: 'navigation',
            eventLabel: 'next races'
        });
        this.closeFn.emit(true);
        this.router.navigateByUrl(link);
    }

    ngOnDestroy(): void {
        this.upCellSubscription && this.upCellSubscription.unsubscribe();
        this.pubSubService.unsubscribe('isTipPresent');
    }

    getGoing(going: string): string {
        return this.nextRacesHomeService.getGoing(going);
    }

    getRaceType(raceType: string): string {
        const KEY_NOT_FOUND = 'KEY_NOT_FOUND';
        let stage = this.locale.getString(`racing.raceType.${raceType}`);

        if (stage === KEY_NOT_FOUND) {
            stage = '';
        }

        return stage;
    }

    getDistance(distance: string): string {
    return this.nextRacesHomeService.getDistance(distance.toString());
    }

    private getNextRaces(isNextRaces: ISportEvent[]): void {
     if(!this.nextRaceData.length) {
        this.checkForBetsData(this.betData);
        if (((this.multiReceipts && !this.multiReceipts.length && this.mainBetReceipts.length === 1)
            || Object.keys(this.quickBetReceipt).length) && this.isBetPlacedOnHR) {
            this.nextRaceData = isNextRaces || this.racingPostData;
            const nextRaces = this.nextRaceData.map((race) => {
                const [time, ...name] = race.name.split(' ');
                race.localTime = time;
                race.name = name.join(' ');
                return race;
            });
            this.nextRaceData = nextRaces;
            this.trackForNextRaces();
            this.changeDetectorRef.markForCheck();
        }
    }
    }

    private trackForNextRaces() {
        this.gtmService.push('trackEvent', {
            eventCategory: 'bet receipt',
            eventAction: 'rendered',
            eventLabel: 'next races'
        });
    }

    /**
     * To Check bet placed on HR or not
     * @param {} betsData
     */
    private checkForBetsData(betPlacedOnHR): void {
        if (betPlacedOnHR.length) {
            betPlacedOnHR.forEach(betsData => {
                    this.checkForBetType(betsData);
            });
        } else {
            this.isBetPlacedOnHR = true;
        }
    }

    /**
     * To Check bet placed on HR tricast and forecast
     * @param {} betsData
     */
    private checkForBetType(betData): void {
        if (betData.combiType === 'TRICAST') {
            this.isBetPlacedOnHR = false;
        } else if (betData.combiType === 'FORECAST') {
            this.isBetPlacedOnHR = false;
        } else {
          this.isBetPlacedOnHR = true;
        }
    }
}
