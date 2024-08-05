import { AfterViewInit, Directive, ElementRef, Input } from '@angular/core';
import { fromEventPattern, Observable } from 'rxjs';
import { IGATrackingModel } from '../models/gtm.event.model';
import { GtmService } from '../services/gtm/gtm.service';
import { SessionStorageService } from '@app/core/services/storage/session-storage.service';
import { GA_TRACKING } from '@app/shared/constants/channel.constant';


// Add this directive on the element which scrolls
//this listens only for first scroll
@Directive({
    // eslint-disable-next-line @angular-eslint/directive-selector
    selector: '[scrollonce]'
})
export class ScrollOnceDirective implements AfterViewInit {
    @Input('scrollonce') targetElementFrom;
    @Input('GATrackingObj') GAtrackingObject: IGATrackingModel;
    @Input('elemEventType') typeOfEvent?= 'scroll';
    eventPattern: Observable<any>;
    constructor(public elr: ElementRef, public gtmService: GtmService, private sessionStorage: SessionStorageService) {
    }
    ngAfterViewInit(): void {
        const clicks = this.callEventPattern();
        const data = clicks.subscribe(() => {
            this.gtmUpdate();
            data.unsubscribe();
        });
    }

    callEventPattern() {
        return fromEventPattern(this.addClickHandler.bind(this), this.removeClickHandler.bind(this))
    }

    //add listner for scroll on targeted element
    addClickHandler(handler) {
        this.elr.nativeElement.addEventListener(this.typeOfEvent, handler);
    }
    // remove the listner for scroll after firsttime scroll
    removeClickHandler(handler) {
        this.elr.nativeElement.removeEventListener(this.typeOfEvent, handler);
    }
    // Based on the targetElement From if it is required to push check and push
    // test is just to test remove once implementaion done
    gtmUpdate() {
        if (this.GAtrackingObject) {
            const isDataLayerUpdated = this.sessionStorage.get(this.targetElementFrom);
            if (!isDataLayerUpdated && this.GAtrackingObject.isHomePage &&
                ['moduleribbon', 'sportsribbon'].includes(this.targetElementFrom)) {
                    //setting this flag to check if the module is updated or not. 
                    //scrollable directive is breaking this logic on scroll. Added sessionstorage to check if updated.
                if (this.targetElementFrom == GA_TRACKING.moduleRibbon.moduleName) {
                    this.sessionStorage.set(this.targetElementFrom, true);
                }
                this.gtmDataHandler(this.GAtrackingObject);
            } else if (this.targetElementFrom == 'surfaceBet') {
                this.gtmDataHandler(this.GAtrackingObject);
            }
        }

    }

    //Based upon the GTM data received gtmservice pushes the event.
    gtmDataHandler(tracker: IGATrackingModel) {
        this.gtmService.push(tracker.event, tracker.GATracking);
    }
}
