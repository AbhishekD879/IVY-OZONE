import { YourCallNotificationService } from '@yourcall/services/yourCallNotification/yourcall-notification.service';
import { commandApi } from '@core/services/communication/command/command-api.constant';

describe('YourCallNotificationService', () => {
  let service: YourCallNotificationService;
  let commandService: any;

  beforeEach(() => {
    commandService = {
      API: commandApi,
      executeAsync: jasmine.createSpy('executeAsync')
    };

    service = new YourCallNotificationService(commandService);
  });

  it('should create', () => {
    expect(service).toBeTruthy();
  });

  it('saveErrorMessage should return correct promise result', () => {
    service.saveErrorMessage('message', 'some type');

    expect(commandService.executeAsync).toHaveBeenCalled();
  });

  it('clear should return correct promise result', () => {
    service.clear();
    expect(commandService.executeAsync).toHaveBeenCalled();
  });
});
