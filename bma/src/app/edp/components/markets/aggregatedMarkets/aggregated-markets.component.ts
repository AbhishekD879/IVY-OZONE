import { Component, Input, ChangeDetectorRef, OnChanges } from '@angular/core';
import { ReplaySubject } from 'rxjs';
import * as _ from 'underscore';
import { AccordionComponent } from '@shared/components/accordion/accordion.component';
import { AccordionService } from '@shared/components/accordion/accordion.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { SportEventPageService } from '@edp/services/sportEventPage/sport-event-page.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { IMarket } from '@core/models/market.model';
import { IOutcome } from '@core/models/outcome.model';
import { IMarketLinks } from '@core/services/cms/models/edp-market.model';
import { EventService } from '@app/sb/services/event/event.service';
import { IMarketTemplate } from '@core/models/market.model';
import { TemplateService } from '@shared/services/template/template.service';
import { CacheEventsService } from '@core/services/cacheEvents/cache-events.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { MARKET_VIEWTYPE, MARKET_MINOR_CODE, OUTCOME_NAME } from '@edp/models/market-constants';

@Component({
    selector: 'aggregated-markets',
    templateUrl: 'aggregated-markets.component.html',
    styleUrls: ['aggregated-markets.component.scss']
})
export class AggregatedMarketsComponent extends AccordionComponent implements OnChanges {
    @Input() event: ISportEvent;
    @Input() templateMarketGroup: IMarketTemplate;
    @Input() marketGroup?: IMarket[];
    @Input() index: number;

    public replaySubj: ReplaySubject<IMarketLinks[]> = new ReplaySubject(1);
    eventEntity: any;
    markets: IMarket[];
    listMarketTabs: any[];
    activeMarket: number = 0;
    showAll: boolean = false;
    limitCount: number = 0;
    updatedMarket: IMarket;
    private selectedCount: number = 8;
    private isOnceExpanded: boolean = false;
    private AGGREGATED_MARKETS: string = 'aggregatedMarkets';
    private UPDATE_OUTCOMES_FOR_MARKET: string = 'UPDATE_OUTCOMES_FOR_MARKET';

    constructor(
        protected accordionService: AccordionService,
        protected gtm: GtmService,
        protected changeDetectorRef: ChangeDetectorRef,
        protected pubsub: PubSubService,
        private eventService: EventService,
        private sportEventPageService: SportEventPageService,
        private templateService: TemplateService,
        private cacheEventService: CacheEventsService,
        private filtersService: FiltersService) {
        super(accordionService, gtm, changeDetectorRef, pubsub);
    }
    ngOnInit() {
        super.ngOnInit();
        this.pubsub.subscribe(this.AGGREGATED_MARKETS, this.UPDATE_OUTCOMES_FOR_MARKET, market => {
            this.updatedMarket = market;
            this.updateMarket();
            this.changeDetectorRef.detectChanges();
        });
    }

    ngOnDestroy(): void {
        this.pubsub.unsubscribe(this.AGGREGATED_MARKETS);
    }
    toggled(event: MouseEvent) {
        /* disable accordion functionality */
        if (this.disabled) {
            return;
        }
        
        this.setState(!this.isExpanded);
        this.trackToggle();
        
        if (this.func) {
            this.func.emit(this.isExpanded);
        }
        event.preventDefault();
        event.stopPropagation();
        this.changeDetectorRef.detectChanges();
    }

    ngOnChanges() {
        if(this.isExpanded){
            this.fetchOutcomesForTemplateMarket();
        }
    }
    
    private fetchOutcomesForTemplateMarket(): void {
        let marketIds = [];
        if(this.isOnceExpanded){
            _.each(this.templateMarketGroup.marketIds, marketId => {
                if(!this.isOutcomeDataAvailable(marketId)){
                    marketIds.push(marketId);
                }
            });
        } else {
            marketIds = this.templateMarketGroup.marketIds;
        }
        if(marketIds.length){
            this.eventService.getEvent(this.event.id, {}, false, true, true, marketIds)
                .then(() => {
                    this.isOnceExpanded = true;
                    this.init();
                });
        } else {
            this.init();
        }
    }

    private init(): void {
        this.eventEntity = this.cacheEventService.storedData.event.data ? this.cacheEventService.storedData.event.data[0] : {};
        this.markets = this.eventEntity?.markets?.filter((market: IMarket) => this.templateMarketGroup.marketIds.includes(market.id));
        this.sortOutcomes(this.markets);
        this.processYourcallMarkets();
        this.sortMarkets();
        this.sportEventPageService.transformMarkets(this.markets);
        this.changeDetectorRef.detectChanges();
    }

    private updateMarket(){
        this.sortOutcomes([this.updatedMarket]);
    }

    private isOutcomeDataAvailable(marketId: number|string) : boolean{
        const market = this.cacheEventService.storedData.event.data[0].markets
                .filter(m => m.id === marketId);
        return market && market.length>0 && market[0].outcomes?.length > 0 ? true : false;
    }

    private sortMarkets(): void {
        this.markets = _.chain(this.markets)
            .sortBy(data => {
                return data.name.toLowerCase();
            })
            .sortBy('displayOrder')
            .value();
        this.markets = _.filter(this.markets, market => !market.hidden && market.outcomes && market.outcomes.length > 0);
    }

    private sortOutcomes(markets: IMarket[]): void {
        _.each(markets, market => {
            market.viewType = this.templateService.getMarketViewType(market);
            if (market.outcomes && market.outcomes.length > 0) {
                const marketsForSortingOutcomes = market.rawHandicapValue ? null : this.markets;
                market.outcomes = this.templateService.getMarketWithSortedOutcomes(market, marketsForSortingOutcomes);
                // Push Fake outcome if outcome is empty
                this.addFakeOutcome(market);
            }
        });
    }

    private addFakeOutcome(market: IMarket): void {
        const outcomeLength = this.getActualOutcomeLength(market)
        if (market.outcomes.length < outcomeLength) {
            let fakeOutcome: any = [];
            const getValue = value => ({ outcomeMeaningMinorCode: value });
            const minorCodeArray = market.marketMeaningMinorCode === MARKET_MINOR_CODE.HL ? [1, 3] :
                outcomeLength === 2 ? [1, 3] : [1, 2, 3];
            _.each(minorCodeArray, (id) => {
                if (!_.findWhere(market.outcomes, getValue(id)) && market.outcomes.length < outcomeLength) {
                    fakeOutcome = {
                        fakeOutcome: true,
                        name: this.getOutcomeHeader(id, market),
                        outcomeMeaningMinorCode: id,
                        outcomeMeaningMajorCode: market.outcomes[0].outcomeMeaningMajorCode,
                        prices: market.outcomes[0].prices,
                    };
                    market.outcomes.push(fakeOutcome);
                }
            });
            market.outcomes = _.sortBy(market.outcomes, 'outcomeMeaningMinorCode');
            if(market.marketMeaningMinorCode === MARKET_MINOR_CODE.MH){
                market.groupedOutcomes = _.toArray(this.filtersService.groupBy(market.outcomes, 'outcomeMeaningMinorCode'));
                market.groupedOutcomes = _.filter(market.groupedOutcomes, outcomes => !_.isEmpty(outcomes));
            }
        }
    }

    private getActualOutcomeLength(market: IMarket): number {
        return (market.marketMeaningMinorCode === MARKET_MINOR_CODE.HL || market.marketMeaningMinorCode === MARKET_MINOR_CODE.WH) ? 2 
            : market.marketMeaningMinorCode === MARKET_MINOR_CODE.MH ? 3 : market.outcomes.length;
    }

    private getOutcomeHeader(id: number, market: IMarket): string {
        const outcomeHeaders = {};
        if(market.marketMeaningMinorCode === MARKET_MINOR_CODE.HL){
            outcomeHeaders[1] = OUTCOME_NAME.OVER;
            outcomeHeaders[3] = OUTCOME_NAME.UNDER;
        }
        const names = this.event.name.includes(' v ') ? this.event.name.split(' v ') : this.event.name.split(' vs ');
        if(market.marketMeaningMinorCode === MARKET_MINOR_CODE.MH || market.marketMeaningMinorCode === MARKET_MINOR_CODE.WH){
            outcomeHeaders[1] = names[0];
            outcomeHeaders[3] = names[1];
            outcomeHeaders[2] = OUTCOME_NAME.TIE;
        }
        return outcomeHeaders[id];
    }

    private processYourcallMarkets(): void {
        _.each(this.markets, marketEntity => {
            if (this.isYourCallMarket(marketEntity) && marketEntity.outcomes && marketEntity.outcomes.length > 0) {
                marketEntity.outcomes = this.templateService.sortOutcomesByPriceAndDisplayOrder(marketEntity.outcomes);  
            }
        });
    }

    private isYourCallMarket(market: IMarket): boolean {
        const yourCallMarketPattern = /(YourCall)/i;
        return !!(market.templateMarketName && market.templateMarketName.match(yourCallMarketPattern));
    }

    getTrackById(index: number, entity: any) {
        return `${entity.id}_${index}`;
    }

    /**
     * Toggle Button for Show All
     */
    toggleShowAll(): void {
        this.showAll = !this.showAll;
        this.changeDetectorRef.detectChanges();
    }

    selectedMarkets(markets: IMarket[]) {
        return this.showAll ? markets : markets.slice(0, this.selectedCount);
    }

    get showLessButton(): boolean {
        return this.markets.length > this.selectedCount;
    }

    getOutcomeNames(): string[] {
        const outcomeNames = [];
        this.markets[0].outcomes.forEach((outcome: IOutcome) => {
            outcomeNames.push(outcome.name.includes('(') ? outcome.name.split('(')[0].trim() : outcome.name);
        });
        return outcomeNames;
    }

    isAccordionExpanded(): boolean {
        return (this.markets[0].viewType === MARKET_VIEWTYPE.CORRECT_SCORE || this.markets[0].viewType === MARKET_VIEWTYPE.SCORER) && this.index <=1
    }
}