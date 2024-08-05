import { ClientConfig, ClientConfigProductName  } from '@frontend/vanilla/core';
import { IRpgPayload } from '@app/lazy-modules/rpg/rpg.model';
@ClientConfig({
  key: 'bmaCasinoGamesConfig',
  product: ClientConfigProductName.SPORTS,
  reload: false
} as any)
export class CasinoGamesClientConfig {
  miniGamesEnabled: boolean;
  miniGamesHost: string;
  miniGamesTemplate: string;
  recentlyPlayedGamesEnabled: boolean;
  recentlyPlayedGamesUrl: string;
  userHostAddress: string;
  seeAllEnabled: boolean;
  seeAllUrl: string;
  gameImageUrl: string;
  gameLaunchUrl: string;
  gymlUrl: string;
  rpgCacheExpiry: number;
  rpgUrl: string;
  rpgPayload: IRpgPayload;
  fzGmImgDsUrl: string;
  fzGmImgMbUrl: string;
  fzGmLaDsUrl: string;
  fzGmLaMbUrl: string;
}
