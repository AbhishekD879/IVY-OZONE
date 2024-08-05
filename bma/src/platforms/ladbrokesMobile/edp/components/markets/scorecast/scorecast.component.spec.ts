import { of as observableOf } from 'rxjs';
import { ScorecastComponent } from "@ladbrokesMobile/edp/components/markets/scorecast/scorecast.component";

const firstMarketMock = {
    id: '1',
    name: 'First Goal Scorecast',
    isLpAvailable: true,
    cashoutAvail: 'Y',
    outcomes: [
        {
            displayOrder: NaN,
            id: '487',
            name: undefined,
            prices: [],
            scorecastPrices: '959656009,295,1,296.00,959655817,300,1,301.00,959655816,160,1,161.00,959655820,1050,1,1051.00,',
            scorerOutcomeId: '959656009'
        }
    ],
    templateMarketName: 'First Goal Scorecast'
};

const outcome = {
    correctPriceType: 'correctPriceType',
    correctedOutcomeMeaningMinorCode: 213,
    displayOrder: 11,
    fakeOutcome: true,
    icon: true,
    id: 'id',
    isUS: true,
    liveServChannels: 'liveServChannels',
    liveServChildrenChannels: 'liveServChildrenChannels',
    name: 'liveServChildrenChannels',
    outcomeMeaningMajorCode: 'outcomeMeaningMajorCode',
    outcomeMeaningMinorCode: 1123,
    outcomeStatusCode: 'outcomeMeaningMinorCode'
};

const teamsMock = [
    {
        name: 'teamA name',
        outcomeMeaningMinorCode: 1
    },
    {
        name: 'teamH name',
        outcomeMeaningMinorCode: 3
    }
];

const scoreCastMarkets = [{
    teamsGoalscorers: {},
    market: [{
        cashoutAvail: 'cashoutAvail',
        correctPriceTypeCode: 'correctPriceTypeCode',
        dispSortName: 'dispSortName',
        eachWayFactorNum: 'eachWayFactorNum',
        eachWayFactorDen: 'eachWayFactorDen',
        eachWayPlaces: 'eachWayPlaces',
        header: 'header',
        id: 'id',
        name: 'nameTest'
    }],
    name: 'name',
    localeName: 'localeName',
    goalscorerMarket: [{
        cashoutAvail: 'cashoutAvail',
        correctPriceTypeCode: 'correctPriceTypeCode',
        dispSortName: 'dispSortName',
        eachWayFactorNum: 'eachWayFactorNum',
        eachWayFactorDen: 'eachWayFactorDen',
        eachWayPlaces: 'eachWayPlaces',
        header: 'header',
        id: 'id',
        name: 'nameTest'
    }],
    outcome: {
        correctPriceType: 'correctPriceType',
        correctedOutcomeMeaningMinorCode: 213,
        displayOrder: 11,
        fakeOutcome: true,
        icon: true,
        id: 'id',
        isUS: true,
        liveServChannels: 'liveServChannels',
        liveServChildrenChannels: 'liveServChildrenChannels',
        name: 'liveServChildrenChannels',
        outcomeMeaningMajorCode: 'outcomeMeaningMajorCode',
        outcomeMeaningMinorCode: 1123,
        outcomeStatusCode: 'outcomeMeaningMinorCode'
    },
    scorecasts: []
}] as any;


describe('ScorecastComponent', () => {

    let fracToDecFactory, scorecastService, betSlipSelectionsData, priceOddsButtonService;
    let pubsubService, localeService, filterService, componentFactoryResolver, dialogService, changeDetectorRef;
    let component: ScorecastComponent;


    beforeEach(() => {

        const fracToDecFactory: any = {
            getFormattedValue: jasmine.createSpy('getFormattedValue').and.returnValue('1/7')
        };

        const scorecastService: any = {
            getTableOddPrice: jasmine.createSpy('getTableOddPrice').and.returnValue(observableOf({
                priceType: "LP",
                priceNum: 1,
                priceDen: 7
            } as any)),
            getMarketByMarketNamePattern: jasmine.createSpy('getMarketByMarketNamePattern').and.returnValue(firstMarketMock),
            isAnyCashoutAvailable: jasmine.createSpy('isAnyCashoutAvailable').and.returnValue(false),
            getMarketOutcomesByTeam: jasmine.createSpy('getMarketOutcomesByTeam').and.returnValue({}),
            getTeams: jasmine.createSpy('getTeams').and.returnValue({}),
        };

        const betSlipSelectionsData: any = {};
        const priceOddsButtonService: any = {};
        const pubsubService: any = {};
        const localeService: any = {};
        const filterService: any = {
            orderBy: jasmine.createSpy().and.callFake(a => a)
        };

        dialogService = {
            openDialog: jasmine.createSpy('openDialog')
        };

        changeDetectorRef = {
            detectChanges: jasmine.createSpy('detectChanges'),
        };

        componentFactoryResolver = jasmine.createSpyObj('componentFactoryResolver', ['resolveComponentFactory']);
        component = new ScorecastComponent(
            fracToDecFactory,
            scorecastService,
            betSlipSelectionsData,
            priceOddsButtonService,
            pubsubService,
            localeService,
            filterService,
            componentFactoryResolver,
            dialogService, changeDetectorRef
        );
    });

});
