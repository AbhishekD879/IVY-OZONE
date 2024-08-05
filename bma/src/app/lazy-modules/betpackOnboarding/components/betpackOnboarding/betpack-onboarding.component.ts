import { Component, OnInit, Output, EventEmitter, Input } from '@angular/core';
import environment from '@environment/oxygenEnvConfig';
import { BetpackCmsService } from '@app/lazy-modules/betpackPage/services/betpack-cms.service';
import { CarouselService } from '@shared/directives/ng-carousel/carousel.service';
import { Carousel } from '@app/shared/directives/ng-carousel/carousel.class';
import { StorageService } from '@core/services/storage/storage.service';
import { RendererService } from '@shared/services/renderer/renderer.service';
import { UserService } from '@core/services/user/user.service';
import { BetPackOnBoardingCMSConfig, OnBoardingImageCollection } from '@app/lazy-modules/betpackOnboarding/models/betpack-onboarding.model';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { DeviceService } from '@coreModule/services/device/device.service';
import { GtmService } from 'app/core/services/gtm/gtm.service';
import { ITrackEvent } from '@core/services/gtm/models';
import { BETPACK_ONBOARDING_CONSTANTS } from '@app/lazy-modules/betpackOnboarding/constants/betpack-onboarding.constants';
import { STRATEGY_TYPES } from '@app/core/constants/strategy-types.constant';

@Component({
    selector: 'betpack-onboarding',
    templateUrl: './betpack-onboarding.component.html',
    styleUrls: ['./betpack-onboarding.component.scss']
})

export class BetpackOnboardingComponent implements OnInit {

    @Input() public onBoardingType: string = BETPACK_ONBOARDING_CONSTANTS.ONBOARDING;
    @Input() public storageKey: string = BETPACK_ONBOARDING_CONSTANTS.BETPACK;
    @Output() public closeOnboardingEmitter: EventEmitter<any> = new EventEmitter();

    public timePerSlide: number = 897000;
    public isLoading: boolean = true;
    public onboardingInfo: BetPackOnBoardingCMSConfig;
    public carouselName: string = BETPACK_ONBOARDING_CONSTANTS.BETPACK_ONBOARDING;
    changeStrategy = STRATEGY_TYPES.ON_PUSH;

    private cmsUri: string = environment.CMS_ROOT_URI;

    constructor(
        private carouselService: CarouselService,
        private betpackCmsService: BetpackCmsService,
        private storageService: StorageService,
        private rendererService: RendererService,
        private userService: UserService,
        private windowRef: WindowRefService,
        private device: DeviceService,
        private gtmService: GtmService
    ) {
    }

    ngOnInit(): void {
        if (this.windowRef.nativeWindow.innerWidth < this.device.mobileWidth) {
            this.betpackCmsService.getBetPackOnboarding().subscribe(onBoardingData => {
                if (onBoardingData && onBoardingData.isActive && onBoardingData.images) {
                    onBoardingData.images = onBoardingData.images.filter(betData => betData.imageType.toLowerCase() === this.onBoardingType.toLowerCase());
                    this.onboardingInfo = onBoardingData;
                    this.isOnBoardingTooltipSeen();
                    this.handleGATracking('launch');
                }
                this.isLoading = false;
                this.onBoardingIsActiveCheck();
            }, (error) => {
                this.onBoardingIsActiveCheck();
            });
            this.rendererService.renderer.addClass(document.body, BETPACK_ONBOARDING_CONSTANTS.MENU_OPENED);
        } else {
            this.onBoardingIsActiveCheck();
        }
    }


    public nextSlide(betPackImage: OnBoardingImageCollection, index: number): void {
        if (betPackImage && betPackImage.nextCTAButtonLabel && betPackImage.nextCTAButtonLabel.toLowerCase() === 'finish') {
            this.handleGATracking(betPackImage.nextCTAButtonLabel.toLowerCase());
            this.closeOnboardingEmitter.emit('');
        } else {
            const stepNum: number = index ? index + 1 : 1;
            const eventLabelTxt: string = `${betPackImage.nextCTAButtonLabel.toLowerCase()} - step ${stepNum}`;
            this.handleGATracking(eventLabelTxt);
            this.bannersCarousel.next();
        }
    }

    public prevSlide(): void {
        this.bannersCarousel.previous();
    }

    public onCloseOnboardingOverlay(event: any, betPackImage: OnBoardingImageCollection): void {
        if (betPackImage && betPackImage.nextCTAButtonLabel
            && betPackImage.nextCTAButtonLabel.toLowerCase() === 'finish'
            && this.onBoardingType.toLowerCase() === BETPACK_ONBOARDING_CONSTANTS.ONBOARDING.toLowerCase()) {
            this.handleGATracking(betPackImage.nextCTAButtonLabel.toLowerCase());
        } else {
            this.handleGATracking('close');
        }
        this.closeOnboardingEmitter.emit(event);
    }

    public getImageSrc(betPackImage: OnBoardingImageCollection): string {
        let bpmpOnboardingImage: string = '';
        if (betPackImage) {
            bpmpOnboardingImage = `${this.cmsUri}${betPackImage.onboardImageDetails.path}/${betPackImage.onboardImageDetails.filename}`;
        }
        return bpmpOnboardingImage;
    }

    private handleGATracking(eventLabelValue: string): void {
        const trackEventData: ITrackEvent = {
            event: 'trackEvent',
            eventAction: this.getEventAction(),
            eventCategory: 'bet bundles marketplace',
            eventLabel: eventLabelValue
        };

        this.gtmService.push('trackEvent', trackEventData);
    }

    private isOnBoardingTooltipSeen(): void {
        const onBoardingData: any = this.storageService.get(BETPACK_ONBOARDING_CONSTANTS.ONBOARDING_TUTORIAL) || {};
        onBoardingData[`${this.storageKey}-${this.userService.username}`] = true;
        this.storageService.set(BETPACK_ONBOARDING_CONSTANTS.ONBOARDING_TUTORIAL, onBoardingData);
    }

    private onBoardingIsActiveCheck(): void {
        if (!this.onboardingInfo
            || (this.onboardingInfo && !this.onboardingInfo.isActive)
            || (this.onboardingInfo && this.onboardingInfo.images.length === 0)) {
            this.closeOnboardingEmitter.emit('');
        }
    }

    private get bannersCarousel(): Carousel {
        return this.carouselService.get(this.carouselName);
    }

    private set bannersCarousel(value: Carousel) { }

    private getEventAction(): string {
        if (this.onBoardingType.toLowerCase() === BETPACK_ONBOARDING_CONSTANTS.BETREVIEW.toLowerCase()) {
            return 'onboarding receipt';
        } else {
            return 'onboarding';
        }
    }

    // Removes menu-opened class from body on component destroy
    ngOnDestroy() {
        this.rendererService.renderer.removeClass(document.body, BETPACK_ONBOARDING_CONSTANTS.MENU_OPENED);
    }

}
