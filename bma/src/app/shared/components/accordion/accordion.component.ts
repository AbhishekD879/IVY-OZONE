import { ChangeDetectorRef, Component, EventEmitter, Input, OnInit, Output, ChangeDetectionStrategy, OnDestroy } from '@angular/core';
import { ITrackEvent } from '@core/services/gtm/models';

import { GtmService } from '@core/services/gtm/gtm.service';
import { AccordionService } from './accordion.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { ISportEvent } from '@core/models/sport-event.model';

  /**
   * Accordion bindings:
   * accordionTitle: accordion title
   *   memoryId: accordion id, for saving state in Storage
   *   memoryLocation: accordion location, for saving state in Storage
   *   inner: used for second level accordion,
   *   card: used for ng-class .page-inner-container (second level accordions with odds-cards),
   *   trackLabel: used for GA, on VIP page,
   *   trackCategory: used for GA, on VIP page,
   *   isExpanded: used for toogle function,
   *   render: used for ng-if instead of ng-show,
   *   disabled: used to disable expand / collapse,
   *   function: callback needed for $timeout when two way data binding in completed,
   */
  @Component({
    changeDetection: ChangeDetectionStrategy.OnPush,
    selector: 'accordion',
    templateUrl: 'accordion.component.html'
  })
  export class AccordionComponent implements OnInit, OnDestroy {

    @Input() accordionTitle?: string;
    @Input() memoryId?: string;
    @Input() memoryLocation?: string;
    @Input() headerClass?: string;
    @Input() inner: any;
    @Input() card: any;
    @Input() trackLabel: any;
    @Input() trackCategory: any;
    @Input() trackAction: string;
    @Input() trackExpandOnly: boolean;
    @Input() isExpanded?: boolean;
    @Input() disabled?: boolean;
    @Input() pcTextBlock?: string;
    @Input() isHeaderHidden?: boolean;
    @Input() isChevronToLeft?: boolean;
    @Input() isShowAll?: boolean;
    @Input() accordionHeaderHtml: string;
    @Input() isSeoContent?: boolean = false;
    @Input() isBybState: boolean;
    @Input() chevronState: boolean;
    @Input() isByb?: boolean = false;
    @Input() isCustomElement?: boolean = false;
    @Input() eventEntity?: ISportEvent;
    @Input() showRaceDetails?: boolean = false;
    @Input() isBCH?: boolean = false;

    // eslint-disable-next-line @angular-eslint/no-output-rename
    @Output('function') func?= new EventEmitter();

    headerClasses: { [key: string]: boolean };

    private initialState = false;
    private memoryEnabled = false;

    constructor(
      protected accordionService: AccordionService,
      protected gtm: GtmService,
      protected changeDetectorRef: ChangeDetectorRef,
      protected pubsub: PubSubService
    ) { }
    /**
     * OnInit controller function
     */
    ngOnInit(): void {
        this.headerClasses = this.setHeaderClass();

        /* initial state for cashout */
        if (this.isExpanded === undefined && this.memoryId) {
            this.isExpanded = true;
        }
        this.initialState = this.isExpanded;
        // set first state for accordion
        this.setState(this.initialState);

        /* init remember state functionality for accordions */
        if (!this.disabled && this.memoryId) {
            this.initMemory(this.initialState);
            return;
        }

        this.pubsub.subscribe('accSocketUpdate', this.pubsub.API.WS_EVENT_UPDATE, () => {
            this.changeDetectorRef.detectChanges();
        });
    }

    /**
     * Triggered after inplayHRHeader(Lazy component) loaded
     */
    inplayHRHeaderLoaded(): void {
        this.changeDetectorRef.detectChanges();
    }

    /**
     * Set Header CSS Class
     * @returns {{toggle-header: boolean, inner-header: (string|boolean)}}
     */
    setHeaderClass(): { [key: string]: any } {
        const classes = {
            'toggle-header': !this.disabled,
            'inner-header': this.isCustomElement ? false : this.inner,
            'hr-header': this.isCustomElement && this.inner
        };
        if (this.headerClass) {
            classes[this.headerClass] = this.headerClass;
        }
        return classes;
    }

    setState(state: boolean): void {
        this.isExpanded = state;
        if (this.memoryEnabled) {
            this.accordionService.saveStateDependsOnParams(state, this.memoryId, this.memoryLocation);
        }
        this.changeDetectorRef.markForCheck();
    }

    trackToggle() {
        /**
         * Google analytics. Track collapses/expands
         */
        if (this.trackLabel && this.trackCategory) {
            if (this.trackExpandOnly && !this.isExpanded) {
                return;
            }
            const toogleTrackEvent: ITrackEvent = {
                event: 'trackEvent',
                eventCategory: this.trackCategory,
                eventAction: this.trackAction || (this.isExpanded ? 'show' : 'hide'),
                eventLabel: this.trackLabel
            };

            this.gtm.push(toogleTrackEvent.event, toogleTrackEvent);
        }
    }

  /**
   * Triggered on toggle.
   *
   * @param event
   */
  toggled(event: MouseEvent) {
        /* disable accordion functionality */
        if (this.disabled) {
            return;
        }

        this.setState(!this.isExpanded);

        this.trackToggle();

        if (this.func) {
            this.func.emit(this.isExpanded);
        }

        event.preventDefault();
        event.stopPropagation();

        this.changeDetectorRef.detectChanges();
    }

    /**
     * check if turn on ability to remember accordion state and depends on it set initial state
     * @param initialState {boolean}
     */
    initMemory(initialState) {
        let state = initialState;
        this.memoryEnabled = true;
        const savedState = this.memoryLocation ? this.accordionService.getLocationStates(this.memoryLocation)[this.memoryId]
            : this.accordionService.getState(this.memoryId);
        state = savedState !== null && savedState !== undefined ? savedState : initialState;
        this.setState(state);
    }

    ngOnDestroy(): void {
        this.pubsub.unsubscribe('accSocketUpdate');
    }
}
