import { Injectable } from '@angular/core';
import { GlobalLoaderService } from '../../shared/globalLoader/loader.service';
import { ApiClientService } from '../../client/private/services/http/index';
import 'rxjs/add/operator/catch';
import { HttpErrorResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/observable/throw';
import { Game } from '../../client/private/models/game.model';
import { EventScore } from '@app/client/private/models/eventScore.model';

@Injectable()
export class GameAPIService {
  constructor(
    private globalLoaderService: GlobalLoaderService,
    private apiClientService: ApiClientService
  ) {
  }

  /**
   * Wrap request to handle success/error.
   * @param observableDate
   */
  wrappedObservable(observableDate) {
    return observableDate
      .map(res => {
        this.globalLoaderService.hideLoader();
        return res;
      })
      .catch(response => {
        if (response instanceof HttpErrorResponse) {
          this.handleRequestError(response.error);
        }

        return Observable.throw(response);
      });
  }

  getGamesData(showLoader: boolean = true) {
    if (showLoader) {
      this.globalLoaderService.showLoader();
    }
    const getData =  this.apiClientService.gamesService().getGames();
    return this.wrappedObservable(getData);
  }

  postNewGame(newGame: Game) {
    this.globalLoaderService.showLoader();
    const getData = this.apiClientService.gamesService().postNewGame(newGame);
    return this.wrappedObservable(getData);
  }

  deleteGame(id: string) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.gamesService().deleteGame(id);
    return this.wrappedObservable(getData);
  }

  getSingleGamesData(id: string) {
    const getData =  this.apiClientService.gamesService().getSingleGame(id);
    return this.wrappedObservable(getData);
  }

  putGamesChanges(game: Game) {
    this.globalLoaderService.showLoader();
    const getData = this.apiClientService.gamesService().putGameChanges(game.id, game);
    return this.wrappedObservable(getData);
  }

  getEventById(eventId: string) {
    const getData = this.apiClientService.eventsService().getEvent(eventId);
    return this.wrappedObservable(getData);
  }

  handleRequestError(error) {
    this.globalLoaderService.hideLoader();
  }

  hideLoader() {
    this.globalLoaderService.hideLoader();
  }

  uploadImage(id: string, eventId: string, teamType: string, fileName: string, file: FormData) {
    this.globalLoaderService.showLoader();
    fileName = fileName.replace(' ', '_');
    const uploadedImage = this.apiClientService.gamesService().uploadImage(id, eventId, teamType, fileName, file);
    return this.wrappedObservable(uploadedImage);
  }

  deleteImage(id: string, eventId: string, teamType: string) {
    this.globalLoaderService.showLoader();
    const getData = this.apiClientService.gamesService().deleteImage(id, eventId, teamType);
    return this.wrappedObservable(getData);
  }

  saveScore(id: string, score: EventScore) {
    this.globalLoaderService.showLoader();
    const getData = this.apiClientService.gamesService().postScore(id, score);
    return this.wrappedObservable(getData);
  }

  getScore(eventId: string) {
    this.globalLoaderService.showLoader();
    const getData = this.apiClientService.gamesService().getScore(eventId);
    return this.wrappedObservable(getData);
  }
}
