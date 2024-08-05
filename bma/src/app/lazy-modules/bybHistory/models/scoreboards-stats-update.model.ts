export interface IScoreboardStatsUpdate {
  ballPossession: string;
  clockRunning: boolean;
  eventId: string;
  obEventId: string;
  period: string;
  provider: string;
  sequenceId: number;
  startTime: string;
  time: string;
  away: IHomeAwayInfo;
  home: IHomeAwayInfo;
  cards: ICards;
  goals: IGoals;
  players: IPlayers;
  score: IScore;
  substitutions: ISubstitutions;
  teams: ITeams;
}

interface IHomeAwayInfo {
  id: string;
  name?: string;
  providerId: string;
}

interface ICards {
  away: ICard[];
  home: ICard[];
}

interface ICard {
  player: string;
  time: string;
  type: string;
  timestamp: string;
}

export interface IGoals {
  away: IGoalInfo[];
  home: IGoalInfo[];
}

export interface IGoalInfo {
  assistingPlayer: string;
  ownGoal: boolean;
  scorer: string;
  time: string;
  timestamp: string;

  // custom properties
  team?: string;
  period?: string;
  player?: IPlayer;
}

export interface ICardsInfo extends ICard {
  team?: string; // custom properties
}

export interface IPlayers {
  away: { [key: string]: IPlayer };
  home: { [key: string]: IPlayer };
}

export interface IPlayersSimple {
  away: IPlayer[];
  home: IPlayer[];
}

export interface IPlayer {
  assists: number;
  cards: IPlayerCards;
  chancesCreated: number;
  fouls: number;
  goals: number;
  id: string;
  name: IPlayerName;
  passes: number;
  providerId: string;
  tackles: number;
  shots: IShots;
  goalConceded: number;
  crosses: number;
  offsides: number;
  goalsInsideBox: number;
  goalsOutsideBox: number;
  shotsOutsideBox: number;
  shotsWoodwork: number;
  secondYellow: number;
  homeAwaySide?: string;
  team?: string; // home|away
}

export interface IPlayerCards {
  yellow: number;
  red: number;
}

interface IPlayerName {
  firstName: string;
  lastName: string;
  matchName: string;
}

interface IShots {
  blockedShot: number;
  offTarget: number;
  onTarget: number;
  total: number;
}

export interface IScore {
  '1h': IScoreByTime;
  '2h'?: IScoreByTime;
  total: IScoreByTime;
}

export interface IScoreByTime {
  home: number;
  away: number;
}

interface ISubstitutions {
  away: ISubstitution[];
  home: ISubstitution[];
}

interface ISubstitution {
  time: string;
  playerOn: string;
  playerOff: string;
}

export interface ITeams {
  home: ITeam;
  away: ITeam;
}

export interface ITeam {
  '1h': ITeamStats;
  '2h'?: ITeamStats;
  pre: ITeamStats;
  total: ITeamStats;
  ht?: ITeamStats;
  ert?: ITeamStats;
}

interface ITeamStats {
  attacks: number;
  cards: IPlayerCards;
  corners: number;
  dangerousAttacks: number;
  fouls: number;
  possession: string;
  shots: IShots;
  substitutions: number;
  throwIns: number;
  id?: string;
  providerId?: string;
}

export interface IScoreByPlayer {
  away: IGoalAndPlayerInfo[];
  home: IGoalAndPlayerInfo[];
}

export interface IScoreByTeams {
  score: IScore;
  away: IHomeAwayInfo;
  home: IHomeAwayInfo;
}

export interface ICardsByPlayer {
  cards: ICards;
  away: IHomeAwayInfo;
  home: IHomeAwayInfo;
}

interface IGoalAndPlayerInfo extends IGoalInfo {
  player: IPlayer;
}

export interface ITeamCards {
  id: string;
  providerId: string;
  periods: ITeam;
}

export interface IRedCardsByTeams {
  away: ITeamCards;
  home: ITeamCards;
}

export interface IMatchCommentaryStatsUpdate {
  incident: IIncident;
 }
interface IIncident{
  eventId?: string;
  correlationId?: string;
  seqId?:null;
  type?:IVartype;
  score?:null;
  periodScore?:null;
  clock?:string;
  participant?:string;
  period?: string;
  timeStamp?: string;
  receiveTimestamp?: string;
  context?:IContext;
  feed?: string;
}
interface IVartype
{
  code?: number,
  description?: string
}
interface IContext{
  teamName?: string,
  playerName?: string,
  playerOnName?: string,
  playerOffName?: string,
  minutes ?: string
  reasonId?: number,
  x?:string,
  y?:string
}