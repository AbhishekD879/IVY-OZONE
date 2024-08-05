import { forkJoin as observableForkJoin, of as observableOf, Observable, throwError } from 'rxjs';
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { DeviceService } from '@core/services/device/device.service';
import { AsyncScriptLoaderService } from '@core/services/asyncScriptLoader/async-script-loader.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { ISystemConfig } from '@core/services/cms/models';
import { ISportEvent, ISportByMapping, IFeedMappings } from '@core/models/sport-event.model';
import environment from '@environment/oxygenEnvConfig';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { concatMap, switchMap } from 'rxjs/operators';
import { IOptaScoreboardConfig, IOptaScoreboardEndpoints } from '@edp/models/opta-scoreboard';
import { OptaScoreboardLoaderService } from '@edp/services/optaScoreboard/opta-scoreboard-loader.service';

@Injectable()
export class SportEventMainProviderService {

  private optaConfig: IOptaScoreboardConfig;
  private sysConfigsWithEventByMapping: ISystemConfig[];
  public isOptaProviderPresent: boolean = false;

  constructor(
    private windowRef: WindowRefService,
    private http: HttpClient,
    private deviceService: DeviceService,
    private asyncScriptLoaderFactory: AsyncScriptLoaderService,
    private optaScoreboardLoaderService: OptaScoreboardLoaderService,
    private cmsService: CmsService
  ) {
  }

  /**
   * Check if opta scoreboard enables in CMS for device and if mapping exist.
   * @param event
   * @returns {*}
   * @private
   */
  public checkOptaScoreboardAvailability(event: ISportEvent): Observable<Object> {
    return observableForkJoin(
      this.cmsService.getSystemConfig(),
      this.cmsService.getFeatureConfig('ScoreboardsSports'),
      this.getConfigForByMapping(event)
    ).pipe(
        concatMap((configs: ISystemConfig[]) => {
          this.sysConfigsWithEventByMapping = configs;
          return  this.checkIsEnabled(configs, event);
        }),
        concatMap(() => this.getConfig(event).pipe(
          switchMap(config =>this.checkIsStarted(event, config.apiKey, config.endpoints))
        )),
        switchMap(() => this.loadPolyfills()),
        switchMap(() => this.loadBundle()),
        switchMap(() => this.optaScoreboardLoaderService.loadBundle())
      );
  }

  /**
   * Get the bet radar mapping for the event
   * Also perform the device and category code
   * @param event
   * @returns {*}
   * @private
   */
  public checkBetradarAvailability(event: ISportEvent): Observable<Object> {
    if(!this.sysConfigsWithEventByMapping) {
      return throwError(`Unable to fetch BetRadar ByMapping for ${event.categoryId} (${event.categoryCode})`);
    }
    const [sysConfig] = this.sysConfigsWithEventByMapping;
    const eventByMapping: ISportByMapping = this.sysConfigsWithEventByMapping[this.sysConfigsWithEventByMapping.length - 1];
    const allowedForByMapping = eventByMapping.feedMappings.some( providerObj => providerObj.provider === 'BETRADAR');
    if(!allowedForByMapping) {
      return throwError(`Bet Radar Disabled for ByMapping event ${event.categoryId} (${event.categoryCode})`);
    }
    const allowed = sysConfig.BetRadarScoreBoard && sysConfig.BetRadarScoreBoard[this.deviceService.requestPlatform];
    if (!allowed) {
      return throwError(`Bet Radar Scoreboard Disabled for ${this.deviceService.requestPlatform}`);
    }
    const allowedForSport=  sysConfig.BetRadarScoreBoardsSports && sysConfig.BetRadarScoreBoardsSports[event.categoryId];
    if (!allowedForSport) {
      return throwError(`Bet Radar Scoreboard Disabled for ${event.categoryId} (${event.categoryCode})`);
    }
    return observableOf(eventByMapping);
  }

  /**
   * Get the img arena scoreboard mapping for the event
   * Also check the device and category code
   * @param event
   * @returns {*}
   * @private
   */
  public checkImgArenaScoreboardAvailability(event: ISportEvent): Observable<Object>{    
    if(!this.sysConfigsWithEventByMapping) {
      return throwError(`Unable to fetch Img Arena Scoreboard ByMapping for ${event.categoryId} (${event.categoryCode})`);
    }
    const [sysConfig] = this.sysConfigsWithEventByMapping;
    const eventByMapping: ISportByMapping = this.sysConfigsWithEventByMapping[this.sysConfigsWithEventByMapping.length - 1];
    const allowedForByMapping = eventByMapping.feedMappings.some((providerObj:IFeedMappings) => providerObj.provider === 'IMG');
    if(!allowedForByMapping) {
      return throwError(`Img Arena Scoreboard Disabled for ByMapping event ${event.categoryId} (${event.categoryCode})`);
    }
    const allowed = sysConfig.IMGScoreBoard && sysConfig.IMGScoreBoard[this.deviceService.requestPlatform];
    if (!allowed) {
      return throwError(`Img Arena Scoreboard Disabled for ${this.deviceService.requestPlatform}`);
    }
    const allowedForSport=  sysConfig.IMGScoreBoardSports && sysConfig.IMGScoreBoardSports[event.categoryId];
    if (!allowedForSport) {
      return throwError(`Img Arena Scoreboard Disabled for ${event.categoryId} (${event.categoryCode})`);
    }
    return observableOf(eventByMapping);
  }

  private loadBundle(): Observable<Object> {
    return observableForkJoin([
      this.asyncScriptLoaderFactory.loadJsFile(`${environment.OPTA_SCOREBOARD.CDN}/scoreboard.bundle.js`),
      this.asyncScriptLoaderFactory.loadCssFile(`${environment.OPTA_SCOREBOARD.CDN}/scoreboard.bundle.css`, true)
    ]);
  }

  private loadPolyfills(): Observable<Object> {

    // polyfills needed for opta-scoreboards
    const polyfills = [];

    if (!this.windowRef.nativeWindow.fetch) {
      polyfills.push(this.asyncScriptLoaderFactory
        .loadJsFile(`${environment.OPTA_SCOREBOARD.CDN}/polyfill-fetch.js`));
    }
    if (!this.windowRef.nativeWindow.EventSource) {
      polyfills.push(this.asyncScriptLoaderFactory
        .loadJsFile(`${environment.OPTA_SCOREBOARD.CDN}/polyfill-event-source.js`));
    }
    if (!this.windowRef.nativeWindow.customElements) {
      polyfills.push(this.asyncScriptLoaderFactory
        .loadJsFile(`${environment.OPTA_SCOREBOARD.CDN}/polyfill-webcomponents.js`));
    }
    // for forkJoin, observables array should have at least one element
    // in case no polyfills are needed
    polyfills.push(observableOf(true));

    return observableForkJoin(polyfills);
  }

  private checkIsStarted(event: ISportEvent, apiKey: string, endpoints: IOptaScoreboardEndpoints): Observable<Object>  {
    return this.http.head(`${endpoints.prematch}/${event.id}?api-key=${apiKey}`);
  }

  private getApiKey(config: IOptaScoreboardConfig, event: ISportEvent): string | null {
    const apiKeys = config.apiKeys;
    if (typeof apiKeys === 'string') {
      return apiKeys;
    }
    return apiKeys[event.categoryCode];
  }

  private loadConfig(): Observable<IOptaScoreboardConfig> {
    if (this.optaConfig) {
      return observableOf(this.optaConfig);
    }
    return this.http.get(`${environment.OPTA_SCOREBOARD.CDN}/scoreboard.config.json`).pipe(
      concatMap((config: any) => {
        const optaEnv = environment.OPTA_SCOREBOARD.ENV;
        if (typeof config.environments[optaEnv] === 'object' ) {
          this.optaConfig = config.environments[optaEnv];
          return observableOf(this.optaConfig);
        }
        return throwError(`Opta Scoreboard: no config available for environment ${optaEnv}`);
      })
    );
  }

  private getConfig(event: ISportEvent): Observable<{apiKey: string, endpoints: IOptaScoreboardEndpoints}> {
    return this.loadConfig().pipe(
      concatMap(config => {
        const apiKey = this.getApiKey(config, event);
        if (apiKey) {
          return observableOf({
            apiKey,
            endpoints: config.endpoints
          });
        } else {
          return throwError(`Opta Scoreboard: no api key available for ${event.categoryId} (${event.categoryCode})`);
        }
      })
    );
  }

  private checkIsEnabled(sysConfigs: ISystemConfig[], event: ISportEvent): Observable<string> {
    const eventByMapping: ISportByMapping = this.sysConfigsWithEventByMapping[this.sysConfigsWithEventByMapping.length - 1];
    const isBetRadarEnabled = eventByMapping.feedMappings.some( providerObj => providerObj.provider === 'BETRADAR');
    const isImgArenaEnabled = eventByMapping.feedMappings.some( providerObj => providerObj.provider === 'IMG');
    this.isOptaProviderPresent = eventByMapping.feedMappings.some( providerObj => providerObj.provider === 'OPTA');
    if(isBetRadarEnabled||isImgArenaEnabled) {
      return throwError(`Opta Scoreboard Disabled for ByMapping event ${event.categoryId} (${event.categoryCode})`);
    }
    const allowedForSport = sysConfigs[1] && sysConfigs[1][event.categoryId];
    if (!allowedForSport) {
      return throwError(`Opta Scoreboard Disabled for ${event.categoryId} (${event.categoryCode})`);
    }
    const allowed = sysConfigs[0].OPTAScoreboard && sysConfigs[0].OPTAScoreboard[this.deviceService.requestPlatform];
    if (!allowed) {
      return throwError(`Opta Scoreboard Disabled for ${this.deviceService.requestPlatform}`);
    }
    return observableOf('');
  }

  private getConfigForByMapping(event: ISportEvent): Observable<ISportByMapping> {
    return this.getConfig(event).pipe(
      switchMap(config => this.http.get(`${config.endpoints.bymapping}/${event.id}?api-key=${config.apiKey}`)
    ));
  }
}

