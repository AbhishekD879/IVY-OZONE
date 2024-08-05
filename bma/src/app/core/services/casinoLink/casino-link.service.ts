import { Injectable } from '@angular/core';
import * as _ from 'underscore';
import { ICasinoDecoratedLink } from './casino-link.model';
import { IFooterMenu, ISportCategory, IVerticalMenu } from '../cms/models';
import { DeviceService } from '@core/services/device/device.service';
import environment from '@environment/oxygenEnvConfig';

@Injectable()
export class CasinoLinkService {
  private readonly env = environment;
  constructor(
    private device: DeviceService
  ) {
    this.uriDecoration = this.uriDecoration.bind(this);
  }

  filterGamingLinkForIOSWrapper(links: Partial<IFooterMenu | ISportCategory | IVerticalMenu>[]): void {
    if (this.device.isWrapper && this.device.isIos) {
      links.forEach((link, index: number) => {
        if (new RegExp(this.env.GAMING_URL[0]).test(link.targetUri)) {
          links.splice(index, 1);
        }
      });
    }
  }

  /**
   * Find mcasino link in menu items array and decorate it
   * @param {Array<Object>} array of menuElements or banners
   */
  decorateCasinoLink<T extends ICasinoDecoratedLink>(array: T[]): T[] {
    return _.map(array, arrayItem => {
      arrayItem.targetUri = this.uriDecoration(arrayItem.targetUri);
      return arrayItem;
    });
  }

  /**
   * Find mcasino link in HTML source and decorate it
   * @param {string} htmlSource of menuElements or banners
   */
  decorateCasinoLinkInHtml(htmlSource: string): string {
    // eslint-disable-next-line max-len
    const mcasinoUriPattern = /\b((?:[a-z][\w-]+:(?:\/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.-]+[.][a-z]{2,4}\/).*mcasino*(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()[\]{};:'".,<>?«»“”‘’]))/g;
    return htmlSource.replace(mcasinoUriPattern, this.uriDecoration);
  }


  /**
   * Decoration rule for mcasino links
   * @param {string} uri
   */
  uriDecoration(uri: string): string {
    if (uri && uri.indexOf('mcasino') !== -1 && uri.indexOf('deliveryPlatform') === -1) {
      const deliveryPlatform = this.device.isWrapper ? 'Wrapper' : 'HTML5';
      const paramDelimiter = uri.match(/[?]/g) ? '&' : '?';
      return `${uri}${paramDelimiter}deliveryPlatform=${deliveryPlatform}`;
    }
    return uri;
  }
}
