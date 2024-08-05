import { Injectable } from '@angular/core';
import { StorageService } from '@app/core/services/storage/storage.service';
import { UserService } from '@app/core/services/user/user.service';

@Injectable({ providedIn: 'root' })
export class SegmentCacheManagerService {
    isChanged: boolean = false;
    private readonly SEGMENT_STORE_KEYTEXT: string = 'Segment';

    constructor(private storageService: StorageService,
        private userService: UserService) { }

    /**
     * validate segment expiry. Any login post the day change should clear the segment
     * @returns boolean value
     */
    isCacheAvailable(): boolean {
        if (this.storageService.get(this.SEGMENT_STORE_KEYTEXT)) {
            this.isSegmentChanged(false);
            let storedTimeStamp = this.storageService.get(this.SEGMENT_STORE_KEYTEXT).timestamp;
            storedTimeStamp = new Date(storedTimeStamp);
            const currentDateTime = new Date(new Date().toUTCString());
            //Check for ExpiryDateTime of segment expiry.
            if (storedTimeStamp < currentDateTime) {
                this.isSegmentChanged(true);
                return false;
            }
            return true;
        }
        return false;
    }

    /**
     * validate whether segment value is changed or not
     * @param change boolean
     * @returns boolean
     */
    isSegmentChanged(change: boolean): boolean {
        return this.isChanged = change;
    }
}
