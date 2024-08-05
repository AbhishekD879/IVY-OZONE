export interface IPlayer {
    index: number;
    player: string;
    statId: number;
    line: number;
    count: number;
}

export interface IPitchDetails {
    formation: string;
    players: IPlayer[];
}
