import { Component, ChangeDetectionStrategy, ChangeDetectorRef, SimpleChanges, EventEmitter, Input, OnInit, Output, OnDestroy } from "@angular/core";
import { Event, NavigationEnd, Router } from "@angular/router";
import { Location } from '@angular/common';
import { Subscription } from "rxjs";
import { PubSubService } from "@app/core/services/communication/pubsub/pubsub.service";
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { FirstBetGAService } from "../services/first-bet-ga.service";
import { SessionStorageService } from "@app/core/services/storage/session-storage.service";
import { IFirstBetDetails } from "@app/lazy-modules/onBoardingTutorial/firstBetPlacement/model/first-bet-placement.model";
import { UserService } from "@app/core/services/user/user.service";
import { STRATEGY_TYPES } from "@app/core/constants/strategy-types.constant";

interface IStepsModel {
    title: string;
    description: string;
    step: number;
    totalStesp: number;
}

@Component({
    selector: 'first-bet-placement',
    templateUrl: 'first-bet-placement.component.html',
    styleUrls: ['./first-bet-placement.component.scss'],
    changeDetection: ChangeDetectionStrategy.OnPush,
})

export class OnBoardingFirstBetComponent implements OnInit, OnDestroy {
    progressData: any;
    firstBetTutorialData: IFirstBetDetails;
    isExpanded: boolean = true;
    accordionHeader: string;
    activeStep: IStepsModel | any; // need to change any with other interface later.
    contentButtons = ['betPlaced', 'myBets'];
    isCloseTutorial: boolean = false;
    closeIconCheck: boolean = true;
    user: UserService;
    @Input() onBoardingData: any;
    @Input() isDigitKeyboardShown: boolean;
    @Output() readonly dismissAction: EventEmitter<boolean> = new EventEmitter();
    showButton: boolean;
    buttonText: string = 'NEXT';
    firstBetTutorialAvailable: boolean;
    hideTutorial: boolean;
    canBoostSelection: boolean = false;
    changeStrategy = STRATEGY_TYPES.ON_PUSH;
    private routeListener: Subscription;
    tutorialSteps = {
        pickYourBet: { step: 1, totalSteps: 5 },
        placeYourBet: { step: 2, totalSteps:5},
        addSelection: { step: 2, totalSteps: 5 },
        betSlip: { step: 3, totalSteps: 5 },
        betPlaced: { step: 3, totalSteps: 5 },
        winAlert: { step: 3, totalSteps: 5 },
        betDetails: { step: 4, totalSteps: 5 },
        myBets: { step: 5, totalSteps: 5 }
    }

    betsPaths = ['/open-bets','/cashout','/bet-history','/in-shop-bets'];

    constructor(private session: SessionStorageService, protected pubSubService: PubSubService, private cdr: ChangeDetectorRef, private windowRef: WindowRefService,
        private firstBetGAService: FirstBetGAService, protected userService: UserService, protected router: Router,
         protected location: Location) {
            this.user = this.userService;
         }

    ngOnInit() {
        this.firstBetHandler(true);
        this.subscribeToRouteChange();
    }

    ngOnChanges(changes: SimpleChanges) {
        if (changes.onBoardingData?.currentValue) {
            this.onBoardingData = changes.onBoardingData.currentValue;
            this.canBoostSelection = this.onBoardingData && this.onBoardingData.type === 'boost';
            this.firstBetHandler(this.isExpanded);
        } else if (changes.isDigitKeyboardShown) {
            this.isExpanded = !changes.isDigitKeyboardShown.currentValue;
            this.expand(this.isExpanded);
            this.cdr.detectChanges();
        }
    }

    firstBetHandler(toggleAccordion?) {
        this.hideTutorial = false;
        this.firstBetTutorialAvailable = this.session.get('firstBetTutorialAvailable');
        if (this.onBoardingData && this.onBoardingData.step && this.firstBetTutorialAvailable) {
            this.firstBetTutorialData = this.session.get('firstBetPlacementDetails');
            this.getActiveStepData(this.onBoardingData.step, this.onBoardingData.type);
            this.expand(toggleAccordion);
            this.windowRef.document.getElementById('footer-menu-nav').classList.add('paddingBtm');
    }
        this.cdr.detectChanges();
    }

    getActiveStepData(key, type?) {
        this.showButton = false;
        const activeObj = this.firstBetTutorialData[key];
        if (activeObj.hasOwnProperty(type)) {
            this.activeStep = { ...this.firstBetTutorialData[key][type], ...this.tutorialSteps[key] };
            const buttonObj = this.firstBetTutorialData[key]['buttonDesc'];
            this.buttonText = buttonObj ? buttonObj : this.buttonText;
        } else {
            this.activeStep = { ...this.firstBetTutorialData[key], ...this.tutorialSteps[key] };
        }
        if (this.contentButtons.indexOf(key) > -1) {
            this.showButton = true;
        }
        this.closeIconCheck = this.activeStep.step !== 5;
        if (!this.canBoostSelection) {
            this.firstBetGAService.setGtmData('contentView', 'load', `step ${this.activeStep.step}`, this.activeStep.title);
        } else {
            this.canBoostSelection = false;
        }
    }

    expand(toggleAccordion?) {
        this.isExpanded = toggleAccordion !== undefined ? toggleAccordion : !this.isExpanded;
        this.accordionHeader = `Step ${this.activeStep.step}/${this.activeStep.totalSteps}`;
    }

    handleNextClick() {
        this.session.set('buttonText', this.buttonText);
        if (this.buttonText === this.firstBetTutorialData.myBets.buttonDesc) {
            this.removeSession();
        } else {
            const dom = this.windowRef.document;
            if (dom.querySelector('.qb-header-close-btn')) {
                const elem: HTMLElement = dom.querySelector('.qb-header-close-btn');
                elem.click();
            } else if (dom.querySelector('.sidebar-close')) {
                const elem: HTMLElement = dom.querySelector('.sidebar-close');
                const currentType = this.session.get('cashOutAvail') ? 'cashOut' : 'defaultContent';
                this.pubSubService.publish(this.pubSubService.API.FIRST_BET_PLACEMENT_TUTORIAL,
                    { step: 'betDetails', tutorialEnabled: true, type: currentType });
                elem.click();
            }
        }
        this.firstBetGAService.setGtmData('Event.Tracking', 'click', `step ${this.activeStep.step}`, `${this.buttonText} cta`);
    }
    
    openUndo(): void {
        this.isCloseTutorial = true;
        this.firstBetGAService.setGtmData('Event.Tracking','close', `step ${this.activeStep.step}`, `${this.activeStep.title}`, `Step ${this.activeStep.step}`);
    }

    closeUndo(): void {
        this.isExpanded = false;
        this.expand();
        this.isCloseTutorial = false;
        this.firstBetGAService.setGtmData('Event.Tracking','click', `step ${this.activeStep.step}`, `${this.firstBetTutorialData.button.leftButtonDesc} cta`);
    }

    dismiss(): void {
        this.dismissAction.emit(this.isCloseTutorial);
        this.isCloseTutorial = false;
        this.firstBetTutorialAvailable = false;
        this.removeSession();
        this.pubSubService.publish(this.pubSubService.API.FIRST_BET);
        this.cdr.detectChanges();
        this.firstBetGAService.setGtmData('Event.Tracking','click', `step ${this.activeStep.step}`, `${this.firstBetTutorialData.button.rightButtonDesc} cta`);
    }

    ngOnDestroy(): void {
        this.routeListener && this.routeListener.unsubscribe();
    }

    private removeSession(): void {
        this.session.remove('firstBetPlacementDetails');
        this.session.remove('firstBetTutorialAvailable');
        this.windowRef.document.getElementById('footer-menu-nav').classList.remove('paddingBtm');
        this.session.remove('betPlaced');
        this.session.remove('initialTabLoaded');
        this.session.remove('tutorialCompleted');
        this.session.remove('buttonText');
        this.isCloseTutorial = false;
        this.firstBetTutorialAvailable = false;
        this.cdr.detectChanges();
        this.session.set('firstBetTutorial', { user: this.session.get('firstBetTutorial').user, firstBetAvailable: this.isCloseTutorial });
    }

    private subscribeToRouteChange(): void {
        this.routeListener = this.router.events.subscribe((event: Event) => {
        if (event instanceof NavigationEnd) {
            const currentPath = this.location.path();
            this.hideTutorial = this.location.path() === '/in-shop-bets';
            if(!this.betsPaths.includes(currentPath) && this.session.get('tutorialCompleted')) {
                this.removeSession();
                this.isCloseTutorial = this.firstBetTutorialAvailable = false;
            }
            this.cdr.detectChanges();
        }
    })}
}