

import { of } from 'rxjs';
import { AWSFirehoseConnectService } from '@lazy-modules/awsFirehose/service/aws-firehose-connect.service';
import { COGNITO_CREDENTIALS, CONFIG } from '@lazy-modules/awsFirehose/test/data/awsFirehose.mock';

describe('AWSFirehoseConnectService', () => {
  let service: AWSFirehoseConnectService,
    windowRef,
    asyncScriptLoaderFactory,
    pubSubService;
  beforeEach(() => {
    windowRef = {
      nativeWindow: {
        document: {
          cookie: 'cookie'
        },
        AWS: {
          CognitoIdentityCredentials: jasmine.createSpy().and.returnValue(COGNITO_CREDENTIALS),
          config: CONFIG
        },
      }
    };
    asyncScriptLoaderFactory = {
      loadJsFile: jasmine.createSpy().and.returnValue(of(null))
    };
    pubSubService = {
      publish: jasmine.createSpy('publish'),
      API: {
        APP_IS_LOADED: 'APP_IS_LOADED',
        INIT_AWS: 'INIT_AWS'
      },
      subscribe: jasmine.createSpy('subscribe').and.callFake((a, b, callback) => callback())
    };
    service = new AWSFirehoseConnectService(windowRef, asyncScriptLoaderFactory, pubSubService);
  });

  it('constructor', () => {
    spyOn<any>(service, 'intializeAWS');
    expect(pubSubService.subscribe).toHaveBeenCalledWith('awsconnect_bmaloaded', pubSubService.API.APP_IS_LOADED, jasmine.any(Function));
  });
  describe('intializeAWS', () => {
    it('intializeAWS', () => {
      asyncScriptLoaderFactory.loadJsFile('/assets/aws-sdk-firehose/aws-sdk-firehose.js')
        .subscribe(() => {
          spyOn<any>(service, 'refreshAwsToken');
          windowRef.nativeWindow.AWS.config.region = CONFIG.region;
          windowRef.nativeWindow.AWS.config.credentials.needsRefresh = jasmine.createSpy().and.returnValue(true);
          service['intializeAWS']();
          expect(windowRef.nativeWindow.AWS.config.region).toEqual('eu-west-2');
          expect(service['refreshAwsToken']).toHaveBeenCalled();
          expect(windowRef.nativeWindow.AWS.config.IdentityPoolId).toEqual('jdukjlcdfhkjds');
        });
    });

    it('not intializeAWS', () => {
      spyOn<any>(service, 'refreshAwsToken');
      windowRef.nativeWindow.AWS = undefined;
      service['intializeAWS']();
      expect(service['refreshAwsToken']).not.toHaveBeenCalled();
    });
  });
  describe('publishAWSLoaded', () => {
    it('should publish AWS initialisation', () => {
      windowRef.nativeWindow.AWS.config.credentials.expired = false;
      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.INIT_AWS);
    });
    it('should not publish AWS initialisation', () => {
      windowRef.nativeWindow.AWS.config.credentials.expired = true;
      service['publishAWSLoaded']();
    });
  });
  describe('refreshAwsToken', () => {
    it('should call refreshAwsToken', () => {
      spyOn<any>(service, 'publishAWSLoaded');
      windowRef.nativeWindow.AWS.config.credentials.needsRefresh = jasmine.createSpy().and.returnValue(true);
      windowRef.nativeWindow.AWS.config.credentials.get = jasmine.createSpy();
      windowRef.nativeWindow.AWS.config.credentials.refresh = jasmine.createSpy();
      service['refreshAwsToken']();
      service['publishAWSLoaded']();
      expect(service['publishAWSLoaded']).toHaveBeenCalled();
      expect(windowRef.nativeWindow.AWS.config.credentials.get).toHaveBeenCalled();
      expect(windowRef.nativeWindow.AWS.config.credentials.refresh).toHaveBeenCalled();
    });
    it('should not call refreshAwsToken', () => {
      spyOn<any>(service, 'publishAWSLoaded');
      windowRef.nativeWindow.AWS.config.credentials.needsRefresh = jasmine.createSpy().and.returnValue(false);
      windowRef.nativeWindow.AWS.config.credentials.get = jasmine.createSpy();
      windowRef.nativeWindow.AWS.config.credentials.refresh = jasmine.createSpy();
      expect(service['publishAWSLoaded']).not.toHaveBeenCalled();
      expect(windowRef.nativeWindow.AWS.config.credentials.get).not.toHaveBeenCalled();
      expect(windowRef.nativeWindow.AWS.config.credentials.refresh).not.toHaveBeenCalled();
    });
  });
});
