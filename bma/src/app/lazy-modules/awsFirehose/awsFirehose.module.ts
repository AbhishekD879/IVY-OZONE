import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { AWSFirehoseConnectService } from '@lazy-modules/awsFirehose/service/aws-firehose-connect.service';

@NgModule({
  providers: [AWSFirehoseConnectService],
  schemas: [NO_ERRORS_SCHEMA]
})

export class AWSFirehoseModule {
  constructor(private awsFirehoseConnectService: AWSFirehoseConnectService) {
  }
}
