import { Injectable } from '@angular/core';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { AsyncScriptLoaderService } from '@core/services/asyncScriptLoader/async-script-loader.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { APP_LOADED_SUBCRIBER, AWS_CONNECT_URL, AWSCONSTANTS } from '@lazy-modules/awsFirehose/constant/aws-firehose.constant';
import environment from '@environment/oxygenEnvConfig';
@Injectable({
  providedIn: 'root'
})

export class AWSFirehoseConnectService {
  private AWS_CONNECT_URL: string = AWS_CONNECT_URL;
  constructor(
    private windowRef: WindowRefService,
    private asyncScriptLoaderFactory: AsyncScriptLoaderService,
    private pubsubService: PubSubService
  ) {
    this.pubsubService.subscribe(APP_LOADED_SUBCRIBER, this.pubsubService.API.APP_IS_LOADED, () => this.intializeAWS());
  }

  /**
   * Creates connection to AWS and loads JS file
   * @returns void
   */
  private intializeAWS(): void {
    this.asyncScriptLoaderFactory.loadJsFile(this.AWS_CONNECT_URL)
      .subscribe(() => {
        if (this.windowRef.nativeWindow.AWS) {
          this.windowRef.nativeWindow.AWS.config.region = AWSCONSTANTS.REGION;
          this.windowRef.nativeWindow.AWS.config.credentials = new this.windowRef.nativeWindow.AWS.CognitoIdentityCredentials({
            IdentityPoolId: environment.IDENTITY_ID
          });
          if (this.windowRef.nativeWindow.AWS.config.credentials.needsRefresh()) {
            this.refreshAwsToken();
          }
          this.publishAWSLoaded();
        }
      });
  }

  /**
   * Refreshes token incase of expiration
   * @returns void
   */
  private refreshAwsToken(): void {
    this.windowRef.nativeWindow.AWS.config.credentials.get(() => { });
    this.windowRef.nativeWindow.AWS.config.credentials.refresh(() => this.publishAWSLoaded());
  }
  /**
   * Publish that AWS is Loaded
   * @returns void
   */
  private publishAWSLoaded(): void {
    if (!this.windowRef.nativeWindow.AWS.config.credentials.expired) {
      this.pubsubService.publish(this.pubsubService.API.INIT_AWS);
    }
  }

}
