import {NexteventsIndividualComponent} from './nextevents-individual.component';
import { of } from 'rxjs';

describe('NexteventsIndividualComponent', () => {
  let component,
    bigCompetitionAPIService,
    snackBar;
  const validMock = ['11111'];

  beforeEach(() => {
    bigCompetitionAPIService = {
      getSiteServeEvents: jasmine.createSpy('getSiteServeEvents').and.returnValue(of({
         body: {
           valid: validMock,
           invalid: ['2222']
         }
      }))
    };

    snackBar = {};

    component = new NexteventsIndividualComponent(
      bigCompetitionAPIService,
      snackBar
    );

    component.module = {
      eventIds: ['11111']
    };

    component.ngOnInit();
  });

  it('should create', () => {
    expect(component.eventIdIsValid).toBeTruthy();
    expect(component.events).toEqual(validMock);
    expect(component.invalidEventIds).toBeDefined();
  });
});
