import { Injectable } from '@angular/core';
import { filter } from 'rxjs/operators';
import { Router, Event, NavigationEnd } from '@angular/router';
import { IRouterStateModel } from './route.model';

@Injectable({ providedIn: 'root' })
export class RouterStateService {
    private previousRouteUrl: string;
    private currentRouteUrl: string;
    constructor(private router: Router) {
        this.currentRouteUrl = this.router.url;
        router.events.pipe(filter((event: Event) => event instanceof NavigationEnd)).subscribe((event: any) => {
            this.previousRouteUrl = this.currentRouteUrl;
            this.currentRouteUrl = event.url;
        });
    }

    public getRouterState(): IRouterStateModel {
        return {
            previousUrl: this.previousRouteUrl, currentUrl: this.currentRouteUrl
        }
    }
}