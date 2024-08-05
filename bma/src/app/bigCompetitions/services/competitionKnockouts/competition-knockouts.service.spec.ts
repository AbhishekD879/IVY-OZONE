import { CompetitionKnockoutsService } from 'app/bigCompetitions/services/competitionKnockouts/competition-knockouts.service';
import * as _ from 'underscore';

describe('CompetitionKnockoutsService', () => {
    let service,
      mockData,
      mockParsedData;

    beforeEach(() => {
      mockData = {
        knockoutRounds: [{
          name: 'name',
          active: true,
          abbreviation: 'NM',
          number: 0
        }, {
          name: 'name1',
          active: false,
          abbreviation: 'NM1',
          number: 1
        }, {
          name: 'name2',
          active: true,
          abbreviation: 'NM2',
          number: 2
        }, {
          name: 'name3',
          active: false,
          abbreviation: 'NM3',
          number: 3
        }],
        knockoutEvents: [{
          abbreviation: 'ABB',
          awayTeam: 'awayTeam',
          homeTeam: 'homeTeam',
          round: 'round'
        }, {
          abbreviation: 'ABB1',
          awayTeam: 'awayTeam1',
          homeTeam: 'homeTeam1',
          round: 'round1'
        }, {
          abbreviation: 'ABB2',
          awayTeam: 'awayTeam2',
          homeTeam: 'homeTeam2',
          round: 'round2'
        }, {
          abbreviation: 'ABB3',
          awayTeam: 'awayTeam3',
          homeTeam: 'homeTeam3',
          round: 'round3'
        }]
      };
      mockParsedData = {
        roundNames: [{
          name: 'name3',
          active: false,
          abbreviation: 'NM3',
          number: 3
        }, {
          name: 'name2',
          active: true,
          abbreviation: 'NM2',
          number: 2
        }, {
          name: 'name1',
          active: false,
          abbreviation: 'NM1',
          number: 1
        }, {
          name: 'name',
          active: true,
          abbreviation: 'NM',
          number: 0
        }],
        name3: [],
        name2: [],
        name1: [],
        name: []
      };

      service = new CompetitionKnockoutsService();
    });

    describe('@parseData', () => {
        it('should return modified data also call parseData with it', () => {
          service['sortEvents'] = jasmine.createSpy('sortEvents');
          const result = service.parseData(mockData);

          expect(service['sortEvents']).toHaveBeenCalledWith(mockParsedData);
          expect(result).toEqual(mockParsedData);
          expect(result.name3).toEqual([]);
        });

        it('should combine events by round name', () => {
          service['sortEvents'] = jasmine.createSpy('sortEvents');
          mockData.knockoutEvents[3].round = 'name3';
          mockData.knockoutEvents[2].round = 'name3';
          mockData.knockoutEvents[1].round = 'name3';
          const result = service.parseData(mockData);

          expect(result.name3).toEqual([mockData.knockoutEvents[1], mockData.knockoutEvents[2], mockData.knockoutEvents[3]]);
        });
    });

    describe('@splitEvents', () => {
      it('@splitEvents should split the array', () => {
        const result = service['splitEvents'](mockData.knockoutEvents);

        expect(result).toEqual([
          [mockData.knockoutEvents[0], mockData.knockoutEvents[1]],
          [mockData.knockoutEvents[2], mockData.knockoutEvents[3]]
        ]);
      });

      it('@splitEvents should NOT split the array', () => {
        const result = service['splitEvents']([mockData.knockoutEvents[0]]);

        expect(result).toEqual([[mockData.knockoutEvents[0]]]);
      });
    });

  describe('@sortEvents', () => {
    beforeEach(() => {
      service['splitEvents'] = jasmine.createSpy('splitEvents');
      spyOn(_, 'sortBy');
    });

    it('@sortEvents should doing nothing for the "roundNames" key', () => {
      service['sortEvents']({roundNames: []});

      expect(service['splitEvents']).not.toHaveBeenCalled();
      expect(_.sortBy).not.toHaveBeenCalled();
    });

    it('@splitEvents should NOT split the array', () => {
      service['sortEvents']({name: [], name1: []});

      expect(service['splitEvents']).toHaveBeenCalledTimes(2);
      expect(_.sortBy).toHaveBeenCalledTimes(2);
    });
  });
});
