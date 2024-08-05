import { Injectable } from '@angular/core';
import { LiveServConnectionService } from '@core/services/liveServ/live-serv-connection.service';
import { ISocketIO } from '@core/services/liveServ/live-serv-connection.model';
import { IMatchCommentaryStatsUpdate } from '@lazy-modules/bybHistory/models/scoreboards-stats-update.model';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { ALTERD_MATCHFACTS, betLegConstants, MATCH_TIME_CONFIG, UNIQUE_TEMPLATE, varReasonId_config } from '@app/betHistory/constants/bet-leg-item.constant';
import { IVarIconData, IMatchCmtryData } from '@app/betHistory/models/bet-history.model';
import { BetHistoryApiModule } from '@app/betHistory/bet-history-api.module';
import { cashoutConstants } from '@app/betHistory/constants/cashout.constant';
import { EVENTS } from '@app/core/constants/websocket-events.constant';

@Injectable({ providedIn: BetHistoryApiModule })
export class HandleVarReasoningUpdatesService {
  private callbacks: { handler: Function };
  private lastCodeCallBacks: { handler: Function };
  private channels: string[] = [];
  private connection: ISocketIO;
  private varIconData: IVarIconData;
  private matchCmtryDataUpdate: IMatchCmtryData= {};
  constructor(
    private liveServConnectionService: LiveServConnectionService,
    private pubSubService: PubSubService
  ) {
    this.disconnectHandler = this.disconnectHandler.bind(this);
  }
  /**
   * Subscribe for match-commentary updates for live-serv-connection.service
   * @param channel - eventId
   */
  subscribeForMatchCmtryUpdates(channel: string): void {
    const updatesMatchCmtryHandler = (cmtryUpdate: IMatchCommentaryStatsUpdate) => {
    this.matchCommentryUpdateHandler(cmtryUpdate);
    }
    this.channels.push(channel);
    this.callbacks = { handler: updatesMatchCmtryHandler };
    this.liveServConnectionService.connect().subscribe((connection: ISocketIO) => {
      this.liveServConnectionService.subscribeToMatchCommentary(cashoutConstants.channelName.facts + channel, this.callbacks.handler);
      this.updateConnection(connection);
    });
  }
  /**
   * request the last match facts
   * @param channels 
   */
  sendRequestForLastMatchFact(channels: string[]) {
    const updatesLastMatchFactHandler: Function = (cmtryUpdate: IMatchCommentaryStatsUpdate) => {
      this.matchCommentryUpdateHandler(cmtryUpdate);
    }
    this.lastCodeCallBacks = { handler: updatesLastMatchFactHandler };
    this.pubSubService.subscribe(
      betLegConstants.handleVarReasoningUpdates,
      `liveServe.${EVENTS.SOCKET_CONNECT_SUCCESS}`,
      (connection: ISocketIO) => connection && this.liveServConnectionService.sendRequestForLastMatchFact(channels, this.lastCodeCallBacks.handler));

    this.liveServConnectionService.sendRequestForLastMatchFact(channels, this.lastCodeCallBacks.handler);
  }
  /**
   * Assigns data to matchCmtryDataUpdate
   * @param cmtryUpdate 
   * @returns object of matchCmtryDataUpdate
   */
  private getMatchFactData(cmtryUpdate:IMatchCommentaryStatsUpdate): IMatchCmtryData {
    this.matchCmtryDataUpdate = {};
    this.matchCmtryDataUpdate.feed = cmtryUpdate.incident.feed;
    this.matchCmtryDataUpdate.matchCmtryEventId = cmtryUpdate.incident.eventId;
    this.matchCmtryDataUpdate.varIconData = null;
    if (cmtryUpdate.incident.type.description && MATCH_TIME_CONFIG[cmtryUpdate.incident.type.description]) {
      this.matchCmtryDataUpdate.matchfact = MATCH_TIME_CONFIG[cmtryUpdate.incident.type.description];
      this.matchCmtryDataUpdate.teamName = null;
      this.matchCmtryDataUpdate.playerName = null;
      return this.matchCmtryDataUpdate;
    }
    else {
      this.matchCmtryDataUpdate.matchfact = cmtryUpdate.incident.type.description && ALTERD_MATCHFACTS[cmtryUpdate.incident.type.description] ? ALTERD_MATCHFACTS[cmtryUpdate.incident.type.description] : cmtryUpdate.incident.type.description;
      this.matchCmtryDataUpdate.teamName = cmtryUpdate.incident.context?.teamName !== betLegConstants.NA && cmtryUpdate.incident.context?.teamName;
      if (cmtryUpdate.incident.feed === betLegConstants.OPTA) {
        this.matchCmtryDataUpdate.playerName = cmtryUpdate.incident.context?.playerName !== betLegConstants.NA && cmtryUpdate.incident.context?.playerName;
      }
      UNIQUE_TEMPLATE[cmtryUpdate.incident.type.code] && this.getAddtionalFactData(cmtryUpdate);
      return this.matchCmtryDataUpdate;
    }
  } 
  /**
   * Remove all subscription after failed connection and re-init again
   */
  reconnect(): void {
    this.liveServConnectionService.connect().subscribe((connection: ISocketIO) => {
      const uniqueChannels: string[] = this.channels.filter((channel, index) => this.channels.indexOf(channel) === index);
      this.channels.forEach(ch => this.unsubscribeForMatchCmtryUpdates(ch));
      uniqueChannels.forEach(channel => {
        this.liveServConnectionService.subscribeToMatchCommentary(cashoutConstants.channelName.facts + channel, this.callbacks.handler);
      });
      this.updateConnection(connection);
    });
  }
  /**
  * Unsubscribe from list of channels
  * @param channel - eventId
  */
  unsubscribeForMatchCmtryUpdates(channel: string): void {
    this.liveServConnectionService.unsubscribeFromMatchCommentary(cashoutConstants.channelName.facts + channel, this.callbacks.handler);
  }
  /**
   * remove all the handler for sendrequestforlastCode
   * @param channels 
   */
  removeHandlers(channels:string[]):void{
    channels.forEach((channel:string)=>{
      this.liveServConnectionService.removeAllEventListner([channel]);
    });
  }
  /**
   *
   * @param {Object} connection - socket connection to Live serve
   * @private
   */
  private updateConnection(connection: ISocketIO): void {
    if (this.isConnectionValid(connection)) {
      this.connection = connection;
      this.setDisconnectHandler();
    }
  }

  /**
   * Check if connection is connected and connection is not duplicated
   * @param {Object} connection
   * @return {boolean}
   * @private
   */
  private isConnectionValid(connection: ISocketIO): boolean {
    return connection && connection.connected && (!this.connection || this.connection.id !== connection.id);
  }

  /**
   * Set disconnect listener only for new socket connections or re-established socket connections
   */
  private setDisconnectHandler(): void {
    this.liveServConnectionService.onDisconnect(this.disconnectHandler);
  }

  /**
   * Handle server disconnect and then reestablish the connection
   */
  private disconnectHandler(error: string): void {
    if (this.liveServConnectionService.isDisconnected(error)) {
      this.reconnect();
    }
  }
  /**
   * will get the additional data for match facts
   * @param cmtryUpdate 
   * @returns matchcommentryupdate
   */
  private getAddtionalFactData(cmtryUpdate: IMatchCommentaryStatsUpdate): IMatchCmtryData {
    this.matchCmtryDataUpdate.matchfact = UNIQUE_TEMPLATE[cmtryUpdate.incident.type.code];
    switch (cmtryUpdate.incident.type.code) {
      case 215: {
        if (cmtryUpdate.incident.context?.playerOnName && cmtryUpdate.incident.context.playerOffName) {
          this.matchCmtryDataUpdate.playerName = null;
          this.matchCmtryDataUpdate.playerOnName = cmtryUpdate.incident.context.playerOnName;
          this.matchCmtryDataUpdate.playerOffName = cmtryUpdate.incident.context.playerOffName;
        }
        return this.matchCmtryDataUpdate;
      }
      case 103: {
        if (cmtryUpdate.incident.clock) {
          this.matchCmtryDataUpdate.clock = cmtryUpdate.incident.clock;
        }
        return this.matchCmtryDataUpdate;
      }
      case 102: {
        if (cmtryUpdate.incident.context?.minutes) {
          this.matchCmtryDataUpdate.playerName = null;
          this.matchCmtryDataUpdate.teamName = null;
          this.matchCmtryDataUpdate.minutes = cmtryUpdate.incident.context.minutes;
        }
        return this.matchCmtryDataUpdate;
      }
      case 200: {
        cmtryUpdate.incident.feed === betLegConstants.OPTA ?  this.matchCmtryDataUpdate.playerName = null :   this.matchCmtryDataUpdate.teamName = null;
        return this.matchCmtryDataUpdate;
      }
    }
  }
  /**
   * process the update and form the matchCmtryUpdate
   * @param cmtryUpdate 
   */
  private matchCommentryUpdateHandler(cmtryUpdate: IMatchCommentaryStatsUpdate) {
    // assign VAR related object
    if (cmtryUpdate?.incident?.type?.code === betLegConstants.varCode && cmtryUpdate.incident.context?.reasonId && varReasonId_config[cmtryUpdate.incident.context.reasonId]) {
      this.varIconData = varReasonId_config[cmtryUpdate.incident.context.reasonId];
      this.matchCmtryDataUpdate.matchCmtryEventId = cmtryUpdate.incident.eventId;
      this.matchCmtryDataUpdate.varIconData = this.varIconData;
      this.matchCmtryDataUpdate.teamName = cmtryUpdate.incident.context.teamName;
      this.matchCmtryDataUpdate.playerName = cmtryUpdate.incident.context.playerName;
      this.pubSubService.publish(this.pubSubService.API.UPDATE_MATCHCOMMENTARY_DATA, this.matchCmtryDataUpdate);
    }
    else {
      // assign Matchfacts data
      if (cmtryUpdate?.incident?.type?.code && cmtryUpdate.incident.type.code !== betLegConstants.varCode && cmtryUpdate.incident.feed) {
        this.matchCmtryDataUpdate = this.getMatchFactData(cmtryUpdate);
        this.pubSubService.publish(this.pubSubService.API.UPDATE_MATCHCOMMENTARY_DATA, this.matchCmtryDataUpdate);
      }
    }
  }
}
