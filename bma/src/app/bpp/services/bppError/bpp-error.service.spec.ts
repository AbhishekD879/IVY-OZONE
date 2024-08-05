import { BppErrorService } from '@app/bpp/services/bppError/bpp-error.service';
import { DialogService } from '@core/services/dialogService/dialog.service';
import { BppErrorDialogComponent } from '@sharedModule/components/bppErrorDialog/bpp-error-dialog.component';
import { IErrorResponse } from '@app/bpp/services/bppError/bpp-error.model';

describe('BPP Error Service', () => {
  let service: BppErrorService,
    dialogServiceStub,
    response,
    parsedError;

  beforeEach(() => {
    response = {
        data: {
          code: 101,
          status: 'BAD_REQUEST'
        },
        config: {
          url: 'testUrl'
        },
        error: {
          error: 'Timeout'
        }
      } as any;

    parsedError = {
        code: '01',
        msg: 'testUrl\nError occured by Pirozhok Proxy. Reason: Bad request from the application.'
      };

    dialogServiceStub = {
     openDialog: jasmine.createSpy()
    };

    service = new BppErrorService(dialogServiceStub);
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  it('should test errorDataParser method', () => {
    expect(service.errorDataParser(response)).toEqual(parsedError);
    response.data.status = 'testStatus';
    parsedError.msg = 'testUrl\nError occured by Pirozhok Proxy. Reason: testStatus';
    expect(service.errorDataParser(response)).toEqual(parsedError);
  });

  it('should testerrorHandler happy flow', () => {
    spyOn(service, 'errorDataParser').and.returnValue( { msg: '' } as any);
    service.errorHandler(response);
    expect(service.errorDataParser).toHaveBeenCalledWith(response);
  });

  it('should test errorHandler fail flow', () => {
    spyOn(service, 'errorDataParser').and.returnValue( { msg: '' } as any);
    service.errorHandler(false as any);
    expect(service.errorDataParser).not.toHaveBeenCalled();
    service.errorHandler({data: false, config: true} as any);
    expect(service.errorDataParser).not.toHaveBeenCalled();
    service.errorHandler({data: true, config: false} as any);
    expect(service.errorDataParser).not.toHaveBeenCalled();
  });

  describe('showPopup method', () => {
    it('should handle response object', () => {
      const defaultErrorKey = 'betPlacementError';
      response.error = '';
      service.showPopup(response);
      expect(dialogServiceStub.openDialog).toHaveBeenCalledWith(DialogService.API.bppErrorDialog, BppErrorDialogComponent, true,
        { error: defaultErrorKey });

      response.data.error = 'Connection timeout';
      service.showPopup(response);
      expect(dialogServiceStub.openDialog).toHaveBeenCalledWith(DialogService.API.bppErrorDialog, BppErrorDialogComponent, true,
        { error: 'betPlacementTimeoutError' });
    });

    it('should handle response object with error', () => {
      response.error.error = 'Connection timeout';
      service.showPopup(response);
      expect(dialogServiceStub.openDialog).toHaveBeenCalledWith(DialogService.API.bppErrorDialog, BppErrorDialogComponent, true,
        { error: 'betPlacementTimeoutError' });
    });

    it('should open dialog with default error key #1', () => {
      const defaultErrorKey = 'betPlacementError';

      service.showPopup(defaultErrorKey as string);
      expect(dialogServiceStub.openDialog).toHaveBeenCalledWith(DialogService.API.bppErrorDialog, BppErrorDialogComponent, true,
        { error: defaultErrorKey });
    });

    it('should open dialog with default error key #2', () => {
      const defaultErrorKey = 'betPlacementError';
      const errorResponse = {
        data: {
          error: 'Some error'
        }
      };

      service.showPopup(errorResponse as IErrorResponse);
      expect(dialogServiceStub.openDialog).toHaveBeenCalledWith(DialogService.API.bppErrorDialog, BppErrorDialogComponent, true,
        { error: defaultErrorKey });
    });

    it('should handle string argument', () => {
      const errorKey = 'openBetError';

      service.showPopup(errorKey);
      expect(dialogServiceStub.openDialog).toHaveBeenCalledWith(DialogService.API.bppErrorDialog, BppErrorDialogComponent, true,
        { error: errorKey });
    });
  });

  afterEach(() => {
    service = null;
  });
});
