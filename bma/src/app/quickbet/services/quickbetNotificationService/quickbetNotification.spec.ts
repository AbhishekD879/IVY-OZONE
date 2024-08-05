import { pubSubApi } from '@app/core/services/communication/pubsub/pubsub-api.constant';
import { QuickbetNotificationService  } from './quickbet-notification.service';

describe('QuickbetNotificationService', () => {
  let service;
  let pubSubService;

  beforeEach(() => {
    pubSubService = {
      publish: jasmine.createSpy('publish'),
      API: pubSubApi
    };

    service = new QuickbetNotificationService(pubSubService);
    spyOn(service, 'publishQuickbetInfoPanel').and.callThrough();
  });

  it('Should return message config', () => {
    expect(service.config).toEqual({
      msg: '',
      type: '',
      location: ''
    });
  });

  it('Should save error message', () => {
    service.saveErrorMessage('test', 'error', 'test');

    expect(service.config).toEqual({
      msg: 'test',
      type: 'error',
      location: 'test',
      errorCode: ''
    });
    expect(service['publishQuickbetInfoPanel']).toHaveBeenCalled();
  });

  it('Should save error message and empty location string', () => {
    service.saveErrorMessage('test', undefined, undefined);

    expect(service.config).toEqual({
      msg: 'test',
      type: 'warning',
      location: '',
      errorCode: ''
    });
    expect(service['publishQuickbetInfoPanel']).toHaveBeenCalled();
  });

  it('Should save error message and set default type and location', () => {
    service.saveErrorMessage('test');

    expect(service.config).toEqual({
      msg: 'test',
      type: 'warning',
      location: '',
      errorCode: ''
    });
    expect(service['publishQuickbetInfoPanel']).toHaveBeenCalledWith();
  });

  it('Should clear error message', () => {
    service.clear();

    expect(service['publishQuickbetInfoPanel']).toHaveBeenCalled();
    expect(service.config).toEqual({
      msg: '',
      type: '',
      location: '',
      errorCode: ''
    });
  });

  it('should clear with custom location', () => {
    service.clear('quick-deposit');

    expect(service['publishQuickbetInfoPanel']).toHaveBeenCalled();
    expect(service.config).toEqual({
      msg: '',
      type: '',
      location: 'quick-deposit',
      errorCode: ''
    });
  });

  it('saveErrorMessageWithCode', () => {
    spyOn(service, 'updateModel');
    service.saveErrorMessageWithCode('', '', '', 'STAKE_TOO_LOW');

    expect(service['publishQuickbetInfoPanel']).toHaveBeenCalled();
    expect(service['updateModel']).toHaveBeenCalled();
  });

  it('@publishQuickbetInfoPanel', () => {
    service['publishQuickbetInfoPanel']();

    expect(pubSubService.publish).toHaveBeenCalled();
  });
});
