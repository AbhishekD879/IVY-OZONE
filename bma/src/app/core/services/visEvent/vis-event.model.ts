export interface IVisEventAvailability {
  id: string;
  providerName: string | null;
  sportName: string | null;
}

export interface IPreMatchAvailability {
  id: string;
  stats: boolean;
  error?: string;
}

export interface IEventVisParams {
  id: string;
  sportName: string | null;
  canDisplayCastro: boolean;
}
