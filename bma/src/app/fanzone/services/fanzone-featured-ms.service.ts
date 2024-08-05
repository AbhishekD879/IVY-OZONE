import { Injectable } from "@angular/core";
import { FeaturedModuleService } from "@featured/services/featuredModule/featured-module.service";
import { CacheEventsService } from "@core/services/cacheEvents/cache-events.service";
import { CommentsService } from "@core/services/comments/comments.service";
import { PubSubService } from "@core/services/communication/pubsub/pubsub.service";
import { TimeSyncService } from "@core/services/timeSync/time-sync.service";
import { AWSFirehoseService } from "@lazy-modules/awsFirehose/service/aws-firehose.service";
import { LiveEventClockProviderService } from "@shared/components/liveClock/live-event-clock-provider.service";
import { SegmentEventManagerService } from "@lazy-modules/segmentEventManager/service/segment-event-manager.service";
import { UserService } from "@app/core/services/user/user.service";
import { DeviceService } from "@app/core/services/device/device.service";
import { WebSocketService } from "@core/services/wsConnector/websocket.service";

@Injectable()
export class FanzoneFeaturedService extends FeaturedModuleService {
    constructor(cacheEventsService: CacheEventsService,
        commentsService: CommentsService,
        timeSyncService: TimeSyncService,
        liveEventClockProviderService: LiveEventClockProviderService,
        pubSubService: PubSubService,
        awsService: AWSFirehoseService,
        segmentEventManagerService: SegmentEventManagerService,
        userService: UserService,
        device: DeviceService,
        websocketService: WebSocketService) {
        super(cacheEventsService, commentsService, timeSyncService, liveEventClockProviderService, pubSubService, awsService, segmentEventManagerService,userService,device,websocketService);
      
    }

}