import {
  EventVideoStreamProviderService
} from '@lazy-modules/eventVideoStream/components/eventVideoStream/event-video-stream-provider.service';
import { of as observableOf } from 'rxjs';

describe('EventVideoStreamProviderService', () => {
  let service;
  let subscriber;
  let cmsService;

  beforeEach(() => {
    subscriber = jasmine.createSpy('subscriber');
    cmsService = {
      getFeatureConfig:jasmine.createSpy('getFeatureConfig').and.returnValue(observableOf({
      enabled: true
      }))
    };

    service = new EventVideoStreamProviderService(cmsService);
  });

  it('should return playListener', () => {
    service.playListener.subscribe(subscriber);
    service.playListener.next();

    expect(subscriber).toHaveBeenCalled();
  });

  it('should return playSuccessErrorListener', () => {
    service.playSuccessErrorListener.subscribe(subscriber);
    service.playSuccessErrorListener.next(true);

    expect(subscriber).toHaveBeenCalledWith(true);
  });

  it('should return showHideStreamListener', () => {
    service.showHideStreamListener.subscribe(subscriber);
    service.showHideStreamListener.next(false);

    expect(subscriber).toHaveBeenCalledWith(false);
  });

  it('should return isStreamBetAvailable value', () => {
    const streamBetConfig = {
      categoryId: '21',
      providerInfo: {
        priorityProviderName:'ATR'
      },
      isMyBets: false,      
      streamBetCmsConfig: {
        enabled: true,
        sportIds: ['16', '21'],
        streamProviders: ['ATR']        
      }
    };
    expect(service.isStreamBetAvailable(streamBetConfig, 'EventVideoStreamComponent')).toBeFalsy();
  });

  it('should return isStreamBetAvailable value#2', () => {
    const streamBetConfig = {
      categoryId: '21',
      providerInfo: {
        priorityProviderName:'ATR'
      },
      isMyBets: false,
      isHR: true,
      streamBetCmsConfig: {
        enabled: true,
        sportIds: ['16', '21'],
        streamProviders: ['ATR']        
      }
    };
    expect(service.isStreamBetAvailable(streamBetConfig, 'racingEventMain')).toBeFalsy();
  });

  it('should return isStreamBetAvailable value#3', () => {
    const streamBetConfig = {
      categoryId: '21',
      providerInfo: {
        priorityProviderName:'ATR'
      },
      isMyBets: false,
      isHR: true,
      streamBetCmsConfig: undefined
    };
    expect(service.isStreamBetAvailable(streamBetConfig, 'EventVideoStreamComponent')).toBeFalsy();
  });

  it('should return isStreamBetAvailable value#4', () => {
    const streamBetConfig = {
      categoryId: '21',
      providerInfo: {
        priorityProviderName:'ATR'
      },
      isMyBets: false,
      isHR: true,
      streamBetCmsConfig: undefined
    };
    expect(service.isStreamBetAvailable(streamBetConfig, 'racingEventMain')).toBeFalsy();
  });

  it('should return isStreamBetAvailable value#5', () => {
    const streamBetConfig = {
      categoryId: '21',
      providerInfo: {
        priorityProviderName:'ATR'
      },
      isMyBets: false,
      isHR: true,
      isTablet: false,
      isDesktop: false,
      streamBetCmsConfig: {
        enabled: true,
        sportIds: undefined,
        streamProviders: ['ATR']        
      }
    };
    expect(service.isStreamBetAvailable(streamBetConfig, 'racingEventMain')).toBeFalsy();
  });

  it('should return isStreamBetAvailable value#6', () => {
    const streamBetConfig = {
      categoryId: '21',
      providerInfo: {
        priorityProviderName: undefined
      },
      isMyBets: false,
      isHR: true,
      isTablet: false,
      isDesktop: false,
      streamBetCmsConfig: {
        enabled: true,
        sportIds: undefined,
        streamProviders: ['ATR']        
      }
    };
    expect(service.isStreamBetAvailable(streamBetConfig, 'racingEventMain')).toBeFalsy();
  });

  it('should return isStreamBetAvailable value#7', () => {
    const streamBetConfig = {
      categoryId: '21',
      providerInfo: {
        priorityProviderName:'ATR'
      },
      isMyBets: false,  
      isMobile: true,  
      providerInfoAvailable: true,  
      streamBetCmsConfig: {
        enabled: true,
        sportIds: ['16', '21'],
        streamProviders: ['ATR']        
      }
    };
    expect(service.isStreamBetAvailable(streamBetConfig, 'EventVideoStreamComponent')).toBeTruthy();
  });

  it('should return isStreamBetAvailable value#8', () => {
    const streamBetConfig = {
      categoryId: '21',
      providerInfo: {
        priorityProviderName:'ATR'
      },
      isMyBets: false,  
      isMobile: true,  
      providerInfoAvailable: true,  
      isIHR: true,
      streamBetCmsConfig: {
        enabled: true,
        sportIds: ['16', '21'],
        streamProviders: ['ATR']        
      }
    };
    expect(service.isStreamBetAvailable(streamBetConfig, 'racingEventMain')).toBeTruthy();
  });

  it('should return isStreamBetAvailable value#9', () => {
    const streamBetConfig = {
      categoryId: '21',
      providerInfo: {
        priorityProviderName:'ATR'
      },
      isMyBets: false,  
      isMobile: true,  
      providerInfoAvailable: true,  
      isHR: true,
      streamBetCmsConfig: {
        enabled: true,
        sportIds: ['16', '21'],
        streamProviders: ['ATR']        
      }
    };
    expect(service.isStreamBetAvailable(streamBetConfig, 'racingEventMain1')).toBeTruthy();
  });

  it('should return isStreamBetAvailable value#10', () => {
    const streamBetConfig = {
      categoryId: '21',
      providerInfo: 'ATR',
      isMyBets: false,  
      isMobile: true,  
      providerInfoAvailable: true,  
      streamBetCmsConfig: {
        enabled: true,
        sportIds: ['16', '21'],
        streamProviders: ['ATR']        
      }
    };
    expect(service.isStreamBetAvailable(streamBetConfig, 'EventVideoStreamComponent')).toBeFalsy();
  });

  it('should return priorityProviderName as ATR', () => {
    expect(service.priorityProviderName({ATR: 'At The Races'})).toEqual('At The Races');
  });

  it('should return priorityProviderName as iGameMedia', () => {
    expect(service.priorityProviderName({iGameMedia: 'iGame Media'})).toEqual('iGame Media');
  });

  it('should return priorityProviderName as IMG', () => {
    expect(service.priorityProviderName({IMG: 'IMG Video Streaming'})).toEqual('IMG Video Streaming');
  });

  it('should return priorityProviderName as IMG-test', () => {
    expect(service.priorityProviderName({IMG1: 'IMG Video Streaming'})).toEqual(null);
  });

  it('should return getStreamBetCmsConfig observable response', () => {
    service.getStreamBetCmsConfig().subscribe(data => {
      expect(data as any).toEqual({enabled: true});
    });
  });
  
});
