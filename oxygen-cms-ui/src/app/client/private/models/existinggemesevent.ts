import { Team } from './baseteam.model';

export interface GamesEvent {
    brand: string;
    gameId: string;
    tvIcon: string;
    eventId: string;
    startTime: string;
    home: Team;
    away: Team;
    sortOrder: number;
}
