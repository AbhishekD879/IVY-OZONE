import { Component, Input, OnInit } from '@angular/core';
import environment from '@environment/oxygenEnvConfig';
import { DomSanitizer, SafeUrl } from '@angular/platform-browser';
import { IEventVisParams } from '@core/services/visEvent/vis-event.model';

import * as _ from 'underscore';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';

@Component({
  selector: 'visualization-container',
  templateUrl: './visualization-container.component.html'
})
export class VisualizationContainerComponent implements OnInit {
  @Input() eventId: string;
  @Input() visType: string;
  @Input() visParams: IEventVisParams[];
  @Input() expandable: boolean;
  @Input() isHidden: boolean;

  isVisualizationAvailable: boolean;
  isExpanded: boolean = false;
  delta: number;
  iframeURL: SafeUrl;
  dimensionMultiplier: number = 0;
  private VISUALIZATION_IFRAME_URL: string = environment.VISUALIZATION_IFRAME_URL;
  private eventParams: IEventVisParams;
  private sportName: string;
  private canDisplayCastro: boolean;
  private visUrl: string;

  constructor(
    private domSanitizer: DomSanitizer,
    private pubSubService: PubSubService
  ) {}

  ngOnInit(): void {
    this.eventParams = _.find(this.visParams, event => event.id === this.eventId);
    this.canDisplayCastro = !_.isEmpty(this.eventParams) ? this.eventParams.canDisplayCastro : false;

    // If it is castro widget and canDisplayCastro === false, do not display visualization
    this.isVisualizationAvailable = (this.visType === 'castro' &&
      !this.canDisplayCastro) ? false : !_.isEmpty(this.eventParams);
    this.sportName = !_.isEmpty(this.eventParams) ? this.eventParams.sportName : 'football';

    // Correction for iframe height
    this.delta = (this.sportName === 'tennis') ? 33 : 0;

    this.visUrl = (this.sportName === 'tennis') ? `${this.sportName}-iframe.html`
      : `${this.sportName}/iframe.html`;

    if (!this.expandable) {
      this.visualize();
    }
  }

  /**
   * URL of visualization Iframe, since it needs to be compound from different variables,
   * we need to use $sce.trustAsResourceUrl
   */
  visualize(): void {
    this.iframeURL = this.domSanitizer.bypassSecurityTrustResourceUrl(
      `${this.VISUALIZATION_IFRAME_URL}/${this.visUrl}#${this.eventId}:${this.visType}`);
  }

  loadHandler(): void {
    this.pubSubService.publish(this.pubSubService.API.SCOREBOARD_VISUALIZATION_LOADED);
  }
}
