import { Injectable } from '@angular/core';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { RoutingState } from '@app/shared/services/routingState/routing-state.service';
import { CoralSportsSegmentProviderService } from '@lazy-modules/coralSportsSegmentProvider/service/coralsports-segment-provider.service';
import { SegmentCacheManagerService } from '@lazy-modules/coralSportsSegmentProvider/service/segment-cache-manager.service';
import { StorageService } from '@app/core/services/storage/storage.service';
import { UserService } from '@app/core/services/user/user.service';
import { DeviceService } from '@app/core/services/device/device.service';

@Injectable({ providedIn: 'root' })
export class SegmentEventManagerService {
    private title: string = 'segment-event-manager';
    private readonly SEGMENT_STORE_KEYTEXT: string = 'Segment';
    private readonly OTF_SEGMENT_STORE_KEYTEXT: string = 'OTF_SEGMENT';
    constructor(
        private pubsubService: PubSubService,
        private route: RoutingState,
        private coralSportsSegmentProviderService: CoralSportsSegmentProviderService,
        private segmentCacheManagerService: SegmentCacheManagerService,
        private storageService: StorageService,
        private userService: UserService,
        private deviceService: DeviceService) {
        this.subscriptionForMobile();
        this.pubsubService.subscribe(this.title, this.pubsubService.API.SESSION_LOGOUT, () => {
           this.storageService.remove(this.OTF_SEGMENT_STORE_KEYTEXT);
        });
    }

    subscriptionForMobile() {
        if (this.deviceService.requestPlatform === 'mobile') {
            this.pubsubService.subscribe(this.title, [this.pubsubService.API.SESSION_LOGIN], this.getSegment.bind(this));
            this.pubsubService.subscribe(this.title, [this.pubsubService.API.SEGMENTED_INITIAL_DATA_RECEIVED], () => {
                this.pubsubService.publish(this.pubsubService.API.SEGMENTED_INIT_FE_REFRESH);
            });
        }
    }

    /**
     * On successfull login, this method publishes segmented page refresh provided user falls under segment
     */
    getSegment(): void {
       this.getSegmentDetails(true);
    }

    /**
     * Method checks for segment expiry before hitting the coralSports API
     * @param firstTimeLogin boolean
     * @returns segment string
     */
    getSegmentDetails(firstTimeLogin: boolean = false): string {
        const cacheAvailable: boolean = this.segmentCacheManagerService.isCacheAvailable();
        const segmentValue = this.storageService.get(this.SEGMENT_STORE_KEYTEXT)?.segment;
        if (firstTimeLogin) {
            if (this.chkIsLoggedInUserDiff() || !cacheAvailable) {
                this.coralSportsSegmentProviderService.getSegmentDetails(true);
            } else {
                segmentValue && this.pubsubService.publish(this.pubsubService.API.SEGMENT_RECEIVED,
                    { action: 'SEGMENT_RECEIVED=>FIRST_LOGIN_CACHE=>' + segmentValue });
            }
        } else if (!this.chkIsLoggedInUserDiff() && cacheAvailable) {
                return segmentValue;
        } else {
            this.coralSportsSegmentProviderService.getSegmentDetails(true);
        }
        return '';
    }

    /**
     * true if current loggedInUser is different to previous loggedIn
     * @returns boolean value
     */
    chkIsLoggedInUserDiff(): boolean {
        return this.userService.username !== this.storageService.get(this.SEGMENT_STORE_KEYTEXT)?.user;
    }

    /**
     * check for current URL if not featured then CMS init call for specific modules
     * e.g.footer-menu = true (if home or any other pages); 
     * e.g.super-button = true (only for home); false (other pages shld call universal CMS init call)
     * @param segmentMandate boolean
     * @returns boolean true/false
     */
    chkModuleForSegmentation(segmentMandate: boolean): boolean {
        if (!segmentMandate) {
            const currentRoute = this.route.getCurrentUrl();
            const [baseURL] = currentRoute.split('?');
            return (baseURL === '/' || baseURL === '/home/featured' || baseURL === '');
        }
        return true;
    }

    /**
     * check for OTF Segment User Status
     */
    getOtfSegmentUserStatus() {
        if (!this.chkIsLoggedInUserDiff() && this.storageService.get(this.OTF_SEGMENT_STORE_KEYTEXT)) {
            return this.storageService.get(this.OTF_SEGMENT_STORE_KEYTEXT).segment
        } else {
            return this.coralSportsSegmentProviderService.getOtfSegmentUserStatus();
        }
    }

}
