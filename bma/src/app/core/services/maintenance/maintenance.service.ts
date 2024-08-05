import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Event, NavigationEnd, Router } from '@angular/router';
import { Observable, of } from 'rxjs';
import { filter, finalize, map, shareReplay, switchMap, take } from 'rxjs/operators';

import environment from '@environment/oxygenEnvConfig';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';

import { IMaintenancePage, ISystemConfig } from '@core/services/cms/models';
import { ISiteServeHealthCheck } from '@core/services/maintenance/models/siteserve-healthcheck.model';

const maintenancePath = '/under-maintenance';
const statusPollDelay = 60 * 1000; // 1min
const getMaintenanceDelay: number = 5 * 1000; // 5sec

@Injectable()
export class MaintenanceService {
  private maintenancePageData$: Observable<IMaintenancePage | null>;
  private isCmsDataActual: boolean = true; // consider CMS data actual while loading only
  private activeMaintenancePage: IMaintenancePage;

  constructor(
    private windowRefService: WindowRefService,
    private cmsService: CmsService,
    private pubSubService: PubSubService,
    private http: HttpClient,
    private router: Router
  ) {
    this.firstNavigationStartsCheck();
  }

  /**
   * Detect when app is ready (finished it's initial navigation),
   *  and if maintenance status has not been checked yet (by page resolver),
   *  then run maintenance checks.
   */
  firstNavigationStartsCheck(): void {
    this.router.events.pipe(
      filter((e: Event) => e instanceof NavigationEnd),
      take(1),
      switchMap(() => {
        // do not (double)check maintenance on maintenance page load
        if (this.router.url.includes(maintenancePath)) { return of(false); }

        return this.isCmsMaintenanceEnabled();
      })
    ).subscribe((isCheckRequiredNow: boolean) => this.runMaintenanceCheck(isCheckRequiredNow));
  }

  /**
   * Return initial config of maintenance page (based on cms data)
   *
   * @returns {Observable}
   */
  isCmsMaintenanceEnabled(): Observable<boolean> {
    return this.cmsService.getSystemConfig().pipe(
      map((config: ISystemConfig) => !!(config.maintenancePage && config.maintenancePage.enabled))
    );
  }

  /**
   * Make maintenance check immediately (if required) and run a poll,
   * mark cms data of maintenance page as non actual
   */
  runMaintenanceCheck(isCheckRequiredNow: boolean): void {
    isCheckRequiredNow && this.checkForMaintenance().subscribe();
    this.runMaintenanceStatusPoll();
    this.isCmsDataActual = false;
  }

  /**
   * Start and repeat status check whole app life
   */
  runMaintenanceStatusPoll(): void {
    this.windowRefService.nativeWindow.setTimeout(() => {
      this.checkForMaintenance()
          .pipe(finalize(() => {
            this.runMaintenanceStatusPoll();
          }))
          .subscribe();
    }, statusPollDelay);
  }

  /**
   * Check if maintenance is active now and user is on appropriate page
   * Reload page if maintenance is active but config was changed
   * @returns {Observable}
   */
  checkForMaintenance(): Observable<void> {
    return this.getActiveMaintenancePage().pipe(map((activeMaintenancePage: IMaintenancePage) => {
      const isOnMaintenancePage = this.router.url.includes(maintenancePath);

      // maintenance activated, but not on the page yet
      if (activeMaintenancePage && !isOnMaintenancePage) {
        this.router.navigate([maintenancePath]);
        return;
      }

      // maintenance deactivated, but still on the page
      if (!activeMaintenancePage && isOnMaintenancePage) {
        this.router.navigate(['/']);
      }

      // maintenance activated and still on the page
      if (activeMaintenancePage && isOnMaintenancePage) {
        this.reload(activeMaintenancePage);
      }
    }));
  }

  /**
   * Reload page if maintenance is active but config was changed
   *
   */
  reload(activeMaintenancePage: IMaintenancePage): void {
    const isMaintenanceParamsChanged = JSON.stringify(activeMaintenancePage) !== JSON.stringify(this.activeMaintenancePage);

      if (isMaintenanceParamsChanged) {
        this.pubSubService.publish(this.pubSubService.API.MAINTENANCE_PAGE_DATA_CHANGED, activeMaintenancePage);
      }
      this.activeMaintenancePage = activeMaintenancePage;
  }

  /**
   * Check if maintenance is enabled in actual cms config (or ignore it)
   *  and get active maintenance page
   *
   * @returns {Observable}
   */
  getMaintenanceIfActive(): Observable<IMaintenancePage> {
    return this.isCmsMaintenanceEnabled().pipe(
      switchMap((isCmsMaintenanceEnabled: boolean) => {

        if (!isCmsMaintenanceEnabled && this.isCmsDataActual) {
          return of(null);
        }

        return this.getActiveMaintenancePage().pipe(map((activePage: IMaintenancePage) => {
          if (!activePage) {
            return null;
          }

          return activePage;
        }));
      })
    );
  }

  /**
   * Request CMS for maintenance pages and return first active one.
   * Share the stream during given delay after resolving (aka debounce)
   *
   * @returns {Observable}
   */
  getActiveMaintenancePage(): Observable<IMaintenancePage | null> {

    if (this.maintenancePageData$) {
      return this.maintenancePageData$;
    }

    this.maintenancePageData$ = this.cmsService.getMaintenancePage().pipe(
      map((maintenancePages: IMaintenancePage[]) => {

        // make a delay and stop sharing the stream when resolved
        this.windowRefService.nativeWindow.setTimeout(() => this.maintenancePageData$ = null, getMaintenanceDelay);

        if (!maintenancePages.length) { return null; }

        const currentTime = Date.now();

        // Get earliest of not ended (active) pages
        // Pages are sorted by validityPeriodStart on backend, it allows use of first match.
        const activeMaintenancePage = maintenancePages.find((page: IMaintenancePage) => {
          const
            startTime = Date.parse(page.validityPeriodStart),
            endTime = Date.parse(page.validityPeriodEnd);

          return startTime <= currentTime && endTime >= currentTime;
        });

        return activeMaintenancePage || null;
      }),
      shareReplay(1)
    );

    return this.maintenancePageData$;
  }

  /**
   * SiteServer Health Check Request
   *
   * @returns {Observable.<T>}
   */
  siteServerHealthCheck(forceRequest: boolean = false): Observable<string> {
    const isOnMaintenancePage = this.router.url.includes(maintenancePath);

    if (!isOnMaintenancePage && !forceRequest) {
      return of('No HealthCheck for non maintenance page');
    }

    return this.http.get<ISiteServeHealthCheck>(`${environment.SITESERVER_COMMON_ENDPOINT}/HealthCheck`, {
      observe: 'response'
    }).pipe(map((response: HttpResponse<ISiteServeHealthCheck>) => {
      const responseData = response.body;
      const healthCheckStatus = responseData.SSResponse.children[0].healthCheck.status;

      return healthCheckStatus === 'OK' ? healthCheckStatus : `Error while checking SS HealthCheck
      (maintenanceFactory.siteServerHealthCheck) ${healthCheckStatus}`;
    }));
  }
}
