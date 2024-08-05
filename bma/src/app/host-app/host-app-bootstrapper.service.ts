import { Injectable } from '@angular/core';
import { OnAppInit } from '@frontend/vanilla/core';
import { ProductActivatorService } from '@frontend/vanilla/shared/product-activation';

/**
 * NOTE: Dynacon HostApp.Products might look similar to this
 *
 * ```
 * {
 *       "portal": {
 *          "enabled": true,
 *           "apiBaseUrl": "http://${dynacon:environment}.portal.${dynacon:label}"
 *      },
 *       "host": {
 *           "enabled": true,
 *           "apiBaseUrl": ""
 *       }
 *   }
 * ```
 */
@Injectable()
export class HostAppBootstrapper implements OnAppInit {
  constructor(private productActivatorService: ProductActivatorService) {
  }

  async onAppInit(): Promise<void> {
    await this.productActivatorService.activate('host');
  }
}
