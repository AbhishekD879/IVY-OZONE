import { OddsCardResultComponent } from './odds-card-result.component';

describe('OddsCardResultComponent', () => {
  let component: OddsCardResultComponent;

  beforeEach(() => {
    component = new OddsCardResultComponent(
    );
  });

  it('should handle no goal scorers received', () => {
    component.event = {
      teamA: {
      },
      teamB: {
      }
    } as any;
    component.ngOnInit();
    expect(component.event.teamA.parsedGoalScorers as any).toEqual([]);
    expect(component.event.teamB.parsedGoalScorers as any).toEqual([]);
  });
  it('should parse galscorers', () => {
    component.event = {
      teamA: {
        goalScorers: 'Player1, Player2'
      },
      teamB: {
        goalScorers: 'Player3, Player4'
      }
    } as any;
    component.ngOnInit();
    expect(component.event.teamA.parsedGoalScorers as any).toEqual(['Player1', 'Player2']);
    expect(component.event.teamB.parsedGoalScorers as any).toEqual(['Player3', 'Player4']);
  });
});
