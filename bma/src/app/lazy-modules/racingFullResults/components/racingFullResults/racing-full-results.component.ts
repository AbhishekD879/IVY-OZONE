import { Component, OnInit, Input } from '@angular/core';

import { IRacingEvent } from '@core/models/racing-event.model';
import { IOutcome } from '@core/models/outcome.model';
import { IRaceGHResultsRunnersData, IRacingPostGHResponse } from '@app/core/services/racing/racingPost/racing-post.model';
import environment from '@environment/oxygenEnvConfig';
import { RACING_FULL_RESULTS_CONSTANTS } from '@lazy-modules/racingFullResults/racing-full-results.constants';

@Component({
    selector: 'racing-full-results',
    templateUrl: 'racing-full-results.component.html',
    styleUrls: ['./racing-full-results.component.scss'],
})

export class RacingFullResultsComponent implements OnInit {
    @Input() eventEntity: IRacingEvent;
    @Input() greyhoundsFullResultsData: IRacingPostGHResponse;
    showRacingSignposting: boolean;
    fullResults: boolean = false;
    brand: string = environment.brand;

    ngOnInit(): void {
        this.showFullResultsOrAwaitingSignposting();
    }

    /**
     * decides to show full results or awaiting full results signposting
     */
    showFullResultsOrAwaitingSignposting() {
        const resultedEventData = this.greyhoundsFullResultsData.document[this.eventEntity.id.toString()];
        const contestGreyhounds = this.eventEntity.resultedWEWMarket.outcomes.length + this.eventEntity.resultedWEWMarket.unPlaced.length + this.eventEntity.resultedWEWMarket.outcomesWithoutPrices.length;
        const loseGreyhounds = this.eventEntity.resultedWEWMarket.unPlaced;
        const resultsDataCheck = resultedEventData?.hasOwnProperty(RACING_FULL_RESULTS_CONSTANTS.RESULTS);
        const runnersDataCheck = resultedEventData?.results?.hasOwnProperty(RACING_FULL_RESULTS_CONSTANTS.RUNNERS);
        const resultedRunners = resultsDataCheck && runnersDataCheck && resultedEventData.results.runners.filter((item: IRaceGHResultsRunnersData) => item.position != RACING_FULL_RESULTS_CONSTANTS.POSITION_NON_RUNNER);
        if (resultsDataCheck && runnersDataCheck && loseGreyhounds && contestGreyhounds === resultedRunners.length) {
            this.showRacingSignposting = true;
            this.mapResultPosition(this.eventEntity, resultedRunners);
        } else {
            this.showRacingSignposting = false;
            this.fullResults = true;
        }
    }

    /**
    * Map positions from one-api in outcome section
    */
    mapResultPosition(event: IRacingEvent, resultedGreyhoundData: IRaceGHResultsRunnersData[]) {
        const unplaced = event.resultedWEWMarket.unPlaced;
        const outcomesWithoutPrices = event.resultedWEWMarket.outcomesWithoutPrices;
        event.resultedWEWMarket.outcomes = event.resultedWEWMarket.outcomes.concat(unplaced, outcomesWithoutPrices);
        event.resultedWEWMarket.outcomes.forEach((greyhound: IOutcome) => {
            resultedGreyhoundData.forEach((item: IRaceGHResultsRunnersData) => {
                if (item.trapNumber == greyhound.runnerNumber) {
                    const position = item.position.replace(/[^0-9]/g, '');
                    greyhound.results.position = position;
                    greyhound.position = position;
                    if (item.position === RACING_FULL_RESULTS_CONSTANTS.POSITION_ZERO) {
                        greyhound.results.resultCode = item.raceOutcomeCode;
                        greyhound.resultCode = item.raceOutcomeCode;
                    }
                }
            });
        });

        event.resultedWEWMarket.outcomes.sort((a, b) => Number(a.position) - Number(b.position));
        let positions = [], withoutPositions = [];
        positions = event.resultedWEWMarket.outcomes.filter(position =>
            position.results.position !== RACING_FULL_RESULTS_CONSTANTS.POSITION_ZERO && position.results.position !== "");
        withoutPositions = event.resultedWEWMarket.outcomes.filter(position =>
            position.results.position === RACING_FULL_RESULTS_CONSTANTS.POSITION_ZERO || position.results.position === "");
        event.resultedWEWMarket.outcomes = positions.concat(withoutPositions);
        this.fullResults = true;
    }
}