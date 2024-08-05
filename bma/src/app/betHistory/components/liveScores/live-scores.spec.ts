import { LiveScoresComponent } from '@app/betHistory/components/liveScores/live-scores.component';

describe('LiveScoresComponent', () => {
  let component: LiveScoresComponent;

  const timeServiceStub = {
    animationDelay: 5000
  } as any;

  const renderer = {
    renderer: {
      addClass: jasmine.createSpy(),
      removeClass: jasmine.createSpy()
    }
  } as any;

  const windowRefStub = {
    nativeWindow: {
      clearTimeout: jasmine.createSpy('clearTimeout'),
      setTimeout: jasmine.createSpy('setTimeout').and.callFake((fn, time) => { fn(); })
    }
  } as any;

  beforeEach(() => {
    component = new LiveScoresComponent(renderer, timeServiceStub, windowRefStub);
    component.event = {
      categoryCode: 'FOOTBALL'
    } as any;
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });
  
  it('should test oninit', () => {
    component.ngOnInit();
    expect(component.isFootball).toBeTruthy();
  });

  it('should check Advance for tennis', () => {
    let currentPoints = 'Adv';
    expect(component.isAdvance(currentPoints)).toBeTruthy();
    currentPoints = '1';
    expect(component.isAdvance(currentPoints)).toBeFalsy();
    currentPoints = undefined;
    expect(component.isAdvance(currentPoints)).toBeFalsy();
  });

  describe('ngOnChanges', () => {
    it('should NOT trigger football score change', () => {
      spyOn<any>(component, 'processFootballScoreChanged');
      component.event = {
        categoryCode: 'not-FOOTBALL'
      } as any;
      component.ngOnChanges({} as any);

      expect(component['processFootballScoreChanged']).not.toHaveBeenCalled();
    });
    it('should trigger football score change', () => {
      spyOn<any>(component, 'processFootballScoreChanged');
      component.isFootball = true;
      component.awayScore = '2';
      component.homeScore = '0';
      let changes = {
        homeScore: {
          firstChange: false,
          currentValue: 1,
          previousValue: 0
        },
        awayScore: {
          firstChange: true
        }
      } as any;
      component.ngOnChanges(changes);

      // home score changed
      expect(component['processFootballScoreChanged']).toHaveBeenCalledWith([1, 2], [0, 2]);
      changes = {
        homeScore: {
          firstChange: true,
        },
        awayScore: {
          firstChange: false,
          currentValue: 3,
          previousValue: 2
        }
      } as any;
      component.ngOnChanges(changes);

      // home score changed
      expect(component['processFootballScoreChanged']).toHaveBeenCalledWith([0, 3], [0, 2]);
    });
  });

  describe('@processFootballScoreChanged', () => {
    beforeEach(() => {
      spyOn<any>(component, 'scoreTextAnimation');
    });

    it('should not animate score if no score changes', () => {
      component['processFootballScoreChanged']([0, 0], [0, 0]);
      expect(component['scoreTextAnimation']).not.toHaveBeenCalled();
    });

    it('should animate goal for home', () => {
      component['processFootballScoreChanged']([1, 0], [0, 0]);
      expect(component['scoreTextAnimation']).toHaveBeenCalledWith(true);
    });

    it('should animate goal for away', () => {
      component['processFootballScoreChanged']([0, 1], [0, 0]);
      expect(component['scoreTextAnimation']).toHaveBeenCalledWith(true);
    });

    it('should animate correction for home', () => {
      component['processFootballScoreChanged']([0, 0], [1, 0]);
      expect(component['scoreTextAnimation']).toHaveBeenCalledWith(false);
    });

    it('should animate correction for away', () => {
      component['processFootballScoreChanged']([0, 0], [0, 1]);
      expect(component['scoreTextAnimation']).toHaveBeenCalledWith(false);
    });
  });

  describe('sets game points scores tests', () => {
    beforeEach(() => {
      component.event = {
        comments: {
          runningSetIndex: 2,
          runningGameScores: {
            id1: '30',
            id2: '40'
          },
          setsScores: {
            0: {
              id1: '2',
              id2: '3'
            },
            1: {
              id1: '3',
              id2: '4'
            }
          },
          teams: {
            player_1: {
              id: 'id1',
              score: '3'
            },
            player_2: {
              id: 'id2',
              score: '4'
            },
            home: {
              currentPoints: '15',
              periodScore: '3',
              score: '1'
            },
            away: {
              currentPoints: '40',
              periodScore: '4',
              score: '2'
            }
          }
        }
      } as any;
    });

    it('should return false if overall scores are not available', () => {
      component.event = {} as any;
      expect(component.getScore('home')).toBeFalsy();
    });
    it('should return score for chosen team alias for commentary data', () => {
      expect(component.getScore('home')).toEqual('3');
      expect(component.getScore('away')).toEqual('4');
    });
    it('should return score for chosen team alias for NON commentary data', () => {
      // @ts-ignore
      component.event.comments.setsScores = undefined;
      expect(component.getScore('home')).toEqual('1');
      expect(component.getScore('away')).toEqual('2');

    });
    it('should return false is set scores is not available', () => {
      component.event = {} as any;
      // @ts-ignore
      expect(component.getSetScores()).toBeFalsy();
    });
    it('should return index of current set', () => {
      expect(component.runningSetIndex).toEqual(2);
    });
    it('should correctly pick team alias when commentary data available', () => {
      // @ts-ignore
      expect(component.getTeamAlias('home')).toEqual('player_1');
      // @ts-ignore
      expect(component.getTeamAlias('away')).toEqual('player_2');
    });
    it('should correctly pick team alias when commentary data is NOT available', () => {
      // @ts-ignore
      component.event.comments.setsScores = undefined;
      // @ts-ignore
      expect(component.getTeamAlias('home')).toEqual('home');
      // @ts-ignore
      expect(component.getTeamAlias('away')).toEqual('away');
    });
    it('should return set game scores for commentary data for last set', () => {
      expect(component.getGamesScore('home')).toEqual('3');
      expect(component.getGamesScore('away')).toEqual('4');
    });
    it('should return set game scores for NON commentary data for last set', () => {
      expect(component.getGamesScore('home')).toEqual('3');
      expect(component.getGamesScore('away')).toEqual('4');
    });
    it('should return set current points for NON commentary data', () => {
      // @ts-ignore
      component.event.comments.setsScores = undefined;
      // @ts-ignore
      component.event.comments.runningGameScores = undefined;
      expect(component.currentPoints('home')).toEqual('15');
      expect(component.currentPoints('away')).toEqual('40');
    });
    it('should return set current points for commentary data', () => {
      expect(component.currentPoints('home')).toEqual('30');
      expect(component.currentPoints('away')).toEqual('40');
    });
  });

  describe('@scoreTextAnimation', () => {
    let element;

    beforeEach(() => {
      element = document.createElement('span');
      component.animatingComponentId = '500';
      spyOn(document, 'querySelector').and.returnValue(element);
    });

    it('should get odds card HTML element', () => {
      component['scoreTextAnimation'](true);

      expect(document.querySelector).toHaveBeenCalledWith('.cashout-odds-card.id-500');
      expect(component['renderer'].renderer.addClass).toHaveBeenCalledWith(element, 'goal-change');
    });

    it('should add class for goal animation', () => {
      component['scoreTextAnimation'](true);

      expect(component['renderer'].renderer.addClass).toHaveBeenCalledWith(element, 'goal-change');
    });

    it('should add class for correction animation', () => {
      component['scoreTextAnimation'](false);

      expect(component['renderer'].renderer.addClass).toHaveBeenCalledWith(element, 'correction-change');
    });

    it('should remove class after timeout', () => {
      component['scoreTextAnimation'](true);

      expect(windowRefStub.nativeWindow.setTimeout).toHaveBeenCalledWith(jasmine.any(Function), component.animationDelay - 500);
    });

    it('should remove class after goal animation', () => {
      component['scoreTextAnimation'](true);

      expect(component['renderer'].renderer.removeClass).toHaveBeenCalledWith(element, 'goal-change');
    });

    it('should remove class after correction animation', () => {
      component['scoreTextAnimation'](false);

      expect(component['renderer'].renderer.removeClass).toHaveBeenCalledWith(element, 'correction-change');
    });
  });
});
