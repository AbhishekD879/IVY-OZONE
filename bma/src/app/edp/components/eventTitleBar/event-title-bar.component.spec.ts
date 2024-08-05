import { EventTitleBarComponent } from '@edp/components/eventTitleBar/event-title-bar.component';
import { of } from 'rxjs';
import { IScoreType } from '@core/services/scoreParser/models/score-data.model';

describe('EventTitleBarComponent', () => {
  let component: EventTitleBarComponent;
  let CMS, freeBetsService, timeService, scoreParserServiceMock;

  beforeEach(() => {
    CMS = {
      getFeatureConfig: jasmine.createSpy('getFeatureConfig').and.returnValue(of({
        '16': true
      }))
    };
    freeBetsService = {
      isFreeBetVisible: jasmine.createSpy('isFreeBetVisible')
    };
    timeService = {
      formatByPattern: jasmine.createSpy('formatByPattern').and.returnValue('')
    };
    scoreParserServiceMock = {
      parseScores: jasmine.createSpy('parseScores'),
      getScoreType: jasmine.createSpy('getScoreType'),
    };

    component = new EventTitleBarComponent(scoreParserServiceMock, freeBetsService, timeService, CMS);

  });

  describe('@onInit', () => {
    beforeEach(() => {
      component['event'] = {
        startTime: 1540579500000
      } as any;
    });

    it('should get ScoreboardsSports config',  () => {
      component.sportname = 'football';
      component.isOutright = true;
      component.ngOnInit();

      expect(CMS.getFeatureConfig).toHaveBeenCalledWith('ScoreboardsSports', false, true);
    });

    it('should set pattern for football and outright events', () => {
      component.sportname = 'football';
      component.isOutright = true;
      component.ngOnInit();
      expect(timeService.formatByPattern).toHaveBeenCalledWith(new Date(component.event.startTime), 'HH:mm, d MMM');
      expect(component.eventStartDate).toBeDefined();
    });

    it('should set pattern for other sports and outright events', () => {
      component.sportname = 'tennis';
      component.isOutright = true;
      component.ngOnInit();
      expect(timeService.formatByPattern).toHaveBeenCalledWith(new Date(component.event.startTime), 'HH:mm, d MMM');
      expect(component.eventStartDate).toBeDefined();
    });

    it('should set pattern for football and not outright events', () => {
      component.sportname = 'football';
      component.ngOnInit();
      expect(timeService.formatByPattern).toHaveBeenCalledWith(new Date(component.event.startTime), 'EEEE, d-MMM-yy. HH:mm');
      expect(component.eventStartDate).toBeDefined();
    });

    it('should set pattern for other sports and not outright events', () => {
      component.sportname = 'tennis';
      component.ngOnInit();
      expect(timeService.formatByPattern).toHaveBeenCalledWith(new Date(component.event.startTime), 'EEEE, d-MMM-yy. HH:mm');
      expect(component.eventStartDate).toBeDefined();
    });

    it('should should show new event title bar template for football', () => {

      component.event.categoryId = '16';
      component.ngOnInit();
      expect(component.showNewTitleBar).toBeTruthy();
    });
  });

  it('should check isFreeBetVisible for event', () => {
    component.event = {} as any;
    component.ngOnInit();
    expect(freeBetsService.isFreeBetVisible).toHaveBeenCalledWith(component.event);
  });

  describe('@parseScores', () => {
    it('should call scoreParserService.parseScores with supplied event name and scoreboard type', () => {
      const eventName: string = 'foo';
      const scoreboardType: IScoreType = 'Simple';
      component['event'] = {} as any;
      component.parseScores(eventName, scoreboardType);

      expect(scoreParserServiceMock.parseScores).toHaveBeenCalledWith(eventName, scoreboardType);
    });
    it('should call scoreParserService.parseScores with supplied event name and scoreboard type', () => {
      const scoreboardType: IScoreType = 'Simple';
      const eventName: string = 'foo';
      component['event'] = {
        comments: {
          teams: {
            home: 'test',
            away: 'test1'
          }
        }
      } as any;
      const result = component.parseScores(eventName, scoreboardType);

      expect(result).toEqual(jasmine.objectContaining(component.event.comments.teams));
    });
  });

  describe('ngOnDestroy', () => {
    it('should unsubscribe from feature config', () => {
      (component['featureConfigSubscription'] as any) = {
        unsubscribe: jasmine.createSpy('unsubscribe')
      };
      component.ngOnDestroy();

      expect(component['featureConfigSubscription'].unsubscribe).toHaveBeenCalled();
    });

    it('should not unsubscribe from feature config', () => {
      (component['featureConfigSubscription'] as any) = undefined;
      component.ngOnDestroy();

      expect(component['featureConfigSubscription']).not.toBeDefined();
    });
  });
});

