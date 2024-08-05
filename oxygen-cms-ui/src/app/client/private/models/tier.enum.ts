export enum Tier {
  TIER_1 = 'TIER_1',
  TIER_2 = 'TIER_2',
  UNTIED = 'UNTIED'
}

enum TierTitle {
  TIER_1 = 'Tier 1',
  TIER_2 = 'Tier 2',
  UNTIED = ''
}

export namespace Tier {
  export function title(tierName: string): string {
    return TierTitle[tierName];
  }
}

