import { Component, Input, OnInit } from '@angular/core';
import environment from '@environment/oxygenEnvConfig';
import { DomSanitizer, SafeUrl } from '@angular/platform-browser';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';

@Component({
  selector: 'vis-pre-match-widget',
  templateUrl: './vis-pre-match-widget.component.html'
})
export class VisPreMatchWidgetComponent implements OnInit {
  @Input() eventId: string;

  dimensionMultiplier: number = 0;
  visType: string = 'slider';
  iframeURL: SafeUrl;
  private VISUALIZATION_PREMATCH_URL: string = environment.VISUALIZATION_PREMATCH_URL;

  constructor(
    private domSanitizer: DomSanitizer,
    private pubSubService: PubSubService
  ) {}

  ngOnInit(): void {
    this.iframeURL = this.domSanitizer.bypassSecurityTrustResourceUrl(`${this.VISUALIZATION_PREMATCH_URL}#${this.eventId}`);
  }

  loadHandler(): void {
    this.pubSubService.publish(this.pubSubService.API.SCOREBOARD_VISUALIZATION_LOADED);
  }
}
