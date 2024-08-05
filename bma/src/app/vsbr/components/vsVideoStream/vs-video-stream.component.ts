import { Component, Input, OnChanges, ChangeDetectionStrategy } from '@angular/core';
import environment from '@environment/oxygenEnvConfig';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';

@Component({
  selector: 'vs-video-stream',
  templateUrl: 'vs-video-stream.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class VsVideoStreamComponent implements OnChanges {

  @Input() baseStreamURL: string;
  @Input() deviceViewType: string;

  streamURL: SafeResourceUrl;
  private VS_QUOLITY_MAP: {
    desktop: string;
    tablet: string;
    mobile: string;
  };

  // This is a default url which will allow to show error message ("No stream data", etc.) if no virtuals sport stream configuration on cms
  private ERROR_URL: string = 'https://player.igamemedia.com/vplayer?c=83127&s=none&q=moblo';

  constructor(
    private sanitizer: DomSanitizer
  ) {
    this.VS_QUOLITY_MAP = environment.VS_QUOLITY_MAP;
  }

  ngOnChanges(): void {
    this.streamURL = this.getIGMStreamURL();
  }

  /**
   * Get url for vs IGM stream
   * @returns {string} url
   */
  getIGMStreamURL(): SafeResourceUrl {
    const url: string = this.baseStreamURL && this.deviceViewType ?
      `${this.baseStreamURL}&q=${this.VS_QUOLITY_MAP[this.deviceViewType]}` : this.ERROR_URL;
    return this.sanitizer.bypassSecurityTrustResourceUrl(url);
  }
}
