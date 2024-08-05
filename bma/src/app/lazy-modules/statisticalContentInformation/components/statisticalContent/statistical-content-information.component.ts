import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { CmsService } from '@coreModule/services/cms/cms.service';
import * as _ from 'underscore';
import { IStatisticalContent, EnumStatisticalFlags } from '@app/core/services/cms/models/statistical-content-info.model';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
@Component({
  selector: 'statistical-content-information',
  templateUrl: './statistical-content-information.component.html',
  styleUrls: ['./statistical-content-information.component.scss']
})
export class StatisticalContentInformationComponent implements OnInit {
  @Input() eventEntity;
  @Input() market;
  @Input() twoUpMarketName;
  @Input() brand;
  @Input() display: string;
  @Output() marketStatistical: EventEmitter<any> = new EventEmitter();
  flagType: string;
  statisticalContentInformation: SafeHtml;
  constructor(protected cmsService: CmsService,private domSanitizer: DomSanitizer) { }
  ngOnInit() {
    this.processFlags()
  }
  /**
   * Find Flags Type
   */
  private processFlags(): void {
    const flags = this.parseFlags(this.display);
    _.each(flags, (flagName: string) => {
      if ((flagName.indexOf('_PB') > 0 || flagName.indexOf('_PR1') > 0)) {
        Object.entries(EnumStatisticalFlags).forEach(([key, value]) => {
          if (key == (this.brand + '_' + flagName)) {
            this.flagType = value;
          }
        });
      }
    });
    if (this.flagType) {
      this.getStatisticalContent(this.flagType);
    }
  }
  /**
 * Parsing drilldownTagNames
 * @param {string} drilldownTagNames
 * @returns {Array} array with available flags
 */
  public parseFlags(drilldownTagNames: string): string[] {
    return drilldownTagNames ? _.without(drilldownTagNames.split(','), '') : [];
  }

  getStatisticalContent(flagType) {
    this.cmsService.getStatisticalContent(this.market.eventId).subscribe((res : IStatisticalContent[]) => {
        if (res && res.length) {
            res.forEach((statisticalContent) => {
              if (this.market.eventId == statisticalContent.eventId && (this.market.id == statisticalContent.marketId || this.market?.marketIds[0] == statisticalContent.marketId) && flagType == statisticalContent.marketType && statisticalContent.enabled) {
                this.statisticalContentInformation = this.domSanitizer.bypassSecurityTrustHtml(statisticalContent.content);
                this.market.isSCAvailable = true;
                this.marketStatistical.emit(this.market);
              }
            })
          }
        })
  }
}