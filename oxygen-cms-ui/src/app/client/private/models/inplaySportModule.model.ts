import { Base } from "./base.model";

export interface InplaySportModule {
  enabled: boolean;
  inplayCount: number;
}

export interface InplaySports {
  categoryId: number;
  sportName: string;
  sportTier: string;
}

export interface HomeInplayModule extends Base {
  id: string;
  eventCount: number,
  categoryId: string,
  tier: string,
  sportName: string,
  brand: string,
  message?: string
}
