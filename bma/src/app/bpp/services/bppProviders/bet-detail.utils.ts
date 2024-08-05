import { IBetDetail } from '@app/bpp/services/bppProviders/bpp-providers.model';

export class BetDetailUtils {
  /**
   * Check status of given stake.
   *
   * Bet <status> is one of:
   *  A - active (accepted)
   *  S - suspended
   *  X - cancelled
   *  Expired - expired
   *  P - pending, but canceled on other grounds (trader timer expired, accepted but topup)
   *
   * Bet <asyncAcceptStatus> is one of:
   * O - Offer still open (default)
   * T - Offer accepted by trader but user requires topup.
   * A - Offer accepted and bet placed
   * D - Offer declined and bet cancelled
   * C - Offer and bet cancelled, probably because offer timed out
   *
   * @param stake
   */
  static isCanceled(stake: IBetDetail): boolean {
    return stake.status === 'X' || stake.status === 'P' || stake.asyncAcceptStatus === 'T';
  }
}
