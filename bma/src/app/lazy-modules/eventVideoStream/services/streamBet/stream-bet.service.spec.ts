import { StreamBetService } from './stream-bet.service';

describe('StreamBetService', () => {
   const service: StreamBetService = new StreamBetService();
    describe('isCorrectScoreMarket', () => {
        it('should return true', () => {
            const marketMock = {
                dispSortName: 'CS'
            }
            expect(service['isCorrectScoreMarket'](marketMock as any)).toBeTrue();
        });
    });
    describe('isSingleDropSingleOdd', () => {
        it('should return true with minorcode', () => {
            const marketMock = {
                name: 'first team home goal scorer',
                templateMarketName: 'Player TEAM Most Consecutive Frames Won',
                dispSortName: 'L1',
                marketMeaningMinorCode: 'FS'
            }
            expect(service['isSingleDropSingleOdd'](marketMock as any)).toBeTrue();
        });
        it('should return return undefined', () => {
            const marketMock = {
                name: null,
                templateMarketName: 'Player TEAM Most Consecutive Frames Won',
                dispSortName: 'L',
                marketMeaningMinorCode: 'S'
            }
            expect(service['isSingleDropSingleOdd'](marketMock as any)).toBeFalse();
        });
        it('should return true with sortName', () => {
            const marketMock = {
                name: 'scoreafter42frames',
                templateMarketName: 'Player TEAM Most Consecutive Frames Won',
                dispSortName: 'L1',
            }
            expect(service['isSingleDropSingleOdd'](marketMock as any)).toBeTrue();
        });
        it('should return true with templateName', () => {
            const marketMock = {
                name: 'scoreafter',
                templateMarketName: 'Player A Most Consecutive Frames Won',
            }
            expect(service['isSingleDropSingleOdd'](marketMock as any)).toBeTrue();
        });
        it('should return true with name', () => {
            const marketMock = {
                name: 'serieswinner',
                templateMarketName: 'Player TEAM Most Consecutive Frames Won',
            }
            expect(service['isSingleDropSingleOdd'](marketMock as any)).toBeTrue();
        });
        it('should return false with isMarketNameExcludedFromSingleDropSingleOdd', () => {
            const marketMock = {
                name: 'doublechance',
                templateMarketName: 'Player TEAM Most Consecutive Frames Won'
            }
            expect(service['isSingleDropSingleOdd'](marketMock as any)).toBeFalse();
        });
        it('should return true with outcomelength and marketName', () => {
            const marketMock = {
                name: 'firstteamhomegoalscorer',
                templateMarketName: 'Player TEAM Most Consecutive Frames Won',
                outcomes: [{ name: 'teamA' }, { name: 'teamB' }, { name: 'teamC' }, { name: 'team' }]
            }
            expect(service['isSingleDropSingleOdd'](marketMock as any)).toBeTrue();
        });
        it('should return true with sortName and minorCode and marketName', () => {
            const marketMock = {
                name: 'lastgoalscorer',
                dispSortName: "--",
                marketMeaningMinorCode: "--",
                templateMarketName: 'Player TEAM Most Consecutive Frames Won',
            }
            expect(service['isSingleDropSingleOdd'](marketMock as any)).toBeTrue();
        });
    });
    describe('isSingleDropDoubleOdd', () => {
        it('should return true', () => {
            const marketMock = {
                outcomes: [{ name: 'teamA' }, { name: 'teamB' }],
                name: "Match Result and Over/Under. Goals"
            }
            expect(service['isSingleDropDoubleOdd'](marketMock as any)).toBeTrue();
        });
        it('should return false', () => {
            const marketMock = {
                outcomes: [{ name: 'teamA' }, { name: 'teamB' }],
                name: "Match Result and Over/Under"
            }
            expect(service['isSingleDropDoubleOdd'](marketMock as any)).toBeFalse();
        });
    });
    describe('isDoubleDropSingleOdd', () => {
        it('should return true', () => {
            const marketMock = {
                name: 'doubleresult'
            }
            expect(service['isDoubleDropSingleOdd'](marketMock as any)).toBeTrue();
        });
        it('should return undefined', () => {
            const marketMock = { name: null }
            expect(service['isDoubleDropSingleOdd'](marketMock as any)).toBeUndefined();
        });
    });
    describe('isMultipleOdds', () => {
        it('should return true', () => {
            const marketMock = {
                dispSortName: 'MR'
            }
            expect(service['isMultipleOdds'](marketMock as any)).toBeTrue();
        });
        it('should return false', () => {
            const marketMock = {
                dispSortName: 'M'
            }
            expect(service['isMultipleOdds'](marketMock as any)).toBeFalse();
        });
    });
    describe('isSingleCounterDoubleOdd', () => {
        it('should return true', () => {
            const marketMock = {
                dispSortName: 'HL'
            }
            expect(service['isSingleCounterDoubleOdd'](marketMock as any)).toBeTrue();
        });
        it('should return false', () => {
            const marketMock = {
                dispSortName: 'M'
            }
            expect(service['isSingleCounterDoubleOdd'](marketMock as any)).toBeFalse();
        });
    });
    describe('isDoubleOdds', () => {
        it('should return true with dispsortname', () => {
            const marketMock = {
                outcomes: [{ name: 'teamA' }, { name: 'TeamB' }],
                dispSortName: 'BO',
                name: 'Set Extra Points Required?'
            }
            expect(service['isDoubleOdds'](marketMock as any)).toBeTrue();
        });
        it('should return true with outcome length and market', () => {
            const marketMock = {
                outcomes: [{ name: 'teamA' }, { name: 'TeamB' }],
                name: "Some Random Text Set Extra Points Required?"
            }
            expect(service['isDoubleOdds'](marketMock as any)).toBeTrue();
        });
        it('should return false', () => {
            const marketMock = {
                dispSortName: 'M'
            }
            expect(service['isDoubleOdds'](marketMock as any)).toBeFalse();
        });
    });
    describe('getMarketTemplate', () => {
        it('should return HR as true', () => {
            const marketMock = {
                templateType: 'single-counter-double-odd'
            }
            const eventEntity = {
                categoryId: '21'
            }
            const templateName = service['getMarketTemplate'](marketMock as any, eventEntity as any);
            expect(templateName).toEqual('horse-racing-template');
        });
        it('should return single-counter-double-odd as true', () => {
            const marketMock = {
                templateType: 'single-counter-double-odd'
            }
            const eventEntity = {
                categoryId: '20'
            }
            const templateName = service['getMarketTemplate'](marketMock as any, eventEntity as any);
            expect(templateName).toEqual('single-counter-double-odd');
        });
        it('should return single-drop-double-odd as true', () => {
            const marketMock = {
                templateType: 'single-drop-double-odd'
            }
            const eventEntity = {
                categoryId: '20'
            }
            const templateName = service['getMarketTemplate'](marketMock as any as any, eventEntity as any);
            expect(templateName).toEqual('single-drop-double-odd');
        });
        it('should return isSingleDropSingleOdd as true', () => {
            const marketMock = {
                templateType: 'single-drop-one-odd'
            };
            const eventEntity = {
                categoryId: '20'
            };
            service.isSingleDropSingleOdd = jasmine.createSpy('isSingleDropSingleOdd').and.returnValue(true);
            const templateName = service['getMarketTemplate'](marketMock as any, eventEntity as any);
            expect(templateName).toEqual('single-drop-single-odd');
        });
        it('should return isDoubleDropSingleOdd as true', () => {
            const marketMock = {
                templateType: 'single-drop-one-odd'
            };
            const eventEntity = {
                categoryId: '20'
            };
            service.isSingleDropSingleOdd = jasmine.createSpy('isSingleDropSingleOdd').and.returnValue(false);
            service.isDoubleDropSingleOdd = jasmine.createSpy('isDoubleDropSingleOdd').and.returnValue(true);
            const templateName = service['getMarketTemplate'](marketMock as any, eventEntity as any);
            expect(templateName).toEqual('double-drop-single-odd');
        });
        it('should return isSingleDropDoubleOdd as true', () => {
            const marketMock = {
                templateType: 'single-drop-one-odd'
            }
            const eventEntity = {
                categoryId: '20'
            }
            service.isSingleDropSingleOdd = jasmine.createSpy('isSingleDropSingleOdd').and.returnValue(false);
            service.isDoubleDropSingleOdd = jasmine.createSpy('isDoubleDropSingleOdd').and.returnValue(false);
            service.isSingleDropDoubleOdd = jasmine.createSpy('isSingleDropDoubleOdd').and.returnValue(true);
            const templateName = service['getMarketTemplate'](marketMock as any, eventEntity as any);
            expect(templateName).toEqual('single-drop-double-odd');
        });
        it('should return isSingleCounterDoubleOdd as true', () => {
            const marketMock = {
                templateType: 'single-drop-one-odd'
            }
            const eventEntity = {
                categoryId: '20'
            }
            service.isSingleDropSingleOdd = jasmine.createSpy('isSingleDropSingleOdd').and.returnValue(false);
            service.isDoubleDropSingleOdd = jasmine.createSpy('isDoubleDropSingleOdd').and.returnValue(false);
            service.isSingleDropDoubleOdd = jasmine.createSpy('isSingleDropDoubleOdd').and.returnValue(false);
            service.isSingleCounterDoubleOdd = jasmine.createSpy('isSingleCounterDoubleOdd').and.returnValue(true);

            const templateName = service['getMarketTemplate'](marketMock as any, eventEntity as any);
            expect(templateName).toEqual('single-counter-double-odd');
        });
        it('should return isDoubleOdds as true', () => {
            const marketMock = {
                templateType: 'single-drop-one-odd'
            }
            const eventEntity = {
                categoryId: '20'
            }
            service.isSingleDropSingleOdd = jasmine.createSpy('isSingleDropSingleOdd').and.returnValue(false);
            service.isDoubleDropSingleOdd = jasmine.createSpy('isDoubleDropSingleOdd').and.returnValue(false);
            service.isSingleDropDoubleOdd = jasmine.createSpy('isSingleDropDoubleOdd').and.returnValue(false);
            service.isSingleCounterDoubleOdd = jasmine.createSpy('isSingleCounterDoubleOdd').and.returnValue(false);
            service.isMultipleOdds = jasmine.createSpy('isMultipleOdds').and.returnValue(false);
            service.isDoubleOdds = jasmine.createSpy('isDoubleOdds').and.returnValue(true);

            const templateName = service['getMarketTemplate'](marketMock as any, eventEntity as any);
            expect(templateName).toEqual('price-odd-button');
        });
        it('should return isCorrectScoreMarket as true', () => {
            const marketMock = {
                templateType: 'single-drop-one-odd'
            }
            const eventEntity = {
                categoryId: '20'
            }
            service.isSingleDropSingleOdd = jasmine.createSpy('isSingleDropSingleOdd').and.returnValue(false);
            service.isDoubleDropSingleOdd = jasmine.createSpy('isDoubleDropSingleOdd').and.returnValue(false);
            service.isSingleDropDoubleOdd = jasmine.createSpy('isSingleDropDoubleOdd').and.returnValue(false);
            service.isSingleCounterDoubleOdd = jasmine.createSpy('isSingleCounterDoubleOdd').and.returnValue(false);
            service.isMultipleOdds = jasmine.createSpy('isMultipleOdds').and.returnValue(false);
            service.isDoubleOdds = jasmine.createSpy('isDoubleOdds').and.returnValue(false);
            service.isCorrectScoreMarket = jasmine.createSpy('isCorrectScoreMarket').and.returnValue(true);
            const templateName = service['getMarketTemplate'](marketMock as any, eventEntity as any);
            expect(templateName).toEqual('correct-score-market');
        });
        it('should return special-market as true', () => {
            const marketMock = {
                templateType: 'single-drop-one-odd'
            }
            const eventEntity = {
                categoryId: '20'
            }
            service.isSingleDropSingleOdd = jasmine.createSpy('isSingleDropSingleOdd').and.returnValue(false);
            service.isDoubleDropSingleOdd = jasmine.createSpy('isDoubleDropSingleOdd').and.returnValue(false);
            service.isSingleDropDoubleOdd = jasmine.createSpy('isSingleDropDoubleOdd').and.returnValue(false);
            service.isSingleCounterDoubleOdd = jasmine.createSpy('isSingleCounterDoubleOdd').and.returnValue(false);
            service.isMultipleOdds = jasmine.createSpy('isMultipleOdds').and.returnValue(false);
            service.isDoubleOdds = jasmine.createSpy('isDoubleOdds').and.returnValue(false);
            service.isCorrectScoreMarket = jasmine.createSpy('isCorrectScoreMarket').and.returnValue(false);
            const templateName = service['getMarketTemplate'](marketMock as any, eventEntity as any);
            expect(templateName).toEqual('special-market');
        });
        it('should return special template if evententity is null', () => {
            const eventEntity = {
                categoryId: '20'
            }
            const marketMock = {
                templateType: 'single-drop-one-odd'
            }
            const templateName = service['getMarketTemplate'](marketMock as any, eventEntity as any);
            expect(templateName).toEqual('special-market');
        });
        it('should return special template if evententity is null', () => {
            const eventEntity = null;
            const marketMock = {
                templateType: 'single-drop-one-odd'
            }
            const templateName = service['getMarketTemplate'](marketMock as any, eventEntity as any);
            expect(templateName).toEqual('special-market');
        });
        it('should return special template if evententity is null', () => {
            const eventEntity = {
                categoryId: null
            }
            const marketMock = {
                templateType: 'single-drop-one-odd'
            }
            const templateName = service['getMarketTemplate'](marketMock as any, eventEntity as any);
            expect(templateName).toEqual('special-market');
        })
    });
});
