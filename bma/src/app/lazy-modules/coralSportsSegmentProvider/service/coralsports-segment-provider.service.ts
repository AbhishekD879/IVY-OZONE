import { Injectable } from '@angular/core';
import { VanillaApiService } from '@frontend/vanilla/core';
import { StorageService } from '@app/core/services/storage/storage.service';
import { ISegmentData } from '@lazy-modules/coralSportsSegmentProvider/model/segment-data.model';
import { UserService } from '@app/core/services/user/user.service';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { DeviceService } from '@app/core/services/device/device.service';
import { UserInterfaceClientConfig } from '@app/client-config/bma-user-interface-config';
import { BehaviorSubject} from 'rxjs';
import environment from '@environment/oxygenEnvConfig';

@Injectable({ providedIn: 'root' })
export class CoralSportsSegmentProviderService {
    private readonly SEGMENT_STORE_KEYTEXT: string = 'Segment';
    private readonly OTF_SEGMENT_STORE_KEYTEXT: string = 'OTF_SEGMENT';

    public isOTFAvailable: BehaviorSubject<any> = new BehaviorSubject({});

    constructor(private vanillaApiService: VanillaApiService,
        private pubsubService: PubSubService,
        private storageService: StorageService,
        private userService: UserService,
        private deviceService:DeviceService,
        private userInterfaceConfig: UserInterfaceClientConfig) { }

    /**
     * get segment value and bind to localstorage object
     */
    getSegmentDetails(firstTimeLogin?: boolean) {
        const segmentExpiryTime = this.userInterfaceConfig.cspSegmentExpiry ? this.userInterfaceConfig.cspSegmentExpiry : 15;
        const currentTime = new Date();
        const currentUTCHours = currentTime.getUTCHours();
        let expiryHours;
        if (currentUTCHours < segmentExpiryTime) {
            expiryHours = segmentExpiryTime - currentUTCHours;
        } else {
            expiryHours = (24 - currentUTCHours) + segmentExpiryTime;
        }
        currentTime.setHours(currentTime.getHours() + expiryHours);
        const expiryDateTime = currentTime.toUTCString();
        if (this.deviceService.requestPlatform === 'mobile') {
           
            this.getCoralSportsSegment().subscribe((segmentData: ISegmentData[]) => {
                const segmentDataValue= segmentData && segmentData.find((segment) => {
                    return segment.group.startsWith('CSP_');
                }); 
                const segmentValue =  segmentDataValue === undefined ? '' : 
                segmentDataValue.group;
                this.storageService.set(this.SEGMENT_STORE_KEYTEXT,
                    { user: this.userService.username, segment: segmentValue, timestamp: expiryDateTime });
                if (firstTimeLogin && segmentValue) {
                    this.pubsubService.publish(this.pubsubService.API.SEGMENT_RECEIVED, { action: 'GET_SEGMENT_API=>SUCCESS=>' + segmentValue });
                }
            }, err => {
                console.warn(err);
                this.storageService.set(this.SEGMENT_STORE_KEYTEXT, { user: this.userService.username, segment: '', timestamp: expiryDateTime });
                this.pubsubService.publish(this.pubsubService.API.SEGMENT_API_FAILED, { action: 'GET_SEGMENT_API=>FAILED' });
            });
        }
    }

    /**
     * calls coralSports API to return segment mapped to user
     * @returns Observable<ISegmentData[]>
     */
    public getCoralSportsSegment() {
        const APIOPTIONS: {
           [name:string]:string;
        } = {
            'prefix': '/en/coralsports'
        };

        return this.vanillaApiService.get('CampaignData', {},APIOPTIONS);
    }

    /**
     * calls OTF API to return user prediction status
     * @returns Observable<boolean>
     */
    public getOtfSegmentUserStatus(){
        this.getOtfUserStatusApi().subscribe(res =>{
             if(typeof res.status === 'boolean'){
                this.storageService.set(this.OTF_SEGMENT_STORE_KEYTEXT,{user: this.userService.username, segment:!res.status});
                this.isOTFAvailable.next(this.storageService.get(this.OTF_SEGMENT_STORE_KEYTEXT).segment);
                 return this.storageService.get(this.OTF_SEGMENT_STORE_KEYTEXT).segment;
             }else {
                return false;
             }        
        })
    }
    
    /**
     * calls predictionStatus API to return userStatus
     */
    private getOtfUserStatusApi(){
        const baseUrl = environment.ONE_TWO_FREE_API_ENDPOINT;
        const APIOPTIONS={
            headers:{
                ['token']:this.userService.bppToken
            }
        } as any;
        return this.vanillaApiService.get(`${baseUrl}/api/v1/predictionStatus/${this.userService.username}`,{},APIOPTIONS); 
    }
}
