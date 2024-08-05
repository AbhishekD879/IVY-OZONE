import { Component, OnInit, OnDestroy, ChangeDetectorRef } from "@angular/core";
import { FeaturedModuleService } from "@app/featured/services/featuredModule/featured-module.service";
import { PubSubService } from "@app/core/services/communication/pubsub/pubsub.service";
import { IFeaturedModel } from "@app/featured/models/featured.model";
import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { IOutputModule } from "@app/featured/models/output-module.model";
import { IVirtualHomePageSystemConfig } from "@app/core/services/cms/models/system-config";
import { DeviceService } from '@core/services/device/device.service';
import { IParams } from "@app/core/models/aem-banners-section.model";
import { VirtualHubService } from "@app/vsbr/services/virtual-hub.service";
import environment from '@environment/oxygenEnvConfig';
import { IVirtualSportsHomePage } from '@app/core/services/cms/models/virtual-sports.model';
import { Subject, Subscription, switchMap, takeUntil } from 'rxjs';
import { InplayConnectionService } from '@app/inPlay/services/inplayConnection/inplay-connection.service';
import { InplayMainService } from '@inplayModule/services/inplayMain/inplay-main.service';
import { IOffer } from '@core/models/aem-banners-section.model';

@Component({
    selector: 'virtual-home-page',
    templateUrl: './virtual-home-page.component.html',
    styleUrls: ['./virtual-home-page.component.scss']
})

export class VirtualHomePageComponent extends AbstractOutletComponent implements OnInit, OnDestroy {
    public titleTranslation: string = 'vsbr.virtualSports';
    public bannerName: string = 'virtuals';
    public VirtualRaceModules: IOutputModule;
    public isHorseracingVirtualsEnabled: boolean = false;
    public sportName: string = 'horseracing';
    public sportId: number = 21;
    public pageType: string = 'sport';
    private settings: IParams = {
        brand: 'coral',
        channel: 'desktop'
    }
    public topSportsImages: IVirtualSportsHomePage[] = [];
    public otherSportImages: IVirtualSportsHomePage[] = [];
    public virtualHubSystemConfig: IVirtualHomePageSystemConfig = {
        headerBanner: false,
        topSports: false,
        nextEvents: false,
        featureZone: false,
        otherSports: false
    };
    private connectSubscription: Subscription;
    private destroyHubSub:Subject<void> = new Subject();
    public virtualsLiveCount: any;
    public topSportsBGImage: string;
    public featuredZoneImages: IOffer[];
    public showLoader: boolean;
    public virtualShowLoader: boolean;
    public IsOnlyNextEventEnabled: boolean = false;
    public vsIconId: string;
    public readFSCFromCF: boolean = true;

    /**
     * Contructor
     */
    constructor(
        protected pubsub: PubSubService,
        protected cmsService: CmsService,
        protected featuredModuleService: FeaturedModuleService,
        protected virtualHubService: VirtualHubService,
        protected deviceService: DeviceService,
        protected inPlayConnectionService: InplayConnectionService,
        protected inPlayMainService: InplayMainService,
        protected changeDetectorRef: ChangeDetectorRef,
        protected pubsubService: PubSubService) {
        super();
    }

    /**
     * OnInit
     */
    ngOnInit(): void {
        this.showSpinner();
        this.showLoader = true;
        this.virtualShowLoader = true;
        this.virtualHubService.getCmsData().pipe(
            takeUntil(this.destroyHubSub)).subscribe((cmsData) => {
            if (cmsData) {
                const cmsVirtualSportsData: any = cmsData.cmsVirtualSportsData;
                this.virtualHubSystemConfig = cmsData.cmsConfig.VirtualHubHomePage;
                this.readFSCFromCF = !(cmsData.cmsConfig['UseFSCCached'] && cmsData.cmsConfig['UseFSCCached'].enabled === false);
                this.isHorseracingVirtualsEnabled = cmsData.cmsConfig.VirtualSports?.['virtual-horse-racing'] ?? false;

                if (this.virtualHubSystemConfig.topSports || this.virtualHubSystemConfig.otherSports || this.virtualHubSystemConfig.featureZone) {
                    this.loadCmsAndSiteCoreImageConfig(cmsVirtualSportsData);
                    this.loadNumberIndicator();
                } else {
                    this.showLoader = false;
                }

                if (this.virtualHubSystemConfig.nextEvents) {
                    this.loadNextEvents();
                } else {
                    this.virtualShowLoader = false;
                }
            }
            this.hideSpinner();
        },
        (error) =>{
            this.hideSpinner();
            this.showLoader = false;
            this.virtualShowLoader = false;
        }
        )
    }

    /**
     * loadCmsAndSiteCoreImageConfig
     */
    private loadCmsAndSiteCoreImageConfig(cmsVirtualSportsData: any): void {
        this.settings.brand = environment.brand;
        this.settings.channel = this.deviceService.getDeviceViewType()?.mobile ? 'mobile':'desktop';
        this.virtualHubService.fetchVirtualImagesFromSiteCore(this.settings, cmsVirtualSportsData, this.virtualHubSystemConfig).subscribe((virtualSportsInfo) => {
            if (virtualSportsInfo) {
                this.topSportsImages = virtualSportsInfo.topSports;
                this.otherSportImages = virtualSportsInfo.otherSports;
                this.featuredZoneImages = virtualSportsInfo.featureZoneOffers;
                this.topSportsBGImage = this.getBGImageUrl();
            }
            this.showLoader = false;
        },
        (error) => {
            this.showLoader = false;
        }
        );
    }

    /**
     * loadNextEvents
     */
    private loadNextEvents(): void {
        if (this.readFSCFromCF) {
            this.cmsService.getFSC(this.sportId.toString())
                .subscribe((featured: IFeaturedModel) => {
                    this.featuredModuleService.trackDataReceived(featured, 'FEATURED_STRUCTURE_CHANGED');
                    this.VirtualRaceModules = featured.modules.find((module) => module['@type'] === 'VirtualRaceModule');
                    this.IsOnlyNextEventEnabled = this.validateNextEventEnabled();
                    this.pubsub.publish(this.pubsub.API.FEATURED_STRUCTURE_CHANGED, []);
                    this.virtualShowLoader = false;
                },
                    (error) => {
                        this.virtualShowLoader = false;
                    });
        }
        else {
            this.pubsub.subscribe('featuredModule', this.pubsub.API.FEATURED_CONNECT_STATUS, (isConnected: boolean) => {
                if (isConnected) {
                    this.featuredModuleService.addEventListener('FEATURED_STRUCTURE_CHANGED', (featured: IFeaturedModel) => {
                        this.VirtualRaceModules = featured.modules.find((module) => module['@type'] === 'VirtualRaceModule');
                        this.IsOnlyNextEventEnabled = this.validateNextEventEnabled();
                        this.virtualShowLoader = false;
                    });
                    this.virtualShowLoader = false;
                } else {
                    this.virtualShowLoader = false;
                }
            });
        }
        this.featuredModuleService.startConnection(this.sportId, this.pageType);
    }

    /**
     * loadNumberIndicator
     */
    private loadNumberIndicator(): void {
        this.connectSubscription = this.inPlayConnectionService.connectComponent().pipe(
            switchMap(() => {
                // inPlay Virtual Sports Live Count functionality
                return this.inPlayMainService.getVirtualsData();
            })
        ).subscribe((data: any) => {
            this.virtualsLiveCount = data;
            this.changeDetectorRef.detectChanges();
        })

        // Update Event Counter
        this.pubsubService.subscribe('virtuals', this.pubsubService.API.VIRTUAL_EVENT_COUNT_UPDATE,
            (data: any[]) => {
                this.virtualsLiveCount = data;
                this.changeDetectorRef.detectChanges();
            });
    }

    /**
     * getBGImageUrl
     */
    getBGImageUrl(): string {
        const bgImageOffer: IOffer = this.virtualHubService.siteCoreOffers.find(offer => offer.Id === this.virtualHubSystemConfig.topSportsBackgroundID);
        const bgImageUrl: string = bgImageOffer ? bgImageOffer.imgUrl : null;
        return bgImageUrl;
    }

    /**
     * validateNextEventEnabled()
     */
    private validateNextEventEnabled() {
        if (this.virtualHubSystemConfig.nextEvents && !this.virtualHubSystemConfig.topSports && !this.virtualHubSystemConfig.otherSports
            && !this.virtualHubSystemConfig.featureZone && !this.virtualHubSystemConfig.headerBanner) {
            return true;
        } else {
            return false;
        }
    }

    /**
     * ngOnDestroy
     */
    ngOnDestroy(): void {
        this.connectSubscription?.unsubscribe();
        this.destroyHubSub.next();
        this.destroyHubSub.complete();
        this.inPlayMainService.unsubscribeForVRUpdates();
    }

}