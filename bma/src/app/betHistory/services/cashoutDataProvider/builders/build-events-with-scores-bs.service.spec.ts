import {
  BuildEventsWithScoresBsService
} from '@app/betHistory/services/cashoutDataProvider/builders/build-events-with-scores-bs.service';

describe('BuildEventsWithScoresBsService', () => {
  let service;

  let filtersServiceStub;
  let siteServerRequestHelperServiceStub;

  beforeEach(() => {
    filtersServiceStub = {
      removeLineSymbol: jasmine.createSpy().and.returnValue('testRemoveLineSymbol')
    };

    const commentsByEventsIds = new Promise((resolve, reject) => {
      const lastPeriod = [
        {
          eventFact: {
            eventParticipantId: '19',
            fact: '12'
          }
        },
        {
          eventFact: {
            eventParticipantId: '25',
            fact: '31'
          }
        }
      ];
      const periods = [
        {
          eventFact: {
            eventParticipantId: '121',
            fact: '127'
          },
          eventPeriod: {
            children: lastPeriod,
            periodIndex: '5'
          }
        },
        {
          eventFact: {
            eventParticipantId: '37',
            fact: '31'
          },
          eventPeriod: {
            children: lastPeriod,
            periodIndex: '12'
          }
        }
      ];
      const comments = [
        {
          eventParticipant: {
            name: 'ParticipantName1'
          },
          eventPeriod: {
            children: periods
          }
        },
        {
          eventParticipant: {
            name: 'ParticipantName2'
          },
          eventPeriod: {
            children: periods
          }
        }
      ];
      const event = {
        children: comments
      };
      const result = {
        SSResponse: {
          children: [{
            event
          }]
        }
      };
      resolve(result);
    });
    siteServerRequestHelperServiceStub = {
      getCommentsByEventsIds: jasmine.createSpy().and.returnValue(commentsByEventsIds)
    };

    service = new BuildEventsWithScoresBsService(siteServerRequestHelperServiceStub, filtersServiceStub);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('#build should call #isSportWithScoresByRequest', () => {
    spyOn(service, 'isSportWithScoresByRequest');
    const event = {
      categoryCode: 'BADMINTON'
    };
    service.build(event);
    expect(service.isSportWithScoresByRequest).toHaveBeenCalledWith(event);
  });

  it('#build should call #scoresExtension', () => {
    spyOn(service, 'scoresExtension');
    const event = {
      categoryCode: 'BADMINTON'
    };
    service.build(event);
    expect(service.scoresExtension).toHaveBeenCalledWith(event);
  });

  it('#scoresExtension should call siteServerRequestHelperService.getCommentsByEventsIds', () => {
    const event = {
      id: '4'
    };
    const expectedParams = {
      eventsIds: '4'
    };
    service.scoresExtension(event);
    expect(siteServerRequestHelperServiceStub.getCommentsByEventsIds).toHaveBeenCalledWith(expectedParams);
  });

  it('#scoreExtension should call filtersService.removeLineSymbol', () => {
    const event = {
      id: '7'
    };

    const resultEvent = {
      id: '7',
      comments: {
        teams:
          {
            away: {
              currentPoints: '31',
              name: 'testRemoveLineSymbol',
              score: '31'
            },
            home: {
              currentPoints: '12',
              name: 'testRemoveLineSymbol',
              score: '127'
            }
          }
      }
    };

    service.scoresExtension(event).subscribe((res) => {
      expect(res).toEqual(resultEvent);
    });
  });

  it('should not create comments if comments array is empty', () => {
    siteServerRequestHelperServiceStub.getCommentsByEventsIds.and.returnValue(Promise.resolve({
      SSResponse: {
        children: [{
          event: {
            children: []
          }
        }]
      }
    }));

    service.scoresExtension({id: '100'} as any).subscribe();

    expect(siteServerRequestHelperServiceStub.getCommentsByEventsIds).toHaveBeenCalled();
    expect(filtersServiceStub.removeLineSymbol).not.toHaveBeenCalled();
  });

  it('should not create comments if comments is not array', () => {
    siteServerRequestHelperServiceStub.getCommentsByEventsIds.and.returnValue(Promise.resolve({
      SSResponse: {
        children: [{
          event: {
            children: 500
          }
        }]
      }
    }));

    service.scoresExtension({id: '100'} as any).subscribe();

    expect(siteServerRequestHelperServiceStub.getCommentsByEventsIds).toHaveBeenCalled();
    expect(filtersServiceStub.removeLineSymbol).not.toHaveBeenCalled();
  });
});
