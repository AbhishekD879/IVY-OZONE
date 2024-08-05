import {  JackpotPoolLegListComponent } from './jackpot-pool-leg-list.component';
import FootballJackpotBet from '../../betModels/footballJackpotBet/football-jackpot-bet.class';
import { ILeg } from '@betslip/services/models/bet.model';

describe(' JackpotPoolLegListComponent', () => {
  let component:  JackpotPoolLegListComponent,
  localeService,
  timeService,
  filtersService;

  beforeEach(() => {
    localeService = {
      getString: jasmine.createSpy('getString').and.callFake(x => x)
    };

    timeService = {
      getLocalDateFromString: jasmine.createSpy('getLocalDateFromString'),
    };

    filtersService = {
      orderBy: jasmine.createSpy(),
      date: jasmine.createSpy('date').and.callFake((x, y) => y)
    };

    component = new JackpotPoolLegListComponent(
      localeService,
      timeService,
      filtersService
    );

    component.pool = { id: '1', legs: [] } as FootballJackpotBet;
    component.ngOnInit();
  });

  it('should init component ', () => {
    expect(component).toBeTruthy();
    expect(filtersService.orderBy).toHaveBeenCalled();
    expect(localeService.getString).toHaveBeenCalledWith('bethistory.today');
  });

  it('trackById should return a string', () => {
    const mockLeg = { id: '1', documentId: '2'} as ILeg;
    const result = component.trackById(1, mockLeg);

    expect(result).toBe('1');
  });

  describe('getEventStartTime', () => {
    it('should return start date in format "dd MMM, h:mm a" format if start time is not today', () => {
      const leg = {
        startTime: '2011-10-05T14:48:00.000Z'
      };
      const startTime = new Date (leg.startTime);
      timeService.getLocalDateFromString.and.returnValue(startTime);
      expect(component.getEventStartTime(leg as any)).toEqual('dd MMM, h:mm a');
      expect(filtersService.date).toHaveBeenCalledWith(startTime, 'dd MMM, h:mm a');
      expect(timeService.getLocalDateFromString).toHaveBeenCalledWith('2011-10-05 14:48:00.000Z');
    });
    it('should return start date in format "today, h:mm a" format if start time is today', () => {
      const leg = {
        startTime: '2011-10-05T14:48:00.000Z'
      };
      const todayStartTime = new Date ();
      timeService.getLocalDateFromString.and.returnValue(todayStartTime);
      expect(component.getEventStartTime(leg as any)).toEqual('bethistory.today, h:mm a');
      expect(filtersService.date).toHaveBeenCalledWith(todayStartTime, 'h:mm a');
      expect(timeService.getLocalDateFromString).toHaveBeenCalledWith('2011-10-05 14:48:00.000Z');
    });
  });
});
