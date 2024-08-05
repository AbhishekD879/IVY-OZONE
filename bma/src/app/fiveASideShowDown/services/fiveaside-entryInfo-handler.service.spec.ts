import { FiveASideEntryInfoService } from '@app/fiveASideShowDown/services/fiveaside-entryInfo-handler.service';
import { MY_ENTRIES_LIST } from '@app/fiveASideShowDown/mockdata/entryinfo.mock';


describe('FiveASideEntryInfohandlerService', () => {
    let service: FiveASideEntryInfoService;
    let fracService;
    beforeEach(() => {
        fracService = {
            getDecimal: jasmine.createSpy('getDecimal').and.returnValue(0.25)
        };
        service = new FiveASideEntryInfoService(fracService);
    });
    describe('entriesCreation', () => {
        it('entriesCreation', () => {
            const entriesList = service.entriesCreation([]);
            expect(entriesList.length).toEqual(0);
            expect(fracService.getDecimal).not.toHaveBeenCalled();
        });
        it('entriesCreation', () => {
            const entriesList = service.entriesCreation(MY_ENTRIES_LIST);
            expect(entriesList.length).not.toBe(0);
            expect(fracService.getDecimal).toHaveBeenCalled();
        });
        it('entriesCreation withoverallProgressPct is undefined ', () => {
            MY_ENTRIES_LIST[0].overallProgressPct = undefined;
            const entriesList = service.entriesCreation(MY_ENTRIES_LIST);
            expect(entriesList.length).not.toBe(0);
            expect(fracService.getDecimal).toHaveBeenCalled();
        });
    });
    describe('progressPercentage', () => {
        it('progress should be 0% (min >= max)', () => {
            expect(service['progressPercentage'](1, 1)).toBe(0);
        });
        it('progress should be 0% (value < min)', () => {
            expect(service['progressPercentage'](0, -10)).toBe(0);
        });
        it('progress should be 100% (value > max)', () => {
            expect(service['progressPercentage'](0, 10, 20)).toBe(100);
        });
        it('progress should be 50%', () => {
            expect(service['progressPercentage'](0, 50, 25)).toBe(50);
        });
        it('progress should be 75%', () => {
            expect(service['progressPercentage'](20, 60, 50)).toBe(75);
        });
        it('progress should be 0%', () => {
            expect(service['progressPercentage'](20, 60, -1)).toBe(0);
        });
    });
    describe('parseStatValue', () => {
        it('should parse ">0.5" as 1', () => {
            expect(service['parseStatValue']('>0.5'))
                .toEqual(1);
        });
        it('should parse "<0.5" as 0', () => {
            expect(service['parseStatValue']('<0.5'))
                .toEqual(0);
        });
        it('should parse "=<0.5" as 0', () => {
            expect(service['parseStatValue']('=<0.5'))
                .toEqual(0);
        });
        it('should parse ">=1" as 1', () => {
            expect(service['parseStatValue']('>=1'))
                .toEqual(1);
        });
        it('should parse "1" as 1', () => {
            expect(service['parseStatValue']('1'))
                .toEqual(1);
        });
        it('should parse "=1" as 1', () => {
            expect(service['parseStatValue']('=1'))
                .toEqual(1);
        });
    });

    describe('outComesFormation', () => {
        it('outComesFormation with data', () => {
            spyOn(service as any, 'outComeProgress').and.returnValue(MY_ENTRIES_LIST[0].legs[0]);
            expect(service.outComesFormation(MY_ENTRIES_LIST[0].legs).length).not.toBe(0);
        });
        it('outComesFormation with data', () => {
            spyOn(service as any, 'outComeProgress').and.returnValue(MY_ENTRIES_LIST[0].legs[0]);
            expect(service.outComesFormation([]).length).toBe(0);
        });
    });

    describe('capitalize', () => {
        it('Properly Casing if any word having diacritical', () => {
          expect(service['capitalize']('RáDéBó')).toEqual('Rádébó');
        });
        it('Properly Casing if any word having diacritical', () => {
          expect(service['capitalize']('RáDéBó AáBó')).toEqual('Rádébó Aábó');
        });
      });

    describe('outComeProgress', () => {
        it('outComeProgress with one Goal Scored', () => {
            const entriesList = MY_ENTRIES_LIST;
            entriesList[0].legs[0].optaStatValue = 1;
            (entriesList[0].legs[0] as any).progressPct = 100;
            spyOn(service as any, 'createSelection').and.returnValue('test');
            expect(service['outComeProgress'](entriesList[0].legs[0]).legprogressdetails).toBe(' Goal');
        });
        it('outComeProgress when 2 Goals Scored', () => {
            const entriesList = MY_ENTRIES_LIST;
            entriesList[0].legs[0].optaStatValue = 2;
            (entriesList[0].legs[0] as any).progressPct = 100;
            spyOn(service as any, 'createSelection').and.returnValue('test');
            expect(service['outComeProgress'](entriesList[0].legs[0]).legprogressdetails).toBe(' Goals');
        });
        it('outComeProgress when 0/undefined Goals Scored', () => {
            const entriesList = MY_ENTRIES_LIST;
            entriesList[0].legs[0].optaStatValue = undefined;
            (entriesList[0].legs[0] as any).progressPct = 100;
            spyOn(service as any, 'createSelection').and.returnValue('test');
            expect(service['outComeProgress'](entriesList[0].legs[0]).legprogressdetails).toBe(' Goals');
        });
        it('outComeProgress when 2 Goals Scored', () => {
            const entriesList = MY_ENTRIES_LIST;
            entriesList[0].legs[0].optaStatValue = 2;
            (entriesList[0].legs[0] as any).progressPct = 90;
            spyOn(service as any, 'createSelection').and.returnValue('test');
            expect(service['outComeProgress'](entriesList[0].legs[0]).legprogressdetails).toBe(' of 2 Goals');
        });
        it('outComeProgress when 2 Goals Scored', () => {
            const entriesList = MY_ENTRIES_LIST;
            entriesList[0].legs[0].optaStatValue = 1;
            (entriesList[0].legs[0] as any).progressPct = 90;
            spyOn(service as any, 'createSelection').and.returnValue('test');
            expect(service['outComeProgress'](entriesList[0].legs[0]).legprogressdetails).toBe(' of 2 Goals');
        });
        it('outComeProgress when 0 Goal Scored', () => {
            const entriesList = MY_ENTRIES_LIST;
            entriesList[0].legs[0].statValue = '>0.5';
            entriesList[0].legs[0].optaStatValue = 0;
            spyOn(service as any, 'createSelection').and.returnValue('test');
            (entriesList[0].legs[0] as any).progressPct = 90;
            expect(service['outComeProgress'](entriesList[0].legs[0]).legprogressdetails).toBe(' of 1 Goal');
        });
        it('outComeProgress when progressPct is morethan 100', () => {
            const entriesList = MY_ENTRIES_LIST;
            entriesList[0].legs[0].optaStatValue = 2;
            (entriesList[0].legs[0] as any).progressPct = 101;
            spyOn(service as any, 'createSelection').and.returnValue('test');
            expect(service['outComeProgress'](entriesList[0].legs[0]).progressPct).toBe(100);
        });
    });
    describe('nameFormat', () => {
        it('if name is correct', () => {
            expect(service['nameFormat']('test-hyd345')).toBe('test-***');
        });
        it('if name is empty', () => {
            expect(service['nameFormat']('')).toBe('');
        });
    });
    describe('isOpened', () => {
        it('isOpened', () => {
            MY_ENTRIES_LIST[0].isOpened = false;
            MY_ENTRIES_LIST[1].isOpened = false;
            const data = service['isOpened'](0, MY_ENTRIES_LIST);
            expect(data[0].isOpened).toBe(true);
            expect(data[1].isOpened).toBe(false);
        });
        it('isOpened When isOpened is true', () => {
            MY_ENTRIES_LIST[0].isOpened = true;
            MY_ENTRIES_LIST[1].isOpened = false;
            const data = service['isOpened'](0, MY_ENTRIES_LIST);
            expect(data[0].isOpened).toBe(false);
            expect(data[1].isOpened).toBe(false);
        });
        it('isOpened When isOpened is true', () => {
            MY_ENTRIES_LIST[0].isOpened = true;
            MY_ENTRIES_LIST[1].isOpened = false;
            const data = service['isOpened'](0, []);
            expect(data.length).toBe(0);
        });
    });
    describe('statsCategorySingularOrNot', () => {
        it('statsCategorySingularOrNot', () => {
            const Outcome = { optaStatValue: 1 } as any;
            const data = service['statsCategorySingularOrNot'](true, Outcome, 1);
            expect(data['Score']).toBe('Goal');
        });
        it('statsCategorySingularOrNot', () => {
            const Outcome = { optaStatValue: 1 } as any;
            const data = service['statsCategorySingularOrNot'](true, Outcome, 2);
            expect(data['Score']).toBe('Goal');
        });
        it('statsCategorySingularOrNot', () => {
            const Outcome = { optaStatValue: 2 } as any;
            const data = service['statsCategorySingularOrNot'](true, Outcome, 1);
            expect(data['Score']).toBe('Goals');
        });
        it('statsCategorySingularOrNot', () => {
            const Outcome = { optaStatValue: 2 } as any;
            const data = service['statsCategorySingularOrNot'](true, Outcome, 2);
            expect(data['Score']).toBe('Goals');
        });
        it('statsCategorySingularOrNot', () => {
            const Outcome = { optaStatValue: 1 } as any;
            const data = service['statsCategorySingularOrNot'](false, Outcome, 1);
            expect(data['Score']).toBe('Goal');
        });
        it('statsCategorySingularOrNot', () => {
            const Outcome = { optaStatValue: 2 } as any;
            const data = service['statsCategorySingularOrNot'](false, Outcome, 1);
            expect(data['Score']).toBe('Goal');
        });
        it('statsCategorySingularOrNot', () => {
            const Outcome = { optaStatValue: 1 } as any;
            const data = service['statsCategorySingularOrNot'](false, Outcome, 2);
            expect(data['Score']).toBe('Goals');
        });
        it('statsCategorySingularOrNot', () => {
            const Outcome = { optaStatValue: 2 } as any;
            const data = service['statsCategorySingularOrNot'](false, Outcome, 2);
            expect(data['Score']).toBe('Goals');
        });
    });



    describe('createSelection', () => {
        let part;
        it('anytime goalscorer', () => {
            part = {
                outcomeName: 'Gomez',
                marketName: 'Build Your Bet Anytime Goalscorer'
            };
            expect(service['createSelection'](part)).toEqual('Gomez Anytime Goalscorer');
        });
        it('to keep a clean sheet', () => {
            part = {
                outcomeName: 'Gomez To Keep A Clean Sheet - Yes',
                marketName: 'Build Your Bet Player To Keep A Clean Sheet'
            };
            expect(service['createSelection'](part)).toEqual('Gomez To Keep A Clean Sheet');
        });

        it('to be shown a card', () => {
            part = {
                outcomeName: 'Gomez',
                marketName: 'Build Your Bet To Be Shown A Card'
            };
            expect(service['createSelection'](part)).toEqual('Gomez To Be Carded');
        });
        it('to score 2 or more goals', () => {
            part = {
                outcomeName: 'Gomez',
                marketName: 'Build Your Bet To Score 2 Or More Goals'
            };
            expect(service['createSelection'](part)).toEqual('Gomez To Score 2+ Goals');
        });
        it('passes, assists, tackles', () => {
            part = {
                outcomeName: 'Gomez To Have 1 Or More Assists',
                marketName: 'Build Your Bet Player Total Assists'
            };
            expect(service['createSelection'](part)).toEqual('Gomez To Make 1+ Assists');
        });
        it('other player bets', () => {
            part = {
                outcomeName: 'Gomez To Have 1 Or More Shots Outside Box',
                marketName: 'Build Your Bet Player Total Shots Outside Box'
            };
            expect(service['createSelection'](part)).toEqual('Gomez To Have 1+ Shots Outside Box');
        });
        it('default title and description', () => {
            part = {
                outcomeName: 'Draw',
                marketName: 'Build Your Bet Corners Match Bet'
            };
            expect(service['createSelection'](part)).toEqual('Draw');
        });
    });

    describe('isCleanSheetMarketUpdate', () => {
        it('isCleanSheetMarketUpdate with marketName other than cleansheet', () => {
            const entriesList = MY_ENTRIES_LIST;
            entriesList[0].legs[0].statValue = '>=2';
            const outcome = service['isCleanSheetMarketUpdate'](entriesList[0].legs[0]);
            expect(outcome.statValue).toBe('>=2');
        });
        it('isCleanSheetMarketUpdate with marketName Build Your Bet Player To Keep A Clean Sheet', () => {
            const entriesList = MY_ENTRIES_LIST;
            entriesList[0].legs[0].marketName = 'Build Your Bet Player To Keep A Clean Sheet';
            const outcome = service['isCleanSheetMarketUpdate'](entriesList[0].legs[0]);
            expect(outcome.statValue).toBe('0');
        });
        it('isCleanSheetMarketUpdate with marketName Build Your Bet Player To Keep A Clean Sheet', () => {
            const entriesList = MY_ENTRIES_LIST;
            entriesList[0].legs[0].marketName = 'Build Your Bet Player To Keep A Clean Sheet';
            (entriesList[0].legs[0] as any).progressPct = -1;
            const outcome = service['isCleanSheetMarketUpdate'](entriesList[0].legs[0]);
            expect(outcome.progressPct).toBe(0);
        });
    });
});
