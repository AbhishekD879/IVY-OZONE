import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { ISeoPage } from '@core/services/cms/models';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import environment from '@environment/oxygenEnvConfig';
import { IAutoSeoPages } from '@core/services/cms/models/seo/seo-pages-paths';
import { SeoDataService } from '@coreModule/services/seoData/seo-data.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { IAutoSeoData, IAutoSeoPage } from '@app/core/services/cms/models/seo/seo-page.model';
import { autoSeoConstants } from '@lazy-modules/seoStaticBlock/seoAutoTags/seo-automated-tags.constant';
import { bma } from '@app/lazy-modules/locale/translations/en-US/bma.lang';
import { ISportEvent } from '@app/core/models/sport-event.model';
import { IConstant } from '@app/core/services/models/constant.model';

@Injectable()
export class SeoAutomatedTagsService extends SeoDataService {

  protected autoseo_Page: Partial<ISeoPage> = {};
  private altered_event_name: string;
  private readonly CORAL: string = 'bma';
  private eventsSchema: IConstant[];
  private schemaScript: HTMLElement;

  constructor(
    protected windowRef: WindowRefService,
    protected cms: CmsService,
    protected pubsub: PubSubService,
    protected router: Router
  ) {
    super(windowRef, cms, pubsub, router);
    this.pubsub.subscribe(autoSeoConstants.subscriberName, this.pubsub.API.AUTO_SEOTAGS_DATA_UPDATED, (autoSeoPagesdata: IAutoSeoPages) => {
      this.isAutoSEO = true;
      autoSeoPagesdata && this.loadAutoSeoPage(autoSeoPagesdata);
    });
    this.getSeoPagesPaths();
    this.schemaForMultipleEvents();
    this.removeSchema();
  }
  /**
   * Assigns a metaTitle and metaDescription for Autoseopage
   * @param autoSeoPagesdata 
   */
  private loadAutoSeoPage(autoSeoPagesdata: IAutoSeoPages): void {
    const activeUrl: string = this.router.url;
    const splitedUrl: string[] = activeUrl.split("/");
    splitedUrl[1] = '/' + splitedUrl[1];
    const currentAutoSeo_Page: IAutoSeoPage = autoSeoPagesdata[splitedUrl[1]];
    if (currentAutoSeo_Page) {
      this.seosubj$.next(true);
      this.pubsub.subscribe(autoSeoConstants.subscriberName, this.pubsub.API.AUTOSEO_DATA_UPDATED, (autoSeoData: IAutoSeoData) => {
        if (this.isAutoSEO) {
          if (autoSeoData.isOutright && autoSeoPagesdata[autoSeoConstants.outrightTag]) {
            this.autoseo_Page.title = autoSeoPagesdata[autoSeoConstants.outrightTag].metaTitle;
            this.autoseo_Page.description = autoSeoPagesdata[autoSeoConstants.outrightTag].metaDescription;
          }
          else {
            this.autoseo_Page.title = currentAutoSeo_Page.metaTitle;
            this.autoseo_Page.description = currentAutoSeo_Page.metaDescription;
          }
          this.replaceAutoSeoPage(this.autoseo_Page, autoSeoData);
        }
      });
    }
    else {
      this.isAutoSEO = false;
      this.seosubj$.next(false);
      this.doUpdate(this.defaultPage);
    }
  }
  /**
   * formats first character of a string
   * @param autoSeoplaceholder 
   * @returns string with the uppercase of first character
   */
  private formatFirstLetter(autoSeoplaceholder: string): string {
    if (autoSeoplaceholder.length) {
      return autoSeoplaceholder.charAt(0).toUpperCase() + autoSeoplaceholder.slice(1);
    }
  }
  /**
   * replace the autoseo-placeholder with actual data
   * @param autoseopage 
   * @param autoSeoData 
   */
  private replaceAutoSeoPage(autoseopage: Partial<ISeoPage>, autoSeoData: IAutoSeoData): void {
    this.altered_event_name = autoSeoData.name.replace(autoSeoConstants.teamSeparationRegex, autoSeoConstants.replacedteamSeparator);
    const altered_Brand: string = environment.brand == this.CORAL ? bma.coral : this.formatFirstLetter(environment.brand);
    autoseopage.title = autoseopage.title.replace(autoSeoConstants.competitionPlaceHoleder, this.formatFirstLetter(autoSeoData.typeName));
    autoseopage.title = autoseopage.title.replace(autoSeoConstants.eventPlaceHolder, this.altered_event_name);
    autoseopage.title = autoseopage.title.replace(autoSeoConstants.sportPlaceHolder, this.formatFirstLetter(autoSeoData.categoryName));
    autoseopage.title = autoseopage.title.replace(autoSeoConstants.brandPlaceHolder, altered_Brand);
    autoseopage.description = autoseopage.description.replace(autoSeoConstants.competitionPlaceHoleder, this.formatFirstLetter(autoSeoData.typeName));
    autoseopage.description = autoseopage.description.replace(autoSeoConstants.eventPlaceHolder, this.altered_event_name);
    autoseopage.description = autoseopage.description.replace(autoSeoConstants.sportPlaceHolder, this.formatFirstLetter(autoSeoData.categoryName));
    autoseopage.description = autoseopage.description.replace(autoSeoConstants.brandPlaceHolder, altered_Brand);
    this.doUpdate(autoseopage);
  }
  /**
   * seo schema for multipleEvents
   */
  private schemaForMultipleEvents(): void {
    this.pubsub.subscribe(autoSeoConstants.subscriberName, this.pubsub.API.SCHEMA_DATA_UPDATED, (events: ISportEvent[], url: string) => {
      if (events?.length && url) {
        this.eventsSchema = [];
        events.forEach((event) => {
          this.schemaSubEvent(event);
        });
        const script = document.createElement('script');
        script.type = 'application/ld+json';
        script.id = url;
        script.text = JSON.stringify(this.eventsSchema);
        this.schemaScript = document.getElementById(script.id);
        if (!this.schemaScript) {
          this.eventsSchema.length && document.querySelector('head').appendChild(script);
        }
        else {
          this.eventsSchema.length && document.querySelector('head').removeChild(this.schemaScript);
          this.eventsSchema.length && document.querySelector('head').appendChild(script);
        }
      }
    });
  }
  /**
   * add all the events of the page to subEvent
   * @param event ISportEvent
   */
  private schemaSubEvent(event: ISportEvent): void {
    const subEvent = {};
    if (event) {
      const isRacing: boolean = this.checkForHorse(event);
      subEvent['@context'] = 'https://schema.org';
      subEvent['@type'] = 'SportsEvent';
      subEvent['name'] = isRacing ? event.originalName : event.name;
      subEvent['description'] = event.categoryName;
      subEvent['startDate'] = this.getseoSchemastartTime(event.startTime,isRacing,event.localTime);
      subEvent['location'] = {};
      subEvent['location']['@type'] = 'city';
      subEvent['location']['name'] = event.typeName;
      subEvent['url'] = `${this.windowRef.nativeWindow.location.origin}` + '/' + `${event.url}`;
      if (!isRacing) {
        subEvent['competitor'] = this.competitorsForSportEvents(event);
      }
      this.eventsSchema.push(subEvent);
    }
  }

  /**
   * to remove the schemaScript from head
   */
  private removeSchema(): void {
    this.pubsub.subscribe(autoSeoConstants.subscriberName, this.pubsub.API.SCHEMA_DATA_REMOVED, (url: string) => {
      const schemaScript: HTMLElement = url && document.getElementById(url);
      schemaScript && document.querySelector('head').removeChild(schemaScript);
    });
  }
  /**
   * append competitiors to the sportEvent
   * @param event 
   * @returns 
   */
  private competitorsForSportEvents(event: ISportEvent): IConstant[] {
    if (event) {
      const competitors = [];
      const splitedName: string[] = event.name.split(autoSeoConstants.teamSeparationRegex);
      const homeTeam:string = splitedName && splitedName[0];
      const awayTeam:string = splitedName && splitedName[1];
      const schemaHome: Object = {};
      schemaHome['@type'] = 'SportsTeam';
      schemaHome['name'] = homeTeam;
      const schemaAway: Object = {};
      schemaAway['@type'] = 'SportsTeam';
      schemaAway['name'] = awayTeam;
      competitors.push(schemaHome);
      competitors.push(schemaAway);
      return competitors;
    }
  }
  /**
   * will get the seo schema start time
   * @param eventStartTime 
   * @param isRacing 
   * @returns startTime of the event time zone config
   */
  private getseoSchemastartTime(eventStartTime: string, isRacing: boolean,eventLocalTime:string): string {
    const eventStartDate: Date = eventStartTime && new Date(eventStartTime);
    if (eventStartDate) {
      return (isRacing && eventLocalTime ? eventStartDate.toISOString().substring(0, 11) + eventLocalTime + eventStartDate.toISOString().substring(16, 19) : eventStartDate.toISOString().substring(0, 19)) + this.getTimeZoneOffSet(eventStartDate.getTimezoneOffset());
    }
    return '';
  }
  /**
   * will get timeZone Offset
   * @param timeZoneOffSet 
   * @returns timeZone offset for the given offset
   */
  private getTimeZoneOffSet(timeZoneOffSet: number): string {
    if (timeZoneOffSet === null || timeZoneOffSet === undefined) {
      return '';
    }
    let timezoneStandard = '';
    const negativeOffset = timeZoneOffSet < 0;
    timeZoneOffSet = Math.abs(timeZoneOffSet);
    const offSetHrs = Math.floor(timeZoneOffSet / 60);
    const offSetMin = Math.abs(timeZoneOffSet % 60);
    if (timeZoneOffSet === 0) {
      timezoneStandard = 'Z';
    } else if (negativeOffset) {
      timezoneStandard = `+${this.paddingValue(offSetHrs)}:${this.paddingValue(offSetMin)}`;
    } else {
      timezoneStandard = `-${this.paddingValue(offSetHrs)}:${this.paddingValue(offSetMin)}`;
    }
    return timezoneStandard;
  }
  /**
   * @param offSetValue 
   * @returns padded offset value
   */
  private paddingValue(offSetValue: number): string {
    return offSetValue.toString().padStart( 2, '0');
  }
}
