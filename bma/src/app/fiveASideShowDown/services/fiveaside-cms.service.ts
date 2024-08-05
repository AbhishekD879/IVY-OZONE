import { HttpClient, HttpResponse } from '@angular/common/http';
import { Inject, Injectable } from '@angular/core';
import { CmsService } from '@app/core/services/cms/cms.service';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { FiveASideShowDownApiModule } from '@app/fiveASideShowDown/fiveASideShowDown-api.module';
import { IFAQ } from '@core/services/cms/models/frequently-asked-question';
import { ITermsAndConditions } from '@core/services/cms/models/terms-and-conditions';
import { IWelcomeOverlay } from '@app/fiveASideShowDown/models/welcome-overlay';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { CmsToolsService } from '@app/core/services/cms/cms.tools';
import { DeviceService } from '@app/core/services/device/device.service';
import { CoreToolsService } from '@app/core/services/coreTools/core-tools.service';
import { CasinoLinkService } from '@app/core/services/casinoLink/casino-link.service';
import { NativeBridgeService } from '@app/core/services/nativeBridge/native-bridge.service';
import { UserService } from '@app/core/services/user/user.service';
import { IInitialData } from '@app/core/services/cms/models';
import { SegmentEventManagerService } from '@lazy-modules/segmentEventManager/service/segment-event-manager.service';
import { SegmentedCMSService } from '@app/core/services/cms/segmented-cms.service';
import { FanzoneStorageService } from '@app/core/services/fanzone/fanzone-storage.service';

@Injectable({ providedIn: FiveASideShowDownApiModule })
export class FiveASideCmsService extends CmsService {

    constructor(
        protected pubsub: PubSubService,
        protected cmsTools: CmsToolsService,
        protected device: DeviceService,
        protected http: HttpClient,
        protected coreToolsService: CoreToolsService,
        protected fanzoneStorageService: FanzoneStorageService,
        protected casinoDecoratorService: CasinoLinkService,
        protected nativeBridgeService: NativeBridgeService,
        protected userService: UserService,
        protected segmentEventManagerService: SegmentEventManagerService,
        protected segmentedCMSService: SegmentedCMSService,
        @Inject('CMS_CONFIG') protected cmsInitConfigPromise: Promise<IInitialData>
    ) {
        super(pubsub, cmsTools, device, http, coreToolsService, fanzoneStorageService,
            casinoDecoratorService, nativeBridgeService, userService,
            segmentEventManagerService, segmentedCMSService, cmsInitConfigPromise);
    }
    /**
     * @returns Observable
     */
    getFAQs(): Observable<IFAQ[]> {
        return this.getData(`faq`)
            .pipe(
                map((data: HttpResponse<IFAQ[]>) => data.body)
            );
    }

    /**
     * To fetch terms and conditions
     * @returns {ITermsAndConditions}
     */
    getTermsAndConditions(): Observable<ITermsAndConditions> {
        return this.getData(`termsandcondition`)
            .pipe(
                map((data: HttpResponse<ITermsAndConditions>) => data.body)
            );
    }

    /**
     * To fetch overlay Content
     * @returns {Observable<IWelcomeOverlay}
     */
    getWelcomeOverlay(): Observable<IWelcomeOverlay> {
        return this.getData(`overlay`)
            .pipe(
                map((data: HttpResponse<IWelcomeOverlay>) => data.body)
            );
    }
}
