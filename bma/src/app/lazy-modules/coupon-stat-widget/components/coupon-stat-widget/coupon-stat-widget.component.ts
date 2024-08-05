import { Component, Input, AfterViewInit, Output, EventEmitter } from '@angular/core';
import { ISportEvent } from '@core/models/sport-event.model';
import environment from '@environment/oxygenEnvConfig';
import { GtmService } from '@core/services/gtm/gtm.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
@Component({
  selector: 'coupon-stat-widget',
  templateUrl: './coupon-stat-widget.component.html',
  styleUrls: ['./coupon-stat-widget.component.scss']
})
export class CouponStatWidgetComponent implements AfterViewInit {


  @Input() couponIndex?: any;
  @Input() eventIndex?: any;
  @Input() dateIndex?: any;
  @Input() event?: ISportEvent;
  @Output() readonly isLoaded: EventEmitter<boolean> = new EventEmitter();
  private isLoadedValue: boolean;
  isWidgetLoaded: boolean;
  constructor(private gtmService: GtmService, private windowRef: WindowRefService) {
  }
  ngAfterViewInit(): void {
    const sb_data = {
      matchId: "",
      provider: "digital",
      sport: "FOOTBALL",
      type: "MINI_PREMATCH"
    };
    const ctag = this.windowRef.document.getElementById('SB' + (this.couponIndex) + (this.dateIndex) + (this.eventIndex));
    const newdiv = this.windowRef.document.createElement('div');
    sb_data.matchId = (this.event.id).toString();
    newdiv.setAttribute("sb-data", JSON.stringify(sb_data));
    newdiv.setAttribute("id", this.event.couponStatId);
    newdiv.setAttribute("style","width: -webkit-fill-available;z-index:3;position: 'relative';");
    newdiv.addEventListener('googleAnalyticsData', this.gtmHandlerFn, true);

    ctag.appendChild(newdiv);
    const dfScript = this.windowRef.document.getElementById("coupon_script");

    if (dfScript) {
      dfScript.remove();
    }

    this.loadScript(environment.COUPON_STATS_EXTERNAL_URL)
      .then(data => {
        this.isWidgetLoaded = true;
      })
      .catch(err => {
        this.loadScript(environment.COUPON_STATS_EXTERNAL_URL);
      });
  }


  loadScript = (FILE_URL, async = true, id = 'coupon_script', type = "text/javascript") => {
    return new Promise((resolve, reject) => {
      const scriptEle = document.createElement("script");
      scriptEle.type = type;
      scriptEle.async = async;
      scriptEle.src = FILE_URL;
      scriptEle.id = 'coupon_script';
      scriptEle.addEventListener("load", (ev) => {
        resolve({ status: true });
      });
      scriptEle.addEventListener("error", (ev) => {
        reject({
          status: false,
          message: `Failed to load the script ＄{FILE_URL}`
        });
      });
      document.body.appendChild(scriptEle);

    });
  }


  gtmHandlerFn = (customEvent): void => {
    const gtmData = {
      event: customEvent.detail.event,
      eventAction: customEvent.detail.eventAction,
      eventCategory: customEvent.detail.eventCategory,
      eventLabel: customEvent.detail.eventLabel,
      categoryID: this.event.categoryId,
      typeID: this.event.typeId,
      eventID: this.event.id
    };
    this.gtmService.push('trackEvent', gtmData);
    if (!this.isLoadedValue) {
      this.isLoadedValue = true;
      this.isLoaded.emit(true);
    }
  }
} 
