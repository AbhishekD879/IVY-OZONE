import { EventHubService } from './event-hub.service';

describe('EventHubService', () => {
  let service: EventHubService;
  let apiClientService;

  beforeEach(() => {
    apiClientService = {
      eventHub: jasmine.createSpy('eventHub').and.returnValue({
        getAllEventHubs: jasmine.createSpy('getAllEventHubs'),
        getEventHubById: jasmine.createSpy('getEventHubById'),
        postNewEventHub: jasmine.createSpy('postNewEventHub'),
        updateEventHub: jasmine.createSpy('updateEventHub')
      })
    };

    service = new EventHubService(apiClientService);
  });

  it('getHubList', () => {
    service.getHubList();

    expect(apiClientService.eventHub().getAllEventHubs).toHaveBeenCalled();
  });

  it('getHubData', () => {
    service.getHubData('mockId');

    expect(apiClientService.eventHub().getEventHubById).toHaveBeenCalledWith('mockId');
  });

  it('createHub', () => {
    const hubData = { title: '' } as any;

    service.createHub(hubData);

    expect(apiClientService.eventHub().postNewEventHub).toHaveBeenCalledWith(hubData);
  });

  it('updateHubData', () => {
    const hubData = { title: '' } as any;

    service.updateHubData(hubData);

    expect(apiClientService.eventHub().updateEventHub).toHaveBeenCalledWith(hubData);
  });
});
