import {MatchCreateComponent} from './match-create.component';

describe('MatchCreateComponent', () => {
  let component,
    bigCompetitionApiService,
    data,
    dialogRef;

  beforeEach(() => {
    bigCompetitionApiService = {};
    data = {
      knockoutModuleData: {
        rounds: [{
          name: 'mockName'
        }],
        events: [{
          name: 'eventName'
        }]
      }
    };
    dialogRef = {};

    component = new MatchCreateComponent(
      bigCompetitionApiService,
      data,
      dialogRef
    );

    component.dateTimeComponent = {
      setDayTime: jasmine.createSpy('setDayTime')
    };

    component.ngOnInit();
  });

  it('should Initialise', () => {
    expect(component.initialDate).toBeDefined();
    expect(component.form).toBeDefined();
    expect(component.dateTimeComponent.setDayTime).toHaveBeenCalled();
  });
});
