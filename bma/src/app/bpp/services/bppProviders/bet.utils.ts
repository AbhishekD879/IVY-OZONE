import { IBet } from '@app/bpp/services/bppProviders/bpp-providers.model';

export class BetUtils {
  static isOffer(bet: IBet): boolean {
    return bet.isOffer === 'Y';
  }
}
