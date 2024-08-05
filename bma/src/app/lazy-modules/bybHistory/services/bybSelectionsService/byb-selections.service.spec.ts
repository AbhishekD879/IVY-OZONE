import { BybSelectionsService } from '@lazy-modules/bybHistory/services/bybSelectionsService/byb-selections.service';
import { IBybSelection } from '@lazy-modules/bybHistory/models/byb-selection.model';

describe('BybSelectionsService', () => {
  let service: BybSelectionsService;
  beforeEach(() => {
    service = new BybSelectionsService();
  });

  describe('createSelection', () => {
    const leg = {
      eventEntity: { name: 'event name' },
      part: [{ description: '', eventMarketDesc: '' }]
    } as any;

    let part;

    it('anytime goalscorer', () => {
      part = {
        description: 'Gomez',
        eventMarketDesc: 'Build Your Bet Anytime Goalscorer',
        outcome: [ { result: { confirmed: 'Y' } } ]
      };
      expect(service['createSelection'](part, leg)).toEqual(
        jasmine.objectContaining({ title: 'Gomez Anytime Goalscorer' })
      );
    });

    it('to keep a clean sheet', () => {
      part = {
        description: 'Gomez To Keep A Clean Sheet - Yes',
        eventMarketDesc: 'Build Your Bet Player To Keep A Clean Sheet',
        outcome: [ { result: { confirmed: 'Y' } } ]
      };
      expect(service['createSelection'](part, leg)).toEqual(
        jasmine.objectContaining({ title: 'Gomez To Keep A Clean Sheet' })
      );
      expect(service['createSelection'](part, leg)).toEqual(
        jasmine.objectContaining({ isCleanSheetMarket: true })
      );
    });

    it('to be shown a card', () => {
      part = {
        description: 'Gomez',
        eventMarketDesc: 'Build Your Bet To Be Shown A Card',
        outcome: [ { result: { confirmed: 'Y' } } ]
      };
      expect(service['createSelection'](part, leg)).toEqual(
        jasmine.objectContaining({ title: 'Gomez To Be Carded' })
      );
    });

    it('to score 2 or more goals', () => {
      part = {
        description: 'Gomez',
        eventMarketDesc: 'Build Your Bet To Score 2 Or More Goals',
        outcome: [ { result: { confirmed: 'Y' } } ]
      };
      expect(service['createSelection'](part, leg)).toEqual(
        jasmine.objectContaining({ title: 'Gomez To Score 2+ Goals' })
      );
    });

    it('passes, assists, tackles', () => {
      part = {
        description: 'Gomez To Have 1 Or More Assists',
        eventMarketDesc: 'Build Your Bet Player Total Assists',
        outcome: [ { result: { confirmed: 'Y' } } ]
      };
      expect(service['createSelection'](part, leg)).toEqual(
        jasmine.objectContaining({ title: 'Gomez To Make 1+ Assists' })
      );
    });

    it('other player bets', () => {
      part =  {
        description: 'Gomez To Have 1 Or More Shots Outside Box',
        eventMarketDesc: 'Build Your Bet Player Total Shots Outside Box',
        outcome: [ { result: { confirmed: 'Y' } } ]
      };
      expect(service['createSelection'](part, leg)).toEqual(
        jasmine.objectContaining({ title: 'Gomez To Have 1+ Shots Outside Box' })
      );
    });

    it('default title and description', () => {
      part = {
        description: 'Draw',
        eventMarketDesc: 'Build Your Bet Corners Match Bet',
        outcome: [ { result: { confirmed: 'Y' } } ]
      };
      expect(service['createSelection'](part, leg )).toEqual(
        jasmine.objectContaining({ title: 'Draw', desc: 'Corners Match Bet' })
      );
    });
  });

  describe('formBYBTitle', () => {
    it('shoud get name from eventEntity', () => {
      const leg: any = { eventEntity: { name: 'Team1 v Team2' } };
      expect(
        service['formBYBTitle'](leg, 'participant_1 - participant_2')
      ).toEqual('Team1 - Team2');
    });

    it('shoud get name from backupEventEntity', () => {
      const leg: any = { backupEventEntity: { name: 'Team3 v Team4' } };
      expect(
        service['formBYBTitle'](leg, 'participant_1 - participant_2')
      ).toEqual('Team3 - Team4');
    });

    it('shoud get name from eventDesc', () => {
      const leg: any = { part: [{ eventDesc: 'Team5 v Team6' }] };
      expect(
        service['formBYBTitle'](leg, 'participant_1 - participant_2')
      ).toEqual('Team5 - Team6');
    });
  });

  describe('sortSelections', () => {
    it('should sort', () => {
      let leg = {
        eventEntity: { name: 'event name' },
        part: [{
          description: 'Gomez',
          eventMarketDesc: 'Build Your Bet Anytime Goalscorer',
          outcome: [ { result: { confirmed: 'Y', value: 'W' } } ]
        }, {
          description:'Ramirez',
          eventMarketDesc:'Build Your To Keep A Clean Sheet',
          outcome: [ { result: { confirmed: 'N', value: '-' } } ]
        }]
      } as any;
      let expectedResult = [
        {
          part:{
            description: 'Gomez',
            eventMarketDesc: 'Build Your Bet Anytime Goalscorer',
            outcome: [ { result: { confirmed: 'Y', value: 'W' } } ]
          },
          title: 'Gomez Anytime Goalscorer',
          status: 'Won',
          partSettled: true,
          showBetStatusIndicator: true,
          betCompletion: true
        },
        {
          part:{
            description: 'Ramirez',
            eventMarketDesc: 'Build Your To Keep A Clean Sheet',
            outcome: [ { result: { confirmed: 'N', value: '-' } } ]
          },
          title: 'Ramirez',
          status: undefined,
          partSettled: false,
          showBetStatusIndicator: undefined,
          betCompletion: false,
          isCleanSheetMarket: true
        }
      ];
      let actualResult = service.getSortedSelections(leg);

      expect(actualResult).toEqual(expectedResult as any);

      leg = {
        eventEntity: { name: 'event name' },
        part: [{
          description:'Ramirez',
          eventMarketDesc:'Build Your To Keep A Clean Sheet',
          outcome: [ { result: { confirmed: 'Y', value: 'L' } } ]
        },{
          description: 'Gomez',
          eventMarketDesc: 'Build Your Bet Anytime Goalscorer',
          outcome: [ { result: { confirmed: 'Y', value: 'V' } } ]
        }]
      } as any;
      expectedResult = [
        {
          part:{
            description:'Gomez',
            eventMarketDesc:'Build Your Bet Anytime Goalscorer',
            outcome: [ { result: { confirmed: 'Y', value: 'V' } } ]
          },
          title:'Gomez Anytime Goalscorer',
          status: 'Lose',
          partSettled: true,
          showBetStatusIndicator: true,
          betCompletion: true
        },
        {
          part:{
            description:'Ramirez',
            eventMarketDesc:'Build Your To Keep A Clean Sheet',
            outcome: [ { result: { confirmed: 'Y', value: 'L' } } ]
          },
          title:'Ramirez',
          status: 'Lose',
          partSettled: true,
          showBetStatusIndicator: true,
          betCompletion: true,
          isCleanSheetMarket: true
        }
        ];
      actualResult = service.getSortedSelections(leg);

      expect(actualResult).toEqual(expectedResult as any);
    });

    it('should not sort', () => {
      const leg = {
        eventEntity: { name: 'event name' },
        part: [{
          description: 'Gomez',
          eventMarketDesc: 'Build Your To Keep A Clean Sheet',
          outcome: [ { result: { confirmed: 'Y', value: 'W' } } ]
        }, {
          description: 'Gomez',
          eventMarketDesc: 'Build Your To Keep A Clean Sheet',
          outcome: [ { result: { confirmed: 'Y', value: 'W' } } ]
        }]
      } as any;
      const expectedResult = [
        {
          part:{
            description:'Gomez',
            eventMarketDesc:'Build Your To Keep A Clean Sheet',
            outcome: [ { result: { confirmed: 'Y', value: 'W' } } ]
          },
          title:'Gomez',
          status: 'Won',
          partSettled: true,
          showBetStatusIndicator: true,
          betCompletion: true,
          isCleanSheetMarket: true
        },
        {
          part:{
            description:'Gomez',
            eventMarketDesc:'Build Your To Keep A Clean Sheet',
            outcome: [ { result: { confirmed: 'Y', value: 'W' } } ]
          },
          title:'Gomez',
          status: 'Won',
          partSettled: true,
          showBetStatusIndicator: true,
          betCompletion: true,
          isCleanSheetMarket: true
        }
        ];
      const actualResult = service.getSortedSelections(leg);

      expect(actualResult).toEqual(expectedResult as any);
    });
  });

  describe('checkForCommonPlayerBetTitle', () => {
    it('eventMarketDesc doesnt include "Build Your Bet Player"', () => {
      expect(service['checkForCommonPlayerBetTitle']('Build Your Bet')).toBeFalsy();
    });

    it('shoud return false for Player To Get First Booking market', () => {
      expect(service['checkForCommonPlayerBetTitle']('Build Your Bet Player To Get First Booking')).toBeFalsy();
    });

    it('shoud return false for Player To Outscore The Opposition market', () => {
      expect(service['checkForCommonPlayerBetTitle']('Build Your Bet Player To Outscore The Opposition')).toBeFalsy();
    });

    it('shoud return false for Player To Get First Booking market', () => {
      expect(service['checkForCommonPlayerBetTitle']('Build Your Bet Player To Test')).toBeTruthy();
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

  describe('define subject', () => {
    it('should define subject', () => {
      expect(service.hideTooltipTriggerSub).toBeDefined();
    });
  });

  describe('replaceStoredSelection', () => {
    it('should trigger next in subject', () => {
      const selection = { showTooltip: false, title: 'Positive' } as IBybSelection;
      const storedSelection: IBybSelection = undefined;
      service['hideTooltipTriggerSub'] = {
         next: jasmine.createSpy('next')
       } as any;
      service['replaceStoredSelection'](selection);
      expect(service['hideTooltipTriggerSub'].next).toHaveBeenCalledWith(storedSelection);
    });

    it('should NOT trigger next in subject', () => {
      const selection = { showTooltip: false, title: 'Positive' } as IBybSelection;
      service['storedSelection'] = selection;
      service['hideTooltipTriggerSub'] = {
         next: jasmine.createSpy('next')
       } as any;
      service['replaceStoredSelection'](selection);
      expect(service['hideTooltipTriggerSub'].next).not.toHaveBeenCalled();
    });
  });
});

