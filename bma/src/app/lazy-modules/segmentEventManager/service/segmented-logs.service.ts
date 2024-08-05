import { Injectable } from "@angular/core";
import { PubSubService } from "@app/core/services/communication/pubsub/pubsub.service";
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';

@Injectable()
export class SegmentLogService {
    private title: string = 'segmented-aws-logs';
    private subscriberChannels = [this.pubsub.API.SEGMENT_RECEIVED, this.pubsub.API.SEGMENT_API_FAILED, this.pubsub.API.SEGMENTED_INITIAL_DATA_RECEIVED,
    this.pubsub.API.CMS_SEGMENT_API_FAILED];
    constructor(public awsFirehorseservice: AWSFirehoseService, public pubsub: PubSubService) {
        this.init();
    }
    init() {
        this.pubsub.subscribe(this.title, this.subscriberChannels, (data: { action: string }) => {
            this.awsFirehorseservice.addAction(data.action);
        });
    }
}