import { pubSubApi } from '@app/core/services/communication/pubsub/pubsub-api.constant';
import { SegmentLogService } from './segmented-logs.service';

describe('SegmentLogService', () => {
    let service: SegmentLogService,
        awsFirehorseservice,
        pubsubService;

    beforeEach(() => {
        pubsubService = {
            publish: jasmine.createSpy('publish'),
            subscribe: jasmine.createSpy('subscribe').and.callFake((fileName: string, method: string, callback: Function) => {
                callback({action:'test=>action'});
            }),
            API: pubSubApi
        };
        awsFirehorseservice = {
            addAction: jasmine.createSpy('addAction')
        };
        service = new SegmentLogService(
            awsFirehorseservice, pubsubService
        );
    });
    describe('#init', () => {
        it('init subscribe', () => {
            service.init();
            expect(awsFirehorseservice.addAction).toHaveBeenCalled();
        })

    })
});
