import { Injectable } from '@angular/core';
import { UserService } from '@core/services/user/user.service';

@Injectable()
export class ProxyHeadersService {
  private token: string;

  constructor(private user: UserService) {
    this.token = '';
  }

  /**
   * Generate headers for BPP Api calls.
   */
  generateBppAuthHeaders(): string | null {
    if (this.user.bppToken) {
      this.token = this.user.bppToken;
    } else {
      this.token = '';
    }
    return this.token;
  }
}
