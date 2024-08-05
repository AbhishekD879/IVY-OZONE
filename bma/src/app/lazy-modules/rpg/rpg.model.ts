export interface IRpgGameModel {
    gamevariant: string,
    displayname: string,
    lobbytype?: string,
    isgameavailable?: string,
    imageUrl: string,
    game?: string,
    name?: string,
    ownerId?: number,
    provider?: string,
    sid?: string
}

export interface IRpgPayload {
    accountName: string,
    brandId: string,
    channelId: string,
    feId: string,
    lang: string,
    lobbyType: string,
    noofgames: number,
    productId: string,
    reqSource: string,
}

export interface IRpgResponse {
    statusCode: number,
    status: string,
    errorMessage: string,
    games: IRpgGameModel[]
}

export interface IDisabledGamesResponse {
    games: string[]
}

export interface IGymlPayload {
    brandId: string,
    invokerProduct: string,
    channelId: string,
    lang: string,
    lobbyType: string,
}

export interface IGymlResponse {
    statusCode: number,
    status: string,
    errorMessage: string,
    categoryid: string,
    subcategoryid: string,
    gamelist: IRpgGameModel[],
    gamevariant?: string,
    displayname?: string,
    imageUrl?: string,
}

export interface IRpgConfig {
    gamesAmount?: number;
    seeMoreLink?: string;
    title?: string;
    categoryId?: string;
    bundleUrl?: string;
    loaderUrl?: string;
    segmentOrder?: number;
  }