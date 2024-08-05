import { fakeAsync, flush } from '@angular/core/testing';

import { WatchRulesService } from '@lazy-modules/eventVideoStream/services/watchRules/watch-rules.service';

describe('WatchRulesService', () => {
  let service: WatchRulesService;

  let awsService;

  beforeEach(() => {

    awsService = {
      addAction: jasmine.createSpy('addAction')
    };

    service = new WatchRulesService(awsService);
  });


  it('@isInactiveUser: should check if user is inactive', () => {
    const actualResult = service.isInactiveUser('deniedByInactiveWatchRules');
    expect(actualResult).toBeTruthy();
  });

  describe('getFailureReason', () => {
    it('should return deniedByWatchRules code', () => {
      const actualResult = service['getFailureReason']('8502');
      expect(actualResult).toEqual('deniedByWatchRules');
    });

    it('should return deniedByInactiveWatchRules code', () => {
      const actualResult = service['getFailureReason']('4105');
      expect(actualResult).toEqual('deniedByInactiveWatchRules');
    });

    it('should return streamIsNotAvailable code', () => {
      const actualResult = service['getFailureReason']('11111');
      expect(actualResult).toEqual('streamIsNotAvailable');
    });

    it('should return streamIsNotAvailable code', () => {
      const actualResult = service['getFailureReason'](null);
      expect(actualResult).toEqual('streamIsNotAvailable');
    });
  });

  describe('canWatchEvent', () => {
    let providerInfo: any;
    let successHandler;
    let errorHandler;

    beforeEach(() => {
      successHandler = jasmine.createSpy('successHandler');
      errorHandler = jasmine.createSpy('errorHanler');
    });

    it(`should return null if it is not ['21', '19', '151'] category`, fakeAsync(() => {
      providerInfo = { priorityProviderName: 'Perform' };

      service.canWatchEvent(providerInfo, '2', 111).subscribe(successHandler, errorHandler);
      flush();

      expect(successHandler).toHaveBeenCalledWith(null);
    }));

    it(`should return provider info if priorityProviderName`, fakeAsync(() => {
      providerInfo = { priorityProviderName: 'Perform' };

      service.canWatchEvent(providerInfo, '21', 111).subscribe(successHandler, errorHandler);
      flush();

      expect(successHandler).toHaveBeenCalledWith(providerInfo);
    }));

    describe(`should return 'streamIsNotAvailable' error`, () => {
      it(`if providerInfo do not have details and priorityProviderName`, () => {
        providerInfo = {};
      });

      it(`if providerInfo.details do not have failureCode`, () => {
        providerInfo = { details: {} };
      });

      it(`if IGM_CONSTANT.FAILURE_ERROR do Not include failureCode`, () => {
        providerInfo = { details: { failureCode: '1234' } };
      });

      afterEach(fakeAsync(() => {
        service.canWatchEvent(providerInfo, '21', 111).subscribe(successHandler, errorHandler);
        flush();

        expect(errorHandler).toHaveBeenCalledWith('streamIsNotAvailable');
      }));
    });

    it(`should return 'deniedByWatchRules' error if IGM_CONSTANT.FAILURE_ERROR include failureCode`,
      fakeAsync(() => {
        providerInfo = { details: { failureCode: '8502' } };
        service.canWatchEvent(providerInfo, '21', 111).subscribe(successHandler, errorHandler);
        flush();

        expect(errorHandler).toHaveBeenCalledWith('deniedByWatchRules');
        expect(awsService.addAction).toHaveBeenCalledWith('STREAM_QUALIFICATION_ERROR', jasmine.objectContaining({
          eventId: 111,
          qualificationErrorCode: '8502',
          errorMessageCode: 'deniedByWatchRules'
        }));
      }));
  });

  describe('@sendAwsData', () => {
    it('should send to AWS eventId, qualificationErrorCode and errorMessageCode', () => {
      service['sendAwsData'](111, '4105', 'deniedByInactiveWatchRules');

      expect(awsService.addAction).toHaveBeenCalledWith('STREAM_QUALIFICATION_ERROR', jasmine.objectContaining({
        eventId: 111,
        qualificationErrorCode: '4105',
        errorMessageCode: 'deniedByInactiveWatchRules'
      }));
    });
  });

  describe('shouldShowCSBIframe', () => {
    let eventEntity;
    let performConfig;

    beforeEach(() => {
      eventEntity = { streamProviders: { Perform: true, RacingUK: false }, sportId: '21' };
      performConfig = { CSBIframeEnabled: true, CSBIframeSportIds: '21,3' };
    });
    describe('should return false', () => {
      it(`if streamProviders is Not Perform`, () => {
        eventEntity.streamProviders.Perform = false;
      });

      it(`if No performConfig`, () => {
        performConfig = undefined;
      });

      it(`if future is off`, () => {
        performConfig.CSBIframeEnabled = false;
      });

      it(`if No CSBIframeSportIds`, () => {
        performConfig.CSBIframeSportIds = undefined;
      });

      it(`if sportId in CSBIframeSportIds`, () => {
        performConfig.CSBIframeSportIds = '3';
      });
      afterEach(() => {
        expect(service.shouldShowCSBIframe(eventEntity, performConfig)).toBeFalsy();
      });
    });

    it(`should return true`, () => {
      expect(service.shouldShowCSBIframe(eventEntity, performConfig)).toBeTruthy();
    });

    it(`should return true`, () => {
      eventEntity.streamProviders.Perform = false;
      eventEntity.streamProviders.RacingUK = true;
      expect(service.shouldShowCSBIframe(eventEntity, performConfig)).toBeTruthy();
    });

    it(`should return true if racingUK is true`, () => {
      eventEntity.streamProviders.RacingUK = true;
      expect(service.shouldShowCSBIframe(eventEntity, performConfig)).toBeTruthy();
    });
  });
});
