import { BetShareImageCardService } from './bet-share-image-card.service';
import * as betShareMockData from './bet-share-data-mock';

describe('BetShareImageCardService', () => {
    let service: BetShareImageCardService;
    let timeService,
        localeService,
        filtersService,
        currencyPipe,
        sessionStorageService,
        bybSelectionsService;

    beforeEach(() => {
        timeService = {
            formatByPattern: jasmine.createSpy('formatByPattern').and.returnValue('DD-MM'),
            getLocalDateFromString: jasmine.createSpy('getLocalDateFromString').and.returnValue(new Date()),
            convertDateStr: jasmine.createSpy('convertDateStr').and.returnValue('2020-12-07T19:30:00Z'),
            getDatetimeWithFormatSuffix: jasmine.createSpy('getDatetimeWithFormatSuffix').and.returnValue(new Date())
        };
        localeService = {
            getString: jasmine.createSpy('getString').and.returnValue('')
        }
        filtersService = {
            date: jasmine.createSpy('date').and.returnValue('Jan 12 2018'),
            filterAddScore: jasmine.createSpy('filterAddScore').and.returnValue('test'),
            filterPlayerName : jasmine.createSpy('filterPlayerName').and.returnValue('test player')
        }
        currencyPipe = {
            transform: jasmine.createSpy('transform').and.returnValue('USD')
        }
        sessionStorageService = {
            get: jasmine.createSpy('get').and.returnValue({ '123-12345-123': { id: '123', odds:'2/3', name:'test name', eventName:'test event', time: '12-1-2023', isMultiples: true, outcomeNames: ['test outcomes'], eventMarketDescription: 'test desc' } })
        }
        bybSelectionsService = {
            getSortedSelections: jasmine.createSpy('getSortedSelections').and.returnValue([{ title: 'test title', desc: 'test desc' }])
        }


    });

    function createService() {
        service = new BetShareImageCardService(
            timeService,
            localeService,
            filtersService,
            currencyPipe,
            sessionStorageService,
            bybSelectionsService
        );
    }

    describe('', () => {
        beforeEach(() => {
            createService();
        });

        it("call prepimg object on load", () => {
            const img = "https://scmedia.itsfogo.com/$-$/5539b5e8d1cc4b6595ea27657d46ce3f.jpg";
            service.prepImgObject(img);
            expect(service).toBeTruthy;
        })

        
        it("call prepimg object on load", () => {
            const img = new Image();
            img.onload = function() {
                expect(img.width).toBeGreaterThan(0);
              };
            service.prepImgObject("https://scmedia.itsfogo.com/$-$/5539b5e8d1cc4b6595ea27657d46ce3f.jpg");
        })

        it('onload()', async () => {
            const img: any = service.prepImgObject("img");
            img.onload();
            expect(service).toBeTruthy;
          });

        it("Should call shareImageDataMapper regular bets", () => {
            const flags = { oddsFlag: true, selectionNameFlag: true, eventNameFlag: true, stakeFlag: true, returnsFlag: true, dateFlag: true };
            const params = [{
                selectionName: 'test selection', marketName: 'test market', odds: '2/3', eventStartTime: '12 Jan2022',
                eventName: 'test event', status: 'cashed out'
              }];
            params['isSettled'] = true;
            params['betType'] = 'regular bet';
            params['stake'] = '$0.1';
            params['returns'] = '$0.111';
            params['betFullDate'] = 'Jan2018,19';
            const data = service.shareImageDataMapper(flags, params, 'regularBets', '$');
            expect(data[0].line2).toBe('test market');
        })

        it("Should call shareImageDataMapper regular bets with no flags", () => {
            const flags = { oddsFlag: false, selectionNameFlag: false, eventNameFlag: false, stakeFlag: false, returnsFlag: false, dateFlag: false };
            const params = betShareMockData.SHARE_DATA;
            params['betType'] = 'regular bet';
            const data = service.shareImageDataMapper(flags, params, 'regularBets', 'USD');
            expect(data[0].line2).toBe('test market');
        })

        it("Should call shareImageDataMapper regular bets with no flags with live score", () => {
            const flags = { oddsFlag: false, selectionNameFlag: true, eventNameFlag: false, stakeFlag: false, returnsFlag: false, dateFlag: false };
            const params= betShareMockData.SHARE_DATA;
            params[0]['eventStartTime'] = '';
            params['bybType'] = 'regular bet';
            params['sortType'] = '';
            const data = service.shareImageDataMapper(flags, params, 'regularBets', 'USD');
            expect(data[0].line2).toBe('test market');
        })
        
        it("Should call shareImageDataMapper regular bets with no flags with live score and eventflag true", () => {
            const flags = { oddsFlag: false, selectionNameFlag: true, eventNameFlag: true, stakeFlag: false, returnsFlag: false, dateFlag: false };
            const params= betShareMockData.SHARE_DATA;
            params[0]['eventStartTime'] = '';
            params['bybType'] = 'regular bet';
            params['sortType'] = '';
            const data = service.shareImageDataMapper(flags, params, 'regularBets', 'USD');
            expect(data[0].line2).toBe('test market');
        })

        it("Should call shareImageDataMapper regularbet with regularBets eventStartTime and no livescore", () => {
            const flags = { oddsFlag: true, selectionNameFlag: true, eventNameFlag: true, stakeFlag: true, returnsFlag: true, dateFlag: true };
            betShareMockData.SHARE_DATA['betType'] = 'regularBets';
            betShareMockData.SHARE_DATA[0].selectionName = ['bet1','selections'] as any;
            betShareMockData.SHARE_DATA[0]['eventStartTime'] = '12-11-2022';
            const data = service.shareImageDataMapper(flags, betShareMockData.SHARE_DATA, 'regularBets', '$');
            expect(data[0].line3).toBe('test event, 12-11-2022');
            expect(data[0].line1).toEqual('bet1,selections @ 2/3');
        })

        it("should get eventStartTime false", () => {
            const flags = { oddsFlag: true, selectionNameFlag: true, eventNameFlag: true, stakeFlag: true, returnsFlag: true, dateFlag: true };
            const params= betShareMockData.SHARE_DATA;
            params[0]['eventStartTime'] = '12:02 pm';
            const data = service.shareImageDataMapper(flags, betShareMockData.SHARE_DATA, 'regularBets', '$');
            expect(data[0].line3).toBe('test event, 12:02 pm');
        })

        it("Should call shareImageDataMapper regular bets with no flags", () => {
            const flags = { oddsFlag: true, selectionNameFlag: false, eventNameFlag: false, stakeFlag: false, returnsFlag: false, dateFlag: false };
            const params= betShareMockData.SHARE_DATA
            params[0]['eventStartTime'] = '';
            params['bybType'] = 'regular bet';
            const data = service.shareImageDataMapper(flags, params, 'regularBets', 'USD');
            expect(data[0].line3).toBe('');
        })

        it("Should call shareImageDataMapper totePotPoolBet bet", () => {
            const flags = { oddsFlag: true, selectionNameFlag: true, eventNameFlag: true, stakeFlag: true, returnsFlag: true, dateFlag: true };
            
            const params = betShareMockData.SHARE_DATA;
            params['betType'] = 'totePotPoolBet';
            const data = service.shareImageDataMapper(flags, params, 'totePotPoolBet', 'USD');
            expect(data[0].line2).toEqual([ 'bet1', 'selections' ]);
        })

        it("Should call shareImageDataMapper totePoolBet bet", () => {
            const flags = { oddsFlag: true, selectionNameFlag: true, eventNameFlag: true, stakeFlag: true, returnsFlag: true, dateFlag: true };
            const params = betShareMockData.SHARE_DATA;
            params['betType'] = 'totePoolBet';
            params['stake'] = '';
            params['returns'] = '';
            const data = service.shareImageDataMapper(flags, params, 'totePoolBet', 'USD');
            expect(data[0].line2).toEqual([ 'bet1', 'selections' ]);
        })

        it("Should call shareImageDataMapper totePoolBet bet with no eventflag", () => {
            const flags = { oddsFlag: true, selectionNameFlag: true, eventNameFlag: false, stakeFlag: true, returnsFlag: true, dateFlag: true };
            const params = betShareMockData.SHARE_DATA;
            params['betType'] = 'totePoolBet';
            const data = service.shareImageDataMapper(flags, params, 'totePoolBet', 'USD');
            expect(data[0].line2).toEqual([ 'bet1', 'selections' ]);
        })

        it("Should call shareImageDataMapper lotto bet", () => {
            const flags = { oddsFlag: true, selectionNameFlag: true, eventNameFlag: true, stakeFlag: true, returnsFlag: true, dateFlag: true };
            const params = betShareMockData.SHARE_DATA;
            params['betType'] = 'lotto';
            params[0].selectionName = ['lotto1','selections'] as any;
            const data = service.shareImageDataMapper(flags, params, 'lotto', 'USD');
            expect(data[0].line3).toBe('');
        })

        it("Should call shareImageDataMapper lotto without flags", () => {
            const flags = { oddsFlag: false, selectionNameFlag: false, eventNameFlag: false, stakeFlag: false, returnsFlag: false, dateFlag: false };
            const params = betShareMockData.SHARE_DATA;
            params['betType'] = 'lotto';
            params['stake'] = '0.1';
            params['returns'] = '0.111';
            const data = service.shareImageDataMapper(flags, params, 'lotto', 'USD');
            expect(data[0].line1).toBe('');
        })

        it("Should call shareImageDataMapper lotto with currency stake and returns", () => {
            const flags = { oddsFlag: true, selectionNameFlag: true, eventNameFlag: true, stakeFlag: true, returnsFlag: true, dateFlag: true };
            const params = betShareMockData.SHARE_DATA;
            params['betType'] = 'lotto';
            params[0].selectionName = ['lotto1','selections'] as any;
            const data = service.shareImageDataMapper(flags, params, 'lotto', '$');
            expect(data[0].line2).toBe('lotto1 selections');
        })

        it("Should call shareImageDataMapper regularbet with forecast type", () => {
            const flags = { oddsFlag: true, selectionNameFlag: true, eventNameFlag: true, stakeFlag: true, returnsFlag: true, dateFlag: true };
            betShareMockData.SHARE_DATA['betType'] = 'RF';
            betShareMockData.SHARE_DATA[0].selectionName = ['bet1','selections'] as any;
            betShareMockData.SHARE_DATA['sortType'] = 'Reverse forecast';
            betShareMockData.SHARE_DATA[0]['eventStartTime'] = '12-11-2022';
            const data = service.shareImageDataMapper(flags, betShareMockData.SHARE_DATA, 'regularBets', '$');
            flags.selectionNameFlag = false;
            expect(data[0].line3).toBe('test event, 12-11-2022');
            expect(data[0].line1).toEqual([ 'bet1', 'selections' ]);
            const datawithNoSelectionFlag = service.shareImageDataMapper(flags, betShareMockData.SHARE_DATA, 'regularBets', '$');
            expect(datawithNoSelectionFlag[0].line1).toEqual('');
        })
        
        it("Should call shareImageDataMapper regularbet with Bet Builder and selectionname", () => {
            const flags = { oddsFlag: true, selectionNameFlag: true, eventNameFlag: true, stakeFlag: true, returnsFlag: true, dateFlag: true };
            const params = betShareMockData.SHARE_DATA;
            params['betType'] = 'Bet Builder';
            params[0].selectionName = ['bet1','selections'] as any;
            params[0]['eventStartTime'] = '12-11-2022';
            const data = service.shareImageDataMapper(flags, params, 'regularBets', '$');
            expect(data[0].line3).toBe('test event, 12-11-2022');
            expect(data[0].line1).toBe('');
        })

        it("Should call shareImageDataMapper regularbet with Build Your Bet type", () => {
            const flags = { oddsFlag: true, selectionNameFlag: true, eventNameFlag: true, stakeFlag: true, returnsFlag: true, dateFlag: true };
            const params = betShareMockData.SHARE_DATA;
            params[0]['marketName'] = 'Build Your Bet - test';
            params['betType'] = 'Build Your Bet';
            const data = service.shareImageDataMapper(flags, params, 'regularBets', '$');
            expect(data[0].line1).toBe('');
        })

        it("Should call shareImageDataMapper regularbet with Build Your Bet type and no eventstarttime", () => {
            const flags = { oddsFlag: true, selectionNameFlag: true, eventNameFlag: true, stakeFlag: true, returnsFlag: true, dateFlag: true };
            const params = betShareMockData.SHARE_DATA;
            params[0]['marketName'] = 'Build Your Bet - test';
            params[0]['eventStartTime'] = null;
            params['betType'] = 'Build Your Bet';
            const data = service.shareImageDataMapper(flags, params, 'regularBets', '$');
            expect(data[0].line1).toBe('');
        })

        it("Should call shareImageDataMapper regularbet with BUILD YOUR BET type and flag flase", () => {
            const flags = { oddsFlag: false, selectionNameFlag: false, eventNameFlag: false, stakeFlag: false, returnsFlag: false, dateFlag: false };
            const params = betShareMockData.SHARE_DATA;
            params[0]['marketName'] = 'Build Your Bet';
            params['stake'] = '$0.1';
            params['returns'] = '$0.111';
            params['betFullDate'] = 'Jan2018,19';
            const data = service.shareImageDataMapper(flags, params, 'regularBets', '$');
            expect(data[0].line3).toBe('');
        })

        it("Should call getOutcomeTitle", () => {
            const data = service.getOutcomeTitle(null, {} as any, 1);
            expect(data).toBe('');
        })

        it("Should call getOutcomeTitle", () => {
            const data = service.getOutcomeTitle({ isOrderedBet: true, poolOutcomes: [{}, {}] } as any, { name: 'test', isFavourite: true, runnerNumber: 'race1' } as any, 1);
            expect(data).toBe('2. test');
        })

        it("Should call getOutcomeTitle with no favorites and isOrderedBet", () => {
            const data = service.getOutcomeTitle({ isOrderedBet: false, poolOutcomes: [{}, {}] } as any, { name: 'test', isFavourite: false, runnerNumber: 'race1' } as any, 1);
            expect(data).toBe('race1. test');
        })

        it("Should call getOutcomeTitle and isOrderedBet", () => {
            const data = service.getOutcomeTitle({ isOrderedBet: false, poolOutcomes: [{}, {}] } as any, { name: 'test', isFavourite: true, runnerNumber: 'race1' } as any, 1);
            expect(data).toBe('test');
        })

        it("Should call getEventStartTime", () => {
            service.getEventStartTime({ startTime: new Date().toDateString() } as any);
            expect(service.otherDay).toBe('');
        })

        it("Should call getEventStartTime with new date", () => {
            timeService.getLocalDateFromString.and.returnValue(new Date(new Date().setFullYear(new Date().getFullYear() + 7)));
            service.getEventStartTime({ startTime: '' } as any);
            expect(service.otherDay).toBeDefined();
        })

        it("Should call totePotPoolBetDataFormation", () => {
            const data = service.totePotPoolBetDataFormation(betShareMockData.POOLS_DATA);
            expect(service.shareData[0].selectionName).toEqual([ 'test' ]);
        })

        it("Should call totePotPoolBetDataFormation with placepot and no favourites", () => {
            const data = betShareMockData.POOLS_DATA;
            data.betData.toteMarketTitle = 'Placepot';
            data.betData.leg[0].orderedOutcomes[0].isFavourite = false;
            service.totePotPoolBetDataFormation(data);
            expect(service.shareData[0].selectionName).toEqual([ 'race1. test' ]);
        })

        it("Should call totePoolBetDataFormation", () => {
            const data = betShareMockData.POOLS_DATA;
            service.totePoolBetDataFormation(data);
            expect(service.shareData[0].selectionName).toEqual('Placepot');
        })

        it("Should call jackPotPoolDataFormation", () => {
            const jackpotPoolData = { betData: { bet: betShareMockData.POOLS_DATA.betData } };
            service.jackPotPoolDataFormation(jackpotPoolData);
            expect(service.shareData.eventName).toEqual(['test']);
        })


        it("Should call regularBetsDataFormation with multiples", () => {
            sessionStorageService.get.and.returnValue({ '123-12345-123': { id: '123', isMultiples: false,
            odds:'2/3', eventName:'test event', time: '12-1-2023', outcomeNames: '', eventMarketDescription: 'test desc' } });
            const data = {...betShareMockData.REGULAR_SHARE_DATA};
            service.regularBetsDataFormation(data);
            expect(service.shareData[0].eventName).toBe('test event');
        })

        it("Should call regularBetsDataFormation without multiples", () => {
            sessionStorageService.get.and.returnValue({ '123-12345-123': { id: '123', isMultiples: false,
                odds:'2/3', eventName:'test event', time: '12-1-2023', outcomeNames: '', eventMarketDescription: 'test desc' } });
            service.regularBetsDataFormation(betShareMockData.REGULAR_SHARE_DATA);
            expect(service.shareData[0].selectionName).toBe('test player');
        })

        it("Should call regularBetsDataFormation without multiples ", () => {
            sessionStorageService.get.and.returnValue({ '123-12345-123': { id: '123', isMultiples: false,
                odds:'2/3', eventName:'test event', time: '12-1-2023', outcomeNames: '', eventMarketDescription: 'test desc' } });
            service.regularBetsDataFormation(betShareMockData.REGULAR_SHARE_DATA);
            expect(service.shareData[0].selectionName).toBe('test player');
        })

        it("Should call regularBetsDataFormation with mutiple outcomes", () => {
            const data = betShareMockData.REGULAR_SHARE_DATA;
            data.betData.eventSource.potentialPayout = 'N/A';
            data.betData.eventSource.leg[0] = {
                eventEntity: { id: '123' },
                part: [{ outcome: [{ id: '123' }] }],
                cashoutId: '12345',
                removedLeg: false
            } as any;
            service.regularBetsDataFormation(data);
            expect(service.shareData[0].selectionName).toEqual([ 'test outcomes' ]);
        })

        it("Should call regularBetsDataFormation with mutiple outcomes and potentional", () => {
            const data = betShareMockData.REGULAR_BET_CATEGORY_ID;
            data.betData.eventSource.potentialPayout = 'N/A';
            data.betData.eventSource.leg[0] = {
                eventEntity: { id: '123' },
                part: [{ outcome: [{ id: '123' }] }],
                cashoutId: '12345',
                removedLeg: false
            } as any;
            service.regularBetsDataFormation(data);
            expect(service.shareData[0].selectionName).toEqual([ 'test outcomes' ]);
        })

        it("Should call regularBetsDataFormation with mutiple outcomes and removedLeg as true", () => {
            const data = betShareMockData.REGULAR_SHARE_DATA;
            data.betData.eventSource.potentialPayout = 'N/A';
            data.betData.eventSource.leg[0] = {
                eventEntity: { id: '123' },
                part: [{ outcome: [{ id: '123' }] }],
                cashoutId: '12345',
                removedLeg: true
            } as any;
            service.regularBetsDataFormation(data)
        })

        it("Should call regularBetsDataFormation Build Your Bet with mutiple outcomes", () => {
            const data = betShareMockData.REGULAR_SHARE_DATA;
            data.betData.eventSource.leg[0] = {
                eventEntity: { id: '123' },
                part: [{ outcome: [{ id: '123' }] }],
                cashoutId: '12345'
            } as any;
            data.betData.eventSource.bybType = 'Build Your Bet';
            data.bets[0].eventSource.bybType = 'Build Your Bet';
            service.regularBetsDataFormation(data);
            expect(service.shareData[0].selectionName).toEqual([ 'test title,test desc' ] );
        })

        it("Should call regularBetsDataFormation Build Your Bet with mutiple outcomes and no description", () => {
            bybSelectionsService.getSortedSelections.and.returnValue([{ title: 'test title', desc: '' },{ title: '', desc: '' }]);
            const data = betShareMockData.REGULAR_SHARE_DATA;
            data.betData.eventSource.leg[0] = {
                eventEntity: { id: '123' },
                part: [{ outcome: [{ id: '123' }] }],
                cashoutId: '12345'
            } as any;
            data.betData.eventSource.bybType = 'Build Your Bet';
            data.bets[0].eventSource.bybType = 'Build Your Bet';
            service.regularBetsDataFormation(data);
            expect(service.shareData[0].selectionName[0]).toEqual('test title' );
        })

        it("Should call lottoDataFormation", () => {
            service.lottoDataFormation(betShareMockData.LOTTO_BET_DATA);
            expect(service.shareData[0].selectionName).toEqual(['11']);
        })

        it("Should call lottoDataFormation with drawAt 2th", () => {
            const data = betShareMockData.LOTTO_BET_DATA;
            data.betData.lotteryResults[0].drawAt = '2-3-2023';
            service.lottoDataFormation(data);
            expect(service.shareData[0].selectionName).toEqual(['11']);
        })

        it("Should call lottoDataFormation with drawAt 3rd", () => {
            const data = betShareMockData.LOTTO_BET_DATA;
            data.betData.lotteryResults[0].drawAt = new Date().toDateString();
            service.lottoDataFormation(data);
            expect(service.shareData[0].selectionName).toEqual(['11']);
        })

        it("Should call lottoDataFormation with drawAt 4th", () => {
            const data = betShareMockData.LOTTO_BET_DATA;
            const tomorowDate1 = new Date().setMonth(new Date().getMonth() + 1);
            data.betData.lotteryResults[0].drawAt = new Date(new Date(tomorowDate1).setDate(new Date(tomorowDate1).getDate() + 1)).toDateString();
            service.lottoDataFormation(data);
            expect(service.shareData[0].selectionName).toEqual(['11']);
        })

        it("Should call dateAndTimeFmt with today", () => {
            const dateTimeFmt = new Date().toLocaleDateString();
            timeService.convertDateStr.and.returnValue(dateTimeFmt);
            timeService.formatByPattern.and.returnValue(dateTimeFmt);
            timeService.getDatetimeWithFormatSuffix.and.returnValue(dateTimeFmt);
            const dateFmt = service.dateAndTimeFmt(dateTimeFmt);
            expect(dateFmt).toEqual(dateTimeFmt);
        })

    });
});