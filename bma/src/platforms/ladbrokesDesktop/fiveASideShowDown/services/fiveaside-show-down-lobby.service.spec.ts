import { FiveASideShowDownLobbyService } from './fiveaside-show-down-lobby.service';

describe('FiveASideShowDownLobbyService', () => {
  let service: FiveASideShowDownLobbyService;

  beforeEach(() => {
    service = new FiveASideShowDownLobbyService();
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });
});
