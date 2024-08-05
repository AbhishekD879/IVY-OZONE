import { Injectable } from '@angular/core';
import {
  Router,
  NavigationEnd,
  Event,
  RoutesRecognized,
  ActivatedRoute,
  ActivatedRouteSnapshot
} from '@angular/router';
import { RendererService } from '@shared/services/renderer/renderer.service';
import { Observable, ReplaySubject } from 'rxjs';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
@Injectable()
export class RoutingState {
  private history: string[] = [];
  private segmentHistory: string[] = [];
  private routeParamsHistory: ActivatedRouteSnapshot[] = [];
  private routerEventsReplaySubject: ReplaySubject<Event> = new ReplaySubject();

  constructor(
    protected router: Router,
    protected route: ActivatedRoute,
    private rendererService: RendererService,
    private windowRef: WindowRefService,
    private pubSubService: PubSubService
  ) {}

  get replayRouterEvents(): Observable<Event> {
    return this.routerEventsReplaySubject.asObservable();
  }
  set replayRouterEvents(value:Observable<Event>){}

  public loadRouting(): void {
    this.router.events
      .subscribe((event: Event) => {
        this.loadRoutingHandler(event);
      });
  }

  public getHistory(): string[] {
    return this.history;
    
  }

  public setHistory(history: string[]) {
    this.history = history;
  }

  public getSegmentHistory(): string[] {
    return this.segmentHistory;
  }

  public setCurrentUrl(url: string): void {
    this.history[this.history.length - 1] = url;
  }

  public getCurrentSegment(): string {
    return this.segmentHistory[this.segmentHistory.length - 1] || '';
  }

  public getPreviousSegment(): string {
    return this.segmentHistory[this.segmentHistory.length - 2] || '';
  }

  public getPreviousUrl(): string {
    return this.history[this.history.length - 2] || '/';
  }

  public getCurrentUrl(): string {
    return this.history[this.history.length - 1] || '/';
  }

  public getPathName(): string {
    const currentUrl: string = this.history[this.history.length - 1];
    const pathName: string[] = currentUrl.split('/');
    return pathName[pathName.length - 1] || '';
  }

  public getPreviousRouteSnapshot(): ActivatedRouteSnapshot {
    return this.routeParamsHistory[this.routeParamsHistory.length - 2];
  }

  public getPreviousRouteParam(param: string): string | null {
    const prevRouteSnapshot = this.getPreviousRouteSnapshot();

    return prevRouteSnapshot ? this.getRouteParam(param, prevRouteSnapshot) : null;
  }

  public getRouteParam(paramName: string, routeSnapshot: ActivatedRouteSnapshot): string | null {
    if (routeSnapshot.paramMap.get(paramName)) {
      return routeSnapshot.paramMap.get(paramName);
    } else if (routeSnapshot.firstChild && routeSnapshot.firstChild.paramMap.get(paramName)) {
      return routeSnapshot.firstChild.paramMap.get(paramName);
    } else if (routeSnapshot.firstChild && routeSnapshot.firstChild.children.length) {
      return this.getRouteParam(paramName, routeSnapshot.firstChild);
    }

    return null;
  }

  public getRouteSegment(snapshotName: string, routeSnapshot: ActivatedRouteSnapshot): string {
    if (!routeSnapshot) {
      return '';
    }

    if (routeSnapshot.firstChild) {
      return this.getRouteSegment(snapshotName, routeSnapshot.firstChild);
    } else if (routeSnapshot.data[snapshotName]) {
      return routeSnapshot.data[snapshotName];
    }

    return '';
  }
  /**
   * Portal is a Vanilla library that handles User pages - Settings, Menu, Gamgling controls, etc
   * Its rendering at the same router-outlet as Oxygen home ot sports components and register as a children to Oxygen
   * root component. Its required to add global class that handles blocks composition and some general styles when
   * Portal components are rendered as they behaves as am overlay
   */
  togglePortalSwitch() {
    const segment = this.getCurrentSegment();
    const isVanillaSegment = segment && segment === 'vanilla';
    this.toggleVanillaScoping(isVanillaSegment);
    this.toggleBmaScoping(!isVanillaSegment);
  }
  /**
   * Add a route segment to the segment history
   * @param event {Event} a router event
   */
  private loadRoutingHandler(event: Event): void {
    if (event instanceof NavigationEnd) {
      this.navigationEndEventListener(event);
    } else if (event instanceof RoutesRecognized) {
      const lastSegment: string = this.getRouteSegment('segment', event.state.root);

      if (lastSegment !== this.getCurrentSegment()) {
        // Add segment to route data to detect segment here
        this.segmentHistory.push(lastSegment);
      }
    }
    this.routerEventsReplaySubject.next(event);
  }

  private navigationEndEventListener(event): void {
    this.history.push(event.urlAfterRedirects);
    this.routeParamsHistory.push(this.route.snapshot);
    this.togglePortalSwitch();
  }

  /**
   * Remove Oxygem scoping class not to impact on Portal components.
   * it end up in Portal selectors to have lower priority than Oxygen.
   * @param apply
   */
  private toggleBmaScoping(apply: boolean): void {
    const bmaClass = 'vn-bma';
    const bma = this.windowRef.document.querySelector('bma-main');
    if (!bma) {
      return;
    }
    apply ? this.rendererService.renderer.addClass(bma, bmaClass)
      : this.rendererService.renderer.removeClass(bma, bmaClass);
  }

  /**
   * Add Scoping class to a body to fix clashes between Oxygen and Portal when Portal components are rendered under
   * specific path (Example: There shouldn't be left menu and right collumn in desktop mode visible when Portal is
   * rendered)
   * Scoping styles are located at platforms/vanillaMobile|vanillaDesktop/assets/styles/vanilla-scoping.scss
   * @param apply
   */
  private toggleVanillaScoping(apply: boolean): void {
    const body = window.document.body;
    const vanillaStateClass = 'vn-scope';

    this.pubSubService.publish(this.pubSubService.API.VANILLA_SCOPE_CHANGE, apply);

    apply ? this.rendererService.renderer.addClass(body, vanillaStateClass)
      : this.rendererService.renderer.removeClass(body, vanillaStateClass);
  }

  /**
   * Validates the uri allows further routing
   * @returns void
   */
  navigateUri($event: MouseEvent, routeUrl: string, sportName: string, defaultTab: string): void {
    $event.preventDefault();
    if ((sportName === 'horseracing' && this.router.url === '/horse-racing' && routeUrl === '/horse-racing/featured') ||
    (sportName === 'greyhound' && this.router.url === '/greyhound-racing' && ((defaultTab === 'today' && routeUrl === '/greyhound-racing/today') || (defaultTab === 'races' && routeUrl === '/greyhound-racing/races/next'))) ||
    (`${this.router.url}/${defaultTab}` === routeUrl)) {
      return;
    }
    this.router.navigateByUrl(routeUrl);
  }
}
