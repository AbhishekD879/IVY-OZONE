import { debounceTime, filter, first } from 'rxjs/operators';
import { AsyncSubject, BehaviorSubject, Observable } from 'rxjs';
import { Injectable } from '@angular/core';
import { Router, Event, NavigationEnd } from '@angular/router';


import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { ISeoPagesPaths, ISeoPage } from '@core/services/cms/models';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { IEventPageSeo } from '@core/services/cms/models/seo/seo-page.model';
import { IAutoSeoPages } from '@core/services/cms/models/seo/seo-pages-paths';

/**
 * SEO data factory
 * Gets SEO configuration from CMS
 * Provides data for Static Block, meta description and page title.
 * @return {Object}
 */

@Injectable({
  providedIn: 'root'
})
export class SeoDataService {
  defaultPage: Partial<ISeoPage> = {
    title: 'Online Sports Betting and Latest Odds - Coral',
    description: 'Betting has never been better with pre-event and in-play markets available from all over the world.' +
      ' Get the latest betting odds at Coral. Don\'t Bet Silly, Bet Savvy!'
  };

  private paths$: Observable<ISeoPagesPaths>;
  private flagPage$: Observable<string>;
  private page$: AsyncSubject<Partial<ISeoPage>> = new AsyncSubject<Partial<ISeoPage>>();
  private activePage: Partial<ISeoPage>;
  private executed: boolean = false;
  private isHashChangeListenerSet: boolean = false;
  private eventSchema: Object = {};
  private organisationSchema: Object = {};

  public seoSubjObservable = new Observable<boolean>();
  public seosubj$ = new BehaviorSubject(false);
  protected isAutoSEO = false;
  constructor(
    protected windowRef: WindowRefService,
    protected cms: CmsService,
    protected pubsub: PubSubService,
    protected router: Router
  ) {
    this.getSeoPagesPaths();
    this.seoSubjObservable = this.seosubj$.asObservable();
  }

  /**
   * getPage should be handled only once.
   * pagePromiseHandled flag is used to prevent
   * seoStaticBlock component from executing on each 'link'.
   */
  getPage(): Observable<Partial <ISeoPage> | string> {
    if (!this.executed) {
      this.executed = true;
      return this.page$;
    }

    this.flagPage$ = new Observable<string>(observer => {
      observer.error('pagePromiseHandled');
      observer.complete();
    });

    return this.flagPage$;
  }

  eventPageSeo(event: { [name: string]: any }, edpUrl: string): void {

    this.eventSchema['@context'] = 'https://schema.org';
    this.eventSchema['@type'] = 'SportsEvent';
    this.eventSchema['name'] = event.name;
    this.eventSchema['description'] = event.categoryName;
    this.eventSchema['startDate'] = new Date(event.startTime)
      .toLocaleString('en-GB', { timeZone: 'Europe/London' });
    this.eventSchema['location'] = {};
    this.eventSchema['location']['@type'] = 'city';
    this.eventSchema['location']['name'] = event.typeName;
    if (this.checkForHorse(event)) {
      this.eventSchema['url'] = this.windowRef.nativeWindow.location.origin + edpUrl;
    } else {
      this.eventSchema['url'] = `${this.windowRef.nativeWindow.location.origin}` + '/' + `${edpUrl}`;
    }
    this.eventSchema['broadcastOfEvent'] = {};
    this.eventSchema['broadcastOfEvent']['@type'] = 'SportsEvent';
    this.eventSchema['broadcastOfEvent']['name'] = event.typeName;
    this.eventSchema['broadcastOfEvent']['startDate'] = new Date(event.startTime)
      .toLocaleString('en-GB', { timeZone: 'Europe/London' });
    this.eventSchema['broadcastOfEvent']['location'] = {};
    this.eventSchema['broadcastOfEvent']['location']['@type'] = 'city';
    this.eventSchema['broadcastOfEvent']['location']['name'] = event.typeName;
    this.eventSchema['broadcastOfEvent']['competitor'] = [];
    this.competitors(event);
    const script = document.createElement('script');
    script.type = 'application/ld+json';
    script.text = JSON.stringify(this.eventSchema);
    document.querySelector('head').appendChild(script);
  }

  competitors(event: { [name: string]: any }): void {
    let homeTeam, awayTeam: string;
    const teamData: Array<string> = [],
          outComes: Array<Object> = event.markets[0]?.outcomes ?? [];
    if (this.checkForSport(event)) {
      if (event.teamAway || event.teamHome) {
        homeTeam = event.teamHome;
        awayTeam = event.teamAway;
      } else {
        homeTeam = event.name.split(/ v | vs | - /)[0];
        awayTeam = event.name.split(/ v | vs | - /)[1];
      }
      const schemaHome: Object = {};
      schemaHome['@type'] = 'SportsTeam';
      schemaHome['name'] = homeTeam;
      const schemaAway: Object = {};
      schemaAway['@type'] = 'SportsTeam';
      schemaAway['name'] = awayTeam;
      this.eventSchema['broadcastOfEvent']['competitor'].push(schemaHome);
      this.eventSchema['broadcastOfEvent']['competitor'].push(schemaAway);

    } else {
      outComes.forEach((outcome: IEventPageSeo) => {
        if (this.checkForHorse(event) && !outcome.outcomeMeaningMinorCode) {
          teamData.push(outcome.name);
        }
        if(event.categoryId !== '21' && event.categoryId !== '19') {
          teamData.push(outcome.name);
        }
      });
      const raceSchema: object = {};
      raceSchema['@type'] = 'SportsTeam';
      raceSchema['name'] = teamData;
      this.eventSchema['broadcastOfEvent']['competitor'].push(raceSchema);
    }
  }
  organisationPageSeo(): void {
    let logo: string;
    const teamData: Array<string> = [];
    if (this.windowRef.nativeWindow.gcData.brand.toLocaleString() === 'Coral') {
      logo = 'https://scmedia.itsfogo.com/$-$/7f10c18c8ae340a9b08219809b3ccd21.svg';
    } else {
      logo = 'https://scmedia.itsfogo.com/$-$/fafd3663f4724e8dba6fb916c2046704.svg';
    }
    this.organisationSchema['@context'] = 'https://schema.org';
    this.organisationSchema['@type'] = 'Organization';
    this.organisationSchema['name'] = this.windowRef.nativeWindow.gcData.brand;
    this.organisationSchema['url'] = this.windowRef.nativeWindow.location.origin;
    this.organisationSchema['logo'] = logo;
    this.organisationSchema['sameAs'] = {};
    /* Once we get details this should be uncommented
    do not remove this code
    this.organisationSchema['contactPoint'] = {};
    this.organisationSchema['contactPoint']['@type'] = 'ContactPoint';
    this.organisationSchema['contactPoint']['telephone'] = '+00 44 20 8507 5544';
    this.organisationSchema['contactPoint']['contactType'] = 'customer service';
    this.organisationSchema['contactPoint']['contactOption'] = 'TollFree';
    this.organisationSchema['contactPoint']['areaServed'] = 'UK'; */
    this.organisationSchema['Address'] = 'LC International Limited ,Suite 6, Atlantic Suites, Gibraltar';
    const socialLinks: { [name: string]: any } = this.windowRef.document.querySelectorAll('.social-content a');
    socialLinks.forEach((outcome: IEventPageSeo) => {
      teamData.push(outcome.href);
    });
    this.organisationSchema['sameAs'] = teamData;
    const script = document.createElement('script');
    script.type = 'application/ld+json';
    script.text = JSON.stringify(this.organisationSchema);
    document.querySelector('head').appendChild(script);
  }

  private checkForSport(event) {
    const eventId = ['21','19','18','23','24','12','46','25','48','26'];
    return !eventId.includes(event.categoryId);
  }

  protected checkForHorse(event) {
    const eventId = ['21','19'];
    return eventId.includes(event.categoryId);
  }

  protected getSeoPagesPaths(): void {
    this.paths$ = new Observable<ISeoPagesPaths>(observer => {
      this.cms.getSeoPagesPaths()
        .subscribe(paths => {
          observer.next(paths);

          this.handlePaths(paths);

          if (!this.isHashChangeListenerSet) {
            /* eslint-disable */
            this.router.events.pipe(
                filter((event: Event) => event instanceof NavigationEnd),
                debounceTime(100)
              )
              .subscribe((event: Event) => {
                this.handlePaths(paths);
              });
            /* eslint-enable */

            this.isHashChangeListenerSet = true;
          }
        });
    }).pipe(first());

    this.paths$.subscribe();
  }

  private handlePaths(paths: ISeoPagesPaths): void {
    const fullPath: string = this.windowRef.nativeWindow.location.pathname,
      lookupPath: string = fullPath.indexOf('/static') === 0 ? fullPath.substring(7) : fullPath;
    // if URL is /static/football only /football should be used

    // If SEO is configured - get seoData for current location and update page
    if (paths[lookupPath]) {
      this.isAutoSEO = false;
      this.cms.getSeoPage(paths[lookupPath]).subscribe(data => this.doUpdate(data));
      this.seosubj$.next(true);

      // If SEO is not configured - set auto-seo values
    } else {
      this.cms.getAutoSeoPages().subscribe((autoSeoPagesdata: IAutoSeoPages) => {
        this.pubsub.publish(this.pubsub.API.AUTO_SEOTAGS_DATA_UPDATED, [autoSeoPagesdata]);
        this.seosubj$.next(false);
      });
    }
  }
  
  protected doUpdate(page: Partial<ISeoPage>): void {
    const document: Document = this.windowRef.nativeWindow.document;
    // Notify listeners on initial load.
    // Promise is used instead of Connect to notify listeners on initial load.
    // This is needed because listeners may initialize after getSeoPagesPaths call is completed.
    this.page$.next(page);
    this.page$.complete();

    // Notify listeners on subsequent changes
    this.pubsub.publish(this.pubsub.API.SEO_DATA_UPDATED, [page]);

    this.activePage = page;

    // Set meta description
    document.querySelector('meta[name=description]').setAttribute('content', page.description);
    document.title = page.title;
  }

}
