import { HttpClient } from '@angular/common/http';
import { Component, ViewChild, AfterViewInit } from '@angular/core';
import { DeviceService } from '@core/services/device/device.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { UserService } from '@core/services/user/user.service';
import { AbstractDialogComponent } from '@shared/components/oxygenDialogs/abstract-dialog';
import { LUCKY_DIP_CONSTANTS } from '@lazy-modules/luckyDip/constants/lucky-dip-constants';
import { AnimationDataConfig } from '@lazy-modules/luckyDip/models/luckyDip';

@Component({
  selector: 'animation-modal',
  templateUrl: './animation-modal.component.html',
  styleUrls: ['./animation-modal.component.scss']
})
export class AnimationModalComponent extends AbstractDialogComponent implements AfterViewInit {

  @ViewChild('dialog', { static: true }) dialog: any;
  animationData: AnimationDataConfig;
  svg: any;
  svgPath = ['Symbol-1', 'Symbol-2', 'Symbol-3', 'Symbol-4', 'Symbol-5'];

  constructor(
    device: DeviceService,
    windowRef: WindowRefService,
    protected http: HttpClient,
    private user: UserService
  ) {
    super(device, windowRef);
  }

  ngAfterViewInit(): void {
    setTimeout(() => this.updateAnimationContent(), 200);
  }

  /**
   * to open animation popup after place bet call
   * @returns {void}
   */
  open(): void {
    this.windowRef.document.body.classList.add(LUCKY_DIP_CONSTANTS.ANIMATION_MODAL_OPEN);
    super.open();
    this.animationData = this.params.data.value;
    this.svg = this.animationData.svg;
  }

  /**
   * to close animation popup
   * @returns {void}
   */
  public closeAnimationDialog(): void {
    this.params.data.openBetReceipt();
  }

  /**
   * to update animation with dynamic content
   * @returns {void}
   */
  updateAnimationContent(): void {
    const paths = [];
    this.svgPath.forEach((path) => {
      paths.push(this.windowRef.document.getElementById(path));
    });
    const pathDetails = [
      {
        path: paths[0],
        className: LUCKY_DIP_CONSTANTS.PLAYER_CARD_DESCRIPTION_POTENTIAL,
        value: this.animationData.cmsConfig.playerCardDesc
      },
      {
        path: paths[1],
        className: LUCKY_DIP_CONSTANTS.PLAYER_NAME,
        value: this.animationData.playerData.playerName
      },
      {
        path: paths[2],
        className: LUCKY_DIP_CONSTANTS.OUTCOME_VALUE,
        value: this.animationData.playerData.odds
      },
      {
        path: paths[3],
        className: LUCKY_DIP_CONSTANTS.RETURN_DESCRIPTION,
        value: this.animationData.cmsConfig.potentialReturnsDesc
      },
      {
        path: paths[4],
        className: LUCKY_DIP_CONSTANTS.AMOUNT,
        value: this.user.currencySymbol + this.animationData.playerData.amount
      }
    ];
    pathDetails.forEach((path) => {
      const symbolPath = path.path.querySelector('path');
      this.addLabelText(symbolPath, path.className, path.value);
      symbolPath.removeAttribute('d');
    });
  }

  /**
   * to replace content on animation card
   * @params {bgPath} any
   * @params {className} string
   * @params {value}  string
   * @returns {void}
   */
  addLabelText(bgPath: SVGGraphicsElement, className: string, value: string) {
    const bbox = bgPath.getBBox();
    const width = bbox.x + bbox.width / 2;
    const height = bbox.y + bbox.height;
    const textElem = document.createElementNS(bgPath.namespaceURI, "text");
    textElem.setAttribute("x", width.toString());
    textElem.setAttribute("y", height.toString());
    textElem.setAttribute("text-anchor", "middle");
    textElem.classList.add(className);
    textElem.textContent = value;
    bgPath.after(textElem);
  }

  /**
   * to check if it is ios
   * @returns {void}
   */
  isIOSsafari() {
    return this.device.isIos && !this.device.isWrapper && this.device.isSafari;
  }
}
