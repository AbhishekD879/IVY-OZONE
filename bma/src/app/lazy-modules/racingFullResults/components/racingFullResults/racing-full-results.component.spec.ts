import { RacingFullResultsComponent } from '@lazy-modules/racingFullResults/components/racingFullResults/racing-full-results.component';
import { greyhoundFullResultsData } from '@lazy-modules/racingFullResults/components/racingFullResults/mocks/greyhound-full-results-data.mock';

describe('RacingFullResultsComponent ', () => {
    let component: RacingFullResultsComponent;

    const mockEvent = {
        "id": 2516472,
        "name": "Romford",
        "eventStatusCode": "S",
        "isDisplayed": "true",
        "isStarted": "true",
        "isResulted": "true",
        "isFinished": "true",
        "classId": 198,
        "categoryId": "19",
        "categoryCode": "GREYHOUNDS",
        "categoryName": "Greyhound Racing",
        "className": "Greyhounds - Live",
        "resultedWEWMarket": {
            "id": "141538793",
            "eventId": "2516472",
            "templateMarketId": "137072",
            "isDisplayed": "true",
            "name": "|Win or Each Way|",
            "isResulted": "true",
            "isFinished": "true",
            "outcomes": [
                {
                    "id": "1254885838",
                    "marketId": "141538793",
                    "isDisplayed": "true",
                    "name": "|Playtime Girl|",
                    "runnerNumber": "3",
                    "resultCode": "W",
                    "isResulted": "true",
                    "position": "1",
                    "isFinished": "true",
                    "results": {
                        "position": "1",
                        "resultCode": "W"
                    }
                }
            ],
            "outcomesWithoutPrices": [],
            "hasPositions": true,
            "terms": "Each Way: 1/4 odds - places 1-2",
            "nonRunners": [

            ],
            "unPlaced": [
                {
                    "id": "1254885835",
                    "marketId": "141538793",
                    "isDisplayed": "true",
                    "name": "|Kingdom Ten|",
                    "runnerNumber": "1",
                    "resultCode": "L",
                    "isResulted": "true",
                    "position": "2",
                    "isFinished": "true",
                    "results": {
                        "position": "2",
                        "resultCode": "L"
                    }
                },
                {
                    "id": "1254885829",
                    "marketId": "141538793",
                    "isDisplayed": "true",
                    "name": "|Glengar Belle|",
                    "runnerNumber": "6",
                    "resultCode": "L",
                    "isResulted": "true",
                    "position": "3",
                    "isFinished": "true",
                    "results": {
                        "position": "3",
                        "resultCode": "L"
                    }
                },
                {
                    "id": "1254885832",
                    "marketId": "141538793",
                    "isDisplayed": "true",
                    "name": "|Highway Sky|",
                    "runnerNumber": "5",
                    "resultCode": "L",
                    "isResulted": "true",
                    "isFinished": "true",
                    "results": {
                        "resultCode": "L"
                    }
                },
                {
                    "id": "1254885826",
                    "marketId": "141538793",
                    "isDisplayed": "true",
                    "name": "|Four Candles|",
                    "runnerNumber": "2",
                    "resultCode": "L",
                    "isResulted": "true",
                    "isFinished": "true",
                    "results": {
                        "resultCode": "L"
                    }
                },
                {
                    "id": "1254885824",
                    "marketId": "141538793",
                    "isDisplayed": "true",
                    "name": "|Bit View Rocky|",
                    "runnerNumber": "4",
                    "resultCode": "L",
                    "isResulted": "true",
                    "isFinished": "true",
                    "results": {
                        "resultCode": "L"
                    }
                }
            ]
        }
    } as any;

    beforeEach(() => {
        component = new RacingFullResultsComponent();
        component.eventEntity = mockEvent;
        component.greyhoundsFullResultsData = greyhoundFullResultsData as any;
    });

    describe('#ngOnInit', () => {
        it('should invoke getFullGreyhoundsResults on init', () => {
            spyOn(component, 'showFullResultsOrAwaitingSignposting');
            component.ngOnInit();
            expect(component.showFullResultsOrAwaitingSignposting).toHaveBeenCalled();
        });
    });

    describe('#showFullResultsOrAwaitingSignposting', () => {
        it('should received full results from one-api and show signpost logo in UI', () => {
            spyOn(component, 'mapResultPosition');
            component.showFullResultsOrAwaitingSignposting();
            expect(component.mapResultPosition).toHaveBeenCalled();
            expect(component.showRacingSignposting).toBeTruthy();
        });

        it('should not received full results from one-api and show awaiting results button in UI', () => {
            component.greyhoundsFullResultsData = {"Error":true,"document":{}} as any;
            component.showFullResultsOrAwaitingSignposting();
            expect(component.showRacingSignposting).toBeFalsy();
            expect(component.fullResults).toBeTruthy();
        });
    });

    describe('#mapResultPosition', () => {
        it('should update position in the outcome in case of all outcomes consists of valid postions', () => {            
            const resultedRunners = greyhoundFullResultsData.document[2516472].results.runners.filter((item) => item.position != 'NR');
            component.mapResultPosition(component.eventEntity, resultedRunners as any);
            expect(component.fullResults).toBeTruthy();
            expect(component.eventEntity.resultedWEWMarket.outcomes[0].position).toBe("1");
            expect(component.eventEntity.resultedWEWMarket.outcomes[1].position).toBe("2");
            expect(component.eventEntity.resultedWEWMarket.outcomes[2].position).toBe("3");
            expect(component.eventEntity.resultedWEWMarket.outcomes[3].position).toBe("4");
            expect(component.eventEntity.resultedWEWMarket.outcomes[4].position).toBe("5");
            expect(component.eventEntity.resultedWEWMarket.outcomes[5].position).toBe("6");
        });

        it('should update position in the outcome in case of one of outcome consists of postion 0', () => {            
            component.eventEntity.resultedWEWMarket.outcomes.splice(1,5);
            greyhoundFullResultsData.document[2516472].results.runners[5].position = "0";
            const resultedRunners = greyhoundFullResultsData.document[2516472].results.runners.filter((item) => item.position != 'NR');
            component.mapResultPosition(component.eventEntity, resultedRunners as any);
            expect(component.fullResults).toBeTruthy();
            expect(component.eventEntity.resultedWEWMarket.outcomes[0].position).toBe("1");
            expect(component.eventEntity.resultedWEWMarket.outcomes[1].position).toBe("2");
            expect(component.eventEntity.resultedWEWMarket.outcomes[2].position).toBe("3");
            expect(component.eventEntity.resultedWEWMarket.outcomes[3].position).toBe("4");
            expect(component.eventEntity.resultedWEWMarket.outcomes[4].position).toBe("5");
            expect(component.eventEntity.resultedWEWMarket.outcomes[5].position).toBe("0");
        });

        it('should update position in the outcome in case of one of outcome consists of empty postion value', () => {            
            component.eventEntity.resultedWEWMarket.outcomes.splice(1,5);
            greyhoundFullResultsData.document[2516472].results.runners[5].position = "";
            const resultedRunners = greyhoundFullResultsData.document[2516472].results.runners.filter((item) => item.position != 'NR');
            component.mapResultPosition(component.eventEntity, resultedRunners as any);
            expect(component.fullResults).toBeTruthy();
            expect(component.eventEntity.resultedWEWMarket.outcomes[0].position).toBe("1");
            expect(component.eventEntity.resultedWEWMarket.outcomes[1].position).toBe("2");
            expect(component.eventEntity.resultedWEWMarket.outcomes[2].position).toBe("3");
            expect(component.eventEntity.resultedWEWMarket.outcomes[3].position).toBe("4");
            expect(component.eventEntity.resultedWEWMarket.outcomes[4].position).toBe("5");
            expect(component.eventEntity.resultedWEWMarket.outcomes[5].position).toBe("");
        });
    });
});
