export enum EventMethods {
  today = 'today',
  tomorrow = 'tomorrow',
  future = 'future',
  upcoming = 'upcoming',
  coupons = 'coupons',
  outrights = 'outrights',
  antepost = 'antepost',
  live = 'live',
  results = 'results',
  matches = 'matches',
  competitions = 'competitions',
  jackpot = 'jackpot',
  specials = 'specials',
}

export interface ISportConfigEventMethods {
  today: string;
  tomorrow: string;
  future: string;
  upcoming: string;
  coupons: string;
  outrights: string;
  antepost: string;
  live: string;
  results: string;
  matches?: string;
  competitions?: string;
  jackpot?: string;
  specials?: string;
  allEvents?:string;
  matchesTab? :string;
}
