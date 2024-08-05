import {
  BuildEventsWithScoresAndClockBsService
} from '@app/betHistory/services/cashoutDataProvider/builders/build-events-with-scores-and-clock-bs.service';

describe('BuildEventsWithScoresAndClockBsService', () => {
  let service;

  let commentServiceStub;
  let scoreParser: any;

  beforeEach(() => {
    commentServiceStub = {
      tennisInitParse: jasmine.createSpy().and.returnValue({}),
      footballClockInitParse: jasmine.createSpy().and.returnValue({}),
      extendWithScoreInfo: jasmine.createSpy('extendWithScoreInfo'),
      extendWithScoreType: jasmine.createSpy('extendWithScoreType')
    };
    scoreParser = {
      parseTypeAndScores: jasmine.createSpy('parseTypeAndScores').and.returnValue({})
    } as any;
    service = new BuildEventsWithScoresAndClockBsService(commentServiceStub as any, scoreParser as any);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('#build should call #addComments and #addClock', () => {
    spyOn(service, 'addClock');
    spyOn(service, 'addComments');

    const events = [{
      id: '5',
      categoryCode: ''
    }];

    const comments = {
      comments: { '1': {} }
    };

    service.build({events, comments});

    expect(service.addClock).toHaveBeenCalledWith(events, comments);
    expect(service.addComments).toHaveBeenCalledWith(events, comments);
  });

  it('#addComments should call commentsService.tennisInitParse', () => {
    const events = [{
      id: '5',
      categoryCode: 'tennis'
    }];

    const callWithParams = {
      eventId: '7'
    };

    const comments = {
      '5': callWithParams
    };

    service.addComments(events, comments);
    expect(commentServiceStub.tennisInitParse).toHaveBeenCalledWith(callWithParams);
  });

  it('#addComments should call try to parse sport name ' +
    'if parser no found', () => {
    const events = [{
      id: '5',
      categoryCode: 'SNOOKER',
      originalName: 'Player1 10 - 10 Player 2'
    }];

    const callWithParams = {
      eventId: '7'
    };

    const commentsWithEvent = {
      '5': callWithParams
    };

    const commentsWithoutEvent = {
      '8': callWithParams
    };

    service.addComments([], commentsWithEvent);
    service.addComments(events, commentsWithoutEvent);
    service.addComments(events, commentsWithEvent);

    expect(scoreParser.parseTypeAndScores).toHaveBeenCalledWith('Player1 10 - 10 Player 2', 'SNOOKER');
  });

  it('#addClock should be called commentsService.footballClockInitParse with correct params', () => {
    const events = [{
      id: '5',
      categoryCode: 'football',
      startTime: '1542041677527',
      responseCreationTime: '1542041713330'
    }];

    const callWithParams = {
      eventId: '7'
    };

    const comments = {
      '5': callWithParams
    };

    service.addClock(events, comments);
    expect(commentServiceStub.footballClockInitParse).toHaveBeenCalledWith(
      callWithParams,
      events[0].categoryCode,
      events[0].startTime,
      events[0].responseCreationTime
    );
  });

  it('#addClock should NOT call commentsService.footballClockInitParse', () => {
    const events = [{
      id: '5',
      categoryCode: 'testCategory'
    }];

    const callWithParams = {
      eventId: '7'
    };

    const commentsWithEvent = {
      '5': callWithParams
    };

    const commentsWithoutEvent = {
      '8': callWithParams
    };

    service.addClock([], commentsWithoutEvent);
    service.addClock(events, commentsWithEvent);
    service.addClock(events, commentsWithEvent);
    expect(commentServiceStub.footballClockInitParse).not.toHaveBeenCalled();
  });
});
