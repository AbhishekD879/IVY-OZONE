import { Observable, Subject } from 'rxjs';
import { Injectable } from '@angular/core';
import { CmsService } from '@core/services/cms/cms.service';
import { IStreamBetWeb, ISystemConfig } from '@core/services/cms/models/system-config';
import environment from '@environment/oxygenEnvConfig';

@Injectable({ providedIn: 'root' })
export class EventVideoStreamProviderService {
  
  snbVideoFullScreenExitSubj: Subject<void> = new Subject<void>();
  private playVideoObservable: Subject<void>;
  private playSucessObservable: Subject<boolean>;
  private hideStreamObservable: Subject<boolean>;
  isStreamAndBet:boolean;
  streamBetWeb: IStreamBetWeb;
  constructor(private cmsService:CmsService) {
    this.playVideoObservable = new Subject<void>();
    this.playSucessObservable = new Subject<boolean>();
    this.hideStreamObservable = new Subject<boolean>();
  }

  get playListener(): Subject<void> {
    return this.playVideoObservable;
  }
  set playListener(value:Subject<void>){}

  get playSuccessErrorListener(): Subject<boolean> {
    return this.playSucessObservable;
  }
  set playSuccessErrorListener(value:Subject<boolean>){}
  get showHideStreamListener(): Subject<boolean> {
    return this.hideStreamObservable;
  }
  set showHideStreamListener(value:Subject<boolean>){}

  isStreamBetAvailable(streamBetConfig,location:string): boolean {  
    const isStreamBetAvailableIntial = streamBetConfig.streamBetCmsConfig?.enabled &&
    (streamBetConfig.streamBetCmsConfig.sportIds?.indexOf(streamBetConfig.categoryId.toString())>-1) &&    
    (streamBetConfig.streamBetCmsConfig.streamProviders.indexOf((streamBetConfig.providerInfo.priorityProviderName? streamBetConfig.providerInfo.priorityProviderName: this.priorityProviderName(streamBetConfig.providerInfo)))>-1) &&
    streamBetConfig.isMobile && !streamBetConfig.isTablet && !streamBetConfig.isDesktop
    if(location === "EventVideoStreamComponent"){
      return isStreamBetAvailableIntial && streamBetConfig.providerInfoAvailable && !streamBetConfig.isMyBets;
    }
    return streamBetConfig.categoryId.toString() === environment.HORSE_RACING_CATEGORY_ID && location === 'racingEventMain'  ? isStreamBetAvailableIntial && streamBetConfig.isIHR : isStreamBetAvailableIntial;
  }
  private priorityProviderName(providerInfo):string{
    const priorityProviderName  = providerInfo.IMG ? 'IMG Video Streaming' : 
     (providerInfo.ATR ? 'At The Races' : (providerInfo.iGameMedia ? 'iGame Media' : (null) ));
    return priorityProviderName;
  }

  getStreamBetCmsConfig(): Observable<ISystemConfig> {
    return this.cmsService.getFeatureConfig('StreamBetWeb');
  }
}
