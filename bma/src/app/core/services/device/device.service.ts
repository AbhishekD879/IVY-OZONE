import { DOCUMENT } from '@angular/common';
import { Inject, Injectable } from '@angular/core';
import * as UAParser from 'ua-parser-js/src/ua-parser.js';
import * as _ from 'underscore';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { StorageService } from '../storage/storage.service';
import { WindowRefService } from '../windowRef/window-ref.service';
import { samsungPrefixesRegexp, sumsungVersion, uaRegexp, uaSamsungRegexp } from './device.constant';
import environment from '@environment/oxygenEnvConfig';
@Injectable()
export class DeviceService {

  mobileWidth = 767;
  landTabletWidth = 1024;
  desktopWidth = 1025;
  parsedUA: any;

  channel: { channelRef: { id: string } };
  viewType: string;
  strictViewType: string;
  browserName: string;
  deviceType: string;
  osVersion: string;
  osName: string;
  deviceId: string;
  gameType: string;
  deliveryPlatform: string;
  uuid: string;
  softSerial: string;
  requestPlatform: string;
  isAndroid: boolean;
  isIos: boolean;
  isWindows: boolean;
  isMobile: boolean;
  isTablet: boolean;
  isTabletOrigin: boolean;
  isTabletLandscape: boolean;
  isDesktop: boolean;
  isWrapper: boolean;
  isPortraitOrientation: boolean;
  isMobileOrigin: boolean;
  isNativeAndroid: boolean;
  isDesktopWindows: boolean;
  isSafari: boolean;
  brand = environment.brand;

  private isDeviceOnline: boolean;
  private navigator: any;
  private device: any;
  private samsungVersionMap: any;
  private readonly IPAD_DEVICE: string = 'ipad';
  private readonly MACBOOK_DEVICE: string = 'macintosh';
  private readonly GOOGLE_BOT: string = 'googlebot';

  constructor(private windowRef: WindowRefService, private storage: StorageService,
              private pubSubService: PubSubService, @Inject(DOCUMENT) private document) {

    this.navigator = this.windowRef.nativeWindow.navigator;
    this.device = new UAParser().getResult();
    this.isMobile = this.performProviderIsMobile(true) || this.windowRef.nativeWindow.innerWidth < this.mobileWidth;

    this.init();
  }

  isTouch(): boolean {
    return !!('ontouchstart' in document);
  }

  /**
   * Returns online indicator.
   * @return {boolean}
   */
  isOnline(): boolean {
      return _.isUndefined(this.isDeviceOnline) ? this.navigator.onLine : this.isDeviceOnline;
  }

  /**
   * Sets online indicator.
   * @param {boolean} value
   */
  setOnline(value: boolean) {
    this.isDeviceOnline = value;
  }

  /**
   * Checks is the device mobile phone
   * DON'T DELETE THIS!!! DISCUSS WITH VOLTRON TEAM BEFORE
   * @returns {boolean}
   */
  get isMobileOnly(): boolean {
    const IS_TOUCH_DEVICE = 'ontouchstart' in this.document, VIEWPORT = this.windowRef.nativeWindow.innerWidth;
    return IS_TOUCH_DEVICE && VIEWPORT < this.mobileWidth;
  }
  set isMobileOnly(value:boolean){}
  get isDesktopSafari() {
    return this.isDesktop && this.browserName.toLowerCase() === 'safari';
  }
  set isDesktopSafari(value:any){}

  /**
   * Test use agent if it is mobile or desktop and use proper rendering
   *
   * @param mobileOnly - boolean with mobile Only
   * @param userAgentName - string with user agent
   * if param mobileOnly equal False will return true if mobile and tablet, false if desktop
   * if param mobileOnly equal True will return true if mobile, false if desktop and tablet
   */
  performProviderIsMobile(mobileOnly?: boolean, userAgentName?: string): boolean {
    const agent = userAgentName || this.navigator.userAgent || this.navigator.vendor || this.windowRef.nativeWindow.opera;
    let check = false;

    /* eslint-disable max-len */
    const regExp: RegExp = new RegExp(`(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino${!mobileOnly ? '|android|ipad|playbook|silk' : ''}`, 'i');
    const regExp2: RegExp = new RegExp('1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-', 'i');
    /* eslint-enable max-len */
    const navigatorAgent: string = this.navigator.userAgent?.toLowerCase();
    const iPadVersionCheck: boolean = navigatorAgent && (navigatorAgent.indexOf(this.IPAD_DEVICE) > -1
      || navigatorAgent.indexOf(this.MACBOOK_DEVICE) > -1);

    if (regExp.test(agent) || regExp2.test(agent.substr(0, 4)) || iPadVersionCheck) {
      check = true;
    }

    return check;
  }

  /**
  * Returns true/false based on device type
  * Adding this method since we are receiving {isMobile: true} from the method {performProviderIsMobile} in case of tablet/ipad/macbook devices
  * @returns {IDeviceViewType}
  */
  getDeviceViewType(): IDeviceViewType {
    return {
      mobile: this.windowRef.nativeWindow.innerWidth < this.mobileWidth,
      tablet: (this.windowRef.nativeWindow.innerWidth >= this.mobileWidth && this.windowRef.nativeWindow.innerWidth < this.landTabletWidth) ||
        (this.windowRef.nativeWindow.innerWidth >= this.landTabletWidth && this.windowRef.nativeWindow.innerWidth < this.desktopWidth),
      desktop: this.windowRef.nativeWindow.innerWidth >= this.desktopWidth
    };
  }

  get freeBetChannel(): string {
    const androidFreeBetChannel = 'Mz';
    const iOsFreeBetChannel = 'My';
    const mobileFreeBetChannel = 'M';
    const desktopFreeBetChannel = 'MI';
    const isWrapper = this.detectWrapper();

    if (isWrapper && this.device.os.name === 'Android') {
      return androidFreeBetChannel;
    }
    if (isWrapper && this.device.os.name === 'iOS') {
      return iOsFreeBetChannel;
    }

    return this.device.device.type ? mobileFreeBetChannel : desktopFreeBetChannel;
  }
  set freeBetChannel(value:string){}
  private init(): void {
    this.samsungUAFix(this.device);

    // make value signUpDeliveryPlatform as global,
    // to add this value to dataLayer for event tracking in GTM, see BMA-8464
    this.windowRef.nativeWindow.signUpDeliveryPlatform = this.getPlatform();
    this.calculateServiceProps();
    this.windowRef.nativeWindow.addEventListener('resize', () => this.onResizeOrOrientationChange());
    this.windowRef.nativeWindow.addEventListener('orientationchange', () => this.onResizeOrOrientationChange());
  }

  private calculateServiceProps(): void {
    this.viewType = this.getViewType();
    this.strictViewType = this.getStrictViewType();
    this.requestPlatform = this.getRequestPlatform(this.strictViewType);

    this.parsedUA = this.device;
    this.browserName = this.getDeviceBrowserName();
    this.deviceType = this.getDeviceData();
    this.osVersion = this.device.os.version;
    this.osName = this.device.os.name;
    this.channel = this.getChannel();
    this.gameType = 'Sportsbook';
    this.deviceId = 'xxPxxx';
    this.deliveryPlatform = this.getPlatform(); // 'HTML5
    this.isAndroid = this.device.os.name === 'Android';
    this.isIos = this.device.os.name === 'iOS';
    this.isWindows = this.device.os.name === 'Windows Phone';
    this.isSafari = this.browserName && this.browserName.toLowerCase().indexOf('safari') > -1;
    this.isTablet = this.strictViewType === 'tablet';    
    this.isTabletLandscape = this.viewType === 'landscapeTablet';
    this.isTabletOrigin = this.isTablet || this.isTabletLandscape || this.device.device.type === 'tablet';
    this.isDesktop = environment.CURRENT_PLATFORM === 'desktop';
    this.isWrapper = this.detectWrapper();
    this.isPortraitOrientation = this.checkPortraitOrientation();
    this.uuid = this.getUuid();
    this.softSerial = this.getSoftSerial();
    this.isMobileOrigin = this.isMobileUA();
    this.isNativeAndroid = this.isAndroid && this.browserName === 'Android Browser';
    this.isDesktopWindows = this.isDesktop && this.osName === 'Windows';
  }

  private samsungUAFix({ device, ua, os }): void {
    if (!device.model && device.type === 'mobile' && os.name === 'Android') {
      const modelPartResult = uaRegexp.exec(ua);

      if (modelPartResult !== null) {
        const modelAndBuild = _.last(_.last(modelPartResult).split(';'));
        const model = modelAndBuild.replace(uaSamsungRegexp, '');

        if (samsungPrefixesRegexp.test(model)) {
          device.vendor = 'Samsung';
          device.model = model;
        }
      }
    }
  }

  private isMobileUA(): boolean {
    return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(this.navigator.userAgent);
  }

  private checkPortraitOrientation(): boolean {
    return this.windowRef.nativeWindow.innerHeight > this.windowRef.nativeWindow.innerWidth;
  }

  private onResizeOrOrientationChange(): void {
    const lastViewType = this.viewType;
    this.calculateServiceProps();

    if (lastViewType !== this.viewType) {
      // will be renamed after removing same logic from controller
      this.pubSubService.publish(this.pubSubService.API.DEVICE_VIEW_TYPE_CHANGED_NEW, this.viewType);
    }
  }

  private getRequestPlatform(strictViewType) {
    return environment.CURRENT_PLATFORM === 'desktop' ? environment.CURRENT_PLATFORM : strictViewType;
  }

  // e.g. HTC One
  private getDeviceData(): string {
    let model = this.device.device.model; // Lumia 520
    const vendor = this.device.device.vendor; // Microsoft

    // In case of unknown mobile devices
    if (!model && this.device.device.type === 'mobile') {
      return 'Mobile Unknown';
    }

    // In case of laptop and desktop devices
    if (!model && !this.device.device.type) {
      return 'Unknown Device';
    }

    // return e.g iPhone 6 Plus
    if (model === 'iPhone') {
      model = this.getiPhoneDevice();
    }

    // return e.g Samsung Galaxy Tab 10.1
    if (vendor === 'Samsung') {
      model = `${this.getSamsungDevice(model)} ${model}`;
    }

    // If parser found vendor name we add it to model e.g. Apple iPhone 4
    if (vendor) {
      return this.getFullDeviceName(vendor, model);
    }

    return model;
  }

  private getDeviceBrowserName(): string {
    return this.device.browser?.name;
  }

  // M - mobile, I - desktop.
  private getChannel(): { channelRef: { id: string } } {
    const channel = (this.device.device.type) ? { id: 'M' } : { id: 'I' };
    return { channelRef: channel };
  }

  private getPlatform(): string {
    return this.detectWrapper() ? 'Wrapper' : 'HTML5';
  }

  /**
   * Detects platform, is wrapper or default(bma).
   * @returns {boolean}
   */
  private detectWrapper(): boolean {
    const isNative = !!this.windowRef.nativeWindow.NativeBridge || // Android and iOS wrapper check
      (this.windowRef.nativeWindow.external && this.windowRef.nativeWindow.external.notify); // windows phone wrapper check
    return !!isNative;
  }

  private buildSamsungVersionMap(): void {
    if (this.samsungVersionMap) {
      return;
    }

    this.samsungVersionMap = {};
    _.each(sumsungVersion, (models, name) => {
      this.samsungVersionMap[name] = new RegExp(models.join('|'), 'i');
    });
  }

  // Parser for Sa,sung devices.
  private getSamsungDevice(model): string {
    const models = model.replace(uaSamsungRegexp, '');
    this.buildSamsungVersionMap();

    const names = Object.keys(this.samsungVersionMap).reverse();
    let len = names.length;

    while (len--) {
      const name = names[len];

      if (this.samsungVersionMap[name].test(models)) {
        return `Samsung Galaxy ${name}`;
      }
    }

    return 'Samsung';
  }

  // Parser for iPhone Devices.
  private getiPhoneDevice(): string {
    const ratio = this.windowRef.nativeWindow.devicePixelRatio || 1,
      w = this.windowRef.nativeWindow.screen.width * ratio,
      h = this.windowRef.nativeWindow.screen.height * ratio,
      res = `${w}x${h}`;
    if (res === '480x320' || res === '320x480') {
      return 'iPhone 2g/3g/3gs';
    } else if (res === '960x640' || res === '640x960') {
      return 'iPhone 4';
    } else if (res === '640x1136' || res === '1136x640') {
      return 'iPhone 5';
    } else if (res === '750x1334' || res === '1334x750') {
      return 'iPhone 6';
    } else if (res === '1242x2208' || res === '2208x1242') {
      return 'iPhone 6 Plus';
    }
    return 'iPhone';
  }

  // Add vendor name to model e.g. LG Nexus.
  private getFullDeviceName(vendor: string, model: string): string {
    return (model.toLowerCase().indexOf(vendor.toLowerCase()) > -1) ? model : `${vendor} ${model}`;
  }

  // View Type start
  /**
   * Returns device view type from ['mobile', 'tablet', 'landscapeTablet', 'desktop'] list.
   * @returns {string}
   */
  private getViewType(): string {
    if (this.isMobile) {
      return 'mobile';
    } else if (this.windowRef.nativeWindow.innerWidth < this.landTabletWidth) {
      return 'tablet';
    } else if (this.windowRef.nativeWindow.innerWidth < this.desktopWidth) {
      return 'landscapeTablet';
    }
    return 'desktop';
  }

  private getNewUuid(): string {
    /* eslint-disable */
    let d = new Date().getTime();
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, c => {
      const r = (d + (Math.random() * 16)) % 16 | 0;
      d = Math.floor(d / 16);
      return (c === 'x' ? r : ((r & 0x3) | 0x8)).toString(16);
    });
    /* eslint-enable */
  }

  /**
   * Generates sets in storage and returns uuid - unique identifier
   * @returns {string}
   */
  private getUuid(): any {
    let uuid = this.storage.get('uuid');
    if (!uuid) {
      uuid = this.getNewUuid();
      this.storage.set('uuid', uuid);
    }

    return uuid;
  }

  /**
   * Generates sets in storage and returns soft serial - 6 digit random number
   * @returns {string}
   */
  private getSoftSerial(): any {
    let softSerial = this.storage.get('softSerial');
    if (!softSerial) {
      softSerial = String(_.random(100000, 999999));
      this.storage.set('softSerial', softSerial);
    }
    return softSerial;
  }

  /**
   * Return view type from ['mobile', 'tablet', 'desktop'] list.
   * Can be used for CMS requests, since CMS API doesn't know about landscapeTablet.
   * @returns {string}
   */
  private getStrictViewType(): string {
    const type = this.getViewType();
    return type === 'landscapeTablet' ? 'tablet' : type;
  }
  /**
   * return boolean if the userAgent is googleBot or not
   * @returns boolean
   */
  isRobot(): boolean {
    const userAgent: string = this.navigator?.userAgent?.toLowerCase();
    return userAgent?.indexOf(this.GOOGLE_BOT) > -1;
  }
}

export interface IDeviceViewType {
  mobile: boolean;
  tablet: boolean;
  desktop: boolean;
}